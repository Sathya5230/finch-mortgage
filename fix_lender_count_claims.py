"""Replace the stale "20+ lenders" claim with the real panel size (23) and remove
unverifiable 24-48 hour pre-approval promises. Turnaround depends on the lender,
so the copy no longer promises a time. Idempotent; dry run unless --apply.

Also rewrites the generator/fix sources so a regenerate doesn't bring the old
claims back.
"""
import glob
import re
import sys

PANEL = "23"

REGEX = [
    (re.compile(r"\b20\+ (NZ )?(lenders|Lenders|banks|bank|Banks)"), rf"{PANEL} \1\2"),
    (re.compile(r'(<div class="stat-number">)20\+(</div><div class="stat-label">Lenders)'), rf"\g<1>{PANEL}\2"),
    (re.compile(r"\b20\+ NZ Lenders"), f"{PANEL} NZ Lenders"),
]

EXACT = {
    "across a panel of more than 20 lenders": f"across a panel of {PANEL} lenders",
    "the underwriting algorithms of over 20 New Zealand lenders": f"the lending policies of {PANEL} New Zealand lenders",
    "sourcing loan options from over 20 different lenders": f"sourcing loan options from {PANEL} different lenders",
    "against the strict criteria of over 20 lenders": f"against the criteria of the {PANEL} lenders on our panel",
    "Finch can give you a lender-specific borrowing limit in 24 hours — accurate to the dollar.":
        "Finch can run your numbers through each lender's own servicing test, so you know which lenders will go furthest before you apply.",
    "✓ 24–48hr turnaround": "✓ Conditional approval before you bid",
    "Conditional pre-approval in 24–48 hours — so you can bid confidently at auction.":
        "Get conditional pre-approval in place before you start bidding, so you know your limit at auction.",
    '<div class="stat-number">24-48h</div><div class="stat-label">Turnaround Time</div>':
        '<div class="stat-number">1</div><div class="stat-label">Application, Many Lenders</div>',
    "Usually within 24 to 48 hours, you'll receive your conditional pre-approval letter. You have 90 days to find a property!":
        "Once the lender has assessed your file you'll get a conditional pre-approval letter. Timing depends on the lender and how complete your documents are, and most approvals last around 90 days.",
    "<title>Mortgage Pre-Approval NZ | Get Approved in 24 Hours | Finch</title>":
        "<title>Mortgage Pre-Approval NZ | Know Your Buying Power | Finch</title>",
    "Get NZ mortgage pre-approval in 24–48 hours. Bid confidently at auction, know your borrowing power, and make offers with certainty. Free pre-approval service.":
        "Get NZ mortgage pre-approval before you bid. Know your borrowing power, bid at auction with a set limit, and make offers with confidence. $0 broker fee.",
    "Get a conditional mortgage pre-approval within 24-48 hours. Bid confidently at auction and negotiate with power. Free pre-approval service in New Zealand.":
        "Get conditional mortgage pre-approval before you bid. Know your limit at auction and negotiate with confidence. Free pre-approval help across New Zealand.",
    "compare policies across all 20+ partners": f"compare policies across all {PANEL} partners",
    ">20+ lender panel</a>": f">{PANEL}-lender panel</a>",
    "across our 20+ lender network": f"across our {PANEL}-lender panel",
    "Finch Mortgages works with 20+ of these lenders": f"Finch Mortgages works with {PANEL} of these lenders",
    "mortgage pre-approval 24 hours NZ, ": "",
    "24 hour pre-approval NZ, ": "",
    "to get you pre-approved in 24 hours.": "to get you pre-approved before you bid.",
}

SKIP_DIRS = ("node_modules", ".venv", "drafts", "output", "published", "rewrites", "research", "topics")
SKIP_PY = {"fix_lender_count_claims.py", "fix_service_pages.py"}


def targets():
    for f in glob.glob("**/*.html", recursive=True):
        if not f.startswith(SKIP_DIRS):
            yield f
    for f in glob.glob("*.py"):
        if f not in SKIP_PY:
            yield f
    yield from ("rss.xml", "llms.txt", "sitemap.xml")


def fix(text):
    for old, new in EXACT.items():
        text = text.replace(old, new)
    for pat, rep in REGEX:
        text = pat.sub(rep, text)
    return text


def main():
    apply = "--apply" in sys.argv
    changed = []
    for f in targets():
        try:
            with open(f, encoding="utf-8") as fh:
                before = fh.read()
        except (FileNotFoundError, UnicodeDecodeError):
            continue
        after = fix(before)
        if after != before:
            changed.append(f)
            if apply:
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(after)
    print(f"files changed: {len(changed)}", "APPLIED" if apply else "(dry run)")
    for f in changed:
        if f.endswith(".py"):
            print("  py:", f)


if __name__ == "__main__":
    main()
