# start_backend.ps1
# Navigates to src/backend, auto-creates venv & installs dependencies if missing, and launches FastAPI server on http://127.0.0.1:8000.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
$BackendDir = Join-Path -Path $ProjectRoot -ChildPath "src\backend"

if (-not (Test-Path $BackendDir)) {
    Write-Host "Creating backend directory at $BackendDir..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $BackendDir -Force | Out-Null
}

Set-Location -Path $BackendDir

$VenvDir = Join-Path -Path $BackendDir -ChildPath "venv"
$VenvActivate = Join-Path -Path $VenvDir -ChildPath "Scripts\Activate.ps1"

if (-not (Test-Path $VenvActivate)) {
    Write-Host "Virtual environment missing. Creating python -m venv venv..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Activating Python virtual environment..." -ForegroundColor Cyan
. $VenvActivate

Write-Host "Ensuring dependencies from requirements.txt are installed..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Set Local Development Environment Variables
$env:ENVIRONMENT = "development"
$env:DATABASE_URL = "sqlite:///./dev.db"
$env:FIREBASE_AUTH_EMULATOR_HOST = "127.0.0.1:9099"

Write-Host "Starting FastAPI Uvicorn Server on http://127.0.0.1:8000 (Reload Enabled)..." -ForegroundColor Green
uvicorn app.main:app --reload --port 8000 --log-level debug
