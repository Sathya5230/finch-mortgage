#!/usr/bin/env python3
"""Generate high-intent NZ mortgage blog posts for local SEO and lead capture.

Three content groups, chosen to avoid cannibalising the 50 existing topic posts:
  A. Region-specific lending obstacles (Auckland leasehold, Wellington EPB,
     Canterbury TC zoning, flood zones, Waikato lifestyle blocks, Queenstown
     short-stay, Healthy Homes)
  B. Debt and income blockers (student loan, BNPL, car debt, parental leave,
     casual income, offshore income, one year self-employed)
  C. Transaction-moment topics (finance condition, expired pre-approval, off
     the plans, LIM and builder's reports, buying from family)

Head/footer wrappers come from an existing blog page so nav, footer NAP and
tracking stay consistent. The lead form is imported from inject_local_seo.py
so the markup has a single source of truth.

Compliance: explains mechanisms only. No invented rates, no named lender
policies, no approval-odds claims — per context/brand-voice.md.

Run:  python3 generate_local_intent_blogs.py [posts_module]   (default: local_intent_posts)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from inject_local_seo import BIZ, lead_form_block

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "blog/mortgage-tips.html"
OUT_DIR = ROOT / "blog"
BASE_URL = "https://www.finchmortgages.co.nz"

ARTICLE_PUBLISHED = "2026-10-03"
ARTICLE_MODIFIED = "2026-10-03"

FOREST = "var(--finch-forest)"
INK = "var(--neutral-black)"


# ---------------------------------------------------------------------------
# Content helpers — keep the post bodies readable and the markup consistent
# ---------------------------------------------------------------------------

def p(text: str) -> str:
    return f'<p style="margin-bottom:1.25rem;">{text}</p>'


def ul(items: list[str]) -> str:
    lis = "".join(
        f'<li style="margin-bottom:0.6rem;">{i}</li>' for i in items
    )
    return f'<ul style="margin:0 0 1.5rem;padding-left:1.4rem;list-style:disc;">{lis}</ul>'


def ol(items: list[str]) -> str:
    lis = "".join(
        f'<li style="margin-bottom:0.75rem;">{i}</li>' for i in items
    )
    return f'<ol style="margin:0 0 1.5rem;padding-left:1.5rem;list-style:decimal;">{lis}</ol>'


def callout(heading: str, text: str) -> str:
    return (
        '<div style="background:white;border-left:3px solid '
        f'{FOREST};border-radius:0 0.75rem 0.75rem 0;padding:1.25rem 1.5rem;margin:0 0 1.5rem;">'
        f'<strong style="display:block;color:{FOREST};margin-bottom:0.4rem;">{heading}</strong>'
        f'<span style="font-size:0.97rem;">{text}</span></div>'
    )


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(
        '<th style="text-align:left;padding:0.7rem 0.9rem;border-bottom:2px solid '
        f'rgba(16,68,62,0.25);font-size:0.85rem;color:{INK};">{h}</th>'
        for h in headers
    )
    body = ""
    for r in rows:
        cells = "".join(
            '<td style="padding:0.7rem 0.9rem;border-bottom:1px solid rgba(180,178,169,0.3);'
            'font-size:0.93rem;vertical-align:top;">' + c + "</td>"
            for c in r
        )
        body += f"<tr>{cells}</tr>"
    return (
        '<div style="overflow-x:auto;margin:0 0 1.5rem;">'
        '<table style="width:100%;border-collapse:collapse;min-width:30rem;background:white;'
        'border-radius:0.5rem;">'
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def link(href: str, text: str) -> str:
    return (
        f'<a href="{href}" style="color:{FOREST};text-decoration:underline;'
        f'font-weight:600;">{text}</a>'
    )


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def schema_for(post: dict) -> str:
    url = f"{BASE_URL}/blog/{post['slug']}.html"
    graph = [
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog.html"},
                {"@type": "ListItem", "position": 3, "name": post["h1"], "item": url},
            ],
        },
        {
            "@type": "BlogPosting",
            "@id": f"{url}#article",
            "headline": post["title"],
            "description": post["description"],
            "url": url,
            "mainEntityOfPage": {"@id": f"{url}#article"},
            "inLanguage": "en-NZ",
            "image": f"{BASE_URL}/images/finch-logo.png",
            "datePublished": post.get("published", ARTICLE_PUBLISHED),
            "dateModified": post.get("published", ARTICLE_MODIFIED),
            "articleSection": post.get("section_label", "Mortgages"),
            "keywords": ", ".join(post["keywords"]),
            "author": {
                "@type": "Person",
                "@id": f"{BASE_URL}/about.html#mukhtar",
                "name": "Mukhtar Kiyani",
                "jobTitle": "Mortgage Adviser & Founder",
                "url": f"{BASE_URL}/about.html",
                "worksFor": {"@id": f"{BASE_URL}/#organization"},
            },
            "publisher": {"@id": f"{BASE_URL}/#organization"},
            "about": [{"@type": "Thing", "name": t} for t in post.get("about", ["New Zealand mortgages"])],
        },
        {
            "@type": ["MortgageBroker", "FinancialService"],
            "@id": f"{BASE_URL}/#organization",
            "name": BIZ["name"],
            "legalName": BIZ["legal_name"],
            "url": f"{BASE_URL}/",
            "logo": f"{BASE_URL}/images/finch-logo.png",
            "telephone": BIZ["phone_e164"],
            "email": BIZ["email"],
            "priceRange": "Free — no broker fee",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": BIZ["street"],
                "addressLocality": BIZ["suburb"],
                "addressRegion": BIZ["city"],
                "postalCode": BIZ["postcode"],
                "addressCountry": BIZ["country"],
            },
            "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        },
        {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": post["lead_service"],
            "serviceType": post["lead_service"],
            "provider": {"@id": f"{BASE_URL}/#organization"},
            "areaServed": (
                [{"@type": "Place", "name": post["region"],
                  "containedInPlace": {"@type": "Country", "name": "New Zealand"}}]
                if post.get("region") else
                [{"@type": "Country", "name": "New Zealand"}]
            ),
            "offers": {
                "@type": "Offer", "price": "0", "priceCurrency": "NZD",
                "description": "No broker fee — the lender pays our commission on settlement.",
            },
        },
    ]
    if post.get("faqs"):
        graph.append({
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in post["faqs"]
            ],
        })
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph},
                         ensure_ascii=False, indent=2)
            + "</script>")


def faq_html(faqs: list[tuple[str, str]], heading: str) -> str:
    if not faqs:
        return ""
    items = ""
    for q, a in faqs:
        items += f"""
    <div class="faq-item" style="border:1px solid rgba(180,178,169,0.2);border-radius:1rem;background:white;overflow:hidden;">
      <button class="faq-trigger" style="width:100%;text-align:left;padding:1.25rem 1.5rem;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:1.05rem;background:none;border:none;cursor:pointer;color:var(--neutral-black);">
        <span>{q}</span>
        <svg fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" style="transition:transform 0.3s;" viewbox="0 0 24 24" width="16"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </button>
      <div class="faq-content" style="display:none;padding:0 1.5rem 1.25rem 1.5rem;color:var(--neutral-medGray);line-height:1.7;font-size:0.95rem;border-top:1px solid rgba(180,178,169,0.1);padding-top:1rem;">
        <p>{a}</p>
      </div>
    </div>"""
    return f"""
  <section style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:800px;">
      <h2 id="faq-section" style="font-family:var(--font-display);font-size:2rem;color:var(--neutral-black);margin-bottom:1.5rem;text-align:center;">{heading}</h2>
      <div class="faq-accordion" style="display:flex;flex-direction:column;gap:1rem;">{items}
      </div>
    </div>
  </section>"""


def related_html(post: dict) -> str:
    cards = ""
    for href, title, blurb in post["related"]:
        cards += (
            f'<a href="{href}" style="display:block;padding:1.5rem;background:var(--finch-mist);'
            'border-radius:1rem;text-decoration:none;color:var(--neutral-black);">'
            f'<strong style="display:block;color:{FOREST};margin-bottom:0.5rem;">{title}</strong>'
            f'<span style="font-size:0.9rem;color:var(--neutral-medGray);">{blurb}</span></a>'
        )
    return f"""
  <section style="padding:4rem 0;background:white;border-top:1px solid rgba(180,178,169,0.15);">
    <div class="container" style="max-width:1000px;">
      <div class="section-label"><span>Keep Reading</span></div>
      <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ mortgage resources</h2>
      <div class="cols-3" style="gap:1.5rem;">{cards}</div>
    </div>
  </section>"""


def main_body(post: dict) -> str:
    sections = ""
    for heading, body in post["sections"]:
        sections += (
            f'<h2 style="font-size:1.6rem;font-weight:700;color:{INK};margin-bottom:1rem;'
            f'margin-top:2.5rem;font-family:var(--font-display);">{heading}</h2>\n{body}\n'
        )

    form = lead_form_block(
        post["cta_heading"],
        post["cta_sub"],
        post["lead_service"],
        post.get("region") or "",
        f"blog-{post['slug']}",
    )

    return f"""
<main style="padding-top:80px;">
  <section class="container page-hero" style="padding-top:4rem;padding-bottom:3rem;">
    <div class="reveal" style="max-width:800px;">
      <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../blog.html">Blog</a><span class="breadcrumb-sep">/</span><span>{post['h1']}</span></nav>
      <div class="page-hero-tag">{post.get('section_label', 'NZ Mortgage Guide')}</div>
      <h1>{post['h1']}</h1>
      <p style="font-size:1.15rem;color:var(--neutral-medGray);line-height:1.7;margin-bottom:0;font-style:italic;">{post['intro_pull']}</p>
    </div>
  </section>

  <section style="padding:3rem 0;background:var(--finch-mist);">
    <div class="container" style="max-width:800px;">
      <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
{sections}
        <p style="margin-top:2.5rem;font-size:0.92rem;color:var(--neutral-warmGray);">This article explains how New Zealand lenders generally assess these situations. It is general information, not personalised financial advice, and lender policy changes often — check your own position with a registered adviser. Official sources: {link('https://www.rbnz.govt.nz/', 'Reserve Bank of New Zealand')} for lending policy and the OCR, and {link('https://sorted.org.nz/guides/', 'Sorted.org.nz')} for independent government-backed money guidance.</p>
      </div>
    </div>
  </section>
{faq_html(post.get('faqs', []), post.get('faq_heading', 'Common questions'))}
{form}
{related_html(post)}
</main>
"""


def build_page(post: dict, template_text: str) -> str:
    head = template_text[: template_text.find("</head>")]
    url = f"{BASE_URL}/blog/{post['slug']}.html"

    subs = [
        (r"<title>.*?</title>", f"<title>{post['title']}</title>"),
        (r'<meta content="[^"]*" name="description"/?>',
         f'<meta content="{post["description"]}" name="description"/>'),
        (r'<link href="https://www\.finchmortgages\.co\.nz/blog/[^"]+" rel="canonical"/?>',
         f'<link href="{url}" rel="canonical"/>'),
        (r'<link href="https://www\.finchmortgages\.co\.nz/blog/[^"]+" hreflang="en-NZ" rel="alternate"/?>',
         f'<link href="{url}" hreflang="en-NZ" rel="alternate"/>'),
        (r'<link href="https://www\.finchmortgages\.co\.nz/blog/[^"]+" hreflang="x-default" rel="alternate"/?>',
         f'<link href="{url}" hreflang="x-default" rel="alternate"/>'),
        (r'<meta content="[^"]*" property="og:title"/?>',
         f'<meta content="{post["title"]}" property="og:title"/>'),
        (r'<meta content="[^"]*" property="og:description"/?>',
         f'<meta content="{post["description"]}" property="og:description"/>'),
        (r'<meta content="[^"]*" property="og:url"/?>',
         f'<meta content="{url}" property="og:url"/>'),
        (r'<meta content="[^"]*" name="twitter:title"/?>',
         f'<meta content="{post["title"]}" name="twitter:title"/>'),
        (r'<meta content="[^"]*" name="twitter:description"/?>',
         f'<meta content="{post["description"]}" name="twitter:description"/>'),
        (r'<meta content="[^"]*" name="keywords"/?>',
         f'<meta content="{", ".join(post["keywords"])}" name="keywords"/>'),
    ]
    for pat, repl in subs:
        head = re.sub(pat, lambda _m, r=repl: r, head, count=1, flags=re.S)

    # Replace every template JSON-LD block with this post's single graph.
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    head += schema_for(post) + "\n"

    # Per-region geo meta where the topic is regional.
    if post.get("region"):
        head = re.sub(r'<meta content="[^"]*" name="geo\.placename"/?>',
                      f'<meta content="{post["region"]}, New Zealand" name="geo.placename"/>',
                      head, count=1)
    head = re.sub(r"</head>\s*$", "", head)
    head += (f'<meta content="{post["lead_service"]}" name="finch:service"/>\n'
             f'<meta content="{post.get("region") or ""}" name="finch:city"/>\n</head>')

    body_open = template_text[template_text.find("<body>"): template_text.find("<main")]
    footer = template_text[template_text.find("</main>") + len("</main>"):]
    return head + "\n" + body_open + main_body(post) + footer


def main() -> None:
    import importlib
    import sys
    # Post batches live in separate data modules; default is the original local-intent set.
    POSTS = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "local_intent_posts").POSTS

    template_text = TEMPLATE.read_text(encoding="utf-8")
    slugs = set()
    for post in POSTS:
        assert post["slug"] not in slugs, f"duplicate slug {post['slug']}"
        slugs.add(post["slug"])
        out = OUT_DIR / f"{post['slug']}.html"
        existed = out.exists()
        out.write_text(build_page(post, template_text), encoding="utf-8")
        print(f"  {'~' if existed else '+'} blog/{post['slug']}.html")
    print(f"\nGenerated {len(POSTS)} posts.")


if __name__ == "__main__":
    main()
