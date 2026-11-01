"""Regression tests for the Gemini FastAPI startup migration script."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "gemini-fastapi" / "scripts" / "run.sh"


class RunScriptTests(unittest.TestCase):
    """Test the one-time migration in run.sh."""

    def setUp(self) -> None:
        """Create an isolated homeassistant, data and app layout."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.root = Path(self.temp_dir.name)
        self.homeassistant = self.root / "homeassistant"
        self.legacy = self.homeassistant / "gemini-fastapi"
        self.legacy_config = self.legacy / "config"
        self.legacy_data = self.legacy / "data"
        self.marker = self.root / "data" / ".homeassistant-migrated"
        self.storage = self.root / "data" / "storage"
        self.app_dir = self.root / "app"
        self.app_data = self.app_dir / "data"
        self.app_dir.mkdir(parents=True)

        self.env = os.environ.copy()
        self.env.update(
            {
                "HOMEASSISTANT_DIR": str(self.homeassistant),
                "LEGACY_DIR": str(self.legacy),
                "LEGACY_CONFIG_DIR": str(self.legacy_config),
                "LEGACY_DATA_DIR": str(self.legacy_data),
                "MIGRATION_MARKER": str(self.marker),
                "DATA_DIR": str(self.storage),
                "APP_DIR": str(self.app_dir),
                "APP_DATA_DIR": str(self.app_data),
                "PYTHON": "/bin/true",
                "RUN_SCRIPT": str(self.root / "apply_options.py"),
            },
        )

    def run_script(self) -> subprocess.CompletedProcess[str]:
        """Run the startup script with all paths redirected into the test directory."""
        return subprocess.run(
            ["bash", str(SCRIPT)],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    def create_legacy_config(self) -> None:
        """Create the legacy configuration directory and file."""
        self.legacy_config.mkdir(parents=True)
        (self.legacy_config / "config.yaml").write_text("old config", encoding="utf-8")

    def create_legacy_data(self) -> None:
        """Create the legacy conversation data."""
        (self.legacy_data / "lmdb").mkdir(parents=True)
        (self.legacy_data / "lmdb" / "data.mdb").write_text("old data", encoding="utf-8")

    def test_first_start_migrates_data_and_removes_legacy_layout(self) -> None:
        """The first start moves data, removes config and records the migration."""
        self.create_legacy_config()
        self.create_legacy_data()

        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert not self.legacy_config.exists()
        assert not self.legacy_data.exists()
        assert (self.storage / "lmdb" / "data.mdb").read_text(encoding="utf-8") == "old data"
        assert self.marker.is_file()
        assert self.app_data.is_symlink()
        assert self.app_data.resolve() == self.storage.resolve()

    def test_second_start_is_idempotent(self) -> None:
        """A second start keeps the migrated storage and does not rerun the migration."""
        self.create_legacy_config()
        self.create_legacy_data()
        assert self.run_script().returncode == 0

        (self.storage / "new.txt").write_text("new data", encoding="utf-8")
        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert (self.storage / "new.txt").read_text(encoding="utf-8") == "new data"
        assert self.marker.is_file()

    def test_missing_homeassistant_defers_migration(self) -> None:
        """A missing configuration folder starts the App and retries later."""
        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert not self.marker.exists()
        assert self.app_data.is_symlink()
        assert "not available" in result.stderr

    def test_existing_storage_is_not_overwritten(self) -> None:
        """Legacy data is left untouched when /data/storage already has data."""
        self.create_legacy_config()
        self.create_legacy_data()
        (self.storage / "lmdb").mkdir(parents=True)
        (self.storage / "lmdb" / "current.mdb").write_text("current data", encoding="utf-8")

        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert (self.storage / "lmdb" / "current.mdb").read_text(encoding="utf-8") == "current data"
        assert self.legacy_data.is_dir()
        assert self.legacy_config.is_dir()
        assert not self.marker.exists()
        assert "already contains data" in result.stderr

    def test_legacy_config_is_removed_when_no_data_exists(self) -> None:
        """A config-only legacy layout is retired and marked complete."""
        self.create_legacy_config()

        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert not self.legacy_config.exists()
        assert self.storage.is_dir()
        assert self.marker.is_file()

    def test_existing_storage_is_kept_without_legacy_data(self) -> None:
        """Existing storage is left intact when only the old config remains."""
        self.create_legacy_config()
        (self.storage / "lmdb").mkdir(parents=True)
        (self.storage / "lmdb" / "current.mdb").write_text("current data", encoding="utf-8")

        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert (self.storage / "lmdb" / "current.mdb").read_text(encoding="utf-8") == "current data"
        assert not self.legacy_config.exists()
        assert self.marker.is_file()

    def test_fresh_layout_is_marked(self) -> None:
        """A fresh installation records the migration without legacy folders."""
        self.homeassistant.mkdir(parents=True)

        result = self.run_script()

        assert result.returncode == 0, result.stderr
        assert self.storage.is_dir()
        assert self.marker.is_file()
        assert self.app_data.is_symlink()


if __name__ == "__main__":
    unittest.main()
