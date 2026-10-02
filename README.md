# codex-project

The Church Assembly in Westminster website rebuild: a small static site that preserves verified church information and the complete original Statement of Faith.

## Current status

Phase 1 provides Home, About, Beliefs, Meetings, Visit Us, and Contact. It uses semantic HTML, one responsive stylesheet, reusable templates, and a Python standard-library build tool. No dependencies, JavaScript, database, or production runtime server are required.

The [verified audit](docs/website-plan.md), [source inventory](docs/source-inventory.json), and [original Statement of Faith](docs/statement-of-faith-source.md) document the source material. Messages, Events archives, the resource library, Hebrews archive, and Gospel Blog remain outside this phase. The missing `/vision` page is not recreated.

## Local development

Use Python 3.12 or newer. No dependency installation is needed. Run commands from the repository root.

Build and validate all six pages into ignored `dist/`:

```sh
PYTHONPATH=src python3 -m codex_project.build
```

Preview the generated files locally (development only):

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open the local server in your browser and stop it with Ctrl+C. Rebuild after content, template, or stylesheet changes; there is no automatic watcher. The build refuses to overwrite a nonempty output directory without its generated `.site-build` marker.

Run all tests and checks:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
git diff --check
```

The build checks internal page/fragment links, unique titles, descriptions, canonical URLs, headings, semantic landmarks, and original faith wording. Tests additionally verify output files, escaping, repeatable builds, and exclusion of review notes, Zoom URLs, historical events, and later-phase destinations. These checks supplement manual keyboard, screen-reader, contrast, and mobile-browser testing.

## Project structure

```text
content/
  site.json                 Verified shared details and production origin
  pages/*.json              Six pages, source references, and review notes
  events.json               Empty event list; not rendered in Phase 1
web/
  templates/base.html       Shared document, navigation, and footer
  templates/page.html       Shared page layout
  assets/styles.css         Mobile-first styles
src/codex_project/build.py   Static generation and validation
tests/                      Build validation and package import tests
docs/                       Verified audit, inventory, and original beliefs
dist/                       Generated files; excluded from Git
AGENTS.md                   Guidance for future Codex tasks
```

## Editing content

Edit `content/site.json` for shared details and `content/pages/*.json` for page text and sections. Supported section kinds are `text`, `meetings`, `contact`, and `beliefs`. All content text is HTML-escaped; arbitrary HTML is not accepted. Keep source URLs and retrieval dates with factual content. Review notes and `[Content needed]` appear only in source files and are not rendered.

The Beliefs content includes all 12 original statements. The build compares their wording, numbering, order, and introduction against `docs/statement-of-faith-source.md` and fails on changes. Do not change that source reference to bypass this safeguard.

Church confirmation is still needed for current Sunday times and time zone; conflicting weekday schedules; online/in-person and language arrangements; Sunday lunch; authentic vision/history; parking, accessibility, and what-to-expect guidance; email/contact destination; and future events. Conflicting weekday meetings are withheld from public output. The empty event list does not mean there are no church events. No events are displayed in Phase 1.

Directions use a plain Google Maps link derived from the verified address. No map embed, tracking script, contact form, or Zoom access URL is included.

## Deployment

The configured production origin is `https://www.caiwhome.org`, based on the audited public domain. Confirm it before deployment, or override it for a different production host:

```sh
PYTHONPATH=src python3 -m codex_project.build --origin https://your-production-domain.example
```

Use an HTTPS origin without a path, query, or credentials. The override changes canonical and Open Graph URLs. A preview deployment should use the intended production canonical origin and host-level indexing restrictions when appropriate.

After building and passing tests, upload the generated HTML directories and `assets/` from `dist/` to an HTTPS static host that serves directory `index.html` files. Do not publish source content, tests, or documentation. The `.site-build` marker is local build bookkeeping and can be excluded from the upload. There is no server process to deploy.

Before replacing the existing site, confirm church content and manually check the six pages on mobile and with keyboard navigation. Preserve existing archive routes and media on the current host or through a reviewed migration plan; this six-page foundation is not a wholesale replacement of the existing archives. No production deployment or DNS change is performed by this repository's build.

Keep credentials and machine-specific configuration out of version control. Add dependencies only when a concrete requirement needs them.
