# PowerShell IEX Loader for Guardian DFIR CLI
# Usage: iex(New-Object Net.WebClient).DownloadString('https://your-server/guardian_loader.ps1')

# Guardian DFIR CLI Loader - Downloads and executes Python Guardian in-memory
# No files left on disk, completely ephemeral

$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'SilentlyContinue'

function Get-PythonExe {
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        return (Get-Command python3).Source
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return (Get-Command python).Source
    }
    return $null
}

function Install-Python3 {
    Write-Host "[*] Python not found. Attempting automated install..." -ForegroundColor Cyan
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        try {
            Write-Host "[*] Installing Python 3 with winget..." -ForegroundColor Cyan
            winget install --id Python.Python.3 -e --source winget --accept-package-agreements --accept-source-agreements -h | Out-Null
            return $true
        } catch {
            Write-Host "[!] winget install failed: $_" -ForegroundColor Yellow
        }
    }
    if (Get-Command choco -ErrorAction SilentlyContinue) {
        try {
            Write-Host "[*] Installing Python 3 with choco..." -ForegroundColor Cyan
            choco install python -y | Out-Null
            return $true
        } catch {
            Write-Host "[!] choco install failed: $_" -ForegroundColor Yellow
        }
    }
    Write-Host "[!] Could not automatically install Python. Please install Python 3.10+ and add to PATH." -ForegroundColor Red
    return $false
}

Write-Host "🛡️  Guardian DFIR CLI - Loading..." -ForegroundColor Green

# Configuration - Change these to your server
$GITHUB_USERNAME = "0gl1tch"  # Update this if using your own GitHub account
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

    $pythonExe = Get-PythonExe
    if (-not $pythonExe) {
        if (-not (Install-Python3)) {
            exit 1
        }
        Start-Sleep -Seconds 3
        $pythonExe = Get-PythonExe
    }

    if (-not $pythonExe) {
        Write-Host "[!] Python not found after installation attempt. Please install Python 3 manually." -ForegroundColor Red
        exit 1
    }

    $terminalCandidates = @(
        "wt.exe",
        "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe",
        "$env:ProgramFiles\PowerShell\7\pwsh.exe",
        "$env:ProgramFiles(x86)\PowerShell\7\pwsh.exe",
        "powershell.exe",
        "pwsh.exe"
    )

    $terminalExe = $null
    foreach ($candidate in $terminalCandidates) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            $terminalExe = (Get-Command $candidate).Source
            break
        }
        if (Test-Path $candidate) {
            $terminalExe = $candidate
            break
        }
    }

    if (-not $terminalExe) {
        Write-Host "[!] Could not find any terminal executable (wt/powershell/pwsh)." -ForegroundColor Red
        exit 1
    }

    Write-Host "[*] Launching Guardian in a new terminal session using: $terminalExe" -ForegroundColor Cyan

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

    if ($terminalExe -match "wt(.exe)?$") {
        # Windows Terminal requires command after executable
        $psArgs = @("powershell", "-NoExit", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $launcherScript)
    } else {
        $psArgs = @(
            '-NoExit',
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-File', $launcherScript
        )
    }

    try {
        Write-Host "[*] Launching new terminal via Start-Process: $terminalExe $($psArgs -join ' ')" -ForegroundColor Cyan
        Start-Process -FilePath $terminalExe -ArgumentList $psArgs -WindowStyle Normal -ErrorAction Stop | Out-Null
        Write-Host "✅ Guardian started in new terminal." -ForegroundColor Green
        Write-Host "Temp script: $tempScript" -ForegroundColor DarkCyan
        Write-Host "Launcher script: $launcherScript" -ForegroundColor DarkCyan
    } catch {
        Write-Host "[!] Start-Process failed: $_" -ForegroundColor Yellow
        Write-Host "[*] Trying fallback via cmd start with powershell..." -ForegroundColor Cyan
        try {
            Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "start", "powershell", "-NoExit", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $launcherScript -WindowStyle Normal -ErrorAction Stop | Out-Null
            Write-Host "✅ Guardian started in new terminal (fallback)." -ForegroundColor Green
            Write-Host "Temp script: $tempScript" -ForegroundColor DarkCyan
            Write-Host "Launcher script: $launcherScript" -ForegroundColor DarkCyan
        } catch {
            Write-Host "[!] Fallback failed too: $_" -ForegroundColor Red
            Write-Host "[!] Running inline in this window." -ForegroundColor Yellow
            & $pythonExe $tempScript
            Read-Host "Press Enter to close"
        }
    }

    Read-Host "Loader complete. Press Enter to close this loader shell."

} catch {
    Write-Host "[!] Error: $_" -ForegroundColor Red
    exit 1
}
