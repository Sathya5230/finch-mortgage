"""Remove unsourced statistics and promises from refinance and city pages.

The refinance service page quoted an "average monthly saving", an "average
refinance time" and "most Kiwis are overpaying $200–$500/month" with no source.
Three refinance pages gave cashback percentages and dollar caps for named banks,
including ASB, Westpac and TSB, which aren't on Finch's lender panel, and the
refinance guide said Finch compares offers from them. Four Auckland city pages
promised "24hr approval", which only the lender can decide. Rate banners still
said "See Live Rates" for a page that no longer shows live rates.

All of these are Fair Trading Act risks on YMYL pages, so the replacements say
only what Finch can stand behind. Idempotent. Run with --apply to write;
default is a dry run.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

PAIRS = {
    # services/refinance.html hero and stats strip.
    "<p>Is your mortgage rate still stuck from 2–3 years ago? Most Kiwi homeowners are overpaying by $200–$500/month. Finch compares 20+ lenders at no cost to you and handles the entire switch.</p>":
        "<p>Fixed rate ending, or rolled onto a higher rate? Finch compares your bank's offer with the 23 lenders on our panel, works out break fees and any cashback clawback, and handles the switch. For residential home loans our advice costs you nothing.</p>",
    '<div class="stat-item"><div class="stat-number">$340</div><div class="stat-label">Avg Monthly Saving</div></div>\n'
    '<div class="stat-item"><div class="stat-number">2 wks</div><div class="stat-label">Avg Refinance Time</div></div>\n'
    '<div class="stat-item"><div class="stat-number">20+</div><div class="stat-label">Lenders Compared</div></div>':
        '<div class="stat-item"><div class="stat-number">23</div><div class="stat-label">Lenders on Our Panel</div></div>\n'
        '<div class="stat-item"><div class="stat-number">15+ yrs</div><div class="stat-label">Bank Lending Experience</div></div>\n'
        '<div class="stat-item"><div class="stat-number">FSCL</div><div class="stat-label">Independent Complaints Scheme</div></div>',

    # Cashback: no lender list, percentages or caps we can't source or keep current.
    ">NZ Refinance Cashback Offers in 2026</h3>": ">How refinance cashback works in NZ</h3>",
    "Almost every major NZ bank — <strong>ANZ, ASB, BNZ, Westpac, TSB, SBS, The Co-operative Bank, and Heartland</strong> — runs an active refinance cashback campaign. Standard contributions range from 0.50% to 0.90% of the loan amount, capped between $3,000 and $20,000. Cashback is repayable if you discharge the loan within the clawback window (typically 3–4 years).":
        "Many NZ lenders offer a cash contribution when you move your mortgage to them. Amounts, conditions and clawback periods differ between lenders and change often, and the contribution usually has to be repaid if you refinance away again within a set period, commonly a few years.",
    ">NZ Cashback Refinance Offers (2026)</h3>": ">How refinance cashback works</h3>",
    "All major NZ banks — <strong>ANZ, ASB, BNZ, Westpac, TSB, SBS, The Co-operative Bank</strong> — currently run active refinance cashback campaigns. Typical structures pay 0.50%–0.90% of the new loan amount, capped at $3,000–$20,000, with a 3–4 year clawback period if you discharge again before then. Some lenders also contribute toward legal disbursements ($800–$1,500).":
        "Many NZ lenders offer a cash contribution when you refinance to them, and some also contribute towards legal costs. Amounts and conditions vary by lender and change often, and the contribution usually has to be repaid if you leave again within the lender's clawback period. We check current offers from the lenders on our panel when we run your numbers.",
    "All major NZ banks pay 0.50%–0.90% cashback on refinances, capped between $3,000 and $20,000. On a $700,000 refinance, that's $3,500–$6,300 deposited into your account on settlement. Cashback is typically clawback-protected for 3–4 years. Finch nets cashback against your current bank's clawback (if any) and the legal costs (~$1,000–$1,500) so you see your true position.":
        "Many NZ lenders pay a cash contribution when you refinance to them. It's usually a percentage of the loan or a set amount, it varies between lenders and over time, and it usually has to be repaid if you leave within the lender's clawback period. Finch nets any contribution against your current bank's clawback (if any) and the legal costs, so you see your true position.",

    # Refinance guide: ASB, Westpac and TSB aren't on the panel.
    "<strong>Lender match</strong> — we compare offers across <strong>ANZ, ASB, BNZ, Westpac, TSB, SBS, The Co-operative Bank, and Heartland</strong>, plus specialist lenders where appropriate.":
        "<strong>Lender match</strong> — we compare offers from the 23 lenders on our panel, including banks such as <strong>ANZ, BNZ, SBS Bank and The Co-operative Bank</strong>, plus specialist non-bank lenders where appropriate.",

    # The rates page links out to bank rate pages; nothing on it is live.
    ">See Live Rates →<": ">Compare NZ Rates →<",
    ">live NZ rates page<": ">NZ rates page<",
    "live NZ mortgage rates": "NZ mortgage rates",
    '">live rates page</a> tracks current advertised fixed and floating rates across the main NZ lenders.':
        '">NZ rates page</a> explains how advertised fixed and floating rates work and links to where each main lender publishes its current rates.',
    "Our live rates page tracks current advertised fixed and floating rates across the main NZ lenders.":
        "Our NZ rates page explains how advertised fixed and floating rates work and links to where each main lender publishes its current rates.",
    "see <a href=\"../mortgage-rates.html\">today's live rates</a> for the current settings and how they're flowing through to mortgage pricing.":
        "see <a href=\"../mortgage-rates.html\">our NZ rates page</a> for where each lender publishes its current rates.",

    # Auckland city pages: approval timing is the lender's call.
    "North Shore Mortgage Broker | $0 Fee, 24hr Approval": "North Shore Mortgage Broker | $0 Fee, 23 Lenders | Finch",
    "East Auckland Mortgage Broker | $0 Fee, 24hr Approval": "East Auckland Mortgage Broker | $0 Fee, 23 Lenders | Finch",
    "South Auckland Mortgage Broker | $0 Fee, 24hr Approval": "South Auckland Mortgage Broker | $0 Fee, 23 Lenders | Finch",
    "West Auckland Mortgage Broker | $0 Fee, 24hr Approval": "West Auckland Mortgage Broker | $0 Fee, 23 Lenders | Finch",
    "Looking for the best home loan in North Shore? Finch compares 20+ NZ lenders to get you pre-approved in 24 hours. $0 broker fee. Compare rates →":
        "Buying or refinancing on the North Shore? Finch compares 23 NZ lenders to find a home loan that fits, with no fee on residential home loans. Book a free chat →",
    "Looking for the best home loan in East Auckland? Finch compares 20+ NZ lenders to get you pre-approved in 24 hours. $0 broker fee. Compare rates →":
        "Buying or refinancing in East Auckland? Finch compares 23 NZ lenders to find a home loan that fits, with no fee on residential home loans. Book a free chat →",
    "Looking for the best home loan in South Auckland? Finch compares 20+ NZ lenders to get you pre-approved in 24 hours. $0 broker fee. Compare rates →":
        "Buying or refinancing in South Auckland? Finch compares 23 NZ lenders to find a home loan that fits, with no fee on residential home loans. Book a free chat →",
    "Looking for the best home loan in West Auckland? Finch compares 20+ NZ lenders to get you pre-approved in 24 hours. $0 broker fee. Compare rates →":
        "Buying or refinancing in West Auckland? Finch compares 23 NZ lenders to find a home loan that fits, with no fee on residential home loans. Book a free chat →",
}


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    hits = {old: 0 for old in PAIRS}
    changed = 0
    for f in files:
        p = ROOT / f
        src = p.read_text(encoding="utf-8")
        out = src
        for old, new in PAIRS.items():
            if old in out:
                hits[old] += out.count(old)
                out = out.replace(old, new)
        if out != src:
            changed += 1
            if APPLY:
                p.write_text(out, encoding="utf-8")
    for old, n in hits.items():
        print(f"{n:4}  {old[:90]!r}")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
