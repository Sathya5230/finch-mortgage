#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SITE = "https://www.finchmortgages.co.nz"

ORG = {
    "@type": "MortgageBroker",
    "@id": f"{SITE}/#organization",
    "name": "Finch Mortgages",
    "url": f"{SITE}/",
    "logo": {
        "@type": "ImageObject",
        "url": f"{SITE}/images/finch-logo.png"
    }
}

AUTHOR = {
    "@type": "Person",
    "@id": f"{SITE}/about.html#mukhtar-kiyani",
    "name": "Mukhtar Kiyani",
    "jobTitle": "Director & Financial Adviser",
    "url": f"{SITE}/about.html",
    "worksFor": {
        "@id": f"{SITE}/#organization"
    }
}


def make_guide_schema(filename, title, desc, url):
    breadcrumb = {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumbs",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{SITE}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Guides",
                "item": f"{SITE}/guides/how-mortgage-works.html"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title.replace(" | Finch", "").replace(" | Finch Mortgage", "").strip(),
                "item": url
            }
        ]
    }
    
    graph = [ORG, AUTHOR, breadcrumb]
    
    if filename == "step-by-step.html":
        howto = {
            "@type": "HowTo",
            "@id": f"{url}#howto",
            "name": "NZ Home Buying: Step-by-Step Guide",
            "description": desc,
            "inLanguage": "en-NZ",
            "publisher": {
                "@id": f"{SITE}/#organization"
            },
            "author": {
                "@id": f"{SITE}/about.html#mukhtar-kiyani"
            },
            "step": [
                {
                    "@type": "HowToStep",
                    "name": "Assess Your Financial Position",
                    "text": "Understand your financial position including income, expenses, and deposit.",
                    "url": f"{url}#step1"
                },
                {
                    "@type": "HowToStep",
                    "name": "Get Pre-Approval",
                    "text": "Secure conditional commitment from a lender up to your borrowing limit.",
                    "url": f"{url}#step2"
                },
                {
                    "@type": "HowToStep",
                    "name": "Search for a Property",
                    "text": "Bid at auction or make conditional offers on target properties.",
                    "url": f"{url}#step3"
                },
                {
                    "@type": "HowToStep",
                    "name": "Make an Offer",
                    "text": "Sign a Sale and Purchase Agreement with desired conditions.",
                    "url": f"{url}#step4"
                },
                {
                    "@type": "HowToStep",
                    "name": "Full Loan Approval",
                    "text": "Lender orders property valuation and issues formal Letter of Offer.",
                    "url": f"{url}#step5"
                },
                {
                    "@type": "HowToStep",
                    "name": "Legal Process",
                    "text": "Solicitor handles LIM report and title checks, prepares mortgage transfer.",
                    "url": f"{url}#step6"
                },
                {
                    "@type": "HowToStep",
                    "name": "Settlement & Keys",
                    "text": "Funds are transferred, property title is registered, and keys are collected.",
                    "url": f"{url}#step7"
                }
            ]
        }
        graph.append(howto)
    else:
        article = {
            "@type": "Article",
            "@id": f"{url}#article",
            "headline": title.replace(" | Finch", "").replace(" | Finch Mortgage", "").strip(),
            "description": desc,
            "image": f"{SITE}/images/og-default.jpg",
            "datePublished": "2026-01-15",
            "dateModified": "2026-06-15",
            "inLanguage": "en-NZ",
            "author": {
                "@id": f"{SITE}/about.html#mukhtar-kiyani"
            },
            "publisher": {
                "@id": f"{SITE}/#organization"
            },
            "mainEntityOfPage": url
        }
        graph.append(article)
        
    schema = {
        "@context": "https://schema.org",
        "@graph": graph
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'


def make_calculator_schema(filename, title, desc, url):
    breadcrumb = {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumbs",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{SITE}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Calculators",
                "item": f"{SITE}/calculators.html"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title.replace(" | Finch", "").replace(" | Finch Mortgage", "").strip(),
                "item": url
            }
        ]
    }
    
    webapp = {
        "@type": "WebApplication",
        "@id": f"{url}#webapp",
        "url": url,
        "name": title.replace(" | Finch", "").replace(" | Finch Mortgage", "").strip(),
        "operatingSystem": "All",
        "applicationCategory": "BusinessApplication",
        "browserRequirements": "Requires JavaScript. Requires HTML5.",
        "description": desc,
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "NZD"
        },
        "publisher": {
            "@id": f"{SITE}/#organization"
        }
    }
    
    schema = {
        "@context": "https://schema.org",
        "@graph": [ORG, breadcrumb, webapp]
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'


def inject_schema_into_file(filepath: Path, make_schema_fn):
    content = filepath.read_text(encoding="utf-8")
    
    title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.I)
    title = title_match.group(1).strip() if title_match else ""
    
    desc_match = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.I)
    if not desc_match:
        desc_match = re.search(r'<meta\s+[^>]*content=["\']([^"\']+)["\']\s+[^>]*name=["\']description["\']', content, re.I)
    desc = desc_match.group(1).strip() if desc_match else ""
    
    canon_match = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content, re.I)
    if not canon_match:
        canon_match = re.search(r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', content, re.I)
    url = canon_match.group(1).strip() if canon_match else ""
    
    schema_str = make_schema_fn(filepath.name, title, desc, url)
    
    pattern = r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>'
    new_content, count = re.subn(pattern, schema_str, content, flags=re.DOTALL | re.IGNORECASE)
    if count == 0:
        new_content = content.replace("</head>", schema_str + "\n</head>", 1)
        
    filepath.write_text(new_content, encoding="utf-8")
    print(f"  Enriched schema: {filepath.relative_to(ROOT)}")


def main():
    print("Enriching Guides schemas...")
    guides_dir = ROOT / "guides"
    for path in sorted(guides_dir.glob("*.html")):
        inject_schema_into_file(path, make_guide_schema)
        
    print("\nEnriching Calculators schemas...")
    calcs_dir = ROOT / "calculators"
    for path in sorted(calcs_dir.glob("*.html")):
        inject_schema_into_file(path, make_calculator_schema)


if __name__ == "__main__":
    main()
