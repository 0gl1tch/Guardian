import cmd
import shlex
import sys
import json
from .bootstrap import download_bootstrap
from .commands import execute
from .analyzer import DFIRAnalyzer
from .windows_native import (
    get_processes,
    get_network_connections,
    get_installed_software,
    get_system_info,
    get_network_summary,
    is_windows,
)


class DFIRShell(cmd.Cmd):
    intro = "DFIR CLI — Forensic toolkit using native commands. Type 'help' for commands."
    prompt = "(dfir) "

    def __init__(self):
        super().__init__()
        self.history = []
        self.analyzer = DFIRAnalyzer()

    def do_run(self, arg: str):
        """run <command>
        Executa um comando de shell.
        """
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
        """bootstrap <url> [dest] [sha256]
        Baixa um script bootstrap e opcionalmente valida sha256.
        """
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
        """history
        Show command history from this session.
        """
        for i, c in enumerate(self.history, 1):
            print(f"{i}: {c}")

    def do_processes(self, arg: str):
        """processes [--json]
        List running processes.
        Use --json for JSON output.
        """
        procs = get_processes()
        if "--json" in arg:
            print(json.dumps(procs, indent=2, default=str))
        else:
            if not procs:
                print("No processes found")
                return
            
            # Print formatted table
            keys = list(procs[0].keys())[:5]  # Show first 5 columns
            print(" | ".join(f"{k:20}" for k in keys))
            print("-" * (22 * len(keys)))
            for proc in procs[:20]:  # Show first 20
                values = [str(proc.get(k, ""))[:20] for k in keys]
                print(" | ".join(f"{v:20}" for v in values))
            if len(procs) > 20:
                print(f"... and {len(procs) - 20} more processes")

    def do_network(self, arg: str):
        """network [--json] [--summary]
        Show active network connections and optional summary.
        Use --json for JSON output.
        """
        if "--summary" in arg:
            summary = get_network_summary()
            print(json.dumps(summary, indent=2, default=str))
            return

        conns = get_network_connections()
        if "--json" in arg:
            print(json.dumps({"summary": get_network_summary(), "connections": conns}, indent=2, default=str))
            return

        print("Network Summary:")
        summary = get_network_summary()
        for key, value in summary.items():
            print(f" - {key}: {value}")
        print("\nActive connections:")

        if not conns:
            print("No active connections found")
            return

        print(f"{'Protocol':<8} {'Local Address':<24} {'Remote Address':<24} {'State':<14} {'PID':<8}")
        print("-" * 84)
        for conn in conns[:30]:
            print(f"{conn.get('protocol', 'N/A'):<8} {conn.get('local_address', 'N/A'):<24} "
                  f"{conn.get('remote_address', 'N/A'):<24} {conn.get('state', 'N/A'):<14} "
                  f"{conn.get('pid', 'N/A'):<8}")
        if len(conns) > 30:
            print(f"... and {len(conns) - 30} more connections")

    def do_software(self, arg: str):
        """software
        List installed software (Windows only).
        """
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
        """sysinfo
        Show system information.
        """
        info = get_system_info()
        for key, value in info.items():
            if key == "systeminfo_text":
                print(f"\nSystem Information Text:\n{value[:500]}...")
            elif key == "network_summary" and isinstance(value, dict):
                print("\nNetwork Summary:")
                for sub_key, sub_val in value.items():
                    print(f"  - {sub_key}: {sub_val}")
            else:
                print(f"{key}: {value}")

    def do_snapshot(self, arg: str):
        """snapshot [type] [--json]
        Take a forensic snapshot: full|processes|network|software|system
        Default is 'full'. Use --json for JSON output.
        """
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
            print(f"Data captures: {', '.join(snapshot['data'].keys())}")
            for key, data in snapshot['data'].items():
                if isinstance(data, list):
                    print(f"  {key}: {len(data)} items")
                else:
                    print(f"  {key}: captured")

    def do_snapshots(self, arg: str):
        """snapshots
        List all snapshots taken in this session.
        """
        snaps = self.analyzer.list_snapshots()
        if not snaps:
            print("No snapshots taken yet. Use 'snapshot' command.")
            return
        
        print(f"{'Index':<6} {'Timestamp':<30} {'Type':<12} {'Data':<40}")
        print("-" * 90)
        for snap in snaps:
            print(f"{snap['index']:<6} {snap['timestamp']:<30} {snap['type']:<12} "
                  f"{', '.join(snap['data_keys']):<40}")

    def do_export(self, arg: str):
        """export <filename>
        Export all snapshots to a JSON file.
        """
        if not arg.strip():
            print("usage: export <filename>")
            return
        
        filename = arg.strip()
        if self.analyzer.export_json(filename):
            print(f"Snapshots exported to {filename}")
        else:
            print(f"Failed to export to {filename}")

    def do_exit(self, arg: str):
        """exit
        Exit the DFIR CLI.
        """
        return True

    do_EOF = do_exit


def main():
    DFIRShell().cmdloop()
