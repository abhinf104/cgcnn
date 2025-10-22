# UV Virtual Environment Guide for CGCNN Project

## What is UV?

`uv` is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for `pip` and `pip-tools`, but with significantly better performance.

## Quick Reference

### Running Python Files

```powershell
# Run a Python file using uv (automatically manages virtual environment)
uv run example.py

# Run a Python script with arguments
uv run example.py --arg1 value1 --arg2 value2

# Run Python commands directly
uv run python -c "print('Hello World')"

# Run with specific Python version
uv run --python 3.12 example.py
```

### Managing Virtual Environments

```powershell
# Create a virtual environment (uv does this automatically, but you can do it manually)
uv venv

# Create with specific Python version
uv venv --python 3.12

# Activate the virtual environment (traditional way)
.venv\Scripts\activate

# Deactivate
deactivate
```

### Package Management

```powershell
# Install packages from pyproject.toml
uv sync

# Install a single package
uv add numpy

# Install a package with version constraint
uv add "torch>=2.0.0"

# Remove a package
uv remove package-name

# Update all packages
uv sync --upgrade

# Install development dependencies
uv sync --dev
```

### Project Commands

```powershell
# Initialize a new project
uv init

# Initialize with a specific name
uv init my-project

# Show installed packages
uv pip list

# Show package information
uv pip show numpy
```

## Your CGCNN Project Setup

### Current Project Structure

```
e:\cgcnn\
├── pyproject.toml          # Project configuration
├── example.py              # Example Python script
├── GNN3.ipynb             # Main notebook
├── GNN.ipynb              # Additional notebook
└── .venv\                 # Virtual environment (created by uv)
```

### Your Dependencies

Based on your `pyproject.toml`:

```toml
[project]
name = "cgcnn"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "ase>=3.26.0",
    "ipykernel>=7.0.1",
    "jupyterlab>=4.4.9",
    "matplotlib>=3.10.7",
    "mp-api>=0.45.12",
    "networkx>=3.4.2",
    "notebook>=7.4.7",
    "numpy>=2.2.6",
    "pymatgen>=2025.10.7",
    "torch>=2.9.0",
]
```

## Common Workflows

### 1. First Time Setup

```powershell
# Navigate to project directory
cd e:\cgcnn

# Sync dependencies from pyproject.toml
uv sync

# This creates .venv and installs all dependencies
```

### 2. Running Python Scripts

```powershell
# Option 1: Use uv run (recommended - no activation needed)
uv run example.py
uv run python my_script.py

# Option 2: Activate virtual environment first
.venv\Scripts\activate
python example.py
deactivate
```

### 3. Running Jupyter Notebooks

```powershell
# Start Jupyter Lab
uv run jupyter lab

# Or start classic Notebook
uv run jupyter notebook

# Run a specific notebook from command line
uv run jupyter execute GNN3.ipynb
```

### 4. Adding New Dependencies

```powershell
# Add a new package
uv add pandas

# This automatically:
# 1. Installs the package
# 2. Updates pyproject.toml
# 3. Creates/updates uv.lock
```

### 5. Working with Materials Project API

```powershell
# Your notebooks need MP_API key
# Option 1: Set environment variable
$env:MP_API = "your_api_key_here"
uv run python your_script.py

# Option 2: Create .env file
echo "MP_API=your_api_key_here" > .env

# Then load in Python:
# from dotenv import load_dotenv
# load_dotenv()
```

## Troubleshooting

### Issue 1: Encoding Errors (like you experienced)

**Problem**: `SyntaxError: Non-UTF-8 code starting with '\xff'`

**Cause**: File was saved with wrong encoding (UTF-16, UTF-16 LE with BOM)

**Solutions**:

```powershell
# Option 1: Recreate file with correct encoding
$content = Get-Content -Path "example.py" -Raw
[System.IO.File]::WriteAllText("example.py", $content, [System.Text.UTF8Encoding]::new($false))

# Option 2: Use VS Code to change encoding
# 1. Open file in VS Code
# 2. Bottom right corner, click encoding
# 3. Select "Save with Encoding"
# 4. Choose "UTF-8"

# Option 3: Add encoding declaration at top of file
# -*- coding: utf-8 -*-
```

### Issue 2: Virtual Environment Not Found

**Problem**: `uv run` can't find virtual environment

**Solution**:
```powershell
# Create it explicitly
uv venv

# Or sync from pyproject.toml
uv sync
```

### Issue 3: Package Conflicts

**Problem**: Dependency resolution errors

**Solution**:
```powershell
# Clear cache
uv cache clean

# Reinstall everything
Remove-Item -Recurse -Force .venv
uv sync
```

### Issue 4: Permission Errors

**Problem**: Can't create virtual environment

**Solution**:
```powershell
# Run PowerShell as Administrator
# Or check execution policy
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## UV vs Traditional Tools

### UV vs pip

```powershell
# Traditional pip
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install numpy

# UV equivalent
uv sync                    # Installs from pyproject.toml
uv add numpy              # Adds package and updates config
```

### UV vs conda

```powershell
# Conda
conda create -n cgcnn python=3.12
conda activate cgcnn
conda install numpy torch

# UV equivalent
uv venv --python 3.12
uv add numpy torch
uv run python script.py   # No manual activation needed
```

## Best Practices

### 1. Always Use `uv run` for Execution

```powershell
# ✅ Good - Consistent environment
uv run python example.py
uv run jupyter lab
uv run pytest

# ❌ Avoid - May use wrong Python
python example.py
jupyter lab
```

### 2. Keep pyproject.toml Updated

```powershell
# ✅ Good - Track dependencies
uv add new-package

# ❌ Avoid - Manual pip installs
pip install new-package
```

### 3. Use Lock File for Reproducibility

```powershell
# Generate lock file
uv lock

# Install exact versions from lock
uv sync --frozen

# Commit uv.lock to version control
git add uv.lock
```

### 4. Separate Dev Dependencies

```toml
# In pyproject.toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

```powershell
# Install dev dependencies
uv sync --extra dev
```

## Performance Tips

### 1. UV is Much Faster

```powershell
# UV can be 10-100x faster than pip
# Example timing:
# pip install torch: ~2 minutes
# uv add torch: ~10 seconds
```

### 2. Use UV Cache

```powershell
# UV caches packages automatically
# Location: C:\Users\<username>\AppData\Local\uv\cache

# View cache size
uv cache dir

# Clean if needed
uv cache clean
```

### 3. Parallel Installation

```powershell
# UV installs packages in parallel automatically
# No special flags needed
uv sync  # Already parallelized
```

## Integration with VS Code

### 1. Select Python Interpreter

```
1. Ctrl+Shift+P → "Python: Select Interpreter"
2. Choose: .\\.venv\Scripts\python.exe
```

### 2. Integrated Terminal

```powershell
# VS Code terminal should automatically detect .venv
# If not, activate manually:
.venv\Scripts\activate
```

### 3. Run Configurations

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File (UV)",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "python": "${workspaceFolder}\\.venv\\Scripts\\python.exe"
        }
    ]
}
```

## Useful UV Commands Cheat Sheet

```powershell
# Installation & Setup
uv venv                    # Create virtual environment
uv sync                    # Install dependencies from pyproject.toml

# Running Code
uv run <script>           # Run Python script
uv run python             # Start Python REPL
uv run --python 3.12      # Run with specific Python version

# Package Management
uv add <package>          # Add package
uv remove <package>       # Remove package
uv lock                   # Generate lock file
uv sync --upgrade         # Update all packages

# Information
uv pip list               # List installed packages
uv pip show <package>     # Show package info
uv version                # Show UV version
uv cache dir              # Show cache directory

# Troubleshooting
uv cache clean            # Clear cache
uv sync --reinstall       # Reinstall all packages
```

## Example: Complete Workflow

```powershell
# 1. Clone/navigate to project
cd e:\cgcnn

# 2. Setup environment
uv sync

# 3. Add Materials Project API key
$env:MP_API = "your_key_here"

# 4. Run analysis script
uv run python analysis.py

# 5. Start Jupyter for notebooks
uv run jupyter lab

# 6. Add new dependency if needed
uv add scikit-learn

# 7. Update pyproject.toml manually if needed
# (Edit file)
uv sync  # Apply changes

# 8. Run tests (if you have them)
uv run pytest

# 9. Export requirements (for compatibility)
uv pip freeze > requirements.txt
```

## Additional Resources

- **UV Documentation**: https://github.com/astral-sh/uv
- **Python Packaging**: https://packaging.python.org/
- **pyproject.toml Guide**: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/

## Summary

✅ **Use `uv run` to execute Python scripts** (no manual activation needed)  
✅ **Use `uv add/remove` to manage packages** (auto-updates pyproject.toml)  
✅ **Use `uv sync` to install dependencies** (from pyproject.toml)  
✅ **Save files as UTF-8 without BOM** (avoid encoding errors)  
✅ **Keep pyproject.toml in version control** (reproducible environment)

---

**Your specific fix for the encoding error:**

```powershell
# The issue was file encoding. Fixed by recreating as UTF-8:
$content = "print('Hello from UV!')"
[System.IO.File]::WriteAllText("example.py", $content, [System.Text.UTF8Encoding]::new($false))

# Then run:
uv run example.py
```
