#!/bin/bash

# Guardian - Setup Update Branches
# Cria os branches develop e dev para versionamento estratégico

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║  Guardian - Setup Update Branches             ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if authenticated
echo -e "${BLUE}Checking GitHub authentication...${NC}"
if ! gh auth status > /dev/null 2>&1; then
    echo -e "${RED}❌ Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi
echo -e "${GREEN}✅ Authenticated${NC}"
echo ""

# Get username and repo
USERNAME=$(gh api user -q .login)
REPO="Guardian"

echo -e "${BLUE}Setting up branches for: $USERNAME/$REPO${NC}"
echo ""

# Check if repo exists
if ! gh repo view "$USERNAME/$REPO" > /dev/null 2>&1; then
    echo -e "${RED}❌ Repository not found: $USERNAME/$REPO${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Repository found${NC}"
echo ""

# Step 1: Clone/update local repo
echo -e "${BLUE}[1/4] Preparing local repository...${NC}"

if [ ! -d ".git" ]; then
    echo "Cloning repository..."
    cd /tmp
    git clone https://github.com/$USERNAME/$REPO.git guardian-temp
    cd guardian-temp
else
    echo "Using existing repository"
    git fetch origin
fi

# Step 2: Create develop branch
echo -e "${BLUE}[2/4] Creating develop branch (stable with new features)...${NC}"

if git rev-parse --verify develop > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  develop branch already exists${NC}"
    git checkout develop
    git pull origin develop 2>/dev/null || true
else
    echo "Creating develop branch from main..."
    git checkout -b develop origin/main 2>/dev/null || git checkout -b develop
    git push -u origin develop
    echo -e "${GREEN}✅ develop branch created${NC}"
fi

# Step 3: Create dev branch
echo -e "${BLUE}[3/4] Creating dev branch (experimental)...${NC}"

if git rev-parse --verify dev > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  dev branch already exists${NC}"
    git checkout dev
    git pull origin dev 2>/dev/null || true
else
    echo "Creating dev branch from main..."
    git checkout -b dev origin/main 2>/dev/null || git checkout -b dev
    git push -u origin dev
    echo -e "${GREEN}✅ dev branch created${NC}"
fi

# Step 4: Push update files to main
echo -e "${BLUE}[4/4] Pushing update configuration files...${NC}"

git checkout main
git pull origin main

# Copy update files if not already there
if [ -f "update_manager.py" ] || [ -f "VERSIONS.json" ]; then
    echo "Staging update files..."
    git add update_manager.py VERSIONS.json UPDATE_STRATEGY.md 2>/dev/null || true
    
    if git diff --cached --quiet; then
        echo "No changes to commit"
    else
        git commit -m "Add update system and version management

- Add update_manager.py for version control
- Add VERSIONS.json for branch tracking
- Add UPDATE_STRATEGY.md documentation
- Support for stable/latest/dev branches"
        git push origin main
        echo -e "${GREEN}✅ Update files pushed${NC}"
    fi
fi

echo ""
echo "════════════════════════════════════════════════"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Branch Structure:${NC}"
echo "  main   → Stable (v0.2.0) - Production ready"
echo "  develop → Latest (v0.3.0-dev) - With new features"
echo "  dev    → Alpha (experimental) - For development"
echo ""

echo -e "${BLUE}Users can now use:${NC}"
echo ""
echo "  Stable (Recommended):"
echo "    ${GREEN}curl https://raw.githubusercontent.com/$USERNAME/$REPO/main/guardian_standalone.py | python3${NC}"
echo ""
echo "  Latest (With new features):"
echo "    ${YELLOW}curl https://raw.githubusercontent.com/$USERNAME/$REPO/develop/guardian_standalone.py | python3${NC}"
echo ""
echo "  Dev (Experimental):"
echo "    ${RED}curl https://raw.githubusercontent.com/$USERNAME/$REPO/dev/guardian_standalone.py | python3${NC}"
echo ""

echo -e "${BLUE}Update Management:${NC}"
echo "  ${GREEN}python3 update_manager.py check${NC}      - Check for updates"
echo "  ${GREEN}python3 update_manager.py update${NC}     - Update interactively"
echo "  ${GREEN}python3 update_manager.py rollback${NC}   - Rollback to previous"
echo ""

echo -e "${GREEN}Next steps:${NC}"
echo "  1. Test each branch's one-liner on different machines"
echo "  2. When ready, move features from dev → develop → main"
echo "  3. Run update_manager.py to test update functionality"
echo ""

echo "Setup complete! 🚀"
