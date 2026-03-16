# PowerShell IEX Loader for Guardian DFIR CLI
# Usage: iex(New-Object Net.WebClient).DownloadString('https://your-server/guardian_loader.ps1')

# Guardian DFIR CLI Loader - Downloads and executes Python Guardian in-memory
# No files left on disk, completely ephemeral

$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'SilentlyContinue'

function Validate-PythonExe {
    param([string]$Candidate)
    try {
        $v = & "$Candidate" --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $v -match 'Python\s+3\.') {
            return $true
        }
    } catch {
    }
    return $false
}

function Get-PythonExeCandidates {
    @(
        'python3',
        'python',
        'py -3',
        'py -3.12',
        'py -3.11',
        'py -3.10',
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:ProgramFiles\Python\Python312\python.exe",
        "$env:ProgramFiles\Python\Python311\python.exe",
        "$env:ProgramFiles\Python\Python310\python.exe",
        "C:\\Python312\\python.exe",
        "C:\\Python311\\python.exe",
        "C:\\Python310\\python.exe"
    )
}

function Find-ValidPythonExe {
    foreach ($candidate in Get-PythonExeCandidates) {
        try {
            if ($candidate -match 'py') {
                $parts = $candidate -split ' '
                $exe = $parts[0]
                $args = $parts[1..($parts.Length-1)]
                $output = & $exe @args --version 2>&1
                if ($LASTEXITCODE -eq 0 -and $output -match 'Python\s+3\.') { return "$exe $($args -join ' ')" }
            } else {
                if (Get-Command $candidate -ErrorAction SilentlyContinue) {
                    $path = (Get-Command $candidate).Source
                    if (Validate-PythonExe -Candidate $path) { return $path }
                } elseif (Test-Path $candidate) {
                    if (Validate-PythonExe -Candidate $candidate) { return $candidate }
                }
            }
        } catch {
        }
    }
    return $null
}

function Validate-PythonExe {
    param([string]$Candidate)
    try {
        $v = & "$Candidate" --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $v -match 'Python\s+3\.') {
            return $true
        }
    } catch {
    }
    return $false
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

    $pythonExe = Find-ValidPythonExe

    if (-not $pythonExe) {
        if (-not (Install-Python3)) {
            Write-Host "[!] Python install failed." -ForegroundColor Red
            exit 1
        }
        Start-Sleep -Seconds 6
        $pythonExe = Find-ValidPythonExe
    }

    if (-not $pythonExe) {
        Write-Host "[!] Python not found after installation attempt. Trying manual fallback list..." -ForegroundColor Yellow
        $pythonExe = Find-ValidPythonExe
    }

    if (-not $pythonExe) {
        Write-Host "[!] Python not found after installation attempt. Please install Python 3 manually and add to PATH." -ForegroundColor Red
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
try {
    & '$pythonExe' '$tempScript'
} catch {
    Write-Host "[!] Python execution failed from launcher: $_" -ForegroundColor Red
    Write-Host "[!] Verifying Python path: $pythonExe" -ForegroundColor Yellow
    Write-Host "[!] Please install Python 3 and add to PATH." -ForegroundColor Red
}
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
