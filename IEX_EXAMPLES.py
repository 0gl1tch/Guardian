#!/usr/bin/env python3
"""
Guardian IEX Execution Examples
Shows real-world usage via remote execution
"""

# ============================================================================
# EXAMPLE 1: Windows PowerShell - Basic IEX
# ============================================================================
"""
# On Windows (PowerShell as Administrator):
PS C:\Users\Admin> iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py')

🛡️  Guardian DFIR CLI - Forensic toolkit (no dependencies)
Type 'help' for commands.
(guardian) processes
Image                | PID       | Session Name     | Session# | Mem Usage
...
"""

# ============================================================================
# EXAMPLE 2: Linux Bash - Basic IEX
# ============================================================================
"""
# On Linux/macOS:
$ curl https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py | python3

🛡️  Guardian DFIR CLI - Forensic toolkit (no dependencies)
Type 'help' for commands.
(guardian) processes
USER       PID     %CPU %MEM    VSZ  
root         1     0.0  0.0  19196
...
"""

# ============================================================================
# EXAMPLE 3: Incident Response Workflow
# ============================================================================
"""
# Quick IR response - everything in-memory, no artifacts

# On Windows:
PS C:\> iex(New-Object Net.WebClient).DownloadString('http://ir-server:8080/guardian')
(guardian) snapshot full
(guardian) run "Get-EventLog Security -Newest 50"
(guardian) run "netstat -ano | findstr ESTABLISHED"
(guardian) export IR_snapshot_$(Get-Date -Format yyyyMMdd_HHmmss).json
(guardian) exit

# Result: IR_snapshot_20260309_153045.json created in current directory
# Once you copy it off the system, there's minimal evidence of Guardian
"""

# ============================================================================
# EXAMPLE 4: Automated Collection via SSH
# ============================================================================
"""
#!/bin/bash
# Remote forensic collection from multiple Linux servers

GUARDIAN_URL="https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

for server in web01 web02 web03 db01 db02; do
    echo "[*] Collecting from $server..."
    
    # SSH to remote, execute Guardian in-memory, collect results
    ssh root@$server << EOF
curl $GUARDIAN_URL | python3 << 'INNER'
snapshot full
export /tmp/forensics_${server}_${TIMESTAMP}.json
exit
INNER

# Copy collected data back
scp /tmp/forensics_${server}_${TIMESTAMP}.json collector@evidence-server:/evidence/
EOF
done
"""

# ============================================================================
# EXAMPLE 5: High-Performance Collection (No Export)
# ============================================================================
"""
# Just capture and analyze on-the-fly, no files left on disk

# PowerShell:
iex(New-Object Net.WebClient).DownloadString('http://ir:8080/guardian') << 'EOF'
processes
network
sysinfo
exit
EOF

# All output goes to PowerShell console, gets logged by logging systems if enabled
# No .json file created means minimal disk footprint
"""

# ============================================================================
# EXAMPLE 6: Chainable Commands (One-liner Collection)
# ============================================================================
"""
# Bash - Pipe commands directly to Guardian

curl http://ir-server:8080/guardian | python3 << 'EOF'
snapshot processes
snapshot network
snapshot system
export /tmp/forensics_complete.json
exit
EOF

# Or with output redirection
curl http://forensic-server:8080/guardian | python3 2>&1 | tee execution.log
"""

# ============================================================================
# EXAMPLE 7: Scheduled Forensic Collection
# ============================================================================
"""
#!/bin/bash
# Linux cron job - Periodic collection without leaving traces

# Add to crontab: 0 2 * * * /opt/forensics/collect.sh

#!/bin/bash
GUARDIAN_URL="https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py"

# Download, execute, and immediately clean up
curl -s $GUARDIAN_URL | python3 << 'EOF'
snapshot full
export /var/tmp/sys_$(date +%s).json
exit
EOF

# Copy to remote server and delete local copy
scp /var/tmp/sys_*.json forensic@evidence-server:~/
rm -f /var/tmp/sys_*.json
"""

# ============================================================================
# EXAMPLE 8: Integration with SIEM/EDR
# ============================================================================
"""
# PowerShell - Integrated with logging infrastructure

$GuardianURL = "http://ir-server:8080/guardian"
$Logfile = "C:\\Logs\\forensics_$(Get-Date -Format yyyyMMdd).log"

# Execute Guardian and log everything
iex(New-Object Net.WebClient).DownloadString($GuardianURL) | Tee-Object -FilePath $Logfile

# SIEM can monitor:
# - PowerShell process creation
# - Network connection to ir-server
# - File creation if export is used
# - Process list output
"""

# ============================================================================
# EXAMPLE 9: Comparison Snapshots (Detect Changes)
# ============================================================================
"""
# Windows - Take before/after snapshots to detect changes

PS C:\> iex(New-Object Net.WebClient).DownloadString('http://ir-server:8080/guardian')

# Initial baseline
(guardian) snapshot full
(guardian) export baseline_$(Get-Date -Format yyyyMMdd_HHmmss).json

# ... Do investigation or wait for incident ...

# After incident 
(guardian) snapshot full
(guardian) export after_$(Get-Date -Format yyyyMMdd_HHmmss).json

# Analysis: Compare baselines to find new processes, connections, etc.
"""

# ============================================================================
# EXAMPLE 10: Zero-Trust Network Execution
# ============================================================================
"""
# Works in restricted networks with Python + Internet only

# Environment: Corporate network with:
# - Python 3 installed (required)
# - No local admin needed
# - HTTP/HTTPS outbound allowed to your server
# - No PowerShell policy restrictions

# Just run:
curl https://your-ir-server.com/guardian | python3

# Works completely in-memory, requires minimal permissions
"""

print("""
Guardian DFIR CLI - IEX Execution Examples
============================================

These examples show real-world usage patterns for:
- Incident Response
- Forensic Collection
- Automated Scanning
- SIEM Integration
- Zero-Trust Networks

See DEPLOY.md for setup instructions
See REMOTE_EXECUTION.md for technical details

Quick Start:
  Windows: iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py')
  Linux:   curl https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py | python3
""")
