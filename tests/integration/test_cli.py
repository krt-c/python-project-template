"""Integration tests for the installed command-line entry point."""

import subprocess
import sys

import pytest


@pytest.mark.integration
def test_module_entry_point_prints_greeting() -> None:
    """Run the installed module entry point and check its visible output."""
    result = subprocess.run(
        [sys.executable, "-m", "starter_app", "--name", "Template"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Template!"
