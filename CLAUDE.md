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

## Key Conventions

- Pure static site — no build step, no framework. Keep it that way unless explicitly asked.
- Python scripts generate/inject HTML — do not hand-edit generated sections; modify the scripts instead.
- Mortgage content must remain accurate and compliant — do not invent rates, terms, or lender details.
- Prefer editing existing files over creating new ones.
- No comments unless the WHY is non-obvious.
