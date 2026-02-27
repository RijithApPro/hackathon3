# Copilot instructions (hackathon3)

## Repo shape / intent
- This repo is a set of **independent, single-file Python challenge exercises** under `challenge*/` plus a small MCP demo in `mcp_sandbox/`.
- Prefer **local, per-challenge changes** (don’t introduce cross-challenge shared packages unless a challenge explicitly needs it).

## How to run (most common workflows)
- Challenges 1–4: **run from each challenge directory** (these are not packaged modules; tests/imports assume the cwd is the challenge folder).
  - Challenge 1: `cd challenge1_hello_world && python hello_world.py` ; tests: `pytest -q`
  - Challenge 2: `cd challenge2_asil_analyst && python asil_analyst.py list D` ; tests: `pytest -q`
  - Challenge 3: `cd challenge3_arxml_watchdog && python arxml_utils.py` ; tests: `pytest -q`
  - Challenge 4: `cd challenge4_ecu_pipeline && python ecu_pipeline.py check` ; tests: `pytest -q`
- Challenge 4 local pipeline:
  - `cd challenge4_ecu_pipeline && python ecu_pipeline.py check`
  - `make all` (lint → test → build) and `make release ECU_ID=BCM` (see `Makefile`).
  - On Windows, `make` may not exist; use the Python CLI equivalents in `ecu_pipeline.py`.
- Python versions:
  - Challenges 1–4 target **Python >= 3.9** (Challenge 4 CI uses Python 3.11).
  - `mcp_sandbox/` is a separate Python project (see `pyproject.toml`) and requires **Python >= 3.13**.

## Conventions you should follow when editing/adding code
- Keep a clear split between:
  - **Core API functions** (pure-ish, unit-testable), and
  - a small `main()` CLI using `argparse` (see `challenge2_asil_analyst/asil_analyst.py` and `challenge4_ecu_pipeline/ecu_pipeline.py`).
- Use **type hints** and **module/function docstrings** (the existing code is typed and documented).
- Keep output strings stable when there are README “Expected output” blocks or tests asserting substrings (e.g., `challenge1_hello_world/test_hello_world.py` uses `capsys`).

## Challenge-specific patterns (examples to copy)
- ASIL analyst (`challenge2_asil_analyst/`):
  - Table-driven logic via `DECOMPOSITIONS` and normalization in `_validate()`.
  - Symmetric decomposition checks by sorting parts before comparison.
- ARXML watchdog (`challenge3_arxml_watchdog/`):
  - Uses stdlib `xml.etree.ElementTree` only; namespace is the AUTOSAR R4 URI.
  - Extract data by iterating tags and reading `SHORT-NAME` text.
- ECU pipeline (`challenge4_ecu_pipeline/`):
  - Treat `VERSION` as the source of truth; validate with regex `vMAJOR.MINOR.PATCH`.
  - `check_release_readiness()` returns a list of human-readable issues (empty list means OK).
  - The GitHub Actions workflow lives under `challenge4_ecu_pipeline/.github/workflows/ecu_release.yml` and runs from that working directory.
- MCP demo (`mcp_sandbox/`):
  - FastMCP tools are defined via `@mcp.tool()` and the server runs via `mcp.run(transport='stdio')` (see `hello_world_new.py`).

## MCP demo briefing (mcp_sandbox/)
- This folder is a standalone MCP sandbox (separate `pyproject.toml`, Python >= 3.13) built on `mcp.server.fastmcp.FastMCP`.
- Treat `mcp_sandbox/.venv/` as a local dev artifact; if paths look stale after renames, recreate the venv.
- Three types of FastMCP servers are supported:
  - **Type 1 (Stdio transport)**: `hello_world_new.py` — server name "Hello World", exposes tool `return_username()` (reads `USER`/`USERNAME`) and runs with `mcp.run(transport='stdio')`. Use this for integration with MCP clients (e.g., VS Code) that communicate via stdin/stdout.
  - **Type 2 (Default transport)**: `test_counter.py` — server name "Test Counter", exposes tool `count_to_five()` and runs with `mcp.run()` (uses FastMCP defaults). Simpler for standalone testing.
  - **Type 3 (HTTP URLs)**: Remote MCP servers accessible via HTTP endpoints. Configure in MCP client with full URL and optional headers/authentication.
- `main.py` is just a normal Python entry point (prints a message); it is not an MCP server.

## Dependencies / installing
- Unit tests are written with `pytest` across challenges.
  - Challenge 1 pins it in `challenge1_hello_world/requirements.txt`; other challenge READMEs assume `pytest` is installed.
- Challenge 4 CI installs `pylint` for linting (local Makefile treats pylint failures as non-blocking).

## When you change behavior
- Update the matching README in that challenge directory if you alter CLI arguments or expected output.
- Prefer adding/adjusting the existing pytest unit tests in the same folder as the code.
