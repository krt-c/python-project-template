"""Pure greeting rule used by the starter example."""


def format_greeting(name: str) -> str:
    """Return a greeting for the supplied name, using a fallback for blank input."""
    normalized_name = name.strip() or "World"
    return f"Hello, {normalized_name}!"
