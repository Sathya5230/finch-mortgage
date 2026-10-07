"""Correct claims that the Kāinga Ora First Home Grant is still available.

The grant closed to new applications on 22 May 2024 and has not been replaced; the
Kāinga Ora First Home Loan (5% deposit) continues. Pages still described the grant as
current. Each fix keeps the "First Home Grant" wording where people search for it,
but states that it has closed. Client stories describing past purchases are left as is; their FAQs are fixed.

Idempotent. Run with --apply to write; default is a dry run.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

CLOSED = "closed to new applications on 22 May 2024"
FHL = "Kāinga Ora First Home Loan"

# Whole sections: (heading regex up to the next <h2) -> replacement.
SECTIONS = [
    (r'<h2 id="grant">The First Home Grant: Free Government Money</h2>.*?(?=<h2)',
     f'<h2 id="grant">The First Home Grant: Closed Since May 2024</h2>\n'
     f'<p>The Kāinga Ora First Home Grant used to add up to $5,000 per person for an existing home, or up to $10,000 per person for a new build. It {CLOSED} and has not been replaced, so it can no longer be part of your deposit plan.</p>\n'
     f'<p>The main government support still available is the <strong>{FHL}</strong>, which lets eligible buyers purchase with a 5% deposit through participating lenders. Check the current criteria on the <a href="https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/" target="_blank" rel="noopener">Kāinga Ora website</a>.</p>\n'),
    (r'<h2 id="grant-difference">Distinguishing Withdrawal from the First Home Grant</h2>.*?(?=<h2)',
     '<h2 id="grant-difference">KiwiSaver Withdrawal vs the First Home Grant</h2>\n'
     '<p>People often confuse the KiwiSaver first home withdrawal with the First Home Grant. They were separate schemes, and only one is still available.</p>\n'
     '<p>The withdrawal is your own money, released by your KiwiSaver provider. It has no income cap and no house price cap — if you meet the eligibility rules, you can use it whatever you earn and whatever the property costs.</p>\n'
     f'<p>The First Home Grant was extra money paid by Kāinga Ora: up to $5,000 for an existing home or $10,000 for a new build, with income and price caps. It {CLOSED} and has not been replaced. The {FHL}, which allows a 5% deposit for eligible buyers, is still available.</p>\n'),
    (r'<h2 id="grant">First Home Grant</h2>.*?(?=<h2)',
     '<h2 id="grant">First Home Grant (Closed May 2024)</h2>\n'
     f'<p>The Kāinga Ora First Home Grant used to top up first home deposits by up to $5,000 per person for an existing home, or $10,000 for a new build. It {CLOSED} and has not been replaced.</p>\n'
     f'<p>The government support still available is the <strong>{FHL}</strong>, which lets eligible buyers purchase with a 5% deposit through participating lenders, alongside your KiwiSaver first home withdrawal.</p>\n'),
]

# Sentence-level swaps. Order matters: longer strings first.
PAIRS = [
    ("The First Home Grant is a government contribution of up to $5,000 per person for an existing home, or up to $10,000 per person for a new build. Couples can combine grants for up to $20,000 of free deposit capital.",
     f"The First Home Grant was a government contribution of up to $5,000 per person for an existing home, or up to $10,000 per person for a new build. It {CLOSED} and has not been replaced. The {FHL}, which lets eligible buyers purchase with a 5% deposit, is still available."),
    ("The Kāinga Ora First Home Grant provides up to $5,000 for an existing home or $10,000 for a new build. Income and house price caps apply. We'll assess your eligibility and help you apply as part of your mortgage process.",
     f"The Kāinga Ora First Home Grant (up to $5,000 for an existing home or $10,000 for a new build) {CLOSED} and has not been replaced. The {FHL} is still available for eligible buyers with a 5% deposit, and we'll check whether you qualify as part of your mortgage process."),
    ("Furthermore, the Kāinga Ora First Home Grant offers up to $5,000 for purchasing an existing property, or up to $10,000 for a new build, provided you meet specific income and regional house price caps.",
     f"The Kāinga Ora First Home Grant, which offered up to $5,000 for an existing property or $10,000 for a new build, {CLOSED}. The {FHL} is still available and lets eligible buyers purchase with a 5% deposit."),
    ("Kāinga Ora First Home Loan and First Home Grant eligibility caps are reviewed annually and vary by region.",
     "Kāinga Ora First Home Loan eligibility criteria are reviewed from time to time, so check the current criteria on the Kāinga Ora website. (The First Home Grant closed in May 2024.)"),
    ("<h3>First Home Grant</h3><p>We assess your eligibility for the Kāinga Ora First Home Grant and help you apply for up to $10,000.</p>",
     f"<h3>{FHL}</h3><p>The First Home Grant closed in May 2024, but the {FHL} is still available. We check whether you qualify to buy with a 5% deposit.</p>"),
    ('<div class="stat-number">$10K</div><div class="stat-label">Max First Home Grant</div>',
     '<div class="stat-number">$0</div><div class="stat-label">Broker Fee</div>'),
    ("Yes to both. If you've been contributing to KiwiSaver for 3+ years, you can likely withdraw most of it for your deposit. You may also qualify for the First Home Grant - up to $10,000 per person. We'll confirm exactly what you're entitled to on the call.",
     f"KiwiSaver, yes — if you've been contributing for 3+ years, you can likely withdraw most of it for your deposit. The First Home Grant closed in May 2024, but the {FHL} (5% deposit) is still available. We'll confirm exactly what you're eligible for on the call."),
    ("<li><strong>First Home Grant:</strong> Up to $10,000 grant on top of your KiwiSaver withdrawal</li>",
     f"<li><strong>{FHL}:</strong> Buy with a 5% deposit if you meet Kāinga Ora's criteria (the First Home Grant closed in May 2024)</li>"),
    ("<li><strong>First Home Grant:</strong> Depending on regional house price caps and your income level, Kāinga Ora offers up to $5,000 per person for an existing home or up to $10,000 per person for a new build.</li>",
     f"<li><strong>First Home Grant (closed):</strong> Kāinga Ora's grant of up to $5,000 per person for an existing home or $10,000 for a new build {CLOSED} and has not been replaced.</li>"),
    ('<li style="margin-bottom:0.5rem;"><strong>Kāinga Ora First Home Grant</strong> — up to $5,000 (existing home) or $10,000 (new build) per applicant.</li>',
     f'<li style="margin-bottom:0.5rem;"><strong>{FHL}</strong> — lets eligible buyers purchase with a 5% deposit. (The First Home Grant closed in May 2024.)</li>'),
    ("<strong>Kāinga Ora First Home Grant</strong> — up to $5,000 (existing) / $10,000 (new build) per applicant. Income and price caps apply by region.",
     f"<strong>Kāinga Ora First Home Grant</strong> — {CLOSED} and not replaced."),
    ("<strong>Kāinga Ora First Home Grant</strong> — up to $5,000 for an existing home or $10,000 for a new build per applicant, subject to income and house price caps.",
     f"<strong>Kāinga Ora First Home Grant</strong> — {CLOSED} and not replaced."),
    ("<li><strong>First Home Grant:</strong> $10,000 (Because he was targeting a new build, he was eligible for the maximum grant).</li>",
     "<li><strong>First Home Grant:</strong> $10,000 (Because he was targeting a new build, he was eligible for the maximum grant). Note: the grant closed to new applications on 22 May 2024, so it can't form part of a deposit today.</li>"),
    ("Buying a new build requires a much smaller deposit (often 10%) compared to an existing home (20%), and unlocks double the First Home Grant.",
     "Buying a new build can require a much smaller deposit (often 10%) than an existing home (20%), because new builds are exempt from the Reserve Bank's LVR speed limits."),
    ("Your KiwiSaver withdrawal, the First Home Grant, and theoretically even a gifted sum from family can legally constitute the entire 5%.",
     "Your KiwiSaver withdrawal and, with many lenders, a gifted sum from family can make up the 5%."),
    ("Crucially, the lower price point means many homes fall under the First Home Grant price caps, allowing eligible buyers to access up to $10,000 per person in free government grants.",
     "Crucially, the lower price point means a smaller deposit in dollar terms, which makes saving 10–20% far more achievable."),
    ("plenty of our clients buy with 10% or even 5% through low-deposit lenders and the First Home Grant.",
     f"plenty of our clients buy with 10% or even 5% through low-deposit lenders and the {FHL}."),
    ("may also qualify for the First Home Grant, subject to Kāinga Ora's income and house-price caps.",
     f"may also qualify for the {FHL} (5% deposit). The First Home Grant closed to new applications in May 2024."),
    ("may also qualify for the First Home Grant, subject to Kainga Ora's income and house-price caps.",
     f"may also qualify for the {FHL} (5% deposit). The First Home Grant closed to new applications in May 2024."),
    ("Learn how to leverage your KiwiSaver, access First Home Grants, and navigate the deposit requirements for your first property.",
     f"Learn how to use your KiwiSaver and the {FHL}, and navigate the deposit requirements for your first property."),
    ("</svg> Kainga Ora First Home Grants</li>", f"</svg> {FHL} (5% Deposit)</li>"),
    ("KiwiSaver withdrawals, First Home Grants, and low-deposit lending", f"KiwiSaver withdrawals, the {FHL}, and low-deposit lending"),
    ("KiwiSaver withdrawals, First Home Grants, low-deposit options", f"KiwiSaver withdrawals, the {FHL}, low-deposit options"),
    ("Maximizing Your KiwiSaver and First Home Grants", "Maximizing Your KiwiSaver and Kāinga Ora Support"),
    ("KiwiSaver withdrawal, First Home Grant, low-deposit lending", "KiwiSaver withdrawal, First Home Loan, low-deposit lending"),
    ("deposit, KiwiSaver, First Home Grant, pre-approval", "deposit, KiwiSaver, First Home Loan, pre-approval"),
    ("KiwiSaver options, and Kainga Ora First Home Grant.", f"KiwiSaver options, and the {FHL}."),
    ("Covers eligibility, withdrawal limits, and the First Home Grant.", "Covers eligibility, withdrawal limits, and what replaced the First Home Grant."),
    ('<a href="#grant">First Home Grant</a>', '<a href="#grant">First Home Grant (Closed)</a>'),
    ("Unlocking First Home Grants in Papakura subdivisions", "Low-deposit new builds in Papakura subdivisions"),
]

SKIP_PREFIX = ("weekly-reports", "testimonials/")


def fix(src):
    for pat, rep in SECTIONS:
        src = re.sub(pat, lambda _m, r=rep: r, src, flags=re.S)
    for old, new in PAIRS:
        src = src.replace(old, new)
        # The same text inside JSON-LD, with ā / — escaped.
        esc = lambda t: t.replace("ā", "\\u0101").replace("—", "\\u2014")
        if esc(old) != old:
            src = src.replace(esc(old), esc(new))
    return src


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    changed = []
    for f in files:
        if f.startswith(SKIP_PREFIX) or f in ("weekly-reports.html", "market-report.html"):
            continue
        p = ROOT / f
        src = p.read_text(encoding="utf-8")
        out = fix(src)
        if out != src:
            changed.append(f)
            if APPLY:
                p.write_text(out, encoding="utf-8")
    print(f"changed: {len(changed)}")
    for f in changed:
        print("  ", f)
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
