# Challenge 2 – ISO 26262 ASIL Decomposition Analyst

## Overview

ISO 26262 is the international standard for functional safety of road vehicles.
The **Automotive Safety Integrity Level (ASIL)** ranges from QM (no special
measures) through A, B, C up to D (highest integrity).

**ASIL Decomposition** (ISO 26262-9) allows a high-integrity safety goal to be
split into two **independent** sub-requirements with lower ASIL levels, as long
as their combined integrity satisfies the original requirement.

### Valid decompositions

| Original | Part A   | Part B   |
|----------|----------|----------|
| ASIL D   | ASIL D   | ASIL QM  |
| ASIL D   | ASIL C   | ASIL A   |
| ASIL D   | ASIL B   | ASIL B   |
| ASIL C   | ASIL C   | ASIL QM  |
| ASIL C   | ASIL B   | ASIL A   |
| ASIL B   | ASIL B   | ASIL QM  |
| ASIL B   | ASIL A   | ASIL A   |
| ASIL A   | ASIL A   | ASIL QM  |

## Usage

### List valid decompositions

```bash
python asil_analyst.py list D
```

Output:
```
ASIL D valid decompositions (ISO 26262-9):
  1. ASIL D → ASIL D(a) + ASIL QM(b)
  2. ASIL D → ASIL C(a) + ASIL A(b)
  3. ASIL D → ASIL B(a) + ASIL B(b)
```

### Validate a proposed decomposition

```bash
python asil_analyst.py validate D B B
```

Output:
```
✔ ASIL D → ASIL B(a) + ASIL B(b) is a VALID decomposition per ISO 26262.
```

```bash
python asil_analyst.py validate D A A
```

Output:
```
✘ ASIL D → ASIL A(a) + ASIL A(b) is NOT a valid decomposition per ISO 26262.
```

## Test

```bash
pytest test_asil_analyst.py
```
