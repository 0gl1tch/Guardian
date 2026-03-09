# DFIR CLI - Forensic Toolkit

A powerful forensic analysis CLI tool using **native Windows/Unix commands** with **zero external dependencies**. 
Perfect for incident response, system analysis, and forensic investigations.

## 🚀 Quick Remote Execution (No Install)

Execute Guardian instantly from any system with internet access:

**Windows (PowerShell):**
```powershell
iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py')
```

**Linux/macOS (Bash):**
```bash
curl https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py | python3
```

👉 [Full deployment guide](DEPLOY.md) | [Technical details](REMOTE_EXECUTION.md)

## Features

### Zero External Dependencies
- Uses only Python standard library (Python 3.10+)
- No pip install required - just run it
- Fully portable across Windows, macOS, and Linux
- Works with native system commands: `tasklist`, `netstat`, `wmic`, `ps`, `ss`, etc.

### DFIR Commands
- **`processes`** - List running processes with detailed info
- **`network`** - Show active network connections with states and PIDs
- **`software`** - List installed software (Windows)
- **`sysinfo`** - Display system information
- **`snapshot`** - Take forensic snapshots for timeline analysis
- **`snapshots`** - List all snapshots taken
- **`export`** - Export snapshots to JSON for external analysis
- **`run <command>`** - Execute arbitrary shell commands
- **`bootstrap <url>`** - Download and verify bootstrap scripts
- **`history`** - View command history

## Installation & Usage

### Quick Start
```bash
# No installation needed!
python3 run.py
```

That's it! No pip, no dependencies.

### Examples

```bash
# Take a full system snapshot
(dfir) snapshot full

# View only process snapshot
(dfir) snapshot processes

# Export all snapshots to JSON
(dfir) export forensic_report.json

# List running processes
(dfir) processes

# Check network connections
(dfir) network

# Display as JSON for automation
(dfir) processes --json

# Run a shell command
(dfir) run dir
(dfir) run "tasklist /v"

# Download and verify a script
(dfir) bootstrap https://example.com/script.sh verify_script.sh abc123...hash...
```

## Architecture

```
Guardian/
├── run.py              # Entry point
├── requirements.txt    # Empty - no dependencies!
└── src/dfir_cli/
    ├── __init__.py
    ├── cli.py          # Interactive shell (cmd module)
    ├── commands.py     # Shell execution
    ├── bootstrap.py    # Download files (uses urllib)
    ├── windows_native.py   # Native OS commands wrapper
    └── analyzer.py     # Forensic analysis logic
```

## Forensic Analysis Features

### Snapshot System
Create point-in-time snapshots of system state:
- **full** - All available data
- **processes** - Running processes
- **network** - Network connections
- **software** - Installed applications  
- **system** - System information

### Snapshot Comparison
Compare snapshots to detect changes:
- New/terminated processes
- Network connection changes
- Software installation/removal

### JSON Export
Export complete forensic data for:
- External analysis tools
- Timeline reconstruction
- Compliance reporting
- Automated processing

## Windows Native Commands Used

- `tasklist /v` - Process information
- `netstat -ano` - Network connections
- `wmic product list` - Installed software
- `systeminfo` - System configuration
- `netsh advfirewall` - Firewall rules
- PowerShell compatible

## Unix/Linux Support

The tool automatically adapts to Unix-like systems:
- `ps aux` - Process listing
- `ss -tlnp` / `netstat -tlnp` - Network
- `uname -a` - System info
- Cross-platform snapshot capability

## Security Notes

⚠️ This tool provides powerful system access:
- Use in controlled forensic environments
- Ensure proper authorization before analysis
- Be cautious with command execution
- Audit trail is maintained in snapshots and export files

## Project Goals

✅ **Achieved**
- Zero external dependencies
- Native command integration
- Forensic snapshot capability
- Cross-platform support
- JSON export for automation

🎯 **Future Enhancements**
- Registry analysis (Windows)
- Event log parsing
- Memory analysis integration
- Plugin system for custom commands
- Web dashboard for reports
- Integration with OSINT databases

## License

MIT License - Use freely in your forensic investigations.

## Support

For issues or contributions, please ensure:
1. No new external dependencies introduced
2. Maintain zero-pip-install requirement
3. Support both Windows and Unix platforms
4. Include native command fallbacks

---

**Guardian** - Your forensic analysis companion powered by native commands.
