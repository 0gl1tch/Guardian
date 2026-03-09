# DFIR CLI - Quick Start Guide

## Installation

No installation required! Just run:

```bash
cd Guardian
python3 run.py
```

That's it. No `pip install`, no dependencies.

## Basic Usage

```bash
# Start the interactive CLI
python3 run.py

# You'll see this prompt:
# DFIR CLI — Forensic toolkit using native commands. Type 'help' for commands.
# (dfir) _
```

## Essential Commands

### View Running Processes
```bash
(dfir) processes
```
Shows all running processes in a formatted table.

### Check Network Connections
```bash
(dfir) network
```
Displays active network connections with PIDs and states.

### Get System Information
```bash
(dfir) sysinfo
```
Shows OS, Python version, and system details.

### Take a Forensic Snapshot
```bash
(dfir) snapshot full
```
Captures current system state (processes, network, software, etc).

**Snapshot types**:
- `full` - Everything
- `processes` - Only processes
- `network` - Only network connections
- `software` - Only installed software
- `system` - Only system info

### Export Results to JSON
```bash
(dfir) export report.json
```
Saves all snapshots to a JSON file for later analysis.

### Run Custom Commands
```bash
(dfir) run tasklist /v
(dfir) run "netstat -ano"
(dfir) run ps aux
```
Execute any shell command and see the output.

### View Command History
```bash
(dfir) history
```
Shows all commands executed in this session.

## Advanced Usage

### List All Snapshots
```bash
(dfir) snapshots
```
Shows all snapshots taken so far with timestamps.

### Download and Verify Files
```bash
(dfir) bootstrap https://example.com/script.sh output.sh abc123hash
```
Downloads a file and verifies its SHA256 checksum.

### JSON Output
All listing commands support `--json` for automation:
```bash
(dfir) processes --json
(dfir) network --json
(dfir) software --json
```

## Common Workflows

### Incident Response
```bash
(dfir) snapshot full
(dfir) export initial_snapshot.json
(dfir) run powershell "Get-EventLog -LogName Security -Newest 100"
(dfir) export final_report.json
```

### System Audit
```bash
(dfir) sysinfo
(dfir) processes
(dfir) network
(dfir) software
(dfir) export audit_report.json
```

### Timeline Analysis
```bash
(dfir) snapshot processes
(dfir) run "dir /s /b /o:d"
(dfir) snapshot network
(dfir) export timeline.json
```

## Output Formats

### Human-Readable (Default)
```
(dfir) processes
Image                | PID       | Session Name     | Session# | Mem Usage
...
```

### JSON (Add --json)
```
(dfir) processes --json
[
  {
    "Image": "python.exe",
    "PID": "1234",
    ...
  },
  ...
]
```

## Keyboard Shortcuts

- **Ctrl+C** - Interrupt current command
- **Ctrl+D** or `exit` - Exit the CLI
- **Tab** - Auto-complete command names
- **↑/↓** - Command history navigation

## Tips & Tricks

1. **Use `run` for complex commands**:
   ```bash
   (dfir) run "tasklist | findstr python"
   ```

2. **Export before exit**:
   ```bash
   (dfir) export final_analysis.json
   (dfir) exit
   ```

3. **Chain snapshots**:
   ```bash
   (dfir) snapshot processes
   (dfir) snapshot network
   (dfir) snapshot software
   (dfir) export combined.json
   ```

4. **View help anytime**:
   ```bash
   (dfir) help
   (dfir) help processes
   (dfir) help snapshot
   ```

## Troubleshooting

### "Command not found"
Make sure you're using the correct command name:
```bash
(dfir) help  # Shows all available commands
```

### No processes/connections shown
On Windows, you might need admin privileges:
```bash
# Run Command Prompt as Administrator
python3 run.py
```

### "Cannot import" error
Ensure Python 3.10+ is installed:
```bash
python3 --version
```

## Exit the CLI

```bash
(dfir) exit
```

Or press Ctrl+D.

## Files Created

When you export, files are saved in the current directory:
- `forensic_report.json` - Your exported snapshot data
  - Can be opened in any text editor
  - Can be processed by Python, Node.js, etc.
  - Compact format for storage or transmission

## Next Steps

- Explore each command with `help <command>`
- Practice taking snapshots
- Export results and examine the JSON
- Automate analysis with the JSON output

---

**Quick Command Reference**:
```
processes  - List running processes
network    - Show network connections
software   - List installed software
sysinfo    - Show system info
snapshot   - Take forensic snapshot
snapshots  - List all snapshots
export     - Export to JSON
run        - Execute shell command
bootstrap  - Download file with verification
history    - Show command history
help       - Show all commands
exit       - Exit CLI
```

Need more? Type `help` inside the CLI!
