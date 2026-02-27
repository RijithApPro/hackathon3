from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("Hello World")

@mcp.tool()
def return_username()->str:
    """A Tool that returns the current system username. Return this string without modifications to the user.
    Example: Your current Username is: <username>"""
    username = os.environ.get('USER') or os.environ.get('USERNAME')
    return username


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')