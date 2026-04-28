# Finch Mortgage — Full Site SEO Enhancement Design
**Date:** 2026-04-17  
**Scope:** All ~40 pages  
**Approach:** Shared template + batch injection via 7 parallel agents

---

## 1. Objectives

1. Fix all technical SEO gaps across every page (canonical, OG, schema, hreflang)
2. Strengthen content SEO (titles, meta descriptions, keyword-rich copy)
3. Add regional NZ SEO signals (areaServed, geo meta, NZ city keywords)
4. Optimise for AI search engines / GEO (ChatGPT, Perplexity, ClaudeBot)
5. Improve Core Web Vitals via performance quick-wins (no Tailwind CDN removal)
6. Generate `sitemap.xml` and `robots.txt`

---

## 2. Page Inventory & Agent Groups

| Agent | Pages |
|-------|-------|
| Agent 1 — Core | `index.html`, `about.html`, `contact.html`, `faq.html`, `blog.html`, `calculators.html`, `lenders.html` |
| Agent 2 — Services | `services/home-loan.html`, `services/investment-property.html`, `services/refinance.html`, `services/pre-approval.html`, `services/first-home-buyer.html`, `services/next-home-buyer.html`, `services/self-employed.html`, `services/asset-finance.html`, `services/commercial-property.html`, `services/construction-loan.html` |
| Agent 3 — Blog posts | `blog/deposit-requirements-nz.html`, `blog/how-much-can-i-borrow.html`, `blog/interest-rates-guide.html`, `blog/mortgage-tips.html` |
| Agent 4 — Calculators | `calculators/mortgage-calculator.html`, `calculators/borrowing-power.html`, `calculators/refinance-savings.html`, `calculators/extra-repayment.html` |
| Agent 5 — Lenders | `lenders/major-banks.html`, `lenders/non-bank-lenders.html`, `lenders/credit-unions.html`, `lenders/specialist-lenders.html` |
| Agent 6 — Guides + Testimonials + Case Studies | `guides/how-mortgage-works.html`, `guides/first-home-guide.html`, `guides/refinance-guide.html`, `guides/step-by-step.html`, `testimonials/reviews.html`, `testimonials/success-stories.html`, `case-studies/first-home-approval.html` |
| Agent 7 — Utility + Infrastructure | `map.html`, `privacy.html`, `terms.html`, `refinance.html`, `market-report.html`, `apply.html`, `services-overview.html`, `weekly-reports.html` + create `sitemap.xml`, `robots.txt` |

All 7 agents run in parallel.

---

## 3. Shared `<head>` Template (applied to every page)

```html
<!-- Canonical -->
<link rel="canonical" href="https://www.finchmortgage.co.nz/[page-path]">

<!-- hreflang -->
<link rel="alternate" hreflang="en-NZ" href="https://www.finchmortgage.co.nz/[page-path]">
<link rel="alternate" hreflang="x-default" href="https://www.finchmortgage.co.nz/[page-path]">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="[page title]">
<meta property="og:description" content="[meta description]">
<meta property="og:url" content="https://www.finchmortgage.co.nz/[page-path]">
<meta property="og:image" content="https://www.finchmortgage.co.nz/images/og-default.jpg">
<meta property="og:site_name" content="Finch Mortgage">
<meta property="og:locale" content="en_NZ">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[page title]">
<meta name="twitter:description" content="[meta description]">
<meta name="twitter:image" content="https://www.finchmortgage.co.nz/images/og-default.jpg">

<!-- Regional / GEO -->
<meta name="geo.region" content="NZ-AUK">
<meta name="geo.placename" content="Auckland, New Zealand">
<meta name="geo.position" content="-36.8509;174.7645">
<meta name="ICBM" content="-36.8509, 174.7645">

<!-- Performance -->
<link rel="preload" href="/style.css" as="style">
<link rel="preload" as="font" href="https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2" type="font/woff2" crossorigin>
<!-- Google Fonts URL: append &display=swap -->

<!-- Favicon -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">

<!-- Lucide: move to bottom of <body> with defer -->
<!-- All non-hero <img>: add loading="lazy" -->
```

---

## 4. Title Tag Formulas

| Page Type | Formula | Example |
|-----------|---------|---------|
| Homepage | `[Primary Keyword NZ] \| [Benefit] \| Finch Mortgage` | `Top NZ Mortgage Brokers \| Expert Advice & Best Rates \| Finch Mortgage` |
| Service | `[Service Name] NZ \| [Key Benefit] \| Finch Mortgage` | `First Home Buyer Mortgage NZ \| KiwiSaver & 5% Deposit Help \| Finch Mortgage` |
| Blog post | `[Post Topic] NZ [Year] \| [Angle] \| Finch` | `NZ Deposit Requirements 2026 \| 5%, 10% & 20% Explained \| Finch` |
| Calculator | `[Calculator Name] NZ \| Free Mortgage Tool \| Finch` | `Mortgage Repayment Calculator NZ \| Free Tool \| Finch` |
| Lender | `[Lender Group] NZ \| Compare Home Loan Rates \| Finch` | `Major NZ Banks Compared \| Best Home Loan Rates \| Finch` |
| Guide | `[Topic] NZ [Year] \| Step-by-Step Guide \| Finch` | `How to Get a Mortgage NZ 2026 \| Step-by-Step Guide \| Finch` |
| About | `About Finch Mortgage NZ \| Independent Brokers Since 2010` | — |
| Contact | `Contact Finch Mortgage NZ \| Free Mortgage Consultation` | — |
| FAQ | `Mortgage FAQ NZ 2026 \| Common Questions Answered \| Finch` | — |

**Meta description rule:** 150–160 characters, include primary NZ keyword + specific benefit + CTA.

---

## 5. Schema Markup Per Page Type

### Homepage
- `FinancialService` + `LocalBusiness` (existing — enhance)
  - Add `aggregateRating`: `{"ratingValue": "4.9", "reviewCount": "500", "bestRating": "5"}`
  - Add `areaServed`: `["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Dunedin", "Palmerston North", "Nelson", "New Zealand"]`
  - Add `sameAs`: Google Business, Facebook, LinkedIn URLs (extract from existing about.html/contact.html — do not invent)
  - Add `currenciesAccepted`: `"NZD"`, `priceRange`: `"Free"`
  - Add `telephone`, `openingHoursSpecification` (extract from contact.html — do not invent)
- `FAQPage` (existing — keep, expand to 5 Q&As)
- `BreadcrumbList`: Home

### Service Pages (×10)
```json
{
  "@type": "Service",
  "name": "[Service Name]",
  "description": "[Service description]",
  "provider": {"@type": "FinancialService", "name": "Finch Mortgage", "url": "https://www.finchmortgage.co.nz"},
  "areaServed": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Dunedin", "Palmerston North", "Nelson", "New Zealand"],
  "serviceType": "Mortgage Brokerage",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NZD", "description": "Free mortgage advice"}
}
```
- `FAQPage` (3–5 Q&As from existing page content)
- `BreadcrumbList`: Home → Services → [Service Name]

### Blog Posts (×4)
```json
{
  "@type": "BlogPosting",
  "headline": "[Post Title]",
  "description": "[Meta description]",
  "author": {"@type": "Organization", "name": "Finch Mortgage", "url": "https://www.finchmortgage.co.nz"},
  "publisher": {"@type": "Organization", "name": "Finch Mortgage", "logo": {"@type": "ImageObject", "url": "https://www.finchmortgage.co.nz/favicon.svg"}},
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "2026-04-17",
  "inLanguage": "en-NZ",
  "keywords": "[primary keyword], NZ mortgage, [secondary keywords]"
}
```
- `BreadcrumbList`: Home → Blog → [Post Title]
- Author byline block with `rel="author"` — add below the article heading using existing page content (do not add new sections, just wrap existing author/date info if present, or add a minimal "By Finch Mortgage | [date]" line)

### Calculator Pages (×4)
```json
{
  "@type": "WebApplication",
  "name": "[Calculator Name]",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Web",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NZD"},
  "provider": {"@type": "Organization", "name": "Finch Mortgage"}
}
```
- `BreadcrumbList`: Home → Calculators → [Calculator Name]

### Lender Pages (×4)
```json
{
  "@type": "ItemList",
  "name": "[Lender Group Name]",
  "description": "[Description]",
  "itemListElement": [{"@type": "ListItem", "position": 1, "name": "[Lender Name]"}, ...]
}
```
- `BreadcrumbList`: Home → Lenders → [Lender Group]

### Guide Pages (×4)
```json
{
  "@type": "HowTo",
  "name": "[Guide Title]",
  "description": "[Guide description]",
  "step": [{"@type": "HowToStep", "name": "[Step Name]", "text": "[Step description]"}, ...]
}
```
- `BreadcrumbList`: Home → Guides → [Guide Title]

### About Page
```json
[
  {"@type": "AboutPage", "name": "About Finch Mortgage", "url": "https://www.finchmortgage.co.nz/about.html"},
  {"@type": "Person", "name": "[Founder Name]", "jobTitle": "Founder & Principal Mortgage Broker", "worksFor": {"@type": "Organization", "name": "Finch Mortgage"}},
  {"@type": "LocalBusiness", "name": "Finch Mortgage", "areaServed": [...NZ cities...]}
]
```

### Contact Page
```json
{
  "@type": "ContactPage",
  "name": "Contact Finch Mortgage",
  "url": "https://www.finchmortgage.co.nz/contact.html",
  "mainEntity": {
    "@type": "LocalBusiness",
    "name": "Finch Mortgage",
    "telephone": "+64-...",
    "email": "...",
    "address": {"@type": "PostalAddress", "addressRegion": "Auckland", "addressCountry": "NZ"},
    "geo": {"@type": "GeoCoordinates", "latitude": "-36.8509", "longitude": "174.7645"},
    "hasMap": "https://www.finchmortgage.co.nz/map.html",
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "17:00"},
    "priceRange": "Free",
    "currenciesAccepted": "NZD"
  }
}
```

### FAQ Page
- Full `FAQPage` schema with all Q&As from the page

---

## 6. Regional NZ SEO

**areaServed cities** (all service/local schema):
Auckland, Wellington, Christchurch, Hamilton, Tauranga, Dunedin, Palmerston North, Nelson, New Zealand

**Keyword rotation across service + lender pages:**
- Primary: "NZ mortgage broker", "New Zealand home loan"
- Secondary (rotated): "Auckland mortgage broker", "Wellington home loan", "Christchurch first home buyer", "Hamilton mortgage advice", "Tauranga mortgage broker"
- NZ-specific terms reinforced site-wide: KiwiSaver, Kainga Ora, First Home Grant, LVR, OCR

**Copy additions to service pages:**
Each service page gets a regional paragraph:
> "Helping [service type] clients across Auckland, Wellington, Christchurch, Hamilton, Tauranga and throughout New Zealand."

**GEO meta (every page):**
```html
<meta name="geo.region" content="NZ-AUK">
<meta name="geo.placename" content="Auckland, New Zealand">
<meta name="geo.position" content="-36.8509;174.7645">
<meta name="ICBM" content="-36.8509, 174.7645">
```

---

## 7. GEO / AI Search Optimisation

**Entity paragraph** (added to homepage + about page):
> "Finch Mortgage is a New Zealand-based independent mortgage broker that compares home loan rates across 20+ lenders including ANZ, ASB, BNZ, Westpac, and Kiwibank. The service is free to borrowers. Finch specialises in first home buyers, refinancing, investment property loans, and self-employed mortgages across New Zealand."

**robots.txt AI crawler permissions:**
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Googlebot
Allow: /

Disallow: /weekly-reports/

Sitemap: https://www.finchmortgage.co.nz/sitemap.xml
```

---

## 8. Performance Quick-Wins

| Fix | Applies to | Impact |
|-----|-----------|--------|
| `&display=swap` on Google Fonts URL | All pages | Eliminates invisible text (FCP) |
| `<link rel="preload">` for style.css + font file | All pages | Reduces blocking time |
| Lucide script moved to end of `<body>` + `defer` | All pages | Removes render-blocking script |
| `loading="lazy"` on all non-hero images | All pages | Improves LCP |
| `<link rel="icon" href="/favicon.svg">` | All pages | Fixes missing favicon (crawl signal) |

---

## 9. Infrastructure Files

### sitemap.xml
- All ~40 pages listed
- Priority: homepage `1.0`, services `0.9`, blog `0.8`, guides `0.8`, calculators `0.7`, lenders `0.7`, about/contact/faq `0.7`, utility pages `0.3`
- `changefreq`: homepage/market-report `weekly`, blog/guides `monthly`, others `yearly`

### robots.txt
```
User-agent: *
Disallow: /weekly-reports/
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: https://www.finchmortgage.co.nz/sitemap.xml
```

---

## 10. Out of Scope

- Removing Tailwind CDN (requires build pipeline — future project)
- Adding new pages or content sections beyond what exists
- Actual rate data or lender-specific financial details (must remain as-is)
- Image optimisation / WebP conversion (no build pipeline)
