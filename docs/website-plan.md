# Church Assembly in Westminster: website audit and foundation plan

## Inspection status

The repository was inspected before changes: it contains a minimal Python package, one import smoke test, README.md, .gitignore, and AGENTS.md. There is no website implementation or dependency manifest.

Initial public-site inspection was blocked on October 2, 2026. A subsequent inspection on the same date succeeded after the saved domain configuration became usable. The draft settings were inspected: network access remains restricted, with exactly `caiwhome.org` and `www.caiwhome.org` as custom rules, alongside the existing package-manager preset. No domains or broader access were added during the successful inspection.

| Source URL | Verified result on October 2, 2026 |
| --- | --- |
| https://www.caiwhome.org/ | HTTP 200; homepage HTML retrieved. |
| https://caiwhome.org/ | Redirects to the www homepage; final HTTP 200. |
| https://www.caiwhome.org/robots.txt | HTTP 200; identifies Squarespace and the sitemap, restricts administrative/search/API paths and certain query formats. |
| https://www.caiwhome.org/sitemap.xml | HTTP 200; 81 entries representing 80 unique page URLs. `/new-page-89` occurs twice with different last-modified dates. |
| https://www.caiwhome.org/vision | HTTP 404; confirmed broken footer destination. |

The inventory followed sitemap URLs and discovered same-site HTML links: 83 distinct pages fetched, 82 HTTP 200 responses and one HTTP 404. Exact source URLs, retrieval dates, titles, final URLs, links, image references, and audio references are recorded in [source-inventory.json](source-inventory.json). The original beliefs text is preserved in [statement-of-faith-source.md](statement-of-faith-source.md). No website implementation has begun.

Scope: server-delivered HTML and source metadata, not a rendered-browser audit. Third-party resources and media playback were not fetched or verified; their URLs are catalogued only. Cart and robots-disallowed paths were excluded. Public Zoom access links are intentionally omitted from committed documentation to avoid retaining meeting access details. HTTP 200 does not prove that client-rendered content, downloads, or external links work.

## Verified content and current structure

All sources below were retrieved on October 2, 2026. These are verified published statements, not independent confirmation that every schedule remains operationally current.

### Identity, contact, and beliefs

The homepage, https://www.caiwhome.org/, identifies the church as “Church Assembly In Westminster.” Its footer publishes **8912 Hazard Ave, Westminster, CA 92683** and **714-894-9424**, followed by an About label and Our Vision link. The same footer appears on other pages. No email link was discovered in the audited HTML. A Facebook link points to https://www.facebook.com/profile.php?id=61554893282182; its external availability was not checked.

The homepage contains “Statement of Faith,” the introduction “We Believe according to the Holy Bible that:”, and 12 numbered statements. The full original visible wording is retained in the separate source document, without substituting a doctrinal summary. This is the source for the future dedicated Beliefs page.

### Navigation and visitor information

Published navigation links to Messages (`/messages`), Weekly Schedule (`/weekly-schedule`), Links (`/links`), Directions (`/directions`), 2025 Year-End Conference (`/conference`), Announcements (`/announcements`), a “Hebrews - 希伯来书” folder (`/hebrews-`), Outline of Hebrews (`/new-page-36`), Sunday Messages (`/sunday-messages`), and Gospel Blog (`/gospel-blog`). Mobile Open Menu/Close Menu controls and a Skip to Content link are present in the HTML; keyboard behavior was not tested.

https://www.caiwhome.org/directions contains a Squarespace map component configured with the same street address as the footer. Its configured address title has the typo “Church Acembly in Westminster.” Map rendering and actual directions behavior remain untested. There is no dedicated Visit Us or Contact destination in the retrieved navigation.

### Meeting information

https://www.caiwhome.org/weekly-schedule publishes:

| Day | Published time | Published meeting/location |
| --- | --- | --- |
| Sunday | 10AM - 10:50AM | Breaking of Bread; Meeting Hall; Zoom Meeting link. |
| Sunday | 11AM - 12:15PM | Sunday Message; Meeting Hall. |
| Sunday | 12:15PM | Lunch. |
| Tuesday | 7:30PM - 8:00PM | Joined Prayer Meeting; Zoom Meeting link. |
| Tuesday | 8:00PM - 9:00PM | Group Prayer Meeting; Chinese Zoom Meeting link. |
| Wednesday | 10:00AM -12:00PM | Sister Bible Study; Zoom Meeting link. |
| “Fryday” | None in retrieved schedule text | Day label without meeting details. |
| Saturday | 7:30PM - 9:00PM | Gospel Meeting; Zoom Meeting (Third Week). |
| Saturday | 7:30PM - 9:00PM | “Chines Bible Study”; Zoom Meeting link. |

https://www.caiwhome.org/announcements also publishes recurring meetings: Tuesday at 7:30 PM, Friday English Online Bible Study at 7:30 PM, and Saturday English Young People Bible Study and Chinese Online Bible Study at 7:30 PM. Its sister-study row reads **“星期三 Thursday” at 10:00 AM**; the Chinese weekday denotes Wednesday while the English says Thursday. This conflicts internally and with the Wednesday weekly schedule. Do not silently resolve it. The Gospel Meeting third-week convention, current weekday schedule, time zone, language arrangements, and online/in-person attendance need church confirmation before migration as current visitor guidance.

### Messages, resources, and images

https://www.caiwhome.org/messages contains monthly message headings through June 2026, with latest listed recording dated June 14, 2026. It exposes 37 Squarespace audio asset references; https://www.caiwhome.org/conference exposes four more. Titles, dates, and exact asset URLs are in the inventory. Playback and download availability are untested.

The messages page includes inconsistent metadata: a February 8, 2026 recording is also listed under May 2026, and a recording labeled March 31, 2024 appears under March 2026. Preserve the source labels and ask for corrections rather than guessing replacement dates or speaker names.

https://www.caiwhome.org/links and https://www.caiwhome.org/library provide hymn, conference, Bible-study, book, and other resource links, including YouTube, Google Drive, Bible tools, and external assemblies. Many sitemap pages contain English/Chinese study material, hymns, and dated resources under opaque `new-page-*` URLs. Keep these in the migration inventory and establish descriptive destinations/redirects after review; do not discard them because they are absent from the main navigation.

The inventory records 13 image-element occurrences, including duplicate image references, plus social preview images. The Weekly Schedule and Outline of Hebrews include image-based content; the Outline image appears at both https://www.caiwhome.org/new-page-36 and https://www.caiwhome.org/hebrews-. The Messages page includes a screenshot. These image elements have empty `alt` values in source. Their visual content, transcription, reuse permissions, and suitable alternative text remain unverified. Sitemap image captions include stock template text such as “Make it stand out” and “Whatever it is, the way you tell your story online can make all the difference.”

### Strengths and weaknesses

Useful existing material includes the original faith statement, published address/phone, recurring meeting details, bilingual content, recent message archive, and a broad resource library. The site has a viewport declaration, canonical metadata, Open Graph metadata, a sitemap, and a skip link. These provide a migration starting point; they do not establish full SEO or accessibility compliance.

The homepage begins with historical schedules rather than a visitor introduction. Dates and times vary in punctuation and AM/PM notation; some entries are incomplete or inconsistent. Key pages rely on images or scripts, opaque URLs make archives hard to identify, and the footer points to a missing vision page. HTML references numerous Squarespace scripts/styles; actual performance, visual contrast, responsive layout, and assistive-technology behavior require a separate browser audit.

## Broken, outdated, missing, and still-unverified content

**Confirmed broken:** https://www.caiwhome.org/vision returns HTTP 404. Do not recreate a vision statement from assumptions or redirect to unrelated About text. Other fetched page URLs return HTTP 200; external links, media, and fragment targets remain unverified.

**Outdated presentation:** https://www.caiwhome.org/ and https://www.caiwhome.org/upcoming-schedule show March, February, then January “Upcoming Schedule” sections without a year. Sitemap `lastmod` for `/upcoming-schedule` is 2024-03-03, and its listed Sunday/day pairings are consistent with 2024, but the visible schedule itself does not explicitly state the year. Do not treat these as upcoming. March 24 lacks a start time (“Sun March 24 - 12:15pm”), and February includes a March 31 entry. The 2025 Year-End Conference, December 19–21, 2025, is historical as of retrieval, although it remains a main navigation destination. Its recordings should remain available as archive content. Announcements include memorial events on December 8–9, 2025; these also belong in historical content rather than an upcoming-events section. No future-dated event was verified in the inspected HTML; this does not establish that the church has no upcoming events.

**Missing from retrieved content:** original vision wording; a dedicated first-visitor explanation; parking/accessibility guidance; verified email/contact-form destination; and a confirmed future-events list. Use `[Content needed]` where those are required, pending church input. No accessible replacement for the missing vision page was identified in the inventoried navigation.

**Still unverified:** operationally current schedules and their conflicts; image-only information; external link health; audio playback; map interaction; dynamic content on https://www.caiwhome.org/sunday-messages and https://www.caiwhome.org/gospel-blog (their fetched HTML has navigation/footer but no substantive readable main content); responsive behavior, contrast, keyboard operation, performance, media rights, and any content outside the discovery scope.

## Recommended sitemap

| Page | Purpose and content requirements |
| --- | --- |
| Home | Welcome, church name, verified introduction, primary meeting details, visit/directions/events actions, upcoming events, brief about section, location/contact, footer. |
| About | Existing church identity and history. Include vision only if authentic source content is recovered. |
| Beliefs | Complete original Statement of Faith, with its wording, order, references, and substance preserved. |
| Meetings | Verified recurring meeting times and locations. |
| Messages | Preserve existing message content and destinations after inventory. |
| Events | Verified upcoming events, with past events separated into an archive. |
| Visit Us | Meeting details, directions, and source-supported information about what to expect. |
| Contact | Verified contact information and location. No contact form service is assumed. |

Do not reproduce a broken vision link. Inspect `/vision` and any alternative source; redirect it to About only if equivalent original content is actually recovered. Otherwise omit the navigation link and record `[Content needed]` for the church to supply.

## Content safeguards

- Inventory reachable pages, navigation, downloads, message destinations, and images before implementation. Record source URLs and retrieval dates.
- Capture the original Statement of Faith and verify the migrated text against it. Do not substitute a theological summary. Any homepage beliefs excerpt must use verified original wording and link to the full page.
- Unknown facts use `[Content needed]`; no invented programs, schedules, ministries, addresses, or doctrinal content.
- Store event dates in ISO format with a verified time zone and explicit end time. Display consistent readable dates and times using semantic `time` elements. Do not infer the church's time zone from its name.
- Exclude ended events from the homepage during builds; rebuild when events expire. Treat dated schedules as historical until their year and current applicability are confirmed.
- Keep missing-content pages out of production publication until reviewed. Do not claim that an empty event list proves the church has no upcoming events.

## Proposed technology and structure

Use static semantic HTML and one responsive CSS stylesheet, generated by a small Python 3.12 standard-library build tool. Retain the existing Python foundation. No frontend framework, runtime server, database, package installation, or third-party dependency is needed for this informational site. Prefer reusable templates and structured JSON content over duplicated page markup. Add JavaScript only when a concrete interaction requires it.

Planned additions, after the public-site audit:

```text
content/
  site.json                 Verified church details and source references
  pages/                    Reviewed page content, including original beliefs
  events.json               Editable event records
web/
  templates/                Shared document, navigation, and footer templates
  assets/styles.css         Mobile-first styles
src/codex_project/
  build.py                  Static generation and content validation
tests/
  test_build.py             Generation, links, metadata, and content tests
docs/
  website-plan.md           Audit, decisions, and missing-content register
dist/                       Generated output; already ignored by Git
```

Keep CSS calm and restrained: legible system fonts, generous whitespace, visible focus, accessible contrast, and no unnecessary animation. Use skip navigation, meaningful headings, landmark elements, descriptive link text, image alternatives, and keyboard-operable navigation. Avoid a JavaScript-dependent mobile menu when wrapping navigation links will work.

## Foundation validation and deployment plan

The future build should validate required content, event date ordering, output links, semantic page structure, unique titles/descriptions, and preservation of original beliefs text. Use a configured production origin for canonical URLs and sitemap generation; do not guess a deployment URL. Automated tests supplement manual keyboard, contrast, narrow-screen, and screen-reader checks. Measure performance once actual assets exist.

Serve generated `dist/` locally with Python's HTTP server. Deploy only the generated directory to a static host supporting HTTPS, clean directory URLs, and redirects for verified legacy paths. No host or cloud service is selected yet. Document exact build, preview, and deployment commands in README.md when implemented and tested.

## Next steps before implementation

Public-site access and the HTML inventory are now verified. Full implementation remains paused as requested. Obtain church confirmation of conflicting meeting details and current events, original vision content if it should be retained, and visitor guidance. Review image-based and dynamic content before deciding what to migrate. A browser-based accessibility/performance assessment and external-media verification remain separate outstanding checks; no additional network domains were enabled for them.
