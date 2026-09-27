"""Command-line presentation for the starter application."""

import argparse
from collections.abc import Sequence

from starter_app.greeting import format_greeting


def main(argv: Sequence[str] | None = None) -> int:
    """Parse command-line input, print a greeting, and return a process status."""
    parser = argparse.ArgumentParser(description="Run the generic Python starter app.")
    parser.add_argument("--name", default="World", help="name to greet")
    arguments = parser.parse_args(argv)
    print(format_greeting(arguments.name))
    return 0
