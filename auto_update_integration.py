#!/usr/bin/env python3
"""
Guardian - Auto-Update Integration Example
Shows how to integrate update checking into Guardian shell
"""

import urllib.request
import json
import sys
from pathlib import Path

class GuardianAutoUpdate:
    """Minimal auto-update integration for Guardian"""
    
    VERSION_API = 'https://api.github.com/repos/0gl1tch/Guardian/releases/latest'
    CURRENT_VERSION = "0.2.0"
    
    @staticmethod
    def get_latest_version() -> str:
        """Get latest version from GitHub"""
        try:
            with urllib.request.urlopen(GuardianAutoUpdate.VERSION_API, timeout=3) as response:
                data = json.loads(response.read().decode())
                version = data.get('tag_name', 'v0.2.0').lstrip('v')
                return version
        except:
            return None
    
    @staticmethod
    def check_for_updates() -> bool:
        """Check if update is available (background, won't block)"""
        latest = GuardianAutoUpdate.get_latest_version()
        if latest and latest != GuardianAutoUpdate.CURRENT_VERSION:
            return True
        return False
    
    @staticmethod
    def notify_update():
        """Notify user about available update"""
        print("\n" + "="*60)
        print("🔔 UPDATE AVAILABLE!")
        print("="*60)
        print(f"Current:  {GuardianAutoUpdate.CURRENT_VERSION}")
        print(f"Latest:   {GuardianAutoUpdate.get_latest_version()}")
        print("\nRun the update at your discretion:")
        print("  $ python3 update_manager.py update stable")
        print("\nOr download fresh:")
        print("  $ curl https://raw...main/guardian_standalone.py | python3")
        print("="*60 + "\n")


# Integration example for DFIRShell
def integrate_into_shell():
    """
    Add this to the DFIRShell.__init__ or main():
    
    # At startup (non-blocking)
    threading.Thread(
        target=lambda: GuardianAutoUpdate.notify_update()
        if GuardianAutoUpdate.check_for_updates()
        else None,
        daemon=True
    ).start()
    
    # Or add command to shell:
    def do_update(self, _):
        \"\"\"Update Guardian to latest version\"\"\"
        os.system('python3 update_manager.py update')
    """
    pass


# Detailed implementation example
INTEGRATION_CODE = '''
# In guardian_standalone.py, add this to DFIRShell class:

def do_update(self, args):
    """Update Guardian to latest version
    
    Usage:
        update              - Interactive update
        update stable       - Update from stable branch
        update latest       - Update from latest branch
        update dev          - Update from dev branch
    """
    import subprocess
    import os
    
    if not args:
        # Interactive
        subprocess.run([sys.executable, 'update_manager.py', 'update'])
    else:
        # Specific branch
        branch = args.split()[0]
        subprocess.run([sys.executable, 'update_manager.py', 'update', branch])
    

def do_check_updates(self, _):
    """Check if Guardian updates are available"""
    import urllib.request
    import json
    
    api_url = 'https://api.github.com/repos/0gl1tch/Guardian/releases/latest'
    current = '0.2.0'
    
    try:
        with urllib.request.urlopen(api_url, timeout=3) as response:
            data = json.loads(response.read().decode())
            latest = data.get('tag_name', 'v0.2.0').lstrip('v')
            
            if latest > current:
                print(f"✨ Update available: {current} → {latest}")
                print(f"Run: update")
            else:
                print(f"✅ Guardian is up to date ({current})")
    except Exception as e:
        print(f"⚠️  Could not check for updates: {e}")


# In shell help:
def do_help(self, arg):
    """Show available commands"""
    commands = {
        'processes': 'List running processes',
        'network': 'Show network connections',
        'snapshot': 'Take system snapshot',
        'export': 'Export snapshots to JSON',
        'check_updates': 'Check for new versions',  # NEW
        'update': 'Update Guardian',  # NEW
        'exit': 'Exit Guardian'
    }
    
    if not arg:
        print("\\nAvailable Commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd:<15} - {desc}")
    else:
        print(commands.get(arg, f"Unknown command: {arg}"))
'''


if __name__ == '__main__':
    # Example usage
    print("Guardian Auto-Update Integration Guide")
    print("="*60)
    print()
    print("1. Check for updates:")
    print(f"   Current: {GuardianAutoUpdate.CURRENT_VERSION}")
    print(f"   Latest:  {GuardianAutoUpdate.get_latest_version()}")
    print()
    print("2. Integration code added to guardian_standalone.py:")
    print("   - do_update() command")
    print("   - do_check_updates() command")
    print()
    print("3. Usage in Guardian shell:")
    print("   Guardian> check_updates")
    print("   Guardian> update")
    print("   Guardian> update stable")
    print()
