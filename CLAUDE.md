# Finch Mortgage — Claude Code Guide

## Project Overview

Static HTML/CSS/JS mortgage website with Python scripts for programmatic page generation (lenders, market reports, calculators, guides).

## Project Structure

```
index.html              # Homepage
style.css / script.js   # Global styles and scripts
blog/                   # Blog posts
calculators/            # Mortgage calculator pages
guides/                 # Mortgage guide pages
lenders/                # Lender pages (programmatically generated)
services/               # Service pages
testimonials/           # Testimonial pages
weekly-reports/         # Weekly market report pages
generate_lender_pages.py
generate_weekly_reports.py
inject_lenders.py
inject_market_report.py
update_calculator_links.py
update_grids.py
```

## Installed Skills

Invoke all skills via the `Skill` tool before responding.

### Design & UI
| Skill | Trigger |
|-------|---------|
| `frontend-design:frontend-design` | Building/styling any web page, component, or UI |
| `ui-ux-pro-max` | Designing dashboards, landing pages, or component systems; when needing color palettes, typography, or style variants |
| `mobile-design` | Mobile-first layouts, touch interactions, React Native / Flutter patterns |

### SEO (use the most specific skill)
| Skill | Trigger |
|-------|---------|
| `seo-audit` | Audit/diagnose SEO issues, meta tags review, SEO health check |
| `seo-optimizer` | Content optimization, keyword strategy, on-page SEO improvements |
| `seo-fundamentals` | E-E-A-T, Core Web Vitals, Google algorithm questions |
| `programmatic-seo` | Generating pages at scale (location pages, lender pages, comparison pages) |
| `schema-markup` | JSON-LD, structured data, rich snippets, schema.org types |
| `roier-seo` | Technical SEO audits with Lighthouse/PageSpeed; auto-fix meta tags, CWV, accessibility |
| `seo` | General "improve SEO", fix meta tags, sitemap optimization |
| `geo-fundamentals` | Optimizing for AI search engines (ChatGPT, Perplexity, Claude) |

### Performance & Quality
| Skill | Trigger |
|-------|---------|
| `web-performance-optimization` | Loading speed, Core Web Vitals, bundle size, caching |
| `web-quality-audit` | Full site audit — performance, accessibility, SEO, best practices |

### Content & Marketing
| Skill | Trigger |
|-------|---------|
| `content-creator` | Blog posts, social media content, brand voice, content calendars |

### Development
| Skill | Trigger |
|-------|---------|
| `code-reviewer` | PR reviews, code quality checks, security scanning |

### Marketing (from seomachine, added July 2026)
26 additional skills covering copywriting, CRO, pricing, email, paid ads, etc. — see `.claude/skills/` for the full list. Use when the task is clearly marketing/conversion strategy rather than SEO/dev (e.g. `copywriting`, `pricing-strategy`, `email-sequence`, `content-strategy`).

## SEO Content Workspace (seomachine)

This repo also includes [seomachine](https://github.com/TheCraigHewitt/seomachine), a Claude Code workspace for long-form SEO content, integrated 2026-07-06. It adds:

- **Commands** (`.claude/commands/`): `/research`, `/write`, `/optimize`, `/rewrite`, `/analyze-existing`, `/article`, `/cluster`, `/performance-review`, `/publish-draft`, plus landing-page and research-specific commands.
- **Agents** (`.claude/agents/`): content-analyzer, seo-optimizer, meta-creator, internal-linker, keyword-mapper, editor, headline-generator, cro-analyst, landing-page-optimizer, performance.
- **Context** (`context/`): brand-voice, features, internal-links-map, target-keywords, style-guide, seo-guidelines — all customized for Finch Mortgages (not the original Castos template). Read these before generating blog content.
- **Data sources** (`data_sources/`): Python modules for GA4, Google Search Console, and DataForSEO. Python env lives in `.venv-seomachine/` (gitignored) — activate with `source .venv-seomachine/bin/activate` before running any `data_sources/modules/*.py` or root-level `research_*.py` / `seo_*.py` scripts.
- **Working directories** (`drafts/`, `research/`, `topics/`, `rewrites/`, `published/`, `output/`): gitignored except `.gitkeep`.

**Important — skill overlap**: seomachine ships its own `seo-audit`, `programmatic-seo`, and `schema-markup` skills. These were **not** installed to avoid clobbering this project's existing customized versions of the same names (see SEO table above) — only non-overlapping seomachine skills were merged in.

**GSC/GA4 credentials are not yet configured.** `data_sources/config/.env` is scaffolded with `GSC_SITE_URL` and company info pre-filled, but `GA4_CREDENTIALS_PATH`/`GSC_CREDENTIALS_PATH` need a real Google Cloud service account JSON key, which only the site owner can create:
1. console.cloud.google.com → create/select a project → enable "Google Search Console API" (and "Google Analytics Data API" for GA4)
2. Create a service account → generate a JSON key → save to `./credentials/gsc-credentials.json` (gitignored)
3. In Search Console (search.google.com/search-console) → Settings → Users and permissions → add the service account's email as a user
4. Fill in `data_sources/config/.env` with the credential paths

Until that's done, do not fabricate or assume GSC/GA4 data — a prior incident in this project involved acting on an unverifiable, partially-fabricated "GSC report" pasted into chat. Only trust data pulled live through `data_sources/modules/google_search_console.py` with real configured credentials, or numbers the user confirms directly from the GSC UI.

## Key Conventions

- Pure static site — no build step, no framework. Keep it that way unless explicitly asked.
- Python scripts generate/inject HTML — do not hand-edit generated sections; modify the scripts instead.
- Mortgage content must remain accurate and compliant — do not invent rates, terms, or lender details.
- Prefer editing existing files over creating new ones.
- No comments unless the WHY is non-obvious.
