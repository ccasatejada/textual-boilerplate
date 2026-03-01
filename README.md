![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet?logo=astral&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![mypy](https://img.shields.io/badge/type%20checker-mypy%20strict-blue?logo=python&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![CI](https://github.com/ccasatejada/uvbp/actions/workflows/ci.yml/badge.svg)      


## boilerplate
- python3.14
- textual (tui)
- sqlalchemy / alembic
- uv
- mypy
- ruff
- pre-commit (run ruff and mypy)
- minimal github action for linting / test

### reminders
```
after cloning, run:
$ uv sync
$ uv run pre-commit install
```

### Install & run

```bash
uv sync
uv run alembic upgrade head
uv run python main.py
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
textual run main.py --dev
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