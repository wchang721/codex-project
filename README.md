# codex-project

A minimal starting point for a Python project, organized for incremental development and future Codex tasks.

## Current status

The repository contains a source package and an automated package import test. Application features, a framework, and third-party dependencies have not been added yet.

The planned Church Assembly in Westminster website rebuild is documented in [the website audit and foundation plan](docs/website-plan.md). Public-site inspection is currently blocked by the environment's network policy; website implementation and deployment instructions are pending that inspection.

## Local development

Use Python 3.12 or newer. No dependency installation or external services are required. Run commands from the repository root.

Run all tests:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Check that source and test files compile:

```sh
python3 -m compileall -q src tests
```

Add application modules under `src/codex_project/` and corresponding `test_*.py` files under `tests/`. Update these instructions when setup or runtime requirements change. There is no application startup command yet.

## Project structure

```text
src/
  codex_project/
    __init__.py       Python package entry point
tests/
  test_package.py    Package import smoke test
.gitignore          Local and generated files excluded from Git
AGENTS.md           Guidance for future Codex tasks
README.md           Project status and development instructions
```

Keep credentials and machine-specific configuration out of version control. Add dependencies only when a concrete requirement needs them.
