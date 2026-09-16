"""Generate 23 individual NZ-lender review pages for SEO.

Each page targets an approved lender from Finch Mortgages' canonical 23-lender roster
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

# ISO 8601 dates for Article rich-result eligibility
ARTICLE_PUBLISHED = "2026-01-15"
ARTICLE_MODIFIED = "2026-09-16"

# --- 23 Approved Lenders Data --------------------------------------------- #
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
            "Active cashback campaigns for purchase and refinance",
            "Full digital application and e-signing workflow",
        ],
        "cons": [
            "Conservative on self-employed or 1-year financials cases",
            "CCCFA-driven living expense scrutiny is among the tightest",
            "Pre-approval validity window of 90 days only",
        ],
    },
    {
        "slug": "avanti-finance-mortgage-review",
        "name": "Avanti Finance Property Loans",
        "full_name": "Avanti Finance Limited",
        "category": "non-bank lender",
        "tier": "Tier 2 (specialist)",
        "founded": "1989",
        "positioning": "one of New Zealand's most established non-bank property and personal finance providers",
        "specialties": "near-prime residential mortgages, bridging finance, second mortgages, self-employed loans",
        "best_for": "borrowers needing rapid conditional approvals, bridging funding, or alternative documentation",
        "pros": [
            "Fast turnaround with conditional offers often issued in 24–48 hours",
            "Flexible bridging finance structures allowing clients to buy before selling",
            "Pragmatic, common-sense underwriting on self-employed and contract income",
            "Accommodates second mortgages and complex property security stacks",
        ],
        "cons": [
            "Interest rates reflect non-bank risk profiles and sit above main-bank specials",
            "Establishment and facility fees apply",
            "Shorter loan terms on specialist bridging facilities",
        ],
    },
    {
        "slug": "basecorp-mortgage-review",
        "name": "Basecorp Finance",
        "full_name": "Basecorp Finance Limited",
        "category": "specialist lender",
        "tier": "Tier 2 (private funder)",
        "founded": "1997",
        "positioning": "a premier privately owned NZ non-bank lender focused on short-to-medium term property finance",
        "specialties": "fast bridging finance, property development, commercial property loans, urgent settlement rescues",
        "best_for": "property investors and developers needing high-speed capital without bureaucratic retail bank delays",
        "pros": [
            "Rapid credit decisions within 24 hours backed by private capital",
            "Asset-backed lending focus with minimal personal income red tape",
            "Flexible exit strategies tailored for property traders and renovators",
            "Unbureaucratic, direct access to senior lending decision-makers",
        ],
        "cons": [
            "Interest rates carry a risk premium above traditional residential loans",
            "Non-bank establishment and legal administration fees",
            "Not suited for long-term prime owner-occupier borrowing",
        ],
    },
    {
        "slug": "bnz-home-loan-review",
        "name": "BNZ",
        "full_name": "Bank of New Zealand",
        "category": "major bank",
        "tier": "Tier 1",
        "founded": "1861",
        "positioning": "one of NZ's largest registered banks, part of National Australia Bank (NAB)",
        "specialties": "professional borrowers, investor lending, TotalMoney offset facility, self-employed mortgages",
        "best_for": "self-employed professionals, investors, and borrowers wanting market-leading offset loan features",
        "pros": [
            "TotalMoney mortgage offset across up to 50 linked family or business accounts",
            "Pragmatic view on self-employed income with strong forward cashflow",
            "Competitive broker rate pricing and active cashback contributions",
            "Strong property investor appetite where serviceability stacks up",
        ],
        "cons": [
            "Heavier document expectations than smaller non-bank funders",
            "Conservative servicing test rates in line with Reserve Bank rules",
            "Turnaround times can vary during high-volume application cycles",
        ],
    },
    {
        "slug": "cfml-mortgage-review",
        "name": "CFML",
        "full_name": "Commercial & Residential First Mortgage Loans (CFML)",
        "category": "non-bank lender",
        "tier": "Tier 2 (specialist)",
        "founded": "1998",
        "positioning": "an established NZ mortgage fund manager and non-bank lender providing tailored property loans",
        "specialties": "first mortgages, residential property loans, commercial and development finance, flexible equity solutions",
        "best_for": "borrowers and investors needing flexible non-bank first mortgages tailored to non-standard property or income profiles",
        "pros": [
            "Human underwriting with common-sense credit assessments",
            "Flexible loan terms and interest-only options tailored to borrower cashflows",
            "Experienced property finance team with deep knowledge of the NZ property market",
            "Accommodates unique residential securities and development equity needs",
        ],
        "cons": [
            "Higher interest rates than prime main banks",
            "Establishment and legal documentation fees apply",
            "Selective geographical security criteria outside primary growth corridors",
        ],
    },
    {
        "slug": "china-construction-bank-mortgage-review",
        "name": "China Construction Bank",
        "full_name": "China Construction Bank (New Zealand) Limited",
        "category": "registered bank",
        "tier": "Tier 1 (international)",
        "founded": "2014 (NZ registered bank)",
        "positioning": "a full registered bank in New Zealand backed by one of the world's largest banking corporations",
        "specialties": "residential mortgages, high-net-worth borrowing, cross-border banking, commercial property finance",
        "best_for": "prime borrowers and cross-border clients seeking competitive registered-bank home loans with global institutional backing",
        "pros": [
            "Full NZ registered bank status and prudential Reserve Bank regulation",
            "Competitive mortgage rates and tailorable fixed borrowing terms",
            "Bilingual client servicing with deep cross-border property expertise",
            "Substantial balance sheet for large commercial and residential transactions",
        ],
        "cons": [
            "Smaller retail branch network in NZ compared to domestic retail banks",
            "Selective appetite for high-LVR or low-deposit borrowing",
            "Standard registered-bank credit verification and CCCFA checks apply",
        ],
    },
    {
        "slug": "cressida-capital-mortgage-review",
        "name": "Cressida Capital",
        "full_name": "Cressida Capital One Limited",
        "category": "property finance",
        "tier": "Tier 2 (private funder)",
        "founded": "2011",
        "positioning": "boutique property financiers specializing in bespoke short-term lending, mezzanine debt, and bridging",
        "specialties": "short-term property loans, bridging finance, land and construction funding, urgent settlements",
        "best_for": "property investors and commercial borrowers needing fast bespoke funding structures",
        "pros": [
            "Fast direct access to credit decision-makers without committee delays",
            "Innovative loan structuring including second mortgages and mezzanine tranches",
            "Asset-focused underwriting that looks at property value and project merit",
            "Reliable execution on urgent settlement deadlines",
        ],
        "cons": [
            "Premium pricing reflecting short-term non-bank risk",
            "Facility establishment and line fees apply",
            "Not designed for 30-year residential owner-occupier mortgages",
        ],
    },
    {
        "slug": "dbr-property-financiers-review",
        "name": "DBR",
        "full_name": "DBR Property Financiers",
        "category": "property finance",
        "tier": "Tier 2 (specialist)",
        "founded": "2002",
        "positioning": "leading New Zealand non-bank property financiers providing short-to-medium term mortgage lending",
        "specialties": "residential bridging, property refurbishment, commercial loans, fast settlement solutions",
        "best_for": "borrowers needing immediate capital to bridge purchases, complete renovations, or resolve short-term financial constraints",
        "pros": [
            "Over 20 years of continuous NZ property lending experience",
            "Approvals in days rather than weeks with minimal institutional friction",
            "Transparent fee and interest structures with clear exit strategies",
            "Strong appetite for residential development, land, and refurbishment",
        ],
        "cons": [
            "Specialized interest rates above standard main-bank specials",
            "Setup and facility inspection fees apply",
            "Primarily short-to-medium term facilities (6–24 months)",
        ],
    },
    {
        "slug": "finbase-mortgage-review",
        "name": "Finbase",
        "full_name": "Finbase Limited",
        "category": "specialist lender",
        "tier": "Tier 2 (non-bank)",
        "founded": "2018",
        "positioning": "a modern technology-enabled non-bank property lender delivering rapid property finance",
        "specialties": "flexible residential mortgages, investment property loans, fast approvals, alternative income verification",
        "best_for": "borrowers seeking streamlined digital non-bank lending with responsive service and sensible credit policies",
        "pros": [
            "Agile digital application and assessment process with fast turnaround times",
            "Competitive non-bank pricing for creditworthy self-employed borrowers",
            "Accommodating on self-employed, contract, and diverse income sources",
            "Transparent broker communication with dedicated underwriting managers",
        ],
        "cons": [
            "Slightly higher interest rates than Tier 1 bank specials",
            "Establishment fees apply on facility setup",
            "Stricter LVR caps on regional and non-metropolitan properties",
        ],
    },
    {
        "slug": "first-mortgage-trust-review",
        "name": "First Mortgage Trust",
        "full_name": "First Mortgage Managers Limited",
        "category": "non-bank fund",
        "tier": "Tier 2 (mortgage fund)",
        "founded": "1996",
        "positioning": "New Zealand's largest non-bank mortgage fund manager with over 28 years of trusted property lending",
        "specialties": "residential mortgages, commercial property, rural and industrial loans, bridging and development",
        "best_for": "property investors, business owners, and borrowers wanting stable non-bank mortgage funding from an established NZ fund",
        "pros": [
            "Substantial capital base offering continuous liquidity across NZ market cycles",
            "Experienced nationwide lending team with practical underwriting guidelines",
            "Interest-only payment options available for qualifying property investors",
            "Transparent governance and long-standing reputation in the NZ lending community",
        ],
        "cons": [
            "Non-bank risk-rated interest rates",
            "Conservative valuation and loan-to-value requirements",
            "Facility management and establishment fees apply",
        ],
    },
    {
        "slug": "funding-partners-review",
        "name": "Funding Partners",
        "full_name": "Funding Partners Limited",
        "category": "property financier",
        "tier": "Tier 2 (private funder)",
        "founded": "2015",
        "positioning": "private real estate and mortgage funding specialist backing New Zealand property borrowers",
        "specialties": "residential property finance, development funding, equity release, short-term debt solutions",
        "best_for": "developers and investors looking for bespoke private debt solutions without traditional banking obstacles",
        "pros": [
            "Highly customized funding structures tailored to individual project milestones",
            "Commercial pragmatism and willingness to fund complex deal architecture",
            "Direct decision-making from experienced principals without lengthy committees",
            "Supports non-standard asset types and progressive drawdown requirements",
        ],
        "cons": [
            "Higher risk-adjusted pricing than institutional retail loans",
            "Not structured for standard low-deposit owner-occupier purchases",
            "Documentation and structuring fees reflect custom legal work",
        ],
    },
    {
        "slug": "gem-by-latitude-review",
        "name": "GEM By Latitude",
        "full_name": "Latitude Financial Services (GEM)",
        "category": "consumer & property finance",
        "tier": "Tier 2 (specialist)",
        "founded": "2000 (NZ presence)",
        "positioning": "a major consumer and personal finance provider supporting structured finance and debt consolidation",
        "specialties": "debt consolidation, personal loans, supplementary property finance, home improvement loans",
        "best_for": "borrowers needing structured debt consolidation to tidy credit profiles before or alongside mortgage applications",
        "pros": [
            "Established brand with nationwide operational footprint",
            "Streamlined digital application and fast electronic identity verification",
            "Effective tool for clearing and consolidating high-interest unsecured debts",
            "Fixed repayment structures that provide clear timelines for debt reduction",
        ],
        "cons": [
            "Unsecured finance carries interest rates higher than standard home loans",
            "Credit scoring criteria require stable employment and clean repayment track records",
            "Strict affordability assessments under the CCCFA",
        ],
    },
    {
        "slug": "general-finance-mortgage-review",
        "name": "General Finance",
        "full_name": "General Finance Limited (NZX: GFL)",
        "category": "non-bank deposit taker",
        "tier": "Tier 2 (NBDT)",
        "founded": "1999",
        "positioning": "an NZX-listed non-bank deposit taker licensed by the Reserve Bank of New Zealand (RBNZ)",
        "specialties": "residential first and second mortgages, business property loans, bridging loans, flexible terms",
        "best_for": "borrowers needing flexible residential or commercial property funding backed by a licensed, publicly listed institution",
        "pros": [
            "Licensed Non-Bank Deposit Taker (NBDT) supervised by the Reserve Bank of NZ",
            "Publicly listed company on the NZX providing transparent governance",
            "Flexible lending policy accommodating self-employed borrowers and unique income",
            "Fast turnaround times on property loan evaluations",
        ],
        "cons": [
            "Interest rates are risk-priced above prime main-bank specials",
            "Establishment and legal fees apply on all loan originations",
            "Conservative maximum loan sizes compared to major corporate banks",
        ],
    },
    {
        "slug": "heartland-bank-mortgage-review",
        "name": "Heartland Bank",
        "full_name": "Heartland Bank Limited",
        "category": "registered bank",
        "tier": "Tier 1 (regional)",
        "founded": "1875 (roots) / 2011 (merged bank)",
        "positioning": "a New Zealand-operated registered bank known for digital home loans, reverse mortgages, and business finance",
        "specialties": "digital home loans, reverse mortgages (home equity release), rural finance, business mortgages",
        "best_for": "borrowers over 60 seeking home equity release / reverse mortgages, or prime borrowers seeking low-rate digital home loans",
        "pros": [
            "New Zealand's undisputed market leader in reverse mortgages and equity release",
            "Aggressive low-rate digital home loans for prime borrowers who qualify",
            "Full registered bank security and RBNZ prudential supervision",
            "Locally operated with headquarters in Auckland and Christchurch",
        ],
        "cons": [
            "Digital home loans have strict criteria (clean PAYE, 20%+ deposit only)",
            "Smaller physical branch network than the Big 4 banks",
            "Selective appetite for complex or non-standard property titles",
        ],
    },
    {
        "slug": "liberty-financial-mortgage-review",
        "name": "Liberty Financial",
        "full_name": "Liberty Financial Limited",
        "category": "non-bank lender",
        "tier": "Tier 2",
        "founded": "1997",
        "positioning": "a leading diversified non-bank lender offering prime, custom, and specialist home loans across Australasia",
        "specialties": "self-employed low-doc mortgages, credit impairment solutions, debt consolidation, commercial-residential mixed properties",
        "best_for": "self-employed borrowers without full financials and applicants with credit defaults needing a pathway back to prime",
        "pros": [
            "Comprehensive product spectrum ranging from near-prime to specialist credit solutions",
            "Outstanding low-doc income options for self-employed Kiwi business owners",
            "Willingness to underwrite unconventional properties and mixed commercial titles",
            "Progressive pathways enabling borrowers to transition to lower rates over time",
        ],
        "cons": [
            "Interest rates increase with the degree of credit impairment",
            "Establishment and risk fees apply on non-prime loan tiers",
            "Strict ongoing servicing buffers applied during underwriting",
        ],
    },
    {
        "slug": "pallas-capital-mortgage-review",
        "name": "Pallas Capital",
        "full_name": "Pallas Capital NZ Limited",
        "category": "non-bank real estate",
        "tier": "Tier 2 (institutional funder)",
        "founded": "2016",
        "positioning": "a premier institutional non-bank real estate financier providing high-capacity commercial and residential funding",
        "specialties": "commercial property finance, residential development, pre-development land loans, bridging debt",
        "best_for": "developers, high-net-worth investors, and commercial property owners seeking institutional-grade non-bank capital",
        "pros": [
            "Substantial lending capacity capable of underwriting multi-million dollar projects",
            "Flexible interest capitalization and structured drawdowns matching build schedules",
            "Sophisticated credit team focused on property feasibility and net asset value",
            "Rapid commercial execution compared to traditional institutional lenders",
        ],
        "cons": [
            "High minimum loan sizes designed for commercial and development borrowers",
            "Institutional structuring and management fees",
            "Not suited for standard individual home purchases",
        ],
    },
    {
        "slug": "pepper-money-mortgage-review",
        "name": "Pepper Money",
        "full_name": "Pepper New Zealand Limited",
        "category": "non-bank specialist",
        "tier": "Tier 2",
        "founded": "2000 (Australasia)",
        "positioning": "a multi-award-winning non-bank specialist recognized for common-sense credit underwriting and transparent tiering",
        "specialties": "self-employed mortgages (Alt-Doc), credit recovery loans, debt consolidation, flexible LVR residential options",
        "best_for": "borrowers declined by major banks due to living expense calculations, complex income, or isolated credit blemishes",
        "pros": [
            "Pragmatic human underwriting without black-box algorithmic rejection",
            "Three clear transparent tiers (Prime, Near Prime, and Specialist)",
            "Market-leading Alt-Doc options accepting 6 months bank statements or accountant letters",
            "Structured credit repair roadmap designed to refinance clients back to prime banks",
        ],
        "cons": [
            "Interest rates scale with risk classification",
            "Non-bank risk fees may apply on specialist product tiers",
            "Conservative lending policies on high-density studio apartments",
        ],
    },
    {
        "slug": "prospa-finance-review",
        "name": "Prospa",
        "full_name": "Prospa NZ Limited",
        "category": "SME & commercial finance",
        "tier": "Tier 2 (specialist)",
        "founded": "2012",
        "positioning": "Australasia's leading small business lending specialist providing rapid cashflow and property-backed commercial facilities",
        "specialties": "business loans, lines of credit, commercial property-backed finance, working capital solutions",
        "best_for": "small business owners needing fast commercial funding without tying up personal residential mortgages",
        "pros": [
            "Ultra-fast credit decisions with approvals often delivered on the same day",
            "Funding dispatched within 24 hours of loan agreement completion",
            "Minimal documentation required for qualifying small business operators",
            "Preserves personal residential borrowing capacity by keeping business debt separated",
        ],
        "cons": [
            "Commercial interest rates higher than 30-year residential mortgage rates",
            "Shorter loan durations (typically 1 to 5 years)",
            "Restricted to business and commercial purposes only",
        ],
    },
    {
        "slug": "sbs-mortgage-review",
        "name": "SBS",
        "full_name": "Southland Building Society (SBS Bank)",
        "category": "registered bank",
        "tier": "Tier 1 (mutual bank)",
        "founded": "1869",
        "positioning": "New Zealand's oldest customer-owned mutual bank, operating with a deep focus on first home buyers and members",
        "specialties": "FirstHome Combo package, competitive fixed home loans, KiwiSaver, reverse mortgages",
        "best_for": "first home buyers looking for market-leading welcome rates, customer-owned banking, and competitive cashback",
        "pros": [
            "Renowned for aggressive promotional first home buyer mortgage packages",
            "Customer-owned mutual structure where profits are reinvested in New Zealand",
            "Personal service delivered by dedicated home loan lending managers",
            "Full registered bank security and RBNZ regulatory supervision",
        ],
        "cons": [
            "Smaller physical branch footprint in the northern North Island",
            "Conservative servicing stress rates matching prudential bank rules",
            "Turnaround times can lengthen during heavily publicized rate campaigns",
        ],
    },
    {
        "slug": "southern-cross-partners-review",
        "name": "Southern Cross Partners",
        "full_name": "Southern Cross Partners Limited",
        "category": "mortgage & P2P finance",
        "tier": "Tier 2 (peer-to-peer / mortgage fund)",
        "founded": "1997",
        "positioning": "a New Zealand-owned peer-to-peer and mortgage lending specialist connecting borrowers with secured private funding",
        "specialties": "short-term residential mortgages, bridging finance, equity release, business purpose property loans",
        "best_for": "borrowers needing short-term property-backed loans where speed and flexibility are paramount",
        "pros": [
            "Over 25 years of continuous New Zealand lending heritage",
            "Fast, practical loan approvals based primarily on underlying property security",
            "Flexible interest-only payment schedules tailored for property transactions",
            "Assessed by experienced Kiwi underwriters with local market insight",
        ],
        "cons": [
            "Risk-rated interest rates sit above long-term retail bank mortgages",
            "Establishment and brokerage fees apply on loan origination",
            "Facilities are tailored for short-to-medium horizons (6 to 24 months)",
        ],
    },
    {
        "slug": "co-operative-bank-mortgage-review",
        "name": "The Co-operative Bank",
        "full_name": "The Co-operative Bank Limited",
        "category": "registered bank",
        "tier": "Tier 1 (customer-owned bank)",
        "founded": "1928 (as PSIS) / 2011 (bank licence)",
        "positioning": "the only registered bank in New Zealand that shares its annual profits directly with its customers as rebates",
        "specialties": "residential mortgages, annual customer profit sharing, competitive fixed rates, first home buyers",
        "best_for": "borrowers wanting ethical, customer-owned registered banking where mortgage holders receive annual cash rebates",
        "pros": [
            "Annual customer profit-sharing rebates paid directly into borrower accounts",
            "Consistently tops NZ customer satisfaction and banking trust surveys",
            "Full RBNZ registered bank protection and deposit safety",
            "Competitive carded rates on 1, 2, and 3-year fixed mortgage terms",
        ],
        "cons": [
            "Branch network is smaller than the Big 4 retail banks",
            "Conservative servicing stress tests in compliance with bank standards",
            "Selective lending policy on high-LVR or low-deposit applications",
        ],
    },
    {
        "slug": "unity-credit-union-review",
        "name": "Unity Credit Union Home Loans",
        "full_name": "Unity Credit Union (formerly NZCU)",
        "category": "credit union",
        "tier": "Tier 2 (financial cooperative)",
        "founded": "1970s (heritage across regional credit unions)",
        "positioning": "New Zealand's leading member-owned financial cooperative providing accessible, human-led home loans",
        "specialties": "residential mortgages, first home buyers, low-deposit lending, personalized common-sense loan assessments",
        "best_for": "everyday Kiwis seeking a genuine member-owned alternative with human credit underwriters and transparent fee structures",
        "pros": [
            "100% member-owned financial cooperative with no profit extraction by overseas shareholders",
            "Competitive fixed rates that often match or beat mainstream bank specials",
            "Human underwriting team that evaluates individual character and savings history",
            "Transparent fee structure with community-focused financial guidance",
        ],
        "cons": [
            "Not a registered bank (regulated under RBNZ as a Non-Bank Deposit Taker)",
            "Smaller branch network across metropolitan centers",
            "Conservative loan caps on unconventional or specialized property types",
        ],
    },
    {
        "slug": "xceda-finance-review",
        "name": "Xceda Finance",
        "full_name": "Xceda Finance Limited",
        "category": "non-bank lender",
        "tier": "Tier 2 (specialist)",
        "founded": "1988",
        "positioning": "a long-standing New Zealand non-bank financier providing versatile property, business, and asset finance",
        "specialties": "residential property finance, bridging loans, second mortgages, business and commercial funding",
        "best_for": "property investors and business owners seeking versatile non-bank finance with fast turnarounds and flexible securities",
        "pros": [
            "Over 35 years of continuous operation in the New Zealand lending industry",
            "Highly responsive credit team offering rapid preliminary assessments",
            "Accepts flexible security arrangements including second mortgages and caveat equity",
            "Pragmatic approach to evaluating self-employed income and property assets",
        ],
        "cons": [
            "Interest rates carry a non-bank premium over retail bank specials",
            "Facility establishment, documentation, and line fees apply",
            "Shorter loan durations compared to 30-year mainstream bank mortgages",
        ],
    },
]


def h1_qualifier(lender: dict) -> str:
    cat = lender["category"].lower()
    if "bank" in cat:
        return "Home Loan"
    if "credit union" in cat:
        return "Home Loan"
    return "Mortgage"


def title_for(lender: dict) -> str:
    name = lender["name"]
    qual = h1_qualifier(lender)
    cat_cap = lender["category"].title()
    return f"{name} {qual} Review 2026 | {cat_cap} | Finch"


def description_for(lender: dict) -> str:
    name_clean = lender['name'].split(' (')[0]
    return (
        f"Independent {name_clean} mortgage review for NZ borrowers — compare rates, "
        f"deposit rules, and how Finch matches you across our 23 approved NZ lenders."
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
        "23 lenders NZ",
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
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}/lenders/{lender['slug']}.html"},
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
        <h1>{f"{name} {h1_qualifier(lender)}".rstrip()} <em style="font-style:italic;color:var(--finch-forest);">Review.</em></h1>
        <p>{description_for(lender)}</p>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
          <a class="btn-primary" href="../contact.html">Compare {name} with 23 NZ Lenders</a>
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
          <p style="margin-bottom:2rem;">{full_name} is {lender['positioning']}. For New Zealand borrowers, the lender's specialties include {lender['specialties']}. As an independent NZ mortgage broker, Finch arranges home and property loans through our approved panel of 23 lenders — registered NZ banks (ANZ, BNZ, Heartland Bank, SBS Bank, The Co-operative Bank, China Construction Bank), specialist non-bank lenders (Avanti Finance, Basecorp Finance, Pepper Money, Liberty Financial, First Mortgage Trust, General Finance, Cressida Capital, CFML, DBR, Finbase, Funding Partners, GEM By Latitude, Pallas Capital, Southern Cross Partners, Prospa, Xceda Finance), and member-owned credit unions (Unity Credit Union) — so we recommend {name} only when their credit policy and pricing genuinely beat the alternatives for your exact situation.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Who {name} Suits Best</h3>
          <p style="margin-bottom:2rem;">{name} suits {lender['best_for']}. We see strongest outcomes when the client's income profile, deposit position, and intended property align with {name}'s current credit appetite. Outside those scenarios, another lender on our 23-lender panel will usually price sharper or move faster — which is why we compare every option before recommending.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{name} — Strengths</h3>
          <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">{pros_html}</ul>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{name} — Considerations</h3>
          <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">{cons_html}</ul>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">How {name} Compares Across Our 23 Approved Lenders</h3>
          <p style="margin-bottom:2rem;">No single lender wins for every scenario. Pricing and policy vary based on your circumstances — registered banks provide sharp carded fixed rates for clean PAYE borrowers, while non-bank lenders like Avanti Finance, Basecorp Finance, or Pepper Money pick up cases that need common-sense credit assessments. Use our <a href="../mortgage-rates.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">live NZ rates comparison</a> to see current pricing, then book a free consultation to match your scenario across our full approved panel.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">The Rules Every NZ Lender Works Within</h3>
          <p style="margin-bottom:2rem;">{name}'s deposit and serviceability settings sit inside the regulatory framework established in New Zealand — the <a href="https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">RBNZ loan-to-value (LVR) and debt-to-income (DTI) restrictions</a> define the baseline every lender must work within. As an FMA-licensed financial advice provider, Finch is bound by the <a href="https://www.fma.govt.nz/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Financial Markets Authority</a> Code of Conduct to recommend {name} only when it genuinely fits your requirements.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Documents {name} Typically Requires</h3>
          <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">
            <li style="margin-bottom:0.5rem;">3 months payslips (PAYE) or latest financial statements / bank cashflows (self-employed)</li>
            <li style="margin-bottom:0.5rem;">3 months bank statements across active accounts and credit facilities</li>
            <li style="margin-bottom:0.5rem;">KiwiSaver statement and confirmation of first-home eligibility (if applicable)</li>
            <li style="margin-bottom:0.5rem;">NZ photo ID and proof of address for AML / CFT compliance</li>
            <li style="margin-bottom:0.5rem;">Evidence of deposit funds, gifted equity, or existing property equity</li>
          </ul>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Service Coverage Across New Zealand</h3>
          <p style="margin-bottom:2rem;">Finch arranges {name} property lending for clients across the country — Auckland, Wellington, Christchurch, Hamilton, Tauranga, Dunedin, Palmerston North, Napier, Nelson, Queenstown, and regional New Zealand. We manage the entire application from initial assessment through to settlement.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Should You Go Direct, or Use an Independent Broker?</h3>
          <p style="margin-bottom:1rem;">Approaching {name} directly gives you only their proprietary products and credit criteria. Using Finch costs you nothing for residential home loans — where approved, the lender pays our commission on settlement — and you receive an objective comparison across our entire panel of 23 approved lenders. Read our real <a href="../case-studies.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">NZ client case studies</a> to see how we structure approvals.</p>
        </div>
      </div>
    </section>

    <!-- Related NZ Resources -->
    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>Compare More NZ Lenders</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Other NZ lender reviews &amp; resources</h2>
        <div class="cols-3" style="gap:1.5rem;">
          <a href="../lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">All 23 Lenders</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Browse our full approved panel.</span></a>
          <a href="../lenders/major-banks.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Registered Banks</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">ANZ, BNZ, Heartland, SBS, Co-op.</span></a>
          <a href="../lenders/non-bank-lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Non-Bank Lenders</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Avanti, Basecorp, Pepper, Liberty, FMT.</span></a>
          <a href="../mortgage-rates.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Live NZ Mortgage Rates</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Compare registered bank fixed rates.</span></a>
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
          <p>Free 15-minute consultation. We match your scenario against our 23 approved NZ lenders — including {name} — and recommend the sharpest option.</p>
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
    head_close = template_text.find("</head>")
    if head_close == -1:
        raise SystemExit("Template missing </head>")

    head = template_text[: head_close]
    title = title_for(lender)
    description = description_for(lender)
    canonical = f"{BASE_URL}/lenders/{lender['slug']}.html"
    keywords = keywords_for(lender)
    schema = schema_for(lender)

    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta\b[^>]*?name\s*=\s*["\']description["\'][^>]*?>',
        f'<meta name="description" content="{description}"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<link\b[^>]*?rel\s*=\s*["\']canonical["\'][^>]*?>',
        f'<link href="{canonical}" rel="canonical"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<meta\b[^>]*?name\s*=\s*["\']keywords["\'][^>]*?>',
        f'<meta name="keywords" content="{keywords}"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<meta\b[^>]*?property\s*=\s*["\']og:title["\'][^>]*?>',
        f'<meta property="og:title" content="{title}"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<meta\b[^>]*?property\s*=\s*["\']og:description["\'][^>]*?>',
        f'<meta property="og:description" content="{description}"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<meta\b[^>]*?property\s*=\s*["\']og:url["\'][^>]*?>',
        f'<meta property="og:url" content="{canonical}"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<meta\b[^>]*?name\s*=\s*["\']twitter:title["\'][^>]*?>',
        f'<meta name="twitter:title" content="{title}"/>',
        head,
        flags=re.I
    )
    head = re.sub(
        r'<meta\b[^>]*?name\s*=\s*["\']twitter:description["\'][^>]*?>',
        f'<meta name="twitter:description" content="{description}"/>',
        head,
        flags=re.I
    )
    if re.search(r"<script type=\"application/ld\+json\">.*?</script>", head, flags=re.S):
        head = re.sub(
            r"<script type=\"application/ld\+json\">.*?</script>",
            lambda _m: schema,
            head,
            count=1,
            flags=re.S,
        )
    else:
        head = head + "\n" + schema

    head += "</head>"

    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]

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
