# First Home Buyers Landing Page — Design Spec

**Date:** 2026-04-30  
**File:** `first-home-buyers.html`

## Goal

A dedicated conversion landing page for first home buyers. No footer. Focused entirely on getting a visitor to book a free 15-minute call with Finch Mortgage.

## Layout

Two-column split on desktop. Single column on mobile (form moves above headline on mobile).

```
┌─────────────────────────────────────────┐
│              NAV (shared header)         │
├────────────────────────┬────────────────┤
│  LEFT (60%)            │  RIGHT (40%)   │
│                        │  ┌──────────┐  │
│  Eyebrow tag           │  │  FORM    │  │
│  H1 headline           │  │  sticky  │  │
│  3 trust bullets       │  │          │  │
│  ─────────────         │  └──────────┘  │
│  Trust bar             │                │
│  Founder card          │                │
│  Testimonials (3)      │                │
│  FAQ (3 questions)     │                │
│  Final CTA link        │                │
└────────────────────────┴────────────────┘
```

## Sections

### Nav
Keep existing Finch shared header (`#main-header`) and mobile menu. No changes to nav.

### Left column (content)
1. **Eyebrow** — "First Home Buyers · Auckland"
2. **H1** — "Still renting in Auckland? You might be closer to your first home than you think."
3. **Sub-copy** — One sentence hook
4. **3 bullet points** — borrow amount / deposit / plan
5. **Trust bar** — Free & confidential · 4.9-star rated · 500+ families helped · FSPR registered
6. **Founder card** — Photo placeholder, name, title, bio, stats
7. **Testimonials** — 3 cards (James & Mere, Sarah & Tom, Priya M.)
8. **FAQ** — 3 questions (free? / not ready? / small deposit?)
9. **Text CTA** — "Ready to start? Book your free call →"

### Right column (sticky form)
- Heading: "Book your free 15-minute call"
- Fields: First name, Mobile, Auckland suburb, Buying timeline (dropdown)
- CTA button: "Yes — show me my options →" (Finch gold)
- Reassurance line: "Free · No obligation · FSPR registered"

## Styles

- Self-contained `<style>` block in `<head>` — page-specific styles do not depend on `style.css` beyond the nav
- Colours: Finch brand vars (forest `#10443e`, sage `#62a29a`, gold `#b29361`, mist `#f3ede5`)
- Sticky form: `position: sticky; top: 100px`
- Mobile breakpoint: `max-width: 768px` — single column, form first

## Out of scope

- Footer (removed — this is a conversion page)
- Any calculator or interactive tool beyond the booking form
