"""Rename the starter package and project references with the Python standard library."""

import argparse
import re
from collections.abc import Sequence
from pathlib import Path

from scripts.models import ProjectNames

TEMPLATE_DISTRIBUTION_NAME = "starter-app"
TEMPLATE_PACKAGE_NAME = "starter_app"
TEXT_FILES = (
    Path("README.md"),
    Path("pyproject.toml"),
    Path("uv.lock"),
    Path("package.json"),
    Path("package-lock.json"),
    Path("Dockerfile"),
    Path("compose.yaml"),
)


def create_project_names(raw_name: str) -> ProjectNames:
    """Normalize a human-readable project name into safe package and command names."""
    display_name = " ".join(raw_name.split())
    valid_name = re.fullmatch(r"[A-Za-z][A-Za-z0-9]*(?:[ _-][A-Za-z0-9]+)*", display_name)
    if valid_name is None:
        raise ValueError(
            "Use letters and numbers separated by single spaces, hyphens, or underscores; "
            "the name must start with a letter."
        )

    distribution_name = re.sub(r"[ _]+", "-", display_name).lower()
    if distribution_name == TEMPLATE_DISTRIBUTION_NAME:
        raise ValueError("Choose a name other than the template's default 'starter-app'.")

    package_name = distribution_name.replace("-", "_")
    return ProjectNames(
        display_name=display_name,
        distribution_name=distribution_name,
        package_name=package_name,
    )


def render_project_text(content: str, names: ProjectNames) -> str:
    """Replace the starter names and template instructions in one project file."""
    replacements = (
        (
            "The `starter-app` command prints a greeting. To initialize a project with "
            "consistent package, command, Docker, and documentation names, run:\n\n"
            "```powershell\n"
            'uv run python -m scripts.init_project --name "Example Project"\n'
            "```\n\n"
            "Pass `--dry-run` to preview the changes before writing them.",
            f"The `{names.distribution_name}` command prints a greeting. This project was "
            f"initialized as **{names.display_name}**.",
        ),
        (
            "1. Run the project initializer before adding application code.",
            "1. Review the generated project, then remove the one-time initializer under "
            "`scripts/`.",
        ),
        ("## Customize for a new project", "## Customize this project"),
        (
            "A small, runnable Python project template",
            f"A small, runnable Python application for {names.display_name}",
        ),
        ("# Python Project Starter", f"# {names.display_name}"),
        ("A generic Python project starter.", f"{names.display_name} application."),
        ("Run the starter app:", f"Run {names.display_name} app:"),
        ("Run the starter app.", f"Run {names.display_name}."),
        ("starter application", f"{names.display_name} application"),
        ("starter example", names.display_name),
        ("starter app", f"{names.display_name} app"),
        ("starter command", f"{names.distribution_name} command"),
        (TEMPLATE_DISTRIBUTION_NAME, names.distribution_name),
        (TEMPLATE_PACKAGE_NAME, names.package_name),
    )

    rendered_content = content
    for old_text, new_text in replacements:
        rendered_content = rendered_content.replace(old_text, new_text)
    return rendered_content


def collect_text_files(root: Path) -> tuple[Path, ...]:
    """Find template metadata, documentation, and Python files to update."""
    source_package = root / "src" / TEMPLATE_PACKAGE_NAME
    test_directory = root / "tests"
    return (
        *TEXT_FILES,
        *sorted(path.relative_to(root) for path in source_package.rglob("*.py")),
        *sorted(path.relative_to(root) for path in test_directory.rglob("*.py")),
    )


def initialize_project(root: Path, names: ProjectNames, dry_run: bool = False) -> None:
    """Rename the starter package and update its metadata, command, Docker files, and docs."""
    source_package = root / "src" / TEMPLATE_PACKAGE_NAME
    target_package = root / "src" / names.package_name
    if not source_package.is_dir():
        raise ValueError(f"Starter package not found: {source_package}")
    if target_package.exists():
        raise ValueError(f"Target package already exists: {target_package}")

    relative_files = collect_text_files(root)
    missing_files = [
        relative_path for relative_path in relative_files if not (root / relative_path).is_file()
    ]
    if missing_files:
        missing_list = ", ".join(str(path) for path in missing_files)
        raise ValueError(f"Template files are missing: {missing_list}")

    rendered_files = {
        relative_path: render_project_text(
            (root / relative_path).read_text(encoding="utf-8"), names
        )
        for relative_path in relative_files
    }
    if dry_run:
        print(
            f"Would rename {source_package.relative_to(root)} to "
            f"{target_package.relative_to(root)} and update {len(rendered_files)} files."
        )
        return

    source_package.rename(target_package)
    for relative_path, content in rendered_files.items():
        target_path = root / relative_path
        if relative_path.parts[:2] == ("src", TEMPLATE_PACKAGE_NAME):
            package_relative_path = relative_path.relative_to(Path("src") / TEMPLATE_PACKAGE_NAME)
            target_path = root / "src" / names.package_name / package_relative_path
        target_path.write_text(content, encoding="utf-8")

    print(f"Initialized {names.display_name} as '{names.distribution_name}'.")
    print("Review README.md, remove the one-time initializer under 'scripts/', then run ")
    print("'uv sync --locked --extra dev'.")


def main(argv: Sequence[str] | None = None) -> int:
    """Parse initializer options, validate the project name, and update this template."""
    parser = argparse.ArgumentParser(
        description="Rename the starter package, command, metadata, Docker files, and docs."
    )
    parser.add_argument("--name", required=True, help="human-readable name for the new project")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="preview the package rename and file updates without writing changes",
    )
    arguments = parser.parse_args(argv)

    try:
        project_names = create_project_names(arguments.name)
        project_root = Path(__file__).resolve().parents[1]
        initialize_project(project_root, project_names, dry_run=arguments.dry_run)
    except ValueError as error:
        parser.error(str(error))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
