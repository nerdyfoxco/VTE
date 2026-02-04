# VTE Local E2E Runner
Write-Host "--- VTE Local E2E Verification ---" -ForegroundColor Cyan

# 1. Start Stack
Write-Host "[1] Starting Stack (Detached)..."
docker-compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker Compose Failed!" -ForegroundColor Red
    exit 1
}

# 2. Wait for startup
Write-Host "[2] Waiting 10s for services..."
Start-Sleep -Seconds 10

# 3. Run Validation Script
Write-Host "[3] Running Python Validation Script..."
# Ensure we use the local python env that has 'requests' or assume user has it.
# We'll try 'python', 'py', or 'poetry run python' if inside spine.
# The script is at C:\Bintloop\VTE\validate_local_stack.py
python validate_local_stack.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Validation Script Failed!" -ForegroundColor Red
    # Show logs
    docker-compose logs --tail=50 spline-worker
    exit 1
}

# 4. Show Worker Logs
Write-Host "[4] Validation Passed. Showing recent Worker Logs:" -ForegroundColor Green
docker-compose logs --tail=20 spine-worker

Write-Host "--- DONE ---" -ForegroundColor Cyan
