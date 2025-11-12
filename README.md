# CGCNN: Crystal Graph Convolutional Neural Network

A PyTorch implementation of Crystal Graph Convolutional Neural Networks for predicting material properties from crystal structures. This project uses graph-based deep learning to model atomic interactions in crystalline materials.

## 🔬 Features

- **Graph-based Learning**: Converts crystal structures (CIF files) to graphs with atoms as nodes and bonds as edges
- **Atom Embeddings**: Custom JSON-based atom feature initialization
- **Materials Project Integration**: Download and process crystal structures from Materials Project database
- **Interactive Notebooks**: Step-by-step Jupyter notebooks for data processing, model training, and visualization
- **Modern Python Tooling**: Uses `uv` for fast, reliable dependency management

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

```text
cgcnn/
├── pyproject.toml              # Project dependencies and configuration
├── uv.lock                     # Locked dependency versions
├── README.md                   # This file
├── .gitignore                  # Git ignore patterns
├── atom_init.json              # Atom initialization config
│
├── data/                       # Data directory (excluded from git)
│   ├── atom_embed_config.json  # Atom embedding configuration
│   ├── atom_embedding.json     # Pre-computed atom embeddings
│   ├── elements.json           # Periodic table data
│   ├── cgcnn_dataset.csv       # Dataset with material properties
│   ├── mp-ids-27430.csv        # Materials Project IDs
│   └── cif/                    # Crystal structure files (CIF format)
│       ├── mp-1.cif
│       ├── mp-1000.cif
│       └── ...
│
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── 01_atom_embeddings.ipynb      # Generate atom embeddings
│   ├── 02_data_download.ipynb        # Download Materials Project data
│   ├── 03_graph_visualization.ipynb  # Visualize crystal graphs
│   ├── 04_cgcnn_data_loading.ipynb   # Dataset loading and preprocessing
│   ├── 05_cgcnn_model.ipynb          # CGCNN model architecture
│   ├── **06_cgcnn_training.ipynb**       # complete Model training and evaluation (Main)
│   └── training_results/             # Training outputs and checkpoints
│
└── setup_and_uv/               # Setup and utility scripts
    ├── example.py              # Example Python script
    ├── quick_test.py           # Quick environment test
    ├── test_environment.py     # Full environment test
    └── UV_GUIDE.md             # UV package manager guide
```

---

## 📚 Notebooks Workflow

Follow the notebooks in order for the complete pipeline:

1. **01_atom_embeddings.ipynb** - Generate atom feature embeddings from periodic table data
2. **02_data_download.ipynb** - Download crystal structures from Materials Project API
3. **03_graph_visualization.ipynb** - Visualize crystal structures as graphs
4. **04_cgcnn_data_loading.ipynb** - Load and preprocess CIF files into graph datasets
5. **05_cgcnn_model.ipynb** - Define CGCNN model architecture
6. **06_cgcnn_training.ipynb** - Train model and evaluate performance

## 🛠️ Troubleshooting

| Issue                        | Solution                                     |
| ---------------------------- | -------------------------------------------- |
| Kernel not showing           | `Ctrl+Shift+P` → "Developer: Reload Window"  |
| Package missing              | `uv sync`                                    |
| Complete reset               | `Remove-Item -Recurse -Force .venv; uv sync` |
| CIF files not found          | Check `data/cif/` directory exists           |
| atom_embedding.json error    | Ensure file exists in `data/` directory      |
| Materials Project API issues | Set `MP_API` environment variable            |

---

## 📝 Notes

- **Data files are excluded from git**: The `data/` and `cif/` directories are in `.gitignore` to avoid committing large datasets
- **Virtual environment**: The `.venv/` directory is auto-generated by `uv sync` and excluded from git
- **Setup scripts**: PowerShell scripts in the root are for initial project setup and are excluded from git

---
