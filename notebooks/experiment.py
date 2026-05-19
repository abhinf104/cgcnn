import os, json, csv, random, functools, time, argparse, shutil, sys
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from torch.utils.data import Dataset, DataLoader, Subset
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import Element
from tqdm import tqdm

# Settings
M_NBR, RAD, DMIN, DSTEP = 12, 8.0, 0.0, 0.2
BS, F_LEN, N_CONV, H_LEN = 32, 64, 3, 128
LR, EPOCHS = 1e-2, 20
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BASE_CFG = {
    "Z": {"use": True, "type": "onehot", "size": 119},
    "group": {"use": True, "type": "onehot", "size": 19},
    "period": {"use": True, "type": "onehot", "size": 8},
    "block": {"use": True, "type": "onehot", "categories": ["s", "p", "d", "f"]},
    "covalent_radius": {"use": True, "type": "gaussian", "bins": 32, "range": "auto"},
    "pauling_electronegativity": {"use": True, "type": "gaussian", "bins": 32, "range": "auto"},
    "first_ionization_energy": {"use": True, "type": "gaussian", "bins": 32, "range": "auto"},
    "valence_s": {"use": True, "type": "linear"},
    "valence_p": {"use": True, "type": "linear"},
    "valence_d": {"use": True, "type": "linear"},
    "valence_f": {"use": True, "type": "linear"},
}

ABLATIONS = [
    ("A1_orig", "Baseline", "USE_UPSTREAM"),
    ("A2_full", "Full", json.loads(json.dumps(BASE_CFG))),
    ("D_no_period", "No Period", {k: {**v, "use": k != "period"} for k, v in BASE_CFG.items()}),
    ("E_min", "Minimal", {k: {**v, "use": k in ["Z", "valence_s", "valence_p", "valence_d", "valence_f"]} for k, v in BASE_CFG.items()}),
]

class GDist:
    def __init__(self, dmin, dmax, step, var=None):
        self.f = np.arange(dmin, dmax+step, step)
        self.v = var or step
    def expand(self, d): return np.exp(-(d[..., np.newaxis] - self.f)**2 / self.v**2)

class AtomInit:
    def __init__(self, f):
        with open(f) as fp: raw = json.load(fp)
        e = raw.get("embeddings", raw)
        self.emb = { (int(k) if str(k).isdigit() else Element(k).Z): np.array(v, dtype=float) for k, v in e.items() }
    def get_fea(self, z): return self.emb[int(z)]

class CifD(Dataset):
    def __init__(self, root, csv_f, ari, gdf):
        self.root, self.ari, self.gdf = Path(root), ari, gdf
        df = pd.read_csv(self.root / csv_f)
        id_c = [c for c in ["material_id", "cif_id", "id"] if c in df.columns][0]
        tgt_c = "formation_energy_per_atom" if "formation_energy_per_atom" in df.columns else df.columns[1]
        self.data = [(str(row[id_c]), float(row[tgt_c])) for _, row in df.iterrows()]
    def __len__(self): return len(self.data)
    @functools.lru_cache(maxsize=1024)
    def __getitem__(self, i):
        cid, t = self.data[i]
        p = self.root / "cif" / f"{cid}.cif"
        c = Structure.from_file(str(p))
        fea = torch.tensor(np.vstack([self.ari.get_fea(c[j].specie.number) for j in range(len(c))]), dtype=torch.float32)
        nbrs = [sorted(n, key=lambda x: x[1]) for n in c.get_all_neighbors(RAD, include_index=True)]
        ni, nf = [], []
        for n in nbrs:
            if len(n) < M_NBR:
                ni.append([x[2] for x in n] + [0]*(M_NBR-len(n)))
                nf.append([x[1] for x in n] + [RAD+1.0]*(M_NBR-len(n)))
            else:
                ni.append([x[2] for x in n[:M_NBR]])
                nf.append([x[1] for x in n[:M_NBR]])
        return (fea, torch.tensor(self.gdf.expand(np.array(nf)), dtype=torch.float32), torch.tensor(ni, dtype=torch.long)), torch.tensor([t], dtype=torch.float32), cid

def coll(smpl):
    b_f, b_nf, b_ni, idxs, b_t, b_ids = [], [], [], [], [], []
    base = 0
    for (f, nf, ni), t, cid in smpl:
        n = f.shape[0]
        b_f.append(f); b_nf.append(nf); b_ni.append(ni+base)
        idxs.append(torch.arange(n) + base)
        b_t.append(t); b_ids.append(cid)
        base += n
    return (torch.cat(b_f, 0), torch.cat(b_nf, 0), torch.cat(b_ni, 0), idxs), torch.stack(b_t, 0), b_ids

class Norm:
    def __init__(self, t): self.m, self.s = t.mean(), t.std() or 1.0
    def n(self, t): return (t - self.m.to(t.device)) / self.s.to(t.device)
    def d(self, t): return t * self.s.to(t.device) + self.m.to(t.device)

class Conv(nn.Module):
    def __init__(self, fl, nfl):
        super().__init__()
        self.fc = nn.Linear(2*fl+nfl, 2*fl)
        self.bn1, self.bn2 = nn.BatchNorm1d(2*fl), nn.BatchNorm1d(fl)
    def forward(self, f, nf, ni):
        N, M = ni.shape
        z = self.fc(torch.cat([f.unsqueeze(1).expand(N, M, -1), f[ni, :], nf], 2))
        z = self.bn1(z.view(-1, 2*f.shape[1])).view(N, M, -1)
        gate, core = z.chunk(2, 2)
        msg = torch.sum(torch.sigmoid(gate) * F.softplus(core), 1)
        return F.softplus(f + self.bn2(msg))

class Net(nn.Module):
    def __init__(self, inf, nfl):
        super().__init__()
        self.emb = nn.Linear(inf, F_LEN)
        self.convs = nn.ModuleList([Conv(F_LEN, nfl) for _ in range(N_CONV)])
        self.fc = nn.Linear(F_LEN, H_LEN)
        self.out = nn.Linear(H_LEN, 1)
    def forward(self, f, nf, ni, c_idx):
        f = self.emb(f)
        for c in self.convs: f = c(f, nf, ni)
        p = torch.cat([f[i].mean(0, True) for i in c_idx], 0)
        return self.out(F.softplus(self.fc(p)))

def run_ep(m, ldr, nrm, opt=None):
    m.train() if opt else m.eval()
    losses, preds, targs = [], [], []
    with (torch.enable_grad() if opt else torch.no_grad()):
        for data, t, _ in tqdm(ldr, leave=False):
            f, nf, ni, c_idx = [x.to(DEV) if torch.is_tensor(x) else x for x in data]
            t = t.to(DEV)
            on = m(f, nf, ni, c_idx)
            loss = F.mse_loss(on, nrm.n(t))
            if opt: opt.zero_grad(); loss.backward(); opt.step()
            losses.append(loss.item() * t.size(0))
            preds.extend(nrm.d(on).cpu().numpy().flatten())
            targs.extend(t.cpu().numpy().flatten())
    return np.sum(losses)/len(ldr.dataset), mean_absolute_error(targs, preds), preds, targs

def build_emb(el_f, cfg, out_f):
    with open(el_f) as f: el = json.load(f)
    if isinstance(el, list): el = {x["symbol"]: x for x in el}
    auto = {}
    for k, s in cfg.items():
        if s.get("use") and s.get("type") == "gaussian" and s.get("range") == "auto":
            vals = [float(p[k]) for p in el.values() if p.get(k) is not None]
            auto[k] = (min(vals), max(vals)) if vals else (0, 1)
    embs = {}
    for s, p in el.items():
        v = []
        for k, sc in cfg.items():
            if not sc.get("use"): continue
            val = p.get(k)
            if sc["type"] == "onehot":
                tmp = [0.]*(len(sc["categories"]) if sc.get("categories") else int(sc["size"]))
                if sc.get("categories"):
                    if val in sc["categories"]: tmp[sc["categories"].index(val)] = 1.
                else:
                    try: 
                        if 0 <= int(val) < len(tmp): tmp[int(val)] = 1.
                    except: pass
                v.extend(tmp)
            elif sc["type"] == "gaussian":
                lo, hi = auto[k] if sc.get("range") == "auto" else (sc["min"], sc["max"])
                bins = sc["bins"]
                v.extend(np.exp(-(float(val or 0) - np.linspace(lo, hi, bins))**2 / (2 * ((hi-lo)/bins)**2)))
            elif sc["type"] == "linear": v.append(float(val or 0))
        embs[s] = list(v)
    with open(out_f, "w") as f: json.dump(embs, f)
    return len(next(iter(embs.values())))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", default="13")
    p.add_argument("--epochs", type=int, default=EPOCHS)
    args = p.parse_args()
    
    root = Path("../data").resolve()
    out = Path("training_results/ablation").resolve()
    out.mkdir(parents=True, exist_ok=True)
    seeds = [int(s) for s in args.seeds.split(",")]
    
    csv_f = "cgcnn_dataset_10k.csv" if (root / "cgcnn_dataset_10k.csv").exists() else "cgcnn_dataset.csv"
    spl_f = root / ("cgcnn_split_10k.json" if "10k" in csv_f else "cgcnn_split_full.json")
    with open(spl_f) as f: spl = json.load(f)
    
    res = []
    gdf = GDist(DMIN, RAD, DSTEP)
    
    for aid, lbl, cfg in ABLATIONS:
        if cfg == "USE_UPSTREAM": e_dim = 92; shutil.copy2(root / "atom_init.json", root / "atom_embedding.json")
        else: e_dim = build_emb(root / "elements.json", cfg, root / "atom_embedding.json")
        
        ari = AtomInit(root / "atom_embedding.json")
        ds = CifD(root, csv_f, ari, gdf)
        common = {"batch_size": BS, "collate_fn": coll, "num_workers": 0}
        tr_l = DataLoader(Subset(ds, spl["train"]), shuffle=True, **common)
        v_l = DataLoader(Subset(ds, spl["val"]), **common)
        te_l = DataLoader(Subset(ds, spl["test"]), **common)
        
        for s in seeds:
            random.seed(s); np.random.seed(s); torch.manual_seed(s)
            (f0, nf0, ni0), _, _ = ds[0]
            m = Net(f0.shape[1], nf0.shape[-1]).to(DEV)
            nrm = Norm(torch.tensor([ds.data[i][1] for i in spl["train"][:500]]))
            opt = optim.Adam(m.parameters(), lr=LR)
            sch = ReduceLROnPlateau(opt, 'min', factor=0.5, patience=5)
            best = float('inf')
            
            for ep in range(args.epochs):
                tl, tm, p, t = run_ep(m, tr_l, nrm, opt)
                vl, vm, p, t = run_ep(m, v_l, nrm)
                sch.step(vl)
                if vl < best: best = vl; torch.save(m.state_dict(), out / f"{aid}_s{s}.pth")
                print(f"{aid} s{s} Ep {ep+1} | Tr MAE: {tm:.4f} | Vl MAE: {vm:.4f}")
            
            m.load_state_dict(torch.load(out / f"{aid}_s{s}.pth"))
            _, tm, p, t = run_ep(m, te_l, nrm)
            res.append({"id": aid, "seed": s, "mae": tm, "r2": r2_score(t, p)})
            pd.DataFrame(res).to_csv(out / "results.csv", index=False)
    print("\nFinal Results saved to", out / "results.csv")

if __name__ == "__main__": main()
