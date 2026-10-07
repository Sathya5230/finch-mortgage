"""Replace stale OCR and rate figures in the shared rate banner and rate FAQ.

These blocks said the OCR was 3.25% with further cuts forecast for late 2026, quoted a
"1-year fixed special from 5.85%" and a June 2026 stress-test rate. The Reserve Bank
held the OCR at 2.25% in April 2026, then raised it to 2.50% (July) and 2.75%
(September). The replacements explain the mechanism without numbers, so they don't
go stale again. Live figures belong on mortgage-rates.html with an as-at date.

Idempotent. Run with --apply to write; default is a dry run.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

BANNER_OLD = "Current OCR at 3.25% · 1-Year Fixed Special from 5.85%"
BANNER_NEW = "Rates are moving — compare 20+ lenders before you fix"

ANSWERS = {
    "Yes, with the OCR currently at 3.25% and further RBNZ cuts forecast for late 2026, retail interest rates are expected to fall. Fixed 1-year terms are sitting around 5.85% special rates, with wholesale swap rates trending down.":
        "No one can say for certain. Mortgage rates follow the Reserve Bank's Official Cash Rate and wholesale funding costs, and the outlook can change at every OCR review. The Reserve Bank publishes each decision and its forecasts at rbnz.govt.nz. Rather than betting on one outcome, many borrowers split their loan across different fixed terms.",
    "Most NZ borrowers are choosing 1-year fixed terms to avoid locking in for too long while rates are falling. This gives the flexibility to refix at a lower rate in 12 months, though 2-year rates offer slightly lower pricing today.":
        "It depends on your plans and how much certainty you want. A shorter term lets you refix sooner if rates fall but exposes you sooner if they rise; a longer term gives certainty for longer. Splitting your loan across terms spreads the risk. We compare current pricing across lenders when your fixed term is due.",
    "As of June 2026, major NZ banks are testing servicing capacity at a stress rate around 7.45%, down from peak levels of nearly 9.0%. A lower test rate expands your maximum borrowing power significantly.":
        "Each lender sets its own test (assessment) rate and changes it as market rates move. Lenders check whether you could afford repayments at a rate above the one you'll actually pay, so what you can borrow depends on each lender's current test rate. We compare lenders' current test rates when working out your borrowing power.",
    "Floating mortgage rates respond directly to RBNZ Official Cash Rate changes. When the OCR is cut, floating rates typically drop by the same amount (25 or 50 basis points) within a few days.":
        "Floating rates usually move after an OCR change, but each bank decides how much of the change to pass on and how quickly. Fixed rates are driven more by wholesale swap rates, which move on expectations of future OCR decisions.",
}

# Body copy that assumed rates were still falling, or quoted rates as "currently".
PAIRS = {
    'Fixing for 6 months (currently around 5.90%) is a tactical play. You are accepting a slightly higher rate today with the expectation that when you "roll off" in 6 months, the 1-year or 2-year rates will have dropped substantially, allowing you to lock in long-term savings. This is a higher-risk strategy suited for those who closely follow macroeconomic trends.':
        "A short fix gives you the chance to refix soon. It works in your favour if rates fall, and against you if they rise. It suits borrowers who want flexibility and can handle repayments changing within a year.",
    'The 18-month and 2-year fixed terms are currently the "sweet spot" of the market (hovering around 5.40% – 5.60%). They offer immediate access to the lowest advertised rates and provide two years of solid certainty, without locking you in for a half-decade.':
        "Medium terms balance certainty and flexibility: your repayments are set for up to two years without committing to a longer term. Which term is cheapest changes with market conditions, so compare current pricing when you fix.",
    "While historically popular for ultimate peace of mind, long-term fixes are less favorable in a falling rate environment. By locking in a 5-year rate at ~6.00% today, you risk being stranded if the market settles at an average of 4.50% by 2027.":
        "Long fixes give the most certainty, which matters most when rates are rising or your budget is tight. The trade-off is less flexibility: if rates fall, or you need to sell or restructure, breaking a long fix can be costly.",
    " as they vie to capture market share in a falling rate environment.": " as they vie to capture market share.",
    "With the easing cycle underway, much of the expected fall is already priced into fixed rates — waiting on floating for a dramatically cheaper fix has a real cost every month.":
        "After cutting the OCR from August 2024, the Reserve Bank began raising it again in July 2026. Fixed rates move ahead of OCR decisions as wholesale rates price in expectations, so trying to time the market is hard.",
    '>2025–2026</td><td style="padding:0.6rem 0.9rem;border-bottom:1px solid rgba(181,206,176,0.4);font-size:0.95rem;">easing from the peak</td><td style="padding:0.6rem 0.9rem;border-bottom:1px solid rgba(181,206,176,0.4);font-size:0.95rem;">OCR cut back as inflation normalised; fixed rates repriced lower</td>':
        '>2024–2026</td><td style="padding:0.6rem 0.9rem;border-bottom:1px solid rgba(181,206,176,0.4);font-size:0.95rem;">easing, then rising again</td><td style="padding:0.6rem 0.9rem;border-bottom:1px solid rgba(181,206,176,0.4);font-size:0.95rem;">OCR cut from August 2024 to 2.25%, then raised from July 2026 as inflation picked up</td>',
    "The plan for Year 3 is to refinance all three to principal-and-interest loans as rates continue to fall.":
        "The plan for Year 3 is to move all three to principal-and-interest repayments as the interest-only periods end.",
}


def fix(src):
    src = src.replace(BANNER_OLD, BANNER_NEW)
    for old, new in {**ANSWERS, **PAIRS}.items():
        src = src.replace(old, new)
    return src


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    changed = 0
    for f in files:
        p = ROOT / f
        src = p.read_text(encoding="utf-8")
        out = fix(src)
        if out != src:
            changed += 1
            if APPLY:
                p.write_text(out, encoding="utf-8")
    print(f"changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
