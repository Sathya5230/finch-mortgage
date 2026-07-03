#!/usr/bin/env python3
"""Adds datePublished/dateModified + author (E-E-A-T) fields to the schema
on services/*.html, calculators/*.html, and the 4 lenders/*.html hub pages --
the site's highest commercial-value pages, which had zero freshness or
author signals in their structured data (Service/WebApplication/WebPage
schema types don't carry these fields by default the way Article does).

AI answer engines weight freshness and attributed authorship when deciding
what to cite (see geo-fundamentals skill). This closes that gap without
touching any visible page content.

Run once. Idempotent -- skips any target type that already has datePublished.
"""
import glob
import json
import re

DATE_PUBLISHED = "2026-01-15"
DATE_MODIFIED = "2026-07-04"
AUTHOR = {
    "@type": "Person",
    "@id": "https://www.finchmortgages.co.nz/#mukhtar-kiyani",
    "name": "Mukhtar Kiyani",
    "jobTitle": "Founder & Mortgage Adviser",
    "url": "https://www.finchmortgages.co.nz/about.html",
}

# file glob -> schema @type to target within that file
TARGETS = [
    ("services/*.html", "Service"),
    ("calculators/*.html", "WebApplication"),
    ("lenders/major-banks.html", "WebPage"),
    ("lenders/non-bank-lenders.html", "WebPage"),
    ("lenders/specialist-lenders.html", "WebPage"),
    ("lenders/credit-unions.html", "WebPage"),
    ("faq.html", "FAQPage"),
    ("mortgage-rates.html", "WebPage"),
    ("first-home-buyers.html", "FinancialService"),
    ("guides/step-by-step.html", "HowTo"),
    ("map.html", "WebPage"),
    ("blog.html", "WebPage"),
    ("lenders.html", "WebPage"),
    ("case-studies.html", "WebPage"),
    ("calculators.html", "WebPage"),
    ("weekly-reports.html", "WebPage"),
    ("services-overview.html", "WebPage"),
]

# Legal/compliance pages get a dateModified freshness signal only -- attaching
# a named personal author to a privacy policy, terms, or disclosure statement
# would misrepresent authorship of an official company document.
DATE_ONLY_TARGETS = [
    ("privacy.html", "WebPage"),
    ("disclaimer.html", "WebPage"),
    ("terms.html", "WebPage"),
    ("disclosure.html", "WebPage"),
    # FinancialService/Person describe the business/founder directly --
    # "authored by" doesn't apply the way it does to an article or guide.
    ("index.html", "FinancialService"),
    ("contact.html", "FinancialService"),
    ("about.html", "Person"),
]


def type_matches(obj_type, target_type) -> bool:
    if isinstance(obj_type, list):
        return target_type in obj_type
    return obj_type == target_type


def patch_object(obj: dict, include_author: bool = True) -> bool:
    if "datePublished" in obj:
        return False
    obj["datePublished"] = DATE_PUBLISHED
    obj["dateModified"] = DATE_MODIFIED
    if include_author:
        obj["author"] = AUTHOR
    return True


def process_file(path: str, target_type: str, include_author: bool = True) -> bool:
    with open(path, encoding="utf-8") as f:
        content = f.read()

    script_re = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
    changed = False

    def repl(m):
        nonlocal changed
        raw = m.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)

        touched = False
        if isinstance(data, dict) and "@graph" in data:
            for item in data["@graph"]:
                if isinstance(item, dict) and type_matches(item.get("@type"), target_type):
                    touched = patch_object(item, include_author) or touched
        elif isinstance(data, dict) and type_matches(data.get("@type"), target_type):
            touched = patch_object(data, include_author) or touched

        if not touched:
            return m.group(0)
        changed = True
        return '<script type="application/ld+json">' + json.dumps(data, indent=2) + "</script>"

    new_content = script_re.sub(repl, content)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return changed


def main():
    total = 0
    for pattern, target_type in TARGETS:
        for path in sorted(glob.glob(pattern)):
            if process_file(path, target_type):
                print(f"  + {path} ({target_type})")
                total += 1
            else:
                print(f"  = {path} (already had dates, skipped)")
    for pattern, target_type in DATE_ONLY_TARGETS:
        for path in sorted(glob.glob(pattern)):
            if process_file(path, target_type, include_author=False):
                print(f"  + {path} ({target_type}, date-only)")
                total += 1
            else:
                print(f"  = {path} (already had dates, skipped)")
    print(f"\nPatched {total} files.")


if __name__ == "__main__":
    main()
