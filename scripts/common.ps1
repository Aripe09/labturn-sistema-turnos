$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$BackendPath = Join-Path $ProjectRoot "backend"
$FrontendPath = Join-Path $ProjectRoot "frontend"
$BackendDepsPath = Join-Path $BackendPath ".deps"
$BundledPython = "C:\Users\pedra\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

function Write-LabTurnStep([string]$Message) {
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Test-LabTurnPort([int]$Port) {
  $client = $null
  try {
    $client = [System.Net.Sockets.TcpClient]::new()
    $async = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    $connected = $async.AsyncWaitHandle.WaitOne(350)
    if (-not $connected) { return $false }
    $client.EndConnect($async)
    return $true
  } catch {
    return $false
  } finally {
    if ($client) { $client.Close() }
  }
}

function Get-LabTurnPortOwner([int]$Port) {
  try {
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $connection) { return $null }
    try {
      $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
      if ($process) {
        return "$($connection.OwningProcess) ($($process.ProcessName))"
      }
    } catch {
      return "$($connection.OwningProcess)"
    }
  } catch {
    try {
      $line = netstat -ano | Select-String -Pattern "LISTENING\s+\d+$" | Where-Object { $_.Line -match ":$Port\s" } | Select-Object -First 1
      if ($line -and $line.Line -match "\s(\d+)\s*$") {
        return $Matches[1]
      }
    } catch {
      return $null
    }
  }

  return $null
}

function Resolve-LabTurnPython {
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

function Invoke-LabTurnPython($Python, [string[]]$Arguments, [string]$WorkingDirectory) {
  Push-Location $WorkingDirectory
  try {
    & $Python.File @($Python.Args) @Arguments
  } finally {
    Pop-Location
  }
}

function Wait-WhilePortIsOwned([int]$Port, [string]$Name) {
  Write-Host "$Name ya parece estar ejecutandose en el puerto $Port. Manteniendo este proceso activo; Ctrl+C para salir." -ForegroundColor Yellow
  while (Test-LabTurnPort $Port) {
    Start-Sleep -Seconds 2
  }
}

