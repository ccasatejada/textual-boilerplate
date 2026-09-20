![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet?logo=astral&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![mypy](https://img.shields.io/badge/type%20checker-mypy%20strict-blue?logo=python&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)      


## boilerplate
- python3.14
- textual (tui)
- sqlalchemy / alembic
- uv
- mypy
- ruff
- pre-commit (run ruff and mypy)
- minimal github action for linting / test
- PyPA-compliant `src` layout, packaged with hatchling, installable as a `textual-boilerplate` CLI

### Project layout

```
.
├── alembic/                        # migrations (not part of the distributed package)
├── src/
│   └── textual_boilerplate/        # the installable package
│       ├── db/
│       ├── model/
│       └── main.py                 # Textual app + `run()` entry point
├── tests/                          # kept out of src/, per PyPA recommendations
└── pyproject.toml
```

### reminders
```
after cloning, run:
$ uv sync
$ uv run pre-commit install
```

### Install & run

During development, `uv sync` installs the project itself in editable mode alongside its
dependencies, so the `textual-boilerplate` command is available in the venv without `uv run`:

```bash
uv sync
uv run alembic upgrade head
textual-boilerplate
```

If the venv's `bin` directory isn't on your `PATH`, prefix with `uv run`:

```bash
uv run textual-boilerplate
```

To install the CLI outside of a project venv (e.g. as a standalone tool):

```bash
uv tool install .
textual-boilerplate
```

---

## Setup

### Database (PostgreSQL)

```sql
CREATE DATABASE example_db;
CREATE USER example_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE example_db TO example_user;
ALTER DATABASE example_db OWNER TO example_user;
```

Copy `.env.example` to `.env` and fill in your database credentials.

## Dev commands

### Run with Textual dev console (for debugging)

```bash
textual console [-v|-x]
textual run src/textual_boilerplate/main.py --dev
```

### Linting & type checking

```bash
uv run pre-commit run --all-files
uv run mypy .
```

### Tests with coverage

```bash
uv run pytest
```

---

## Using this boilerplate for a new project

This repo is meant to be cloned/forked as a starting point.

### Option 1: bootstrap script (recommended)

```bash
python3 scripts/new_project.py
```

It's a standalone, stdlib-only script (no `uv sync` needed to run it). It will:
- ask for your new project's name and derive a kebab-case distribution/CLI name
  and a snake_case Python package name (both editable)
- copy this repo into a new destination folder, excluding git/venv/cache artifacts
- rename `src/textual_boilerplate/` to `src/<your_package>/` and rewrite every
  occurrence of `textual-boilerplate` / `textual_boilerplate` accordingly
  (`pyproject.toml`, imports, README, …)
- remove this "using this boilerplate" section and the script itself from the
  generated project, since it no longer needs them
- optionally run `git init` + an initial commit, and print the exact
  `git remote add` / `git push` commands to finish publishing it

### Option 2: manual rename

To rename it by hand for your own project (replace `textual-boilerplate` /
`textual_boilerplate` with your project's name, e.g. `my-app` / `my_app`), adapt
the following:

- **`pyproject.toml`**
  - `[project].name` — the distribution name (`textual-boilerplate`)
  - `[project.scripts]` — the CLI command name and its target (`textual-boilerplate = "textual_boilerplate.main:run"`)
  - `[tool.hatch.build.targets.wheel].packages` — `["src/textual_boilerplate"]`
  - `[tool.pytest.ini_options].addopts` — `--cov=textual_boilerplate`
  - `[project].description` and `dependencies` — trim/extend to what your app actually needs
- **`src/textual_boilerplate/`** — rename the directory to your package name (`git mv src/textual_boilerplate src/<your_package>`)
- **Imports** referencing the package — update after the rename:
  - `tests/conftest.py` (`from textual_boilerplate.model.model import Base`)
  - `alembic/env.py` (`from textual_boilerplate.model.model import Base`)
- **`README.md`** — title/description, badges (`<owner>/<repo>` in the CI badge), CLI command name, project layout tree
- **`.idea/textual-boilerplate.iml`** and other IDE metadata, if versioned — safe to regenerate/rename
- **`alembic.ini`** — `script_location` and any project-specific settings if migrations are renamed/moved
- **`.env.example`** / `.env` — adjust `DATABASE_*` variables to your schema/service naming
- **`.github/workflows/ci.yml`** — no rename needed, but double-check `python-version` and job steps if your dependencies change

After renaming, run `uv sync`, `uv run pytest`, `uv run mypy .` and `uv run ruff check .` to confirm everything still resolves.