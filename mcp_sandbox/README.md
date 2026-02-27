# MCP Sandbox

Standalone MCP demo project (Python >= 3.13) using `mcp.server.fastmcp.FastMCP`.

## What’s here

Three types of FastMCP servers:

- **Type 1 (Stdio)**: `hello_world_new.py` — Server "Hello World" with tool `return_username()`. Uses `mcp.run(transport='stdio')` for MCP client integration (e.g., VS Code).
- **Type 2 (Default)**: `test_counter.py` — Server "Test Counter" with tool `count_to_five()`. Uses `mcp.run()` with default transport for standalone use.
- **Type 3 (HTTP URLs)**: Remote MCP servers accessible via HTTP endpoints. Configured in the MCP client with full URL and optional authentication headers.
- `main.py`: normal Python entry point (not an MCP server).

## Run

Install deps (choose one):

- `uv sync` (recommended; creates `.venv/`)
- `python -m pip install mcp>=1.26.0`

Run a server:

- `uv run python hello_world_new.py` (stdio; for VS Code MCP client)
- `uv run python test_counter.py` (default transport; for standalone testing)
