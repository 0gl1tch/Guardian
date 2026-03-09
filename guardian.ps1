$ErrorActionPreference = 'SilentlyContinue'
$Global:Snapshots = @()

function Show-Menu {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "        Guardian DFIR CLI - PowerShell Native" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. Processes        - List running processes"
    Write-Host "  2. Network          - Show network connections"
    Write-Host "  3. System Info      - Display system information"
    Write-Host "  4. Full Snapshot    - Capture all data"
    Write-Host "  5. Export to JSON   - Save snapshots to file"
    Write-Host "  6. View Snapshots   - List all snapshots"
    Write-Host "  0. Exit             - Exit Guardian"
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
}

function Get-ProcessList {
    Get-Process | Select-Object -First 20 -Property Name, Id, @{Name='Memory_MB';Expression={[math]::Round($_.WorkingSet/1MB, 2)}}
}

function Get-NetworkConnections {
    Get-NetTCPConnection -State Established | Select-Object -First 20 -Property LocalAddress, LocalPort, RemoteAddress, RemotePort, State
}

function Get-SystemInfo {
    Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, CsProcessors, CsTotalPhysicalMemory
}

function Take-Snapshot {
    param([string]$Type = 'full')
    Write-Host ""
    Write-Host "Taking snapshot..." -ForegroundColor Yellow
    
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
    Write-Host ("Snapshot #" + ($Global:Snapshots.Count) + " taken at " + $snap.Time) -ForegroundColor Green
}

function Export-ToJson {
    param([string]$File = 'guardian.json')
    if ($Global:Snapshots.Count -eq 0) {
        Write-Host "No snapshots to export" -ForegroundColor Red
        return
    }
    
    $Global:Snapshots | ConvertTo-Json | Out-File $File
    Write-Host ("Exported to " + $File) -ForegroundColor Green
}

function Show-Snapshots {
    if ($Global:Snapshots.Count -eq 0) {
        Write-Host "No snapshots taken yet" -ForegroundColor Yellow
        return
    }
    
    Write-Host ""
    Write-Host "Snapshots:" -ForegroundColor Cyan
    for ($i = 0; $i -lt $Global:Snapshots.Count; $i++) {
        $snap = $Global:Snapshots[$i]
        Write-Host ("  " + $i + ". " + $snap.Time + " - " + $snap.Type) -ForegroundColor White
    }
}

function Start-Guardian {
    while ($true) {
        Show-Menu
        Write-Host "(guardian) " -ForegroundColor Yellow -NoNewline
        $choice = Read-Host
        
        switch ($choice) {
            '1' {
                Write-Host ""
                Write-Host "Running Processes:" -ForegroundColor Cyan
                Write-Host "============================================================" -ForegroundColor Cyan
                Get-ProcessList | Format-Table -AutoSize
            }
            '2' {
                Write-Host ""
                Write-Host "Network Connections:" -ForegroundColor Cyan
                Write-Host "============================================================" -ForegroundColor Cyan
                Get-NetworkConnections | Format-Table -AutoSize
            }
            '3' {
                Write-Host ""
                Write-Host "System Information:" -ForegroundColor Cyan
                Write-Host "============================================================" -ForegroundColor Cyan
                Get-SystemInfo | Format-List
            }
            '4' {
                Take-Snapshot -Type 'full'
            }
            '5' {
                Write-Host ""
                Write-Host "Export options:" -ForegroundColor Cyan
                Write-Host "  1. Export as guardian.json (default)"
                Write-Host "  2. Export with custom name"
                Write-Host ""
                Write-Host "(guardian-export) " -ForegroundColor Yellow -NoNewline
                $exportChoice = Read-Host
                
                switch ($exportChoice) {
                    '1' { Export-ToJson }
                    '2' {
                        Write-Host "Enter filename: " -NoNewline
                        $filename = Read-Host
                        Export-ToJson -File $filename
                    }
                    default { Write-Host "Invalid option" -ForegroundColor Red }
                }
            }
            '6' {
                Show-Snapshots
            }
            '0' {
                Write-Host ""
                Write-Host "Exiting Guardian..." -ForegroundColor Green
                Write-Host ""
                break
            }
            default {
                Write-Host "Invalid option. Please select 0-6." -ForegroundColor Red
            }
        }
        
        Write-Host ""
        Write-Host "Press Enter to continue..." -ForegroundColor Gray
        Read-Host | Out-Null
    }
}

Start-Guardian
