# CGCNN Project Guide

## 🚀 Quick Start

### Setup (First Time Only)
```powershell
.\setup_environment.ps1
```

### Commands

| Task | Command |
|------|---------|
| Run Python file | `uv run python file.py` |
| Test environment | `uv run python setup_and_uv/test_environment.py` |
| Start Jupyter | `uv run jupyter lab` |
| Add package | `uv add package-name` |
| Sync dependencies | `uv sync` |

### Run Jupyter Notebooks
1. Open `GNN3.ipynb` in VS Code
2. Click **"Select Kernel"** → Choose **"Python (cgcnn)"**
3. Press `Shift+Enter` to run cells

---

## � Troubleshooting

| Issue | Solution |
|-------|----------|
| Kernel not showing | `Ctrl+Shift+P` → "Developer: Reload Window" |
| Package missing | `uv sync` |
| Complete reset | `.\setup_environment.ps1` |

---

## 📁 Project Files

- `GNN3.ipynb` - Main notebook
- `atom_init.json` - Atomic properties
- `pyproject.toml` - Dependencies
- `setup_environment.ps1` - Setup script
- `setup_and_uv/` - Testing utilities
