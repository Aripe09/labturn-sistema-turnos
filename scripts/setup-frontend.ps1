$ErrorActionPreference = "Stop"
. "$PSScriptRoot\common.ps1"

Write-LabTurnStep "Preparando frontend Angular"
$npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
if (-not $npm) {
  throw "No se encontro npm. Instala Node.js LTS."
}

if (-not (Test-Path (Join-Path $FrontendPath "node_modules"))) {
  Write-Host "Instalando dependencias Angular..."
  Push-Location $FrontendPath
  try {
    npm install
  } finally {
    Pop-Location
  }
} else {
  Write-Host "Dependencias Angular listas."
}

