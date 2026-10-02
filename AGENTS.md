# Development guidance

Use the existing checkout; cloud tasks already run in an isolated environment. Do not create a worktree unless requested.

Keep changes focused on the requested task. Prefer the Python standard library and add dependencies only when needed. Source modules belong in `src/codex_project/`; tests belong in `tests/test_*.py`.

From the repository root, run these checks before finishing:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
git diff --check
```

Keep README.md current when development commands or project structure change. Never commit credentials, local environment files, or generated outputs. Inspect existing changes before editing and preserve unrelated work.
