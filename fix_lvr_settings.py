"""Bring LVR statements in line with the Reserve Bank's current settings.

Since 1 December 2025 banks may make up to 25% of new owner-occupier lending
above 80% LVR and up to 10% of new investor lending above 70% LVR. The Reserve
Bank's Financial Policy Committee kept those settings on 14 August 2026
(rbnz.govt.nz, "Reserve Bank maintains Loan-to-Value Ratio (LVR) settings").
Several pages still quoted the earlier 20% / 5% limits, a "60-65% LVR" investor
limit, or "30-35%" investor deposits.

Idempotent. Run with --apply to write; default is a dry run. Re-check the
figures after each annual Reserve Bank review (next due around August 2027).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

PAIRS = {
    "maximum 20% of a bank's new lending can be above 80% LVR (i.e. with less than 20% deposit).":
        "up to 25% of a bank's new owner-occupier lending can be above 80% LVR (that is, with less than a 20% deposit).",
    "maximum 5% of a bank's new lending can be above 70% LVR (i.e. with less than 30% deposit).":
        "up to 10% of a bank's new investor lending can be above 70% LVR (that is, with less than a 30% deposit).",
    "Current RBNZ LVR Speed Limits (2026)": "Current Reserve Bank LVR limits",
    "<p>As of 2026:</p>": "<p>These settings have applied since 1 December 2025, and the Reserve Bank kept them unchanged at its August 2026 review:</p>",
    "As of 2026:": "These settings have applied since 1 December 2025, and the Reserve Bank kept them unchanged at its August 2026 review:",

    "To understand why the 20% threshold exists, we must look to the Reserve Bank of New Zealand (RBNZ). The RBNZ orchestrates the financial stability of the country and imposes Loan-to-Value Ratio (LVR) restrictions on retail banks. These macroeconomic 'speed limits' dictate that banks are only permitted to issue a very small percentage of their total residential lending to owner-occupiers who have less than a 20% deposit. By mandating a 20% equity buffer, the RBNZ ensures that if the housing market completely crashes and property values plummet by 15%, the bank is theoretically insulated from financial loss if forced to enact a mortgagee sale.":
        "The 20% figure comes from the Reserve Bank of New Zealand's loan-to-value ratio (LVR) restrictions. Since 1 December 2025, a bank can make up to 25% of its new owner-occupier lending to borrowers with less than a 20% deposit. That leaves room for low-deposit loans, but each bank rations its share, so the criteria are tighter and the pricing is usually higher than for a borrower with 20% or more. The buffer exists so that a fall in house prices doesn't leave the loan larger than the property is worth.",

    "existing builds generally need ~30–35% down; new builds are LVR-exempt":
        "existing builds generally need a 30% deposit; new builds are LVR-exempt",
    "banks generally want roughly 30–35% equity in the deal for existing builds":
        "most investor loans on existing properties need 30% equity in the deal, because banks can make only 10% of new investor lending above 70% LVR",
    "banks generally want around 30–35% equity in the purchase":
        "banks generally want 30% equity in the purchase",
    "supports an existing-build purchase in the $850k–$1M range, subject to servicing":
        "supports an existing-build purchase of up to about $1M at a 30% deposit, subject to servicing",

    "(within the 65% LVR investor cap)": "(within the lender's investor LVR limit)",
    "the strict RBNZ 60-65% LVR limit on existing homes": "the Reserve Bank's 70% LVR limit on existing investment properties",
    # Investor deposit: the limit is 70% LVR (30% deposit), not 60%.
    "RBNZ rules typically require investors to have at least 40% deposit (LVR 60%) for investment properties. Some non-bank lenders allow lower deposits with appropriate risk pricing.":
        "Most investor loans on an existing property need a 30% deposit, because banks can make only 10% of their new investor lending above 70% LVR. New builds are exempt, and non-bank lenders set their own limits.",
    "Navigate RBNZ investor LVR restrictions (40% deposit) with smart lending strategies and lender selection.":
        "How the Reserve Bank's 70% LVR limit for investors applies to you, and which lenders suit your equity.",
    "Typically require 40% deposit (LVR 60% or below)": "Typically require a 30% deposit (LVR of 70% or below)",
    "40% deposit investor NZ, ": "30% deposit investor NZ, ",
    "NZ banks typically require a 35% or 40% deposit (LVR of 60-65%), whereas new-build investments only require a 20% deposit":
        "NZ banks typically require a 30% deposit (LVR of 70%), whereas new-build investments are exempt from the Reserve Bank's limit and often need less",
    "Existing houses require a 35% to 40% deposit.": "Existing houses usually require a 30% deposit.",
    "Buy with 5% deposit if you meet income and price caps": "Buy with a 5% deposit if you meet the income caps",
}

SKIP_DIRS = ("node_modules/", "wordpress/", "output/", "scratch/", "docs/", "research/")


def main():
    files = subprocess.run(["git", "ls-files", "*.html", "*.py"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.splitlines()
    total = 0
    for rel in files:
        if rel.startswith(SKIP_DIRS) or rel == Path(__file__).name:
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for old, rep in PAIRS.items():
            new = new.replace(old, rep)
        if new != text:
            total += 1
            print(rel)
            if APPLY:
                path.write_text(new, encoding="utf-8")
    print(f"{total} file(s)", "APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
