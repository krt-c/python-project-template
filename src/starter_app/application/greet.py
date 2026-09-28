"""Application use case for creating a greeting."""

from starter_app.domain.greeting import format_greeting


def greet(name: str) -> str:
    """Return the greeting produced by the domain rule for the supplied name."""
    return format_greeting(name)
