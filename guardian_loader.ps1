# PowerShell IEX Loader for Guardian DFIR CLI
# Usage: iex(New-Object Net.WebClient).DownloadString('https://your-server/guardian_loader.ps1')

# Guardian DFIR CLI Loader - Downloads and executes Python Guardian in-memory
# No files left on disk, completely ephemeral

$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'SilentlyContinue'

# Check if Python is available
try {
    $pythonCheck = python3 --version 2>&1
    if (-not $pythonCheck) {
        Write-Host "[!] Python 3 not found or not in PATH"
        Write-Host "[!] Please install Python 3.10+ and add to PATH"
        exit 1
    }
} catch {
    Write-Host "[!] Python 3 is required. Please install it first."
    exit 1
}

Write-Host "🛡️  Guardian DFIR CLI - Loading..." -ForegroundColor Green

# Configuration - Change these to your server
$GITHUB_USERNAME = "your-username"
$GITHUB_REPO = "Guardian"
$GITHUB_BRANCH = "master"

# Build the raw content URL (using GitHub as default)
$RAW_URL = "https://raw.githubusercontent.com/$GITHUB_USERNAME/$GITHUB_REPO/$GITHUB_BRANCH/guardian_standalone.py"

# Alternative: Use custom server
# $RAW_URL = "https://your-server.com/guardian_standalone.py"

Write-Host "[*] Downloading Guardian DFIR CLI..." -ForegroundColor Cyan

try {
    # Download the Python script
    $webClient = New-Object Net.WebClient
    $pythonCode = $webClient.DownloadString($RAW_URL)
    
    if (-not $pythonCode) {
        Write-Host "[!] Failed to download Guardian. Check your internet connection and server URL."
        exit 1
    }
    
    Write-Host "[*] Preparing Guardian temp script..." -ForegroundColor Cyan

    $tempScript = Join-Path $env:TEMP "guardian_standalone_$(Get-Random).py"
    $pythonCode | Out-File -FilePath $tempScript -Encoding UTF8

    $pythonExe = $null
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonExe = (Get-Command python3).Source
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonExe = (Get-Command python).Source
    }

    if (-not $pythonExe) {
        Write-Host "[!] Python not found. Install Python 3 and add to PATH." -ForegroundColor Red
        exit 1
    }

    $terminalExe = "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe"
    if (-not (Test-Path $terminalExe)) {
        $terminalExe = "$env:ProgramFiles\PowerShell\7\pwsh.exe"
    }
    if (-not (Test-Path $terminalExe)) {
        $terminalExe = "$env:ProgramFiles(x86)\PowerShell\7\pwsh.exe"
    }
    if (-not (Test-Path $terminalExe)) {
        Write-Host "[!] Could not find powershell executable to spawn terminal." -ForegroundColor Red
        exit 1
    }

    Write-Host "[*] Launching Guardian in a new terminal session..." -ForegroundColor Cyan

    # Create a temporary PowerShell launcher script to avoid escaping issues
    $launcherScript = Join-Path $env:TEMP "guardian_launcher_$(Get-Random).ps1"
    $launcherContent = @"
Write-Host 'Guardian session started. Output below:' -ForegroundColor Green
& '$pythonExe' '$tempScript'
Write-Host ''
Write-Host 'Guardian session ended.' -ForegroundColor Green
Read-Host 'Press Enter to close this window.'
"@
    $launcherContent | Out-File -FilePath $launcherScript -Encoding UTF8

    $psArgs = @(
        '-NoExit',
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', $launcherScript
    )

    try {
        Write-Host "[*] Launching new terminal via Start-Process: $terminalExe $($psArgs -join ' ')" -ForegroundColor Cyan
        Start-Process -FilePath $terminalExe -ArgumentList $psArgs -WindowStyle Normal -ErrorAction Stop | Out-Null
        Write-Host "✅ Guardian started in new terminal." -ForegroundColor Green
        Write-Host "Temp script: $tempScript" -ForegroundColor DarkCyan
        Write-Host "Launcher script: $launcherScript" -ForegroundColor DarkCyan
    } catch {
        Write-Host "[!] Failed to start new terminal: $_" -ForegroundColor Red
        Write-Host "[!] Falling back to running inline in this window." -ForegroundColor Yellow
        & $pythonExe $tempScript
        Read-Host "Press Enter to close"
    }

    Read-Host "Loader complete. Press Enter to close this loader shell."

} catch {
    Write-Host "[!] Error: $_" -ForegroundColor Red
    exit 1
}
