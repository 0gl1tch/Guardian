"""
DFIR analysis module using native Windows commands.
Provides structured access to system information for forensics.
"""
import json
from datetime import datetime
from typing import Dict, List
from .windows_native import (
    get_processes,
    get_network_connections,
    get_installed_software,
    get_system_info,
    get_firewall_rules,
    get_scheduled_tasks,
    is_windows,
)


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
        
        # Compare processes
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
