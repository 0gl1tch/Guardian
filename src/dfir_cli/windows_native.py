"""
Windows-native DFIR commands using built-in tools.
Supports tasklist, netstat, wmic, Get-Process (PowerShell), etc.
"""
import subprocess
import platform
import json
import re
import socket
from typing import Dict, List, Tuple, Optional


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


def _extract_ipv4_from_ipconfig(output: str) -> Optional[str]:
    for line in output.splitlines():
        line = line.strip()
        if re.search(r'IPv4.*Address|IPv4 Address|Endereço IPv4', line, re.IGNORECASE):
            parts = re.split(r'[: ]+', line)
            for token in parts:
                if re.match(r'\d+\.\d+\.\d+\.\d+', token):
                    return token
    return None


def _extract_default_gateway(output: str) -> Optional[str]:
    for line in output.splitlines():
        line = line.strip()
        if re.search(r'Default Gateway', line, re.IGNORECASE):
            parts = re.split(r'[: ]+', line)
            for token in parts:
                if re.match(r'\d+\.\d+\.\d+\.\d+', token):
                    return token
    return None


def get_internal_ip() -> Optional[str]:
    """Get the primary internal IP address."""
    if is_windows():
        code, out, _ = run_command("ipconfig")
        if code != 0 or not out:
            return None
        ip = _extract_ipv4_from_ipconfig(out)
        return ip

    # Unix-like fallback
    code, out, _ = run_command("hostname -I")
    if code != 0 or not out.strip():
        return None
    return out.strip().split()[0]


def get_default_gateway() -> Optional[str]:
    """Get default gateway for active route."""
    if is_windows():
        code, out, _ = run_command("route print 0.0.0.0")
        if code == 0 and out:
            for line in out.splitlines():
                if re.match(r"\s*0\.0\.0\.0", line):
                    columns = line.split()
                    if len(columns) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", columns[2]):
                        return columns[2]
        code, out, _ = run_command("ipconfig")
        return _extract_default_gateway(out)

    code, out, _ = run_command("ip route show default 2>/dev/null")
    if code == 0 and out:
        match = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", out)
        if match:
            return match.group(1)
    return None


def get_dns_servers() -> List[str]:
    """Get configured DNS servers."""
    dns = []
    if is_windows():
        code, out, _ = run_command("ipconfig /all")
        if code != 0:
            return dns
        for line in out.splitlines():
            if re.search(r"DNS Servers", line, re.IGNORECASE):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    server = parts[1].strip()
                    if server:
                        dns.append(server)
            elif dns and line.strip() and re.match(r"\d+\.\d+\.\d+\.\d+", line.strip()):
                dns.append(line.strip())
        return dns

    # Unix-like
    try:
        with open("/etc/resolv.conf", "r") as resolv:
            for row in resolv:
                if row.startswith("nameserver"):
                    parts = row.split()
                    if len(parts) >= 2:
                        dns.append(parts[1].strip())
    except FileNotFoundError:
        pass
    return dns


def get_active_interface() -> Optional[str]:
    """Get interface used for outbound traffic."""
    if is_windows():
        code, out, _ = run_command("route print 0.0.0.0")
        if code == 0:
            for line in out.splitlines():
                if re.match(r"\s*0\.0\.0\.0", line):
                    parts = line.split()
                    if len(parts) >= 5:
                        return parts[-1]
        return None

    code, out, _ = run_command("ip route get 8.8.8.8 2>/dev/null")
    if code == 0 and out:
        match = re.search(r"dev\s+(\S+)", out)
        if match:
            return match.group(1)
    return None


def get_public_ip() -> Optional[str]:
    """Get public IP using common HTTP services."""
    candidates = ["https://ifconfig.me/ip", "https://api.ipify.org", "https://ident.me"]
    for url in candidates:
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=5) as r:
                ip = r.read().decode().strip()
                if re.match(r"\d+\.\d+\.\d+\.\d+", ip):
                    return ip
        except Exception:
            continue
    return None


def get_connection_uptime() -> Optional[str]:
    """Get system uptime as proxy for connection uptime."""
    if is_windows():
        code, out, _ = run_command("net statistics workstation")
        if code == 0:
            for line in out.splitlines():
                if "Statistics since" in line:
                    return line.split("Statistics since", 1)[1].strip()
        return None

    code, out, _ = run_command("cat /proc/uptime")
    if code == 0 and out:
        seconds = float(out.split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    return None


def get_network_summary() -> Dict[str, Optional[object]]:
    """Return a parsed network overview with key fields."""
    return {
        "internal_ip": get_internal_ip(),
        "public_ip": get_public_ip(),
        "active_interface": get_active_interface(),
        "default_gateway": get_default_gateway(),
        "dns_servers": get_dns_servers(),
        "connection_uptime": get_connection_uptime(),
    }


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
    info = {
        "os": platform.system(),
        "platform": platform.platform(),
        "python": platform.python_version(),
    }

    network_summary = get_network_summary()
    if network_summary:
        info["network_summary"] = network_summary

    if is_windows():
        code, out, err = run_command('systeminfo')
        if code == 0:
            info["systeminfo_text"] = out
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
