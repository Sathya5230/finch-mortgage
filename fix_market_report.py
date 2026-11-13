"""Rebuild market-report.html without unverifiable market statistics.

The page carried invented rate averages, regional price figures, forecasts and
an unattributed adviser quote. This replaces everything between the hero and
the CTA with an evergreen explainer of the settings that drive NZ mortgage
rates and lending, pointing to official sources for live figures. It also
rewrites link blurbs elsewhere that promised "latest" or "live" commentary.
Idempotent; dry run unless --apply.
"""
import glob
import re
import sys

from fix_remove_weekly_reports import MR_END, MR_START, guides_block

START, END = "<!-- FINCH-MARKET:START -->", "<!-- FINCH-MARKET:END -->"
REVIEWED = "November 2026"
A = 'style="color:var(--finch-forest);text-decoration:underline;font-weight:600;"'
RBNZ = "https://www.rbnz.govt.nz/"
RBNZ_LVR = "https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions"

CARDS = [
    ("The Official Cash Rate",
     "The Reserve Bank sets the OCR several times a year. Floating mortgage rates usually follow it within days. Fixed rates move earlier, on what markets expect the OCR to do next, so they can fall before a cut or rise before a hike.",
     "blog/how-ocr-affects-mortgages-nz", "How the OCR affects your mortgage"),
    ("Deposit rules (LVR)",
     "The Reserve Bank limits how much low-deposit lending banks can do. Most owner-occupier loans need a 20% deposit and most loans on existing rentals need about 30%, with a limited allowance above those levels that was widened on 1 December 2025. New builds are exempt.",
     "blog/what-is-lvr-nz-mortgage", "How LVR works"),
    ("Debt-to-income limits",
     "Banks can make only a small share of new loans to owner-occupiers borrowing more than six times their income, or investors borrowing more than seven times. New builds are exempt. For many buyers this now sets the ceiling, not the deposit.",
     "blog/dti-calculator-debt-to-income-nz", "DTI limits explained"),
    ("Each bank's test rate",
     "Lenders check you could afford the loan at a rate above the one you'll pay. Each lender sets its own test rate and changes it as the market moves, which is why two banks can approve very different amounts for the same person.",
     "blog/mortgage-stress-test-rate-nz", "The stress test rate"),
    ("Tax settings for investors",
     "Interest on residential rental loans has been fully deductible again since 1 April 2025, and the bright-line test applies to sales within two years. Both change the sums on a rental, so check your own position with an accountant.",
     "blog/mortgage-interest-tax-deductible-nz", "Interest deductibility"),
    ("Help for first home buyers",
     "The First Home Grant closed on 22 May 2024. The Kāinga Ora First Home Loan remains, letting eligible buyers start from a 5% deposit, and KiwiSaver withdrawals are still available after three years of membership.",
     "blog/first-home-loan-kainga-ora-nz", "The First Home Loan"),
]

SOURCES = [
    ("The OCR, and the dates of each decision", "Reserve Bank of New Zealand", RBNZ),
    ("Deposit (LVR) and debt-to-income settings", "Reserve Bank of New Zealand", RBNZ_LVR),
    ("House sales and median prices", "Real Estate Institute of New Zealand", "https://www.reinz.co.nz/"),
    ("Market rents by suburb", "Tenancy Services", "https://www.tenancy.govt.nz/rent-bond-and-bills/market-rent/"),
    ("Inflation, wages and population", "Stats NZ", "https://www.stats.govt.nz/"),
    ("First Home Loan criteria", "Kāinga Ora", "https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/"),
    ("Tax rules for property", "Inland Revenue", "https://www.ird.govt.nz/"),
]


def block():
    cards = "".join(
        f'<div class="benefit-card bg-white"><h3>{h}</h3><p>{p}</p>'
        f'<a href="{href}" style="font-size:0.8rem;font-weight:700;color:var(--finch-forest);text-decoration:none;'
        f'display:inline-block;margin-top:0.75rem;">{label} →</a></div>\n'
        for h, p, href, label in CARDS)
    td = 'style="padding:0.7rem 0.9rem;border-bottom:1px solid rgba(180,178,169,0.3);font-size:0.93rem;vertical-align:top;"'
    rows = "".join(
        f'<tr><td {td}>{what}</td><td {td}><a href="{url}" rel="noopener" target="_blank" {A}>{who}</a></td></tr>\n'
        for what, who, url in SOURCES)
    return f"""{START}
<section style="background:var(--finch-forest); padding:5rem 0 4rem; position:relative; overflow:hidden;">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 50%, rgba(98,162,154,0.15) 0%, transparent 65%);pointer-events:none;"></div>
<div class="container">
<nav class="breadcrumb" style="margin-bottom:1.5rem;"><a href="./" style="color:rgba(255,255,255,0.65);">Home</a><span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span><span style="color:white;">Market Report</span></nav>
<div style="display:inline-flex;align-items:center;gap:0.5rem;background:rgba(255,255,255,0.1);color:var(--finch-sage);border-radius:9999px;padding:0.35rem 1rem;font-size:0.7rem;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:1.5rem;border:1px solid rgba(98,162,154,0.3);">NZ Mortgage Market</div>
<h1 style="color:white;font-family:var(--font-display);font-size:clamp(2rem,4.5vw,3.5rem);font-weight:700;line-height:1.1;margin-bottom:1rem;">What Moves NZ Mortgage Rates<br/><em style="color:var(--finch-sage);font-style:italic;font-weight:400;">and Lending Rules.</em></h1>
<p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Reviewed: {REVIEWED}</p>
<p style="color:rgba(255,255,255,0.75);max-width:600px;line-height:1.75;">Rates and prices change every week, and we don't publish numbers we can't keep current. This page explains the settings behind them, what each means for your borrowing, and where to find today's official figures.</p>
</div>
</section>

<section style="padding:5rem 0;background:var(--finch-mist);">
<div class="container">
<div class="section-label"><span>The Settings</span></div>
<h2 class="section-heading" style="margin-bottom:0.75rem;">Six things that decide<br/><em>what you can borrow.</em></h2>
<p style="color:var(--neutral-medGray);max-width:680px;line-height:1.7;margin-bottom:2.5rem;">Settings are as at {REVIEWED}. The Reserve Bank and the Government change them from time to time, so confirm the current position with the sources further down.</p>
<div class="cols-3">
{cards}</div>
</div>
</section>

<section style="padding:5rem 0;background:white;">
<div class="container" style="max-width:860px;">
<div class="section-label"><span>Live Figures</span></div>
<h2 class="section-heading" style="margin-bottom:0.75rem;">Where to find<br/><em>today's numbers.</em></h2>
<p style="color:var(--neutral-medGray);line-height:1.7;margin-bottom:1.5rem;">These organisations publish the figures themselves. Go to them for anything you plan to act on.</p>
<div style="overflow-x:auto;margin-bottom:1.5rem;"><table style="width:100%;border-collapse:collapse;background:white;">
<thead><tr><th style="text-align:left;padding:0.7rem 0.9rem;border-bottom:2px solid rgba(16,68,62,0.25);font-size:0.85rem;">What you want to know</th><th style="text-align:left;padding:0.7rem 0.9rem;border-bottom:2px solid rgba(16,68,62,0.25);font-size:0.85rem;">Who publishes it</th></tr></thead>
<tbody>
{rows}</tbody></table></div>
<p style="color:var(--neutral-medGray);line-height:1.7;">Mortgage rates are set by each lender and change often. Our <a href="mortgage-rates" {A}>mortgage rates page</a> explains how to compare them, and we'll send you current rates from the 23 lenders on our panel if you <a href="contact" {A}>get in touch</a>.</p>
</div>
</section>

{guides_block()}{END}
"""


HEAD = [
    (re.compile(r'<title>.*?</title>', re.S), "<title>NZ Mortgage Market: What Moves Rates &amp; Lending | Finch</title>"),
    (re.compile(r'(<meta content=")[^"]*(" (?:property="og:title"|name="twitter:title")/>)'),
     r"\1NZ Mortgage Market: What Moves Rates &amp; Lending | Finch\2"),
    (re.compile(r'"headline": "NZ Mortgage Market Report 2026[^"]*"'), '"headline": "What moves NZ mortgage rates and lending rules"'),
    (re.compile(r'"description": "OCR currently at[^"]*"'),
     '"description": "How the OCR, deposit rules, debt-to-income limits and bank test rates shape NZ home lending, with links to official sources for current figures."'),
    (re.compile(r'"dateModified": "2026-0[56]-\d\d"'), '"dateModified": "2026-11-13"'),
    (re.compile(r'(<meta content=")NZ mortgage market report 2026, NZ housing market analysis[^"]*(" name="keywords"/>)'),
     r"\1NZ mortgage market, what affects mortgage rates NZ, OCR and mortgage rates, LVR rules NZ, DTI limits NZ, NZ lending rules\2"),
]
CTA_TEXT = {
    "Ready to make your move in 2026's market?": "Want to know what this means for you?",
    "Our advisers monitor the market daily. Book a free consultation and we'll tell you exactly what today's rates mean for your situation.":
        "Book a free consultation and we'll show you current rates from our lender panel and what you could borrow.",
}
BLURB = re.compile(r'((?:NZ |Finch )?(?:Mortgage )?Market Report</strong><span[^>]*>)[^<]*')
BLURB_NEW = "What moves NZ rates and lending rules."
SKIP_DIRS = ("node_modules", ".venv", "drafts", "output", "published", "rewrites", "research", "topics")


def fix_page(t):
    new = block()
    if START in t:
        t = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", lambda m: new, t, flags=re.S)
    else:
        a, b = t.find("<!-- ── HERO ── -->"), t.find("<!-- ── CTA ── -->")
        if a < 0 or b < 0:
            sys.exit("market-report.html: hero/CTA anchors not found")
        t = t[:a] + new + t[b:]
    assert t.count(MR_START) == 1 and t.count(MR_END) == 1
    for pat, rep in HEAD:
        t = pat.sub(rep, t)
    for a, b in CTA_TEXT.items():
        t = t.replace(a, b)
    return t


def main():
    apply = "--apply" in sys.argv
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)] + glob.glob("*.py")
    changed = 0
    for f in files:
        if f == "fix_market_report.py":
            continue
        with open(f, encoding="utf-8") as fh:
            before = fh.read()
        after = BLURB.sub(lambda m: m.group(1) + BLURB_NEW, before)
        if f == "market-report.html":
            after = fix_page(after)
        if after != before:
            changed += 1
            if apply:
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(after)
    print(f"files changed: {changed}", "APPLIED" if apply else "(dry run)")


if __name__ == "__main__":
    main()
