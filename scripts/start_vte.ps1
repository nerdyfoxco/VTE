# Startup Script for VTE
Write-Host "Starting VTE Stack..." -ForegroundColor Green

# 1. Reset Database
$DB_FILE = "C:\Bintloop\VTE\vte.db"
if (Test-Path $DB_FILE) {
    Write-Host "Removing existing Database..." -ForegroundColor Yellow
    Remove-Item $DB_FILE -Force
}

# 2. Kill Zombie Python/Node (Aggressive Cleanup)
Write-Host "Killing Orphaned Processes..."
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. Start Backend
Write-Host "Starting Backend..."
$backendProcess = Start-Process -FilePath "uvicorn" -ArgumentList "vte.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory "C:\Bintloop\VTE\spine" -PassThru -NoNewWindow
Write-Host "Backend PID: $($backendProcess.Id)"

# 4. Start Frontend
Write-Host "Starting Frontend..."
$frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "C:\Bintloop\VTE\apps\frontend" -PassThru -NoNewWindow
Write-Host "Frontend PID: $($frontendProcess.Id)"

# 5. Wait for Services
Write-Host "Waiting for services to stabilize..."
Start-Sleep -Seconds 10
Write-Host "VTE Stack Running." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"

# Note: This script exits but processes run in background. 
# Use 'Stop-Process' or Task Manager to kill them.
