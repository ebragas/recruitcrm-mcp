"""One-click installer for the Recruit CRM MCP server in Claude Desktop."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

MCP_SERVER_ARGS = ["recruit-crm-mcp"]


def _find_msix_config_path() -> Path | None:
    """Return the Claude Desktop config path for Windows Store (MSIX) installs.

    Windows Store apps run in a sandboxed environment where %APPDATA% is
    virtualized to %LOCALAPPDATA%/Packages/<package>/LocalCache/Roaming/.
    External processes must write to the sandboxed path directly.
    """
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        return None
    packages_dir = Path(local_appdata) / "Packages"
    if not packages_dir.exists():
        return None
    claude_dirs = list(packages_dir.glob("Claude_*"))
    if not claude_dirs:
        return None
    return (
        claude_dirs[0]
        / "LocalCache"
        / "Roaming"
        / "Claude"
        / "claude_desktop_config.json"
    )


def get_config_path() -> Path:
    """Return the path to claude_desktop_config.json for the current OS."""
    system = platform.system()
    if system == "Darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "Claude"
            / "claude_desktop_config.json"
        )
    if system == "Windows":
        # Windows Store (MSIX) installs use a sandboxed config path
        msix_path = _find_msix_config_path()
        if msix_path:
            return msix_path
        # Fall back to standard (direct installer) path
        appdata = os.environ.get("APPDATA", "")
        if not appdata:
            raise SystemExit("Error: APPDATA environment variable is not set.")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    raise SystemExit(
        f"Error: Unsupported operating system '{system}'. "
        "This installer supports macOS and Windows."
    )


def find_uvx() -> str | None:
    """Return the absolute path to uvx, or None if not found."""
    return shutil.which("uvx")


def prompt_install_uv() -> None:
    """Guide the user to install uv/uvx if missing."""
    print("\n⚠  'uvx' was not found on your PATH.")
    print("   The Recruit CRM MCP server requires 'uv' to run.")
    print()
    system = platform.system()
    if system == "Darwin":
        print("   To install manually, open Terminal and run:")
        print("     curl -LsSf https://astral.sh/uv/install.sh | sh")
    elif system == "Windows":
        print("   To install manually, open PowerShell and run:")
        print("     powershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
    print()

    answer = input("Would you like to install it now? [Y/n] ").strip()
    if answer.lower() in ("n", "no"):
        raise SystemExit(
            "Please install uv (https://docs.astral.sh/uv/getting-started/installation/) "
            "and re-run this installer."
        )
    _auto_install_uv(system)


def _auto_install_uv(system: str) -> None:
    """Attempt to install uv automatically."""
    print("\nInstalling uv…")
    try:
        if system == "Darwin":
            subprocess.run(
                ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
                check=True,
            )
        elif system == "Windows":
            subprocess.run(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "ByPass",
                    "-c",
                    "irm https://astral.sh/uv/install.ps1 | iex",
                ],
                check=True,
            )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SystemExit(f"Automatic installation failed: {exc}") from exc

    # The installer may have modified shell profile files that won't be
    # reloaded in the current process, so uvx may not be on PATH yet.
    if not find_uvx():
        raise SystemExit(
            "uv installation completed, but 'uvx' is not yet on your PATH.\n"
            "Please restart your terminal (or open a new one) and re-run this installer."
        )
    print("✓ uv installed successfully.\n")


def backup_config(config_path: Path) -> Path | None:
    """Back up existing config file. Returns backup path or None if no file existed."""
    if not config_path.exists():
        return None
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = config_path.with_suffix(f".backup-{timestamp}.json")
    shutil.copy2(config_path, backup_path)
    return backup_path


def load_config(config_path: Path) -> dict:
    """Load existing config or return empty structure."""
    if not config_path.exists():
        return {}
    try:
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise SystemExit(
            f"Error: {config_path} contains invalid JSON.\n"
            "Please fix the file manually or restore from a backup "
            "(look for .backup-*.json files in the same directory)."
        )


def inject_server(config: dict, api_key: str, uvx_path: str) -> dict:
    """Add or update the recruit-crm MCP server entry in the config."""
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    entry = {
        "command": uvx_path,
        "args": MCP_SERVER_ARGS,
        "env": {"RECRUIT_CRM_API_KEY": api_key},
    }
    config["mcpServers"]["recruit-crm"] = entry
    return config


def write_config(config_path: Path, config: dict) -> None:
    """Write config JSON to disk, creating parent directories if needed."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def main() -> None:
    try:
        print("=" * 56)
        print("  Recruit CRM MCP — Claude Desktop Installer")
        print("=" * 56)
        print()

        # 1. Pre-requisite check
        uvx_path = find_uvx()
        if not uvx_path:
            prompt_install_uv()
            uvx_path = find_uvx()
            if not uvx_path:
                raise SystemExit("Error: could not locate uvx after installation.")

        # 2. Detect config path
        config_path = get_config_path()
        print(f"Claude Desktop config: {config_path}")

        if config_path.exists():
            print("  ✓ Config file found.")
        else:
            print("  • Config file does not exist yet — it will be created.")
        print()

        # 3. Prompt for API key
        api_key = ""
        while not api_key.strip():
            api_key = getpass("Enter your Recruit CRM API key: ")
            if not api_key.strip():
                print("  API key cannot be empty. Please try again.")
        print()

        # 4. Backup existing config
        backup_path = backup_config(config_path)
        if backup_path:
            print(f"  ✓ Backed up existing config to:\n    {backup_path}")

        # 5. Load, inject, write
        config = load_config(config_path)
        config = inject_server(config, api_key.strip(), uvx_path)
        write_config(config_path, config)

        print(f"  ✓ Wrote updated config to:\n    {config_path}")
        print()
        print("Done! Restart Claude Desktop to start using the Recruit CRM MCP server.")
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled.")
        return


if __name__ == "__main__":
    main()
