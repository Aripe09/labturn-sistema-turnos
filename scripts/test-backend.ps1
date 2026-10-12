$ErrorActionPreference = "Stop"
. "$PSScriptRoot\common.ps1"

$Python = Resolve-LabTurnPython
$env:PYTHONPATH = $BackendDepsPath
Invoke-LabTurnPython $Python @("-m", "pytest") $BackendPath

