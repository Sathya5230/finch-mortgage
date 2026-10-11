"""Correct and simplify the shared copy on the 'mortgage broker {city}' pages.

The template paragraphs claimed Finch compares ASB, Westpac, TSB, Resimac and
Bluestone (none are on the 23-lender panel), quoted cashback of "0.50-0.90%, up
to $20,000" with no source, said we model "every NZ lender", and listed which
banks offer the First Home Loan. They also averaged 25+ words per sentence. The
replacements say only what we can stand behind, in plain English, and keep each
page's own region and city names. 29 pages also had a doubled heading
("Hamilton & Hamilton & Waikato").

Also rewrites the same text in generate_city_broker_pages.py so new pages match.

Idempotent. Run with --apply to write; default is a dry run.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
LINK = 'style="color:var(--finch-forest);text-decoration:underline;font-weight:600;"'

REGEX = [
    ("lender panel", re.compile(
        r"Walking directly into your own bank limits your options to that single lender's pricing, scorecard, and product range\. "
        r"As an independent NZ mortgage broker covering (?P<region>[^<]+?), Finch compares your scenario across the full panel of "
        r"<strong>ANZ, ASB, BNZ, Westpac, TSB, SBS, The Co-operative Bank, Heartland</strong>, plus specialist non-bank lenders including "
        r"<strong>Resimac, Pepper Money, Avanti Finance, Liberty Financial, Basecorp, and Bluestone</strong>\. "
        r"Because each NZ lender's policy, test rate, and credit appetite differs week-to-week, knowing which one wins for your specific "
        r"situation can be the difference between a clean approval at a sharp rate and a frustrating decline\."),
     "If you go straight to your own bank, you only see that bank's rates and lending rules. "
     r"As an independent mortgage broker covering \g<region>, Finch compares your situation across our "
     f'<a href="../lenders.html" {LINK}>panel of 23 lenders</a>. '
     "That includes banks such as <strong>ANZ, BNZ, SBS Bank, The Co-operative Bank and Heartland Bank</strong>, "
     "and specialist lenders such as <strong>Pepper Money, Avanti Finance, Liberty Financial and Basecorp Finance</strong>. "
     "Lenders change their rules and rates often, and the right choice can mean a quick approval at a good rate instead of a decline."),

    ("doubled heading", re.compile(
        r"(?P<open><h3[^>]*>)(?P<city>[^<&]+?) &amp; (?P=city) &amp; (?P<rest>[^<]+?) — Local Market Notes</h3>"),
     r"\g<open>\g<city> &amp; \g<rest> — Local Market Notes</h3>"),

    ("first home paragraph", re.compile(
        r"We specialise in helping (?P<city>[^<]+?) first home buyers combine every available NZ deposit pathway — "
        r"KiwiSaver withdrawal \(after 3 years of contributions\), the (?P<kof><a [^>]*>Kāinga Ora First Home Loan</a>) "
        r"\(5% deposit through Westpac, SBS, The Co-operative Bank\), family guarantees, and new-build LVR exemption set by the "
        r"(?P<rbnz><a [^>]*>Reserve Bank's LVR rules</a>)\. Most first home buyers find their effective deposit goes much further "
        r"than they expected once we layer these properly\."),
     r"We help \g<city> first home buyers make the most of every deposit option. That can include a KiwiSaver withdrawal "
     r"(once you've been a member for three years), the \g<kof> (from a 5% deposit, through participating lenders), "
     r"a family guarantee, or the new-build exemption under the \g<rbnz>. Used together, these often stretch a deposit "
     r"further than people expect."),

    ("price band note", re.compile(
        r"\. Knowing which deposit pathway works best for each band — Kāinga Ora First Home Loan, family guarantee, "
        r"new-build LVR exemption, or standard 20% deposit — is part of how we match you to the right lender\."),
     ". These are indicative ranges only, not valuations. Your price range affects which deposit option suits you best, "
     "whether that's the First Home Loan, a family guarantee, a new build or a standard 20% deposit."),
]

PAIRS = {
    "We work with PAYE professionals and complex self-employed scenarios alike, including LTCs, trusts, and partnership entities — and we know which NZ lender's scorecard treats each scenario most favourably.":
        "We help salary and wage earners and self-employed people alike, including those trading through companies, look-through companies (LTCs), trusts and partnerships. We know which lenders are most likely to approve each kind of income.",
    "<strong>Lender match</strong> — we model your scenario across every NZ lender and recommend the strongest 1-2 options.":
        "<strong>Lender match</strong> — we compare your situation across our lender panel and recommend the best one or two options.",
    "For residential home loans, Finch charges you nothing. We are paid by the lender on settlement — not by you. That fee comes from the bank's distribution budget and would otherwise stay with the bank if you walked in direct. Our independent broker obligations under the Financial Markets Conduct Act mean we are legally required to act in your best interest, not the lender's. We hold FSP1011206 (FSPR FSP1011125) and are subject to NZ regulatory oversight.":
        "For residential home loans, Finch charges you nothing. The lender pays us a commission when your loan settles, and we disclose it in writing before you act on our advice. New Zealand law requires financial advisers to put your interests first. Finch Mortgages (FSP1011125) is an Authorised Body under the Financial Advice Provider licence held by Finsure New Zealand Limited (FSP1005389). "
        f'Read our <a href="../disclosure.html" {LINK}>disclosure statement</a>.',
    "If your fixed term is rolling off in the next 60 days, you're paying the loyalty tax. Refinancing through Finch typically captures a sharper rate plus 0.50-0.90% cashback (up to $20,000 depending on lender and loan size). We model your full economics — break fees, cashback clawback on existing loan, new cashback, legal costs — before recommending any move.":
        "If your fixed term ends in the next 60 days, it's a good time to check whether your bank's renewal offer is competitive. Some lenders offer cashback when you switch, but it usually comes with conditions, and leaving early can mean break fees or repaying an earlier cashback. We work out the full cost before recommending any move.",
    "refinance savings calculator</a> to ballpark the benefit.": "refinance savings calculator</a> for a quick estimate.",

    # Shared FAQ answers (visible accordion and FAQPage JSON-LD).
    "Yes. Banks reserve their sharpest rate discounts and cashback contributions for the broker channel. A broker compares 20+ lenders side-by-side to construct a competitive rate package you won't get walking in direct.":
        "Often, yes. A broker can compare offers from many lenders at once and ask them to sharpen their pricing. Sometimes your own bank's offer is the best one, and a good broker will tell you so.",
    "A local broker understands regional market conditions, localized bank valuation hurdles (like seismic registers or land classifications), and coordinates with local real estate agents and solicitors to speed up pre-approval.":
        "A local broker knows how lenders view your area, including valuation issues such as earthquake-prone buildings or land classifications, and works with local agents and lawyers to keep your purchase on track.",
    "A family guarantee allows parents to secure up to 20% of your home loan against the equity in their own property. This bridges your deposit gap without requiring parents to give you cash, avoiding low-equity bank premiums.":
        "A family guarantee lets a family member use the equity in their own home as extra security for part of your loan. It can cover a deposit gap without them handing over cash, and may help you avoid low-equity charges.",
}


def fix(src, hits):
    for name, rx, repl in REGEX:
        src, n = rx.subn(repl, src)
        hits[name] += n
    for old, new in PAIRS.items():
        if old in src:
            hits[old[:60]] += src.count(old)
            src = src.replace(old, new)
    return src


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    targets = [ROOT / f for f in files] + [ROOT / "generate_city_broker_pages.py"]
    hits = {name: 0 for name, _, _ in REGEX} | {old[:60]: 0 for old in PAIRS}
    changed = 0
    for p in targets:
        src = p.read_text(encoding="utf-8")
        out = fix(src, hits)
        if out != src:
            changed += 1
            if APPLY:
                p.write_text(out, encoding="utf-8")
    for k, n in hits.items():
        print(f"{n:4}  {k}")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
