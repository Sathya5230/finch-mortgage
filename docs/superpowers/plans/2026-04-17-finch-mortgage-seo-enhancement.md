# Finch Mortgage — Full Site SEO Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance all ~40 pages of the Finch Mortgage static site with full technical SEO, content SEO, regional NZ signals, GEO/AI search optimisation, performance quick-wins, plus generate sitemap.xml and robots.txt.

**Architecture:** 7 parallel agents each own a page group. Every page receives the same shared `<head>` additions (canonical, hreflang, OG, Twitter card, geo meta, font preload, favicon) plus page-type-specific schema, updated title/description, and regional NZ copy. Infrastructure files (sitemap.xml, robots.txt) are created by Agent 7.

**Tech Stack:** Static HTML, Tailwind CDN (unchanged), CSS custom properties in style.css, JSON-LD schema, Lucide icons.

---

## Shared Reference — Applied to EVERY Page

Every agent must apply all items in this block to each page they own. Agents should read this section first, then apply it to every file in their group.

### `<head>` additions (insert after `<meta name="description">`)

```html
<!-- Canonical -->
<link rel="canonical" href="https://www.finchmortgage.co.nz/PAGE_PATH">

<!-- hreflang -->
<link rel="alternate" hreflang="en-NZ" href="https://www.finchmortgage.co.nz/PAGE_PATH">
<link rel="alternate" hreflang="x-default" href="https://www.finchmortgage.co.nz/PAGE_PATH">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="PAGE_TITLE">
<meta property="og:description" content="PAGE_DESCRIPTION">
<meta property="og:url" content="https://www.finchmortgage.co.nz/PAGE_PATH">
<meta property="og:image" content="https://www.finchmortgage.co.nz/images/og-default.jpg">
<meta property="og:site_name" content="Finch Mortgage">
<meta property="og:locale" content="en_NZ">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="PAGE_TITLE">
<meta name="twitter:description" content="PAGE_DESCRIPTION">
<meta name="twitter:image" content="https://www.finchmortgage.co.nz/images/og-default.jpg">

<!-- Regional GEO -->
<meta name="geo.region" content="NZ-AUK">
<meta name="geo.placename" content="Auckland, New Zealand">
<meta name="geo.position" content="-36.8509;174.7645">
<meta name="ICBM" content="-36.8509, 174.7645">

<!-- Performance -->
<link rel="preload" href="RELATIVE_PATH_TO_style.css" as="style">
<link rel="preload" as="font" href="https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2" type="font/woff2" crossorigin>

<!-- Favicon -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
```

### Google Fonts URL fix (every page)
Find: `googleapis.com/css2?family=Inter...Playfair+Display...`
Ensure URL ends with `&display=swap`. If not present, append it.

### Lucide performance fix (every page)
- Remove `<script src="https://unpkg.com/lucide@latest"></script>` from `<head>`
- Add `<script src="https://unpkg.com/lucide@latest" defer></script>` just before `</body>`

### Lazy-load images (every page)
- Add `loading="lazy"` to every `<img>` tag that is NOT the first visible hero image
- Hero/first-visible images: add `loading="eager"` explicitly

### PAGE_PATH notes
- Root pages: `index.html` → path is just `index.html` (or `/`)
- Sub-pages: `services/home-loan.html` → path is `services/home-loan.html`
- `RELATIVE_PATH_TO_style.css`: root pages use `style.css`, sub-pages use `../style.css`

### areaServed array (reuse in all schema)
```json
["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Dunedin", "Palmerston North", "Nelson", "New Zealand"]
```

### Known contact data (extracted from contact.html)
- Phone: `0800 FINCH MZ`
- Email: `advisor@finchmortgage.co.nz`
- Region: Auckland, New Zealand
- Hours: Monday–Friday 09:00–17:00

---

## Task 1 — Agent 1: Core Pages

**Files to modify:**
- `index.html`
- `about.html`
- `contact.html`
- `faq.html`
- `blog.html`
- `calculators.html`
- `lenders.html`

- [ ] **Step 1.1: Apply shared `<head>` block to `index.html`**

  PAGE_PATH = `index.html`  
  PAGE_TITLE = `Top NZ Mortgage Brokers | Expert Advice & Best Rates | Finch Mortgage`  
  PAGE_DESCRIPTION = `Compare 20+ NZ lenders, get expert mortgage advice, and secure pre-approval in 24 hours. $0 broker fees. First home buyers welcome. Free consultation today.`  

  Insert the shared `<head>` block after `<meta name="description">`. Set `href` for `style.css` preload to `style.css` (root level).

- [ ] **Step 1.2: Enhance homepage schema in `index.html`**

  Find the existing `<script type="application/ld+json">` block and replace it with:

  ```json
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": ["FinancialService", "LocalBusiness"],
        "name": "Finch Mortgage",
        "url": "https://www.finchmortgage.co.nz",
        "logo": "https://www.finchmortgage.co.nz/favicon.svg",
        "description": "New Zealand independent mortgage broker. Compare 20+ lenders, $0 broker fees. Expert advice for first home buyers, refinancers, and property investors across NZ.",
        "telephone": "0800 FINCH MZ",
        "email": "advisor@finchmortgage.co.nz",
        "address": {
          "@type": "PostalAddress",
          "addressRegion": "Auckland",
          "addressCountry": "NZ"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": "-36.8509",
          "longitude": "174.7645"
        },
        "areaServed": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Dunedin", "Palmerston North", "Nelson", "New Zealand"],
        "currenciesAccepted": "NZD",
        "priceRange": "Free",
        "openingHoursSpecification": {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "09:00",
          "closes": "17:00"
        },
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "4.9",
          "reviewCount": "500",
          "bestRating": "5"
        }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "How long does the pre-approval process take?",
            "acceptedAnswer": {"@type": "Answer", "text": "Once you provide all the necessary documents (ID, proof of income, bank statements), we can typically get you a conditional pre-approval from a lender within 24 to 48 hours."}
          },
          {
            "@type": "Question",
            "name": "Do you charge a fee for your services?",
            "acceptedAnswer": {"@type": "Answer", "text": "For standard residential home loans, our service is completely free to you. We are paid a commission by the lender (bank) you choose to go with once the loan settles."}
          },
          {
            "@type": "Question",
            "name": "Can you help me use my KiwiSaver?",
            "acceptedAnswer": {"@type": "Answer", "text": "Absolutely. We specialise in helping first home buyers withdraw their KiwiSaver funds and apply for the First Home Grant (Kainga Ora)."}
          },
          {
            "@type": "Question",
            "name": "How many lenders do you compare?",
            "acceptedAnswer": {"@type": "Answer", "text": "We compare 20+ banks and non-bank lenders across New Zealand, including ANZ, ASB, BNZ, Westpac, Kiwibank, and specialist lenders."}
          },
          {
            "@type": "Question",
            "name": "What is the minimum deposit required to buy a home in NZ?",
            "acceptedAnswer": {"@type": "Answer", "text": "Most lenders require a 20% deposit for standard purchases. However, first home buyers may qualify for loans with as little as 5–10% deposit through Kainga Ora schemes and specialist lenders."}
          }
        ]
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.finchmortgage.co.nz/"}]
      }
    ]
  }
  ```

- [ ] **Step 1.3: Add GEO entity paragraph to `index.html`**

  Find the `<p>` tag in the hero section that begins "Compare lenders, explore better rates...". Add the following paragraph immediately after the footer `<p>` inside `.footer-brand` div (keep existing text, append new paragraph):

  ```html
  <p style="font-size:0.75rem;color:var(--neutral-warmGray);margin-top:0.5rem;line-height:1.6;">Finch Mortgage is a New Zealand-based independent mortgage broker comparing home loan rates across 20+ lenders including ANZ, ASB, BNZ, Westpac, and Kiwibank. Free to borrowers. Specialising in first home buyers, refinancing, investment property loans, and self-employed mortgages across New Zealand.</p>
  ```

- [ ] **Step 1.4: Apply Lucide defer + lazy-load images to `index.html`**

  Move Lucide script from `<head>` to just before `</body>` with `defer`. Add `loading="lazy"` to carousel slides 2, 3, 4 images. Slide 1 image gets `loading="eager"`.

- [ ] **Step 1.5: Apply shared `<head>` block to `about.html`**

  PAGE_PATH = `about.html`  
  PAGE_TITLE = `About Finch Mortgage NZ | Independent Mortgage Brokers Since 2010`  
  PAGE_DESCRIPTION = `Meet the team behind Finch Mortgage — New Zealand's trusted independent mortgage broker. 15 years experience, 500+ clients helped, $2.1B+ loans settled across NZ.`  

  Also fix the existing `<title>` tag from "Our Origins | Finch" to the new title above.

- [ ] **Step 1.6: Add schema + GEO entity to `about.html`**

  Add after existing `</style>` or before `</head>`:

  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "AboutPage",
        "name": "About Finch Mortgage",
        "url": "https://www.finchmortgage.co.nz/about.html",
        "description": "New Zealand's trusted independent mortgage broker with 15 years of experience helping Kiwi families buy homes."
      },
      {
        "@type": "LocalBusiness",
        "name": "Finch Mortgage",
        "url": "https://www.finchmortgage.co.nz",
        "telephone": "0800 FINCH MZ",
        "email": "advisor@finchmortgage.co.nz",
        "address": {"@type": "PostalAddress", "addressRegion": "Auckland", "addressCountry": "NZ"},
        "geo": {"@type": "GeoCoordinates", "latitude": "-36.8509", "longitude": "174.7645"},
        "areaServed": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Dunedin", "Palmerston North", "Nelson", "New Zealand"],
        "foundingDate": "2010",
        "priceRange": "Free",
        "currenciesAccepted": "NZD"
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.finchmortgage.co.nz/"},
          {"@type": "ListItem", "position": 2, "name": "About", "item": "https://www.finchmortgage.co.nz/about.html"}
        ]
      }
    ]
  }
  </script>
  ```

  Add GEO entity paragraph in the main body — find the first `<p>` in the main content area and add before it:

  ```html
  <p style="font-size:0.9rem;color:var(--neutral-medGray);line-height:1.7;margin-bottom:1.5rem;">Finch Mortgage is a New Zealand-based independent mortgage broker that compares home loan rates across 20+ lenders including ANZ, ASB, BNZ, Westpac, and Kiwibank. The service is free to borrowers. Finch specialises in first home buyers, refinancing, investment property loans, and self-employed mortgages across New Zealand.</p>
  ```

- [ ] **Step 1.7: Apply shared `<head>` + schema to `contact.html`**

  PAGE_PATH = `contact.html`  
  PAGE_TITLE = `Contact Finch Mortgage NZ | Free Mortgage Consultation`  
  PAGE_DESCRIPTION = `Get in touch with Finch Mortgage NZ for free expert mortgage advice. Call 0800 FINCH MZ, email us, or book a free consultation. Auckland-based, serving all of NZ.`  

  Add schema:
  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ContactPage",
    "name": "Contact Finch Mortgage",
    "url": "https://www.finchmortgage.co.nz/contact.html",
    "mainEntity": {
      "@type": "LocalBusiness",
      "name": "Finch Mortgage",
      "telephone": "0800 FINCH MZ",
      "email": "advisor@finchmortgage.co.nz",
      "address": {"@type": "PostalAddress", "addressRegion": "Auckland", "addressCountry": "NZ"},
      "geo": {"@type": "GeoCoordinates", "latitude": "-36.8509", "longitude": "174.7645"},
      "hasMap": "https://www.finchmortgage.co.nz/map.html",
      "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "17:00"},
      "priceRange": "Free",
      "currenciesAccepted": "NZD",
      "areaServed": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Dunedin", "Palmerston North", "Nelson", "New Zealand"]
    }
  }
  </script>
  ```
  BreadcrumbList: Home → Contact.

- [ ] **Step 1.8: Apply shared `<head>` + FAQPage schema to `faq.html`**

  PAGE_PATH = `faq.html`  
  PAGE_TITLE = `Mortgage FAQ NZ 2026 | Common Questions Answered | Finch`  
  PAGE_DESCRIPTION = `Answers to New Zealand's most common mortgage questions — deposit requirements, KiwiSaver, pre-approval timelines, lender criteria, and more. Free advice from Finch.`  

  Read all Q&As from the page and build a full `FAQPage` schema from them. BreadcrumbList: Home → FAQ.

- [ ] **Step 1.9: Apply shared `<head>` + schema to `blog.html`**

  PAGE_PATH = `blog.html`  
  PAGE_TITLE = `NZ Mortgage Blog 2026 | Expert Guides & Rate Updates | Finch`  
  PAGE_DESCRIPTION = `Expert NZ mortgage guides, interest rate updates, first home buyer tips, and refinancing advice from Finch Mortgage. Updated regularly for 2026.`  

  Add `CollectionPage` schema + BreadcrumbList: Home → Blog.

  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Finch Mortgage Blog",
    "url": "https://www.finchmortgage.co.nz/blog.html",
    "description": "Expert NZ mortgage guides, interest rate updates, and first home buyer advice.",
    "publisher": {"@type": "Organization", "name": "Finch Mortgage", "url": "https://www.finchmortgage.co.nz"}
  }
  </script>
  ```

- [ ] **Step 1.10: Apply shared `<head>` + schema to `calculators.html`**

  PAGE_PATH = `calculators.html`  
  PAGE_TITLE = `Free NZ Mortgage Calculators 2026 | Repayments, Borrowing Power | Finch`  
  PAGE_DESCRIPTION = `Free NZ mortgage calculators — repayment calculator, borrowing power, refinance savings, and extra repayment tools. No sign-up required. Try them now.`  

  Add `WebPage` + BreadcrumbList: Home → Calculators.

- [ ] **Step 1.11: Apply shared `<head>` + schema to `lenders.html`**

  PAGE_PATH = `lenders.html`  
  PAGE_TITLE = `NZ Mortgage Lenders Compared 2026 | Banks & Non-Bank Rates | Finch`  
  PAGE_DESCRIPTION = `Compare 20+ NZ mortgage lenders — major banks, non-bank lenders, credit unions, and specialist lenders. Find the best home loan rate for your situation.`  

  Add `ItemList` schema listing lender groups + BreadcrumbList: Home → Lenders.

- [ ] **Step 1.12: Apply Lucide defer + lazy-load to all Agent 1 pages**

  For each page in this group: move Lucide script from `<head>` to before `</body>` with `defer`. Add `loading="lazy"` to all non-first-visible `<img>` tags.

---

## Task 2 — Agent 2: Service Pages (×10)

**Files to modify:**
- `services/home-loan.html`
- `services/investment-property.html`
- `services/refinance.html`
- `services/pre-approval.html`
- `services/first-home-buyer.html`
- `services/next-home-buyer.html`
- `services/self-employed.html`
- `services/asset-finance.html`
- `services/commercial-property.html`
- `services/construction-loan.html`

Apply shared `<head>` block to every file. Use `../style.css` for the preload href (sub-directory).

**Title/description/path/schema values per service page:**

| File | PAGE_PATH | Title | Description |
|------|-----------|-------|-------------|
| home-loan.html | services/home-loan.html | `Home Loan NZ \| Buy Your Dream Home \| Finch Mortgage` | `Expert NZ home loan advice. Compare 20+ lenders, get the best rate, and secure your mortgage in 24 hours. $0 broker fee. Free consultation.` |
| investment-property.html | services/investment-property.html | `Investment Property Loan NZ \| Grow Your Portfolio \| Finch Mortgage` | `Get the best NZ investment property loan. We compare 20+ lenders for investors across Auckland, Wellington, Christchurch and all of NZ. Free advice.` |
| refinance.html | services/refinance.html | `Refinance Mortgage NZ \| Lower Your Rate & Save \| Finch Mortgage` | `Refinance your NZ mortgage and save. We find better rates across 20+ lenders. Average client saves $340/month. Free comparison — no obligation.` |
| pre-approval.html | services/pre-approval.html | `Mortgage Pre-Approval NZ \| 24hr Conditional Approval \| Finch Mortgage` | `Get mortgage pre-approval in 24 hours. Know your buying power before house hunting. Compare NZ lenders — $0 fee, no obligation. Apply online today.` |
| first-home-buyer.html | services/first-home-buyer.html | `First Home Buyer Mortgage NZ \| KiwiSaver & 5% Deposit \| Finch Mortgage` | `Expert first home buyer mortgage advice in NZ. KiwiSaver withdrawal, First Home Grant, 5–10% deposit options. Pre-approved in 24hrs. Free consult.` |
| next-home-buyer.html | services/next-home-buyer.html | `Next Home Buyer Mortgage NZ \| Upgrade or Move \| Finch Mortgage` | `Moving to your next home in NZ? We manage the mortgage for your existing sale and new purchase simultaneously. Expert advice, best rates, free service.` |
| self-employed.html | services/self-employed.html | `Self Employed Mortgage NZ \| Low Doc & Alt Doc Loans \| Finch Mortgage` | `Self-employed NZ mortgage specialists. Low-doc and alt-doc options, specialist lenders who understand business income. Get approved in 48 hours.` |
| asset-finance.html | services/asset-finance.html | `Asset Finance NZ \| Vehicles & Equipment Loans \| Finch Mortgage` | `NZ asset finance for vehicles, equipment, and business assets. Fast approval, competitive rates. Compare lenders across New Zealand. Free advice.` |
| commercial-property.html | services/commercial-property.html | `Commercial Property Loan NZ \| Expert Finance Advice \| Finch Mortgage` | `Commercial property loans in New Zealand. Expert advice for retail, office, and industrial property finance. Compare lenders. Free consultation.` |
| construction-loan.html | services/construction-loan.html | `Construction Loan NZ \| Build Your Home \| Finch Mortgage` | `New build and construction loans across New Zealand. Progressive drawdown finance, compare 20+ lenders, expert guidance. Free consultation.` |

- [ ] **Step 2.1: Apply shared `<head>` block to all 10 service pages**

  For each file: insert canonical, hreflang, OG tags, Twitter card, geo meta, preload links, and favicon after `<meta name="description">`. Update `<title>` tags to the new titles in the table above. Update `<meta name="description">` content to the new descriptions above.

- [ ] **Step 2.2: Add Service schema to all 10 service pages**

  For each service page, add inside `<head>` before `</head>`:

  **home-loan.html:**
  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {"@type":"Service","name":"Home Loan / Buy a Home","description":"Expert NZ home loan advice comparing 20+ lenders to find the best mortgage rate for your situation.","provider":{"@type":"FinancialService","name":"Finch Mortgage","url":"https://www.finchmortgage.co.nz"},"areaServed":["Auckland","Wellington","Christchurch","Hamilton","Tauranga","Dunedin","Palmerston North","Nelson","New Zealand"],"serviceType":"Mortgage Brokerage","offers":{"@type":"Offer","price":"0","priceCurrency":"NZD","description":"Free mortgage advice"}},
    {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},{"@type":"ListItem","position":2,"name":"Services","item":"https://www.finchmortgage.co.nz/services-overview.html"},{"@type":"ListItem","position":3,"name":"Home Loan","item":"https://www.finchmortgage.co.nz/services/home-loan.html"}]}
  ]}
  </script>
  ```

  Apply the same pattern for all 10 service pages, updating `name`, `description`, and the final BreadcrumbList item `name`/`item` for each service.

  **Service names for BreadcrumbList:**
  - investment-property.html → "Investment Property Loan"
  - refinance.html → "Refinance Mortgage"
  - pre-approval.html → "Mortgage Pre-Approval"
  - first-home-buyer.html → "First Home Buyer Mortgage"
  - next-home-buyer.html → "Next Home Buyer Mortgage"
  - self-employed.html → "Self Employed Mortgage"
  - asset-finance.html → "Asset Finance"
  - commercial-property.html → "Commercial Property Loan"
  - construction-loan.html → "Construction Loan"

- [ ] **Step 2.3: Add regional NZ paragraph to each service page**

  For each service page, find the first descriptive `<p>` in the `<main>` content (not nav, not header). Add this paragraph immediately after it, adapting `[service type]`:

  | File | [service type] text |
  |------|---------------------|
  | home-loan.html | `home loan` |
  | investment-property.html | `investment property loan` |
  | refinance.html | `mortgage refinancing` |
  | pre-approval.html | `mortgage pre-approval` |
  | first-home-buyer.html | `first home buyer mortgage` |
  | next-home-buyer.html | `next home buyer mortgage` |
  | self-employed.html | `self-employed mortgage` |
  | asset-finance.html | `asset finance` |
  | commercial-property.html | `commercial property finance` |
  | construction-loan.html | `construction loan` |

  ```html
  <p style="font-size:0.9rem;color:var(--neutral-medGray);line-height:1.7;margin-top:1rem;">Helping [service type] clients across Auckland, Wellington, Christchurch, Hamilton, Tauranga and throughout New Zealand. Free advice, $0 broker fee.</p>
  ```

- [ ] **Step 2.4: Apply Lucide defer + lazy-load to all 10 service pages**

  Move Lucide from `<head>` to before `</body>` with `defer`. Add `loading="lazy"` to all non-first `<img>` tags.

---

## Task 3 — Agent 3: Blog Posts (×4)

**Files to modify:**
- `blog/deposit-requirements-nz.html`
- `blog/how-much-can-i-borrow.html`
- `blog/interest-rates-guide.html`
- `blog/mortgage-tips.html`

Use `../style.css` for preload href. All `og:type` values should be `article`.

**Values per blog page:**

| File | PAGE_PATH | Title | Description | datePublished | Keywords |
|------|-----------|-------|-------------|---------------|---------|
| deposit-requirements-nz.html | blog/deposit-requirements-nz.html | `NZ Deposit Requirements 2026 \| 5%, 10% & 20% Explained \| Finch` | `How much deposit do you need to buy a home in NZ in 2026? We explain the 5%, 10%, and 20% thresholds, KiwiSaver options, and Kainga Ora First Home Grant.` | 2025-01-15 | NZ deposit requirements, first home buyer deposit NZ, KiwiSaver deposit |
| how-much-can-i-borrow.html | blog/how-much-can-i-borrow.html | `How Much Can I Borrow for a Mortgage NZ 2026 \| Finch` | `Find out how much NZ banks will lend you. We explain income multipliers, DTI ratios, and how lenders calculate your maximum NZ mortgage borrowing power.` | 2025-02-10 | how much can I borrow NZ, NZ mortgage borrowing power, NZ home loan limits |
| interest-rates-guide.html | blog/interest-rates-guide.html | `NZ Mortgage Interest Rates Guide 2026 \| Fixed vs Floating \| Finch` | `Fixed vs floating mortgage rates in NZ — which wins in 2026? Compare 1-year, 2-year, and floating rate options. Expert NZ mortgage rate advice from Finch.` | 2025-03-01 | NZ mortgage interest rates 2026, fixed vs floating NZ, best mortgage rate NZ |
| mortgage-tips.html | blog/mortgage-tips.html | `Top NZ Mortgage Tips 2026 \| Expert Advice for Kiwi Borrowers \| Finch` | `Expert NZ mortgage tips for 2026 — how to get the best rate, improve your borrowing power, use KiwiSaver, and navigate the NZ home loan market.` | 2025-04-01 | NZ mortgage tips, home loan advice NZ, mortgage broker tips NZ |

- [ ] **Step 3.1: Apply shared `<head>` block to all 4 blog pages**

  For each file: insert all shared `<head>` tags. Set `og:type` to `article` (not `website`). Update `<title>` and `<meta name="description">` to values in the table above.

- [ ] **Step 3.2: Add BlogPosting schema to all 4 blog pages**

  Add inside `<head>` before `</head>` for each blog post (substitute values from table above):

  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {
      "@type":"BlogPosting",
      "headline":"[Title from table]",
      "description":"[Description from table]",
      "author":{"@type":"Organization","name":"Finch Mortgage","url":"https://www.finchmortgage.co.nz"},
      "publisher":{"@type":"Organization","name":"Finch Mortgage","logo":{"@type":"ImageObject","url":"https://www.finchmortgage.co.nz/favicon.svg"}},
      "datePublished":"[datePublished from table]",
      "dateModified":"2026-04-17",
      "inLanguage":"en-NZ",
      "keywords":"[Keywords from table]",
      "url":"https://www.finchmortgage.co.nz/[PAGE_PATH]",
      "mainEntityOfPage":{"@type":"WebPage","@id":"https://www.finchmortgage.co.nz/[PAGE_PATH]"}
    },
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"Blog","item":"https://www.finchmortgage.co.nz/blog.html"},
      {"@type":"ListItem","position":3,"name":"[Post Title short]","item":"https://www.finchmortgage.co.nz/[PAGE_PATH]"}
    ]}
  ]}
  </script>
  ```

- [ ] **Step 3.3: Add author byline to all 4 blog pages**

  For each blog post, find the main article `<h1>` or first `<h2>`. Immediately after it, add:

  ```html
  <p style="font-size:0.8rem;color:var(--neutral-warmGray);margin-bottom:1.5rem;" rel="author">By <strong>Finch Mortgage</strong> | Updated April 2026 | Auckland, New Zealand</p>
  ```

- [ ] **Step 3.4: Apply Lucide defer + lazy-load to all 4 blog pages**

---

## Task 4 — Agent 4: Calculator Pages (×4)

**Files to modify:**
- `calculators/mortgage-calculator.html`
- `calculators/borrowing-power.html`
- `calculators/refinance-savings.html`
- `calculators/extra-repayment.html`

Use `../style.css` for preload href.

**Values per calculator page:**

| File | PAGE_PATH | Title | Description | App Name |
|------|-----------|-------|-------------|---------|
| mortgage-calculator.html | calculators/mortgage-calculator.html | `Mortgage Repayment Calculator NZ 2026 \| Free Tool \| Finch` | `Calculate your NZ mortgage repayments instantly. Weekly, fortnightly, or monthly. Free mortgage calculator — no sign-up. Try it now.` | Mortgage Repayment Calculator NZ |
| borrowing-power.html | calculators/borrowing-power.html | `Borrowing Power Calculator NZ 2026 \| How Much Can You Borrow \| Finch` | `Find out how much you can borrow for a home loan in NZ. Free borrowing power calculator — see what NZ banks will lend you based on your income.` | Borrowing Power Calculator NZ |
| refinance-savings.html | calculators/refinance-savings.html | `Refinance Savings Calculator NZ 2026 \| See How Much You Save \| Finch` | `Calculate how much you could save by refinancing your NZ mortgage. Compare current vs new rate and see instant monthly savings. Free tool.` | Refinance Savings Calculator NZ |
| extra-repayment.html | calculators/extra-repayment.html | `Extra Repayment Calculator NZ 2026 \| Pay Off Mortgage Faster \| Finch` | `See how extra mortgage repayments reduce your NZ loan term and total interest. Free extra repayment calculator — no sign-up required.` | Extra Repayment Calculator NZ |

- [ ] **Step 4.1: Apply shared `<head>` block to all 4 calculator pages**

  Update `<title>` and `<meta name="description">` from the table above.

- [ ] **Step 4.2: Add WebApplication schema to all 4 calculator pages**

  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {
      "@type":"WebApplication",
      "name":"[App Name from table]",
      "applicationCategory":"FinanceApplication",
      "operatingSystem":"Web",
      "url":"https://www.finchmortgage.co.nz/[PAGE_PATH]",
      "offers":{"@type":"Offer","price":"0","priceCurrency":"NZD","description":"Free online mortgage calculator"},
      "provider":{"@type":"Organization","name":"Finch Mortgage","url":"https://www.finchmortgage.co.nz"}
    },
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"Calculators","item":"https://www.finchmortgage.co.nz/calculators.html"},
      {"@type":"ListItem","position":3,"name":"[App Name]","item":"https://www.finchmortgage.co.nz/[PAGE_PATH]"}
    ]}
  ]}
  </script>
  ```

- [ ] **Step 4.3: Apply Lucide defer + lazy-load to all 4 calculator pages**

---

## Task 5 — Agent 5: Lender Pages (×4)

**Files to modify:**
- `lenders/major-banks.html`
- `lenders/non-bank-lenders.html`
- `lenders/credit-unions.html`
- `lenders/specialist-lenders.html`

Use `../style.css` for preload href.

**Values per lender page:**

| File | PAGE_PATH | Title | Description |
|------|-----------|-------|-------------|
| major-banks.html | lenders/major-banks.html | `Major NZ Banks Compared 2026 \| ANZ, ASB, BNZ, Westpac Rates \| Finch` | `Compare NZ major bank home loan rates — ANZ, ASB, BNZ, Westpac, Kiwibank. Find the best mortgage rate from NZ's big banks. Free comparison from Finch.` |
| non-bank-lenders.html | lenders/non-bank-lenders.html | `NZ Non-Bank Mortgage Lenders 2026 \| Alternative Home Loans \| Finch` | `Explore NZ non-bank mortgage lenders — Resimac, Pepper Money, Liberty, Bluestone. Better rates for complex situations. Free comparison from Finch Mortgage.` |
| credit-unions.html | lenders/credit-unions.html | `NZ Credit Union Home Loans 2026 \| Compare Member Rates \| Finch` | `Compare NZ credit union mortgage rates — NZCU Baywide, Unity, Police Credit Union. Member-owned lenders with competitive home loan rates. Free advice.` |
| specialist-lenders.html | lenders/specialist-lenders.html | `NZ Specialist Mortgage Lenders 2026 \| Non-Conforming Loans \| Finch` | `NZ specialist mortgage lenders for complex borrowing situations. Low-doc, non-conforming, and second-chance home loans. Free expert advice from Finch.` |

- [ ] **Step 5.1: Apply shared `<head>` block to all 4 lender pages**

  Update titles and descriptions from the table above.

- [ ] **Step 5.2: Add ItemList schema to all 4 lender pages**

  Read each lender page to identify the lenders listed. Build `ItemList` schema from the actual lenders present. Example for `major-banks.html`:

  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {
      "@type":"ItemList",
      "name":"Major NZ Banks — Home Loan Comparison",
      "description":"Comparison of major New Zealand bank mortgage rates by Finch Mortgage.",
      "url":"https://www.finchmortgage.co.nz/lenders/major-banks.html",
      "itemListElement":[
        {"@type":"ListItem","position":1,"name":"ANZ Home Loan"},
        {"@type":"ListItem","position":2,"name":"ASB Home Loan"},
        {"@type":"ListItem","position":3,"name":"BNZ Home Loan"},
        {"@type":"ListItem","position":4,"name":"Westpac Home Loan"},
        {"@type":"ListItem","position":5,"name":"Kiwibank Home Loan"}
      ]
    },
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"Lenders","item":"https://www.finchmortgage.co.nz/lenders.html"},
      {"@type":"ListItem","position":3,"name":"Major Banks","item":"https://www.finchmortgage.co.nz/lenders/major-banks.html"}
    ]}
  ]}
  </script>
  ```

  Apply the same pattern to the other 3 lender pages reading actual lender names from each page.

- [ ] **Step 5.3: Apply Lucide defer + lazy-load to all 4 lender pages**

---

## Task 6 — Agent 6: Guides, Testimonials & Case Studies

**Files to modify:**
- `guides/how-mortgage-works.html`
- `guides/first-home-guide.html`
- `guides/refinance-guide.html`
- `guides/step-by-step.html`
- `testimonials/reviews.html`
- `testimonials/success-stories.html`
- `case-studies/first-home-approval.html`

Use `../style.css` for preload href.

**Values per page:**

| File | PAGE_PATH | Title | Description |
|------|-----------|-------|-------------|
| how-mortgage-works.html | guides/how-mortgage-works.html | `How Mortgages Work NZ 2026 \| Complete Guide \| Finch` | `Everything you need to know about how NZ mortgages work — types, rates, LVR, repayments, and the full approval process. Free guide from Finch Mortgage.` |
| first-home-guide.html | guides/first-home-guide.html | `First Home Buyer Guide NZ 2026 \| KiwiSaver, Grants & Deposits \| Finch` | `Complete NZ first home buyer guide for 2026. KiwiSaver withdrawal, Kainga Ora First Home Grant, deposit requirements, and step-by-step buying process.` |
| refinance-guide.html | guides/refinance-guide.html | `Mortgage Refinancing Guide NZ 2026 \| When & How to Refinance \| Finch` | `Should you refinance your NZ mortgage? Our 2026 guide covers when to refinance, how to compare rates, break fees, and how to save thousands.` |
| step-by-step.html | guides/step-by-step.html | `Step-by-Step Mortgage Guide NZ 2026 \| From Application to Settlement \| Finch` | `A complete step-by-step NZ mortgage guide — from first consultation to settlement. Know exactly what to expect at every stage of your home loan journey.` |
| reviews.html | testimonials/reviews.html | `Finch Mortgage Client Reviews NZ \| 4.9★ Google Rating \| Finch` | `Read 500+ verified client reviews for Finch Mortgage NZ. 4.9★ Google rating. Real stories from first home buyers, investors, and refinancers across NZ.` |
| success-stories.html | testimonials/success-stories.html | `Finch Mortgage Success Stories NZ \| Real Client Results \| Finch` | `Real NZ mortgage success stories — first home approvals, refinancing savings, and investment portfolio growth. See how Finch helped Kiwi families.` |
| first-home-approval.html | case-studies/first-home-approval.html | `First Home Approval Case Study NZ \| 9% Deposit \| Finch Mortgage` | `How Finch Mortgage helped a NZ couple get first home approval with just 9% deposit after being rejected by major banks. Real case study.` |

- [ ] **Step 6.1: Apply shared `<head>` block to all 7 pages in this group**

  Update titles and descriptions from the table above.

- [ ] **Step 6.2: Add HowTo schema to guide pages**

  Read each guide page to identify the numbered steps in the content. Build `HowTo` schema from actual step content. Example pattern for `how-mortgage-works.html`:

  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {
      "@type":"HowTo",
      "name":"How to Get a Mortgage in NZ",
      "description":"A step-by-step guide to getting a mortgage in New Zealand.",
      "step":[
        {"@type":"HowToStep","position":"1","name":"Free Consultation","text":"Tell us about your situation — income, deposit, goals. No obligation, no cost."},
        {"@type":"HowToStep","position":"2","name":"We Compare Lenders","text":"Finch searches 20+ banks and non-bank lenders simultaneously, finding the lowest rate for your situation."},
        {"@type":"HowToStep","position":"3","name":"Pre-Approval in 24h","text":"Once your documents are in, we typically deliver a conditional pre-approval within one business day."},
        {"@type":"HowToStep","position":"4","name":"Settlement & Support","text":"We handle lender negotiations, paperwork, and solicitor coordination through to settlement."}
      ]
    },
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"Guides","item":"https://www.finchmortgage.co.nz/guides/how-mortgage-works.html"},
      {"@type":"ListItem","position":3,"name":"How Mortgages Work","item":"https://www.finchmortgage.co.nz/guides/how-mortgage-works.html"}
    ]}
  ]}
  </script>
  ```

  Apply same pattern to the other 3 guide pages — read actual steps from each page.

- [ ] **Step 6.3: Add Review/AggregateRating schema to testimonials pages**

  For `testimonials/reviews.html`:
  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {
      "@type":"LocalBusiness",
      "name":"Finch Mortgage",
      "url":"https://www.finchmortgage.co.nz",
      "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"500","bestRating":"5"}
    },
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"Reviews","item":"https://www.finchmortgage.co.nz/testimonials/reviews.html"}
    ]}
  ]}
  </script>
  ```

  For `testimonials/success-stories.html`: same pattern with BreadcrumbList pointing to success-stories.html.

- [ ] **Step 6.4: Add CaseStudy schema to `case-studies/first-home-approval.html`**

  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {
      "@type":"Article",
      "headline":"First Home Approval Case Study — 9% Deposit NZ",
      "description":"How Finch Mortgage helped a NZ couple get first home approval with just 9% deposit after being rejected by major banks.",
      "author":{"@type":"Organization","name":"Finch Mortgage","url":"https://www.finchmortgage.co.nz"},
      "publisher":{"@type":"Organization","name":"Finch Mortgage","logo":{"@type":"ImageObject","url":"https://www.finchmortgage.co.nz/favicon.svg"}},
      "datePublished":"2025-06-01",
      "dateModified":"2026-04-17",
      "inLanguage":"en-NZ"
    },
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"Case Studies","item":"https://www.finchmortgage.co.nz/case-studies/first-home-approval.html"}
    ]}
  ]}
  </script>
  ```

- [ ] **Step 6.5: Apply Lucide defer + lazy-load to all 7 pages in this group**

---

## Task 7 — Agent 7: Utility Pages + Infrastructure Files

**Files to modify:**
- `map.html`
- `privacy.html`
- `terms.html`
- `refinance.html`
- `market-report.html`
- `apply.html`
- `services-overview.html`
- `weekly-reports.html`

**Files to create:**
- `sitemap.xml`
- `robots.txt`

**Values per utility page:**

| File | PAGE_PATH | Title | Description |
|------|-----------|-------|-------------|
| map.html | map.html | `Find Finch Mortgage NZ \| Auckland Mortgage Broker Location \| Finch` | `Find Finch Mortgage's Auckland office. NZ mortgage broker serving all of New Zealand. Get directions and book a free in-person consultation.` |
| privacy.html | privacy.html | `Privacy Policy \| Finch Mortgage NZ` | `Finch Mortgage NZ privacy policy — how we collect, use, and protect your personal information in accordance with the NZ Privacy Act 2020.` |
| terms.html | terms.html | `Terms & Conditions \| Finch Mortgage NZ` | `Finch Mortgage NZ terms and conditions of service. Read our terms before using our mortgage advisory services.` |
| refinance.html | refinance.html | `Refinance Calculator NZ \| Should You Refinance? \| Finch Mortgage` | `Use Finch Mortgage's NZ refinance tool to see if refinancing makes sense for your situation. Compare rates and calculate potential savings.` |
| market-report.html | market-report.html | `NZ Mortgage Market Report 2026 \| Latest Rate Insights \| Finch` | `Latest NZ mortgage market report — interest rate trends, OCR updates, and housing market insights for 2026. Updated weekly by Finch Mortgage.` |
| apply.html | apply.html | `Apply for a Mortgage NZ \| Start Your Application \| Finch Mortgage` | `Start your NZ mortgage application with Finch Mortgage. Free, no-obligation process. Pre-approval in 24 hours. Compare 20+ lenders.` |
| services-overview.html | services-overview.html | `All NZ Mortgage Services \| Home Loans, Refinancing & More \| Finch` | `Complete overview of Finch Mortgage's NZ services — home loans, investment property, refinancing, first home buyer, self-employed, and more.` |
| weekly-reports.html | weekly-reports.html | `NZ Weekly Mortgage Rate Reports \| Market Updates \| Finch` | `Weekly NZ mortgage rate and market reports from Finch Mortgage. Stay up to date with OCR changes, bank rate movements, and housing market news.` |

- [ ] **Step 7.1: Apply shared `<head>` block to all 8 utility pages**

  Add all shared tags, canonical, hreflang, OG, geo meta, preload, favicon. Update titles and descriptions from the table above. Use `style.css` (root level) for preload href on root pages; `../style.css` would not apply here as all utility pages are at root level.

- [ ] **Step 7.2: Add minimal schema to utility pages**

  Add `WebPage` + `BreadcrumbList` schema to each:

  ```html
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {"@type":"WebPage","name":"[Page Title]","url":"https://www.finchmortgage.co.nz/[PAGE_PATH]","publisher":{"@type":"Organization","name":"Finch Mortgage"}},
    {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://www.finchmortgage.co.nz/"},
      {"@type":"ListItem","position":2,"name":"[Page Name]","item":"https://www.finchmortgage.co.nz/[PAGE_PATH]"}
    ]}
  ]}
  </script>
  ```

  Exception — `map.html` also gets `LocalBusiness` with geo coordinates:
  ```json
  {"@type":"LocalBusiness","name":"Finch Mortgage","geo":{"@type":"GeoCoordinates","latitude":"-36.8509","longitude":"174.7645"},"hasMap":"https://www.finchmortgage.co.nz/map.html","address":{"@type":"PostalAddress","addressRegion":"Auckland","addressCountry":"NZ"}}
  ```

- [ ] **Step 7.3: Apply Lucide defer + lazy-load to all 8 utility pages**

- [ ] **Step 7.4: Create `sitemap.xml`**

  Create `sitemap.xml` at project root:

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <!-- Homepage -->
    <url><loc>https://www.finchmortgage.co.nz/index.html</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>

    <!-- Core pages -->
    <url><loc>https://www.finchmortgage.co.nz/about.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/contact.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/faq.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/blog.html</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/calculators.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/lenders.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services-overview.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/apply.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/market-report.html</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/refinance.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/weekly-reports.html</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>

    <!-- Service pages -->
    <url><loc>https://www.finchmortgage.co.nz/services/home-loan.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/investment-property.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/refinance.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/pre-approval.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/first-home-buyer.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/next-home-buyer.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/self-employed.html</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/asset-finance.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/commercial-property.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/services/construction-loan.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>

    <!-- Blog posts -->
    <url><loc>https://www.finchmortgage.co.nz/blog/deposit-requirements-nz.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/blog/how-much-can-i-borrow.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/blog/interest-rates-guide.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/blog/mortgage-tips.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>

    <!-- Calculators -->
    <url><loc>https://www.finchmortgage.co.nz/calculators/mortgage-calculator.html</loc><changefreq>yearly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/calculators/borrowing-power.html</loc><changefreq>yearly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/calculators/refinance-savings.html</loc><changefreq>yearly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/calculators/extra-repayment.html</loc><changefreq>yearly</changefreq><priority>0.7</priority></url>

    <!-- Lenders -->
    <url><loc>https://www.finchmortgage.co.nz/lenders/major-banks.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/lenders/non-bank-lenders.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/lenders/credit-unions.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/lenders/specialist-lenders.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>

    <!-- Guides -->
    <url><loc>https://www.finchmortgage.co.nz/guides/how-mortgage-works.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/guides/first-home-guide.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/guides/refinance-guide.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/guides/step-by-step.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>

    <!-- Testimonials & Case Studies -->
    <url><loc>https://www.finchmortgage.co.nz/testimonials/reviews.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/testimonials/success-stories.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/case-studies/first-home-approval.html</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>

    <!-- Utility -->
    <url><loc>https://www.finchmortgage.co.nz/map.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/privacy.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>
    <url><loc>https://www.finchmortgage.co.nz/terms.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>

  </urlset>
  ```

- [ ] **Step 7.5: Create `robots.txt`**

  Create `robots.txt` at project root:

  ```
  User-agent: *
  Allow: /
  Disallow: /weekly-reports/

  User-agent: GPTBot
  Allow: /

  User-agent: ClaudeBot
  Allow: /

  User-agent: PerplexityBot
  Allow: /

  User-agent: Googlebot
  Allow: /

  Crawl-delay: 1

  Sitemap: https://www.finchmortgage.co.nz/sitemap.xml
  ```

---

## Self-Review Checklist

After all 7 tasks complete:

- [ ] Validate JSON-LD on 3 sample pages using [schema.org validator](https://validator.schema.org) — check homepage, one service page, one blog post
- [ ] Confirm `sitemap.xml` lists all 40+ pages
- [ ] Confirm `robots.txt` is at project root and allows GPTBot/ClaudeBot/PerplexityBot
- [ ] Confirm every page has `<link rel="canonical">`, `og:title`, `geo.region`, `<link rel="icon">`
- [ ] Confirm Lucide is deferred on 3 spot-check pages (index.html, one service, one blog)
- [ ] Confirm `about.html` title is no longer "Our Origins | Finch"
- [ ] Confirm entity paragraph appears in index.html footer-brand and about.html main content
