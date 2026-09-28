"""Immutable data models used by the project initializer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectNames:
    """Hold the display, distribution, and import names for a new project."""

    display_name: str
    distribution_name: str
    package_name: str
