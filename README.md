# CGCNN: Crystal Graph Convolutional Neural Network

## 🚀 Quick Start

### 1. Environment Setup (First Time Only)

```powershell
cd C:/Users/abhin/Desktop/cgcnn
uv sync
```

### 2. Running Python Scripts

```powershell
# Run a script (recommended)
uv run python setup_and_uv/example.py
uv run python setup_and_uv/quick_test.py

# Or activate the virtual environment manually
.venv/Scripts/activate
python setup_and_uv/example.py
deactivate
```

### 3. Running Jupyter Notebooks

```powershell
uv run jupyter lab

uv run jupyter notebook

uv run jupyter execute GNN.ipynb
uv run jupyter execute notebooks/01_atom_embeddings.ipynb
```

### 4. Adding New Dependencies

```powershell
uv add <package-name>
# This will:
# 1. Install the package
# 2. Update pyproject.toml
# 3. Update uv.lock
```

### 5. Using Materials Project API

```powershell
$env:MP_API = "your_api_key_here"
uv run python your_script.py

# Or Create a .env file (persistent)
echo "MP_API=your_api_key_here" > .env
# In your Python code:
# from dotenv import load_dotenv
# load_dotenv()
```

---

## 📁 Project Structure

cgcnn/
├── pyproject.toml
├── README.md
├── create_structure.ps1
├── setup_environment.ps1
├── data/ # Data files
│ ├── atom_embed_config.json
│ ├── atom_embedding.json
│ ├── elements.json
│ └── mp-ids-27430.csv # Materials Project IDs
├── notebooks
│ ├── 01_atom_embeddings.ipynb # Atom embeddings notebook
│ ├── 02_graph_building.ipynb # Graph building notebook
│ ├── 03_graph_visualization.ipynb# Graph visualization notebook
│ ├── atom_embed_config.json # Atom embedding
config (notebook copy)
(notebook copy)
└── setup_and_uv/ # Setup and utility scripts
├── example.py # Example Python script
├── quick_test.py # Quick test script
├── test_environment.py # Environment test script
└── UV_GUIDE.md # UV and environment guide

---

## 🛠️ Troubleshooting

| Issue              | Solution                                     |
| ------------------ | -------------------------------------------- |
| Kernel not showing | `Ctrl+Shift+P` → "Developer: Reload Window"  |
| Package missing    | `uv sync`                                    |
| Complete reset     | `Remove-Item -Recurse -Force .venv; uv sync` |

---
