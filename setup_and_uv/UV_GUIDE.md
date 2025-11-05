# UV Virtual Environment Guide for CGCNN Project

## What is UV?

`uv` is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for `pip` and `pip-tools`, but with significantly better performance.

## Installing UV

If you see "CommandNotFoundException" for `uv` (for example when running `uv venv`), it means the `uv` command-line tool isn't installed or isn't available on your PATH. Install it using one of these approaches (PowerShell):

```powershell
# Or install directly into the current Python environment
python -m pip install --upgrade pip
python -m pip install uv
```

After installation open a new terminal (so PATH changes apply) and verify:

```powershell
uv --version
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

### Important: uv add vs pip install

**`uv add` (Recommended)**:

- Adds package to `pyproject.toml`
- Creates/updates `uv.lock` file
- Ensures reproducible builds
- Manages dependencies properly

**`pip install` (Use only for troubleshooting)**:

- Installs directly to environment
- Doesn't update `pyproject.toml`
- Can cause dependency conflicts
- Not reproducible

**When to use pip install**: Only when `uv add` fails and you're troubleshooting (like we did with the Python 3.14/spglib issue).

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

# Activate the virtual environment (PowerShell)
# You can use the PowerShell activation script:
.\.venv\Scripts\Activate.ps1

# If you prefer cmd.exe activation (or are using a cmd terminal):
.venv\Scripts\activate

# Deactivate
deactivate
```

## Your CGCNN Project Setup

### Current Project Structure

```
c:\Users\abhin\Desktop\cgcnn\
├── pyproject.toml          # Project configuration
├── README.md               # Project documentation
├── GNN.ipynb              # Main GNN notebook
├── atom_init.json         # Atom initialization data
├── create_structure.ps1    # PowerShell script for structure creation
├── setup_environment.ps1   # PowerShell script for environment setup
├── data/                   # Data directory
│   ├── atom_init.json      # Atom initialization data (duplicate)
│   └── mp-ids-27430.csv    # Materials Project IDs
├── notebooks/              # Jupyter notebooks directory
│   ├── 01_atom_embeddings.ipynb    # Atom embeddings notebook
│   ├── 02_graph_building.ipynb     # Graph building notebook
│   ├── 03_graph_visualization.ipynb # Graph visualization notebook
│   ├── atom_embed_config.json      # Atom embedding configuration
│   ├── atom_embedding.json         # Atom embedding data
│   ├── elements.json               # Elements data
│   ├── graph_dataset.pt            # PyTorch graph dataset
│   ├── mp_training_data.json       # Materials Project training data
│   └── mp-ids-27430.csv            # Materials Project IDs (duplicate)
└── setup_and_uv/           # Setup and UV utilities
    ├── example.py           # Example Python script
    ├── quick_test.py        # Quick test script
    ├── test_environment.py  # Environment testing script
    └── UV_GUIDE.md          # This guide
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
cd C:\Users\abhin\Desktop\cgcnn

# Sync dependencies from pyproject.toml
uv sync

# This creates .venv and installs all dependencies
```

### 2. Running Python Scripts

```powershell
# Option 1: Use uv run (recommended - no activation needed)
uv run setup_and_uv\example.py
uv run python setup_and_uv\my_script.py

# Option 2: Activate virtual environment first
.venv\Scripts\activate
python setup_and_uv\example.py
deactivate
```

### 3. Running Jupyter Notebooks

```powershell
# Start Jupyter Lab
uv run jupyter lab

# Or start classic Notebook
uv run jupyter notebook

# Run a specific notebook from command line
uv run jupyter execute GNN.ipynb
uv run jupyter execute notebooks\01_atom_embeddings.ipynb
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

### Issue 5: Building Packages from Source (spglib, etc.)

**Problem**: `Failed to build 'spglib==2.6.0'` with errors like:

```
CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
*** CMake configuration failed
```

**Cause**: Some packages (like `spglib`) require compilation from source and need:

- CMake
- A C/C++ compiler (MSVC/Visual Studio Build Tools or MinGW)
- Python version with pre-built wheels available

**Solutions** (in order of preference):

**Option A: Use Python 3.12 (Recommended - Best Package Support)**

Python 3.14 is very new and many packages don't have pre-built wheels yet. Python 3.12 has the best ecosystem support:

```powershell
# Install Python 3.12 (if not already installed)
py install 3.12

# Remove old venv
Remove-Item -Recurse -Force .venv

# Create new venv with Python 3.12
py -3.12 -m venv .venv

# Install dependencies
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pymatgen ase torch jupyterlab mp-api notebook python-dotenv

# Or use uv with specific Python version
uv venv --python 3.12
uv sync
```

**Option B: Install Visual Studio Build Tools (If you need Python 3.14)**

Download and install Microsoft C++ Build Tools (requires ~6 GB, 15-20 min install):

1. Download: https://visualstudio.microsoft.com/downloads/
2. Scroll to "Tools for Visual Studio" → "Build Tools for Visual Studio 2022"
3. Install with "Desktop development with C++" workload
4. Restart terminal and run: `uv add pymatgen`

**Option C: Use conda/mamba (Alternative Package Manager)**

Conda provides pre-built binaries for scientific packages:

```powershell
# Install miniconda, then:
conda create -n cgcnn python=3.12
conda activate cgcnn
conda install -c conda-forge pymatgen ase pytorch jupyterlab
```

**Verification after fix:**

```powershell
# Test imports
.\.venv\Scripts\python.exe -c "import pymatgen; import spglib; print('✓ All packages working')"
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

### . Parallel Installation

````powershell
# UV installs packages in parallel automatically
# No special flags needed

### Issue: Adding user-local bin to PATH (PowerShell)

**Problem**: Running a command like

```powershell
$env:Path = "C:\Users\abhin\.local\bin;$env:Path"
````

can produce the error:

```
The filename, directory name, or volume label syntax is incorrect.
```

**Cause**: This usually indicates the value being written to PATH is malformed (contains invalid characters or incorrect quoting) or the tool used to persist the PATH (for example `setx`) was passed an incorrectly-expanded value. In PowerShell it's safer to build strings explicitly and verify the directory exists before updating PATH.

**Safe steps (PowerShell)**:

1. Create the directory if it doesn't exist:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\.local\bin" -Force
```

2. Add it to the current session PATH (temporary — only this terminal):

```powershell
$env:Path = "$($env:USERPROFILE)\.local\bin;" + $env:Path
# Verify it's present
$env:Path -split ';' | Select-String "$($env:USERPROFILE)\\.local\\bin"
```

3. Persist it for your user account (recommended method):

```powershell
uv sync  # Already parallelized
```

# After running the above, open a new PowerShell window to pick up the change.

````

Alternate (cmd-friendly) persist method using setx (be careful with length limits):

```powershell
# Note: setx is a separate program that expects %PATH% expansion; run from PowerShell like this:
cmd /c "setx PATH \"%USERPROFILE%\\.local\\bin;%PATH%\""

# Then open a new terminal session to see the change.
````

Notes:

- Prefer the `[Environment]::SetEnvironmentVariable(...,'User')` approach — it's explicit and avoids odd cmd/PowerShell quoting pitfalls.
- Restart any open terminals (or VS Code) after changing the user PATH so they pick up the new value.
- If you get the same error again, check for stray characters in your PATH (e.g. unpaired quotes or invalid % expansions) and run `echo $env:Path` to inspect it.

## Integration with VS Code

### 1. Select Python Interpreter

```
1. Ctrl+Shift+P → "Python: Select Interpreter"
2. Choose: C:\Users\abhin\Desktop\cgcnn\.venv\Scripts\python.exe
```

### 2. Integrated Terminal

```powershell
# VS Code terminal should automatically detect .venv
# If not, activate manually:
.venv\Scripts\activate
```

### 3. Run Configurations

Create `.vscode/launch.json`:

````json
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
```## Additional Resources

- **UV Documentation**: https://github.com/astral-sh/uv
- **Python Packaging**: https://packaging.python.org/
- **pyproject.toml Guide**: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/

## Summary

✅ **Use `uv run` to execute Python scripts** (no manual activation needed)
✅ **Use `uv add/remove` to manage packages** (auto-updates pyproject.toml)
✅ **Use `uv sync` to install dependencies** (from pyproject.toml)
✅ **Save files as UTF-8 without BOM** (avoid encoding errors)
✅ **Keep pyproject.toml in version control** (reproducible environment)
````
