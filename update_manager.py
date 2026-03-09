#!/usr/bin/env python3
"""
Guardian Update Manager
Handles versioning, updates, and rollback strategies
"""

import subprocess
import json
import urllib.request
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Version:
    """Version information"""
    major: int
    minor: int
    patch: int
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch < other.patch
    
    @staticmethod
    def parse(version_str: str) -> 'Version':
        parts = version_str.split('.')
        return Version(int(parts[0]), int(parts[1]), int(parts[2]))


class GuardianUpdateManager:
    """Manage Guardian updates from GitHub"""
    
    # Branches strategy
    BRANCHES = {
        'stable': 'https://raw.githubusercontent.com/0gl1tch/Guardian/main/guardian_standalone.py',
        'latest': 'https://raw.githubusercontent.com/0gl1tch/Guardian/develop/guardian_standalone.py',
        'dev': 'https://raw.githubusercontent.com/0gl1tch/Guardian/dev/guardian_standalone.py',
    }
    
    # Version info endpoint
    VERSION_API = 'https://api.github.com/repos/0gl1tch/Guardian/releases/latest'
    VERSIONS_FILE = 'https://raw.githubusercontent.com/0gl1tch/Guardian/main/VERSIONS.json'
    
    def __init__(self):
        self.current_version = self.parse_current_version()
        self.cache_dir = Path.home() / '.guardian'
        self.cache_dir.mkdir(exist_ok=True)
    
    def parse_current_version(self) -> Version:
        """Parse current Guardian version from source"""
        try:
            # Try to find version in guardian_standalone.py
            if Path('guardian_standalone.py').exists():
                with open('guardian_standalone.py') as f:
                    for line in f:
                        if '__version__' in line and '=' in line:
                            version_str = line.split('=')[1].strip().strip('"\'')
                            return Version.parse(version_str)
        except:
            pass
        
        # Default to 0.2.0
        return Version(0, 2, 0)
    
    def get_latest_version(self, branch: str = 'stable') -> Optional[Dict]:
        """Get latest version info from GitHub"""
        try:
            with urllib.request.urlopen(self.VERSION_API, timeout=5) as response:
                data = json.loads(response.read().decode())
                return {
                    'version': data.get('tag_name', 'v0.2.0').lstrip('v'),
                    'url': data.get('html_url'),
                    'notes': data.get('body', 'No release notes'),
                    'prerelease': data.get('prerelease', False),
                }
        except Exception as e:
            print(f"Error fetching version: {e}")
            return None
    
    def check_updates(self, branch: str = 'stable') -> bool:
        """Check if updates available"""
        latest = self.get_latest_version(branch)
        if not latest:
            return False
        
        latest_ver = Version.parse(latest['version'])
        return latest_ver > self.current_version
    
    def download_update(self, branch: str = 'stable') -> Optional[bytes]:
        """Download latest Guardian from specified branch"""
        url = self.BRANCHES.get(branch)
        if not url:
            print(f"Unknown branch: {branch}")
            return None
        
        try:
            print(f"📥 Downloading Guardian from {branch}...")
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read()
                print(f"✅ Downloaded {len(content)} bytes")
                return content
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None
    
    def backup_current(self) -> Path:
        """Backup current version"""
        backup_path = self.cache_dir / f'guardian_backup_{self.current_version}.py'
        try:
            if Path('guardian_standalone.py').exists():
                Path('guardian_standalone.py').read_bytes()
                backup_path.write_bytes(Path('guardian_standalone.py').read_bytes())
                print(f"💾 Backup saved: {backup_path}")
                return backup_path
        except Exception as e:
            print(f"⚠️  Backup failed: {e}")
        return None
    
    def apply_update(self, content: bytes, branch: str = 'stable') -> bool:
        """Apply downloaded update"""
        try:
            # Backup current
            self.backup_current()
            
            # Write new version
            Path('guardian_standalone.py').write_bytes(content)
            print(f"✅ Updated to latest from {branch}")
            
            # Verify it's valid Python
            compile(content, 'guardian_standalone.py', 'exec')
            print("✅ Syntax validated")
            return True
        except Exception as e:
            print(f"❌ Update failed: {e}")
            print("⏮️  Rolling back...")
            self.rollback()
            return False
    
    def rollback(self) -> bool:
        """Rollback to previous version"""
        backups = sorted(self.cache_dir.glob('guardian_backup_*.py'))
        if not backups:
            print("❌ No backups available for rollback")
            return False
        
        latest_backup = backups[-1]
        try:
            content = latest_backup.read_bytes()
            Path('guardian_standalone.py').write_bytes(content)
            print(f"✅ Rolled back to {latest_backup.name}")
            return True
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False
    
    def list_backups(self):
        """List available backups"""
        backups = sorted(self.cache_dir.glob('guardian_backup_*.py'))
        if not backups:
            print("No backups available")
            return
        
        print("Available backups:")
        for i, backup in enumerate(backups, 1):
            size = backup.stat().st_size / 1024  # KB
            print(f"  {i}. {backup.name} ({size:.1f}KB)")
    
    def update_interactive(self):
        """Interactive update process"""
        print("\n" + "="*60)
        print("Guardian Update Manager")
        print("="*60)
        print(f"\nCurrent version: {self.current_version}")
        
        # Check for updates
        if not self.check_updates():
            print("✅ Guardian is up to date")
            return
        
        latest = self.get_latest_version()
        if latest:
            print(f"📌 Latest available: {latest['version']}")
            print(f"\nRelease notes:\n{latest['notes'][:200]}...\n")
        
        # Ask about update
        response = input("Update available! Install? (y/n): ").strip().lower()
        if response != 'y':
            print("Update cancelled")
            return
        
        # Choose branch
        print("\nSelect branch:")
        print("  1. stable  (Recommended, tested)")
        print("  2. latest  (New features, may have bugs)")
        print("  3. dev     (Development, use with caution)")
        
        branch_map = {'1': 'stable', '2': 'latest', '3': 'dev'}
        choice = input("Choice (1-3): ").strip()
        branch = branch_map.get(choice, 'stable')
        
        # Download and apply
        content = self.download_update(branch)
        if content:
            self.apply_update(content, branch)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Guardian Update Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  guardian-update check              # Check for updates
  guardian-update update             # Interactive update
  guardian-update update stable      # Install from stable
  guardian-update update latest      # Install from latest
  guardian-update rollback           # Rollback to previous
  guardian-update list-backups       # Show all backups
        """
    )
    
    parser.add_argument('command', nargs='?', default='check',
                       choices=['check', 'update', 'rollback', 'list-backups'],
                       help='Command to run')
    parser.add_argument('branch', nargs='?', default='stable',
                       choices=['stable', 'latest', 'dev'],
                       help='Branch to use (for update)')
    
    args = parser.parse_args()
    
    manager = GuardianUpdateManager()
    
    if args.command == 'check':
        if manager.check_updates():
            print(f"✨ Update available!")
            latest = manager.get_latest_version()
            if latest:
                print(f"   {manager.current_version} → {latest['version']}")
        else:
            print("✅ Guardian is up to date")
    
    elif args.command == 'update':
        manager.update_interactive()
    
    elif args.command == 'rollback':
        manager.rollback()
    
    elif args.command == 'list-backups':
        manager.list_backups()


if __name__ == '__main__':
    main()
