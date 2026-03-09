# ✅ Guardian - Pre-Deployment Checklist

Ready to deploy Guardian to GitHub? Use this checklist to make sure everything is in place.

---

## System Requirements

- [ ] Operating System: Windows 10+, macOS, or Linux
- [ ] Python 3.10+ installed (`python3 --version`)
- [ ] GitHub CLI installed (`gh --version`)
- [ ] Internet connection
- [ ] GitHub account

---

## GitHub Requirements

- [ ] GitHub account created
- [ ] GitHub CLI authenticated (`gh auth status` shows "Logged in as USERNAME")
- [ ] SSH key or HTTPS token configured
- [ ] No existing repository named "Guardian" (or okay with overwriting)

### Check GitHub Authentication

```bash
gh auth status
# Output should show: "Logged in to github.com as YOUR-USERNAME"
```

---

## Guardian Project Files

All of these should exist in `/home/vincius.souza/Guardian/`:

### Core Application

- [ ] `guardian_standalone.py` - Main standalone tool (20KB)
- [ ] `server.py` - HTTP server for remote delivery
- [ ] `run.py` - Entry point script
- [ ] `requirements.txt` - Dependencies (should be empty)

### Modular Version (src/)

- [ ] `src/dfir_cli/__init__.py` - Package init
- [ ] `src/dfir_cli/cli.py` - CLI interface
- [ ] `src/dfir_cli/analyzer.py` - DFIR analyzer
- [ ] `src/dfir_cli/windows_native.py` - Native commands
- [ ] `src/dfir_cli/bootstrap.py` - Secure downloads
- [ ] `src/dfir_cli/commands.py` - Command wrapper

### Documentation

- [ ] `README.md` - Main documentation
- [ ] `DEPLOY.md` - Quick deployment guide
- [ ] `REMOTE_EXECUTION.md` - Technical guide
- [ ] `IEX_READY.md` - IEX feature documentation
- [ ] `IEX_EXAMPLES.py` - Usage examples
- [ ] `GITHUB_DEPLOY.md` - This deployment guide

### Tests

- [ ] `tests.py` - Primary test suite
- [ ] `test_remote.py` - Remote execution tests
- [ ] `test_live.py` - Live demo tests
- [ ] `demo.py` - Interactive demo script

### Deployment Automation

- [ ] `github_deploy.py` - Python deployment script
- [ ] `github_deploy.sh` - Bash deployment script
- [ ] `guardian_loader.ps1` - PowerShell loader
- [ ] `guardian_loader.sh` - Bash loader

---

## Pre-Flight Validation

### 1. Verify Python Installation

```bash
python3 --version
# Expected: Python 3.10.x or higher
```

**Status**: ✅ / ❌

### 2. Verify GitHub CLI

```bash
gh --version
# Expected: gh version X.XX.x (YYYY-MM-DD)
```

**Status**: ✅ / ❌

### 3. Verify GitHub Authentication

```bash
gh auth status
# Expected: Logged in to github.com as YOUR-USERNAME
```

**Status**: ✅ / ❌

### 4. Test Guardian Standalone

```bash
cd /home/vincius.souza/Guardian
python3 guardian_standalone.py << EOF
processes
exit
EOF
```

**Status**: ✅ / ❌

### 5. Run Test Suite

```bash
cd /home/vincius.souza/Guardian
python3 tests.py
# Expected: All tests pass
```

**Status**: ✅ / ❌

### 6. Check Disk Space

```bash
df -h /home/vincius.souza/Guardian
# Expected: At least 100MB free
```

**Status**: ✅ / ❌

---

## Pre-Deployment Decisions

### Repository Name

- [ ] Repository will be named: **Guardian** (default)
- [ ] Repository will be named: **________________** (custom)

### Repository Visibility

- [ ] Public (anyone can see and download)
- [ ] Private (only you and collaborators)

### Branch Name

- [ ] Using main branch (default)
- [ ] Using different branch: **________________**

### Commit Message

- [ ] Using default: "Initial Guardian deployment"
- [ ] Using custom: **________________**

---

## Deployment Method Selection

Choose ONE method:

### Option A: Python Script (Recommended)

```bash
python3 github_deploy.py
```

- Pros: Robust, better error handling, informative output
- Cons: Requires Python 3.10+
- Status: [ ] Selected

### Option B: Bash Script

```bash
bash github_deploy.sh Guardian
```

- Pros: Simple, no Python dependency
- Cons: Less error handling
- Status: [ ] Selected

### Option C: Manual Git Commands

```bash
git init
git add .
git commit -m "Initial Guardian deployment"
gh repo create Guardian --public --push --source=. --remote=origin
```

- Pros: Full control, can execute step-by-step
- Cons: More manual work
- Status: [ ] Selected

---

## Internet Requirements

- [ ] Domain: `github.com` accessible
- [ ] Domain: `raw.githubusercontent.com` accessible (for one-liners)
- [ ] Bandwidth: At least 1MB for initial push

### Test Connectivity

```bash
# Test GitHub access
curl -I https://github.com
# Expected: HTTP 200

# Test raw.githubusercontent access
curl -I https://raw.githubusercontent.com
# Expected: HTTP 200 or 301
```

**Status**: ✅ / ❌

---

## Final Checklist

**Before Running Deployment:**

- [ ] All system requirements installed
- [ ] GitHub authentication verified
- [ ] Guardian project files present
- [ ] Python or Bash environment ready
- [ ] Internet connectivity confirmed
- [ ] Disk space available
- [ ] Deployment method chosen
- [ ] Repository name decided

**Ready to Deploy?**

```bash
# Python method
cd /home/vincius.souza/Guardian && python3 github_deploy.py

# OR Bash method
cd /home/vincius.souza/Guardian && bash github_deploy.sh Guardian
```

---

## What Happens During Deployment

When you run the deployment script:

1. **Validation** (~5 sec)
   - Checks GitHub CLI installation
   - Verifies GitHub authentication
   - Retrieves your GitHub username

2. **Repository Setup** (~5 sec)
   - Creates local git repository
   - Configures git with your info
   - Creates repository on GitHub

3. **Commit & Push** (~10-30 sec)
   - Stages all Guardian files
   - Creates initial commit
   - Pushes to GitHub main branch

4. **Final Output** (~2 sec)
   - Generates one-liner commands
   - Displays GitHub repository URL
   - Shows raw file URL

**Total Time**: 20-50 seconds typically

---

## Expected Output

After successful deployment, you'll see:

```
✓ Guardian repository created successfully!

Repository URL:
  https://github.com/YOUR-USERNAME/Guardian

Raw file URL (for IEX):
  https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py

One-liner commands ready:

Windows (PowerShell):
  iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py')

Linux/macOS (Bash):
  curl https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py | python3
```

---

## After Deployment

### Verify Repository

Visit: `https://github.com/YOUR-USERNAME/Guardian`

You should see:
- [ ] All project files uploaded
- [ ] README.md displayed
- [ ] Documentation visible
- [ ] guardian_standalone.py available

### Test One-Liner Delivery

On another machine:

```bash
# Linux/macOS
curl https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py | python3

# Windows PowerShell
iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py')
```

Expected: Guardian interactive shell starts

### Share with Team

Copy the one-liner from the output and share:
- Via email
- Via Slack
- Via Teams
- Via chat
- Copy to clipboard and distribute

---

## Troubleshooting

### Issue: "gh: command not found"

**Solution:**
```bash
# Install GitHub CLI
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: sudo apt install gh (or your package manager)
```

### Issue: "Not authenticated with GitHub"

**Solution:**
```bash
gh auth login
# Choose HTTPS, provide personal access token or auth via browser
```

### Issue: "Repository already exists"

**Solution:**
The script will ask if you want to overwrite. Answer `y` or `n`.

Or delete the remote repository first:
```bash
gh repo delete YOUR-USERNAME/Guardian --confirm
```

### Issue: "Permission denied" on script execution

**Solution:**
```bash
chmod +x github_deploy.sh
bash github_deploy.sh
```

### Issue: Git not configured

**Solution:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Success Indicators

✅ **Deployment was successful if:**

1. No errors in terminal output
2. Repository appears on GitHub profile
3. Files committed and pushed
4. One-liner URLs work

✅ **One-liners work if:**

1. Guardian starts on remote system
2. Interactive shell begins
3. Commands execute (try `help`)
4. No connection errors

---

## Next Steps After Deployment

1. **Test the one-liners** on different systems
2. **Document** how your team should use Guardian
3. **Create issues** for feature requests
4. **Set up credentials** if using private repo
5. **Configure GitHub Actions** for CI/CD (optional)

---

## Questions?

Refer to:
- `GITHUB_DEPLOY.md` - Deployment guide
- `DEPLOY.md` - Quick start guide
- `README.md` - Main documentation
- `REMOTE_EXECUTION.md` - Technical details

---

**Ready?** Let's deploy Guardian! 🚀

```bash
python3 github_deploy.py
# or
bash github_deploy.sh
```

---

**Deployment Timestamp**: 2024
**Guardian Version**: 0.2.0
**Python Required**: 3.10+
**External Dependencies**: None (zero-trust)
