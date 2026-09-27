"""Unit tests for the example greeting behavior."""

from starter_app.greeting import format_greeting


def test_format_greeting_uses_the_name() -> None:
    """Format a greeting with a non-empty name."""
    assert format_greeting("Ada") == "Hello, Ada!"


def test_format_greeting_uses_fallback_for_blank_name() -> None:
    """Use the default name when the supplied value contains only whitespace."""
    assert format_greeting("  ") == "Hello, World!"
