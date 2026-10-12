$ErrorActionPreference = "Stop"
. "$PSScriptRoot\common.ps1"

$Port = 4200
if (Test-LabTurnPort $Port) {
  $owner = Get-LabTurnPortOwner $Port
  Write-Host "Puerto $Port ocupado por $owner." -ForegroundColor Yellow
  Wait-WhilePortIsOwned $Port "Angular"
  exit 0
}

Write-Host "LabTurn disponible en http://127.0.0.1:$Port/" -ForegroundColor Green
Push-Location $FrontendPath
try {
  npm start
} finally {
  Pop-Location
}

