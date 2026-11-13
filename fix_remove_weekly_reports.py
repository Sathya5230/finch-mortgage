"""Retire the weekly market reports (removed 2026-11-12 at the owner's request).

The report pages and their generator are deleted. This script removes every
link to them from the remaining HTML and from generator sources, repoints
in-content links to the evergreen replacements, and strips the weekly section
and "updated weekly" claims from market-report.html. Old URLs are 301'd in
vercel.json. Idempotent; dry run unless --apply.
"""
import glob
import re
import sys

# old weekly slug -> replacement path from site root (no extension)
REDIRECTS = {
    "week-1-year-ahead-2026": "blog/will-mortgage-rates-drop-nz-2026",
    "week-2-mortgage-stress-testing": "blog/mortgage-stress-test-rate-nz",
    "week-3-summer-sales-slump": "blog/best-time-of-year-to-buy-a-house-nz",
    "week-4-dti-caps-bite": "blog/how-much-house-can-i-afford-nz",
    "week-5-new-build-exemptions": "blog/new-build-home-loan-deposit-nz",
    "week-6-floating-vs-fixed": "blog/fixed-vs-floating-mortgage-nz",
    "week-7-kiwisaver-tips": "blog/kiwisaver-first-home-withdrawal",
    "week-8-interest-deductibility": "blog/mortgage-interest-tax-deductible-nz",
    "week-9-bay-of-plenty": "locations/mortgage-broker-bay-of-plenty",
    "week-10-ocr-cut-march": "blog/how-ocr-affects-mortgages-nz",
    "week-12-rental-yields": "blog/good-rental-yield-nz",
    "week-13-canterbury-surge": "locations/mortgage-broker-canterbury",
    "week-14-anz-rates": "blog/special-vs-standard-mortgage-rates-nz",
    "week-15-ocr-hold": "blog/rate-rise-mortgage-repayments-nz",
    "week-16-major-banks-cut-rates": "blog/how-to-negotiate-mortgage-rate-nz",
    "week-17-autumn-update": "blog/buy-now-or-wait-nz",
    "week-18-winter-strategies": "blog/best-time-of-year-to-buy-a-house-nz",
    "week-19-spring-market-prep": "blog/buy-now-or-wait-nz",
    "week-20-fixed-rates-dip": "blog/mortgage-rate-lock-nz",
}
HUB_TARGET = "blog"

NAV_LINK = re.compile(
    r'<a\b[^>]*href=\\?"[^"]*weekly-reports(?:\.html)?\\?"[^>]*>\s*(?:📅|&#128197;)?\s*Weekly Reports\s*</a>\n?')
REPORT_HREF = re.compile(r'href="((?:\.\./)*)weekly-reports/([a-z0-9-]+?)(?:\.html)?"')
HUB_HREF = re.compile(r'href="((?:\.\./)*)weekly-reports(?:\.html)?"')

CARD_TEXT = {
    '>How DTI Caps Bite</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Market analysis of who the caps actually constrain.</span>':
        '>How Much House Can You Afford?</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Your own budget against the lender\'s limit.</span>',
    '>New-Build Exemptions</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Why new builds bypass LVR and DTI limits.</span>':
        '>New Build Deposits</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Why new builds are exempt from LVR and DTI limits.</span>',
    'and the latest <a href="blog" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">weekly market report</a>':
        'and our guide to <a href="blog/rate-rise-mortgage-repayments-nz" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">what a rate rise does to your repayments</a>',
}

GUIDES = [
    ("how-to-negotiate-mortgage-rate-nz", "How to negotiate a better rate", "When banks discount, and what to say."),
    ("special-vs-standard-mortgage-rates-nz", "Special vs standard rates", "Who qualifies for the lower rate card."),
    ("mortgage-rate-lock-nz", "Rate locks", "Holding a rate before you settle or refix."),
    ("5-year-fixed-mortgage-nz", "Fixing for 5 years", "Certainty against flexibility and break fees."),
    ("rate-rise-mortgage-repayments-nz", "What a rate rise costs", "Repayments at each rate, by loan size."),
    ("buy-now-or-wait-nz", "Buy now or wait?", "A readiness checklist that beats timing."),
    ("best-time-of-year-to-buy-a-house-nz", "Best time of year to buy", "How the seasons change choice and competition."),
    ("how-much-house-can-i-afford-nz", "How much house can you afford?", "Your budget against the lender's limit."),
    ("new-build-home-loan-deposit-nz", "New build deposits", "How the deposit exemption works."),
    ("good-rental-yield-nz", "What is a good rental yield?", "Gross and net yield, with a worked example."),
]
MR_START, MR_END = "<!-- FINCH-RATEGUIDES:START -->", "<!-- FINCH-RATEGUIDES:END -->"


def guides_block():
    cards = "".join(
        f'<a href="blog/{slug}" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;'
        f'text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);'
        f'margin-bottom:0.5rem;">{title}</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">{sub}</span></a>\n'
        for slug, title, sub in GUIDES)
    return f"""{MR_START}
<section id="rate-guides" style="padding:5rem 0;background:white;">
<div class="container">
<div class="section-label"><span>Rate &amp; Timing Guides</span></div>
<h2 class="section-heading" style="margin-top:0.75rem;margin-bottom:0.5rem;">Decisions that<br/><em>don't date.</em></h2>
<p style="color:var(--neutral-medGray);max-width:680px;line-height:1.7;margin-bottom:2rem;">Rates change every week. How to choose a term, negotiate with a bank and judge what you can afford doesn't. These guides cover the decisions behind the headlines.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">
{cards}</div>
</div>
</section>
{MR_END}
"""


MR_TEXT = {
    "Live NZ mortgage market insights: OCR moves, bank rate changes, housing data and expert forecasts, updated weekly by Finch.":
        "NZ mortgage market overview from Finch: how the OCR, bank rates and lending rules affect buyers, investors and refinancers, with rate and timing guides.",
    '"name": "NZ Mortgage Market Report — Weekly Rate Insights"': '"name": "NZ Mortgage Market Report"',
    '"description": "Weekly NZ mortgage market report — OCR moves, bank rate changes, property market trends, and lender activity. Expert analysis from Finch Mortgages."':
        '"description": "NZ mortgage market overview: OCR, bank rates, lending rules and property trends, with rate and timing guides from Finch Mortgages."',
    "weekly mortgage market update NZ, ": "",
    " Our <strong>Weekly Reports</strong> are published every Monday and cover breaking news like OCR decisions, bank rate movements, and regional market data. Scroll up to the Weekly Reports section to browse or filter by category.":
        " For decisions that don't depend on this week's numbers, see the rate and timing guides above.",
    " Our Weekly Reports are published every Monday and cover breaking news like OCR decisions, bank rate movements, and regional market data. Scroll up to the Weekly Reports section to browse or filter by category.":
        " For decisions that don't depend on this week's numbers, see the rate and timing guides on this page.",
}
MR_ARCHIVE_BTN = re.compile(r'<a aria-label="Link icon" href="(?:weekly-reports|blog)"[^>]*>(?:(?!</a>).)*View Weekly Reports Archive →\s*</a>\n?', re.S)
MR_SECTION = re.compile(r'(?:<!--[^>]*WEEKLY REPORTS[^>]*-->\s*)?<!-- ── LATEST REPORT \(FEATURED\) ── -->.*?(?=<!-- ── FAQ ── -->)', re.S)

SKIP_DIRS = ("node_modules", ".venv", "drafts", "output", "published", "rewrites", "research", "topics")
SKIP_PY = {"fix_remove_weekly_reports.py", "inject_related_resources.py", "update_keywords.py"}


def fix_market_report(t):
    t = MR_ARCHIVE_BTN.sub("", t)
    if MR_START not in t:
        t = MR_SECTION.sub(lambda m: guides_block(), t, count=1)
    else:
        t = re.sub(re.escape(MR_START) + r".*?" + re.escape(MR_END) + r"\n?", lambda m: guides_block(), t, flags=re.S)
    for a, b in MR_TEXT.items():
        t = t.replace(a, b)
    return t


def fix(text, path):
    text = NAV_LINK.sub("", text)
    if path.endswith(".html"):
        if path == "market-report.html":
            text = fix_market_report(text)
        text = REPORT_HREF.sub(
            lambda m: f'href="{m.group(1)}{REDIRECTS[m.group(2)]}"' if m.group(2) in REDIRECTS else f'href="{m.group(1)}{HUB_TARGET}"',
            text)
        text = HUB_HREF.sub(lambda m: f'href="{m.group(1)}{HUB_TARGET}"', text)
        for a, b in CARD_TEXT.items():
            text = text.replace(a, b)
    return text


def targets():
    for f in glob.glob("**/*.html", recursive=True):
        if not f.startswith(SKIP_DIRS) and not f.startswith("weekly-reports"):
            yield f
    for f in glob.glob("*.py"):
        if f not in SKIP_PY:
            yield f


def main():
    apply = "--apply" in sys.argv
    changed = 0
    for f in targets():
        try:
            with open(f, encoding="utf-8") as fh:
                before = fh.read()
        except (FileNotFoundError, UnicodeDecodeError):
            continue
        after = fix(before, f)
        if after != before:
            changed += 1
            if apply:
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(after)
    print(f"files changed: {changed}", "APPLIED" if apply else "(dry run)")


if __name__ == "__main__":
    main()
