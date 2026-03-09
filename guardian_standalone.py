#!/usr/bin/env python3
"""
Guardian DFIR CLI - Standalone version
Complete self-contained application for remote execution via Python one-liner
"""
import cmd
import shlex
import sys
import json
import subprocess
import platform
import os
from datetime import datetime
from typing import Dict, List, Tuple

# ============================================================================
# NATIVE COMMANDS MODULE
# ============================================================================

def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def run_command(cmd_str: str, timeout: int = 30) -> Tuple[int, str, str]:
    """Execute a command and return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd_str,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "Command timeout"
    except Exception as e:
        return 1, "", str(e)


def get_processes() -> List[Dict]:
    """Get list of running processes."""
    if is_windows():
        code, out, err = run_command("tasklist /v /fo csv")
        if code != 0:
            return []
        
        processes = []
        lines = out.strip().split('\n')
        if len(lines) > 1:
            header = [h.strip('"') for h in lines[0].split('","')]
            for line in lines[1:]:
                values = [v.strip('"') for v in line.split('","')]
                if len(values) == len(header):
                    proc = dict(zip(header, values))
                    processes.append(proc)
        return processes
    else:
        code, out, err = run_command("ps aux")
        if code != 0:
            return []
        
        processes = []
        lines = out.strip().split('\n')
        if lines:
            header = lines[0].split()
            for line in lines[1:]:
                parts = line.split(None, len(header) - 1)
                if len(parts) >= len(header):
                    proc = dict(zip(header, parts))
                    processes.append(proc)
        return processes


def get_network_connections() -> List[Dict]:
    """Get active network connections."""
    if is_windows():
        code, out, err = run_command("netstat -ano")
    else:
        code, out, err = run_command("ss -tlnp 2>/dev/null || netstat -tlnp")
    
    if code != 0:
        return []
    
    connections = []
    lines = out.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or 'Proto' in line or 'Active' in line:
            continue
        parts = line.split()
        if len(parts) >= 4:
            conn = {
                "protocol": parts[0],
                "local_address": parts[1],
                "remote_address": parts[2] if len(parts) > 2 else "N/A",
                "state": parts[3] if len(parts) > 3 else "N/A",
                "pid": parts[-1] if parts[-1].isdigit() else "N/A",
            }
            connections.append(conn)
    
    return connections


def get_installed_software() -> List[Dict]:
    """Get installed software (Windows only)."""
    if not is_windows():
        return []
    
    code, out, err = run_command('wmic product list brief /format:csv')
    if code != 0:
        return []
    
    software = []
    lines = out.strip().split('\n')
    if len(lines) > 1:
        header = lines[0].split(',')
        for line in lines[1:]:
            if line.strip():
                values = line.split(',')
                if len(values) == len(header):
                    soft = dict(zip(header, values))
                    software.append(soft)
    
    return software


def get_system_info() -> Dict:
    """Get system information."""
    info = {"os": platform.system(), "platform": platform.platform(), "python": platform.python_version()}
    
    if is_windows():
        code, out, err = run_command('systeminfo')
        if code == 0:
            info["systeminfo"] = out
    else:
        code, out, err = run_command('uname -a')
        if code == 0:
            info["uname"] = out.strip()
    
    return info


def get_firewall_rules() -> List[str]:
    """Get Windows firewall rules (Windows only)."""
    if not is_windows():
        return []
    
    code, out, err = run_command('netsh advfirewall show allprofiles')
    if code == 0:
        return out.strip().split('\n')
    return []


def get_scheduled_tasks() -> List[Dict]:
    """Get scheduled tasks (Windows only)."""
    if not is_windows():
        return []
    
    code, out, err = run_command('tasklist /svc /fo csv')
    if code != 0:
        return []
    
    tasks = []
    lines = out.strip().split('\n')
    if len(lines) > 1:
        for line in lines[1:]:
            parts = [p.strip('"') for p in line.split('","')]
            if len(parts) >= 2:
                tasks.append({"image": parts[0], "pid": parts[1], "services": parts[2] if len(parts) > 2 else ""})
    
    return tasks


# ============================================================================
# ANALYZER MODULE
# ============================================================================

class DFIRAnalyzer:
    """Forensic analysis wrapper for native system commands."""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.platform = "Windows" if is_windows() else "Unix-like"
        self.snapshots = []
    
    def take_snapshot(self, snapshot_type: str = "full") -> Dict:
        """Take a snapshot of the system for forensic analysis."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "type": snapshot_type,
            "data": {}
        }
        
        if snapshot_type in ["full", "processes"]:
            snapshot["data"]["processes"] = get_processes()
        
        if snapshot_type in ["full", "network"]:
            snapshot["data"]["network"] = get_network_connections()
        
        if snapshot_type in ["full", "software"]:
            snapshot["data"]["software"] = get_installed_software()
        
        if snapshot_type in ["full", "system"]:
            snapshot["data"]["system"] = get_system_info()
        
        if snapshot_type == "full":
            snapshot["data"]["firewall"] = get_firewall_rules()
            snapshot["data"]["scheduled_tasks"] = get_scheduled_tasks()
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def compare_snapshots(self, snap1_idx: int, snap2_idx: int) -> Dict:
        """Compare two snapshots to find changes."""
        if snap1_idx >= len(self.snapshots) or snap2_idx >= len(self.snapshots):
            return {"error": "Snapshot index out of range"}
        
        snap1 = self.snapshots[snap1_idx]["data"]
        snap2 = self.snapshots[snap2_idx]["data"]
        
        comparison = {
            "from": self.snapshots[snap1_idx]["timestamp"],
            "to": self.snapshots[snap2_idx]["timestamp"],
            "changes": {}
        }
        
        if "processes" in snap1 and "processes" in snap2:
            pids1 = {p.get("Image", p.get("Name", "")): p for p in snap1["processes"]}
            pids2 = {p.get("Image", p.get("Name", "")): p for p in snap2["processes"]}
            
            comparison["changes"]["new_processes"] = [p for p in pids2 if p not in pids1]
            comparison["changes"]["terminated_processes"] = [p for p in pids1 if p not in pids2]
        
        return comparison
    
    def export_json(self, filename: str) -> bool:
        """Export all snapshots to JSON file."""
        try:
            with open(filename, "w") as f:
                json.dump({
                    "platform": self.platform,
                    "export_time": datetime.now().isoformat(),
                    "snapshots": self.snapshots
                }, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False
    
    def list_snapshots(self) -> List:
        """List all snapshots taken."""
        return [
            {
                "index": i,
                "timestamp": snap["timestamp"],
                "type": snap["type"],
                "data_keys": list(snap["data"].keys())
            }
            for i, snap in enumerate(self.snapshots)
        ]


# ============================================================================
# BOOTSTRAP MODULE
# ============================================================================

def download_bootstrap(url: str, dest: str = "bootstrap.sh", verify_sha256: str = None, timeout: int = 15):
    """Download a bootstrap script with optional SHA256 verification."""
    import urllib.request
    import urllib.error
    import hashlib
    
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
    except urllib.error.URLError as e:
        if os.path.exists(dest):
            os.remove(dest)
        raise RuntimeError(f"Failed to download from {url}: {e}")

    if verify_sha256:
        h = hashlib.sha256()
        with open(dest, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        actual = h.hexdigest()
        if actual != verify_sha256:
            os.remove(dest)
            raise ValueError(f"sha256 mismatch: expected {verify_sha256}, got {actual}")

    if platform.system() != "Windows":
        os.chmod(dest, 0o750)
    
    return dest


def execute(cmd_str: str, timeout: int = 600):
    """Execute a shell command and return (returncode, stdout, stderr)."""
    try:
        p = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)


# ============================================================================
# INTERACTIVE SHELL
# ============================================================================

class DFIRShell(cmd.Cmd):
    intro = "🛡️  Guardian DFIR CLI - Forensic toolkit (no dependencies)\nType 'help' for commands."
    prompt = "(guardian) "

    def __init__(self):
        super().__init__()
        self.history = []
        self.analyzer = DFIRAnalyzer()

    def do_run(self, arg: str):
        """run <command> - Execute a shell command"""
        cmdline = arg.strip()
        if not cmdline:
            print("usage: run <command>")
            return
        self.history.append(cmdline)
        code, out, err = execute(cmdline)
        if out:
            print(out, end="")
        if err:
            print(err, file=sys.stderr, end="")
        print(f"[exit:{code}]")

    def do_bootstrap(self, arg: str):
        """bootstrap <url> [dest] [sha256] - Download and verify files"""
        parts = shlex.split(arg)
        if not parts:
            print("usage: bootstrap <url> [dest] [sha256]")
            return
        url = parts[0]
        dest = parts[1] if len(parts) > 1 else "bootstrap.sh"
        verify = parts[2] if len(parts) > 2 else None
        try:
            download_bootstrap(url, dest, verify)
            print(f"Downloaded to {dest}")
        except Exception as e:
            print("Error:", e)

    def do_history(self, arg: str):
        """history - Show command history"""
        for i, c in enumerate(self.history, 1):
            print(f"{i}: {c}")

    def do_processes(self, arg: str):
        """processes [--json] - List running processes"""
        procs = get_processes()
        if "--json" in arg:
            print(json.dumps(procs, indent=2, default=str))
        else:
            if not procs:
                print("No processes found")
                return
            
            keys = list(procs[0].keys())[:5]
            print(" | ".join(f"{k:20}" for k in keys))
            print("-" * (22 * len(keys)))
            for proc in procs[:20]:
                values = [str(proc.get(k, ""))[:20] for k in keys]
                print(" | ".join(f"{v:20}" for v in values))
            if len(procs) > 20:
                print(f"... and {len(procs) - 20} more processes")

    def do_network(self, arg: str):
        """network [--json] - Show network connections"""
        conns = get_network_connections()
        if "--json" in arg:
            print(json.dumps(conns, indent=2, default=str))
        else:
            if not conns:
                print("No connections found")
                return
            
            print(f"{'Protocol':<10} {'Local Address':<25} {'Remote Address':<25} {'State':<15} {'PID':<8}")
            print("-" * 85)
            for conn in conns[:30]:
                print(f"{conn.get('protocol', 'N/A'):<10} {conn.get('local_address', 'N/A'):<25} "
                      f"{conn.get('remote_address', 'N/A'):<25} {conn.get('state', 'N/A'):<15} "
                      f"{conn.get('pid', 'N/A'):<8}")
            if len(conns) > 30:
                print(f"... and {len(conns) - 30} more connections")

    def do_software(self, arg: str):
        """software [--json] - List installed software"""
        soft = get_installed_software()
        if not soft:
            print("No software found or not supported on this OS")
            return
        
        if "--json" in arg:
            print(json.dumps(soft, indent=2, default=str))
        else:
            for item in soft[:20]:
                print(f"  • {item.get('Name', item.get('Description', 'Unknown'))}")
            if len(soft) > 20:
                print(f"... and {len(soft) - 20} more")

    def do_sysinfo(self, arg: str):
        """sysinfo - Show system information"""
        info = get_system_info()
        for key, value in info.items():
            if key == "systeminfo":
                print(f"\n{key}:")
                truncated = value[:500] + "..." if len(value) > 500 else value
                print(truncated)
            else:
                print(f"{key}: {value}")

    def do_snapshot(self, arg: str):
        """snapshot [type] [--json] - Take forensic snapshot (full|processes|network|software|system)"""
        snap_type = "full"
        args = arg.split()
        if args and not args[0].startswith("--"):
            snap_type = args[0]
        
        snapshot = self.analyzer.take_snapshot(snap_type)
        
        if "--json" in arg:
            print(json.dumps(snapshot, indent=2, default=str))
        else:
            print(f"Snapshot taken at {snapshot['timestamp']}")
            print(f"Type: {snapshot['type']}")
            data_keys = ', '.join(snapshot['data'].keys())
            print(f"Data captures: {data_keys}")
            for key, data in snapshot['data'].items():
                if isinstance(data, list):
                    print(f"  {key}: {len(data)} items")
                else:
                    print(f"  {key}: captured")

    def do_snapshots(self, arg: str):
        """snapshots - List all snapshots"""
        snaps = self.analyzer.list_snapshots()
        if not snaps:
            print("No snapshots taken yet. Use 'snapshot' command.")
            return
        
        print(f"{'Index':<6} {'Timestamp':<30} {'Type':<12} {'Data':<40}")
        print("-" * 90)
        for snap in snaps:
            data_str = ', '.join(snap['data_keys'])[:40]
            print(f"{snap['index']:<6} {snap['timestamp']:<30} {snap['type']:<12} {data_str:<40}")

    def do_export(self, arg: str):
        """export <filename> - Export snapshots to JSON"""
        if not arg.strip():
            print("usage: export <filename>")
            return
        
        filename = arg.strip()
        if self.analyzer.export_json(filename):
            print(f"✓ Snapshots exported to {filename}")
        else:
            print(f"✗ Failed to export to {filename}")

    def do_exit(self, arg: str):
        """exit - Exit Guardian CLI"""
        print("Exiting Guardian DFIR CLI...")
        return True

    do_EOF = do_exit


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    try:
        DFIRShell().cmdloop()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
