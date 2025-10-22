# PowerShell Script to Create Project Structure

Write-Host "Creating project directories..." -ForegroundColor Yellow

# List of directories to create
$directories = @(
    "data/raw",
    "data/processed",
    "notebooks",
    "results/models",
    "results/plots",
    "src/cgcnn",
    "tests"
)

foreach ($dir in $directories) {
    if (-not (Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Exists:  $dir" -ForegroundColor Gray
    }
}

# Create __init__.py files to make 'src' and 'src/cgcnn' Python packages
Write-Host "`nCreating __init__.py files..." -ForegroundColor Yellow
$initFiles = @(
    "src/__init__.py",
    "src/cgcnn/__init__.py"
)

foreach ($file in $initFiles) {
    if (-not (Test-Path -Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
        Write-Host "✅ Created: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Exists:  $file" -ForegroundColor Gray
    }
}

Write-Host "`n🎉 Project structure created successfully!" -ForegroundColor Cyan
