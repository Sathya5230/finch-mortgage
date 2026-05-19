#!/usr/bin/env python3
"""Inject JSON-LD schema into schema-less pages. Idempotent.

NEVER touches first-home-buyers.html.
"""
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SITE = "https://www.finchmortgages.co.nz"
SKIP_FILES = {"first-home-buyers.html"}

ORG = {
    "@type": "MortgageBroker",
    "@id": f"{SITE}/#organization",
    "name": "Finch Mortgage",
    "alternateName": "Finch Mortgages",
    "url": f"{SITE}/",
    "logo": f"{SITE}/images/finch-logo.png",
    "image": f"{SITE}/images/finch-logo.png",
    "telephone": "+64273433293",
    "email": "Mukhtar@finchmortgages.co.nz",
    "priceRange": "$0 broker fee",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "17a Marlene Ave",
        "addressLocality": "Te Atatu South",
        "addressRegion": "Auckland",
        "postalCode": "0610",
        "addressCountry": "NZ",
    },
    "areaServed": {"@type": "Country", "name": "New Zealand"},
    "founder": {"@type": "Person", "name": "Mukhtar Kiyani"},
    "foundingDate": "2010",
    "sameAs": [
        f"{SITE}/about.html",
        f"{SITE}/contact.html",
    ],
}


# --- Page schema configs ----------------------------------------------------
# Each entry: schema graph for the page. Built dynamically below.

def breadcrumbs(items):
    """items = [(name, url_or_None)]"""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                **({"item": url} if url else {}),
            }
            for i, (name, url) in enumerate(items)
        ],
    }


def webpage(url, name, description, breadcrumb=None, extras=None):
    page = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": name,
        "description": description,
        "inLanguage": "en-NZ",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "publisher": {"@id": f"{SITE}/#organization"},
    }
    if breadcrumb:
        page["breadcrumb"] = {"@id": url + "#breadcrumbs"}
    if extras:
        page.update(extras)
    return page


def website():
    return {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": "Finch Mortgage",
        "publisher": {"@id": f"{SITE}/#organization"},
        "inLanguage": "en-NZ",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{SITE}/blog.html?q={{search_term_string}}",
            },
            "query-input": "required name=search_term_string",
        },
    }


def graph(entities):
    return {"@context": "https://schema.org", "@graph": entities}


# --- Per-page schema builders -----------------------------------------------

def build_blog_html():
    url = f"{SITE}/blog.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Blog", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "NZ Mortgage Blog — Expert Guides & Rate Updates",
                   "Expert NZ mortgage guides, interest rate updates, first home buyer tips, and refinancing advice from Finch Mortgage. Updated regularly for 2026.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    return graph([ORG, website(), bc, page])


def build_calculators_html():
    url = f"{SITE}/calculators.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Calculators", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Free NZ Mortgage Calculators",
                   "Free NZ mortgage calculators — repayment, borrowing power, refinance savings, and extra repayment tools. No sign-up required.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    return graph([ORG, website(), bc, page])


def build_case_studies_html():
    url = f"{SITE}/case-studies.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Case studies", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Mortgage Case Studies NZ — Real Client Success Stories",
                   "Real NZ mortgage case studies — first home buyers, refinancing, self-employed approvals, construction loans, and investment property success stories from Finch Mortgage clients.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    return graph([ORG, website(), bc, page])


def build_lenders_html():
    url = f"{SITE}/lenders.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Lenders", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "NZ Mortgage Lenders — Compare Banks & Non-Banks",
                   "Compare 20+ NZ mortgage lenders — ANZ, BNZ, Kiwibank, ASB, Westpac, credit unions, and specialist lenders. Finch finds the best home loan rate for your situation.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    return graph([ORG, website(), bc, page])


def build_mortgage_rates_html():
    url = f"{SITE}/mortgage-rates.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Mortgage rates", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Current NZ Mortgage Rates — Compare ANZ, BNZ, Kiwibank",
                   "Compare today's NZ mortgage rates across ANZ, BNZ, Kiwibank, ASB, Westpac and more. OCR updates, rate trends, and expert analysis — updated weekly by Finch Mortgage.",
                   breadcrumb=True,
                   extras={"@type": ["WebPage"], "datePublished": "2024-01-01", "dateModified": "2026-05-19"})
    return graph([ORG, website(), bc, page])


def build_refinance_html():
    url = f"{SITE}/refinance.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Refinance", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Refinance Calculator NZ — Should You Refinance?",
                   "Use Finch Mortgage's free NZ refinance tool to see if refinancing makes sense for your situation. Compare current rates and calculate potential savings.",
                   breadcrumb=True)
    service = {
        "@type": "Service",
        "serviceType": "Mortgage refinance advisory",
        "provider": {"@id": f"{SITE}/#organization"},
        "areaServed": {"@type": "Country", "name": "New Zealand"},
        "name": "Mortgage Refinance NZ",
        "description": "Independent NZ mortgage refinance advice — compare 20+ lenders, calculate break fees, negotiate cashback, and switch with no broker fee.",
        "url": url,
    }
    return graph([ORG, website(), bc, page, service])


def build_market_report_html():
    url = f"{SITE}/market-report.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Market report", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "NZ Mortgage Market Report — Weekly Rate Insights",
                   "Weekly NZ mortgage market report — OCR moves, bank rate changes, property market trends, and lender activity. Expert analysis from Finch Mortgage.",
                   breadcrumb=True,
                   extras={"@type": ["WebPage"], "datePublished": "2024-01-01", "dateModified": "2026-05-19"})
    return graph([ORG, website(), bc, page])


def build_services_overview_html():
    url = f"{SITE}/services-overview.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Services", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "NZ Mortgage Services — Home Loans, Refinance & More",
                   "Every mortgage solution under one roof: home loans, first home buyer loans, refinancing, investment property, construction, commercial, asset finance, and self-employed lending.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    return graph([ORG, website(), bc, page])


def build_testimonials_html():
    url = f"{SITE}/testimonials.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Testimonials", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Finch Mortgage Client Reviews & Testimonials",
                   "Read genuine reviews from Finch Mortgage clients across New Zealand — first home buyers, refinancers, investors, and self-employed borrowers share their experiences.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    # Add aggregateRating on the Organization
    org_with_rating = dict(ORG)
    org_with_rating["aggregateRating"] = {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "127",
        "bestRating": "5",
        "worstRating": "1",
    }
    return graph([org_with_rating, website(), bc, page])


def build_weekly_reports_html():
    url = f"{SITE}/weekly-reports.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Weekly reports", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Weekly NZ Mortgage Market Reports",
                   "Weekly NZ mortgage market reports — OCR commentary, fixed/floating rate moves, lender promotions, and Auckland property market trends.",
                   breadcrumb=True,
                   extras={"@type": ["CollectionPage", "WebPage"]})
    return graph([ORG, website(), bc, page])


def build_map_html():
    url = f"{SITE}/map.html"
    bc = breadcrumbs([("Home", f"{SITE}/"), ("Find us", url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, "Find Finch Mortgage NZ — Auckland Office",
                   "Find Finch Mortgage's Auckland office. NZ mortgage broker serving all of New Zealand. Get directions and book a free in-person consultation.",
                   breadcrumb=True)
    org_with_geo = dict(ORG)
    org_with_geo["geo"] = {"@type": "GeoCoordinates", "latitude": -36.8509, "longitude": 174.7645}
    org_with_geo["hasMap"] = "https://www.google.com/maps?q=17a+Marlene+Ave,+Te+Atatu+South,+Auckland"
    return graph([org_with_geo, website(), bc, page])


def build_legal(slug, name):
    url = f"{SITE}/{slug}"
    bc = breadcrumbs([("Home", f"{SITE}/"), (name, url)])
    bc["@id"] = url + "#breadcrumbs"
    page = webpage(url, f"{name} | Finch Mortgage NZ",
                   f"{name} for Finch Mortgage NZ.",
                   breadcrumb=True)
    return graph([ORG, website(), bc, page])


def build_thank_you(slug):
    url = f"{SITE}/{slug}"
    page = webpage(url, "Thank You — Finch Mortgage NZ",
                   "Thank you for contacting Finch Mortgage. We will be in touch shortly with next steps for your home loan consultation.")
    return graph([ORG, page])


PAGES = {
    "blog.html": build_blog_html,
    "calculators.html": build_calculators_html,
    "case-studies.html": build_case_studies_html,
    "lenders.html": build_lenders_html,
    "mortgage-rates.html": build_mortgage_rates_html,
    "refinance.html": build_refinance_html,
    "market-report.html": build_market_report_html,
    "services-overview.html": build_services_overview_html,
    "testimonials.html": build_testimonials_html,
    "weekly-reports.html": build_weekly_reports_html,
    "map.html": build_map_html,
    "disclaimer.html": lambda: build_legal("disclaimer.html", "Website Disclaimer"),
    "disclosure.html": lambda: build_legal("disclosure.html", "Publicly Available Disclosure Statement"),
    "privacy.html": lambda: build_legal("privacy.html", "Privacy Policy"),
    "terms.html": lambda: build_legal("terms.html", "Terms & Conditions"),
    "fhb-disclaimer.html": lambda: build_legal("disclaimer.html", "Website Disclaimer"),
    "fhb-disclosure.html": lambda: build_legal("disclosure.html", "Publicly Available Disclosure Statement"),
    "fhb-privacy.html": lambda: build_legal("privacy.html", "Privacy Policy"),
    "fhb-terms.html": lambda: build_legal("terms.html", "Terms & Conditions"),
    "thank-you.html": lambda: build_thank_you("thank-you.html"),
    "fhb-thank-you.html": lambda: build_thank_you("fhb-thank-you.html"),
}


def has_jsonld(html):
    return bool(re.search(r'<script[^>]+type=["\']application/ld\+json', html, re.I))


def inject(path: Path, schema_dict):
    import json
    if path.name in SKIP_FILES:
        return "SKIPPED (protected file)"
    html = path.read_text(encoding="utf-8")
    if has_jsonld(html):
        return "SKIPPED (already has JSON-LD)"
    block = f'<script type="application/ld+json">\n{json.dumps(schema_dict, indent=2, ensure_ascii=False)}\n</script>\n'
    if "</head>" not in html:
        return "ERROR (no </head>)"
    new_html = html.replace("</head>", block + "</head>", 1)
    path.write_text(new_html, encoding="utf-8")
    return "INJECTED"


def main():
    for rel, builder in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING: {rel}")
            continue
        schema = builder()
        status = inject(path, schema)
        print(f"{status}: {rel}")


if __name__ == "__main__":
    main()
