# Eleventy SSG Migration — Phase 1: Foundation + Lenders

## Context

Finch Mortgage is a static HTML/CSS/JS site, but "static" today means ~30 ad hoc
Python scripts (`generate_*.py`, `fix_*.py`, `update_*.py`, `add_*.py`,
`inject_*.py`) that either write whole HTML files from scratch or regex-patch
already-generated HTML in place. There is no templating layer: header/nav/footer
markup is duplicated as literal Python string constants across multiple
generator scripts (e.g. `generate_lender_pages.py`,
`generate_lender_pages_expanded.py`, and `generate_lender_reviews.py` each embed
their own copy of the same nav/footer HTML). This drift is what caused the
prior meta-stamping incident (a bulk script duplicated `<meta>` tags across 48
pages and caused deindexing).

Goal: migrate the site to a real static site generator (Eleventy) so that
content and templates are separated, shared layout lives in one place, and
pages are produced fresh from data + templates instead of hand-patched after
the fact. This is a large migration across many content types (blog, case
studies, lenders, weekly reports, guides, calculators, services, testimonials,
~15 static pages, plus RSS/sitemap/internal-linking tooling), so it is being
decomposed into phases. **This spec covers Phase 1 only**: the Eleventy
foundation (repo layout, build pipeline, shared layout/partials) plus migrating
`lenders/` end-to-end as the proof-of-concept.

## Decisions made

- **SSG tool:** Eleventy (11ty). Outputs plain static HTML, no client-side
  framework, keeps Vercel deploy simple, mature ecosystem for
  collections/pagination/RSS/sitemap that will eventually replace the
  Python content-generation scripts.
- **Repo layout:** move everything into `src/` now (mechanical relocation, no
  content changes) rather than leaving legacy files at root and merging build
  output back over them. One clean input root from day one; avoids a second
  reorg later.
- **Build output:** Eleventy builds to `_site/` (gitignored). Vercel runs the
  build at deploy time rather than committing generated HTML to git.
- **First content type to migrate:** `lenders/` — it's the most data-shaped
  content already (a clear repeating schema: name, category, rates commentary,
  pros/cons, FAQs), so it validates the whole pipeline (data files, pagination,
  permalinks, shared partials, JSON-LD macros) on a manageable, well-understood
  set of pages (29 files) before rolling the same pattern out to larger content
  types.

## Scope (Phase 1)

### 1. Repo reorganization

Move all current root-level files/folders into `src/`, unchanged:
`index.html`, `blog/`, `blog.html`, `calculators/`, `calculators.html`,
`case-studies/`, `case-studies.html`, `guides/`, `lenders/`, `lenders.html`,
`services/`, `services-overview.html`, `testimonials/`, `weekly-reports/`,
`weekly-reports.html`, `market-report.html`, `mortgage-rates.html`, `map.html`,
all static top-level pages (`about.html`, `contact.html`, `faq.html`,
`privacy.html`, `terms.html`, `disclaimer.html`, `disclosure.html`,
`fhb-*.html`, `thank-you.html`, etc.), `images/`, `logos/`, `favicon.png`,
`finch.mp4`, `style.css`, `script.js`, `robots.txt`, `sitemap.xml`, `rss.xml`,
`llms.txt`, `llms.md`. `tailwind.src.css` also moves into `src/`.

### 2. Eleventy configuration

- Input: `src/`. Output: `_site/` (gitignored).
- `htmlTemplateEngine: false` globally, so any plain `.html` file passes
  through byte-for-byte untouched unless it explicitly opts into templating
  (front matter + `.njk`/layout). This guarantees zero regression for every
  content type not yet migrated.
- Passthrough copy for `images/`, `logos/`, `favicon.png`, `finch.mp4`,
  `style.css`, `script.js`, `tailwind.css`, `robots.txt`, `sitemap.xml`,
  `rss.xml`.
- `tailwind.config.js` content globs updated from `./*.html`, `./blog/*.html`,
  etc. to `./src/**/*.html`.
- `package.json` `build:css` script outputs to `src/tailwind.css` (so it gets
  passthrough-copied to `_site/tailwind.css`, same public path as today). Add a
  combined `build` script that runs `build:css` then `eleventy`.

### 3. Shared layout & partials

New `src/_includes/`:
- `base.njk` — doctype/html/head boilerplate (charset, viewport, title/meta
  blocks driven by front matter, favicon, canonical link).
- `header.njk` / `footer.njk` — the nav and footer markup, extracted once from
  the current duplicated string constants.
- `schema.njk` — Nunjucks macro(s) for the JSON-LD blocks currently hand-written
  per page (BreadcrumbList, Article, Person, Organization), parameterized by
  page front matter (title, description, dates, breadcrumb trail).

### 4. Lenders migration

- `src/_data/lenders.js` — single source of truth, ported directly from the
  data currently embedded in the Python scripts:
  - The 4 hub categories (major banks, non-bank lenders, specialist lenders,
    credit unions) — each with badge, intro copy, member lender summaries, and
    FAQs (currently the `CATEGORIES` list in `generate_lender_pages.py` /
    `generate_lender_pages_expanded.py` — these two scripts must be reconciled
    since they appear to duplicate the same responsibility; the more recent /
    complete version wins).
  - The 25 individual lender review records (currently the `LENDERS` list in
    `generate_lender_reviews.py`): slug, name, category, tier, founded,
    positioning, specialties, best-for, and full review copy.
- `lender-review.njk` — templated once, driven by Eleventy pagination over the
  25 records, with `permalink` set per record to preserve the exact current
  URL (e.g. `/lenders/anz-home-loan-review.html`).
- `lenders-hub.njk` — templated once, paginated over the 4 categories, same
  permalink-preservation approach (`/lenders/major-banks.html`, etc.).
- `lenders.html` (top-level directory/listing page) converted to read from the
  same `_data/lenders.js` instead of its current hand-written listing.
- No URL changes anywhere in this phase — canonical URLs, sitemap entries, and
  inbound links all keep working unchanged.

### 5. Script retirement

Once every one of the 29 generated lender URLs is diffed against Eleventy's
output and confirmed equivalent (content and metadata parity — intentional
copy changes aside), delete:
- `generate_lender_pages.py`
- `generate_lender_pages_expanded.py`
- `generate_lender_reviews.py`
- `inject_lenders.py`

### 6. Deploy configuration

- `vercel.json`: add `"buildCommand": "npm run build"` and
  `"outputDirectory": "_site"`. Existing `redirects` and `headers` blocks are
  unchanged (they operate on public URL paths, which don't change).
- `.gitignore`: add `_site/`.

### 7. Verification

- For every one of the 29 `lenders/*.html` URLs, diff the Eleventy-rendered
  output against the current committed HTML (ignoring incidental whitespace)
  to confirm: same `<title>`, same meta description, same canonical URL, same
  JSON-LD content, same visible copy.
- Confirm `npm run build` succeeds end-to-end (tailwind build → eleventy
  build) and `_site/` contains a full mirror of every current top-level file
  and directory (untouched passthrough content) plus the newly templated
  lender pages.
- Spot-check a handful of non-lenders pages in `_site/` (e.g. `index.html`,
  `about.html`, a `blog/` post) to confirm passthrough left them byte-for-byte
  identical to their `src/` source.

## Out of scope (future phases)

- Migrating `blog/`, `case-studies/`, `guides/`, `services/`, `testimonials/`,
  `weekly-reports/`, `calculators/`, and the remaining static top-level pages
  to Eleventy templates/data collections.
- Converting `generate_rss_feed.py`, `build_internal_links.py`, sitemap
  generation, and the various one-off `fix_*.py` / `update_*.py` / `add_*.py`
  scripts into Eleventy collections/plugins. These continue to run as Python
  scripts in this phase, just repointed at `src/...` paths instead of repo
  root (a required companion fix even in Phase 1, otherwise they break
  immediately after the `src/` move).
- Calculators' client-side JS logic is relocated but not rewritten.

## Risks & considerations

- **Non-migrated tooling breaks after the `src/` move.** Any script that
  isn't retired in this phase (RSS, sitemap, internal links, the `fix_*`
  family) hardcodes `ROOT = "/Users/.../finch mortgage"` and writes to
  paths like `lenders/`, `blog/` relative to that root. These need their
  output paths repointed to `src/lenders/`, `src/blog/`, etc. as part of the
  Phase 1 implementation, even though converting their *logic* to Eleventy is
  out of scope.
- **Local preview workflow changes.** Previously pages could be opened
  directly or served from repo root; now `npx @11ty/eleventy --serve` (or
  `vercel dev`) is needed to see the true built output. Relative asset paths
  (e.g. `../images/...` from nested pages) are unaffected since Eleventy
  mirrors the `src/` directory structure 1:1 into `_site/`.
- **`generate_lender_pages.py` vs `generate_lender_pages_expanded.py`
  duplication.** Both appear to generate the same 4 hub pages independently;
  whichever produced the content currently committed in `lenders/*.html` is
  the one whose data migrates into `_data/lenders.js` — the other is dead code
  to be deleted, not reconciled.
