"""Correct and simplify the shared copy on the 23 lender review pages.

Two statements were wrong: Finch is not itself FMA-licensed (it is an Authorised
Body under Finsure New Zealand Limited's FAP licence, per disclosure.html), and
the RBNZ LVR/DTI restrictions bind registered banks only, not "every lender" -
most of the panel are non-banks. The opening paragraph also listed all 23
lenders in a single 100-word sentence, the main reason these pages scored ~22 on
Flesch reading ease. The coverage paragraph now links each city to its broker page.

Also rewrites the same text in generate_lender_reviews.py so a re-run matches.

Idempotent. Run with --apply to write; default is a dry run.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
LINK = 'style="color:var(--finch-forest);text-decoration:underline;font-weight:600;"'

CITY_PAGES = [
    ("Auckland", "auckland-city"), ("Wellington", "wellington"),
    ("Christchurch", "christchurch"), ("Hamilton", "hamilton"),
    ("Tauranga", "tauranga"), ("Dunedin", "dunedin"),
    ("Palmerston North", "palmerston-north"), ("Napier", "napier-hawkes-bay"),
    ("Nelson", "nelson"), ("Queenstown", "queenstown"),
]
CITY_LINKS = [f'<a href="../blog/mortgage-broker-{slug}.html" {LINK}>{city}</a>' for city, slug in CITY_PAGES]
CITY_LIST = ", ".join(CITY_LINKS[:-1]) + " and " + CITY_LINKS[-1]

REGEX = [
    ("panel sentence", re.compile(
        r"As an independent NZ mortgage broker, Finch arranges home and property loans through our approved panel of 23 lenders — "
        r"registered NZ banks \([^)]*\), specialist non-bank lenders \([^)]*\), and member-owned credit unions \([^)]*\) — "
        r"so we recommend (?P<name>[^<]+?) only when their credit policy and pricing genuinely beat the alternatives for your exact situation\."),
     "Finch is an independent NZ mortgage broker with a panel of 23 lenders: registered banks, specialist non-bank lenders and a credit union. "
     r"We only recommend \g<name> when its lending rules and pricing beat the alternatives for your situation. "
     f'<a href="../lenders.html" {LINK}>See all 23 lenders</a>.'),

    ("rules paragraph", re.compile(
        r"(?P<name>[^<>]+?)'s deposit and serviceability settings sit inside the regulatory framework established in New Zealand — "
        r"the (?P<rbnz><a [^>]*>)RBNZ loan-to-value \(LVR\) and debt-to-income \(DTI\) restrictions</a> define the baseline every lender must work within\. "
        r"As an FMA-licensed financial advice provider, Finch is bound by the (?P<fma><a [^>]*>)Financial Markets Authority</a> Code of Conduct "
        r"to recommend (?P=name) only when it genuinely fits your requirements\."),
     r"In New Zealand, the \g<rbnz>Reserve Bank's loan-to-value (LVR) and debt-to-income (DTI) restrictions</a> apply to registered banks. "
     "Non-bank lenders aren't bound by them, but every lender must follow the responsible lending rules in the Credit Contracts and "
     "Consumer Finance Act (CCCFA). Finch gives advice as an Authorised Body under the Financial Advice Provider licence held by "
     "Finsure New Zealand Limited (FSP1005389), and follows the Code of Professional Conduct for Financial Advice Services, overseen by the "
     r"\g<fma>Financial Markets Authority</a>. That means we only recommend \g<name> when it suits your needs."),

    ("suits tail", re.compile(
        r"We see strongest outcomes when the client's income profile, deposit position, and intended property align with "
        r"(?P<name>[^<]+?)'s current credit appetite\. Outside those scenarios, another lender on our 23-lender panel will usually "
        r"price sharper or move faster — which is why we compare every option before recommending\."),
     r"It works best when your income, deposit and property type fit \g<name>'s current lending rules. If they don't, another "
     "lender on our panel may be cheaper or faster, so we compare options before recommending one."),

    ("coverage", re.compile(
        r"Finch arranges (?P<name>[^<]+?) property lending for clients across the country — Auckland, Wellington, Christchurch, "
        r"Hamilton, Tauranga, Dunedin, Palmerston North, Napier, Nelson, Queenstown, and regional New Zealand\. "
        r"We manage the entire application from initial assessment through to settlement\."),
     r"Finch arranges \g<name> lending for clients across New Zealand, including " + CITY_LIST.replace("\\", "\\\\")
     + ". We handle the whole application, from first assessment to settlement."),

    ("go direct", re.compile(
        r"Approaching (?P<name>[^<]+?) directly gives you only their proprietary products and credit criteria\. "
        r"Using Finch costs you nothing for residential home loans — where approved, the lender pays our commission on settlement — "
        r"and you receive an objective comparison across our entire panel of 23 approved lenders\. "
        r"Read our real (?P<cs><a [^>]*>NZ client case studies</a>) to see how we structure approvals\."),
     r"If you go to \g<name> directly, you only see its own products and lending rules. Through Finch, you get a comparison "
     "across our panel of 23 lenders. For residential home loans our advice is free, because the lender pays us a commission "
     r"when your loan settles. Read our \g<cs> to see how we structure approvals."),
]

PAIRS = {
    ">The Rules Every NZ Lender Works Within<": ">The Rules NZ Lenders Work Within<",
    "No single lender wins for every scenario. Pricing and policy vary based on your circumstances — registered banks provide sharp carded fixed rates for clean PAYE borrowers, while non-bank lenders like Avanti Finance, Basecorp Finance, or Pepper Money pick up cases that need common-sense credit assessments. Use our "
    f'<a href="../mortgage-rates.html" {LINK}>live NZ rates comparison</a> to see current pricing, then book a free consultation to match your scenario across our full approved panel.':
        "No lender is best for everyone. Banks usually offer their lowest rates to borrowers with steady salary or wage income and a good deposit. "
        "Non-bank lenders such as Avanti Finance, Basecorp Finance and Pepper Money often help when your situation is less straightforward. Check "
        f'<a href="../mortgage-rates.html" {LINK}>current NZ mortgage rates</a>, then book a free call and we\'ll compare your options across the whole panel.',
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
    targets = sorted((ROOT / "lenders").glob("*-review.html")) + [ROOT / "generate_lender_reviews.py"]
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
    print(f"\nfiles changed: {changed} of {len(targets)}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
