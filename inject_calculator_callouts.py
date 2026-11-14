"""Link topic posts to the calculator that answers their question.

Adds one marked callout above the first section heading of each listed post,
so the break fee, LVR, interest-only and cashback clawback calculators are
reachable from the posts people land on. Idempotent: the block is replaced in
place on each run. Run after the post generators and before strip_html_ext.py.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
START, END = "<!-- FINCH-CALC:START -->", "<!-- FINCH-CALC:END -->"

CALCS = {
    "break-fee-calculator": ("Break fee calculator", "Estimate what it would cost to break your fixed rate, and whether switching still leaves you ahead.",
                             ["break-fixed-mortgage-break-fees-nz", "fixed-rate-ending-refix-guide-nz", "is-it-worth-refinancing-mortgage-nz",
                              "refinance-costs-nz", "mortgage-portability-nz", "selling-house-with-mortgage-nz"]),
    "cashback-clawback-calculator": ("Cashback clawback calculator", "Estimate how much of your bank's cash contribution you'd repay if you left today.",
                                     ["mortgage-cashback-clawback-nz", "mortgage-cashback-offers-nz", "how-often-can-you-refinance-nz",
                                      "refinance-with-same-bank-nz"]),
    "lvr-calculator": ("LVR calculator", "Work out your loan-to-value ratio and how much more deposit you'd need to reach 80%.",
                       ["what-is-lvr-nz-mortgage", "low-equity-margin-fee-nz", "low-deposit-home-loan-nz", "deposit-requirements-nz",
                        "usable-equity-nz", "new-build-home-loan-deposit-nz"]),
    "interest-only-calculator": ("Interest-only calculator", "Compare interest-only repayments with standard repayments, and see what they rise to afterwards.",
                                 ["interest-only-home-loan-nz", "interest-only-ending-refinance-nz"]),
}


def block(calc, name, text):
    return (f'{START}\n<p style="background:white;border-left:3px solid var(--finch-forest);border-radius:0 0.75rem 0.75rem 0;'
            f'padding:1rem 1.25rem;margin:0 0 1.5rem;font-size:0.97rem;"><a href="../calculators/{calc}.html" '
            f'style="color:var(--finch-forest);text-decoration:underline;font-weight:700;">{name}</a>: {text}</p>\n{END}\n')


def main():
    done = 0
    for calc, (name, text, slugs) in CALCS.items():
        for slug in slugs:
            path = ROOT / "blog" / f"{slug}.html"
            html = path.read_text(encoding="utf-8")
            html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
            main_at = html.index("<main")
            h2 = html.index("<h2", main_at)
            html = html[:h2] + block(calc, name, text) + html[h2:]
            path.write_text(html, encoding="utf-8")
            done += 1
    print(f"calculator callouts: {done} posts")


if __name__ == "__main__":
    main()
