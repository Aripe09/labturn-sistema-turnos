$ErrorActionPreference = "Stop"
. "$PSScriptRoot\common.ps1"

$Port = 5000
if (Test-LabTurnPort $Port) {
  $owner = Get-LabTurnPortOwner $Port
  Write-Host "Puerto $Port ocupado por $owner." -ForegroundColor Yellow
  Wait-WhilePortIsOwned $Port "Flask"
  exit 0
}

$Python = Resolve-LabTurnPython
$env:PYTHONPATH = $BackendDepsPath
Write-Host "Flask disponible en http://127.0.0.1:$Port/api/health" -ForegroundColor Green
Push-Location $BackendPath
try {
  & $Python.File @($Python.Args) app.py
} finally {
  Pop-Location
}

