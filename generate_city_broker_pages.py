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
ARTICLE_PUBLISHED = "2026-10-06"
ARTICLE_MODIFIED = "2026-10-06"

# Slugs to (re)generate when run directly. Keep this scoped to newly added
# entries -- existing pages accumulate hand edits (FAQ schema tweaks, freshness
# copy) after generation, and a full re-run would blow those away.
NEW_SLUGS = {
    "mortgage-broker-lower-hutt",
    "mortgage-broker-upper-hutt",
    "mortgage-broker-porirua",
    "mortgage-broker-kapiti-coast",
    "mortgage-broker-hastings",
    "mortgage-broker-mount-maunganui-papamoa",
    "mortgage-broker-taupo",
    "mortgage-broker-timaru",
    "mortgage-broker-blenheim-marlborough",
    "mortgage-broker-cambridge",
    "mortgage-broker-rolleston-selwyn",
    "mortgage-broker-rangiora-kaiapoi",
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
        "text": "A local broker knows how lenders view your area, including valuation issues such as earthquake-prone buildings or land classifications, and works with local agents and lawyers to keep your purchase on track."
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
        "text": "Often, yes. A broker can compare offers from many lenders at once and ask them to sharpen their pricing. Sometimes your own bank's offer is the best one, and a good broker will tell you so."
      }
    },
    {
      "@type": "Question",
      "name": "How does a family guarantee work to buy a home?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A family guarantee lets a family member use the equity in their own home as extra security for part of your loan. It can cover a deposit gap without them handing over cash, and may help you avoid low-equity charges."
      }
    }
  ]
}
</script>"""


from city_data import CITIES
from fix_city_page_heads import fix_head


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
            "@type": "FinancialService",
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


H3 = 'style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;"'
LINK = 'style="color:var(--finch-forest);text-decoration:underline;font-weight:600;"'


def optional_sections(c: dict) -> str:
    # Newer towns omit price_band: we only publish price figures we can source.
    city = c["city"]
    out = []
    if c.get("lending_note"):
        out.append(f'<h3 {H3}>What NZ Lenders Look At in {city}</h3>\n'
                   f'          <p style="margin-bottom:2rem;">{c["lending_note"]}</p>')
    if c.get("price_band"):
        out.append(f'<h3 {H3}>Typical {city} Property Price Bands (2026)</h3>\n'
                   f'          <p style="margin-bottom:2rem;">{c["price_band"]}. These are indicative ranges only, not valuations. Your price range affects which deposit option suits you best, whether that\'s the First Home Loan, a family guarantee, a new build or a standard 20% deposit.</p>')
    if c.get("parent_slug"):
        out.append(f'<p style="margin-bottom:2rem;">Looking more widely? See our <a href="{c["parent_slug"]}.html" {LINK}>{c["parent_label"]}</a> page for the surrounding region.</p>')
    return "\n\n          ".join(out) + ("\n" if out else "")


def main_body(c: dict) -> str:
    city = c["city"]
    region = c["region"]
    # Regions like "Hamilton &amp; Waikato" already start with the city name.
    market_heading = region if region.startswith(city) else f"{city} &amp; {region}"
    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <!-- Hero -->
    <section class="container page-hero" style="padding-top:4rem;padding-bottom:4rem;">
      <div class="reveal" style="max-width:800px;">
        <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../blog.html">Blog</a><span class="breadcrumb-sep">/</span><span>Mortgage Broker {city}</span></nav>
        <div class="page-hero-tag">Local NZ Coverage · {region}</div>
        <h1>Mortgage Broker<br/><em style="font-style:italic;color:var(--finch-forest);">{city}.</em></h1>
        <p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: October 2026</p>
        <p>{c['intro_one_liner']}</p>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
          <a class="btn-primary" href="../contact.html">Book a Free 15-Minute Call</a>
          <a class="btn-secondary" href="../mortgage-rates.html">View NZ Rates</a>
        </div>
      </div>
    </section>

    <!-- Body -->
    <section style="padding:4rem 0;background:var(--finch-mist);">
      <div class="container" style="max-width:800px;">
        <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
          <h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Why You Need an Independent Mortgage Broker in {city}</h2>
          <p style="margin-bottom:2rem;">If you go straight to your own bank, you only see that bank's rates and lending rules. As an independent mortgage broker covering {region}, Finch compares your situation across our <a href="../lenders.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">panel of 23 lenders</a>. That includes banks such as <strong>ANZ, BNZ, SBS Bank, The Co-operative Bank and Heartland Bank</strong>, and specialist lenders such as <strong>Pepper Money, Avanti Finance, Liberty Financial and Basecorp Finance</strong>. Lenders change their rules and rates often, and the right choice can mean a quick approval at a good rate instead of a decline.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{market_heading} — Local Market Notes</h3>
          <p style="margin-bottom:2rem;">{c['market_note']}</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Suburbs &amp; Areas We Cover Across {region}</h3>
          <p style="margin-bottom:2rem;">We arrange mortgages for clients across {c['suburbs']}.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Who Finch Helps in {city}</h3>
          <p style="margin-bottom:2rem;">Our typical {city} clients include {c['common_buyers']}. We help salary and wage earners and self-employed people alike, including those trading through companies, look-through companies (LTCs), trusts and partnerships. We know which lenders are most likely to approve each kind of income.</p>

          {optional_sections(c)}
          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">How the Finch Process Works for {city} Buyers</h3>
          <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style:decimal;">
            <li style="margin-bottom:0.5rem;"><strong>Free 15-minute discovery call</strong> — by phone or Zoom, no obligation.</li>
            <li style="margin-bottom:0.5rem;"><strong>Document gathering</strong> — we send you a tailored checklist for {city}.</li>
            <li style="margin-bottom:0.5rem;"><strong>Lender match</strong> — we compare your situation across our lender panel and recommend the best one or two options.</li>
            <li style="margin-bottom:0.5rem;"><strong>Pre-approval</strong> — typically issued within 5-10 working days for clean scenarios.</li>
            <li style="margin-bottom:0.5rem;"><strong>House hunting in {city}</strong> — bid at auction or negotiate by private treaty with certainty.</li>
            <li style="margin-bottom:0.5rem;"><strong>Full approval &amp; settlement</strong> — typically 4-6 weeks from accepted offer.</li>
            <li style="margin-bottom:0.5rem;"><strong>Ongoing reviews</strong> — at every fixed-term roll-off and annually.</li>
          </ol>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">What Finch Costs (Spoiler: $0 to You)</h3>
          <p style="margin-bottom:2rem;">For residential home loans, Finch charges you nothing. The lender pays us a commission when your loan settles, and we disclose it in writing before you act on our advice. New Zealand law requires financial advisers to put your interests first. Finch Mortgages (FSP1011125) is an Authorised Body under the Financial Advice Provider licence held by Finsure New Zealand Limited (FSP1005389). Read our <a href="../disclosure.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">disclosure statement</a>.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">First Home Buyer Support in {city}</h3>
          <p style="margin-bottom:2rem;">We help {city} first home buyers make the most of every deposit option. That can include a KiwiSaver withdrawal (once you've been a member for three years), the <a href="https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Kāinga Ora First Home Loan</a> (from a 5% deposit, through participating lenders), a family guarantee, or the new-build exemption under the <a href="https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Reserve Bank's LVR rules</a>. Used together, these often stretch a deposit further than people expect. Read the full <a href="../guides/first-home-guide.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">NZ first home buyer guide</a>.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Refinance &amp; Restructure for {city} Homeowners</h3>
          <p style="margin-bottom:1rem;">If your fixed term ends in the next 60 days, it's a good time to check whether your bank's renewal offer is competitive. Some lenders offer cashback when you switch, but it usually comes with conditions, and leaving early can mean break fees or repaying an earlier cashback. We work out the full cost before recommending any move. Use our <a href="../calculators/refinance-savings.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">refinance savings calculator</a> for a quick estimate.</p>
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
          <a href="../mortgage-rates.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Mortgage Rates</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Current carded and broker rates.</span></a>
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
            <a class="btn-cta-outline" href="../mortgage-rates.html">View NZ Rates</a>
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

    return fix_head(head + "\n" + body_open + main_body(c) + footer, f"{c['slug']}.html")


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
