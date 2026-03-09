"""
Windows-native DFIR commands using built-in tools.
Supports tasklist, netstat, wmic, Get-Process (PowerShell), etc.
"""
import subprocess
import platform
import json
from typing import Dict, List, Tuple


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def run_command(cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
    """Execute a command and return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
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
    """Get list of running processes.
    Works on Windows (tasklist) and Unix (ps).
    """
    if is_windows():
        code, out, err = run_command("tasklist /v /fo csv")
        if code != 0:
            return []
        
        processes = []
        lines = out.strip().split('\n')
        if len(lines) > 1:
            # Parse CSV header
            header = [h.strip('"') for h in lines[0].split('","')]
            for line in lines[1:]:
                values = [v.strip('"') for v in line.split('","')]
                if len(values) == len(header):
                    proc = dict(zip(header, values))
                    processes.append(proc)
        return processes
    else:
        # Unix fallback
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
    """Get active network connections.
    Windows: netstat -ano
    Unix: netstat -tlnp or ss -tlnp
    """
    if is_windows():
        code, out, err = run_command("netstat -ano")
    else:
        code, out, err = run_command("ss -tlnp 2>/dev/null || netstat -tlnp")
    
    if code != 0:
        return []
    
    connections = []
    lines = out.strip().split('\n')
    
    # Skip header lines and parse connections
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
    """Get installed software (Windows only using registry/wmic)."""
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
