# Guardian - DFIR CLI Project Structure

## Project Overview

**Guardian** is a forensic analysis CLI tool designed for Digital Forensics and Incident Response (DFIR) using native operating system commands with **zero external dependencies**.

### Key Design Principles

1. **Zero External Dependencies** - Uses only Python standard library (3.10+)
2. **Native Commands** - Leverages `tasklist`, `netstat`, `wmic`, `ps`, `ss`, etc.
3. **Cross-Platform** - Supports Windows, macOS, and Linux
4. **Forensic-Ready** - Snapshot and comparison capabilities for timeline analysis
5. **Export-Friendly** - JSON export for integration with other tools

## Directory Structure

```
Guardian/
├── run.py                      # CLI entry point
├── tests.py                    # Test suite
├── requirements.txt            # Empty - no external deps!
├── README.md                   # User documentation
├── PROJECT_STRUCTURE.md        # This file
│
└── src/dfir_cli/              # Main package
    ├── __init__.py            # Package initialization
    ├── cli.py                 # Interactive shell (cmd module)
    ├── commands.py            # Shell command execution wrapper
    ├── bootstrap.py           # File download with SHA256 validation
    ├── windows_native.py      # Native OS commands abstraction
    ├── analyzer.py            # Forensic snapshot & analysis
    └── __pycache__/           # Python bytecode cache
```

## Module Descriptions

### `run.py`
- **Purpose**: Entry point for the application
- **Usage**: `python3 run.py`
- **Functionality**: Initializes the interactive DFIR shell

### `src/dfir_cli/cli.py`
- **Class**: `DFIRShell` (extends `cmd.Cmd`)
- **Purpose**: Interactive command-line interface
- **Commands**:
  - `processes` - List running processes
  - `network` - Show network connections
  - `software` - List installed software (Windows)
  - `sysinfo` - Display system information
  - `snapshot` - Take forensic snapshot
  - `snapshots` - List all snapshots
  - `export` - Export snapshots to JSON
  - `run` - Execute shell commands
  - `bootstrap` - Download and verify files
  - `history` - Show command history
  - `help` - Display help
  - `exit` - Exit the CLI

### `src/dfir_cli/windows_native.py`
- **Purpose**: Abstraction layer for native OS commands
- **Key Functions**:
  - `is_windows()` - Platform detection
  - `run_command()` - Execute shell commands
  - `get_processes()` - List running processes
  - `get_network_connections()` - Show network state
  - `get_installed_software()` - List software (Windows)
  - `get_system_info()` - System configuration
  - `get_firewall_rules()` - Firewall status (Windows)
  - `get_scheduled_tasks()` - Scheduled tasks
- **Native Commands Used**:
  - Windows: `tasklist`, `netstat`, `wmic`, `systeminfo`, `netsh`
  - Unix: `ps`, `ss`, `uname`

### `src/dfir_cli/analyzer.py`
- **Class**: `DFIRAnalyzer`
- **Purpose**: Forensic analysis and snapshot management
- **Key Methods**:
  - `take_snapshot()` - Capture system state point-in-time
  - `compare_snapshots()` - Detect changes between snapshots
  - `export_json()` - Export snapshots to JSON file
  - `list_snapshots()` - Display all snapshots
- **Snapshot Types**:
  - `full` - Complete system capture
  - `processes` - Process listing only
  - `network` - Network connections only
  - `software` - Software inventory only
  - `system` - System information only

### `src/dfir_cli/commands.py`
- **Purpose**: Shell command execution utility
- **Function**: `execute()` - Run commands with timeout and capture output
- **Return**: (returncode, stdout, stderr)

### `src/dfir_cli/bootstrap.py`
- **Purpose**: Secure file download and validation
- **Function**: `download_bootstrap()` - Download file with optional SHA256 verification
- **Dependencies**: `urllib` (stdlib only)
- **Features**:
  - Stream-based download (memory efficient)
  - SHA256 checksum validation
  - File permission management
  - Cross-platform support

## Command Workflow Examples

### Taking a Forensic Snapshot
```
(dfir) snapshot full
Snapshot taken at 2026-03-09T10:35:21.799163
Type: full
Data captures: processes, network, software, system, firewall, scheduled_tasks
```

### Exporting for Analysis
```
(dfir) export forensic_report.json
Snapshots exported to forensic_report.json
```

### Running Shell Commands
```
(dfir) run tasklist /v
[detailed process output]
[exit:0]
```

### Listing Processes
```
(dfir) processes
Image                | PID       | Session Name     | Session# | Mem Usage
[process table...]
... and 530 more processes
```

## Testing

The project includes a comprehensive test suite in `tests.py`:

```bash
python3 tests.py
```

**Tests Coverage**:
- Module imports
- Snapshot functionality
- JSON export
- System information gathering
- Process listing
- Network connection detection

## Architecture Decisions

### Why Zero Dependencies?
- **Portability**: Works anywhere Python 3.10+ is installed
- **Security**: No third-party library risks
- **Performance**: Minimal overhead
- **Forensic Integrity**: Known, auditable codebase

### Why Native Commands?
- **Accuracy**: Direct OS data
- **Compatibility**: Works on all systems
- **Performance**: Lightweight
- **Forensic Value**: Authentic system artifacts

### Why cmd Module (Instead of Click/Typer)?
- **Stdlib Only**: Zero dependencies
- **Interactive**: Natural REPL experience
- **Extensible**: Easy to add subcommands
- **Familiar**: Similar to shell environments

## Performance Characteristics

- **Startup Time**: <100ms
- **Process Listing**: <1 second (Linux), <3 seconds (Windows)
- **Network Enumeration**: <2 seconds
- **Full Snapshot**: <10 seconds
- **JSON Export**: <500ms

## Security Considerations

⚠️ **Important**: This tool provides deep system access.

- Use in controlled forensic environments only
- Ensure proper authorization
- Be careful with `run` command - it executes arbitrary commands
- Audit exported data - may contain sensitive information
- Snapshots maintain audit trails via timestamps

## Future Enhancements

Planned features (maintaining zero external dependencies):

- [ ] Windows Registry parsing
- [ ] Event Log analysis (Windows)
- [ ] Memory analysis integration
- [ ] Plugin system for custom commands
- [ ] Web-based dashboard for reports
- [ ] Timeline visualization
- [ ] Artifact hashing (MD5/SHA256)
- [ ] Configuration profiles

## Contributing Guidelines

When contributing to Guardian:

1. **No External Dependencies** - Use only Python stdlib
2. **Cross-Platform** - Support Windows, macOS, Linux
3. **Forensic-Ready** - Maintain audit trails
4. **Testing** - Add tests for new features
5. **Documentation** - Document native commands used
6. **Performance** - Keep overhead minimal

## License

MIT License - Free for forensic use and research.

---

**Last Updated**: March 9, 2026
**Version**: 0.2.0
**Python Required**: 3.10+
