#!/usr/bin/env powershell
<#
.SYNOPSIS
    Guardian DFIR CLI - Pure PowerShell Implementation
    Complete forensic toolkit with zero dependencies
#>

$ErrorActionPreference = 'SilentlyContinue'
$WarningPreference = 'SilentlyContinue'

$Global:Snapshots = @()
$Global:History = @()

function Write-Title {
    param([string]$Text)
    Write-Host '' -ForegroundColor White
    Write-Host ('=' * 60) -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host ('=' * 60) -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host ('✓ ' + $Text) -ForegroundColor Green
}

function Write-Info {
    param([string]$Text)
    Write-Host ('ℹ ' + $Text) -ForegroundColor Cyan
}

function Write-ErrorMsg {
    param([string]$Text)
    Write-Host ('✗ ' + $Text) -ForegroundColor Red
}

function Get-ProcessList {
    try {
        $processes = Get-Process | Select-Object -Property Name, Id, @{Name='Memory_MB';Expression={[math]::Round($_.WorkingSet/1MB, 2)}}, CPU, Path, Company
        return $processes
    }
    catch {
        Write-ErrorMsg ('Failed to get processes: ' + $_)
        return $null
    }
}

function Get-NetworkConnections {
    try {
        $connections = @()
        
        if (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue) {
            $tcpConnections = Get-NetTCPConnection -State Established, Listen, TimeWait, CloseWait -ErrorAction SilentlyContinue | 
                Select-Object -Property @{Name='Protocol';Expression={'TCP'}}, LocalAddress, LocalPort, RemoteAddress, RemotePort, State
            $connections += $tcpConnections
        }
        else {
            $netstatOutput = netstat -ano | Select-String 'ESTABLISHED|LISTENING'
            foreach ($line in $netstatOutput) {
                $parts = $line -split '\s+' | Where-Object {$_}
                if ($parts.Count -ge 5) {
                    $connections += [PSCustomObject]@{
                        Protocol = $parts[0]
                        LocalAddress = $parts[1]
                        RemoteAddress = $parts[2]
                        State = $parts[3]
                        PID = $parts[4]
                    }
                }
            }
        }
        
        return $connections | Select-Object -First 100
    }
    catch {
        Write-ErrorMsg ('Failed to get network connections: ' + $_)
        return $null
    }
}

function Get-SoftwareList {
    try {
        $software = Get-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
            Where-Object {$_.DisplayName} |
            Select-Object -Property DisplayName, DisplayVersion, Publisher, InstallDate |
            Sort-Object -Property DisplayName
        
        return $software | Select-Object -First 100
    }
    catch {
        Write-ErrorMsg ('Failed to get software list: ' + $_)
        return $null
    }
}

function Get-SystemInfo {
    try {
        $osInfo = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction SilentlyContinue
        $computerInfo = Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction SilentlyContinue
        
        $sysInfo = [PSCustomObject]@{
            ComputerName = $env:COMPUTERNAME
            OSName = $osInfo.Caption
            OSVersion = $osInfo.Version
            OSBuild = $osInfo.BuildNumber
            Manufacturer = $computerInfo.Manufacturer
            Model = $computerInfo.Model
            Processors = $computerInfo.NumberOfProcessors
            LogicalCores = $computerInfo.NumberOfLogicalProcessors
            TotalMemory_GB = [math]::Round($computerInfo.TotalPhysicalMemory / 1GB, 2)
            InstallDate = $osInfo.InstallDate
            LastBootUpTime = $osInfo.LastBootUpTime
            TimeZone = [System.TimeZoneInfo]::Local.DisplayName
            CurrentUser = $env:USERNAME
            Domain = $env:USERDOMAIN
            PowerShellVersion = $PSVersionTable.PSVersion.ToString()
        }
        
        return $sysInfo
    }
    catch {
        Write-ErrorMsg ('Failed to get system info: ' + $_)
        return $null
    }
}

function Get-FirewallRules {
    try {
        $rules = Get-NetFirewallRule -ErrorAction SilentlyContinue | 
            Select-Object -Property Name, DisplayName, Enabled, Action, Direction |
            Where-Object {$_.Enabled} |
            Select-Object -First 50
        
        return $rules
    }
    catch {
        Write-ErrorMsg ('Failed to get firewall rules: ' + $_)
        return $null
    }
}

function Get-ScheduledTasks {
    try {
        $tasks = Get-ScheduledTask -ErrorAction SilentlyContinue | 
            Select-Object -Property TaskName, State, LastRunTime, NextRunTime, Author |
            Where-Object {$_.State -eq 'Ready'} |
            Select-Object -First 50
        
        return $tasks
    }
    catch {
        Write-ErrorMsg ('Failed to get scheduled tasks: ' + $_)
        return $null
    }
}

function Get-EventLogs {
    try {
        $events = Get-EventLog -LogName System -Newest 50 -ErrorAction SilentlyContinue | 
            Select-Object -Property TimeGenerated, Type, EventID, Source, Message
        
        return $events
    }
    catch {
        Write-ErrorMsg ('Failed to get event logs: ' + $_)
        return $null
    }
}

function Take-Snapshot {
    param(
        [ValidateSet('full', 'processes', 'network', 'software', 'system', 'firewall', 'tasks', 'logs')]
        [string]$Type = 'full'
    )
    
    Write-Info ('Taking ' + $Type + ' snapshot...')
    
    $snapshot = [PSCustomObject]@{
        Timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        Type = $Type
        Data = @{}
    }
    
    if ($Type -in 'full', 'processes') {
        $snapshot.Data['Processes'] = Get-ProcessList
    }
    
    if ($Type -in 'full', 'network') {
        $snapshot.Data['Network'] = Get-NetworkConnections
    }
    
    if ($Type -in 'full', 'software') {
        $snapshot.Data['Software'] = Get-SoftwareList
    }
    
    if ($Type -in 'full', 'system') {
        $snapshot.Data['System'] = Get-SystemInfo
    }
    
    if ($Type -in 'full', 'firewall') {
        $snapshot.Data['Firewall'] = Get-FirewallRules
    }
    
    if ($Type -in 'full', 'tasks') {
        $snapshot.Data['Tasks'] = Get-ScheduledTasks
    }
    
    if ($Type -in 'full', 'logs') {
        $snapshot.Data['EventLogs'] = Get-EventLogs
    }
    
    $Global:Snapshots += $snapshot
    Write-Success ('Snapshot #' + $Global:Snapshots.Count + ' taken')
    
    return $snapshot
}

function Show-Snapshots {
    if ($Global:Snapshots.Count -eq 0) {
        Write-ErrorMsg 'No snapshots taken yet'
        return
    }
    
    Write-Title 'Snapshots'
    Write-Host 'Index | Type    | Timestamp           | Items Captured' -ForegroundColor Cyan
    Write-Host ('-' * 65) -ForegroundColor Cyan
    
    foreach ($snap in $Global:Snapshots) {
        $index = $Global:Snapshots.IndexOf($snap)
        $itemCount = ($snap.Data.Keys | Measure-Object).Count
        $line = $index.ToString().PadRight(5) + ' | ' + $snap.Type.PadRight(7) + ' | ' + $snap.Timestamp + ' | ' + $itemCount + ' data types'
        Write-Host $line -ForegroundColor White
    }
}

function Export-Snapshot {
    param(
        [string]$FileName = 'guardian_export.json'
    )
    
    if ($Global:Snapshots.Count -eq 0) {
        Write-ErrorMsg 'No snapshots to export'
        return
    }
    
    try {
        $export = [PSCustomObject]@{
            ExportTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            ComputerName = $env:COMPUTERNAME
            SnapshotCount = $Global:Snapshots.Count
            Snapshots = $Global:Snapshots
        }
        
        $json = $export | ConvertTo-Json -Depth 10
        $json | Out-File -FilePath $FileName -Encoding UTF8
        
        Write-Success ('Exported to ' + $FileName)
    }
    catch {
        Write-ErrorMsg ('Export failed: ' + $_)
    }
}

function Invoke-Command {
    param([string]$CommandString)
    
    if ([string]::IsNullOrWhiteSpace($CommandString)) {
        return
    }
    
    $Global:History += $CommandString
    
    try {
        Invoke-Expression $CommandString | Format-List -AutoSize
    }
    catch {
        Write-ErrorMsg ('Command failed: ' + $_)
    }
}

function Show-Help {
    Write-Title 'Guardian DFIR CLI - Command Reference'
    $helpText = @'
DFIR Collection Commands:
  processes (p)         - List running processes
  network (n)           - Show network connections
  software (s)          - List installed software
  sysinfo (sys)         - Display system information
  firewall (fw)         - Show firewall rules
  tasks (t)             - List scheduled tasks
  logs (l)              - Show recent event logs

Snapshot Commands:
  snapshot [type]       - Take a forensic snapshot
  snapshots             - List all snapshots
  export [filename]     - Export snapshots to JSON

System Commands:
  run [command]         - Execute arbitrary PowerShell command
  history (hist)        - Show command history
  help (?)              - Show this help
  exit (quit, q)        - Exit Guardian

Examples:
  snapshot full
  processes
  export my_forensics.json
  run Get-LocalUser
'@
    Write-Host $helpText -ForegroundColor White
}

function Start-GuardianShell {
    Write-Host '' -ForegroundColor White
    Write-Host '╔══════════════════════════════════════════════════════════╗' -ForegroundColor Green
    Write-Host '║         Guardian DFIR CLI - PowerShell Native          ║' -ForegroundColor Green
    Write-Host '║                   Version 0.3.0                          ║' -ForegroundColor Green
    Write-Host '╚══════════════════════════════════════════════════════════╝' -ForegroundColor Green
    Write-Host '' -ForegroundColor Cyan
    Write-Host 'Type help for commands. exit to quit.' -ForegroundColor Cyan
    Write-Host '' -ForegroundColor White
    
    while ($true) {
        Write-Host '(guardian) ' -ForegroundColor Yellow -NoNewline
        $input = Read-Host
        
        $cmd = $input.Trim().ToLower()
        
        if ([string]::IsNullOrWhiteSpace($cmd)) {
            continue
        }
        
        switch -Regex ($cmd) {
            '^help$|^\?$' {
                Show-Help
            }
            '^processes$|^p$' {
                Write-Title 'Running Processes'
                Get-ProcessList | Format-Table -AutoSize
            }
            '^network$|^n$' {
                Write-Title 'Network Connections'
                Get-NetworkConnections | Format-Table -AutoSize
            }
            '^software$|^s$' {
                Write-Title 'Installed Software'
                Get-SoftwareList | Format-Table -AutoSize
            }
            '^sysinfo$|^sys$' {
                Write-Title 'System Information'
                Get-SystemInfo | Format-List
            }
            '^firewall$|^fw$' {
                Write-Title 'Firewall Rules'
                Get-FirewallRules | Format-Table -AutoSize
            }
            '^tasks$|^t$' {
                Write-Title 'Scheduled Tasks'
                Get-ScheduledTasks | Format-Table -AutoSize
            }
            '^logs$|^l$' {
                Write-Title 'Event Logs'
                Get-EventLogs | Format-Table -AutoSize
            }
            '^snapshot\s+' {
                $type = $cmd -replace '^snapshot\s+', ''
                Take-Snapshot -Type $type
            }
            '^snapshot$' {
                Take-Snapshot -Type 'full'
            }
            '^snapshots$' {
                Show-Snapshots
            }
            '^export\s+' {
                $filename = $cmd -replace '^export\s+', ''
                Export-Snapshot -FileName $filename
            }
            '^export$' {
                Export-Snapshot
            }
            '^history$|^hist$' {
                Write-Title 'Command History'
                $i = 1
                foreach ($c in $Global:History) {
                    Write-Host ($i.ToString() + ' : ' + $c) -ForegroundColor White
                    $i++
                }
            }
            '^run\s+' {
                $cmdToRun = $cmd -replace '^run\s+', ''
                Invoke-Command -CommandString $cmdToRun
            }
            '^exit$|^quit$|^q$' {
                Write-Host '' -ForegroundColor Green
                Write-Host 'Exiting Guardian...' -ForegroundColor Green
                break
            }
            default {
                Write-ErrorMsg ('Unknown command: ' + $cmd + '. Type help for commands.')
            }
        }
    }
}

Start-GuardianShell
