"""Tests for the one-click installer."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from recruit_crm_mcp.install import (
    _find_msix_config_path,
    backup_config,
    find_uvx,
    inject_server,
    load_config,
    main,
    prompt_install_uv,
    write_config,
)

UVX_PATH = "/usr/local/bin/uvx"


class TestFindUvx:
    def test_found(self):
        with patch("recruit_crm_mcp.install.shutil.which", return_value=UVX_PATH):
            assert find_uvx() == UVX_PATH

    def test_not_found(self):
        with patch("recruit_crm_mcp.install.shutil.which", return_value=None):
            assert find_uvx() is None


class TestInjectServer:
    def test_empty_config(self):
        config = inject_server({}, "test-key-123", UVX_PATH)
        assert config == {
            "mcpServers": {
                "recruit-crm": {
                    "command": UVX_PATH,
                    "args": ["--refresh-package", "recruit-crm-mcp", "recruit-crm-mcp"],
                    "env": {"RECRUIT_CRM_API_KEY": "test-key-123"},
                }
            }
        }

    def test_args_include_refresh_package_flag(self):
        """Auto-update guarantee: every install gets --refresh-package so users
        pick up new releases on the next Claude Desktop launch without manual
        cache invalidation."""
        config = inject_server({}, "k", UVX_PATH)
        args = config["mcpServers"]["recruit-crm"]["args"]
        assert args[0] == "--refresh-package"
        assert args[1] == "recruit-crm-mcp"
        assert args[-1] == "recruit-crm-mcp"  # tool name is always the last arg

    def test_uses_absolute_uvx_path(self):
        config = inject_server({}, "key", "/home/user/.local/bin/uvx")
        entry = config["mcpServers"]["recruit-crm"]
        assert entry["command"] == "/home/user/.local/bin/uvx"

    def test_preserves_existing_servers(self):
        config = {
            "mcpServers": {
                "other-server": {"command": "other", "args": []},
            }
        }
        result = inject_server(config, "key-456", UVX_PATH)
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
        result = inject_server(config, "new-key", UVX_PATH)
        entry = result["mcpServers"]["recruit-crm"]
        assert entry["command"] == UVX_PATH
        assert entry["env"]["RECRUIT_CRM_API_KEY"] == "new-key"

    def test_preserves_non_mcp_keys(self):
        config = {"theme": "dark", "mcpServers": {}}
        result = inject_server(config, "key", UVX_PATH)
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

    def test_invalid_json(self, tmp_path: Path):
        config_path = tmp_path / "config.json"
        config_path.write_text("{invalid json")
        with pytest.raises(SystemExit, match="invalid JSON"):
            load_config(config_path)


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



class TestFindMsixConfigPath:
    def test_no_localappdata(self):
        with patch.dict("os.environ", {}, clear=True):
            assert _find_msix_config_path() is None

    def test_no_packages_dir(self, tmp_path: Path):
        with patch.dict("os.environ", {"LOCALAPPDATA": str(tmp_path)}):
            # No Packages directory exists
            assert _find_msix_config_path() is None

    def test_no_claude_package(self, tmp_path: Path):
        packages_dir = tmp_path / "Packages"
        packages_dir.mkdir()
        with patch.dict("os.environ", {"LOCALAPPDATA": str(tmp_path)}):
            assert _find_msix_config_path() is None

    def test_msix_path_found(self, tmp_path: Path):
        packages_dir = tmp_path / "Packages"
        claude_pkg = packages_dir / "Claude_pzs8sxrjxfjjc"
        claude_pkg.mkdir(parents=True)
        with patch.dict("os.environ", {"LOCALAPPDATA": str(tmp_path)}):
            result = _find_msix_config_path()
            assert result is not None
            assert "LocalCache" in str(result)
            assert "Roaming" in str(result)
            assert result.name == "claude_desktop_config.json"


class TestGetConfigPath:
    def test_mac(self):
        with patch("recruit_crm_mcp.install.platform.system", return_value="Darwin"):
            from recruit_crm_mcp.install import get_config_path

            path = get_config_path()
            assert "Application Support" in str(path)
            assert path.name == "claude_desktop_config.json"

    def test_windows_standard(self):
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Windows"),
            patch(
                "recruit_crm_mcp.install._find_msix_config_path", return_value=None
            ),
            patch.dict("os.environ", {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}),
        ):
            from recruit_crm_mcp.install import get_config_path

            path = get_config_path()
            assert "Roaming" in str(path)
            assert path.name == "claude_desktop_config.json"

    def test_windows_msix(self, tmp_path: Path):
        msix_path = (
            tmp_path
            / "Packages"
            / "Claude_abc123"
            / "LocalCache"
            / "Roaming"
            / "Claude"
            / "claude_desktop_config.json"
        )
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Windows"),
            patch(
                "recruit_crm_mcp.install._find_msix_config_path",
                return_value=msix_path,
            ),
        ):
            from recruit_crm_mcp.install import get_config_path

            path = get_config_path()
            assert path == msix_path

    def test_windows_msix_preferred_over_standard(self, tmp_path: Path):
        """MSIX path takes precedence when Windows Store install is detected."""
        msix_path = tmp_path / "msix" / "claude_desktop_config.json"
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Windows"),
            patch(
                "recruit_crm_mcp.install._find_msix_config_path",
                return_value=msix_path,
            ),
            patch.dict("os.environ", {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}),
        ):
            from recruit_crm_mcp.install import get_config_path

            path = get_config_path()
            assert path == msix_path

    def test_unsupported_os(self):
        with patch("recruit_crm_mcp.install.platform.system", return_value="Linux"):
            from recruit_crm_mcp.install import get_config_path

            with pytest.raises(SystemExit, match="Unsupported operating system"):
                get_config_path()


class TestPromptInstallUv:
    def test_user_declines(self):
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Darwin"),
            patch("builtins.input", return_value="n"),
        ):
            with pytest.raises(SystemExit, match="Please install uv"):
                prompt_install_uv()

    def test_user_accepts_darwin(self):
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Darwin"),
            patch("builtins.input", return_value="y"),
            patch("recruit_crm_mcp.install._auto_install_uv") as mock_auto,
        ):
            prompt_install_uv()
            mock_auto.assert_called_once_with("Darwin")

    def test_user_accepts_default(self):
        """Pressing Enter (empty input) should proceed with install."""
        with (
            patch("recruit_crm_mcp.install.platform.system", return_value="Darwin"),
            patch("builtins.input", return_value=""),
            patch("recruit_crm_mcp.install._auto_install_uv") as mock_auto,
        ):
            prompt_install_uv()
            mock_auto.assert_called_once_with("Darwin")


class TestAutoInstallUv:
    def test_darwin_success(self):
        with (
            patch("recruit_crm_mcp.install.subprocess.run") as mock_run,
            patch("recruit_crm_mcp.install.find_uvx", return_value=UVX_PATH),
        ):
            from recruit_crm_mcp.install import _auto_install_uv

            _auto_install_uv("Darwin")
            mock_run.assert_called_once()
            assert "curl" in str(mock_run.call_args)

    def test_subprocess_failure(self):
        import subprocess

        with patch(
            "recruit_crm_mcp.install.subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "sh"),
        ):
            from recruit_crm_mcp.install import _auto_install_uv

            with pytest.raises(SystemExit, match="Automatic installation failed"):
                _auto_install_uv("Darwin")

    def test_uvx_not_on_path_after_install(self):
        with (
            patch("recruit_crm_mcp.install.subprocess.run"),
            patch("recruit_crm_mcp.install.find_uvx", return_value=None),
        ):
            from recruit_crm_mcp.install import _auto_install_uv

            with pytest.raises(SystemExit, match="not yet on your PATH"):
                _auto_install_uv("Darwin")


class TestMain:
    def test_success_new_config(self, tmp_path: Path):
        """Full flow: uvx present, no existing config, writes new config."""
        config_path = tmp_path / "claude_desktop_config.json"
        with (
            patch("recruit_crm_mcp.install.find_uvx", return_value=UVX_PATH),
            patch("recruit_crm_mcp.install.get_config_path", return_value=config_path),
            patch("recruit_crm_mcp.install.getpass", return_value="test-key-123"),
        ):
            main()

        data = json.loads(config_path.read_text())
        entry = data["mcpServers"]["recruit-crm"]
        assert entry["command"] == UVX_PATH
        assert entry["env"]["RECRUIT_CRM_API_KEY"] == "test-key-123"

    def test_success_existing_config(self, tmp_path: Path):
        """Full flow: existing config is backed up and merged."""
        config_path = tmp_path / "claude_desktop_config.json"
        config_path.write_text(json.dumps({"mcpServers": {"other": {"command": "x"}}}))

        with (
            patch("recruit_crm_mcp.install.find_uvx", return_value=UVX_PATH),
            patch("recruit_crm_mcp.install.get_config_path", return_value=config_path),
            patch("recruit_crm_mcp.install.getpass", return_value="key-456"),
        ):
            main()

        data = json.loads(config_path.read_text())
        assert "other" in data["mcpServers"]
        assert "recruit-crm" in data["mcpServers"]
        # Verify backup was created
        backups = list(tmp_path.glob("*.backup-*.json"))
        assert len(backups) == 1

    def test_missing_uvx_triggers_prompt(self, tmp_path: Path):
        """When uvx is missing, prompt_install_uv is called, then find_uvx resolves."""
        config_path = tmp_path / "claude_desktop_config.json"
        with (
            patch("recruit_crm_mcp.install.find_uvx", side_effect=[None, UVX_PATH]),
            patch("recruit_crm_mcp.install.get_config_path", return_value=config_path),
            patch("recruit_crm_mcp.install.prompt_install_uv") as mock_prompt,
            patch("recruit_crm_mcp.install.getpass", return_value="key"),
        ):
            main()
            mock_prompt.assert_called_once()

    def test_keyboard_interrupt(self, tmp_path: Path):
        """Ctrl+C exits gracefully without a traceback."""
        with (
            patch("recruit_crm_mcp.install.find_uvx", side_effect=KeyboardInterrupt),
        ):
            # Should return cleanly, not raise
            main()

    def test_empty_api_key_reprompts(self, tmp_path: Path):
        """Empty API key input causes a re-prompt."""
        config_path = tmp_path / "claude_desktop_config.json"
        with (
            patch("recruit_crm_mcp.install.find_uvx", return_value=UVX_PATH),
            patch("recruit_crm_mcp.install.get_config_path", return_value=config_path),
            patch("recruit_crm_mcp.install.getpass", side_effect=["", "  ", "real-key"]),
        ):
            main()

        data = json.loads(config_path.read_text())
        assert data["mcpServers"]["recruit-crm"]["env"]["RECRUIT_CRM_API_KEY"] == "real-key"
