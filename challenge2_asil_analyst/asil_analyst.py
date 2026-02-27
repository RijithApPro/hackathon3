"""Challenge 2: ISO 26262 ASIL Decomposition Analyst

ISO 26262 defines Automotive Safety Integrity Levels (ASIL) for road vehicles.
This tool computes valid ASIL decompositions and validates proposed decompositions.

ASIL Decomposition Rule:
  A safety goal with ASIL X can be split into two independent sub-requirements
  whose combined ASIL level equals X.  Independence is mandatory.

ASIL numeric mapping  (QM=0, A=1, B=2, C=3, D=4):
  Valid decompositions for each ASIL level
    ASIL D → (D, QM) | (C, A) | (B, B)
    ASIL C → (C, QM) | (B, A)
    ASIL B → (B, QM) | (A, A)
    ASIL A → (A, QM)
"""

from __future__ import annotations

from typing import List, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ASIL_LEVELS = ("QM", "A", "B", "C", "D")
ASIL_VALUE: dict[str, int] = {level: i for i, level in enumerate(ASIL_LEVELS)}

# Pre-computed decomposition table: original → sorted list of (part_a, part_b)
# Both parts satisfy  value(part_a) + value(part_b) == value(original)
DECOMPOSITIONS: dict[str, List[Tuple[str, str]]] = {
    "D": [("D", "QM"), ("C", "A"), ("B", "B")],
    "C": [("C", "QM"), ("B", "A")],
    "B": [("B", "QM"), ("A", "A")],
    "A": [("A", "QM")],
    "QM": [],  # QM cannot be decomposed further
}


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------


def get_decompositions(asil: str) -> List[Tuple[str, str]]:
    """Return valid decompositions for the given ASIL level.

    Args:
        asil: One of 'QM', 'A', 'B', 'C', 'D' (case-insensitive).

    Returns:
        List of (part_a, part_b) tuples representing valid decompositions.

    Raises:
        ValueError: If *asil* is not a recognised level.
    """
    asil = _validate(asil)
    return list(DECOMPOSITIONS[asil])


def is_valid_decomposition(original: str, part_a: str, part_b: str) -> bool:
    """Check whether (*part_a*, *part_b*) is a valid decomposition of *original*.

    The check is symmetric: order of parts does not matter.

    Args:
        original: The ASIL level of the original safety goal.
        part_a:   ASIL level of the first independent sub-requirement.
        part_b:   ASIL level of the second independent sub-requirement.

    Returns:
        True if the decomposition is valid according to ISO 26262.
    """
    original = _validate(original)
    part_a = _validate(part_a)
    part_b = _validate(part_b)

    pair = tuple(sorted([part_a, part_b], key=lambda x: ASIL_VALUE[x], reverse=True))
    return pair in DECOMPOSITIONS[original]


def describe_decomposition(original: str) -> str:
    """Return a human-readable description of all valid decompositions.

    Args:
        original: The ASIL level to describe.

    Returns:
        Multi-line string summarising valid decompositions.
    """
    original = _validate(original)
    decompositions = DECOMPOSITIONS[original]
    if not decompositions:
        return f"ASIL {original}: No decomposition possible (already at lowest level)."

    lines = [f"ASIL {original} valid decompositions (ISO 26262-9):"]
    for idx, (a, b) in enumerate(decompositions, start=1):
        lines.append(f"  {idx}. ASIL {original} → ASIL {a}(a) + ASIL {b}(b)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _validate(asil: str) -> str:
    """Normalise and validate an ASIL level string."""
    asil = asil.strip().upper()
    if asil not in ASIL_VALUE:
        raise ValueError(
            f"Unknown ASIL level '{asil}'. Valid levels: {', '.join(ASIL_LEVELS)}"
        )
    return asil


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="ISO 26262 ASIL Decomposition Analyst",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # list command
    list_cmd = sub.add_parser(
        "list",
        help="List valid decompositions for an ASIL level.",
    )
    list_cmd.add_argument(
        "asil",
        metavar="ASIL",
        help="ASIL level to decompose (QM | A | B | C | D).",
    )

    # validate command
    val_cmd = sub.add_parser(
        "validate",
        help="Validate a proposed ASIL decomposition.",
    )
    val_cmd.add_argument("original", metavar="ORIGINAL", help="Original ASIL level.")
    val_cmd.add_argument("part_a", metavar="PART_A", help="ASIL level of part A.")
    val_cmd.add_argument("part_b", metavar="PART_B", help="ASIL level of part B.")

    args = parser.parse_args()

    if args.command == "list":
        print(describe_decomposition(args.asil))
    elif args.command == "validate":
        valid = is_valid_decomposition(args.original, args.part_a, args.part_b)
        if valid:
            print(
                f"✔ ASIL {args.original.upper()} → "
                f"ASIL {args.part_a.upper()}(a) + ASIL {args.part_b.upper()}(b) "
                "is a VALID decomposition per ISO 26262."
            )
        else:
            print(
                f"✘ ASIL {args.original.upper()} → "
                f"ASIL {args.part_a.upper()}(a) + ASIL {args.part_b.upper()}(b) "
                "is NOT a valid decomposition per ISO 26262."
            )


if __name__ == "__main__":
    main()
