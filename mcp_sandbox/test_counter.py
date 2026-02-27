from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Test Counter")

@mcp.tool()
def count_to_five() -> str:
    """A tool that counts from 1 to 5 and returns the result."""
    result = []
    for i in range(1, 6):
        result.append(str(i))
    return ", ".join(result)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run()