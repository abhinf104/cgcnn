# CGCNN Environment Setup Script
# Run this once to configure everything

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 CGCNN Environment Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Step 1: Check UV
Write-Host "`n[1/6] Checking UV installation..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version
    Write-Host "✅ UV is installed: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ UV is not installed!" -ForegroundColor Red
    Write-Host "Install from: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    exit 1
}

# Step 2: Sync dependencies
Write-Host "`n[2/6] Syncing dependencies from pyproject.toml..." -ForegroundColor Yellow
uv sync
Write-Host "✅ Dependencies synced" -ForegroundColor Green

# Step 3: Register Jupyter kernels
Write-Host "`n[3/6] Registering Jupyter kernels..." -ForegroundColor Yellow
uv run python -m ipykernel install --user --name=cgcnn --display-name="Python (cgcnn)"
uv run python -m ipykernel install --prefix=.venv --name=python3 --display-name="Python 3 (cgcnn venv)"
Write-Host "✅ Jupyter kernels registered" -ForegroundColor Green

# Step 4: List available kernels
Write-Host "`n[4/6] Available Jupyter kernels:" -ForegroundColor Yellow
uv run jupyter kernelspec list

# Step 5: Test environment
Write-Host "`n[5/6] Testing Python environment..." -ForegroundColor Yellow
uv run python test_environment.py

# Step 6: Check execution policy
Write-Host "`n[6/6] Checking PowerShell execution policy..." -ForegroundColor Yellow
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "RemoteSigned" -or $policy -eq "Unrestricted") {
    Write-Host "✅ Execution policy is set: $policy" -ForegroundColor Green
} else {
    Write-Host "⚠️  Current policy: $policy" -ForegroundColor Yellow
    Write-Host "Setting execution policy to RemoteSigned..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✅ Execution policy updated" -ForegroundColor Green
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Reload VS Code: Ctrl+Shift+P → 'Developer: Reload Window'"
Write-Host "   2. Open GNN3.ipynb"
Write-Host "   3. Click 'Select Kernel' (top-right)"
Write-Host "   4. Choose 'Python (cgcnn)' or 'Python 3 (cgcnn venv)'"
Write-Host ""
Write-Host "🚀 Quick Commands:" -ForegroundColor Yellow
Write-Host "   • Run Python file:    uv run python your_file.py"
Write-Host "   • Run with .venv:     .\.venv\Scripts\python.exe your_file.py"
Write-Host "   • Start Jupyter:      uv run jupyter lab"
Write-Host "   • Test environment:   uv run python test_environment.py"
Write-Host ""

# PyTorch warning if needed
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  PyTorch Issue Detected:" -ForegroundColor Yellow
    Write-Host "   Install Visual C++ Redistributable:"
    Write-Host "   https://aka.ms/vs/17/release/vc_redist.x64.exe" -ForegroundColor Cyan
    Write-Host "   Then restart your computer.`n"
}

Write-Host ("=" * 70) -ForegroundColor Cyan
