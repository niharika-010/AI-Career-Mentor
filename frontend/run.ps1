# Silence npm and Node.js verbose warnings
$env:Path = "$env:Path;C:\Program Files\nodejs"
$env:NEXT_TELEMETRY_DISABLED = "1"
$env:NODE_NO_WARNINGS = "1"

Write-Host "Starting AI Career Assistant Frontend on http://localhost:3000..." -ForegroundColor Green
npm run dev
