"""Challenge 3: ARXML Watchdog Boilerplate – parser/validator helper.

Provides lightweight utilities to parse and inspect the watchdog.arxml
boilerplate without requiring a full AUTOSAR tool-chain.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List


# AUTOSAR R4 namespace
_NS = {"ar": "http://autosar.org/schema/r4.0"}


def load_arxml(path: str | Path) -> ET.Element:
    """Parse an ARXML file and return the root element.

    Args:
        path: Path to the .arxml file.

    Returns:
        Root XML element (AUTOSAR).
    """
    tree = ET.parse(str(path))
    return tree.getroot()


def get_component_names(root: ET.Element) -> List[str]:
    """Return SHORT-NAMEs of all AtomicSwComponentType and CompositionSwComponentType.

    Args:
        root: Root element returned by :func:`load_arxml`.

    Returns:
        Sorted list of component short-names found in the file.
    """
    names: List[str] = []
    tags = (
        "{http://autosar.org/schema/r4.0}ATOMIC-SW-COMPONENT-TYPE",
        "{http://autosar.org/schema/r4.0}COMPOSITION-SW-COMPONENT-TYPE",
    )
    for elem in root.iter():
        if elem.tag in tags:
            short_name = elem.find(
                "{http://autosar.org/schema/r4.0}SHORT-NAME"
            )
            if short_name is not None and short_name.text:
                names.append(short_name.text.strip())
    return sorted(names)


def get_runnables(root: ET.Element) -> List[str]:
    """Return SHORT-NAMEs of all RunnableEntity elements.

    Args:
        root: Root element returned by :func:`load_arxml`.

    Returns:
        Sorted list of runnable short-names.
    """
    names: List[str] = []
    tag = "{http://autosar.org/schema/r4.0}RUNNABLE-ENTITY"
    for elem in root.iter(tag):
        short_name = elem.find("{http://autosar.org/schema/r4.0}SHORT-NAME")
        if short_name is not None and short_name.text:
            names.append(short_name.text.strip())
    return sorted(names)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Inspect an AUTOSAR ARXML Watchdog file."
    )
    parser.add_argument(
        "arxml",
        nargs="?",
        default=str(Path(__file__).parent / "watchdog.arxml"),
        help="Path to the .arxml file (default: watchdog.arxml in this directory).",
    )
    args = parser.parse_args()

    root = load_arxml(args.arxml)
    print(f"Loaded: {args.arxml}")

    components = get_component_names(root)
    print(f"\nSoftware Components ({len(components)}):")
    for c in components:
        print(f"  • {c}")

    runnables = get_runnables(root)
    print(f"\nRunnables ({len(runnables)}):")
    for r in runnables:
        print(f"  • {r}")


if __name__ == "__main__":
    main()
