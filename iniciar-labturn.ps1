param(
  [int]$BackendPort = 5000,
  [int]$FrontendPort = 4200
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendPath = Join-Path $Root "backend"
$FrontendPath = Join-Path $Root "frontend"
$DepsPath = Join-Path $BackendPath ".deps"
$BundledPython = "C:\Users\pedra\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

function Write-Step($Message) {
  Write-Host ""
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Test-PortInUse($Port) {
  try {
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return $null -ne $connection
  } catch {
    return $false
  }
}

function Resolve-Python {
  $candidates = @()

  $py = Get-Command py.exe -ErrorAction SilentlyContinue
  if ($py) {
    $candidates += @{ File = $py.Source; Args = @("-3") }
  }

  $python = Get-Command python.exe -ErrorAction SilentlyContinue
  if ($python -and $python.Source -notlike "*WindowsApps*") {
    $candidates += @{ File = $python.Source; Args = @() }
  }

  if (Test-Path $BundledPython) {
    $candidates += @{ File = $BundledPython; Args = @() }
  }

  foreach ($candidate in $candidates) {
    try {
      & $candidate.File @($candidate.Args) --version *> $null
      return $candidate
    } catch {
      continue
    }
  }

  throw "No se encontro Python funcional. Instala Python 3.11+ o ejecuta desde Codex con el runtime incluido."
}

function Invoke-Python($Python, [string[]]$Arguments, [string]$WorkingDirectory) {
  Push-Location $WorkingDirectory
  try {
    & $Python.File @($Python.Args) @Arguments
  } finally {
    Pop-Location
  }
}

Write-Host "LabTurn - Inicio local" -ForegroundColor Green
Write-Host "Proyecto: $Root"

if (-not (Test-Path $BackendPath)) { throw "No existe la carpeta backend." }
if (-not (Test-Path $FrontendPath)) { throw "No existe la carpeta frontend." }

Write-Step "Verificando Python"
$Python = Resolve-Python
Write-Host "Python: $($Python.File) $($Python.Args -join ' ')"

Write-Step "Verificando dependencias Flask"
New-Item -ItemType Directory -Force -Path $DepsPath | Out-Null
$env:PYTHONPATH = $DepsPath
$flaskOk = $true
try {
  Invoke-Python $Python @("-c", "import flask, flask_cors") $BackendPath *> $null
} catch {
  $flaskOk = $false
}

if (-not $flaskOk) {
  Write-Host "Instalando dependencias Python en backend\.deps..."
  Invoke-Python $Python @("-m", "pip", "install", "--target", ".deps", "-r", "requirements.txt") $BackendPath
}

Write-Step "Verificando Node.js y npm"
$npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
if (-not $npm) { throw "No se encontro npm. Instala Node.js LTS." }
Write-Host "npm: $($npm.Source)"

if (-not (Test-Path (Join-Path $FrontendPath "node_modules"))) {
  Write-Step "Instalando dependencias Angular"
  Push-Location $FrontendPath
  try {
    npm install
  } finally {
    Pop-Location
  }
}

Write-Step "Revisando puertos"
$backendBusy = Test-PortInUse $BackendPort
$frontendBusy = Test-PortInUse $FrontendPort

if ($backendBusy) {
  Write-Host "Backend: el puerto $BackendPort ya esta ocupado. No se inicia otro Flask." -ForegroundColor Yellow
} else {
  Write-Host "Iniciando Flask en http://127.0.0.1:$BackendPort"
  $backendCommand = "`$env:PYTHONPATH='$DepsPath'; & '$($Python.File)' $($Python.Args -join ' ') app.py"
  Start-Process powershell.exe -ArgumentList "-NoExit", "-NoProfile", "-Command", $backendCommand -WorkingDirectory $BackendPath
}

if ($frontendBusy) {
  Write-Host "Frontend: el puerto $FrontendPort ya esta ocupado. No se inicia otro Angular." -ForegroundColor Yellow
} else {
  Write-Host "Iniciando Angular en http://127.0.0.1:$FrontendPort"
  Start-Process powershell.exe -ArgumentList "-NoExit", "-NoProfile", "-Command", "npm start" -WorkingDirectory $FrontendPath
}

Write-Host ""
Write-Host "Direcciones:" -ForegroundColor Green
Write-Host "  App completa:       http://127.0.0.1:$FrontendPort/"
Write-Host "  Generar turno:      http://127.0.0.1:$FrontendPort/clientes"
Write-Host "  Monitor de turnos:  http://127.0.0.1:$FrontendPort/clientes/monitor"
Write-Host "  Mesas de atencion:  http://127.0.0.1:$FrontendPort/atencion"
Write-Host "  API Flask:          http://127.0.0.1:$BackendPort/api/health"
Write-Host ""
Write-Host "Mantén abiertas las ventanas de Flask y Angular mientras uses LabTurn." -ForegroundColor Green

