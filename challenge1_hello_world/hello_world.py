"""Challenge 1: Setup & Hello World

A simple Hello World script demonstrating the environment is set up correctly.
"""


def greet(name: str = "World") -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"


def main() -> None:
    print(greet())
    print(greet("Automotive Developer"))
    print("Environment setup complete. Ready for Challenges 2-4!")


if __name__ == "__main__":
    main()
