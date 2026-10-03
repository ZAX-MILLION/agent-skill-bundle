$ErrorActionPreference = "Stop"

$RawBase = if ($env:DEVMAX_RAW_BASE) { $env:DEVMAX_RAW_BASE } else { "https://raw.githubusercontent.com/ZAX-MILLION/agent-skill-bundle/main" }
$BinDir = if ($env:DEVMAX_BIN_DIR) { $env:DEVMAX_BIN_DIR } else { Join-Path $env:USERPROFILE ".devmax\bin" }
New-Item -ItemType Directory -Path $BinDir -Force | Out-Null

$PyTarget = Join-Path $BinDir "devmax-init.py"
$CmdTarget = Join-Path $BinDir "devmax-init.cmd"

Invoke-WebRequest -UseBasicParsing -Uri "$RawBase/scripts/devmax_init.py" -OutFile $PyTarget

$Wrapper = @"
@echo off
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 "$PyTarget" %*
  exit /b %ERRORLEVEL%
)
python "$PyTarget" %*
"@
Set-Content -Path $CmdTarget -Value $Wrapper -Encoding ASCII

$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$Parts = @()
if ($UserPath) { $Parts = $UserPath -split ";" | Where-Object { $_ } }
if ($Parts -notcontains $BinDir) {
    $NewPath = (($Parts + $BinDir) -join ";")
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
}
if (($env:Path -split ";") -notcontains $BinDir) {
    $env:Path = "$BinDir;$env:Path"
}

Write-Host "Installed: $CmdTarget"
Write-Host "For every new project: open its terminal and run: devmax-init"
Write-Host "If this terminal does not recognize it, open a new terminal once."
