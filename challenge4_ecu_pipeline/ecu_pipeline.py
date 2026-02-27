"""Challenge 4: ECU Release Pipeline – build & static-analysis helpers.

This module is invoked by the Makefile and the GitHub Actions workflow.
It provides version stamping, artifact naming, and a lightweight
release-readiness check.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Version helpers
# ---------------------------------------------------------------------------

VERSION_FILE = Path(__file__).parent / "VERSION"


def read_version() -> str:
    """Return the current ECU software version string from VERSION file."""
    return VERSION_FILE.read_text().strip()


def validate_version(version: str) -> bool:
    """Return True if *version* matches the semantic-versioning pattern vMAJOR.MINOR.PATCH."""
    return bool(re.fullmatch(r"v\d+\.\d+\.\d+", version))


# ---------------------------------------------------------------------------
# Artifact naming
# ---------------------------------------------------------------------------


def artifact_name(ecu_id: str, version: str, suffix: str = ".bin") -> str:
    """Return a canonical artifact filename.

    Args:
        ecu_id:  ECU identifier string (e.g. 'BCM', 'ECM').
        version: Version string (e.g. 'v1.2.3').
        suffix:  File extension including the dot (default '.bin').

    Returns:
        Canonical filename such as 'BCM_v1.2.3.bin'.
    """
    if not validate_version(version):
        raise ValueError(f"Invalid version '{version}'. Expected format: vMAJOR.MINOR.PATCH")
    return f"{ecu_id}_{version}{suffix}"


# ---------------------------------------------------------------------------
# Release readiness check
# ---------------------------------------------------------------------------

REQUIRED_FILES = [
    "VERSION",
    "Makefile",
    "README.md",
]


def check_release_readiness(base_dir: str | Path = ".") -> list[str]:
    """Return a list of issues blocking a release.

    Args:
        base_dir: Root directory to inspect.

    Returns:
        List of issue strings; empty list means the release is ready.
    """
    base_dir = Path(base_dir)
    issues: list[str] = []

    for required in REQUIRED_FILES:
        if not (base_dir / required).exists():
            issues.append(f"Missing required file: {required}")

    version_path = base_dir / "VERSION"
    if version_path.exists():
        version = version_path.read_text().strip()
        if not validate_version(version):
            issues.append(
                f"VERSION file contains '{version}' which does not match vMAJOR.MINOR.PATCH"
            )

    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ECU Release Pipeline helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="Print the current ECU software version.")

    art = sub.add_parser("artifact-name", help="Compute a canonical artifact name.")
    art.add_argument("ecu_id", metavar="ECU_ID")
    art.add_argument("--suffix", default=".bin")

    sub.add_parser("check", help="Run release readiness checks.")

    args = parser.parse_args()

    if args.command == "version":
        print(read_version())
    elif args.command == "artifact-name":
        version = read_version()
        print(artifact_name(args.ecu_id, version, args.suffix))
    elif args.command == "check":
        issues = check_release_readiness(Path(__file__).parent)
        if issues:
            for issue in issues:
                print(f"[FAIL] {issue}", file=sys.stderr)
            sys.exit(1)
        else:
            print("[PASS] Release readiness check passed.")


if __name__ == "__main__":
    main()
