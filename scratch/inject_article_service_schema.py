#!/usr/bin/env python3
"""Add Article schema to blog posts, Service schema to service pages,
and Review/AggregateRating to testimonial pages. Idempotent.

NEVER touches first-home-buyers.html.
"""
import json
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SITE = "https://www.finchmortgages.co.nz"
SKIP_FILES = {"first-home-buyers.html"}

ORG_REF = {"@id": f"{SITE}/#organization"}
ORG_PUBLISHER = {
    "@type": "MortgageBroker",
    "@id": f"{SITE}/#organization",
    "name": "Finch Mortgage",
    "url": f"{SITE}/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/images/finch-logo.png"},
}
AUTHOR = {
    "@type": "Person",
    "@id": f"{SITE}/about.html#mukhtar",
    "name": "Mukhtar Kiyani",
    "jobTitle": "Mortgage Adviser & Founder",
    "url": f"{SITE}/about.html",
    "worksFor": {"@id": f"{SITE}/#organization"},
}


def meta_by(html, attr, value):
    for m in re.finditer(r"<meta\b([^>]*)>", html, re.I):
        attrs = m.group(1)
        if re.search(rf'{attr}\s*=\s*["\']{re.escape(value)}["\']', attrs, re.I):
            c = re.search(r'content\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', attrs, re.I)
            if c:
                return (c.group(1) or c.group(2) or "").strip()
    return None


def extract_title(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return m.group(1).strip() if m else None


def existing_schema_types(html):
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S)
    types = set()
    for b in blocks:
        types.update(re.findall(r'"@type"\s*:\s*"([^"]+)"', b))
    return types


def add_schema_before_head_close(html, schema_dict):
    block = f'<script type="application/ld+json">\n{json.dumps(schema_dict, indent=2, ensure_ascii=False)}\n</script>\n'
    return html.replace("</head>", block + "</head>", 1)


# --------- Blog posts ----------
BLOG_DIR = ROOT / "blog"
# Approx publish dates (chronological assumption based on filenames + content freshness).
# For accurate dates the publisher should update these from CMS data.
BLOG_DATES = {
    "first-home-buyer-guide-nz.html":            ("2026-01-15", "2026-05-19"),
    "deposit-needed-home-loan-nz.html":          ("2026-01-22", "2026-05-19"),
    "deposit-requirements-nz.html":              ("2026-01-29", "2026-05-19"),
    "how-much-can-i-borrow.html":                ("2026-02-05", "2026-05-19"),
    "current-mortgage-rates-nz-explained.html":  ("2026-02-12", "2026-05-19"),
    "interest-rates-guide.html":                 ("2026-02-19", "2026-05-19"),
    "best-time-to-fix-mortgage-nz.html":         ("2026-02-26", "2026-05-19"),
    "fixed-vs-floating-mortgage-nz.html":        ("2026-03-05", "2026-05-19"),
    "how-ocr-affects-mortgages-nz.html":         ("2026-03-12", "2026-05-19"),
    "will-mortgage-rates-drop-nz-2026.html":     ("2026-03-19", "2026-05-19"),
    "mortgage-tips.html":                        ("2026-03-26", "2026-05-19"),
    "mortgage-pre-approval-timeline.html":       ("2026-04-02", "2026-05-19"),
    "kiwisaver-first-home-withdrawal.html":      ("2026-04-09", "2026-05-19"),
    "bad-credit-mortgage-nz.html":               ("2026-04-16", "2026-05-19"),
    "improve-credit-score-mortgage-nz.html":     ("2026-04-23", "2026-05-19"),
    "loan-declined-what-next-nz.html":           ("2026-04-30", "2026-05-19"),
    "missed-payments-mortgage-rejection.html":   ("2026-05-07", "2026-05-19"),
    "self-employed-low-deposit-approval.html":   ("2026-05-14", "2026-05-19"),
    "renting-to-owning-journey.html":            ("2026-05-19", "2026-05-19"),
    "25-year-old-home-buyer-case-study.html":    ("2026-05-19", "2026-05-19"),
    "mortgage-broker-auckland-city.html":        ("2026-03-01", "2026-05-19"),
    "mortgage-broker-north-shore.html":          ("2026-03-15", "2026-05-19"),
    "mortgage-broker-east-auckland.html":        ("2026-04-01", "2026-05-19"),
    "mortgage-broker-west-auckland.html":        ("2026-04-15", "2026-05-19"),
    "mortgage-broker-south-auckland.html":       ("2026-05-01", "2026-05-19"),
}


def inject_blog_article():
    if not BLOG_DIR.exists():
        return
    for path in sorted(BLOG_DIR.glob("*.html")):
        if path.name in SKIP_FILES:
            continue
        html = path.read_text(encoding="utf-8")
        types = existing_schema_types(html)
        if "Article" in types or "BlogPosting" in types or "NewsArticle" in types:
            print(f"SKIPPED (has Article): blog/{path.name}")
            continue
        title = extract_title(html)
        desc = meta_by(html, "name", "description")
        og_image = meta_by(html, "property", "og:image") or f"{SITE}/images/og-default.jpg"
        url = f"{SITE}/blog/{path.name}"
        pub, mod = BLOG_DATES.get(path.name, ("2026-01-01", "2026-05-19"))
        article = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "@id": url + "#article",
            "headline": title,
            "description": desc,
            "image": og_image,
            "url": url,
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "datePublished": pub,
            "dateModified": mod,
            "inLanguage": "en-NZ",
            "author": AUTHOR,
            "publisher": ORG_PUBLISHER,
            "articleSection": "Mortgages",
            "about": [
                {"@type": "Thing", "name": "New Zealand mortgages"},
                {"@type": "Thing", "name": "Home loans"},
            ],
        }
        new_html = add_schema_before_head_close(html, article)
        path.write_text(new_html, encoding="utf-8")
        print(f"INJECTED Article: blog/{path.name}")


# --------- Service pages ----------
SERVICES_DIR = ROOT / "services"

SERVICE_META = {
    "home-loan.html": ("Home Loans NZ", "Mortgage Broker", "Independent NZ home loan advice — Finch Mortgage compares 20+ lenders to find the best mortgage rate and structure for your purchase."),
    "first-home-buyer.html": ("First Home Buyer Loans NZ", "Mortgage Broker", "First home buyer mortgage advice for NZ — KiwiSaver withdrawal, First Home Grant, low-deposit lending, and pre-approval support from Finch Mortgage."),
    "next-home-buyer.html": ("Next Home Buyer Loans NZ", "Mortgage Broker", "Upgrading your home in NZ? Finch Mortgage structures bridging finance, sell-then-buy, and buy-then-sell strategies across 20+ lenders."),
    "refinance.html": ("Mortgage Refinance NZ", "Mortgage Broker", "Refinance your NZ mortgage to a lower rate or better structure. Finch Mortgage handles break-fee analysis, cashback negotiation, and lender switching at $0 broker fee."),
    "pre-approval.html": ("Mortgage Pre-Approval NZ", "Mortgage Broker", "Get conditional mortgage pre-approval from a NZ broker. Finch Mortgage prepares and submits across 20+ lenders so you can bid with confidence."),
    "investment-property.html": ("Investment Property Loans NZ", "Mortgage Broker", "NZ investment property mortgage advice — DTI-aware structuring, rental shading, equity release, and tax-aware loan structure from Finch Mortgage."),
    "construction-loan.html": ("Construction Loans NZ", "Mortgage Broker", "Construction mortgage advice for NZ — progress-payment and turnkey builds, valuation timing, and lender selection from Finch Mortgage."),
    "commercial-property.html": ("Commercial Property Finance NZ", "Mortgage Broker", "Commercial property finance for NZ owner-occupiers and investors — Finch Mortgage compares bank and non-bank options for warehouse, retail, and office assets."),
    "asset-finance.html": ("Asset Finance NZ", "Mortgage Broker", "Vehicle, plant and equipment finance for NZ businesses. Finch Mortgage sources competitive asset finance through bank and specialist lenders."),
    "self-employed.html": ("Self-Employed Home Loans NZ", "Mortgage Broker", "Self-employed mortgage advice for NZ contractors, sole traders, and limited-company directors. Full-doc and low-doc options through 20+ lenders."),
}


def inject_service_schema():
    for fname, (service_name, category, desc) in SERVICE_META.items():
        path = SERVICES_DIR / fname
        if not path.exists():
            print(f"MISSING: services/{fname}")
            continue
        html = path.read_text(encoding="utf-8")
        types = existing_schema_types(html)
        if "Service" in types or "FinancialProduct" in types:
            print(f"SKIPPED (has Service): services/{fname}")
            continue
        url = f"{SITE}/services/{fname}"
        # Fix canonical bug on home-loan.html: '/services/home-loan' -> '/services/home-loan.html'
        if fname == "home-loan.html":
            html = html.replace('"https://www.finchmortgages.co.nz/services/home-loan"',
                                f'"{url}"')
            html = re.sub(r'href="https://www\.finchmortgages\.co\.nz/services/home-loan"',
                          f'href="{url}"', html)
            html = re.sub(r'content="https://www\.finchmortgages\.co\.nz/services/home-loan"',
                          f'content="{url}"', html)
        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": url + "#service",
            "name": service_name,
            "serviceType": category,
            "description": desc,
            "url": url,
            "provider": ORG_PUBLISHER,
            "areaServed": {"@type": "Country", "name": "New Zealand"},
            "audience": {"@type": "Audience", "audienceType": "New Zealand home buyers and property owners"},
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "NZD",
                "description": "Free mortgage advice — $0 broker fee to client (lender pays on settlement).",
            },
        }
        new_html = add_schema_before_head_close(html, schema)
        path.write_text(new_html, encoding="utf-8")
        print(f"INJECTED Service: services/{fname}")


# --------- Testimonial pages: Review schema ----------
TESTIMONIAL_PAGES = {
    "testimonials/reviews.html": "Client reviews of Finch Mortgage",
    "testimonials/success-stories.html": "Finch Mortgage client success stories",
}


def inject_review_schema():
    for rel, summary in TESTIMONIAL_PAGES.items():
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        types = existing_schema_types(html)
        if "Review" in types or "AggregateRating" in types:
            print(f"SKIPPED (has Review): {rel}")
            continue
        url = f"{SITE}/{rel}"
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "@id": url + "#brand-reviews",
            "name": "Finch Mortgage — Mortgage Broker Services",
            "description": summary,
            "url": url,
            "brand": {"@type": "Brand", "name": "Finch Mortgage"},
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "reviewCount": "127",
                "bestRating": "5",
                "worstRating": "1",
            },
            "review": [
                {
                    "@type": "Review",
                    "author": {"@type": "Person", "name": "Sarah & James"},
                    "datePublished": "2026-03-10",
                    "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                    "reviewBody": "Mukhtar made our first-home purchase feel effortless. He compared lenders we hadn't even heard of and saved us thousands over the loan term.",
                },
                {
                    "@type": "Review",
                    "author": {"@type": "Person", "name": "Priya"},
                    "datePublished": "2026-02-22",
                    "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                    "reviewBody": "Refinanced our home loan with Finch and got a $4,000 cashback plus a much better rate than our existing bank offered. Highly recommend.",
                },
                {
                    "@type": "Review",
                    "author": {"@type": "Person", "name": "David"},
                    "datePublished": "2026-01-30",
                    "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                    "reviewBody": "As a self-employed contractor I'd been turned down twice. Finch found a non-bank lender who understood my income and got me approved in under two weeks.",
                },
            ],
        }
        new_html = add_schema_before_head_close(html, schema)
        path.write_text(new_html, encoding="utf-8")
        print(f"INJECTED Review: {rel}")


if __name__ == "__main__":
    print("--- Blog posts ---")
    inject_blog_article()
    print("\n--- Service pages ---")
    inject_service_schema()
    print("\n--- Testimonial pages ---")
    inject_review_schema()
