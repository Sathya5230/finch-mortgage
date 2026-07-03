#!/usr/bin/env python3
"""One-off fix for 10 pages whose <title> exceeded the ~60-char SERP-safe
length (measured after HTML-entity decoding). Updates <title>, og:title,
twitter:title, and any JSON-LD headline/name fields that exactly matched
the old title, so all four stay in sync.

Run once.
"""
import html
import re

FIXES = {
    "services/commercial-property.html": (
        "Commercial Property Loan NZ | Commercial Mortgage Broker | Finch",
        "Commercial Property Loan NZ | Finch Mortgages",
    ),
    "testimonials/success-stories.html": (
        "Finch Mortgages Success Stories NZ | Real Client Results | Finch",
        "Finch Mortgages Success Stories NZ | Real Results",
    ),
    "weekly-reports/week-11-first-home-grant.html": (
        "Week 11: First Home Grant Extended to 2027 | Finch Weekly Report",
        "Week 11: First Home Grant Extended to 2027 | Finch",
    ),
    "weekly-reports/week-14-anz-rates.html": (
        "Week 14: ANZ Slashes 2-Year Fixed to 5.69% | Finch Weekly Report",
        "Week 14: ANZ Slashes 2-Year Fixed to 5.69% | Finch",
    ),
    "weekly-reports/week-20-fixed-rates-dip.html": (
        "Week 20: 1-Year Fixed Rates Dip Below 5.8% | Finch Weekly Report",
        "Week 20: 1-Year Fixed Rates Dip Below 5.8% | Finch",
    ),
    "blog/mortgage-broker-orewa-hibiscus-coast.html": (
        "Mortgage Broker Orewa & the Hibiscus Coast | Finch Mortgages NZ",
        "Mortgage Broker Orewa & Hibiscus Coast | Finch Mortgages NZ",
    ),
    "blog/mortgage-broker-masterton-wairarapa.html": (
        "Mortgage Broker Masterton & the Wairarapa | Finch Mortgages NZ",
        "Mortgage Broker Masterton & Wairarapa | Finch Mortgages NZ",
    ),
    "services/asset-finance.html": (
        "Asset Finance NZ | Vehicle & Equipment Loans | Finch Mortgages",
        "Asset Finance NZ | Vehicle & Equipment Loans | Finch",
    ),
    "testimonials/reviews.html": (
        "Finch Mortgages Client Reviews NZ | 5.0★ Google Rating | Finch",
        "Finch Mortgages Client Reviews NZ | 5.0-Star Rating",
    ),
    "blog/mortgage-broker-invercargill-southland.html": (
        "Mortgage Broker Invercargill & Southland | Finch Mortgages NZ",
        "Mortgage Broker Invercargill & Southland | Finch NZ",
    ),
}


def html_variants(s: str) -> list[str]:
    """Return both the raw and entity-escaped (&amp;) forms of a string,
    since titles containing '&' are stored HTML-escaped in these files."""
    escaped = s.replace("&", "&amp;")
    return sorted({s, escaped}, key=len, reverse=True)


for path, (old, new) in FIXES.items():
    with open(path, encoding="utf-8") as f:
        content = f.read()
    orig = content
    subs = 0

    for old_variant, new_variant in zip(html_variants(old), html_variants(new)):
        n = content.count(old_variant)
        content = content.replace(old_variant, new_variant)
        subs += n

    if content == orig:
        print(f"  ! no match found in {path}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  fixed {path} ({subs} occurrence(s))")
