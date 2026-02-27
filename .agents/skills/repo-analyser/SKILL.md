---
name: repo-analyser
description: Analyse the repo for any potential errors in the source code available, and generate a report of findings
---

Analysing the repo for any potential errors in the source code available. The repo contains multiple challenges and a sandbox for MCP demo. Each challenge has its own directory and is designed to be independent, with local changes preferred over cross-challenge shared packages. The challenges target Python >= 3.9, while the MCP sandbox requires Python >= 3.13. The code follows conventions such as clear separation between core API functions and CLI, use of type hints and docstrings, and stable output strings for tests. Specific patterns are used in each challenge, such as table-driven logic in the ASIL analyst and XML parsing in the ARXML watchdog. The MCP demo includes different types of FastMCP servers for integration with clients. Unit tests are written with pytest, and any changes to behavior should be reflected in the corresponding README and tests.
