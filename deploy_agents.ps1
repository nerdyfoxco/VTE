# Deploy All VTE Agents (Strangler Fig 6-Agent Framework)

Write-Host "========================================="
Write-Host "🚀 DEPLOYING VTE MULTI-AGENT FRAMEWORK"
Write-Host "========================================="

# 1. 🏗️ Infrastructure Agent (PostgreSQL + pgvector & Redis)
Write-Host "`n[1/4] Waking the Architect (Docker Infrastructure)..."
docker-compose up -d

Write-Host "`nWaiting 5 seconds for databases to accept connections..."
Start-Sleep -Seconds 5

# 2. 🧠 Identity, Security & Orchestration Agents (The Node.js Gateway)
Write-Host "`n[2/4] Waking the Gatekeeper, Brain, and Intelligence (UMP Gateway)..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd canonical-ump-system\foundation; npx tsx src/gateway.ts`"" -WindowStyle Normal

# 3. 👁️ Senses Agent (Gmail Poller)
Write-Host "`n[3/4] Waking the Senses (Asynchronous Email Ingestion Edge)..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd canonical-ump-system\chapters\senses\topic-ingestion; npx tsx src/index.ts`"" -WindowStyle Normal

# 4. 🦾 Face & Hands Agent (Next.js Control Plane)
Write-Host "`n[4/4] Waking the Face (Next.js Dashboard)..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd apps\frontend; npm run dev`"" -WindowStyle Normal

Write-Host "`n========================================="
Write-Host "✅ ALL AGENTS DEPLOYED SUCCESSFULLY!"
Write-Host "The VTE framework is now running concurrently across 3 separate terminal windows."
Write-Host "Dashboard available at: http://localhost:3000"
Write-Host "Gateway available at: http://localhost:8000"
Write-Host "========================================="
