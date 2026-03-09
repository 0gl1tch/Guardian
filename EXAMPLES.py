"""
Example usage scripts for DFIR CLI.
Run these examples after starting the CLI with: python3 run.py
"""

# EXAMPLE 1: Quick System Overview
"""
# Get a complete picture of the current system
(dfir) sysinfo
(dfir) processes
(dfir) network
(dfir) software
"""

# EXAMPLE 2: Take a Full Forensic Snapshot
"""
# Capture a point-in-time snapshot for forensic analysis
(dfir) snapshot full
(dfir) snapshots
(dfir) export forensic_baseline.json
"""

# EXAMPLE 3: Process Analysis
"""
# Look at processes with different filters
(dfir) processes
(dfir) processes --json > processes.json
(dfir) run "tasklist | findstr python"
"""

# EXAMPLE 4: Network Investigation
"""
# Analyze network connections for suspicious activity
(dfir) network
(dfir) network --json
(dfir) run "netstat -ano | findstr ESTABLISHED"
"""

# EXAMPLE 5: Timeline Creation
"""
# Build a timeline by taking multiple snapshots
(dfir) snapshot processes
(dfir) run "dir /s /o:d /b"
(dfir) snapshot network
(dfir) snapshot software
(dfir) export timeline.json
"""

# EXAMPLE 6: Incident Response
"""
# Complete IR workflow
(dfir) snapshot full
(dfir) export ir_snapshot_initial.json
(dfir) run "tasklist /v"
(dfir) run "netstat -ano"
(dfir) run "systeminfo"
(dfir) snapshot full
(dfir) export ir_snapshot_final.json
"""

# EXAMPLE 7: Persistence Mechanisms
"""
# Check for common persistence techniques
(dfir) run "reg query HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
(dfir) run "Get-ScheduledTask | Select TaskName, State"
(dfir) snapshot full
(dfir) export persistence_check.json
"""

# EXAMPLE 8: Software Inventory
"""
# Create a complete software audit
(dfir) software
(dfir) software --json
(dfir) export software_inventory.json
"""

# EXAMPLE 9: Multi-Point Timeline
"""
# Capture multiple snapshots over time for comparison
(dfir) snapshot full
(dfir) run "ping google.com"
(dfir) snapshot full
(dfir) run "ipconfig /all"
(dfir) snapshot network
(dfir) export multi_timeline.json
"""

# EXAMPLE 10: Automated Report Generation
"""
# Full forensic report in one go
(dfir) snapshot full
(dfir) run "systeminfo > system_report.txt"
(dfir) run "tasklist /v > processes_report.txt"
(dfir) run "netstat -ano > network_report.txt"
(dfir) export forensic_report.json
(dfir) history > history.log
"""

# ADDITIONAL COMMANDS FOR MANUAL INVESTIGATION
"""
# Check for rootkits/suspicious processes
(dfir) run "Get-Process | Where-Object {$_.Path -like '*temp*'}"

# List network listeners
(dfir) run "netstat -ab"

# Check firewall status
(dfir) run "netsh advfirewall show allprofiles"

# Event log analysis (Windows)
(dfir) run "Get-EventLog Security -Newest 50"

# File permissions check
(dfir) run "icacls C:\\Windows\\Temp"

# Running services
(dfir) run "Get-Service | Where-Object {$_.Status -eq 'Running'}"
"""

# USING JSON OUTPUT FOR AUTOMATION
"""
# These commands output JSON that can be processed by other tools
(dfir) processes --json | python3 analyze.py
(dfir) network --json | python3 check_suspicious.py
(dfir) export full_report.json
"""

# Example of processing JSON export with Python
"""
import json

with open('forensic_report.json', 'r') as f:
    data = json.load(f)
    
    for snapshot in data['snapshots']:
        print(f"Snapshot: {snapshot['timestamp']}")
        print(f"Type: {snapshot['type']}")
        
        if 'processes' in snapshot['data']:
            print(f"Processes: {len(snapshot['data']['processes'])}")
        
        if 'network' in snapshot['data']:
            print(f"Connections: {len(snapshot['data']['network'])}")
"""

# PYTHON SCRIPTING WITH DFIR CLI
"""
# You can also import and use DFIR CLI modules directly
from src.dfir_cli.analyzer import DFIRAnalyzer
from src.dfir_cli.windows_native import get_processes, get_network_connections

analyzer = DFIRAnalyzer()

# Take snapshots
snap1 = analyzer.take_snapshot('full')
print(f"Snapshot 1: {snap1['timestamp']}")

# Do something...
import time
time.sleep(5)

snap2 = analyzer.take_snapshot('full')
print(f"Snapshot 2: {snap2['timestamp']}")

# Compare
comparison = analyzer.compare_snapshots(0, 1)
print(f"Changes: {comparison['changes']}")

# Export
analyzer.export_json('comparison_report.json')
"""

print("See examples above for DFIR CLI usage patterns!")
