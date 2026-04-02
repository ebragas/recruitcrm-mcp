#!/usr/bin/env bash
# Recruit CRM MCP — bootstrap installer
# Usage: curl -LsSf https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.sh | bash
#
# This script:
#   1. Installs uv (if not already installed)
#   2. Runs the interactive MCP installer via uvx

set -euo pipefail

echo "========================================================"
echo "  Recruit CRM MCP — Bootstrap Installer"
echo "========================================================"
echo

# --- Step 1: Ensure uv is available ---

if command -v uvx >/dev/null 2>&1; then
    echo "✓ uvx is already installed."
else
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Source the env file that the uv installer creates, so uvx is on PATH
    # in this session without requiring a terminal restart.
    if [ -f "$HOME/.local/bin/env" ]; then
        # shellcheck source=/dev/null
        . "$HOME/.local/bin/env"
    elif [ -f "$HOME/.cargo/env" ]; then
        # shellcheck source=/dev/null
        . "$HOME/.cargo/env"
    fi

    if ! command -v uvx >/dev/null 2>&1; then
        echo
        echo "Error: uv was installed but 'uvx' is not on your PATH."
        echo "Please restart your terminal and re-run this script."
        exit 1
    fi
    echo "✓ uv installed successfully."
fi

echo

# --- Step 2: Run the interactive installer ---

uvx --from recruit-crm-mcp recruit-crm-mcp-install

echo

# --- Step 3: Pre-cache packages for Claude Desktop ---
# Claude Desktop launches the server via `uvx recruit-crm-mcp`. On first run,
# uvx must download ~70 packages which can exceed the 60-second init timeout.
# Warm the cache now so the first Claude Desktop launch is fast.

echo "Pre-caching packages for fast startup..."
uvx --from recruit-crm-mcp python -c "print('ok')" > /dev/null 2>&1
echo "✓ Packages cached. Claude Desktop will start quickly."
