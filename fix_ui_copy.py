"""Remove filler text and wrong details from shared UI, heroes and the FAQ page.

What it fixes:
- Menus and footer: emoji in the Resources menu, a footer tagline promising
  "fast approvals", and no links to the newer calculators.
- aria-label="Link icon" / "Interactive button" on thousands of links and
  buttons, which made screen readers announce those words instead of the
  link text. Removed wherever the element has its own text.
- Service page heroes written as slogans ("Secure Your Dream Home", "Save
  Thousands Today"), and stat tiles with unverifiable counts or a wrong
  investor LVR.
- map.html said the office was in Newmarket. It is in Te Atatu South.
- faq.html had four questions, a promise to respond "within 1 hour" and
  approval turnaround times. It is rebuilt from FAQS below, with matching
  FAQPage JSON-LD.

Idempotent. Run with --apply to write; default is a dry run. Run before
strip_html_ext.py (it handles both .html and extensionless links).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
EM = '<br/><em style="font-style:italic;color:var(--finch-forest);">'

SITEWIDE = {
    ">📊 Market Report<": ">Market Report<",
    ">🏨 Lenders<": ">Lenders<",
    ">📍 Locations<": ">Locations<",
    "New Zealand's trusted independent mortgage broker. Expert advice, 23 lenders, fast approvals.":
        "Independent mortgage adviser in Te Atatu South, Auckland. We compare 23 lenders for home buyers and homeowners across New Zealand.",
    ">Secure your dream home<": ">Buying a home to live in<",
    "dream home?": "home?",
}

# (path, old, new). Old strings are exact; a pair that no longer matches is skipped.
PAGES = [
    ("services/asset-finance.html", f"Asset Finance NZ to{EM}Drive Your Business Forward.</em>", f"Asset Finance NZ{EM}Vehicles, Plant and Equipment.</em>"),
    ("services/asset-finance.html", "From company fleets to heavy equipment and machinery, we structure asset finance to protect your cash flow and scale your operations.",
     "Finance for vehicles, machinery and equipment, set up so the repayments suit your cash flow. We compare lenders and explain the difference between a loan, a lease and hire purchase."),
    ("services/commercial-property.html", f"Commercial Property Loans NZ to{EM}Invest in Real Estate.</em>", f"Commercial Property Loans NZ{EM}Offices, Retail and Industrial.</em>"),
    ("services/commercial-property.html", "Commercial lending is complex. We negotiate directly with bank commercial managers and private lenders to secure favourable LVRs and interest rates for your portfolio.",
     "Commercial lending is assessed differently from a home loan. We prepare the application, approach the lenders that suit the property, and explain the deposit, term and rate you can expect."),
    ("services/construction-loan.html", f"Construction Loans NZ to{EM}Build From the Ground Up.</em>", f"Construction Loans NZ{EM}Turnkey and Progress-Payment Builds.</em>"),
    ("services/construction-loan.html", "Construction finance requires careful timing and cash flow management. We specialise in turnkey builds, progress payments, and multi-unit development funding.",
     "When you build, the loan is drawn in stages. We arrange lending for turnkey contracts and progress-payment builds, and manage the drawdowns with your builder and lender."),
    ("services/first-home-buyer.html", f"First Home Buyer Loans to{EM}Buy with Confidence.</em>", f"First Home Buyer Loans NZ{EM}From Deposit to Keys.</em>"),
    ("services/first-home-buyer.html", "Finch guides first home buyers through every step — KiwiSaver withdrawals, the Kāinga Ora First Home Loan, low-deposit options, and everything in between. We've helped 300+ Kiwis get their first set of keys.",
     "We help first home buyers work out their deposit, including KiwiSaver, the Kāinga Ora First Home Loan and low-deposit options, then compare lenders and manage the application through to settlement."),
    ("services/home-loan.html", f"NZ Home Loans to{EM}Secure Your Dream Home.</em>", f"Home Loans NZ{EM}Compare 23 Lenders.</em>"),
    ("services/home-loan.html", "Finch guides buyers through every step of purchasing a home. From exploring loan options to matching you with the perfect lender, we ensure a smooth, transparent process.",
     "Buying a home to live in? We work out what you can borrow, compare the 23 lenders on our panel and manage the application through to settlement. There's no fee for residential home loans."),
    ("services/home-loan.html", "See exactly how much an NZ bank will lend you on your income.", "A rough idea of what lenders may lend on your income."),
    ("services/investment-property.html", f"NZ Investment Property Loans to{EM}Grow Your Portfolio.</em>", f"Investment Property Loans NZ{EM}Rental and Portfolio Lending.</em>"),
    ("services/investment-property.html", "Whether it's your first investment property or your tenth, Finch structures your loan to maximise cash flow, tax efficiency, and long-term wealth growth. NZ LVR rules, interest-only, and portfolio lending — we know it all.",
     "For a first rental or another for the portfolio, we work out what you can borrow against your equity, explain the investor LVR and DTI rules, and structure the lending across your properties."),
    ("services/next-home-buyer.html", f"NZ Next-Home Buyer Loans to{EM}Upgrade or Move with Ease.</em>", f"Next Home Loans NZ{EM}Buying and Selling Together.</em>"),
    ("services/pre-approval.html", f"NZ Mortgage Pre-Approval to{EM}Know Your Buying Power.</em>", f"Mortgage Pre-Approval NZ{EM}Know Your Budget Before You Offer.</em>"),
    ("services/pre-approval.html", "Before you fall in love with a property, get a conditional mortgage pre-approval so you can bid at auction and negotiate with complete confidence.",
     "A pre-approval tells you how much a lender will lend, and on what conditions, before you make an offer or bid at auction. We compare lenders and prepare the application for you."),
    ("services/refinance.html", f"Refinance Your NZ Mortgage &amp;{EM}Save Thousands Today.</em>", f"Refinance Your Mortgage NZ{EM}Compare Before You Refix.</em>"),
    ("services/self-employed.html", f"Self-Employed Home Loans NZ —{EM}We Specialise in You.</em>", f"Self-Employed Home Loans NZ{EM}For Contractors and Business Owners.</em>"),
    ("services/self-employed.html", "Being self-employed shouldn't stop you from owning your home. Finch works with contractors, sole traders, business owners, and freelancers to find lenders who understand variable income — and approve the loan.",
     "Self-employed income doesn't fit on a payslip, and lenders read it in different ways. We work with contractors, sole traders and business owners to present the income properly and find the lenders whose rules suit it."),

    # Stat tiles: counts nobody can verify, and a wrong investor LVR.
    ("services/home-loan.html", '<div class="stat-number">500+</div><div class="stat-label">Homes Funded</div>', '<div class="stat-number">15+ yrs</div><div class="stat-label">Bank Lending Experience</div>'),
    ("services/first-home-buyer.html", '<div class="stat-number">300+</div><div class="stat-label">First Homes Funded</div>', '<div class="stat-number">15+ yrs</div><div class="stat-label">Bank Lending Experience</div>'),
    ("services/next-home-buyer.html", '<div class="stat-number">100+</div><div class="stat-label">Upgrades Funded</div>', '<div class="stat-number">15+ yrs</div><div class="stat-label">Bank Lending Experience</div>'),
    ("services/investment-property.html", '<div class="stat-number">40%</div><div class="stat-label">Max LVR for Investors</div>', '<div class="stat-number">70%</div><div class="stat-label">Standard Investor LVR</div>'),

    ("services-overview.html", f"Every Mortgage Solution{EM}Under One Roof.</em>", f"NZ Mortgage Services{EM}Home, Investment and Business Lending.</em>"),
    ("services-overview.html", "Whether you're buying your first home, growing your investment portfolio, refinancing, or building from scratch — Finch has a tailored solution for you. Explore all 10 of our mortgage services below.",
     "Ten mortgage services, from first homes and refinancing to construction, investment and commercial lending. Choose the one that matches what you're doing."),
    ("blog.html", f"NZ Mortgage Blog &amp;{EM}Expert Insights.</em>", f"NZ Mortgage Blog{EM}Guides and Explainers.</em>"),
    ("blog.html", "Mortgage guides, NZ rate updates, and property tips from the Finch team.", "Plain-English guides to home loans, refinancing, deposits and interest rates in New Zealand."),
    ("lenders.html", "We partner with 23 approved lenders across Registered Banks, Non-Bank Lenders, Specialist Lenders, and Credit Unions to ensure you get the most competitive rates and terms, tailored to your exact situation.",
     "Our panel has 23 lenders: registered banks, non-bank lenders, specialist lenders and a credit union. We compare them against your situation and explain why one suits you better than another."),
    ("case-studies.html", "Every client situation is different. These case studies show how Finch finds creative solutions where others say no — and delivers outcomes that genuinely change lives.",
     "Every client's situation is different. These case studies show how particular lending problems were worked through, and what the outcome was."),
    ("map.html", "Finch Mortgages is based in Auckland but serves clients across all of New Zealand. Meet us in person at our Newmarket office, or connect virtually — we work the way you work.",
     "Finch Mortgages is based in Te Atatu South, Auckland, and works with clients across New Zealand. Meet us at the office, or by phone or video."),

    ("map.html", "Meeting face to face can help when you are working through a complex scenario, want to bring supporting documents in person, or simply prefer discussing your mortgage in a room rather than over the phone. Our Newmarket office is set up for exactly that kind of conversation, with parking and public transport links nearby for clients travelling in from other parts of Auckland.",
     "Some people prefer to go through a mortgage in person, particularly when there are documents to look at together. You're welcome at our office at 17a Marlene Ave, Te Atatu South. Please book a time first so we can have everything ready."),
    ("map.html", "Distance is not a barrier to getting the same level of service. Clients outside Auckland are supported through video calls, phone appointments, and secure digital document sharing, so the advice process looks the same whether you are down the road or at the other end of the country.",
     "If you're outside Auckland, or would just like to save the trip, we work the same way by phone and video, and you upload documents through a secure link."),
    ("map.html", f"Find Us &amp; Our{EM}Service Areas.</em>", f"Finch Mortgages Office{EM}Te Atatu South, Auckland.</em>"),

    # Homepage: the hero already shows the client count and rating, so the band below repeats them.
    ("index.html", '<div class="stat-item"><div class="stat-number">500+</div><div class="stat-label">Happy Clients</div></div>',
     '<div class="stat-item"><div class="stat-number">15+ yrs</div><div class="stat-label">Bank Lending Experience</div></div>'),
    ("index.html", '<div class="stat-item"><div class="stat-number">5.0★</div><div class="stat-label">Google Rating</div></div>',
     '<div class="stat-item"><div class="stat-number">$0</div><div class="stat-label">Fee on Residential Home Loans</div></div>'),
    ("index.html", "<span>1. Our Services</span>", "<span>Our Services</span>"),
    ("index.html", "<span>2. Interactive Tools</span>", "<span>Calculators</span>"),
    ("index.html", "Discover exactly how much the banks will lend you today.", "A rough idea of what lenders may lend you."),
    ("services/commercial-property.html", "Specialist loans for offices, retail, warehouses, and industrial sites — navigating complex commercial lending criteria for you.",
     "Loans for offices, retail, warehouses and industrial sites, assessed on the property's income and your business."),
    ("services/first-home-buyer.html", "We help you navigate first-home withdrawal rules — what qualifies, how much you can access, and timing.",
     "We explain the first-home withdrawal rules: who qualifies, how much you can take out, and how long it takes."),
    ("calculators/extra-repayment.html", "See exactly how much time and interest you can save by adding a little extra to your regular mortgage repayments.",
     "See how much time and interest a higher regular repayment takes off your loan."),
    ("calculators/borrowing-power.html", "A larger deposit means lower LVR, which unlocks better rates and higher loan amounts.",
     "A larger deposit means a lower LVR, which usually means a lower rate and more lenders to choose from."),
    ("calculators/refinance-savings.html", "Enter your current loan details and compare against a new rate. See exactly how much you could save per month and over the life of your loan.",
     "Enter your current loan and a new rate to see the difference in repayments each month and over the rest of the loan."),

    # FAQ hero and sidebar.
    ("faq.html", "Transparency is our core principle. If you don't find the clarity you seek here, our adviser is available 8am–6pm, 7 days a week — and responds within 1 hour.",
     "Straight answers to the questions we're asked most about deposits, borrowing, interest rates and how we work."),
    ("faq.html", ">Direct Inquiry</h2>", ">Talk to us</h2>"),
    ("faq.html", "For complex financial structures or urgent rate locks, please connect with our Priority Desk directly.", "Can't find your answer? Call or email and we'll come back to you."),
    ("faq.html", ">Priority Desk</p>", ">Phone</p>"),
    ("faq.html", ">Message Portal</p>", ">Email</p>"),
    ("faq.html", ">0273433293</p>", ">027 343 3293</p>"),
]

A = 'style="color:var(--finch-forest);font-weight:600;text-decoration:underline;"'
FAQS = [
    ("Deposits &amp; first homes", [
        ("How much deposit do I need to buy a home in NZ?",
         f'Most buyers need 20%. Some lenders accept 10% to 19% and charge a low equity margin, eligible first home buyers can use the Kāinga Ora First Home Loan with 5%, and new builds can need less than 20%. Our <a href="blog/deposit-needed-home-loan-nz.html" {A}>deposit guide</a> compares the options, and the <a href="calculators/lvr-calculator.html" {A}>LVR calculator</a> shows where you sit.'),
        ("Can I use my KiwiSaver to buy my first home?",
         f'Usually, yes. After three years as a member you can withdraw your balance apart from $1,000 to buy a home you\'ll live in. The money is paid to your lawyer, and the application takes a few weeks. See our <a href="blog/kiwisaver-first-home-withdrawal.html" {A}>KiwiSaver first-home withdrawal guide</a>.'),
        ("Is the First Home Grant still available?",
         f'No. The First Home Grant closed to new applications in May 2024. KiwiSaver withdrawals and the Kāinga Ora First Home Loan are still available. See <a href="blog/first-home-grant-nz-closed-alternatives.html" {A}>what replaced the First Home Grant</a>.'),
        ("Can my parents help with my deposit?",
         f'Yes. Most lenders accept a gift from family with a signed gift letter, and a parent can also use equity in their own home as a guarantee. See <a href="blog/gifted-deposit-home-loan-nz.html" {A}>gifted deposits</a> and <a href="blog/guarantor-home-loan-nz.html" {A}>guarantees</a>.'),
    ]),
    ("Borrowing", [
        ("How much can I borrow?",
         f'It depends on three things: whether you can afford the repayments at the lender\'s higher test rate, how your total debt compares with your income, and how much deposit you have. Lenders work these out differently, so the answer varies between them. Read <a href="blog/how-much-can-i-borrow.html" {A}>how much can I borrow</a> or try the <a href="calculators/borrowing-power.html" {A}>borrowing power calculator</a>.'),
        ("What is a debt-to-income (DTI) limit?",
         f'Reserve Bank rules limit how much lending banks can do above six times income for owner-occupiers and seven times for investors. New builds are exempt. Check yours with the <a href="calculators/dti-calculator.html" {A}>DTI calculator</a>.'),
        ("How long does a pre-approval last?",
         f'Usually 60 to 90 days, depending on the lender, and it can normally be renewed with updated documents. See <a href="services/pre-approval.html" {A}>mortgage pre-approval</a>.'),
        ("How long does a home loan approval take?",
         f'It depends on the lender and on how complete your documents are. Some decisions come back within days and others take longer, particularly at busy times. Having everything on our <a href="blog/mortgage-document-checklist-nz.html" {A}>document checklist</a> ready is the best way to avoid delays.'),
        ("Can I get a home loan if I'm self-employed?",
         f'Yes. Most lenders want two years of financial statements, and some will consider one year or other evidence of income. See <a href="services/self-employed.html" {A}>self-employed home loans</a>.'),
    ]),
    ("Rates &amp; refinancing", [
        ("Should I fix or float my mortgage?",
         f'Most borrowers fix most of their loan for certainty and keep a smaller part floating for extra repayments. The right split depends on your plans. See <a href="blog/fixed-vs-floating-mortgage-nz.html" {A}>fixed vs floating</a>.'),
        ("What is a break fee?",
         f'A charge that can apply if you repay or refinance a fixed-rate loan before the term ends and interest rates have fallen since you fixed. Only your bank can give the exact figure. Our <a href="calculators/break-fee-calculator.html" {A}>break fee calculator</a> gives an estimate.'),
        ("Will I have to pay back my cashback if I change banks?",
         f'Possibly. Most cash contributions have to be repaid in full or in part if you leave within a set period, commonly three or four years. Check your loan agreement, or use the <a href="calculators/cashback-clawback-calculator.html" {A}>cashback clawback calculator</a>.'),
        ("When should I look at refinancing?",
         f'About two months before a fixed term ends is a good time, because there\'s no break fee on the expiry date and lenders will often hold a rate for you. See our <a href="guides/refinance-guide.html" {A}>refinance guide</a>.'),
    ]),
    ("Working with Finch", [
        ("Does it cost anything to use Finch?",
         f'Not for residential home loans. The lender pays us a commission when your loan settles. If a fee would ever apply, for example on some commercial lending, we tell you before you commit. Our <a href="disclosure.html" {A}>disclosure statement</a> has the detail.'),
        ("Which lenders do you work with?",
         f'Our panel has 23 lenders: registered banks, non-bank lenders, specialist lenders and a credit union. See the <a href="lenders.html" {A}>full list of lenders</a>.'),
        ("Are you licensed?",
         f'Yes. Finch Mortgages Limited (FSP1011125) is an authorised body under the financial advice provider licence held by Finsure New Zealand Limited (FSP1005389), which is issued by the Financial Markets Authority. If we can\'t resolve a complaint, you can take it to Financial Services Complaints Ltd (FSCL) at no cost.'),
        ("Where are you, and when are you open?",
         f'Our office is at 17a Marlene Ave, Te Atatu South, Auckland. We\'re open Monday to Friday 9am to 6pm and Saturday 10am to 2pm, and we work with clients across New Zealand by phone and video. <a href="contact.html" {A}>Contact us</a> to book a time.'),
    ]),
]

FAQ_ICON = ('<svg class="faq-icon" fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" '
            'stroke-width="2.5" style="display:inline-block;vertical-align:middle;flex-shrink:0;transition: transform 0.3s;" '
            'viewBox="0 0 24 24" width="20"><line x1="12" y1="5" x2="12" y2="19" class="vertical-line" '
            'style="transition: opacity 0.3s;"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>')


def text_of(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).replace("&amp;", "&").strip()


def faq_column(stripped):
    out = ["<!-- FAQ Content -->", '<div class="lg-col-span-8 space-y-16">']
    for cat, items in FAQS:
        out.append('<div class="reveal">\n<div class="flex items-center gap-3 mb-10">\n'
                   '<span class="bg-brand-gold" style="height: 1px; width: 2rem;"></span>\n'
                   f'<h2 class="text-xs uppercase font-bold tracking-widest text-brand-amber" style="margin:0;">{cat}</h2>\n'
                   '</div>\n<div class="space-y-4">')
        for q, a in items:
            if stripped:
                a = a.replace('.html"', '"')
            out.append(f'<div class="faq-item">\n<button class="faq-trigger">\n<span>{q}</span>\n{FAQ_ICON}\n</button>\n'
                       f'<div class="faq-content">\n<p>{a}</p>\n</div>\n</div>')
        out.append("</div>\n</div>")
    out.append("</div>\n</div>\n")
    return "\n".join(out)


def rebuild_faq(html):
    stripped = 'href="contact"' in html
    a, b = html.index("<!-- FAQ Content -->"), html.index("</main>")
    html = html[:a] + faq_column(stripped) + html[b:]
    entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": text_of(ans)}}
                for _, items in FAQS for q, ans in items]
    m = re.search(r'<script type="application/ld\+json">(\{(?:(?!</script>).)*?"@type": "FAQPage".*?)</script>', html, re.S)
    data = json.loads(m.group(1))
    data["mainEntity"] = entities
    return html[:m.start(1)] + json.dumps(data, indent=2, ensure_ascii=False) + html[m.end(1):]


LABEL = re.compile(r'<(a|button)\b([^>]*?)\s+aria-label="(?:Link icon|Interactive button)"([^>]*)>(.*?)</\1>', re.S)


def drop_junk_labels(html):
    def fix(m):
        if text_of(m.group(4)):
            return f"<{m.group(1)}{m.group(2)}{m.group(3)}>{m.group(4)}</{m.group(1)}>"
        return m.group(0)
    return LABEL.sub(fix, html)


CALC_LINK = re.compile(r'(<a( class="dropdown-item")? href="((?:\.\./)?)calculators/rental-yield-calculator(\.html)?">Rental Yield</a>)(?!<a[^>]*break-fee)')


def add_calculators(html):
    def fix(m):
        cls, pre, ext = m.group(2) or "", m.group(3), m.group(4) or ""
        extra = "".join(f'<a{cls} href="{pre}{href}">{label}</a>' for href, label in [
            (f"calculators/break-fee-calculator{ext}", "Break Fee"),
            (f"calculators/lvr-calculator{ext}", "LVR"),
            (f"calculators{ext}", "All Calculators"),
        ])
        return m.group(1) + extra
    return CALC_LINK.sub(fix, html)


CITY_H1 = re.compile(r'<h1>(Home Loan|Refinance|Pre-Approval|First Home Buyer|Investment Property|Self-Employed Mortgage)<br/>(<em[^>]*>)([^<]+?)\.</em></h1>')
CITY_H1_NAMES = {
    "Home Loan": "Home Loans in", "Refinance": "Refinance Your Mortgage in", "Pre-Approval": "Mortgage Pre-Approval in",
    "First Home Buyer": "First Home Buyer Loans in", "Investment Property": "Investment Property Loans in",
    "Self-Employed Mortgage": "Self-Employed Home Loans in",
}
LENDER_HUBS = {
    "Major & Registered Banks (Tier 1) in NZ | Finch Mortgage": "NZ Bank Home Loans: Major and Registered Banks | Finch",
    ">Major & Registered Banks (Tier 1)</h1>": ">Bank Home Loans in NZ: Major and Registered Banks</h1>",
    "Non-Bank Lenders in NZ | Finch Mortgage": "Non-Bank Mortgage Lenders NZ: Who They Suit | Finch",
    ">Non-Bank Lenders</h1>": ">Non-Bank Mortgage Lenders in NZ</h1>",
    "Specialist Lenders in NZ | Finch Mortgage": "Specialist Mortgage Lenders in NZ | Finch Mortgages",
    ">Specialist Lenders</h1>": ">Specialist Mortgage Lenders in NZ</h1>",
    "Credit Unions & Customer-Owned in NZ | Finch Mortgage": "Credit Union Home Loans in NZ | Finch Mortgages",
    ">Credit Unions & Customer-Owned</h1>": ">Credit Union Home Loans in NZ</h1>",
    "Property Loans Home Loan <em": "Property Loans <em",
    "Home Loans Home Loan <em": "Home Loans <em",
}


def fix_headings(rel, html):
    """Location-service H1s were bare labels ("Refinance / Auckland."); lender hubs had internal tier names."""
    if rel.startswith("locations/"):
        html = CITY_H1.sub(lambda m: f"<h1>{CITY_H1_NAMES[m.group(1)]}<br/>{m.group(2)}{m.group(3)}</em></h1>", html)
    if rel.startswith("lenders/"):
        for old, new in LENDER_HUBS.items():
            # Titles end with the brand; never touch "Finch Mortgages".
            html = re.sub(re.escape(old) + r"(?!s)", lambda _m, n=new: n, html)
            html = re.sub(re.escape(old.replace("&", "&amp;")) + r"(?!s)", lambda _m, n=new: n, html)
    return html


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True,
                           check=True).stdout.splitlines()
    skip = ("node_modules/", "wordpress/", "output/", "scratch/", "docs/", "research/")
    by_page = {}
    for path, old, new in PAGES:
        by_page.setdefault(path, []).append((old, new))
    changed = 0
    for rel in files:
        path = ROOT / rel
        if rel.startswith(skip) or not path.exists():
            continue
        src = path.read_text(encoding="utf-8")
        out = src
        for old, new in SITEWIDE.items():
            out = out.replace(old, new)
        for old, new in by_page.get(rel, []):
            out = out.replace(old, new)
        out = add_calculators(drop_junk_labels(out))
        out = fix_headings(rel, out)
        if rel == "faq.html":
            out = rebuild_faq(out)
        if out != src:
            changed += 1
            if APPLY:
                path.write_text(out, encoding="utf-8")
    print(f"files changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
