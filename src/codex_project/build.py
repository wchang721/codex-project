"""Build and validate the six Phase 1 pages without third-party dependencies."""

import argparse
import json
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from string import Template
from urllib.parse import urlencode, urlsplit


ROOT = Path(__file__).resolve().parents[2]
PAGE_SLUGS = ("home", "about", "beliefs", "meetings", "visit-us", "contact")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def page_url(slug):
    return "/" if slug == "home" else f"/{slug}/"


def production_origin(value):
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or parsed.path not in ("", "/")
            or parsed.query or parsed.fragment):
        raise ValueError("Production origin must be an HTTPS origin without a path or credentials.")
    return value.rstrip("/")


def actions(items):
    if not items:
        return ""
    links = []
    for item in items:
        href = item["href"]
        if not href.startswith("/") or href.startswith("//"):
            raise ValueError("Content actions must link within the site.")
        links.append(f'<a class="button" href="{escape(href)}">{escape(item["label"])}</a>')
    return '<div class="actions">' + "".join(links) + "</div>"


def display_time(value):
    from datetime import time

    parsed = time.fromisoformat(value)
    return f"{parsed.hour % 12 or 12}:{parsed.minute:02d} {'AM' if parsed.hour < 12 else 'PM'}"


def meeting_content(site):
    rows = []
    for meeting in site["sunday_meetings"]:
        start, end = meeting["start"], meeting["end"]
        if start >= end:
            raise ValueError("Meeting end must follow its start.")
        rows.append(
            f'<li><h3>{escape(meeting["name"])}</h3><p>Sunday · '
            f'<time datetime="{escape(start)}">{display_time(start)}</time>–'
            f'<time datetime="{escape(end)}">{display_time(end)}</time></p>'
            f'<p>{escape(meeting["location"])}</p></li>'
        )
    return ('<ul class="meeting-list">' + "".join(rows) + '</ul>'
            '<p>Please call <a href="' + escape(site["phone_href"]) + '">'
            + escape(site["phone"]) + '</a> to confirm meeting details before visiting.</p>')


def contact_content(site):
    address = site["address"]
    destination = address["street"] + ", " + address["locality"]
    directions = "https://www.google.com/maps/dir/?" + urlencode({"api": "1", "destination": destination})
    return (f'<address>{escape(site["name"])}<br>{escape(address["street"])}<br>'
            f'{escape(address["locality"])}<br><a href="{escape(site["phone_href"])}">'
            f'{escape(site["phone"])}</a></address>'
            f'<p><a href="{escape(directions)}">Get Directions with Google Maps</a></p>')


def render_section(section, site, index):
    kind = section["kind"]
    if kind == "text":
        body = "".join(f"<p>{escape(p)}</p>" for p in section["paragraphs"])
        body += actions(section.get("actions", []))
    elif kind == "meetings":
        body = meeting_content(site)
    elif kind == "contact":
        body = contact_content(site)
    elif kind == "beliefs":
        body = '<ol class="faith-list">' + "".join(
            f"<li>{escape(statement)}</li>" for statement in section["statements"]
        ) + "</ol>"
    else:
        raise ValueError(f"Unsupported section kind: {kind}")
    section_id = section.get("id", f"section-{index}")
    return (f'<section id="{escape(section_id)}" aria-labelledby="heading-{index}">'
            f'<h2 id="heading-{index}">{escape(section["heading"])}</h2>{body}</section>')


class PageInspection(HTMLParser):
    """Collect the document facts needed for build validation."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.text = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_title:
            self.title += data


def validate_documents(documents, origin):
    inspections = {}
    titles = set()
    for url, document in documents.items():
        parser = PageInspection()
        parser.feed(document)
        inspections[url] = parser
        if not parser.title.strip() or parser.title in titles:
            raise ValueError("Every page must have a unique, nonempty title.")
        titles.add(parser.title)
        elements = parser.elements
        for landmark in ("header", "nav", "main", "footer"):
            if not any(tag == landmark for tag, _ in elements):
                raise ValueError(f"Missing {landmark} landmark on {url}")
        if sum(tag == "h1" for tag, _ in elements) != 1:
            raise ValueError(f"Expected one h1 on {url}")
        if not any(tag == "meta" and attrs.get("name") == "description"
                   and attrs.get("content", "").strip() for tag, attrs in elements):
            raise ValueError(f"Missing description on {url}")
        canonicals = [attrs.get("href") for tag, attrs in elements
                      if tag == "link" and attrs.get("rel") == "canonical"]
        if canonicals != [origin + url]:
            raise ValueError(f"Incorrect canonical on {url}")
        if "[Content needed]" in document or "zoom.us" in document:
            raise ValueError("Private review content must not be published.")
    for url, parser in inspections.items():
        for tag, attrs in parser.elements:
            if tag not in ("a", "link") or "href" not in attrs:
                continue
            target = urlsplit(attrs["href"])
            if target.scheme or target.netloc:
                continue
            path = target.path or url
            if path == "/assets/styles.css" and not target.fragment:
                continue
            if path not in inspections:
                raise ValueError(f"Unresolved internal link: {attrs['href']} on {url}")
            ids = {a["id"] for _, a in inspections[path].elements if "id" in a}
            if target.fragment and target.fragment not in ids:
                raise ValueError(f"Unresolved fragment: {attrs['href']} on {url}")


def build(root=ROOT, output=None, origin=None):
    root = Path(root)
    output = Path(output) if output is not None else root / "dist"
    site = read_json(root / "content/site.json")
    origin = production_origin(origin or site["production_origin"])
    pages = [read_json(root / f"content/pages/{slug}.json") for slug in PAGE_SLUGS]
    if [p["slug"] for p in pages] != list(PAGE_SLUGS):
        raise ValueError("Page slugs must match their content filenames.")
    events = read_json(root / "content/events.json")
    if not isinstance(events["events"], list):
        raise ValueError("Events must be a list; they are not rendered in Phase 1.")
    beliefs = next(p for p in pages if p["slug"] == "beliefs")
    original = (root / "docs/statement-of-faith-source.md").read_text(encoding="utf-8")
    original = original.split("## Statement of Faith\n\n", 1)[1].strip()
    statements = beliefs["sections"][0]["statements"]
    transcription = beliefs["intro"] + "\n\n" + "\n\n".join(
        f"{i}. {statement}" for i, statement in enumerate(statements, 1)
    )
    if transcription != original:
        raise ValueError("Statement of Faith must match the original source exactly.")
    base = Template((root / "web/templates/base.html").read_text(encoding="utf-8"))
    page_template = Template((root / "web/templates/page.html").read_text(encoding="utf-8"))
    documents = {}
    for page in pages:
        navigation = "".join(
            f'<li><a href="{page_url(p["slug"])}"'
            + (' aria-current="page"' if p["slug"] == page["slug"] else "")
            + f'>{escape(p["label"])}</a></li>' for p in pages
        )
        body = page_template.substitute(
            heading=escape(page["heading"]), intro=escape(page["intro"]),
            actions=actions(page.get("actions", [])),
            sections="\n".join(render_section(s, site, i) for i, s in enumerate(page["sections"])),
        )
        url = page_url(page["slug"])
        documents[url] = base.substitute(
            title=escape(page["title"]), description=escape(page["description"]),
            canonical=escape(origin + url), name=escape(site["name"]),
            navigation=navigation, body=body, street=escape(site["address"]["street"]),
            locality=escape(site["address"]["locality"]),
            phone_href=escape(site["phone_href"]), phone=escape(site["phone"]),
        )
    validate_documents(documents, origin)
    if output.exists() and any(output.iterdir()) and not (output / ".site-build").is_file():
        raise ValueError("Refusing to overwrite a nonempty directory not owned by this build.")
    output.mkdir(parents=True, exist_ok=True)
    for url, document in documents.items():
        path = output / url.lstrip("/") / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(document, encoding="utf-8")
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "styles.css").write_bytes((root / "web/assets/styles.css").read_bytes())
    (output / ".site-build").write_text("Phase 1 static output\n", encoding="utf-8")
    return documents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", help="Override the configured HTTPS production origin.")
    args = parser.parse_args()
    documents = build(origin=args.origin)
    print(f"Built and validated {len(documents)} pages in {ROOT / 'dist'}")


if __name__ == "__main__":
    main()
