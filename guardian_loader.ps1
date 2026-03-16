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

    $terminalExe = $null
    if (Get-Command pwsh -ErrorAction SilentlyContinue) {
        $terminalExe = (Get-Command pwsh).Source
    } elseif (Get-Command powershell -ErrorAction SilentlyContinue) {
        $terminalExe = (Get-Command powershell).Source
    } else {
        Write-Host "[!] Neither pwsh nor powershell found to spawn interactive terminal." -ForegroundColor Red
        exit 1
    }

    Write-Host "[*] Launching Guardian in a new terminal session..." -ForegroundColor Cyan
    $guardianCommand = "& '$pythonExe' '$tempScript'"
    $terminalArgs = @('-NoExit', '-NoProfile', '-Command', "$guardianCommand; if ($?) { Write-Host 'Guardian session ended.'; } Read-Host 'Press Enter to close this window.'")

    Start-Process -FilePath $terminalExe -ArgumentList $terminalArgs | Out-Null
    Write-Host "✅ Guardian started in a new terminal. You can continue using this window." -ForegroundColor Green
    Write-Host "Temp script: $tempScript" -ForegroundColor DarkCyan

} catch {
    Write-Host "[!] Error: $_" -ForegroundColor Red
    exit 1
}
