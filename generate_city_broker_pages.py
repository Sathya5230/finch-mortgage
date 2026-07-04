"""Generate location-based 'NZ mortgage broker [city]' pages for SEO.

Each page targets a high-search-volume NZ city/region phrase like
'mortgage broker Wellington', 'mortgage broker Christchurch' etc.

Reuses the head + footer wrappers from an existing blog page so the new
pages match the rest of the site's nav, styles, and breadcrumb structure.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "blog/mortgage-broker-north-shore.html"
OUT_DIR = ROOT / "blog"
BASE_URL = "https://www.finchmortgages.co.nz"

# ISO 8601 dates for Article schema (required for Article rich results)
ARTICLE_PUBLISHED = "2026-01-15"
ARTICLE_MODIFIED = "2026-07-03"

# Slugs to (re)generate when run directly. Keep this scoped to newly added
# entries -- existing pages accumulate hand edits (FAQ schema tweaks, freshness
# copy) after generation, and a full re-run would blow those away.
NEW_SLUGS = {
    "mortgage-broker-rotorua",
    "mortgage-broker-new-plymouth-taranaki",
    "mortgage-broker-invercargill-southland",
    "mortgage-broker-whanganui",
    "mortgage-broker-gisborne",
    "mortgage-broker-masterton-wairarapa",
    "mortgage-broker-pukekohe-franklin",
    "mortgage-broker-orewa-hibiscus-coast",
}

FAQ_SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How does a local mortgage broker help me in my region?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A local broker understands regional market conditions, localized bank valuation hurdles (like seismic registers or land classifications), and coordinates with local real estate agents and solicitors to speed up pre-approval."
      }
    },
    {
      "@type": "Question",
      "name": "Do I have to pay a fee to use a mortgage broker in NZ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. For standard residential home loans, our services are 100% free to the client. The chosen lender pays us a commission upon settlement, which doesn't increase your interest rate or loan fees."
      }
    },
    {
      "@type": "Question",
      "name": "Can a broker negotiate a better interest rate than a bank direct?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Banks reserve their sharpest rate discounts and cashback contributions for the broker channel. A broker compares 20+ lenders side-by-side to construct a competitive rate package you won't get walking in direct."
      }
    },
    {
      "@type": "Question",
      "name": "How does a family guarantee work to buy a home?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A family guarantee allows parents to secure up to 20% of your home loan against the equity in their own property. This bridges your deposit gap without requiring parents to give you cash, avoiding low-equity bank premiums."
      }
    }
  ]
}
</script>"""


from city_data import CITIES


def title_for(c: dict) -> str:
    # Kept under 60 characters so titles don't truncate in SERPs.
    if c["slug"] == "mortgage-broker-nz":
        return "Mortgage Broker NZ | Independent NZ-Wide Broker | Finch"
    return f"Mortgage Broker {c['city']} | Finch Mortgages NZ"


def description_for(c: dict) -> str:
    # Trimmed to land near the 150-160 character SERP sweet spot.
    if c["slug"] == "mortgage-broker-nz":
        return (
            "Independent NZ mortgage broker — Finch arranges home loans across 20+ NZ lenders for "
            "buyers anywhere in New Zealand. Free advice, $0 broker fee, fast pre-approvals."
        )
    return (
        f"Independent {c['city']} mortgage broker — Finch compares 20+ NZ lenders to find local "
        f"buyers the sharpest rate and structure. Free advice, $0 broker fee."
    )


def keywords_for(c: dict) -> str:
    city = c["city"].replace("&amp;", "&")
    base = [
        f"mortgage broker {city}",
        f"{city} mortgage broker",
        f"{city} home loan",
        f"home loan broker {city}",
        f"best mortgage broker {city}",
        f"{city} mortgage advice",
        f"{city} mortgage rates",
        "NZ mortgage broker",
        "independent mortgage broker NZ",
        "free mortgage broker NZ",
        "NZ home loan broker",
    ]
    return ", ".join(base)


def schema_for(c: dict) -> str:
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog.html"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"Mortgage Broker {c['city'].replace('&amp;', '&')}",
                "item": f"{BASE_URL}/blog/{c['slug']}.html",
            },
        ],
    }
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"Mortgage Broker {c['city'].replace('&amp;', '&')} — Independent NZ Advice",
        "description": description_for(c),
        "url": f"{BASE_URL}/blog/{c['slug']}.html",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}/blog/{c['slug']}.html"},
        "inLanguage": "en-NZ",
        "image": f"{BASE_URL}/images/finch-logo.png",
        "datePublished": ARTICLE_PUBLISHED,
        "dateModified": ARTICLE_MODIFIED,
        "author": {
            "@type": "Person",
            "@id": f"{BASE_URL}/#mukhtar-kiyani",
            "name": "Mukhtar Kiyani",
            "jobTitle": "Founder & Mortgage Adviser",
            "url": f"{BASE_URL}/about.html",
        },
        "publisher": {
            "@type": "MortgageBroker",
            "@id": f"{BASE_URL}/#organization",
            "name": "Finch Mortgages",
            "url": f"{BASE_URL}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/finch-logo.png"},
        },
        "about": {
            "@type": "Service",
            "name": f"Mortgage broker in {c['city'].replace('&amp;', '&')}",
            "areaServed": {"@type": "Place", "name": c["region"]},
        },
    }
    return (
        "<script type=\"application/ld+json\">"
        + json.dumps(breadcrumb, indent=2)
        + "</script>\n<script type=\"application/ld+json\">"
        + json.dumps(article, indent=2)
        + "</script>\n"
        + FAQ_SCHEMA
    )


def main_body(c: dict) -> str:
    city = c["city"]
    region = c["region"]
    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <!-- Hero -->
    <section class="container page-hero" style="padding-top:4rem;padding-bottom:4rem;">
      <div class="reveal" style="max-width:800px;">
        <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../blog.html">Blog</a><span class="breadcrumb-sep">/</span><span>Mortgage Broker {city}</span></nav>
        <div class="page-hero-tag">Local NZ Coverage · {region}</div>
        <h1>Mortgage Broker<br/><em style="font-style:italic;color:var(--finch-forest);">{city}.</em></h1>
        <p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: July 2026</p>
        <p>{c['intro_one_liner']}</p>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
          <a class="btn-primary" href="../contact.html">Book a Free 15-Minute Call</a>
          <a class="btn-secondary" href="../mortgage-rates.html">View Live NZ Rates</a>
        </div>
      </div>
    </section>

    <!-- Body -->
    <section style="padding:4rem 0;background:var(--finch-mist);">
      <div class="container" style="max-width:800px;">
        <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
          <h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Why You Need an Independent Mortgage Broker in {city}</h2>
          <p style="margin-bottom:2rem;">Walking directly into your own bank limits your options to that single lender's pricing, scorecard, and product range. As an independent NZ mortgage broker covering {region}, Finch compares your scenario across the full panel of <strong>ANZ, ASB, BNZ, Westpac, Kiwibank, TSB, SBS, The Co-operative Bank, Heartland</strong>, plus specialist non-bank lenders including <strong>Resimac, Pepper Money, Avanti Finance, Liberty Financial, Basecorp, and Bluestone</strong>. Because each NZ lender's policy, test rate, and credit appetite differs week-to-week, knowing which one wins for your specific situation can be the difference between a clean approval at a sharp rate and a frustrating decline.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{city} &amp; {region} — Local Market Notes</h3>
          <p style="margin-bottom:2rem;">{c['market_note']}</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Suburbs &amp; Areas We Cover Across {region}</h3>
          <p style="margin-bottom:2rem;">We arrange mortgages for clients across {c['suburbs']}.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Who Finch Helps in {city}</h3>
          <p style="margin-bottom:2rem;">Our typical {city} clients include {c['common_buyers']}. We work with PAYE professionals and complex self-employed scenarios alike, including LTCs, trusts, and partnership entities — and we know which NZ lender's scorecard treats each scenario most favourably.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Typical {city} Property Price Bands (2026)</h3>
          <p style="margin-bottom:2rem;">{c['price_band']}. Knowing which deposit pathway works best for each band — Kāinga Ora First Home Loan, family guarantee, new-build LVR exemption, or standard 20% deposit — is part of how we match you to the right lender.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">How the Finch Process Works for {city} Buyers</h3>
          <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style:decimal;">
            <li style="margin-bottom:0.5rem;"><strong>Free 15-minute discovery call</strong> — by phone or Zoom, no obligation.</li>
            <li style="margin-bottom:0.5rem;"><strong>Document gathering</strong> — we send you a tailored checklist for {city}.</li>
            <li style="margin-bottom:0.5rem;"><strong>Lender match</strong> — we model your scenario across every NZ lender and recommend the strongest 1-2 options.</li>
            <li style="margin-bottom:0.5rem;"><strong>Pre-approval</strong> — typically issued within 5-10 working days for clean scenarios.</li>
            <li style="margin-bottom:0.5rem;"><strong>House hunting in {city}</strong> — bid at auction or negotiate by private treaty with certainty.</li>
            <li style="margin-bottom:0.5rem;"><strong>Full approval &amp; settlement</strong> — typically 4-6 weeks from accepted offer.</li>
            <li style="margin-bottom:0.5rem;"><strong>Ongoing reviews</strong> — at every fixed-term roll-off and annually.</li>
          </ol>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">What Finch Costs (Spoiler: $0 to You)</h3>
          <p style="margin-bottom:2rem;">For residential home loans, Finch charges you nothing. We are paid by the lender on settlement — not by you. That fee comes from the bank's distribution budget and would otherwise stay with the bank if you walked in direct. Our independent broker obligations under the Financial Markets Conduct Act mean we are legally required to act in your best interest, not the lender's. We hold FSP1011206 (FSPR FSP1011125) and are subject to NZ regulatory oversight.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">First Home Buyer Support in {city}</h3>
          <p style="margin-bottom:2rem;">We specialise in helping {city} first home buyers combine every available NZ deposit pathway — KiwiSaver withdrawal (after 3 years of contributions), the <a href="https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Kāinga Ora First Home Loan</a> (5% deposit through Westpac, Kiwibank, SBS, The Co-operative Bank), family guarantees, and new-build LVR exemption set by the <a href="https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Reserve Bank's LVR rules</a>. Most first home buyers find their effective deposit goes much further than they expected once we layer these properly. Read the full <a href="../guides/first-home-guide.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">NZ first home buyer guide</a>.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Refinance &amp; Restructure for {city} Homeowners</h3>
          <p style="margin-bottom:1rem;">If your fixed term is rolling off in the next 60 days, you're paying the loyalty tax. Refinancing through Finch typically captures a sharper rate plus 0.50-0.90% cashback (up to $20,000 depending on lender and loan size). We model your full economics — break fees, cashback clawback on existing loan, new cashback, legal costs — before recommending any move. Use our <a href="../calculators/refinance-savings.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">refinance savings calculator</a> to ballpark the benefit.</p>
        </div>
      </div>
    </section>

    <!-- Related NZ Resources -->
    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>Keep Reading</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ mortgage resources</h2>
        <div class="cols-3" style="gap:1.5rem;">
          <a href="../services/home-loan.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Home Loan Service</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Independent advice across 20+ NZ lenders.</span></a>
          <a href="../calculators/borrowing-power.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Borrowing Power</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">See how much NZ banks will lend you.</span></a>
          <a href="../calculators/mortgage-calculator.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Mortgage Calculator</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Estimate repayments at NZ rates.</span></a>
          <a href="../guides/first-home-guide.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ First Home Buyer Guide</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Complete NZ FHB playbook.</span></a>
          <a href="../mortgage-rates.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Live NZ Mortgage Rates</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Current carded and broker rates.</span></a>
          <a href="../lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Lender Directory</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">All 20+ NZ lenders reviewed.</span></a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section style="padding:5rem 0;">
      <div class="container">
        <div class="cta-section reveal">
          <h2>Ready to talk to a<br/>{city} mortgage broker?</h2>
          <p>Book a free 15-minute consultation. No obligation, no cost — just honest NZ-specific advice.</p>
          <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
            <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
            <a class="btn-cta-outline" href="../mortgage-rates.html">View Live NZ Rates</a>
          </div>
        </div>
      </div>
    </section>
    </main>
    """)


def build_page(c: dict, template_text: str) -> str:
    head_close = template_text.find("</head>")
    head = template_text[:head_close]

    title = title_for(c)
    description = description_for(c)
    canonical = f"{BASE_URL}/blog/{c['slug']}.html"
    keywords = keywords_for(c)
    schema = schema_for(c)

    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"description\"/?>',
        f'<meta content="{description}" name="description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<link href=\"https://www\.finchmortgages\.co\.nz/blog/[^\"]+\" rel=\"canonical\"/?>',
        f'<link href="{canonical}" rel="canonical"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:title\"/?>',
        f'<meta content="{title}" property="og:title"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:description\"/?>',
        f'<meta content="{description}" property="og:description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:url\"/?>',
        f'<meta content="{canonical}" property="og:url"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"twitter:title\"/?>',
        f'<meta content="{title}" name="twitter:title"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"twitter:description\"/?>',
        f'<meta content="{description}" name="twitter:description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"keywords\"/?>',
        f'<meta content="{keywords}" name="keywords"/>',
        head,
    )
    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        lambda _m: schema,
        head,
        count=1,
        flags=re.S,
    )
    head += "</head>"

    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]

    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]

    return head + "\n" + body_open + main_body(c) + footer


def main() -> None:
    template_text = TEMPLATE.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    targets = [c for c in CITIES if c["slug"] in NEW_SLUGS]
    for c in targets:
        out_path = OUT_DIR / f"{c['slug']}.html"
        out_path.write_text(build_page(c, template_text), encoding="utf-8")
        print(f"  + {out_path.relative_to(ROOT)}")

    print()
    print(f"Generated {len(targets)} city broker pages.")


if __name__ == "__main__":
    main()
