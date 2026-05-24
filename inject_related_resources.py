"""Inject the 'Related NZ Resources' link block before </main> on all
blog, weekly-report, case-study, and lender-hub pages that don't already have it.

Idempotent: detects the marker "Related NZ" and skips pages already updated.

Skips the user's protected pages (about, contact, FHB landing, privacy/terms/
disclaimer/disclosure, thank-you variants, fhb-* duplicates).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent

EXCLUDED_PATHS = {
    "about.html",
    "contact.html",
    "first-home-buyers.html",
    "privacy.html",
    "terms.html",
    "disclaimer.html",
    "disclosure.html",
    "thank-you.html",
    "fhb-privacy.html",
    "fhb-terms.html",
    "fhb-disclaimer.html",
    "fhb-disclosure.html",
    "fhb-thank-you.html",
}

EXCLUDED_DIRS = {".claude", ".git", ".vscode", "node_modules", "scratch", "docs"}

MARKER = "Related NZ Resources"


def relpath_to_root(file_path: Path) -> str:
    """Return '../' prefix needed for href references back to site root."""
    depth = len(file_path.relative_to(ROOT).parts) - 1
    return "../" * depth


def block_for_blog(prefix: str) -> str:
    return f"""
<!-- Related NZ Resources -->
<section style=\"padding:4rem 0;background:white;\">
<div class=\"container\" style=\"max-width:1000px;\">
<div class=\"section-label\"><span>Keep Reading</span></div>
<h2 class=\"section-heading\" style=\"margin-bottom:2.5rem;\">Related NZ mortgage resources</h2>
<div class=\"cols-3\" style=\"gap:1.5rem;\">
<a href=\"{prefix}services/home-loan.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Home Loan Service</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Independent advice across 20+ NZ lenders.</span></a>
<a href=\"{prefix}calculators/mortgage-calculator.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Mortgage Calculator</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Estimate repayments at current NZ rates.</span></a>
<a href=\"{prefix}calculators/borrowing-power.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Borrowing Power</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">See how much NZ banks will lend.</span></a>
<a href=\"{prefix}guides/first-home-guide.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ First Home Buyer Guide</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Complete NZ FHB playbook.</span></a>
<a href=\"{prefix}mortgage-rates.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Live NZ Mortgage Rates</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Current carded and broker rates.</span></a>
<a href=\"{prefix}market-report.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Market Report</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">OCR &amp; rate movements.</span></a>
</div>
</div>
</section>
"""


def block_for_weekly_report(prefix: str) -> str:
    return f"""
<!-- Related NZ Resources -->
<section style=\"padding:4rem 0;background:white;\">
<div class=\"container\" style=\"max-width:1000px;\">
<div class=\"section-label\"><span>Keep Reading</span></div>
<h2 class=\"section-heading\" style=\"margin-bottom:2.5rem;\">More NZ mortgage market analysis</h2>
<div class=\"cols-3\" style=\"gap:1.5rem;\">
<a href=\"{prefix}market-report.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Market Report</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Full NZ mortgage market overview.</span></a>
<a href=\"{prefix}weekly-reports.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">All Weekly NZ Reports</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Archive of weekly NZ rate updates.</span></a>
<a href=\"{prefix}mortgage-rates.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Live NZ Mortgage Rates</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Current carded and broker rates.</span></a>
<a href=\"{prefix}lenders.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Lender Directory</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Compare every NZ bank and non-bank.</span></a>
<a href=\"{prefix}services/refinance.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Refinance Service</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Lock in a better NZ rate.</span></a>
<a href=\"{prefix}calculators/refinance-savings.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Refinance Savings Calculator</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Model your switching benefit.</span></a>
</div>
</div>
</section>
"""


def block_for_case_study(prefix: str) -> str:
    return f"""
<!-- Related NZ Resources -->
<section style=\"padding:4rem 0;background:white;\">
<div class=\"container\" style=\"max-width:1000px;\">
<div class=\"section-label\"><span>Keep Reading</span></div>
<h2 class=\"section-heading\" style=\"margin-bottom:2.5rem;\">More NZ client success stories &amp; tools</h2>
<div class=\"cols-3\" style=\"gap:1.5rem;\">
<a href=\"{prefix}case-studies.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">All NZ Case Studies</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Real outcomes across every scenario.</span></a>
<a href=\"{prefix}testimonials/reviews.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Client Reviews</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">5.0 star Google rating.</span></a>
<a href=\"{prefix}testimonials/success-stories.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Success Stories</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">In-depth client journeys.</span></a>
<a href=\"{prefix}services/home-loan.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Home Loan Service</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Start your own approval today.</span></a>
<a href=\"{prefix}calculators/borrowing-power.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Borrowing Power</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">See your NZ borrowing capacity.</span></a>
<a href=\"{prefix}contact.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Book a Free Call</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">15-min discovery, no obligation.</span></a>
</div>
</div>
</section>
"""


def block_for_lender_hub(prefix: str) -> str:
    return f"""
<!-- Related NZ Resources -->
<section style=\"padding:4rem 0;background:white;\">
<div class=\"container\" style=\"max-width:1000px;\">
<div class=\"section-label\"><span>Keep Reading</span></div>
<h2 class=\"section-heading\" style=\"margin-bottom:2.5rem;\">Compare other NZ lender categories</h2>
<div class=\"cols-3\" style=\"gap:1.5rem;\">
<a href=\"{prefix}lenders.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">All NZ Lenders</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Browse the full NZ lender directory.</span></a>
<a href=\"{prefix}lenders/major-banks.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Major Banks</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">ANZ, ASB, BNZ, Westpac, Kiwibank.</span></a>
<a href=\"{prefix}lenders/non-bank-lenders.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Non-Bank Lenders</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Resimac, Pepper, Liberty, Avanti.</span></a>
<a href=\"{prefix}lenders/specialist-lenders.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Specialist Lenders</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Asset finance &amp; complex deals.</span></a>
<a href=\"{prefix}lenders/credit-unions.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">NZ Credit Unions</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Member-owned NZ lenders.</span></a>
<a href=\"{prefix}mortgage-rates.html\" style=\"display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);\"><strong style=\"display:block;color:var(--finch-forest);margin-bottom:0.5rem;\">Live NZ Mortgage Rates</strong><span style=\"font-size:0.9rem;color:var(--neutral-medGray);\">Current carded and broker rates.</span></a>
</div>
</div>
</section>
"""


def pick_block(file_path: Path, prefix: str) -> str | None:
    rel = file_path.relative_to(ROOT).as_posix()
    if rel.startswith("blog/"):
        return block_for_blog(prefix)
    if rel.startswith("weekly-reports/"):
        return block_for_weekly_report(prefix)
    if rel.startswith("case-studies/"):
        return block_for_case_study(prefix)
    if rel.startswith("lenders/"):
        return block_for_lender_hub(prefix)
    if rel.startswith("testimonials/"):
        return block_for_case_study(prefix)
    return None


def should_skip(file_path: Path) -> bool:
    parts = file_path.relative_to(ROOT).parts
    if any(p in EXCLUDED_DIRS for p in parts):
        return True
    if file_path.name in EXCLUDED_PATHS:
        return True
    return False


def process(file_path: Path) -> tuple[bool, str]:
    text = file_path.read_text(encoding="utf-8")
    if MARKER in text:
        return False, "already-has-block"
    if "</main>" not in text:
        return False, "no-main-tag"
    prefix = relpath_to_root(file_path)
    block = pick_block(file_path, prefix)
    if block is None:
        return False, "no-block-defined"
    new_text = text.replace("</main>", block + "</main>", 1)
    file_path.write_text(new_text, encoding="utf-8")
    return True, "injected"


def main() -> None:
    html_files = sorted(p for p in ROOT.rglob("*.html") if not should_skip(p))
    injected = skipped = errored = 0
    for f in html_files:
        ok, reason = process(f)
        rel = f.relative_to(ROOT)
        if ok:
            injected += 1
            print(f"  + injected:  {rel}")
        else:
            if reason == "already-has-block":
                skipped += 1
            elif reason == "no-block-defined":
                pass  # silent — pages we don't auto-handle
            else:
                errored += 1
                print(f"  ! {reason}: {rel}")
    print()
    print(f"Done. Injected: {injected}  Skipped(had block): {skipped}  Errored: {errored}")


if __name__ == "__main__":
    main()
