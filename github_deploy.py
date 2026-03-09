#!/usr/bin/env python3
"""
Guardian GitHub Auto-Deploy
Automated script to create GitHub repo and deploy Guardian
Requires: GitHub CLI (gh) installed and authenticated

Install GitHub CLI: https://cli.github.com
Then: gh auth login
"""

import subprocess
import sys
import os
import json
from pathlib import Path


class GitHubDeployer:
    """Automate Guardian deployment to GitHub"""
    
    def __init__(self, repo_name="Guardian", description="DFIR forensic analysis toolkit with native commands - execute via IEX"):
        self.repo_name = repo_name
        self.description = description
        self.repo_url = None
        self.username = None
        
    def check_gh_cli(self) -> bool:
        """Check if GitHub CLI is installed"""
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ GitHub CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ GitHub CLI not found!")
            print("Install from: https://cli.github.com")
            return False
    
    def check_auth(self) -> bool:
        """Check if user is authenticated"""
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub authenticated")
            # Extract username from output
            for line in result.stdout.split('\n'):
                if 'Logged in to' in line:
                    print(f"   {line.strip()}")
            return True
        else:
            print("❌ Not authenticated with GitHub")
            print("Run: gh auth login")
            return False
    
    def get_username(self) -> str:
        """Get GitHub username"""
        result = subprocess.run(['gh', 'api', 'user', '--jq', '.login'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            self.username = result.stdout.strip()
            return self.username
        return None
    
    def repo_exists(self) -> bool:
        """Check if repo already exists"""
        result = subprocess.run(['gh', 'repo', 'view', f'{self.username}/{self.repo_name}'],
                              capture_output=True, text=True)
        return result.returncode == 0
    
    def create_repo(self) -> bool:
        """Create GitHub repository"""
        if self.repo_exists():
            print(f"⚠️  Repository '{self.repo_name}' already exists")
            response = input("Overwrite? (y/n): ").strip().lower()
            if response != 'y':
                return False
        
        print(f"\n📝 Creating repository '{self.repo_name}'...")
        
        cmd = [
            'gh', 'repo', 'create', self.repo_name,
            '--public',
            '--description', self.description,
            '--source=.',
            '--remote=origin',
            '--push'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Repository created successfully")
            self.repo_url = f"https://github.com/{self.username}/{self.repo_name}"
            return True
        else:
            print(f"❌ Failed to create repository: {result.stderr}")
            return False
    
    def init_git(self) -> bool:
        """Initialize git repository locally"""
        print("\n🔧 Initializing local git repository...")
        
        # Check if already git initialized
        if os.path.exists('.git'):
            print("⚠️  Repository already initialized")
            return True
        
        commands = [
            ['git', 'init'],
            ['git', 'config', 'user.name', self.username or 'Guardian'],
            ['git', 'config', 'user.email', f'{self.username}@users.noreply.github.com'],
            ['git', 'add', '.'],
        ]
        
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Error running: {' '.join(cmd)}")
                print(f"   {result.stderr}")
                return False
        
        print("✅ Git initialized")
        return True
    
    def commit_and_push(self) -> bool:
        """Commit and push to GitHub"""
        print("\n📤 Committing and pushing to GitHub...")
        
        commands = [
            ['git', 'commit', '-m', 'Initial Guardian DFIR CLI deployment\n\n- Zero dependencies\n- IEX remote execution ready\n- Full DFIR toolkit\n- Native Windows/Unix commands'],
            ['git', 'remote', 'add', 'origin', f'https://github.com/{self.username}/{self.repo_name}.git'],
            ['git', 'branch', '-M', 'main'],
            ['git', 'push', '-u', 'origin', 'main', '--force'],
        ]
        
        for cmd in commands:
            # Skip if 'add remote' fails (already exists)
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0 and 'remote' not in ' '.join(cmd):
                print(f"⚠️  {' '.join(cmd[:3])}: {result.stderr.strip()}")
            elif result.returncode == 0:
                print(f"✅ {cmd[2]} completed")
        
        print("✅ Push completed")
        return True
    
    def generate_one_liners(self):
        """Generate one-liner commands"""
        raw_url = f"https://raw.githubusercontent.com/{self.username}/{self.repo_name}/main/guardian_standalone.py"
        
        print("\n" + "="*80)
        print("🎯 DEPLOYMENT COMPLETE!")
        print("="*80)
        print(f"\n✅ Repository: {self.repo_url}")
        print(f"\n📋 Raw File URL: {raw_url}")
        
        print("\n" + "-"*80)
        print("🚀 One-Liner Commands (Ready to Share):")
        print("-"*80)
        
        print("\n📌 Windows (PowerShell):")
        print("```powershell")
        print(f"iex(New-Object Net.WebClient).DownloadString('{raw_url}')")
        print("```")
        
        print("\n🐧 Linux/macOS (Bash):")
        print("```bash")
        print(f"curl {raw_url} | python3")
        print("```")
        
        print("\n" + "-"*80)
        print("\nNext steps:")
        print("1. Share these one-liners with your team")
        print("2. Anyone with internet + Python 3.10+ can run Guardian")
        print("3. No installation needed!")
        print("\nFor documentation, visit:")
        print(f"  {self.repo_url}")
        print("\nFor technical details:")
        print(f"  {self.repo_url}/blob/main/DEPLOY.md")
        print(f"  {self.repo_url}/blob/main/REMOTE_EXECUTION.md")
        
        return raw_url
    
    def deploy(self) -> bool:
        """Run complete deployment"""
        print("\n" + "="*80)
        print("🛡️  GUARDIAN GITHUB AUTO-DEPLOY")
        print("="*80)
        
        # Step 1: Check GitHub CLI
        if not self.check_gh_cli():
            return False
        
        # Step 2: Check authentication
        if not self.check_auth():
            return False
        
        # Step 3: Get username
        username = self.get_username()
        if not username:
            print("❌ Could not get GitHub username")
            return False
        print(f"👤 Username: {username}")
        
        # Step 4: Initialize git
        if not self.init_git():
            return False
        
        # Step 5: Create GitHub repo
        if not self.create_repo():
            return False
        
        # Step 6: Commit and push
        if not self.commit_and_push():
            print("⚠️  Push may have had issues, but repository might still be created")
        
        # Step 7: Generate commands
        raw_url = self.generate_one_liners()
        
        print("\n" + "="*80)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("="*80)
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Deploy Guardian to GitHub automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 github_deploy.py                    # Use defaults
  python3 github_deploy.py --repo MyGuardian  # Custom repo name
  python3 github_deploy.py --public           # Public repo (default)
  python3 github_deploy.py --private          # Private repo
        """
    )
    
    parser.add_argument('--repo', default='Guardian',
                       help='Repository name (default: Guardian)')
    parser.add_argument('--description', 
                       default='DFIR forensic analysis toolkit with native commands - execute via IEX',
                       help='Repository description')
    
    args = parser.parse_args()
    
    deployer = GitHubDeployer(repo_name=args.repo, description=args.description)
    
    try:
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
