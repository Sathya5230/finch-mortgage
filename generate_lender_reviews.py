"""Generate 25 individual NZ-lender review pages for SEO.

Each page targets a specific NZ bank or non-bank lender (eg ANZ, BNZ, Resimac)
and is hand-crafted with NZ-specific positioning, pros/cons, and product detail.

The script reuses the exact <head> and footer wrappers from an existing lender
hub page so navigation, styles, and breadcrumb structure stay consistent.

Idempotent: re-run any time to regenerate or refresh pages.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE_PAGE = ROOT / "lenders/major-banks.html"
OUT_DIR = ROOT / "lenders"
BASE_URL = "https://www.finchmortgages.co.nz"

# --- Lender data ---------------------------------------------------------- #
# Each tuple drives one generated page.
LENDERS = [
    {
        "slug": "anz-home-loan-review",
        "name": "ANZ",
        "full_name": "ANZ Bank New Zealand",
        "category": "major bank",
        "tier": "Tier 1",
        "founded": "1840 (NZ presence)",
        "positioning": "the largest registered bank in New Zealand by mortgage book size",
        "specialties": "owner-occupier home loans, investment lending, KiwiSaver, business banking",
        "best_for": "buyers with clean PAYE income wanting fast main-bank turnaround and large lending appetite",
        "pros": [
            "Largest NZ mortgage book — strong pricing depth on prime deals",
            "Fast turnaround for clean PAYE scenarios",
            "Active cashback campaigns (0.50–0.90% of loan amount)",
            "Full digital application + e-signing workflow",
        ],
        "cons": [
            "Conservative on self-employed or 1-year financials cases",
            "CCCFA-driven living expense scrutiny is among the tightest",
            "Pre-approval validity window of 90 days only",
        ],
    },
    {
        "slug": "asb-mortgage-review",
        "name": "ASB",
        "full_name": "ASB Bank",
        "category": "major bank",
        "tier": "Tier 1",
        "founded": "1847",
        "positioning": "one of New Zealand's largest registered banks, owned by Commonwealth Bank of Australia",
        "specialties": "owner-occupier, first home buyers, KiwiSaver, business banking, investor lending",
        "best_for": "first home buyers and clean-PAYE borrowers wanting efficient main-bank lending",
        "pros": [
            "Highly efficient digital application and decisioning",
            "Strong first home buyer policies and Welcome Home Loan participation in some scenarios",
            "Competitive carded and broker rates",
            "Active cashback contributions for refinance and purchase",
        ],
        "cons": [
            "Test rate runs at the higher end of the main-bank range",
            "Investor LVR policies are conservative",
            "Less appetite for complex self-employed scenarios",
        ],
    },
    {
        "slug": "bnz-home-loan-review",
        "name": "BNZ",
        "full_name": "Bank of New Zealand",
        "category": "major bank",
        "tier": "Tier 1",
        "founded": "1861",
        "positioning": "one of NZ's most established main banks, part of National Australia Bank",
        "specialties": "professional borrowers, investor lending, business banking, premium client servicing",
        "best_for": "higher-income professionals and investors who value larger loan sizes and tailored pricing",
        "pros": [
            "Often most generous on borrowing power for professional/high-income earners",
            "Strong investor lending appetite where serviceability stacks up",
            "Broker channel pricing can be sharper than carded for the right scenarios",
            "Cashback contributions across purchase and refinance",
        ],
        "cons": [
            "Heavier document expectations than ANZ/ASB",
            "Longer turnaround for non-routine cases",
            "Test rate is conservative",
        ],
    },
    {
        "slug": "westpac-mortgage-review",
        "name": "Westpac",
        "full_name": "Westpac New Zealand",
        "category": "major bank",
        "tier": "Tier 1",
        "founded": "1861 (NZ)",
        "positioning": "one of New Zealand's main banks with a strong Auckland and South Island presence",
        "specialties": "owner-occupier, first home buyers (Welcome Home Loan participant), business lending",
        "best_for": "first home buyers using Kāinga Ora First Home Loan (5% deposit pathway)",
        "pros": [
            "Participates in Kāinga Ora First Home Loan — accepts 5% deposit",
            "Family Springboard equity-sharing product for assisted purchases",
            "Solid carded and broker rate pricing",
            "Active refinance cashback campaigns",
        ],
        "cons": [
            "Heavy CCCFA living expense scrutiny",
            "Investor lending policy more conservative than ANZ/BNZ",
            "Pre-approval renewal sometimes needs full re-documentation",
        ],
    },
    {
        "slug": "kiwibank-home-loan-review",
        "name": "Kiwibank",
        "full_name": "Kiwibank Limited",
        "category": "major bank",
        "tier": "Tier 1",
        "founded": "2002",
        "positioning": "New Zealand's only majority Crown-owned major bank",
        "specialties": "first home buyers, low-deposit Welcome Home Loan, owner-occupier lending",
        "best_for": "first home buyers wanting the Kāinga Ora First Home Loan 5% pathway with a NZ-owned bank",
        "pros": [
            "Strong Kāinga Ora First Home Loan partner — accepts 5% deposit",
            "Welcoming policies for first home buyers",
            "NZ-owned and locally focused",
            "Competitive carded rates",
        ],
        "cons": [
            "Smaller branch footprint than other Tier 1 banks",
            "Investor lending appetite more constrained",
            "Some processing slower than ANZ/ASB in peak periods",
        ],
    },
    {
        "slug": "tsb-mortgage-review",
        "name": "TSB",
        "full_name": "TSB Bank",
        "category": "regional bank",
        "tier": "Tier 1 (regional)",
        "founded": "1850",
        "positioning": "Taranaki-headquartered NZ-owned bank with a strong customer service reputation",
        "specialties": "owner-occupier mortgages, term deposits, KiwiSaver",
        "best_for": "borrowers who value relationship-led NZ-owned banking and competitive rates",
        "pros": [
            "Sharp carded rates — frequently among NZ's lowest",
            "NZ-owned with strong customer service ratings",
            "Active cashback contributions",
            "Straightforward digital application",
        ],
        "cons": [
            "Smaller branch network outside Taranaki",
            "Less flexibility on complex investor cases",
            "Test rate is conservative",
        ],
    },
    {
        "slug": "sbs-mortgage-review",
        "name": "SBS Bank",
        "full_name": "Southland Building Society (SBS Bank)",
        "category": "registered bank",
        "tier": "Tier 1 (regional)",
        "founded": "1869",
        "positioning": "NZ's only mutual-ownership registered bank, headquartered in Invercargill",
        "specialties": "first home buyers, Welcome Home Loan, regional NZ lending",
        "best_for": "first home buyers seeking 5% deposit lending through a mutual NZ-owned bank",
        "pros": [
            "Participates in Kāinga Ora First Home Loan",
            "Member-owned mutual structure",
            "Often accepts 1-year financials for self-employed",
            "Strong regional NZ lending support",
        ],
        "cons": [
            "Smaller branch footprint outside Southland and Otago",
            "Investor pricing not as sharp as Tier 1 majors",
        ],
    },
    {
        "slug": "co-operative-bank-mortgage-review",
        "name": "The Co-operative Bank",
        "full_name": "The Co-operative Bank",
        "category": "registered bank",
        "tier": "Tier 1 (regional)",
        "founded": "1928",
        "positioning": "NZ's only customer-owned registered bank — members are shareholders",
        "specialties": "first home buyers, Welcome Home Loan, owner-occupier lending",
        "best_for": "first home buyers wanting Kāinga Ora First Home Loan via a customer-owned bank",
        "pros": [
            "Profits returned to members as annual rebates",
            "Active Welcome Home Loan partner",
            "Genuinely competitive carded rates",
            "Strong NZ-owned identity",
        ],
        "cons": [
            "Smaller branch network than majors",
            "Less appetite for complex investor or commercial deals",
        ],
    },
    {
        "slug": "heartland-bank-mortgage-review",
        "name": "Heartland Bank",
        "full_name": "Heartland Bank Limited",
        "category": "registered bank",
        "tier": "Tier 1 (specialist)",
        "founded": "2011",
        "positioning": "NZ-owned bank specialising in reverse mortgages, asset finance, and motor lending",
        "specialties": "reverse mortgages, asset finance, motor finance, livestock lending",
        "best_for": "retirees considering a reverse mortgage; SME owners seeking asset finance",
        "pros": [
            "Reverse mortgage market leader in NZ",
            "Strong asset finance and motor lending products",
            "Direct, broker-friendly underwriting",
            "Specialist agricultural lending",
        ],
        "cons": [
            "Limited standard residential home loan product range",
            "Branch network is small",
        ],
    },
    {
        "slug": "resimac-mortgage-review",
        "name": "Resimac",
        "full_name": "Resimac Home Loans (NZ)",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "1985 (Aus); active in NZ",
        "positioning": "specialist non-bank lender with both prime and near-prime product suites",
        "specialties": "alt-doc self-employed, near-prime credit, investor lending",
        "best_for": "self-employed borrowers with 1-year financials, or borrowers declined by main banks for non-credit reasons",
        "pros": [
            "Accepts 6 months bank statements as alt-doc income evidence",
            "Lower turnaround than main banks on complex deals",
            "Direct broker channel access — clear, repeatable policies",
            "Strong investor lending appetite",
        ],
        "cons": [
            "Carded rates higher than main banks (yield premium for flexibility)",
            "No branch network in NZ",
            "Cashback offers usually less than main banks",
        ],
    },
    {
        "slug": "pepper-money-mortgage-review",
        "name": "Pepper Money",
        "full_name": "Pepper Money (NZ)",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "2000 (Aus); active in NZ",
        "positioning": "specialist non-bank with deep expertise in near-prime and credit-impaired lending",
        "specialties": "credit-impaired borrowers, self-employed alt-doc, debt consolidation",
        "best_for": "borrowers with credit history issues (past defaults, arrears) seeking a refinance pathway",
        "pros": [
            "Accepts past defaults, arrears, and recent enquiries that main banks decline",
            "Strong debt consolidation positioning",
            "Alt-doc self-employed product line",
            "Clear matrix-based credit policy",
        ],
        "cons": [
            "Higher rate band than main banks reflecting risk profile",
            "Application fee applies to most products",
        ],
    },
    {
        "slug": "avanti-finance-mortgage-review",
        "name": "Avanti Finance",
        "full_name": "Avanti Finance",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "1991",
        "positioning": "NZ-owned non-bank lender across mortgages, personal loans, and motor finance",
        "specialties": "self-employed alt-doc, debt consolidation, bridging finance",
        "best_for": "self-employed borrowers wanting a NZ-owned non-bank alternative to Resimac or Pepper",
        "pros": [
            "NZ-owned and NZ-decisioned",
            "Bridging finance product available",
            "Accepts complex income structures (trusts, LTCs)",
            "Solid alt-doc options",
        ],
        "cons": [
            "Higher rates than main banks",
            "Limited branch presence",
        ],
    },
    {
        "slug": "liberty-financial-mortgage-review",
        "name": "Liberty Financial",
        "full_name": "Liberty Financial (NZ)",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "1997 (Aus); active in NZ",
        "positioning": "specialist non-bank lender with niche product lines including SMSF and complex investor lending",
        "specialties": "investor lending, complex serviceability, alt-doc, commercial-residential hybrids",
        "best_for": "established property investors with complex serviceability scenarios main banks decline",
        "pros": [
            "Generous on complex investor cases",
            "Accepts alt-doc and full-doc with broader criteria",
            "Strong commercial lending capability",
            "Broker channel relationship-led",
        ],
        "cons": [
            "Higher carded rates than main banks",
            "Application and ongoing fees apply",
        ],
    },
    {
        "slug": "basecorp-mortgage-review",
        "name": "Basecorp",
        "full_name": "Basecorp Finance",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "1997",
        "positioning": "NZ-owned non-bank specialising in residential property lending where main banks decline",
        "specialties": "near-prime, low-doc, complex credit, second-tier residential",
        "best_for": "borrowers declined by main banks for credit or income complexity, seeking a NZ-owned alternative",
        "pros": [
            "NZ-owned, NZ-decisioned",
            "Accepts low-doc and complex credit",
            "Strong relationship with brokers across NZ",
        ],
        "cons": [
            "Higher rate band than main banks",
            "Limited brand recognition",
        ],
    },
    {
        "slug": "bluestone-mortgage-review",
        "name": "Bluestone",
        "full_name": "Bluestone Mortgages (NZ)",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "2000 (Aus); active in NZ",
        "positioning": "specialist non-bank lender focused on near-prime and self-employed residential lending",
        "specialties": "self-employed, near-prime credit, debt consolidation",
        "best_for": "self-employed borrowers needing an alt-doc product main banks won't offer",
        "pros": [
            "Strong alt-doc product suite",
            "Accepts 6 months business bank statements",
            "Clear matrix-based credit decisioning",
        ],
        "cons": [
            "Higher rates than main banks",
            "No branch presence in NZ",
        ],
    },
    {
        "slug": "first-credit-union-mortgage-review",
        "name": "First Credit Union",
        "full_name": "First Credit Union",
        "category": "credit union",
        "tier": "Member-owned",
        "founded": "1955",
        "positioning": "Hamilton-based member-owned credit union active in residential and personal lending",
        "specialties": "member residential lending, personal loans, community-focused finance",
        "best_for": "credit union members seeking competitive residential lending with mutual ownership",
        "pros": [
            "Member-owned, profits returned via better rates",
            "Strong regional NZ presence (Waikato, Bay of Plenty)",
            "Personalised service",
        ],
        "cons": [
            "Smaller lending book than registered banks",
            "Membership requirement",
        ],
    },
    {
        "slug": "police-credit-union-mortgage-review",
        "name": "Police Credit Union (NZCU)",
        "full_name": "NZCU Baywide / Police and Families Credit Union",
        "category": "credit union",
        "tier": "Member-owned",
        "founded": "1969",
        "positioning": "NZ credit union serving Police and emergency-services members with residential lending",
        "specialties": "member residential lending, personal loans, community-focused finance",
        "best_for": "Police, emergency-services personnel and families seeking member-owned residential lending",
        "pros": [
            "Member-owned with profits returning to members",
            "Strong relationship-led service",
            "Competitive carded rates",
        ],
        "cons": [
            "Eligibility tied to qualifying employment",
            "Smaller residential lending appetite than banks",
        ],
    },
    {
        "slug": "hsbc-nz-mortgage-review",
        "name": "HSBC NZ",
        "full_name": "HSBC Bank New Zealand",
        "category": "registered bank",
        "tier": "Tier 1 (international)",
        "founded": "1865 (global); active in NZ",
        "positioning": "international banking group with NZ residential and premier-banking presence",
        "specialties": "premier banking, expatriate clients, high-net-worth lending",
        "best_for": "globally mobile clients, expats, and high-net-worth borrowers seeking international banking",
        "pros": [
            "Strong for offshore-income clients and expatriates",
            "Premier banking suite with global account linkage",
            "Competitive pricing for premier-tier clients",
        ],
        "cons": [
            "Smaller NZ residential lending appetite",
            "Limited branch footprint in NZ",
        ],
    },
    {
        "slug": "icbc-nz-mortgage-review",
        "name": "ICBC NZ",
        "full_name": "Industrial and Commercial Bank of China (NZ)",
        "category": "registered bank",
        "tier": "Tier 1 (international)",
        "founded": "1984 (global); 2013 (NZ)",
        "positioning": "global Chinese bank with NZ commercial and residential lending capability",
        "specialties": "commercial property lending, residential lending for offshore-linked clients",
        "best_for": "borrowers with offshore income or links to the Chinese banking system",
        "pros": [
            "Specialist in offshore-linked client lending",
            "Strong commercial property lending",
        ],
        "cons": [
            "Smaller residential mortgage book",
            "Limited consumer brand presence in NZ",
        ],
    },
    {
        "slug": "udc-finance-asset-review",
        "name": "UDC Finance",
        "full_name": "UDC Finance",
        "category": "specialist lender",
        "tier": "Specialist",
        "founded": "1937",
        "positioning": "NZ's largest specialist asset and equipment finance provider",
        "specialties": "asset finance, equipment finance, motor vehicle finance, commercial leasing",
        "best_for": "businesses financing vehicles, equipment, plant, or heavy machinery in NZ",
        "pros": [
            "NZ's largest asset finance specialist by book",
            "Deep industry expertise in yellow goods, transport, agriculture",
            "Flexible product suite — chattel mortgage, lease, hire purchase",
        ],
        "cons": [
            "Not a residential home loan lender",
        ],
    },
    {
        "slug": "marac-asset-finance-review",
        "name": "Marac (Heartland)",
        "full_name": "Marac, division of Heartland Bank",
        "category": "specialist lender",
        "tier": "Specialist",
        "founded": "1957",
        "positioning": "Heartland Bank's specialist asset and motor finance division",
        "specialties": "motor vehicle finance, asset finance, marine and recreational lending",
        "best_for": "NZ buyers needing motor or recreational asset finance through a registered bank specialist",
        "pros": [
            "Backed by Heartland Bank — registered bank security",
            "Strong motor and recreational finance positioning",
            "Direct broker channel",
        ],
        "cons": [
            "Limited residential lending product",
        ],
    },
    {
        "slug": "finance-now-asset-review",
        "name": "Finance Now",
        "full_name": "Finance Now",
        "category": "specialist lender",
        "tier": "Specialist",
        "founded": "1999",
        "positioning": "SBS-owned specialist consumer finance and asset finance provider",
        "specialties": "consumer finance, asset finance, retail point-of-sale lending",
        "best_for": "NZ consumers and SMEs needing flexible specialist consumer / asset finance",
        "pros": [
            "SBS-owned, NZ-based",
            "Wide retail and motor finance distribution",
            "Flexible underwriting",
        ],
        "cons": [
            "Higher rates than main banks for some products",
        ],
    },
    {
        "slug": "asap-finance-mortgage-review",
        "name": "ASAP Finance",
        "full_name": "ASAP Finance",
        "category": "specialist lender",
        "tier": "Specialist (short-term)",
        "founded": "2000s",
        "positioning": "specialist short-term and bridging finance lender in NZ",
        "specialties": "bridging finance, short-term property finance, second-mortgage solutions",
        "best_for": "buyers needing bridging finance or short-term property funding main banks won't provide",
        "pros": [
            "Bridging finance specialist",
            "Fast turnaround for short-term deals",
            "Flexible second-mortgage product",
        ],
        "cons": [
            "Higher rate band reflecting short-term risk profile",
            "Not a long-term residential lender",
        ],
    },
    {
        "slug": "cressida-capital-mortgage-review",
        "name": "Cressida Capital",
        "full_name": "Cressida Capital",
        "category": "specialist lender",
        "tier": "Specialist (commercial)",
        "founded": "2010s",
        "positioning": "specialist commercial and development finance lender in NZ",
        "specialties": "commercial property finance, residential development, complex investor deals",
        "best_for": "property developers and complex investors needing commercial-grade financing",
        "pros": [
            "Commercial development finance specialist",
            "Flexible structuring on complex deals",
            "Direct broker channel",
        ],
        "cons": [
            "Higher rates than main banks",
            "Not a standard owner-occupier lender",
        ],
    },
    {
        "slug": "mitsubishi-hc-capital-review",
        "name": "Mitsubishi HC Capital",
        "full_name": "Mitsubishi HC Capital New Zealand",
        "category": "specialist lender",
        "tier": "Specialist (asset)",
        "founded": "1970s (NZ presence)",
        "positioning": "specialist commercial asset and equipment finance provider",
        "specialties": "commercial equipment finance, leasing, vehicle fleet finance",
        "best_for": "NZ businesses financing commercial vehicle fleets and large equipment",
        "pros": [
            "Strong commercial equipment finance",
            "Fleet leasing specialist",
            "International parent supports large deal capacity",
        ],
        "cons": [
            "Not a residential home loan lender",
        ],
    },
]


def title_for(lender: dict) -> str:
    if lender["category"] in ("specialist lender",):
        return f"{lender['name']} Review NZ 2026 | Asset &amp; Specialist Finance | Finch"
    if lender["category"] == "credit union":
        return f"{lender['name']} Review NZ 2026 | Credit Union Lending | Finch"
    if lender["category"] == "non-bank lender":
        return f"{lender['name']} NZ Review 2026 | Non-Bank Mortgages | Finch"
    return f"{lender['name']} Home Loan Review NZ 2026 | Mortgage Rates &amp; Policy | Finch"


def description_for(lender: dict) -> str:
    return (
        f"Independent {lender['name']} ({lender['full_name']}) review for NZ borrowers — "
        f"{lender['positioning']}. Compare rates, deposit requirements, policy strengths, "
        f"and how Finch matches your scenario across 20+ NZ lenders."
    )


def keywords_for(lender: dict) -> str:
    name = lender["name"]
    base = [
        f"{name} home loan NZ",
        f"{name} mortgage NZ 2026",
        f"{name} mortgage rates NZ",
        f"{name} home loan review",
        f"{name} mortgage broker NZ",
        f"NZ mortgage {name}",
        f"{name} refinance NZ",
        f"{name} first home buyer NZ",
        f"{name} investor lending NZ",
        "NZ mortgage broker",
        "NZ home loan comparison",
        "20 lenders NZ",
    ]
    return ", ".join(base)


def schema_for(lender: dict) -> str:
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Lenders", "item": f"{BASE_URL}/lenders.html"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{lender['name']} Review",
                "item": f"{BASE_URL}/lenders/{lender['slug']}.html",
            },
        ],
    }
    review = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{lender['full_name']} Review for NZ Mortgage Borrowers (2026)",
        "description": description_for(lender),
        "url": f"{BASE_URL}/lenders/{lender['slug']}.html",
        "inLanguage": "en-NZ",
        "publisher": {
            "@type": "MortgageBroker",
            "@id": f"{BASE_URL}/#organization",
            "name": "Finch Mortgages",
            "url": f"{BASE_URL}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/finch-logo.png"},
        },
        "about": {
            "@type": "FinancialService",
            "name": lender["full_name"],
            "areaServed": {"@type": "Country", "name": "New Zealand"},
        },
    }
    return (
        "<script type=\"application/ld+json\">"
        + json.dumps(breadcrumb, indent=2)
        + "</script>\n<script type=\"application/ld+json\">"
        + json.dumps(review, indent=2)
        + "</script>"
    )


def main_body(lender: dict) -> str:
    name = lender["name"]
    full_name = lender["full_name"]
    pros_html = "".join(f"<li style=\"margin-bottom:0.5rem;\">{p}</li>" for p in lender["pros"])
    cons_html = "".join(f"<li style=\"margin-bottom:0.5rem;\">{c}</li>" for c in lender["cons"])

    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <!-- Hero -->
    <section class="container page-hero" style="padding-top:4rem;padding-bottom:4rem;">
      <div class="reveal" style="max-width:800px;">
        <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../lenders.html">Lenders</a><span class="breadcrumb-sep">/</span><span>{name} Review</span></nav>
        <div class="page-hero-tag">{lender['tier']} · {lender['category'].title()}</div>
        <h1>{name} <em style="font-style:italic;color:var(--finch-forest);">Review.</em></h1>
        <p>{description_for(lender)}</p>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
          <a class="btn-primary" href="../contact.html">Compare {name} with 20+ NZ Lenders</a>
          <a class="btn-secondary" href="../mortgage-rates.html">View Live NZ Rates</a>
        </div>
      </div>
    </section>

    <!-- Lender Snapshot -->
    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:900px;">
        <div class="cols-3" style="gap:1.5rem;">
          <div style="padding:1.5rem;background:var(--finch-mist);border-radius:1rem;">
            <strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Category</strong>
            <span style="color:var(--neutral-medGray);">{lender['category'].title()}</span>
          </div>
          <div style="padding:1.5rem;background:var(--finch-mist);border-radius:1rem;">
            <strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Presence Since</strong>
            <span style="color:var(--neutral-medGray);">{lender['founded']}</span>
          </div>
          <div style="padding:1.5rem;background:var(--finch-mist);border-radius:1rem;">
            <strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Specialty</strong>
            <span style="color:var(--neutral-medGray);">{lender['specialties']}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Comprehensive Review -->
    <section style="padding:5rem 0;background:var(--finch-mist);">
      <div class="container" style="max-width:800px;">
        <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
          <h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">{full_name} — NZ Mortgage Review (2026)</h2>
          <p style="margin-bottom:2rem;">{full_name} is {lender['positioning']}. For New Zealand borrowers, the lender's specialties include {lender['specialties']}. As an independent NZ mortgage broker, Finch arranges loans through {name} alongside the full panel of registered NZ banks (ANZ, ASB, BNZ, Westpac, Kiwibank, TSB, SBS, The Co-operative Bank, Heartland) and the specialist non-bank market — so we can recommend {name} only when their offer genuinely beats the alternatives for your scenario.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Who {name} Suits Best</h3>
          <p style="margin-bottom:2rem;">{name} suits {lender['best_for']}. We see strongest outcomes when the client's income profile, deposit position, and intended property align with {name}'s current scorecard. Outside those scenarios, another NZ lender will usually price sharper or move faster — which is why we compare every option before recommending.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{name} — Strengths</h3>
          <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">{pros_html}</ul>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{name} — Considerations</h3>
          <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">{cons_html}</ul>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">How {name} Compares Across the NZ Lender Panel</h3>
          <p style="margin-bottom:2rem;">No single NZ lender wins for every scenario. Pricing varies by week and by deal type — {name} may be sharpest one month and uncompetitive the next, while a non-bank like Resimac or Pepper Money picks up cases the main banks decline. Use our <a href="../mortgage-rates.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">live NZ rates comparison</a> to see where {name} sits today, then book a free consultation to match your scenario against the full panel.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Documents {name} Typically Requires</h3>
          <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">
            <li style="margin-bottom:0.5rem;">3 months payslips (PAYE) or 2 years accountant-signed financials (self-employed)</li>
            <li style="margin-bottom:0.5rem;">3 months bank statements across every account including credit cards</li>
            <li style="margin-bottom:0.5rem;">KiwiSaver provider statement and annual summary (for first home buyers)</li>
            <li style="margin-bottom:0.5rem;">NZ photo ID + proof of address (AML compliance)</li>
            <li style="margin-bottom:0.5rem;">Evidence of deposit and recent savings history</li>
          </ul>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Service Coverage Across NZ</h3>
          <p style="margin-bottom:2rem;">Finch arranges {name} lending for clients across the country — Auckland, Wellington, Christchurch, Hamilton, Tauranga, Dunedin, Palmerston North, Napier, Nelson, Queenstown, and regional NZ. We submit your file via the lender's broker channel which usually delivers a faster, sharper outcome than walking into a branch.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Should You Go Direct, or Use a Broker?</h3>
          <p style="margin-bottom:1rem;">Going direct to {name} only gives you {name}. Using Finch costs you nothing — {name} (where they're the right answer) pays the broker fee on settlement, not you — and you get the comparison across every other NZ lender for free. Read our real <a href="../case-studies.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">NZ client case studies</a> for examples.</p>
        </div>
      </div>
    </section>

    <!-- Related NZ Resources -->
    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>Compare More NZ Lenders</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Other NZ lender reviews &amp; resources</h2>
        <div class="cols-3" style="gap:1.5rem;">
          <a href="../lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">All NZ Lenders</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Browse every NZ lender reviewed.</span></a>
          <a href="../lenders/major-banks.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Major Banks</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">ANZ, ASB, BNZ, Westpac, Kiwibank.</span></a>
          <a href="../lenders/non-bank-lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Non-Bank Lenders</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Resimac, Pepper, Liberty, Avanti.</span></a>
          <a href="../mortgage-rates.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Live NZ Mortgage Rates</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Current carded and broker rates.</span></a>
          <a href="../services/home-loan.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Home Loan Service</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Independent NZ broker advice.</span></a>
          <a href="../contact.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Book a Free Call</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">15-min discovery, no obligation.</span></a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section style="padding:5rem 0;">
      <div class="container">
        <div class="cta-section reveal">
          <h2>Ready to compare<br/>{name} with the full panel?</h2>
          <p>Free 15-minute consultation. We match your scenario against 20+ NZ lenders — including {name} — and recommend the sharpest option.</p>
          <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
            <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
            <a class="btn-cta-outline" href="../mortgage-rates.html">View Live NZ Rates</a>
          </div>
        </div>
      </div>
    </section>
    </main>
    """)


def build_page(lender: dict, template_text: str) -> str:
    # Replace title, description, canonical, keywords, schema, and main body.
    head_close = template_text.find("</head>")
    if head_close == -1:
        raise SystemExit("Template missing </head>")

    head = template_text[: head_close]
    # Build a fresh <head> reusing fonts, lucide, and stylesheet from template.
    # We replace title + description + canonical + keywords + schema cleanly.
    title = title_for(lender)
    description = description_for(lender)
    canonical = f"{BASE_URL}/lenders/{lender['slug']}.html"
    keywords = keywords_for(lender)
    schema = schema_for(lender)

    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"description\"/?>',
        f'<meta content="{description}" name="description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<link href=\"https://www\.finchmortgages\.co\.nz/lenders/[^\"]+\" rel=\"canonical\"/?>',
        f'<link href="{canonical}" rel="canonical"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"keywords\"/?>',
        f'<meta content="{keywords}" name="keywords"/>',
        head,
    )
    # Replace breadcrumb JSON-LD block with our combined schema
    # Use lambda to avoid backslash escape interpretation in JSON strings.
    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        lambda _m: schema,
        head,
        count=1,
        flags=re.S,
    )

    head += "</head>"

    # Extract footer (from </main> onwards in original template)
    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]

    # Extract body open (everything between </head> and <main>)
    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]

    return head + "\n" + body_open + main_body(lender) + footer


def main() -> None:
    template_text = TEMPLATE_PAGE.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    for lender in LENDERS:
        out_path = OUT_DIR / f"{lender['slug']}.html"
        page = build_page(lender, template_text)
        out_path.write_text(page, encoding="utf-8")
        generated.append(out_path)
        print(f"  + {out_path.relative_to(ROOT)}")

    print()
    print(f"Generated {len(generated)} lender pages.")


if __name__ == "__main__":
    main()
