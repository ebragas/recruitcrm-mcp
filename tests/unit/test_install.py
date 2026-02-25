"""Tests for the one-click installer."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from recruit_crm_mcp.install import (
    backup_config,
    check_uvx,
    inject_server,
    load_config,
    write_config,
)


class TestCheckUvx:
    def test_found(self):
        with patch("recruit_crm_mcp.install.shutil.which", return_value="/usr/local/bin/uvx"):
            assert check_uvx() is True

    def test_not_found(self):
        with patch("recruit_crm_mcp.install.shutil.which", return_value=None):
            assert check_uvx() is False


class TestInjectServer:
    def test_empty_config(self):
        config = inject_server({}, "test-key-123")
        assert config == {
            "mcpServers": {
                "recruit-crm": {
                    "command": "uvx",
                    "args": ["recruit-crm-mcp"],
                    "env": {"RECRUIT_CRM_API_KEY": "test-key-123"},
                }
            }
        }

    def test_preserves_existing_servers(self):
        config = {
            "mcpServers": {
                "other-server": {"command": "other", "args": []},
            }
        }
        result = inject_server(config, "key-456")
        assert "other-server" in result["mcpServers"]
        assert "recruit-crm" in result["mcpServers"]

    def test_overwrites_existing_entry(self):
        config = {
            "mcpServers": {
                "recruit-crm": {
                    "command": "old-command",
                    "env": {"RECRUIT_CRM_API_KEY": "old-key"},
                }
            }
        }
        result = inject_server(config, "new-key")
        entry = result["mcpServers"]["recruit-crm"]
        assert entry["command"] == "uvx"
        assert entry["env"]["RECRUIT_CRM_API_KEY"] == "new-key"

    def test_preserves_non_mcp_keys(self):
        config = {"theme": "dark", "mcpServers": {}}
        result = inject_server(config, "key")
        assert result["theme"] == "dark"


class TestBackupConfig:
    def test_no_file(self, tmp_path: Path):
        config_path = tmp_path / "claude_desktop_config.json"
        assert backup_config(config_path) is None

    def test_creates_backup(self, tmp_path: Path):
        config_path = tmp_path / "claude_desktop_config.json"
        config_path.write_text('{"existing": true}')

        backup_path = backup_config(config_path)
        assert backup_path is not None
        assert backup_path.exists()
        assert json.loads(backup_path.read_text()) == {"existing": True}
        assert "backup-" in backup_path.name


class TestLoadConfig:
    def test_missing_file(self, tmp_path: Path):
        config_path = tmp_path / "nonexistent.json"
        assert load_config(config_path) == {}

    def test_existing_file(self, tmp_path: Path):
        config_path = tmp_path / "config.json"
        config_path.write_text('{"mcpServers": {}}')
        assert load_config(config_path) == {"mcpServers": {}}


class TestWriteConfig:
    def test_creates_parent_dirs(self, tmp_path: Path):
        config_path = tmp_path / "nested" / "dir" / "config.json"
        write_config(config_path, {"key": "value"})
        assert config_path.exists()
        assert json.loads(config_path.read_text()) == {"key": "value"}

    def test_trailing_newline(self, tmp_path: Path):
        config_path = tmp_path / "config.json"
        write_config(config_path, {})
        assert config_path.read_text().endswith("\n")


class TestGetConfigPath:
    def test_mac(self):
        with patch("recruit_crm_mcp.install.platform.system", return_value="Darwin"):
            from recruit_crm_mcp.install import get_config_path

            path = get_config_path()
            assert "Application Support" in str(path)
            assert path.name == "claude_desktop_config.json"

    def test_windows(self):
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Windows"),
            patch.dict("os.environ", {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}),
        ):
            from recruit_crm_mcp.install import get_config_path

            path = get_config_path()
            assert "Claude" in str(path)
            assert path.name == "claude_desktop_config.json"

    def test_unsupported_os(self):
        with patch("recruit_crm_mcp.install.platform.system", return_value="Linux"):
            from recruit_crm_mcp.install import get_config_path

            with pytest.raises(SystemExit, match="Unsupported operating system"):
                get_config_path()
