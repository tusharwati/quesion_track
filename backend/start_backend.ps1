# QuestionTrack Backend Startup Script

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "QuestionTrack Backend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install and verify all declared dependencies using the active Python interpreter
Write-Host ""
Write-Host "Installing dependencies (this may take a few minutes on first run)..." -ForegroundColor Yellow
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Dependency installation failed. See the pip error above." -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "Dependencies are installed." -ForegroundColor Green

# Create .env if it doesn't exist
if (-Not (Test-Path "../.env")) {
    Write-Host ""
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item "..\.env.example" "..\.env"
    Write-Host ".env file created." -ForegroundColor Green
}

# Create data directory
if (-Not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}

# Create uploads directory
if (-Not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs will be at: http://localhost:8000/api/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Note: First run will download Whisper model (~74MB)" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the application
python run.py
