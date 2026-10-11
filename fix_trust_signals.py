"""Remove unsupported claims and off-panel lender references from shared copy.

Finch's lender panel is the 23 lenders listed on lenders.html. Several pages still
named lenders that were dropped from the panel (ASB, Westpac, TSB, Resimac,
Bluestone), quoted per-bank turnaround times and low-equity pricing nobody can
source, or used superlatives ("NZ's best", "Kiwis Most Trusted", "NZ's lowest")
that the Fair Trading Act requires a business to be able to prove. Mortgage
content is YMYL, so these hurt both compliance and how Google rates the site.

Idempotent. Run with --apply to write; default is a dry run.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
LINK = 'style="color:var(--finch-forest);font-weight:600;"'

PAIRS = {
    # Location-page taglines (also shown on the locations hub and homepage cards).
    "Secure your next residential property with NZ's best lending structures.":
        "Compare 20+ NZ lenders and get a home loan structured around you.",
    "Maximize leverage and structure portfolio lending tax-effectively.":
        "Structure investment lending around your equity, rental income and DTI limits.",
    "Know your borrowing capacity and bid at auction with absolute confidence.":
        "Know what you can borrow before you bid at auction.",
    "Secure finance using smart profit declarations and low-doc pathways.":
        "Get finance using your business financials, or low-doc options if you're newer to business.",

    # Homepage.
    "</svg> Kiwis Most Trusted Mortgage Broker": "</svg> Independent NZ Mortgage Broker",
    "Compare NZ's lowest home loan rates.": "Compare NZ home loan rates.",
    "Why check 5 different bank websites? We aggregate the latest advertised interest rates from New Zealand's top-tier banks weekly.":
        "Why check five different bank websites? See advertised rates from NZ banks in one place, then ask us what you could actually be offered.",
    "Finch searches 20+ banks and non-bank lenders simultaneously, finding the lowest rate and best structure for your specific situation.":
        "Finch compares 20+ banks and non-bank lenders to find a rate and loan structure that suit your situation.",
    "Visualize how extra payments aggressively reduce your loan term.":
        "See how extra repayments can shorten your loan term.",

    # The rates table is maintained by hand, so don't call it live.
    ">View Live NZ Rates<": ">View NZ Rates<",
    ">Live NZ Mortgage Rates<": ">NZ Mortgage Rates<",

    # Reviews page: "500+ happy clients" is a different claim from 500+ reviews.
    "Read 500+ verified client reviews for Finch Mortgages NZ. 5.0★ Google rating. Real stories from first home buyers, investors, and refinancers across NZ.":
        "Read Google reviews from Finch Mortgages clients across NZ (5.0★ rating). First home buyers, investors and refinancers share how the process went.",

    # how-to-choose-mortgage-broker-nz: the old test was one Finch's own panel fails.
    "Ask how many lenders the broker works with. A serious NZ mortgage broker should have at least 15 lenders on panel — all 5 main NZ banks (ANZ, ASB, BNZ, Westpac), the major regional/registered banks (TSB, SBS, The Co-operative Bank, Heartland), and a healthy suite of specialist non-banks (Resimac, Pepper Money, Avanti, Liberty, Bluestone, Basecorp). A broker with only 2-3 lenders is functionally a bank salesperson.":
        "Ask how many lenders the broker works with, and which ones. A good panel mixes registered banks with specialist non-bank lenders, because non-banks often help people the banks turn down. Panels differ, so also ask which lenders a broker can't access. A broker with only two or three lenders can't offer much real choice. (Finch works with "
        f'<a href="../lenders.html" {LINK}>23 lenders</a>.)',

    # mortgage-broker-vs-bank-nz.
    "Walking into your own bank gives you access to that bank's rates, scorecard, and product range — nothing more. A New Zealand mortgage broker (like Finch) compares your scenario across the full panel of <strong>ANZ, ASB, BNZ, Westpac, TSB, SBS, The Co-operative Bank, Heartland</strong>, plus the "
    f'<a href="../lenders/non-bank-lenders.html" {LINK}>specialist non-bank market</a> (<strong>Resimac, Pepper Money, Avanti, Liberty, Basecorp, Bluestone</strong>). Because every lender\'s pricing, test rate, and credit appetite differs week to week, the spread between best and worst offer for the same client is usually <strong>0.30-0.60 percentage points</strong> — equivalent to $1,500-$3,000 of saving per year on a $500,000 loan.':
        "Walking into your own bank gets you that bank's rates and lending rules, and nothing more. A New Zealand mortgage broker compares your situation across many lenders. Finch's panel of "
        f'<a href="../lenders.html" {LINK}>23 lenders</a> includes banks such as <strong>ANZ, BNZ, SBS Bank, The Co-operative Bank and Heartland Bank</strong>, plus '
        f'<a href="../lenders/non-bank-lenders.html" {LINK}>specialist non-bank lenders</a> such as <strong>Pepper Money, Avanti Finance, Liberty Financial and Basecorp Finance</strong>. Lenders price differently, and small gaps add up: on a $500,000 loan, every 0.30 percentage points is about <strong>$1,500 a year</strong> in interest.',

    # how-long-mortgage-approval-takes-nz: per-bank day counts had no source.
    "Lender-specific turnaround varies week to week and depends heavily on credit team workload. As a general 2026 guide: <strong>ANZ and ASB</strong> are usually the fastest for clean PAYE files (4-7 working days to pre-approval); <strong>BNZ and Westpac</strong> are typically 7-10 days; <strong>TSB, SBS, The Co-operative Bank</strong> run 7-12 days. Specialist non-banks (<strong>Resimac, Pepper Money, Avanti, Liberty</strong>) often pre-approve within 5-7 working days because their broker channel teams are more streamlined.":
        "Turnaround times differ between lenders and change from week to week, depending on how busy each credit team is. Straightforward applications from salary and wage earners are usually quickest. Self-employed income, unusual properties and missing documents all add time. Because we deal with lenders every day, we know which ones are moving quickly right now and can tell you what to expect before you apply.",

    # what-is-lvr-nz-mortgage.
    'Borrowers above 80% LVR pay a "Low Equity Premium" or LEM/LEP — typically an additional 0.25%-1.20% on the rate. Banks set their LEPs differently — ASB and Westpac structure them as a margin on the rate; ANZ and BNZ structure them as a one-off fee.':
        "Borrowers above 80% LVR usually pay extra for having less equity, known as a low equity margin or premium (LEM or LEP). Banks charge it in different ways: some add a margin to your interest rate, others charge a one-off fee.",
    "<strong>Kāinga Ora First Home Loan</strong> — 5% deposit (95% LVR) accepted through Westpac, SBS, The Co-operative Bank.":
        "<strong>Kāinga Ora First Home Loan</strong> — 5% deposit (95% LVR), available through participating lenders.",

    # deposit-requirements-nz.
    "<strong>Specialist lenders:</strong> Non-bank and specialist lenders (such as Resimac, Pepper Money, or Liberty) are not subject to the exact same RBNZ LVR restrictions as the main registered banks. They often provide excellent 10% or 15% deposit options, albeit usually at a slightly higher interest rate.":
        "<strong>Specialist lenders:</strong> Non-bank lenders (such as Pepper Money, Avanti Finance or Liberty Financial) aren't bound by the Reserve Bank's LVR restrictions, which apply to registered banks. Some will lend with a 10% or 15% deposit, usually at a higher interest rate.",

    # current-mortgage-rates-nz-explained.
    "It is impossible to comprehensively explain current New Zealand mortgage rates without addressing the Tier-2, or 'Non-Bank' lending sector. Institutions like Resimac, Pepper Money, and Avanti operate under entirely different legislations than registered retail banks.":
        "You can't fully explain New Zealand mortgage rates without the non-bank lenders. Lenders such as Pepper Money, Avanti Finance and Liberty Financial aren't registered banks, so the Reserve Bank's LVR and DTI restrictions don't apply to them. They still have to follow the responsible lending rules in the Credit Contracts and Consumer Finance Act (CCCFA).",

    # Shared bad-credit FAQ answer (visible copy and FAQPage JSON-LD).
    "specialist non-bank lenders (like Resimac, Pepper, and Avanti) manually assess bad credit files.":
        "specialist non-bank lenders (such as Pepper Money, Avanti Finance and Liberty Financial) assess bad credit files case by case.",

    # mortgage-broker-vs-bank-nz myths list.
    "Usually false. Banks reserve their sharpest rates for new business sourced through brokers.":
        "Not always. Banks often compete hardest for new customers, and a broker can put several lenders' offers side by side.",

    # first-home-guide: per-bank tendencies had no source; "Welcome Home" was renamed First Home Loan in 2019.
    "<strong>Kāinga Ora First Home Loan</strong> — buy with just 5% deposit through Westpac, SBS, The Co-operative Bank.":
        "<strong>Kāinga Ora First Home Loan</strong> — buy with a 5% deposit through participating lenders.",
    "Each of <strong>ANZ, ASB, BNZ, Westpac, TSB, SBS, The Co-operative Bank, and Heartland</strong> runs its own first-home-buyer scorecard. ANZ and ASB tend to be efficient on clean PAYE applications; BNZ and Westpac are often generous with professional buyers; SBS and The Co-operative Bank are strongest on Welcome Home / First Home Loan low-deposit cases. Specialist non-bank lenders (Resimac, Pepper Money, Avanti Finance, Liberty Financial) step in when you have variable income, a recent business start, or a credit history blemish.":
        "Every lender assesses first home buyers in its own way, so the same application can get a yes from one bank and a no from another. Some lenders are quicker with straightforward salary and wage applications, and some are more comfortable with low-deposit First Home Loan cases. Specialist non-bank lenders, such as Pepper Money, Avanti Finance and Liberty Financial, can help if your income varies, your business is new or your credit history has a blemish.",

    # refinance-guide: lenders don't pay a loyalty tax, and the claim had no source.
    'Every NZ lender pays a "loyalty tax" to existing customers in the form of slightly worse-than-market pricing, while reserving the sharpest deals (and the chunky cashback contributions) for new business. A refinance every 2–3 years often returns thousands of dollars and shaves years off your loan term.':
        "Your bank's renewal offer isn't always its best price, because lenders often compete hardest for new customers. Reviewing your loan every two to three years, and switching when the numbers work, can save you money and help you pay the loan off sooner.",

    # Related-resource card blurbs.
    ">Deposits across every NZ lender.<": ">Deposit rules across NZ lenders.<",
    ">Current rates across every NZ lender.<": ">Current NZ mortgage rates.<",

    # borrowing-power / mortgage-calculator: 2026 test and carded rate ranges went stale with the OCR rises.
    'Every NZ lender uses a "test rate" to size your loan — typically 7.0% to 9.0% in 2026, well above the actual carded rates of 5.5%–6.5%. This buffer protects against future rate rises and is the single biggest reason borrowers can borrow less than they expect. Each bank\'s test rate moves quarterly. Finch tracks the live test rates across every lender so you know which bank will lend you the most for your scenario before you apply. See live carded rates on our':
        'Every NZ lender uses a "test rate" to size your loan. It sits above the rate you would actually pay, as a buffer against future rate rises, and it is the biggest reason people can borrow less than they expect. Test rates differ between lenders and change as market rates move, so we check current test rates before recommending where to apply. See current advertised rates on our',
    "(what you'll actually pay in year one — see live rates on our":
        "(what you'll actually pay in year one — see current rates on our",
    "(what banks use to stress-test serviceability — typically 7.0% to 9.0% in 2026)":
        "(a higher rate banks use to check you could still afford repayments if rates rise)",
    "each lender uses a different stress-test rate (7.0%-9.0% range in 2026). Lower test rate = higher borrowing capacity.":
        "each lender uses its own stress-test rate, set above the rate you'll pay. A lower test rate means you can borrow more.",

    # Heartland announced in March 2025 it would phase out its online-only home loan.
    "a New Zealand-operated registered bank known for digital home loans, reverse mortgages, and business finance":
        "a New Zealand registered bank known for reverse mortgages, rural lending and business finance",
    "digital home loans, reverse mortgages (home equity release), rural finance, business mortgages":
        "home loans, reverse mortgages (home equity release), rural finance, business mortgages",
    "borrowers over 60 seeking home equity release / reverse mortgages, or prime borrowers seeking low-rate digital home loans":
        "borrowers over 60 seeking home equity release through a reverse mortgage, and borrowers with rural or business lending needs",
    "New Zealand's undisputed market leader in reverse mortgages and equity release":
        "One of New Zealand's best-known reverse mortgage providers",
    "Aggressive low-rate digital home loans for prime borrowers who qualify":
        "Publishes its home loan rates on its own website",
    "Digital home loans have strict criteria (clean PAYE, 20%+ deposit only)":
        "Announced in 2025 that it would phase out its online-only home loan",
    "Market leader in home equity release and reverse mortgages, alongside competitive digital home loans":
        "Known for home equity release and reverse mortgages, plus rural and business lending",

    # Welcome Home Loan was renamed the First Home Loan in 2019; the First Home Grant closed 22 May 2024.
    "with as little as 5% through Welcome Home loans (Kāinga Ora), family guarantees, or specialist non-bank lenders.":
        "with as little as 5% through the Kāinga Ora First Home Loan, a family guarantee, or specialist non-bank lenders.",
    "maximising their eligibility for the First Home Grant. By utilising these government schemes":
        "maximising their eligibility for the First Home Grant (which has since closed to new applications). By utilising these government schemes",
}


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    hits = {old: 0 for old in PAIRS}
    changed = 0
    for f in files:
        p = ROOT / f
        src = p.read_text(encoding="utf-8")
        out = src
        for old, new in PAIRS.items():
            if old in out:
                hits[old] += out.count(old)
                out = out.replace(old, new)
        if out != src:
            changed += 1
            if APPLY:
                p.write_text(out, encoding="utf-8")
    for old, n in hits.items():
        print(f"{n:4}  {old[:90]}")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
