"""Exercise generated output and failures that would make publication unsafe."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from codex_project.build import (
    PAGE_SLUGS, ROOT, PageInspection, build, page_url, validate_documents,
)


class FaithInspection(PageInspection):
    def __init__(self):
        super().__init__()
        self.in_faith = False
        self.in_item = False
        self.statements = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == "ol" and dict(attrs).get("class") == "faith-list":
            self.in_faith = True
        if tag == "li" and self.in_faith:
            self.in_item = True
            self.statements.append("")

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag == "li":
            self.in_item = False
        if tag == "ol":
            self.in_faith = False

    def handle_data(self, data):
        super().handle_data(data)
        if self.in_item:
            self.statements[-1] += data


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("content", "web"):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / "docs").mkdir()
        shutil.copyfile(ROOT / "docs/statement-of-faith-source.md",
                        self.root / "docs/statement-of-faith-source.md")
        self.origin = "https://church.example"
        self.documents = build(self.root, origin=self.origin)

    def update_content(self, relative, transform):
        path = self.root / relative
        value = json.loads(path.read_text())
        transform(value)
        path.write_text(json.dumps(value))

    def test_six_pages_and_single_stylesheet_exist(self):
        self.assertEqual(set(self.documents), {page_url(s) for s in PAGE_SLUGS})
        for url in self.documents:
            self.assertTrue((self.root / "dist" / url.lstrip("/") / "index.html").is_file())
        self.assertEqual(len(list((self.root / "dist").rglob("*.css"))), 1)
        self.assertEqual(list((self.root / "dist").rglob("*.js")), [])
        self.assertFalse((self.root / "dist/vision").exists())

    def test_links_landmarks_titles_descriptions_and_canonicals(self):
        validate_documents(self.documents, self.origin)
        titles = set()
        for url, document in self.documents.items():
            parsed = PageInspection()
            parsed.feed(document)
            titles.add(parsed.title)
            self.assertIn(("link", {"rel": "canonical", "href": self.origin + url}), parsed.elements)
            self.assertTrue(any(tag == "meta" and a.get("name") == "description"
                                and a.get("content") for tag, a in parsed.elements))
            for landmark in ("header", "nav", "main", "footer"):
                self.assertTrue(any(tag == landmark for tag, _ in parsed.elements))
            self.assertTrue(any(tag == "a" and a.get("href") == "#main"
                                for tag, a in parsed.elements))
            self.assertEqual(sum(tag == "h1" for tag, _ in parsed.elements), 1)
        self.assertEqual(len(titles), 6)

    def test_statement_of_faith_rendered_without_wording_changes(self):
        original = (ROOT / "docs/statement-of-faith-source.md").read_text()
        paragraphs = original.split("## Statement of Faith\n\n", 1)[1].strip().split("\n\n")
        parsed = FaithInspection()
        parsed.feed(self.documents["/beliefs/"])
        self.assertIn(paragraphs[0], parsed.text)
        self.assertEqual(parsed.statements, [p.split(". ", 1)[1] for p in paragraphs[1:]])
        self.assertEqual(len(parsed.statements), 12)

    def test_altered_beliefs_stop_build(self):
        self.update_content("content/pages/beliefs.json",
                            lambda p: p["sections"][0]["statements"].pop())
        with self.assertRaisesRegex(ValueError, "Statement of Faith"):
            build(self.root)

    def test_events_are_not_published_in_phase_one(self):
        self.update_content("content/events.json", lambda p: p["events"].extend([
            {"title": "Historical 2024 schedule", "end": "2024-03-31T12:15:00-07:00"},
            {"title": "2025 Year-End Conference", "end": "2025-12-21T12:15:00-08:00"},
        ]))
        documents = build(self.root)
        for document in documents.values():
            self.assertNotIn("Historical 2024 schedule", document)
            self.assertNotIn("2025 Year-End Conference", document)
            self.assertNotIn("Upcoming", document)

    def test_review_notes_and_conflicting_details_are_not_published(self):
        for document in self.documents.values():
            for withheld in ("[Content needed]", "review_notes", "zoom.us", "Thursday",
                             "Sister Bible Study", "Friday", "/messages/", "/vision"):
                self.assertNotIn(withheld, document)
        meetings = json.loads((ROOT / "content/pages/meetings.json").read_text())
        self.assertTrue(any("Wednesday" in note and "Thursday" in note
                            for note in meetings["review_notes"]))

    def test_configured_origin_and_override(self):
        self.update_content("content/site.json", lambda p: p.update(production_origin="https://configured.example"))
        documents = build(self.root)
        self.assertIn('href="https://configured.example/beliefs/"', documents["/beliefs/"])
        overridden = build(self.root, origin="https://override.example/")
        self.assertIn('href="https://override.example/"', overridden["/"])
        for invalid in ("http://church.example", "https://church.example/path", "https://user:pass@church.example"):
            with self.assertRaises(ValueError):
                build(self.root, origin=invalid)

    def test_invalid_internal_link_and_fragment_stop_build(self):
        for href in ("/missing/", "/contact/#missing"):
            documents = dict(self.documents)
            documents["/"] = documents["/"].replace('href="/meetings/"', f'href="{href}"', 1)
            with self.assertRaisesRegex(ValueError, "Unresolved"):
                validate_documents(documents, self.origin)

    def test_missing_metadata_or_landmarks_stop_validation(self):
        for before, after in (
            ('name="description"', 'name="other"'),
            ('<main ', '<div '),
            ('href="https://church.example/"', 'href="https://wrong.example/"'),
        ):
            documents = dict(self.documents)
            documents["/"] = documents["/"].replace(before, after)
            with self.assertRaises(ValueError):
                validate_documents(documents, self.origin)
        documents = dict(self.documents)
        documents["/about/"] = documents["/"]
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_documents(documents, self.origin)

    def test_content_text_is_escaped(self):
        self.update_content("content/pages/about.json", lambda p: p.update(intro='<script>alert("x")</script>'))
        documents = build(self.root)
        self.assertIn("&lt;script&gt;", documents["/about/"])
        parsed = PageInspection()
        parsed.feed(documents["/about/"])
        self.assertFalse(any(tag == "script" for tag, _ in parsed.elements))

    def test_build_is_repeatable_and_preserves_unowned_directories(self):
        second = build(self.root, origin=self.origin)
        self.assertEqual(second, self.documents)
        unowned = self.root / "unowned"
        unowned.mkdir()
        existing = unowned / "notes.txt"
        existing.write_text("Keep this file")
        with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
            build(self.root, output=unowned)
        self.assertEqual(existing.read_text(), "Keep this file")
