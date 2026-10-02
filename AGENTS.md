# Development guidance

Use the existing checkout; cloud tasks already run in an isolated environment. Do not create a worktree unless requested.

Keep changes focused on the requested task. Prefer the Python standard library and add dependencies only when needed. Source modules belong in `src/codex_project/`; tests belong in `tests/test_*.py`.

From the repository root, run these checks before finishing:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m codex_project.build
python3 -m compileall -q src tests
git diff --check
```

Keep README.md current when development commands or project structure change. Never commit credentials, local environment files, or generated outputs. Inspect existing changes before editing and preserve unrelated work.

The website is static and limited to six Phase 1 pages. Content belongs in `content/`, templates in `web/templates/`, and styles in the single `web/assets/styles.css` file. Do not migrate later-phase archives unless requested. Do not commit `dist/`.

Use the verified audit and source inventory in `docs/` for church facts. Preserve the original Statement of Faith wording; never edit its source reference to make a failed test pass. Keep unresolved information and conflicting schedules in source review notes, never invent replacements or render `[Content needed]` publicly. Do not commit Zoom access URLs. The production origin is configurable; no deploy, DNS change, or new service is implied by a development task.
