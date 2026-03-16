# PowerShell IEX Loader for Guardian DFIR CLI
# Usage: iex(New-Object Net.WebClient).DownloadString('https://your-server/guardian_loader.ps1')

# Guardian DFIR CLI Loader - Downloads and executes Python Guardian in-memory
# No files left on disk, completely ephemeral

$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'SilentlyContinue'

function Invoke-PythonVersionCheck {
    param([string]$Exe, [string[]]$Args)
    try {
        $cmdArgs = @($Args) + '--version'
        $output = & $Exe @cmdArgs 2>&1
        if ($LASTEXITCODE -eq 0 -and $output -match 'Python\s+3\.') {
            return $true
        }
    } catch {
    }
    return $false
}

function Get-PythonCandidates {
    @(
        @{Exe='py'; Args=@('-3')},
        @{Exe='py'; Args=@('-3.12')},
        @{Exe='py'; Args=@('-3.11')},
        @{Exe='py'; Args=@('-3.10')},
        @{Exe='python3'; Args=@()},
        @{Exe='python'; Args=@()},
        @{Exe="$env:WINDIR\py.exe"; Args=@('-3')},
        @{Exe="$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"; Args=@()},
        @{Exe="$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"; Args=@()},
        @{Exe="$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"; Args=@()},
        @{Exe="$env:ProgramFiles\Python\Python312\python.exe"; Args=@()},
        @{Exe="$env:ProgramFiles\Python\Python311\python.exe"; Args=@()},
        @{Exe="$env:ProgramFiles\Python\Python310\python.exe"; Args=@()},
        @{Exe='C:\Python312\python.exe'; Args=@()},
        @{Exe='C:\Python311\python.exe'; Args=@()},
        @{Exe='C:\Python310\python.exe'; Args=@()}
    )
}

function Find-ValidPythonExe {
    foreach ($candidate in Get-PythonCandidates) {
        $exe = $candidate.Exe
        $args = $candidate.Args
        try {
            $checkExe = $null
            if (Test-Path $exe) {
                $checkExe = $exe
            } elseif (Get-Command $exe -ErrorAction SilentlyContinue) {
                $checkExe = (Get-Command $exe).Source
            }
            if (-not $checkExe -and $exe -match '^.*\\python.exe$' -and Test-Path $exe) {
                $checkExe = $exe
            }
            if (-not $checkExe) { continue }

            if (Invoke-PythonVersionCheck -Exe $checkExe -Args $args) {
                return @{ Exe = $checkExe; Args = $args }
            }
        } catch {
        }
    }
    return $null
}

function Install-Python3 {
    Write-Host "[*] Python not found. Attempting automated install..." -ForegroundColor Cyan
    $installSucceeded = $false
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        $wingetCandidates = @(
            'Python.Python.3',
            'Python.Python.3.12',
            'Python.Python.3.11',
            'Python.Python.3.10'
        )
        foreach ($id in $wingetCandidates) {
            try {
                Write-Host "[*] winget installing $id..." -ForegroundColor Cyan
                winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements -h | Out-Null
                $installSucceeded = $true
                break
            } catch {
                Write-Host "[!] winget $id failed: $_" -ForegroundColor Yellow
            }
        }
    }
    if (-not $installSucceeded -and (Get-Command choco -ErrorAction SilentlyContinue)) {
        foreach ($pkg in @('python', 'python3')) {
            try {
                Write-Host "[*] choco installing $pkg..." -ForegroundColor Cyan
                choco install $pkg -y | Out-Null
                $installSucceeded = $true
                break
            } catch {
                Write-Host "[!] choco $pkg failed: $_" -ForegroundColor Yellow
            }
        }
    }
    return $installSucceeded
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
    $pythonCmd = if ($pythonExe.Args -and $pythonExe.Args.Count -gt 0) { "& '$($pythonExe.Exe)' $($pythonExe.Args -join ' ') '$tempScript'" } else { "& '$($pythonExe.Exe)' '$tempScript'" }
    $launcherContent = @"
Write-Host 'Guardian session started. Output below:' -ForegroundColor Green
try {
    $($pythonCmd)
} catch {
    Write-Host "[!] Python execution failed from launcher: $_" -ForegroundColor Red
    Write-Host "[!] Verifying Python command: $pythonCmd" -ForegroundColor Yellow
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
