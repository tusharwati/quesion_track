# QuestionTrack Frontend Startup Script

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "QuestionTrack Frontend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Node version
Write-Host "Checking Node.js version..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Node $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host ""
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] Dependencies already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Starting Frontend Development Server..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend will be available at: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "Make sure the backend is running at http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the development server
npm run dev
