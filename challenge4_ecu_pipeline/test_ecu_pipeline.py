"""Tests for Challenge 4: ECU Release Pipeline."""
import pytest
from pathlib import Path
from ecu_pipeline import (
    read_version,
    validate_version,
    artifact_name,
    check_release_readiness,
)

BASE_DIR = Path(__file__).parent


class TestValidateVersion:
    def test_valid_semver(self):
        assert validate_version("v1.0.0") is True

    def test_valid_semver_multidigit(self):
        assert validate_version("v12.34.56") is True

    def test_missing_v_prefix(self):
        assert validate_version("1.0.0") is False

    def test_extra_suffix(self):
        assert validate_version("v1.0.0-beta") is False

    def test_empty_string(self):
        assert validate_version("") is False


class TestReadVersion:
    def test_reads_version_file(self):
        version = read_version()
        assert validate_version(version), f"VERSION file contains invalid version: {version}"


class TestArtifactName:
    def test_default_suffix(self):
        assert artifact_name("BCM", "v1.2.3") == "BCM_v1.2.3.bin"

    def test_custom_suffix(self):
        assert artifact_name("ECM", "v0.0.1", ".hex") == "ECM_v0.0.1.hex"

    def test_invalid_version_raises(self):
        with pytest.raises(ValueError):
            artifact_name("ECU", "1.0.0")


class TestCheckReleaseReadiness:
    def test_challenge_dir_is_ready(self):
        issues = check_release_readiness(BASE_DIR)
        assert issues == [], f"Release readiness issues: {issues}"

    def test_missing_version_file(self, tmp_path):
        (tmp_path / "Makefile").write_text("")
        (tmp_path / "README.md").write_text("")
        issues = check_release_readiness(tmp_path)
        assert any("VERSION" in issue for issue in issues)

    def test_invalid_version_in_file(self, tmp_path):
        (tmp_path / "VERSION").write_text("bad-version")
        (tmp_path / "Makefile").write_text("")
        (tmp_path / "README.md").write_text("")
        issues = check_release_readiness(tmp_path)
        assert any("VERSION" in issue for issue in issues)
