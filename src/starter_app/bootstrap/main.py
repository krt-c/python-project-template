"""Wire the starter use case to its command-line presentation adapter."""

from collections.abc import Sequence

from starter_app.application.greet import greet
from starter_app.presentation.cli import run_cli


def main(argv: Sequence[str] | None = None) -> int:
    """Start the CLI with the application use case wired into its presentation adapter."""
    return run_cli(argv, greet)
