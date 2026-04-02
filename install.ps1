# Recruit CRM MCP — bootstrap installer for Windows
# Usage: powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.ps1 | iex"
#
# This script:
#   1. Installs uv (if not already installed)
#   2. Runs the interactive MCP installer via uvx

$ErrorActionPreference = "Stop"

Write-Host "========================================================"
Write-Host "  Recruit CRM MCP — Bootstrap Installer"
Write-Host "========================================================"
Write-Host ""

# --- Step 1: Ensure uv is available ---

$uvx = Get-Command uvx -ErrorAction SilentlyContinue
if ($uvx) {
    Write-Host "✓ uvx is already installed."
} else {
    Write-Host "Installing uv..."
    & ([scriptblock]::Create((irm https://astral.sh/uv/install.ps1)))

    # The uv installer adds its bin directory to the user PATH in the Windows
    # registry, but the current PowerShell session still has the old PATH.
    # Rebuild $env:PATH from the registry so uvx is available immediately.
    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $env:PATH = "$machinePath;$userPath"

    $uvx = Get-Command uvx -ErrorAction SilentlyContinue
    if (-not $uvx) {
        Write-Host ""
        Write-Error "uv was installed but 'uvx' is not on your PATH. Please restart PowerShell and re-run this script."
        return
    }
    Write-Host "✓ uv installed successfully."
}

Write-Host ""

# --- Step 2: Run the interactive installer ---

& uvx --from recruit-crm-mcp recruit-crm-mcp-install
if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
