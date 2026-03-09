#!/bin/bash

# Guardian Deployment - Numerical Menu System
# Access all deployment functions by number

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_menu() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║        🛡️  GUARDIAN - DEPLOYMENT MANAGER              ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${BLUE}Select an option:${NC}"
    echo ""
    echo "  1. Quick Deploy (Fastest)"
    echo "  2. Full Deploy with Details (Python)"
    echo "  3. Bash-only Deploy"
    echo "  4. Setup Update Branches"
    echo "  5. Check GitHub Authentication"
    echo "  6. Install GitHub CLI"
    echo "  7. Get Repository Info"
    echo "  8. Test IEX Commands"
    echo "  9. View Deployment Documentation"
    echo "  0. Exit"
    echo ""
    echo "════════════════════════════════════════════════════════"
}

deploy_quick() {
    echo -e "\n${BLUE}[1] Quick Deploy${NC}\n"
    bash quick_deploy.sh
}

deploy_python() {
    echo -e "\n${BLUE}[2] Python Deploy${NC}\n"
    python3 github_deploy.py
}

deploy_bash() {
    echo -e "\n${BLUE}[3] Bash Deploy${NC}\n"
    bash github_deploy.sh Guardian
}

setup_branches() {
    echo -e "\n${BLUE}[4] Setup Update Branches${NC}\n"
    if [ -f "setup_update_branches.sh" ]; then
        bash setup_update_branches.sh
    else
        echo -e "${RED}❌ setup_update_branches.sh not found${NC}"
    fi
}

check_github() {
    echo -e "\n${BLUE}[5] GitHub Authentication Status${NC}\n"
    
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI not installed${NC}"
        echo "Run option 6 to install"
        return 1
    fi
    
    echo -e "${GREEN}✅ GitHub CLI found${NC}"
    gh auth status
}

install_github() {
    echo -e "\n${BLUE}[6] Install GitHub CLI${NC}\n"
    
    if command -v gh &> /dev/null; then
        echo -e "${GREEN}✅ GitHub CLI already installed${NC}"
        gh --version
        return 0
    fi
    
    echo "Installing GitHub CLI..."
    
    if command -v brew &> /dev/null; then
        echo "Using brew..."
        brew install gh
    elif command -v apt &> /dev/null; then
        echo "Using apt..."
        sudo apt install -y gh
    else
        echo -e "${YELLOW}⚠️  Please install GitHub CLI manually:${NC}"
        echo "https://cli.github.com"
    fi
}

repo_info() {
    echo -e "\n${BLUE}[7] Repository Information${NC}\n"
    
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}⚠️  Not a git repository${NC}"
        return 1
    fi
    
    echo "Origin URL:"
    git remote -v | head -2
    echo ""
    echo "Current Branch:"
    git branch --show-current
    echo ""
    echo "Latest Commit:"
    git log -1 --oneline
    echo ""
    echo "Files to Deploy:"
    git status --short
}

test_iex() {
    echo -e "\n${BLUE}[8] Test IEX Commands${NC}\n"
    
    if [ ! -f "guardian_standalone.py" ]; then
        echo -e "${RED}❌ guardian_standalone.py not found${NC}"
        return 1
    fi
    
    echo "Testing guardian_standalone.py..."
    
    # Test 1: Check syntax
    if python3 -m py_compile guardian_standalone.py 2>/dev/null; then
        echo -e "${GREEN}✅ Python syntax valid${NC}"
    else
        echo -e "${RED}❌ Python syntax error${NC}"
        return 1
    fi
    
    # Test 2: Test execution
    echo ""
    echo "Testing basic execution..."
    echo "help" | python3 guardian_standalone.py > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Execution test passed${NC}"
    else
        echo -e "${YELLOW}⚠️  Execution test may have issues${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}IEX Commands (Ready to Use):${NC}"
    echo ""
    echo "Windows (PowerShell):"
    echo -e "  ${GREEN}iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/0gl1tch/Guardian/master/guardian_standalone.py')${NC}"
    echo ""
    echo "Linux/macOS (Bash):"
    echo -e "  ${GREEN}curl https://raw.githubusercontent.com/0gl1tch/Guardian/master/guardian_standalone.py | python3${NC}"
}

view_docs() {
    echo -e "\n${BLUE}[9] Deployment Documentation${NC}\n"
    
    echo "Available Documents:"
    echo "  1. START_HERE.md"
    echo "  2. GITHUB_DEPLOY.md"
    echo "  3. DEPLOYMENT_CHECKLIST.md"
    echo "  4. READY_TO_DEPLOY.md"
    echo "  5. IEX_READY.md"
    echo ""
    
    read -p "Select document (1-5) or 0 to cancel: " doc_choice
    
    case $doc_choice in
        1) less START_HERE.md ;;
        2) less GITHUB_DEPLOY.md ;;
        3) less DEPLOYMENT_CHECKLIST.md ;;
        4) less READY_TO_DEPLOY.md ;;
        5) less IEX_READY.md ;;
        0) echo "Cancelled" ;;
        *) echo "Invalid choice" ;;
    esac
}

main_loop() {
    while true; do
        show_menu
        read -p "Select option (0-9): " choice
        
        case $choice in
            1) deploy_quick ;;
            2) deploy_python ;;
            3) deploy_bash ;;
            4) setup_branches ;;
            5) check_github ;;
            6) install_github ;;
            7) repo_info ;;
            8) test_iex ;;
            9) view_docs ;;
            0) 
                echo -e "\n${GREEN}👋 Goodbye!${NC}\n"
                exit 0
                ;;
            *)
                echo -e "\n${RED}❌ Invalid option${NC}\n"
                ;;
        esac
        
        if [ $choice -ne 0 ]; then
            echo ""
            read -p "Press Enter to continue..."
        fi
    done
}

main_loop
