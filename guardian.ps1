$ErrorActionPreference = 'SilentlyContinue'
$Global:Snapshots = @()

function Write-GuardianTitle {
    Write-Host ('=' * 60) -ForegroundColor Cyan
}

function Get-ProcessList {
    Get-Process | Select-Object -First 20 -Property Name, Id, @{Name=MEM;Expression={$_.WorkingSet/1MB}}
}

function Get-NetworkConnections {
    Get-NetTCPConnection -State Established | Select-Object -First 20
}

function Get-SystemInfo {
    Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, CsProcessors
}

function Take-Snapshot {
    param([string]$Type = 'full')
    $snap = @{
        Time = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        Type = $Type
    }
    if ($Type -eq 'full' -or $Type -eq 'processes') {
        $snap['Processes'] = Get-ProcessList
    }
    if ($Type -eq 'full' -or $Type -eq 'network') {
        $snap['Network'] = Get-NetworkConnections
    }
    if ($Type -eq 'full' -or $Type -eq 'system') {
        $snap['System'] = Get-SystemInfo
    }
    $Global:Snapshots += $snap
    Write-Host ('Snapshot taken at ' + $snap.Time)
}

function Export-ToJson {
    param([string]$File = 'guardian.json')
    $Global:Snapshots | ConvertTo-Json | Out-File $File
    Write-Host ('Exported to ' + $File)
}

function Start-Shell {
    Write-Host ''
    Write-GuardianTitle
    Write-Host 'Guardian DFIR - PowerShell CLI' -ForegroundColor Green
    Write-GuardianTitle
    Write-Host ''
    
    while ($true) {
        Write-Host '(guardian) ' -ForegroundColor Yellow -NoNewline
        $input = Read-Host
        $cmd = $input.Trim().ToLower()
        
        switch ($cmd) {
            'help' { Write-Host 'Commands: processes, network, sysinfo, snapshot, snapshot full, export, history, exit' }
            'processes' { Write-GuardianTitle; Get-ProcessList | Format-Table }
            'network' { Write-GuardianTitle; Get-NetworkConnections | Format-Table }
            'sysinfo' { Write-GuardianTitle; Get-SystemInfo | Format-List }
            'system' { Write-GuardianTitle; Get-SystemInfo | Format-List }
            'snapshot' { Take-Snapshot -Type 'full' }
            { $_ -match '^snapshot' } { $type = $_.Replace('snapshot ', ''); Take-Snapshot -Type $type }
            'export' { Export-ToJson }
            'history' { Write-GuardianTitle; $Global:Snapshots | Format-Table }
            'exit' { Write-Host 'Goodbye'; break }
            'quit' { Write-Host 'Goodbye'; break }
            'q' { Write-Host 'Goodbye'; break }
            default { if ($cmd) { Write-Host 'Unknown command' } }
        }
    }
}

Start-Shell
