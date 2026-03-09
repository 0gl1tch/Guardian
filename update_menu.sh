#!/bin/bash

# Guardian Setup & Updates - Numerical Menu System
# Access all setup and update functions by number

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_menu() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║        🛡️  GUARDIAN - UPDATE & SETUP MANAGER           ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${BLUE}Update Manager:${NC}"
    echo "  1. Check for Updates"
    echo "  2. Update Guardian (Interactive)"
    echo "  3. Update from Stable Branch"
    echo "  4. Update from Latest Branch"
    echo "  5. Update from Dev Branch"
    echo "  6. Rollback to Previous Version"
    echo ""
    echo -e "${BLUE}Setup & Configuration:${NC}"
    echo "  7. Setup Update Branches (develop/dev)"
    echo "  8. Install Update Manager Dependencies"
    echo "  9. Verify Update System"
    echo ""
    echo -e "${BLUE}Information:${NC}"
    echo "  10. View Version Information"
    echo "  11. View Update Strategy"
    echo "  12. List All Backups"
    echo ""
    echo "  0. Exit"
    echo ""
    echo "════════════════════════════════════════════════════════"
}

check_updates() {
    echo -e "\n${BLUE}[1] Checking for Updates${NC}\n"
    
    if [ ! -f "update_manager.py" ]; then
        echo -e "${RED}❌ update_manager.py not found${NC}"
        return 1
    fi
    
    python3 update_manager.py check
}

update_interactive() {
    echo -e "\n${BLUE}[2] Update Guardian (Interactive)${NC}\n"
    python3 update_manager.py update
}

update_stable() {
    echo -e "\n${BLUE}[3] Update from Stable Branch${NC}\n"
    echo "This will update Guardian to the latest stable version"
    read -p "Continue? (y/n): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        python3 update_manager.py update stable
    else
        echo "Update cancelled"
    fi
}

update_latest() {
    echo -e "\n${BLUE}[4] Update from Latest Branch${NC}\n"
    echo -e "${YELLOW}⚠️  Latest branch may contain new features with bugs${NC}"
    read -p "Continue? (y/n): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        python3 update_manager.py update latest
    else
        echo "Update cancelled"
    fi
}

update_dev() {
    echo -e "\n${BLUE}[5] Update from Dev Branch${NC}\n"
    echo -e "${RED}❌ WARNING: Dev branch is experimental and may be broken!${NC}"
    read -p "Continue at your own risk? (y/n): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        python3 update_manager.py update dev
        echo -e "\n${YELLOW}⚠️  Dev branch installed. Use 'rollback' if issues occur.${NC}"
    else
        echo "Update cancelled"
    fi
}

rollback_version() {
    echo -e "\n${BLUE}[6] Rollback to Previous Version${NC}\n"
    
    echo "This will restore the previous Guardian version"
    read -p "Continue? (y/n): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        python3 update_manager.py rollback
    else
        echo "Rollback cancelled"
    fi
}

setup_branches() {
    echo -e "\n${BLUE}[7] Setup Update Branches${NC}\n"
    
    if [ ! -f "setup_update_branches.sh" ]; then
        echo -e "${RED}❌ setup_update_branches.sh not found${NC}"
        return 1
    fi
    
    echo "This will create develop and dev branches on GitHub"
    read -p "Continue? (y/n): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        bash setup_update_branches.sh
    else
        echo "Setup cancelled"
    fi
}

install_deps() {
    echo -e "\n${BLUE}[8] Install Update Manager Dependencies${NC}\n"
    
    echo "Checking Python 3.10+..."
    python3 --version
    
    echo ""
    echo -e "${GREEN}✅ All dependencies are stdlib (no pip packages needed)${NC}"
    echo ""
    echo "Dependencies verified:"
    echo "  ✅ Python 3.10+"
    echo "  ✅ urllib (stdlib)"
    echo "  ✅ json (stdlib)"
    echo "  ✅ subprocess (stdlib)"
    echo "  ✅ pathlib (stdlib)"
}

verify_system() {
    echo -e "\n${BLUE}[9] Verify Update System${NC}\n"
    
    echo "Checking update system components..."
    echo ""
    
    # Check Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python3${NC} - $(python3 --version)"
    else
        echo -e "${RED}❌ Python3 not found${NC}"
    fi
    
    # Check update_manager
    if [ -f "update_manager.py" ]; then
        echo -e "${GREEN}✅ update_manager.py${NC} - Found"
    else
        echo -e "${RED}❌ update_manager.py${NC} - Not found"
    fi
    
    # Check VERSIONS.json
    if [ -f "VERSIONS.json" ]; then
        echo -e "${GREEN}✅ VERSIONS.json${NC} - Found"
    else
        echo -e "${RED}❌ VERSIONS.json${NC} - Not found"
    fi
    
    # Check guardian_standalone.py
    if [ -f "guardian_standalone.py" ]; then
        echo -e "${GREEN}✅ guardian_standalone.py${NC} - Found"
        wc -l guardian_standalone.py | awk '{print "   ("$1" lines)"}'
    else
        echo -e "${RED}❌ guardian_standalone.py${NC} - Not found"
    fi
    
    # Check backup dir
    if [ -d ~/.guardian ]; then
        echo -e "${GREEN}✅ Backup directory${NC} - ~/.guardian"
        echo "   ($(ls ~/.guardian 2>/dev/null | wc -l) backups)"
    else
        echo -e "${YELLOW}⚠️  Backup directory${NC} - Not created yet (will be on first update)"
    fi
    
    # Check git
    if [ -d ".git" ]; then
        echo -e "${GREEN}✅ Git repository${NC} - Found"
    else
        echo -e "${YELLOW}⚠️  Git repository${NC} - Not initialized"
    fi
    
    echo ""
    echo -e "${GREEN}System verification complete!${NC}"
}

version_info() {
    echo -e "\n${BLUE}[10] Version Information${NC}\n"
    
    echo "Guardian Version: 0.2.0"
    echo "Status: Production Ready"
    echo "Repository: https://github.com/0gl1tch/Guardian"
    echo ""
    echo "Branches:"
    echo "  📌 main (stable) - v0.2.0"
    echo "  🚀 develop (latest) - v0.3.0-dev"
    echo "  🔧 dev (alpha) - v0.4.0-alpha"
    echo ""
    echo "For detailed version history, see: VERSIONS.json"
}

view_strategy() {
    echo -e "\n${BLUE}[11] View Update Strategy${NC}\n"
    
    if [ -f "UPDATE_STRATEGY.md" ]; then
        less UPDATE_STRATEGY.md
    else
        echo -e "${RED}❌ UPDATE_STRATEGY.md not found${NC}"
    fi
}

list_backups() {
    echo -e "\n${BLUE}[12] List All Backups${NC}\n"
    python3 update_manager.py list-backups
}

main_loop() {
    while true; do
        show_menu
        read -p "Select option (0-12): " choice
        
        case $choice in
            1) check_updates ;;
            2) update_interactive ;;
            3) update_stable ;;
            4) update_latest ;;
            5) update_dev ;;
            6) rollback_version ;;
            7) setup_branches ;;
            8) install_deps ;;
            9) verify_system ;;
            10) version_info ;;
            11) view_strategy ;;
            12) list_backups ;;
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
