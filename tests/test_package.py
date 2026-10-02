"""Smoke tests for the source package."""

import importlib
from pathlib import Path
import unittest


class PackageTests(unittest.TestCase):
    def test_source_package_imports(self):
        package = importlib.import_module("codex_project")
        expected = Path(__file__).resolve().parents[1] / "src" / "codex_project"
        self.assertEqual(Path(package.__file__).resolve().parent, expected)
