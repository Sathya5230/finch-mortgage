#!/usr/bin/env python3
"""Per-page title and meta description rewrites for SEO/AEO.

Each entry:
  rel_path: (new_title, new_description)

new_title:        target 50-60 chars, keep primary keywords, brand suffix.
new_description:  target 130-160 chars, action + value + keywords.

NEVER touches first-home-buyers.html (per user instruction).
"""
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SKIP = {"first-home-buyers.html"}

# (path → (title, description))
REWRITES = {
    # ----- HUBS / TOP-LEVEL -----
    "calculators.html": (
        "Free NZ Mortgage Calculators 2026 | Finch Mortgage",
        "Free NZ mortgage calculators — repayment, borrowing power, refinance savings, and extra repayment. No sign-up. Built for Kiwi home buyers and owners.",
    ),
    "case-studies.html": (
        "Mortgage Case Studies NZ | Finch Mortgage",
        "Real Finch Mortgage case studies — first home approvals, refinances, self-employed loans, construction and investment property success stories across New Zealand.",
    ),
    "map.html": (
        "Finch Mortgage Office | Auckland Mortgage Broker",
        "Find Finch Mortgage's Auckland office in Te Atatu South. NZ mortgage broker serving all of New Zealand. Get directions or book a free in-person consultation.",
    ),
    "services-overview.html": (
        "NZ Mortgage Services | Home Loans & More | Finch",
        "Every mortgage service under one roof — home loans, first home buyer, refinance, pre-approval, investment, construction, commercial, asset finance and self-employed.",
    ),
    "mortgage-rates.html": (
        "NZ Mortgage Rates 2026 | Compare ANZ BNZ Kiwibank | Finch",
        "Compare today's NZ mortgage rates across ANZ, BNZ, Kiwibank, ASB, Westpac and more. Live updates, OCR commentary, and expert analysis from Finch Mortgage.",
    ),
    "refinance.html": (
        "Refinance Calculator NZ | Save on Your Mortgage | Finch",
        "Use Finch Mortgage's free NZ refinance tool to compare current rates, estimate break fees, and calculate the savings from switching home loan lenders.",
    ),
    "about.html": (
        "About Finch Mortgage NZ | Independent Mortgage Brokers",
        "Meet the team behind Finch Mortgage — NZ's trusted independent mortgage broker. 15+ years' experience, 500+ Kiwi clients helped, $0 broker fee on every loan.",
    ),
    "faq.html": (
        "Mortgage FAQ NZ 2026 | Common Questions | Finch",
        "Answers to New Zealand's most common mortgage questions — deposits, KiwiSaver withdrawals, pre-approval timelines, lender criteria, and broker fees explained.",
    ),

    # ----- BLOG (long-title fixes only; descs already OK or fixed individually) -----
    "blog/deposit-requirements-nz.html": (
        "NZ Mortgage Deposit Requirements 2026 | Finch",
        "How much deposit do you need for a NZ mortgage in 2026? Standard 20%, low-deposit pathways, KiwiSaver and First Home Grant rules explained by Finch Mortgage.",
    ),
    "blog/mortgage-tips.html": (
        "NZ Mortgage Tips 2026 | Expert Advice | Finch",
        "Practical mortgage tips for NZ home buyers and owners in 2026 — from deposit-saving strategies to refinancing checkpoints and avoiding common loan-application mistakes.",
    ),
    "blog/mortgage-broker-east-auckland.html": (
        "Mortgage Broker East Auckland | Finch Mortgage",
        "Independent mortgage broker for East Auckland — Howick, Pakuranga, Botany, Half Moon Bay. Compare 20+ lenders, get pre-approval, and bid with confidence.",
    ),
    "blog/mortgage-broker-north-shore.html": (
        "Mortgage Broker North Shore Auckland | Finch",
        "Independent mortgage broker for Auckland's North Shore — Takapuna, Albany, Devonport, Browns Bay. Compare 20+ lenders for the best home loan rate and structure.",
    ),
    "blog/mortgage-broker-south-auckland.html": (
        "Mortgage Broker South Auckland | Finch Mortgage",
        "Independent mortgage broker for South Auckland — Manukau, Manurewa, Papakura, Pukekohe. Compare 20+ lenders, secure pre-approval, and find your best home loan rate.",
    ),
    "blog/mortgage-pre-approval-timeline.html": (
        "Mortgage Pre-Approval Timeline NZ | Finch",
        "How long does mortgage pre-approval take in NZ? Typical 3–10 business day timeline, document checklist, and common delays explained by Finch Mortgage.",
    ),
    "blog/loan-declined-what-next-nz.html": (
        "Loan Declined in NZ — What to Do Next | Finch",
        "Mortgage declined? Here's what to do next in NZ — understand the reason, fix common issues, explore non-bank lenders, and reapply successfully with Finch Mortgage.",
    ),

    # ----- CALCULATORS (long titles) -----
    "calculators/borrowing-power.html": (
        "Borrowing Power Calculator NZ | Finch Mortgage",
        "How much can you borrow in NZ? Use Finch Mortgage's free borrowing-power calculator to estimate your maximum home loan based on income, expenses, and deposit.",
    ),
    "calculators/extra-repayment.html": (
        "Extra Repayment Calculator NZ | Finch Mortgage",
        "See how much you'll save on a NZ mortgage by making extra repayments. Finch Mortgage's free calculator shows years and dollars saved over your loan term.",
    ),
    "calculators/refinance-savings.html": (
        "Refinance Savings Calculator NZ | Finch Mortgage",
        "Calculate the savings from refinancing your NZ home loan. Compare your current rate vs market rates and estimate total interest saved with Finch Mortgage.",
    ),

    # ----- CASE STUDIES (long titles) -----
    "case-studies/construction-loan-turnkey.html": (
        "Construction Loan Case Study | Finch Mortgage NZ",
        "A real Finch Mortgage NZ client case study — securing a turnkey construction loan with progress payments and a smooth handover to the homeowner.",
    ),
    "case-studies/portfolio-growth.html": (
        "Investment Portfolio Growth Case Study | Finch",
        "How Finch Mortgage helped a NZ investor scale a property portfolio with DTI-aware structuring, equity release, and lender diversification.",
    ),
    "case-studies/self-employed-approval.html": (
        "Self-Employed Approval Case Study | Finch",
        "A NZ self-employed contractor's mortgage approval story — how Finch Mortgage navigated income proofs and a non-bank lender to secure the home loan.",
    ),

    # ----- GUIDES (long titles) -----
    "guides/first-home-guide.html": (
        "First Home Buyer Guide NZ 2026 | Finch Mortgage",
        "The complete NZ first home buyer guide for 2026 — deposit, KiwiSaver, First Home Grant, pre-approval, and step-by-step settlement from Finch Mortgage.",
    ),
    "guides/refinance-guide.html": (
        "Mortgage Refinance Guide NZ 2026 | Finch",
        "The complete NZ mortgage refinance guide — when to refinance, how break fees work, cashback offers, and switching lenders explained by Finch Mortgage.",
    ),
    "guides/step-by-step.html": (
        "NZ Home Buying — Step-by-Step Guide | Finch",
        "Buying a home in NZ — the complete step-by-step process from deposit to settlement, including pre-approval, offers, conditions and key dates from Finch Mortgage.",
    ),

    # ----- SERVICES (long titles + long descs) -----
    "services/first-home-buyer.html": (
        "First Home Buyer Loans NZ | Finch Mortgage",
        "NZ first home buyer mortgage advice — KiwiSaver withdrawal, First Home Grant, low-deposit lending, and pre-approval support from Finch Mortgage.",
    ),
    "services/next-home-buyer.html": (
        "Next Home Buyer Mortgage NZ | Finch Mortgage",
        "Upgrading your NZ home? Finch Mortgage structures bridging finance, sell-then-buy, and buy-then-sell strategies across 20+ lenders.",
    ),
    "services/refinance.html": (
        "Refinance Mortgage NZ | Finch Mortgage Broker",
        "Refinance your NZ mortgage with Finch — lower rate, better structure, or cashback. Independent advice across 20+ lenders at $0 broker fee.",
    ),
    "services/home-loan.html": (
        "Home Loans NZ | Best Mortgage Rates | Finch",
        "Independent NZ home loan advice — Finch Mortgage compares 20+ lenders to find the best rate and structure for your purchase. $0 broker fee.",
    ),
    "services/construction-loan.html": (
        "Construction Loans NZ | Finch Mortgage Broker",
        "Construction mortgage advice for NZ — progress-payment and turnkey builds, valuation timing, and lender selection from Finch Mortgage.",
    ),
    "services/investment-property.html": (
        "Investment Property Loans NZ | Finch Mortgage",
        "NZ investment property mortgage advice — DTI-aware structuring, rental shading, equity release, and tax-aware loan structure from Finch Mortgage.",
    ),
    "services/self-employed.html": (
        "Self-Employed Home Loans NZ | Finch Mortgage",
        "Self-employed mortgage advice for NZ contractors, sole traders, and limited-company directors. Full-doc and low-doc options through 20+ lenders.",
    ),

    # ----- WEEKLY REPORTS (all long titles) -----
    "weekly-reports/week-1-year-ahead-2026.html": (
        "Week 1: NZ Mortgage Year-Ahead 2026 | Finch",
        "Finch Mortgage NZ Week 1 report: the year-ahead view for mortgage rates, OCR moves, and Kiwi housing market outlook entering 2026.",
    ),
    "weekly-reports/week-2-mortgage-stress-testing.html": (
        "Week 2: NZ Mortgage Stress Testing | Finch",
        "Finch Mortgage NZ Week 2: how banks stress-test mortgage applications and what serviceability rates mean for Kiwi borrowers in 2026.",
    ),
    "weekly-reports/week-3-summer-sales-slump.html": (
        "Week 3: NZ Summer Sales Slump | Finch Reports",
        "Finch Mortgage NZ Week 3: the summer property sales slowdown — listings, buyer activity, and what it means for mortgage strategy.",
    ),
    "weekly-reports/week-4-dti-caps-bite.html": (
        "Week 4: DTI Caps Bite NZ Lending | Finch",
        "Finch Mortgage NZ Week 4: how the RBNZ debt-to-income (DTI) caps are reshaping investment property lending in New Zealand.",
    ),
    "weekly-reports/week-5-new-build-exemptions.html": (
        "Week 5: NZ New-Build Exemptions | Finch",
        "Finch Mortgage NZ Week 5: how new-build LVR exemptions affect first home buyers and investors entering the New Zealand property market.",
    ),
    "weekly-reports/week-6-floating-vs-fixed.html": (
        "Week 6: NZ Floating vs Fixed Rates | Finch",
        "Finch Mortgage NZ Week 6: a deep dive into fixed vs floating mortgage rate strategy for Kiwi borrowers in the current OCR cycle.",
    ),
    "weekly-reports/week-7-kiwisaver-tips.html": (
        "Week 7: KiwiSaver Home-Buying Tips | Finch",
        "Finch Mortgage NZ Week 7: using KiwiSaver for a first home — withdrawal rules, the First Home Grant, and lender treatment.",
    ),
    "weekly-reports/week-8-interest-deductibility.html": (
        "Week 8: NZ Interest Deductibility Update | Finch",
        "Finch Mortgage NZ Week 8: where interest deductibility rules sit for property investors in New Zealand and the cash-flow impact.",
    ),
    "weekly-reports/week-9-bay-of-plenty.html": (
        "Week 9: Bay of Plenty Property Update | Finch",
        "Finch Mortgage NZ Week 9: Bay of Plenty house prices, listing trends, and mortgage demand — where the regional market is heading.",
    ),
    "weekly-reports/week-12-rental-yields.html": (
        "Week 12: NZ Rental Yields Snapshot | Finch",
        "Finch Mortgage NZ Week 12: rental yields across the main NZ cities and what they mean for investment-property mortgage decisions.",
    ),
    "weekly-reports/week-13-canterbury-surge.html": (
        "Week 13: Canterbury Property Surge | Finch",
        "Finch Mortgage NZ Week 13: the Canterbury price surge — what's driving it and how it changes the lending and pre-approval landscape.",
    ),
    "weekly-reports/week-15-ocr-hold.html": (
        "Week 15: RBNZ OCR Hold Decision | Finch",
        "Finch Mortgage NZ Week 15: the RBNZ OCR hold decision, market reaction, and what it means for fixed and floating mortgage rates.",
    ),
    "weekly-reports/week-18-winter-strategies.html": (
        "Week 18: NZ Winter Mortgage Strategies | Finch",
        "Finch Mortgage NZ Week 18: cooler-season strategy for Kiwi borrowers — rate-lock timing, refinance windows, and pre-approval planning.",
    ),

    # ----- Short-description weekly-reports -----
    "weekly-reports/week-10-ocr-cut-march.html": (
        None,
        "Finch Mortgage NZ Week 10: the March OCR cut — market reaction, fixed and floating rate moves, and what it means for borrowers in 2026.",
    ),
    "weekly-reports/week-11-first-home-grant.html": (
        None,
        "Finch Mortgage NZ Week 11: First Home Grant changes — eligibility, regional price caps, and the impact on NZ first home buyers in 2026.",
    ),
    "weekly-reports/week-14-anz-rates.html": (
        None,
        "Finch Mortgage NZ Week 14: ANZ's rate moves — fixed and floating updates and what borrowers across New Zealand should consider next.",
    ),
    "weekly-reports/week-16-major-banks-cut-rates.html": (
        None,
        "Finch Mortgage NZ Week 16: major banks cut mortgage rates — ANZ, ASB, BNZ, Westpac, and Kiwibank moves and what borrowers should do now.",
    ),
    "weekly-reports/week-17-autumn-update.html": (
        None,
        "Finch Mortgage NZ Week 17: autumn 2026 market update — OCR outlook, fixed-rate trends, and Auckland property activity summarised.",
    ),

    # ----- Legal pages with thin description -----
    "disclaimer.html": (
        None,
        "Finch Mortgage NZ website disclaimer — limitation of liability, accuracy of information, third-party links, and use of the finchmortgages.co.nz site.",
    ),
    "disclosure.html": (
        None,
        "Finch Mortgage Publicly Available Disclosure Statement — operating under Finsure NZ Ltd (FSP1010474), commissions, conflicts, and complaints process.",
    ),
}


def fix(path: Path, new_title, new_desc):
    html = path.read_text(encoding="utf-8")
    changed = False

    if new_title:
        new_html, n = re.subn(
            r"<title[^>]*>.*?</title>",
            f"<title>{new_title}</title>",
            html, count=1, flags=re.S | re.I,
        )
        if n:
            html = new_html
            changed = True

        # Update OG / Twitter titles if they exist
        def replace_meta(html, attr, value, new_content):
            pat = re.compile(
                rf'(<meta\b[^>]*?{attr}\s*=\s*["\']' + re.escape(value)
                + r'["\'][^>]*?content\s*=\s*)(?:"([^"]*)"|\'([^\']*)\')',
                re.I,
            )
            pat2 = re.compile(
                r'(<meta\b[^>]*?content\s*=\s*)(?:"([^"]*)"|\'([^\']*)\')(?P<mid>[^>]*?'
                + attr + r'\s*=\s*["\']' + re.escape(value) + r'["\'][^>]*?>)',
                re.I,
            )
            html2, n1 = pat.subn(lambda m: m.group(1) + f'"{new_content}"', html, count=1)
            if n1 == 0:
                html2, n1 = pat2.subn(lambda m: m.group(1) + f'"{new_content}"' + m.group("mid"), html, count=1)
            return html2, n1

        html, _ = replace_meta(html, "property", "og:title", new_title)
        html, _ = replace_meta(html, "name", "twitter:title", new_title)

    if new_desc:
        # description
        def replace_meta_content(html, attr, value, new_content):
            pat = re.compile(
                rf'(<meta\b[^>]*?{attr}\s*=\s*["\']' + re.escape(value)
                + r'["\'][^>]*?content\s*=\s*)(?:"([^"]*)"|\'([^\']*)\')',
                re.I,
            )
            pat2 = re.compile(
                r'(<meta\b[^>]*?content\s*=\s*)(?:"([^"]*)"|\'([^\']*)\')(?P<mid>[^>]*?'
                + attr + r'\s*=\s*["\']' + re.escape(value) + r'["\'][^>]*?>)',
                re.I,
            )
            new_html, n1 = pat.subn(lambda m: m.group(1) + f'"{new_content}"', html, count=1)
            if n1 == 0:
                new_html, n1 = pat2.subn(lambda m: m.group(1) + f'"{new_content}"' + m.group("mid"), html, count=1)
            return new_html, n1

        before = html
        html, n = replace_meta_content(html, "name", "description", new_desc)
        if n:
            changed = True
        html, _ = replace_meta_content(html, "property", "og:description", new_desc)
        html, _ = replace_meta_content(html, "name", "twitter:description", new_desc)

    if changed:
        path.write_text(html, encoding="utf-8")
        return "UPDATED"
    return "NOCHANGE"


def main():
    for rel, (t, d) in REWRITES.items():
        if rel in SKIP or Path(rel).name in SKIP:
            print(f"SKIPPED (protected): {rel}")
            continue
        p = ROOT / rel
        if not p.exists():
            print(f"MISSING: {rel}")
            continue
        status = fix(p, t, d)
        print(f"{status}: {rel}")


if __name__ == "__main__":
    main()
