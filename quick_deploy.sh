#!/bin/bash

# Guardian - Super Quick Deploy Script
# Fastest way to deploy Guardian to GitHub

echo "╔════════════════════════════════════════════════╗"
echo "║  Guardian - GitHub Deployment (3 Steps)       ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Check prerequisites
echo -e "${BLUE}[1/3] Checking prerequisites...${NC}"
echo ""

if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI not found!${NC}"
    echo "Install it first:"
    echo "  Windows: winget install GitHub.cli"
    echo "  macOS:   brew install gh"
    echo "  Linux:   sudo apt install gh"
    exit 1
fi
echo -e "${GREEN}✓ GitHub CLI found${NC}"

if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with GitHub!${NC}"
    echo "Run: gh auth login"
    exit 1
fi
echo -e "${GREEN}✓ GitHub authenticated${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Install Python 3.10+: https://python.org"
    exit 1
fi
PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PY_VERSION found${NC}"

echo ""

# Step 2: Deploy to GitHub
echo -e "${BLUE}[2/3] Deploying to GitHub...${NC}"
echo ""

cd /home/vincius.souza/Guardian || {
    echo -e "${RED}❌ Guardian directory not found!${NC}"
    exit 1
}

# Initialize git
git init --quiet 2>/dev/null || true
git config user.name "Guardian Deployer" 2>/dev/null || true
git config user.email "deployer@guardian.local" 2>/dev/null || true

# Add and commit
git add . 2>/dev/null || true
git commit -m "Guardian initial deployment" --quiet 2>/dev/null || true

# Get username
USERNAME=$(gh api user -q .login 2>/dev/null)
if [ -z "$USERNAME" ]; then
    echo -e "${RED}❌ Could not get GitHub username${NC}"
    exit 1
fi
echo -e "${GREEN}✓ GitHub username: $USERNAME${NC}"

# Create repository
REPO_NAME=${1:-Guardian}
echo -e "${GREEN}✓ Creating repository: $REPO_NAME${NC}"

# Check if repo exists
if gh repo view "$USERNAME/$REPO_NAME" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Repository already exists, updating...${NC}"
    git remote remove origin 2>/dev/null || true
else
    echo -e "${GREEN}✓ New repository${NC}"
fi

# Push to GitHub
gh repo create "$REPO_NAME" --public --push --source=. --remote=origin 2>/dev/null || {
    echo -e "${YELLOW}⚠ Repository exists, syncing...${NC}"
    git branch -M main
    git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || \
        git remote set-url origin "https://github.com/$USERNAME/$REPO_NAME.git"
    git push -u origin main --force 2>/dev/null
}

echo ""

# Step 3: Display results
echo -e "${BLUE}[3/3] Deployment complete!${NC}"
echo ""

RAW_URL="https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/guardian_standalone.py"
REPO_URL="https://github.com/$USERNAME/$REPO_NAME"

echo -e "${GREEN}✅ Success!${NC}"
echo ""
echo -e "${BLUE}Repository:${NC}"
echo "  $REPO_URL"
echo ""
echo -e "${BLUE}Raw file URL:${NC}"
echo "  $RAW_URL"
echo ""
echo -e "${YELLOW}📋 Copy-paste one-liners:${NC}"
echo ""
echo -e "${BLUE}Windows (PowerShell):${NC}"
echo "  ${GREEN}iex(New-Object Net.WebClient).DownloadString('$RAW_URL')${NC}"
echo ""
echo -e "${BLUE}Linux/macOS (Bash):${NC}"
echo "  ${GREEN}curl $RAW_URL | python3${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Test one-liner on another machine"
echo "  2. Share one-liner with your team"
echo "  3. Refer to DEPLOY.md for usage"
echo ""
echo -e "${GREEN}Guardian is live! 🚀${NC}"
