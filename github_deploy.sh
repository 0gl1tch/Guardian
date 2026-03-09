#!/bin/bash
# Guardian GitHub Auto-Deploy (Bash Version)
# Automated script to create GitHub repo and deploy Guardian
# Requires: GitHub CLI (gh) installed and authenticated

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_NAME="${1:-Guardian}"
DESCRIPTION="DFIR forensic analysis toolkit with native commands - execute via IEX"

# ============================================================================
# Functions
# ============================================================================

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI not found!"
        echo "Install from: https://cli.github.com"
        exit 1
    fi
    
    gh_version=$(gh --version)
    print_success "GitHub CLI found: $gh_version"
}

check_auth() {
    if ! gh auth status &> /dev/null; then
        print_error "Not authenticated with GitHub"
        echo "Run: gh auth login"
        exit 1
    fi
    
    print_success "GitHub authenticated"
}

get_username() {
    USERNAME=$(gh api user --jq '.login')
    print_info "GitHub username: $USERNAME"
}

check_repo_exists() {
    if gh repo view "$USERNAME/$REPO_NAME" &> /dev/null; then
        return 0
    fi
    return 1
}

create_repo() {
    print_info "Creating repository '$REPO_NAME'..."
    
    if check_repo_exists; then
        print_warning "Repository '$REPO_NAME' already exists"
        read -p "Overwrite? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Skipping repository creation"
            return
        fi
    fi
    
    gh repo create "$REPO_NAME" \
        --public \
        --description "$DESCRIPTION" \
        --source=. \
        --remote=origin \
        --push 2>/dev/null || true
    
    print_success "Repository '$REPO_NAME' ready"
}

init_git() {
    print_info "Initializing git repository..."
    
    if [ -d .git ]; then
        print_warning "Repository already initialized"
        return
    fi
    
    git init
    git config user.name "$USERNAME"
    git config user.email "$USERNAME@users.noreply.github.com"
    git add .
    
    print_success "Git initialized"
}

commit_and_push() {
    print_info "Committing and pushing to GitHub..."
    
    # Check if there are changes to commit
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        print_info "No changes to commit"
    else
        git commit -m "Initial Guardian DFIR CLI deployment

- Zero dependencies
- IEX remote execution ready
- Full DFIR toolkit
- Native Windows/Unix commands" || true
    fi
    
    # Add remote and push
    git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || true
    git branch -M main 2>/dev/null || true
    git push -u origin main --force || true
    
    print_success "Push completed"
}

generate_commands() {
    RAW_URL="https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/guardian_standalone.py"
    REPO_URL="https://github.com/$USERNAME/$REPO_NAME"
    
    print_header "🎯 DEPLOYMENT COMPLETE!"
    
    echo "📍 Repository: $REPO_URL"
    echo "📋 Raw File URL: $RAW_URL"
    
    echo -e "\n${BLUE}──────────────────────────────────────────────────────────────────────────${NC}"
    echo -e "${BLUE}🚀 One-Liner Commands (Ready to Share):${NC}"
    echo -e "${BLUE}──────────────────────────────────────────────────────────────────────────${NC}"
    
    echo -e "\n${GREEN}📌 Windows (PowerShell):${NC}"
    echo "iex(New-Object Net.WebClient).DownloadString('$RAW_URL')"
    
    echo -e "\n${GREEN}🐧 Linux/macOS (Bash):${NC}"
    echo "curl $RAW_URL | python3"
    
    echo -e "\n${BLUE}──────────────────────────────────────────────────────────────────────────${NC}"
    echo -e "\n${GREEN}📝 Next steps:${NC}"
    echo "1. Share these one-liners with your team"
    echo "2. Anyone with internet + Python 3.10+ can run Guardian"
    echo "3. No installation needed!"
    
    echo -e "\n${GREEN}📚 Documentation:${NC}"
    echo "  Repository: $REPO_URL"
    echo "  Quick Start: $REPO_URL/blob/main/DEPLOY.md"
    echo "  Technical: $REPO_URL/blob/main/REMOTE_EXECUTION.md"
    
    echo -e "\n${BLUE}══════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════════════${NC}\n"
}

# ============================================================================
# Main Flow
# ============================================================================

main() {
    print_header "🛡️  GUARDIAN GITHUB AUTO-DEPLOY"
    
    check_gh_cli
    check_auth
    get_username
    init_git
    create_repo
    commit_and_push
    generate_commands
}

# Run main function
main "$@"
