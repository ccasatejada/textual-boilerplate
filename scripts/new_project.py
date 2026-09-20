#!/usr/bin/env python3
"""Bootstrap a new project from this boilerplate.

Standalone, stdlib-only script: run it directly, no `uv sync` required.

    python3 scripts/new_project.py

It copies this repository into a new directory, renames the distribution
and the importable package to the name you choose, strips out the
bootstrap-only bits (this script, the "using this boilerplate" README
section), and optionally runs `git init` for you.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OLD_DIST_NAME = "textual-boilerplate"
OLD_PKG_NAME = "textual_boilerplate"

EXCLUDED_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "htmlcov",
    "dist",
    "build",
    ".idea",
    "uv.lock",
    ".env",
    ".coverage",
    "coverage.json",
    "coverage.xml",
    "report.xml",
    "pytest-output.txt",
}
README_TEMPLATE_MARKER = "## Using this boilerplate for a new project"


def slugify(raw: str) -> str:
    slug = raw.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def prompt(question: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{question}{suffix} : ").strip()
    return answer or (default or "")


def prompt_yes_no(question: str, default_yes: bool = True) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    answer = input(f"{question} {suffix} : ").strip().lower()
    if not answer:
        return default_yes
    return answer in {"y", "yes"}


def is_valid_dist_name(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)*", name))


def is_valid_package_name(name: str) -> bool:
    return name.isidentifier() and not name[0].isdigit()


def ignore_excluded(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED_NAMES}


def replace_in_file(path: Path, dist_name: str, pkg_name: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, ValueError):
        return
    updated = text.replace(OLD_DIST_NAME, dist_name).replace(OLD_PKG_NAME, pkg_name)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def strip_readme_template_section(readme_path: Path) -> None:
    if not readme_path.exists():
        return
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    try:
        marker_index = next(
            i for i, line in enumerate(lines) if line.startswith(README_TEMPLATE_MARKER)
        )
    except StopIteration:
        return
    end = marker_index
    if end > 0 and lines[end - 1].strip() == "---":
        end -= 1
    while end > 0 and lines[end - 1].strip() == "":
        end -= 1
    readme_path.write_text("\n".join(lines[:end]).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    print("=== Create a new project from this boilerplate ===\n")

    raw_name = prompt("New project name (e.g. My Cool App)")
    if not raw_name:
        print("A project name is required.", file=sys.stderr)
        return 1

    default_dist = slugify(raw_name)
    dist_name = prompt("Package/CLI name (kebab-case)", default_dist)
    if not is_valid_dist_name(dist_name):
        print(
            f"Invalid name: '{dist_name}' (expected kebab-case, e.g. my-cool-app)",
            file=sys.stderr,
        )
        return 1

    default_pkg = dist_name.replace("-", "_")
    pkg_name = prompt("Importable Python module name (snake_case)", default_pkg)
    if not is_valid_package_name(pkg_name):
        print(
            f"Invalid name: '{pkg_name}' (expected a valid Python identifier)",
            file=sys.stderr,
        )
        return 1

    default_dest = REPO_ROOT.parent / dist_name
    dest_input = prompt("Destination directory", str(default_dest))
    destination = Path(dest_input).expanduser().resolve()
    if destination.exists() and any(destination.iterdir()):
        print(
            f"Directory '{destination}' already exists and is not empty.",
            file=sys.stderr,
        )
        return 1

    print(f"""
Summary:
  Project name     : {raw_name}
  Distribution/CLI : {dist_name}
  Python package   : {pkg_name}
  Destination      : {destination}
""")
    if not prompt_yes_no("Continue?"):
        print("Cancelled.")
        return 0

    shutil.copytree(REPO_ROOT, destination, ignore=ignore_excluded)

    for path in destination.rglob("*"):
        if path.is_file():
            replace_in_file(path, dist_name, pkg_name)

    old_pkg_dir = destination / "src" / OLD_PKG_NAME
    if old_pkg_dir.exists():
        old_pkg_dir.rename(destination / "src" / pkg_name)

    strip_readme_template_section(destination / "README.md")

    this_script_in_dest = destination / "scripts" / "new_project.py"
    if this_script_in_dest.exists():
        this_script_in_dest.unlink()
        scripts_dir = this_script_in_dest.parent
        if scripts_dir.exists() and not any(scripts_dir.iterdir()):
            scripts_dir.rmdir()

    print(f"\n✅ New project created at: {destination}\n")

    git_initialized = False
    remote_added = False
    if prompt_yes_no("Initialize a git repository (git init + initial commit) now?"):
        subprocess.run(["git", "init", "-b", "main"], cwd=destination, check=True)
        subprocess.run(["git", "add", "-A"], cwd=destination, check=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"chore: bootstrap {dist_name} from textual-boilerplate",
            ],
            cwd=destination,
            check=True,
        )
        git_initialized = True

        remote_url = prompt("Git remote URL (leave empty to add it later)", "")
        if remote_url:
            subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                cwd=destination,
                check=True,
            )
            remote_added = True

    print("Next steps:")
    print(f"  cd {destination}")
    if not git_initialized:
        print("  git init -b main")
        print("  git add -A")
        print(f'  git commit -m "chore: bootstrap {dist_name}"')
    if not remote_added:
        print("  git remote add origin <your-repo-url>")
    print("  git push -u origin main")
    print("  uv sync")
    print("  uv run pre-commit install")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
