#!/usr/bin/env python3
"""
Guardian Tools - Numerical Menu System
Access all Guardian functions by number
"""

import subprocess
import sys
import os
from pathlib import Path

class GuardianTools:
    """Main menu system for Guardian management"""
    
    def __init__(self):
        self.menu_options = {
            1: ("Check for Updates", self.check_updates),
            2: ("Update Guardian (Stable)", self.update_stable),
            3: ("Update Guardian (Latest)", self.update_latest),
            4: ("Update Guardian (Dev)", self.update_dev),
            5: ("Rollback to Previous Version", self.rollback),
            6: ("List Available Backups", self.list_backups),
            7: ("Run Guardian", self.run_guardian),
            8: ("View Update Strategy", self.view_strategy),
            9: ("View Version Info", self.version_info),
            0: ("Exit", self.exit_program),
        }
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🛡️  GUARDIAN - DFIR TOOLKIT MANAGER")
        print("="*60 + "\n")
        
        for num, (desc, _) in self.menu_options.items():
            if num == 0:
                print("-"*60)
            print(f"  {num}. {desc}")
        
        print("\n" + "="*60)
    
    def check_updates(self):
        """Check for updates"""
        print("\n📋 Checking for updates...\n")
        result = subprocess.run(['python3', 'update_manager.py', 'check'], 
                              capture_output=False)
        return result.returncode == 0
    
    def update_stable(self):
        """Update to stable branch"""
        print("\n📥 Updating to STABLE branch...\n")
        result = subprocess.run(['python3', 'update_manager.py', 'update', 'stable'],
                              capture_output=False)
        return result.returncode == 0
    
    def update_latest(self):
        """Update to latest branch"""
        print("\n📥 Updating to LATEST branch (with new features)...\n")
        result = subprocess.run(['python3', 'update_manager.py', 'update', 'latest'],
                              capture_output=False)
        return result.returncode == 0
    
    def update_dev(self):
        """Update to dev branch"""
        print("\n⚠️  Updating to DEV branch (experimental)...\n")
        print("WARNING: Dev branch may be unstable!")
        response = input("Continue? (y/n): ").strip().lower()
        if response != 'y':
            print("Update cancelled")
            return False
        
        result = subprocess.run(['python3', 'update_manager.py', 'update', 'dev'],
                              capture_output=False)
        return result.returncode == 0
    
    def rollback(self):
        """Rollback to previous version"""
        print("\n⏮️  Rolling back to previous version...\n")
        result = subprocess.run(['python3', 'update_manager.py', 'rollback'],
                              capture_output=False)
        return result.returncode == 0
    
    def list_backups(self):
        """List available backups"""
        print("\n💾 Available Backups:\n")
        result = subprocess.run(['python3', 'update_manager.py', 'list-backups'],
                              capture_output=False)
        return result.returncode == 0
    
    def run_guardian(self):
        """Run Guardian interactive shell"""
        print("\n🚀 Starting Guardian...\n")
        result = subprocess.run(['python3', 'guardian_standalone.py'],
                              capture_output=False)
        return result.returncode == 0
    
    def view_strategy(self):
        """View update strategy documentation"""
        print("\n📖 Opening UPDATE_STRATEGY.md...\n")
        if Path('UPDATE_STRATEGY.md').exists():
            subprocess.run(['less', 'UPDATE_STRATEGY.md'])
        else:
            print("❌ UPDATE_STRATEGY.md not found")
            return False
        return True
    
    def version_info(self):
        """Show version information"""
        print("\n📊 Guardian Version Information\n")
        print("Current Version: 0.2.0")
        print("Status: Production Ready")
        print("Repository: https://github.com/0gl1tch/Guardian")
        print("Branches: main (stable), develop (latest), dev (experimental)")
        print("\nFor detailed info, see: UPDATE_SYSTEM_COMPLETE.md")
        return True
    
    def exit_program(self):
        """Exit the program"""
        print("\n👋 Goodbye!\n")
        sys.exit(0)
    
    def run(self):
        """Main loop"""
        while True:
            self.display_menu()
            
            try:
                choice = input("Select an option (0-9): ").strip()
                
                if not choice.isdigit():
                    print("❌ Invalid input. Please enter a number (0-9)")
                    continue
                
                choice = int(choice)
                
                if choice not in self.menu_options:
                    print(f"❌ Invalid option: {choice}")
                    continue
                
                desc, func = self.menu_options[choice]
                print(f"\n▶️  {desc}...\n")
                
                func()
                
                if choice != 0:
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
                input("\nPress Enter to continue...")


def main():
    """Entry point"""
    tools = GuardianTools()
    tools.run()


if __name__ == '__main__':
    main()
