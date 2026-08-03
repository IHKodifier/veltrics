# start_backend.ps1
# This script navigates to the src/backend directory, activates the Python virtual environment,
# seeds the local SQLite database if missing, and launches the FastAPI Uvicorn server on port 8000.
# Zero Docker required! High-speed local development setup.

$ErrorActionPreference = "Stop"

# Get the directory where the script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

# Navigate to the src/backend directory (or create if not present)
$BackendDir = Join-Path -Path $ProjectRoot -ChildPath "src\backend"

if (-not (Test-Path $BackendDir)) {
    Write-Host "Creating backend directory at $BackendDir..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $BackendDir -Force | Out-Null
}

Set-Location -Path $BackendDir

# Check and activate virtual environment
$VenvPath = Join-Path -Path $BackendDir -ChildPath "venv\Scripts\Activate.ps1"

Write-Host "Activating Python virtual environment..." -ForegroundColor Cyan
if (Test-Path $VenvPath) {
    . $VenvPath
} else {
    Write-Host "Warning: Virtual environment not found at $VenvPath." -ForegroundColor Yellow
    Write-Host "Please create one using: python -m venv venv" -ForegroundColor Yellow
}

# Set Local Development Environment Variables
$env:ENVIRONMENT = "development"
$env:DATABASE_URL = "sqlite:///./dev.db"
$env:FIREBASE_AUTH_EMULATOR_HOST = "127.0.0.1:9099"

Write-Host "Starting FastAPI Uvicorn Server on http://127.0.0.1:8000 (Reload Enabled)..." -ForegroundColor Green
uvicorn main:app --reload --port 8000 --log-level debug
