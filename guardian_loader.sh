#!/bin/bash
# Guardian DFIR CLI Loader - Bash Version
# Usage: curl -s https://your-server/guardian_loader.sh | bash
# or: bash <(curl -s https://your-server/guardian_loader.sh)

set -e

echo "🛡️  Guardian DFIR CLI - Loading..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is required but not installed."
    echo "[!] Please install Python 3.10+ first"
    exit 1
fi

# Configuration - Change these to your server
GITHUB_USERNAME="your-username"
GITHUB_REPO="Guardian"
GITHUB_BRANCH="main"

# Build the raw content URL (using GitHub as default)
RAW_URL="https://raw.githubusercontent.com/$GITHUB_USERNAME/$GITHUB_REPO/$GITHUB_BRANCH/guardian_standalone.py"

# Alternative: Use custom server
# RAW_URL="https://your-server.com/guardian_standalone.py"

echo "[*] Downloading Guardian DFIR CLI..."

# Download and execute in one step (completely in-memory)
if command -v curl &> /dev/null; then
    curl -s "$RAW_URL" | python3
elif command -v wget &> /dev/null; then
    wget -q -O - "$RAW_URL" | python3
else
    echo "[!] Neither curl nor wget is available"
    exit 1
fi
