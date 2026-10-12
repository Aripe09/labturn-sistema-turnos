$ErrorActionPreference = "Stop"
. "$PSScriptRoot\common.ps1"

Write-LabTurnStep "Preparando backend Flask"
$Python = Resolve-LabTurnPython
Write-Host "Python: $($Python.File) $($Python.Args -join ' ')"

New-Item -ItemType Directory -Force -Path $BackendDepsPath | Out-Null
$env:PYTHONPATH = $BackendDepsPath

$depsOk = $true
try {
  Invoke-LabTurnPython $Python @("-c", "import flask, flask_cors") $BackendPath *> $null
} catch {
  $depsOk = $false
}

if (-not $depsOk) {
  Write-Host "Instalando dependencias Python en backend\.deps..."
  Invoke-LabTurnPython $Python @("-m", "pip", "install", "--target", ".deps", "-r", "requirements.txt") $BackendPath
} else {
  Write-Host "Dependencias Flask listas."
}

