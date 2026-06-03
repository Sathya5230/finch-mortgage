"""Generate new NZ case studies with diverse client scenarios.

Reuses the head + footer wrappers from an existing case study to keep
nav, styles, and breadcrumb structure consistent.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "case-studies/refinance-savings.html"
OUT_DIR = ROOT / "case-studies"
BASE_URL = "https://www.finchmortgages.co.nz"

# ISO 8601 dates for Article rich-result eligibility
ARTICLE_PUBLISHED = "2026-01-15"
ARTICLE_MODIFIED = "2026-06-03"


CASE_STUDIES = [
    {
        "slug": "new-migrant-first-mortgage",
        "tag": "Migrant Buyer — Case Study",
        "title_short": "New Migrant Buys First Auckland Home",
        "h1_top": "New Zealand Migrant Buys",
        "h1_bottom": "Their First Auckland Home in 14 Months.",
        "summary": "A UK-trained engineer who moved to Auckland 14 months earlier had no NZ credit history but strong income. Finch matched him to a lender comfortable with short residency.",
        "stats": [
            ("14 mo", "NZ Residency"),
            ("$120K", "Salary"),
            ("12%", "Deposit"),
            ("$780K", "Property"),
            ("21 days", "To Pre-Approval"),
        ],
        "situation": [
            "Daniel moved to Auckland from the UK in early 2025 on a Skilled Migrant pathway, working as a senior engineer for an Auckland infrastructure firm. By April 2026 he'd been in NZ 14 months on a permanent role with a clean local employment record. He had saved roughly $95,000 for a deposit (held partly in KiwiSaver from contributions during his first 12 months, partly in his personal savings account).",
            "When Daniel approached his own bank, they declined his application. Their stated reason: insufficient NZ credit history. He had no defaults, no missed payments, and a strong UK credit history — but the bank's automated scorecard required at least 2 years of NZ credit file activity before recommending approval. Daniel was frustrated and almost gave up on buying for another year.",
            "He reached Finch after a colleague mentioned that brokers can access lenders with more flexible migrant policies. We assessed his full position and confirmed several main banks (plus a strong non-bank option) would absolutely consider his application — the trick was selecting the right lender and presenting the file in the way each lender's credit team prefers.",
        ],
        "approach": [
            ("Migrant-friendly lender selection", "We identified three NZ lenders whose current scorecard treats Skilled Migrant residents favourably when they hold a permanent role and clean employment record — and one specialist non-bank as a back-up. Each had different documentation expectations for international applicants."),
            ("Cross-border income evidence", "We compiled Daniel's UK-employer reference letter, NZ employment contract, 6 months of NZ payslips, NZ IRD tax assessment, plus a UK credit reference report to demonstrate his repayment history overseas. This addressed every reasonable lender concern up front."),
            ("LVR-band optimisation", "With his $95K deposit plus KiwiSaver of $11K (after 12 months of contributions) at a $780,000 price point, his LVR sat at 86% — above the standard 80% main-bank threshold. We selected a lender whose Low Equity Premium pricing was sharpest for the 80-90% LVR band, saving ~0.35% versus other lenders' premiums."),
            ("Pre-approval before competing", "We secured the pre-approval before Daniel made his auction bid, giving him certainty on his upper limit and the confidence to bid against established Kiwi buyers without finance conditions."),
        ],
        "outcome": [
            "Daniel's pre-approval was issued within 21 days of full document submission, against an initial main-bank decline. He attended his second auction with a $780,000 ceiling and secured a 4-bedroom Papakura family home for $762,000 — under his ceiling and with $18,000 of his approved capacity unused.",
            "Settlement occurred 5 weeks after the auction, on time. Daniel's first NZ mortgage was structured as a 50/50 split between a 2-year fixed at 5.79% and a floating portion he plans to attack with extra repayments from his bonus and tax refund each year. Total cost to Daniel: $0 — the lender paid Finch on settlement.",
            "His feedback: \"My own bank told me I'd have to wait another year. Finch found me a lender comfortable with my situation and structured the loan in a way I'd never have known to ask for. The whole process was 6 weeks from first conversation to keys.\"",
        ],
    },
    {
        "slug": "single-parent-rebuilds",
        "tag": "Single Parent — Case Study",
        "title_short": "Single Parent Rebuilds After Divorce",
        "h1_top": "Single Parent",
        "h1_bottom": "Buys Back Into Wellington Post-Divorce.",
        "summary": "A Wellington physiotherapist with two children sold the family home in divorce settlement. Finch helped her re-enter the market on a single income.",
        "stats": [
            ("$95K", "Annual Income"),
            ("12%", "Deposit"),
            ("$680K", "Property"),
            ("17 days", "Pre-Approval"),
            ("0", "Compromises"),
        ],
        "situation": [
            "Rebecca is a 37-year-old senior physiotherapist working for a Wellington DHB. Following a divorce in late 2025, the family home in Karori was sold and the proceeds split — leaving Rebecca with $82,000 deposit savings plus her KiwiSaver balance of $26,000. She wanted to buy back into Wellington as quickly as possible to maintain stability for her two primary-school children.",
            "The challenges were significant: her income at $95,000 had to service a Wellington-priced mortgage on a single income; she'd been declared as a co-borrower on the prior mortgage, so her credit file showed the historic loan; and as the children's primary caregiver, she received Working for Families tax credits which her own bank refused to count toward serviceability.",
            "When she approached the bank she'd held the original mortgage with, they offered her borrowing capacity of just $480,000 — well short of what Wellington's market required even for a modest 3-bedroom home. She was advised to consider renting for 2-3 years before reapplying. Rebecca reached out to Finch as a second opinion before accepting that recommendation.",
        ],
        "approach": [
            ("Working for Families income inclusion", "Multiple NZ lenders accept Working for Families and Best Start payments as income for serviceability, where it's evidenced by IRD statements and projected to continue. We presented Rebecca's case to lenders who count this income, which lifted her borrowing capacity by ~$80,000 immediately."),
            ("Clean credit file presentation", "We worked with her to obtain a current Centrix and Equifax credit report, confirming her credit file was clean despite the divorce. The historic mortgage was correctly recorded as paid out at settlement, not as a default."),
            ("Lender match for single-parent scenarios", "Three NZ main banks plus one specialist non-bank each treat single-parent applications differently. We selected the lender whose stress-test rate and living-expense floor combination produced the most generous outcome for Rebecca's specific circumstances."),
            ("KiwiSaver + savings deposit stack", "Rebecca's $82,000 personal savings + $26,000 KiwiSaver withdrawal (she'd held KiwiSaver 8+ years and had repaid her previous first home withdrawal during her marriage) combined to give her a 16% deposit on a $680,000 property — close to the standard 20% threshold with a manageable Low Equity Premium."),
        ],
        "outcome": [
            "Rebecca secured pre-approval of $570,000 — almost $90,000 above her own bank's offer — within 17 days of submission. She purchased a 3-bedroom townhouse in Newtown for $678,000 (close to school and her workplace), settling 6 weeks later.",
            "Her loan was structured as a 70/30 split: 70% on a 2-year fixed at 5.69%, 30% floating so she could attack the principal with annual tax refunds and bonus income. She also captured a $4,200 cashback contribution from the new lender, which fully covered her solicitor and moving costs.",
            "Rebecca's feedback: \"Three months earlier I was told I'd have to rent for years. Finch took my actual situation seriously instead of plugging me into a single bank's tick-box calculator. The kids are settled in our own home and life is moving forward again.\"",
        ],
    },
    {
        "slug": "apartment-investor-scaling",
        "tag": "Investor Scaling — Case Study",
        "title_short": "Apartment Investor Scales to 5 Properties",
        "h1_top": "Apartment Investor",
        "h1_bottom": "Scales From 1 Property to 5 in 18 Months.",
        "summary": "A Hamilton-based investor used equity recycling, new-build LVR exemption, and a multi-lender structure to grow a portfolio of 5 income properties.",
        "stats": [
            ("1 → 5", "Properties"),
            ("18 mo", "Timeframe"),
            ("$2.1M", "Portfolio Value"),
            ("3 lenders", "Diversified"),
            ("$0", "Fresh Cash"),
        ],
        "situation": [
            "James, a 41-year-old Hamilton engineer earning $145,000, owned a single investment property valued at $620,000 with a $310,000 mortgage. He had a clear goal: grow to 5 income properties within 2 years to support semi-retirement by age 50. His own bank told him he could potentially add one more property — but no more — using the equity in his existing property.",
            "His existing bank's serviceability calculation treated rental income at 70% shading and applied their high test rate to both his existing and any new debt. The combined assessment showed he'd reach his investor LVR cap quickly. James felt stuck — the path to 5 properties seemed mathematically impossible without significant cash injection.",
            "James met Finch through a referral from his accountant. We modelled his portfolio across the full NZ lender panel, including specialist non-banks comfortable with multi-property investors. The result: a sequencing strategy that would let him hit his target within his original timeframe without injecting fresh cash.",
        ],
        "approach": [
            ("Equity recycling from existing property", "We refinanced his existing investment property with a new lender at a sharper rate and split structure, releasing $124,000 of usable equity (within the 65% LVR investor cap) without selling the asset. That equity became the deposit for property #2."),
            ("New-build LVR exemption strategy", "Properties #2, #3, and #4 were all new-build purchases in growth Hamilton suburbs (Rototuna and Flagstaff). New builds are LVR-speed-limit exempt, allowing 80% LVR on each rather than the 65% investor cap — meaning his equity went much further per purchase."),
            ("Three-lender diversification", "Rather than concentrate all loans with one bank (which compounds serviceability constraints), we placed each property with a different lender — main bank for properties #1 and #2, a regional bank for #3 and #4, and a specialist non-bank for #5. This stand-alone structure preserved his serviceability headroom at each step."),
            ("Interest-only structuring on investment properties", "All five properties were structured with 2-5 year interest-only periods, maximising cash flow during the scaling phase. With interest deductibility restored from April 2025, the strategy is tax-efficient and supports continued portfolio growth."),
        ],
        "outcome": [
            "James reached 5 properties exactly 18 months after his first conversation with Finch. Combined portfolio value: $2,100,000. Combined borrowings: $1,540,000. Combined gross rent: ~$2,650/week. He invested $0 of fresh cash — every purchase was funded through equity recycling and the new-build LVR exemption.",
            "His existing property (now property #1) was refinanced again at month 12 of the journey to capture continued equity growth and a $4,800 cashback contribution. His total cashback collected across the 5 transactions: $18,400.",
            "James's feedback: \"My existing bank told me one more was the limit. Working with Finch and structuring across multiple lenders meant the limit was actually about 5 — and I got there inside the timeframe I set. The semi-retirement plan is now well on track.\"",
        ],
    },
    {
        "slug": "family-guarantee-first-home",
        "tag": "Low-Deposit FHB — Case Study",
        "title_short": "First Home With 8% Deposit Plus Family Guarantee",
        "h1_top": "First Home Buyer",
        "h1_bottom": "Crosses the Line with an 8% Deposit + Family Guarantee.",
        "summary": "A young Christchurch couple bought their first home with just 8% saved, using a family guarantee from her parents to bridge the deposit gap without injecting fresh cash.",
        "stats": [
            ("8%", "Their Deposit"),
            ("$520K", "Property Price"),
            ("$0", "Family Cash"),
            ("$8K", "Cashback"),
            ("28 days", "To Pre-Approval"),
        ],
        "situation": [
            "Liam and Aroha are a young couple in their late 20s living in Christchurch — Liam works as an early-career civil engineer ($82,000) and Aroha as a registered nurse ($78,000). They'd been saving for 4 years and had $41,000 in savings plus $19,000 in combined KiwiSaver. On a $520,000 starter home in Halswell, that gave them an 11.5% deposit including KiwiSaver — well short of the 20% main-bank threshold.",
            "They'd been told repeatedly by Christchurch agents and one bank visit that they should keep saving for another 18-24 months. Aroha's parents, who owned their Hornby home mortgage-free, had offered to help — but Liam was uncomfortable with the idea of accepting cash from family, and her parents preferred not to liquidate any savings either.",
            "When they approached Finch, we explained that the family guarantee structure available across all main NZ banks allows family equity to support a deposit without requiring family cash. Aroha's parents would essentially co-pledge a portion of their home equity (which they'd never need to liquidate) to bridge the LVR gap for Liam and Aroha's loan — a clean, well-established NZ structure.",
        ],
        "approach": [
            ("Family Guarantee structure", "We explained the Family Guarantee facility to Aroha's parents in detail — including the strictly limited exposure (capped at the gap amount, ~$62,000, not the whole loan), the release mechanism once Liam and Aroha's equity grows to 20% of property value, and the requirement for independent legal advice for the guarantors. Aroha's parents agreed."),
            ("Independent legal advice for guarantors", "We coordinated with a solicitor to provide Aroha's parents independent legal advice on the guarantee — a regulatory requirement designed to protect family guarantors from undue pressure. The advice confirmed the guarantee was limited, well-structured, and unlikely to crystallise unless Liam and Aroha defaulted (which their serviceability comfortably supported)."),
            ("Lender selection for family guarantee", "Three of the main NZ banks offer family guarantee facilities under different brand names. We selected the lender whose family guarantee terms were cleanest, paired with the sharpest current 2-year fixed rate, and offered an $8,000 cashback contribution to cover Liam and Aroha's legal fees, valuation, and moving costs."),
            ("Release strategy planning", "We modelled the timeline for Aroha's parents' guarantee release. With expected Christchurch property growth plus principal repayment, Liam and Aroha's equity should cross the 20% LVR mark in approximately 3-4 years, at which point the family guarantee is fully released and Aroha's parents' home title is unencumbered again."),
        ],
        "outcome": [
            "Pre-approval was issued within 28 days. Liam and Aroha purchased a 3-bedroom Halswell home for $518,000, just under their $520,000 ceiling. Settlement occurred 5 weeks later. Their loan was structured 70/30 — 70% on a 2-year fixed at 5.69%, 30% floating to allow extra repayments.",
            "The $8,000 cashback contribution from the new lender fully covered their solicitor fees, valuation, and moving costs — meaning the move was effectively cost-neutral despite the lender requiring no fresh family cash. Aroha's parents' home title carries a strictly limited second mortgage that will release automatically once equity hits 20%.",
            "Liam's feedback: \"We were told to wait two more years. Two months later we had keys. Finch found a structure that worked for everyone — including Aroha's parents, who got proper legal advice and were genuinely comfortable with the protections built in.\"",
        ],
    },
]


def schema_for(c: dict) -> str:
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": f"{BASE_URL}/case-studies.html"},
            {"@type": "ListItem", "position": 3, "name": c["title_short"], "item": f"{BASE_URL}/case-studies/{c['slug']}.html"},
        ],
    }
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": c["title_short"],
        "description": c["summary"],
        "url": f"{BASE_URL}/case-studies/{c['slug']}.html",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}/case-studies/{c['slug']}.html"},
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
    }
    return (
        "<script type=\"application/ld+json\">"
        + json.dumps(breadcrumb, indent=2)
        + "</script>\n<script type=\"application/ld+json\">"
        + json.dumps(article, indent=2)
        + "</script>"
    )


def keywords_for(c: dict) -> str:
    base = [
        "NZ mortgage case study",
        c["title_short"].lower(),
        "NZ mortgage broker case study",
        "real NZ home loan story",
        "Finch Mortgages case study",
        "NZ home loan client story",
    ]
    return ", ".join(base)


def title_for(c: dict) -> str:
    # Kept under 60 characters so titles don't truncate in SERPs.
    return f"{c['title_short']} | Finch"


def main_body(c: dict) -> str:
    stats_html = "".join(
        textwrap.dedent(f"""
            <div style=\"text-align:center;\">
              <div style=\"font-size:2.5rem;font-weight:800;color:var(--finch-gold);line-height:1;\">{value}</div>
              <div style=\"font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.65);margin-top:0.3rem;\">{label}</div>
            </div>
        """)
        for value, label in c["stats"]
    )

    situation_html = "".join(f"<p style=\"color:var(--neutral-medGray);line-height:1.8;margin-bottom:1rem;\">{p}</p>" for p in c["situation"])

    approach_html = ""
    for idx, (heading, body) in enumerate(c["approach"], start=1):
        approach_html += textwrap.dedent(f"""
            <div style=\"display:flex;gap:1.25rem;align-items:flex-start;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;\">
              <div style=\"width:2rem;height:2rem;background:var(--finch-forest);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;\"><span style=\"color:white;font-size:0.7rem;font-weight:800;\">{idx}</span></div>
              <div><strong style=\"display:block;margin-bottom:0.3rem;color:var(--finch-forest);\">{heading}</strong><span style=\"color:var(--neutral-medGray);font-size:0.95rem;line-height:1.6;\">{body}</span></div>
            </div>
        """)

    outcome_html = "".join(f"<p style=\"color:var(--neutral-medGray);line-height:1.8;margin-bottom:1rem;\">{p}</p>" for p in c["outcome"])

    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <section class="container page-hero" style="padding-bottom:3rem; max-width:780px;">
      <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../case-studies.html">Case Studies</a><span class="breadcrumb-sep">/</span><span>{c['title_short']}</span></nav>
      <div class="page-hero-tag">{c['tag']}</div>
      <h1>{c['h1_top']}<br/><em style="font-style:italic;color:var(--finch-forest);">{c['h1_bottom']}</em></h1>
      <p>{c['summary']}</p>
    </section>

    <section style="background:var(--finch-forest);padding:2.5rem 0;">
      <div class="container">
        <div style="display:flex;gap:3rem;flex-wrap:wrap;justify-content:center;">
          {stats_html}
        </div>
      </div>
    </section>

    <section style="padding:5rem 0;background:white;">
      <div class="container" style="max-width:780px;">
        <div style="margin-bottom:3.5rem;">
          <div class="section-label" style="margin-bottom:1rem;"><span>The Situation</span></div>
          <h2 class="section-heading" style="margin-bottom:1.5rem;">The problem.</h2>
          {situation_html}
        </div>

        <div style="margin-bottom:3.5rem;">
          <div class="section-label" style="margin-bottom:1rem;"><span>The Finch Approach</span></div>
          <h2 class="section-heading" style="margin-bottom:1.5rem;">How we solved it.</h2>
          <div style="display:flex;flex-direction:column;gap:1.25rem;">
            {approach_html}
          </div>
        </div>

        <div style="margin-bottom:1rem;">
          <div class="section-label" style="margin-bottom:1rem;"><span>The Outcome</span></div>
          <h2 class="section-heading" style="margin-bottom:1.5rem;">The result.</h2>
          {outcome_html}
          <p style="color:var(--neutral-medGray);line-height:1.8;margin-top:1.5rem;font-size:0.95rem;">Useful NZ sources: the <a href="https://www.rbnz.govt.nz/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Reserve Bank of New Zealand</a> for current lending policy, and <a href="https://kaingaora.govt.nz/en_NZ/home-ownership/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Kāinga Ora</a> for first-home support schemes.</p>
        </div>
      </div>
    </section>

    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>More NZ Stories</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ case studies &amp; tools</h2>
        <div class="cols-3" style="gap:1.5rem;">
          <a href="../case-studies.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">All NZ Case Studies</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Real client outcomes across scenarios.</span></a>
          <a href="../testimonials/reviews.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Client Reviews</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">5.0 star Google rating.</span></a>
          <a href="../testimonials/success-stories.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Success Stories</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">In-depth client journeys.</span></a>
          <a href="../calculators/borrowing-power.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Borrowing Power</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">See your NZ borrowing capacity.</span></a>
          <a href="../services/home-loan.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Home Loan Service</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Start your own approval.</span></a>
          <a href="../contact.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Book a Free Call</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">15-min discovery, no obligation.</span></a>
        </div>
      </div>
    </section>

    <section style="padding:5rem 0;">
      <div class="container">
        <div class="cta-section reveal">
          <h2>Could we help you<br/>get the same result?</h2>
          <p>Book a free 15-minute consultation. We compare your scenario across 20+ NZ lenders and structure the loan for the best outcome.</p>
          <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
            <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
            <a class="btn-cta-outline" href="../case-studies.html">More NZ Case Studies</a>
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
    description = c["summary"]
    canonical = f"{BASE_URL}/case-studies/{c['slug']}.html"
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
        r'<link href=\"https://www\.finchmortgages\.co\.nz/case-studies/[^\"]+\" rel=\"canonical\"/?>',
        f'<link href="{canonical}" rel="canonical"/>',
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
    for c in CASE_STUDIES:
        out_path = OUT_DIR / f"{c['slug']}.html"
        out_path.write_text(build_page(c, template_text), encoding="utf-8")
        print(f"  + {out_path.relative_to(ROOT)}")
    print(f"\nGenerated {len(CASE_STUDIES)} new case studies.")


if __name__ == "__main__":
    main()
