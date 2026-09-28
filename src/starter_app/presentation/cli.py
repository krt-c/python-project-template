"""Command-line presentation for the starter example."""

import argparse
from collections.abc import Callable, Sequence


def run_cli(argv: Sequence[str] | None, greet: Callable[[str], str]) -> int:
    """Parse command-line input, call the greeting use case, and print its result."""
    parser = argparse.ArgumentParser(description="Run the starter app.")
    parser.add_argument("--name", default="World", help="name to greet")
    arguments = parser.parse_args(argv)
    print(greet(arguments.name))
    return 0
