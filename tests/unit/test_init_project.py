"""Unit tests for the standard-library project initializer."""

import json
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from scripts.init_project import (
    TEXT_FILES,
    collect_text_files,
    create_project_names,
    initialize_project,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_FILES = (
    Path("scripts/__init__.py"),
    Path("scripts/models.py"),
    Path("scripts/init_project.py"),
)
AGENT_FILES = (
    Path("AGENTS.md"),
    Path(".agents/skills/python-clean-architecture/SKILL.md"),
    Path(".agents/skills/python-solid-principles/SKILL.md"),
)


def copy_template_files(destination: Path) -> Path:
    """Copy only initializer inputs into a temporary project directory."""
    for relative_path in (*collect_text_files(PROJECT_ROOT), *SCRIPT_FILES, *AGENT_FILES):
        destination_path = destination / relative_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT_ROOT / relative_path, destination_path)

    return destination


def test_create_project_names_normalizes_distribution_and_import_names() -> None:
    """Normalize a readable name to a hyphenated distribution and underscored package."""
    names = create_project_names("  Example   Project  2 ")

    assert names.display_name == "Example Project 2"
    assert names.distribution_name == "example-project-2"
    assert names.package_name == "example_project_2"


@pytest.mark.parametrize("invalid_name", ["", "123 project", "project/name", "two--hyphens"])
def test_create_project_names_rejects_invalid_names(invalid_name: str) -> None:
    """Reject names that cannot form a simple package and command name."""
    with pytest.raises(ValueError):
        create_project_names(invalid_name)


def test_initialize_project_updates_names_across_the_template(tmp_path: Path) -> None:
    """Rename the package and update imports, metadata, command, Docker files, and docs."""
    project_root = copy_template_files(tmp_path / "initialized")
    result = subprocess.run(
        [sys.executable, "-m", "scripts.init_project", "--name", "Quality Toolkit"],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert not (project_root / "src" / "starter_app").exists()
    assert (project_root / "src" / "quality_toolkit").is_dir()
    pyproject_data = tomllib.loads((project_root / "pyproject.toml").read_text())
    python_lock_data = tomllib.loads((project_root / "uv.lock").read_text())
    package_data = json.loads((project_root / "package.json").read_text())
    npm_lock_data = json.loads((project_root / "package-lock.json").read_text())
    readme = (project_root / "README.md").read_text()
    assert pyproject_data["project"]["name"] == "quality-toolkit"
    assert pyproject_data["project"]["scripts"]["quality-toolkit"] == (
        "quality_toolkit.bootstrap.main:main"
    )
    assert (
        next(
            package["name"]
            for package in python_lock_data["package"]
            if package.get("source") == {"editable": "."}
        )
        == "quality-toolkit"
    )
    assert 'CMD ["quality-toolkit"]' in (project_root / "Dockerfile").read_text()
    assert package_data["name"] == "quality-toolkit"
    assert "name: quality-toolkit" in (project_root / "compose.yaml").read_text()
    assert "# Quality Toolkit" in readme
    assert "scripts.init_project" not in readme
    assert npm_lock_data["name"] == "quality-toolkit"
    for relative_path in AGENT_FILES:
        assert (project_root / relative_path).is_file()
    for layer_name in ("domain", "application", "infrastructure", "presentation", "bootstrap"):
        assert (project_root / "src" / "quality_toolkit" / layer_name).is_dir()

    for rendered_path in (
        *TEXT_FILES,
        *sorted((project_root / "src" / "quality_toolkit").rglob("*.py")),
        *sorted((project_root / "tests").rglob("*.py")),
    ):
        rendered_content = (project_root / rendered_path).read_text(encoding="utf-8")
        assert "starter-app" not in rendered_content
        assert "starter_app" not in rendered_content

    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(project_root / "src")
    smoke_result = subprocess.run(
        [sys.executable, "-m", "quality_toolkit", "--name", "Template"],
        cwd=project_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    assert smoke_result.returncode == 0
    assert smoke_result.stdout.strip() == "Hello, Template!"


def test_initialize_project_dry_run_leaves_template_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Preview the rename without moving or rewriting any template files."""
    project_root = copy_template_files(tmp_path / "preview")
    original_readme = (project_root / "README.md").read_text()

    initialize_project(project_root, create_project_names("Preview Project"), dry_run=True)

    assert (project_root / "src" / "starter_app").is_dir()
    assert (project_root / "README.md").read_text() == original_readme
    assert "Would rename" in capsys.readouterr().out
