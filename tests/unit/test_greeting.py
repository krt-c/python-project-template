"""Unit tests for the example greeting behavior."""

from starter_app.application.greet import greet


def test_format_greeting_uses_the_name() -> None:
    """Format a greeting with a non-empty name."""
    assert greet("Ada") == "Hello, Ada!"


def test_format_greeting_uses_fallback_for_blank_name() -> None:
    """Use the default name when the supplied value contains only whitespace."""
    assert greet("  ") == "Hello, World!"
