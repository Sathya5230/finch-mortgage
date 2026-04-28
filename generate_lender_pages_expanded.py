#!/usr/bin/env python3
import os, textwrap

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"
OUT  = os.path.join(ROOT, "lenders")
os.makedirs(OUT, exist_ok=True)

NAV = """<header id="main-header">
  <div class="container" style="display:flex;align-items:center;justify-content:space-between;height:80px;">
    <a href="../index.html" class="nav-logo">Finch<span class="nav-logo-dot">.</span></a>
    <nav class="hidden md-flex items-center gap-6">
      <a href="../index.html" class="nav-link">Home</a>
      <div class="nav-item"><div class="dropdown-trigger nav-link">Services <i data-lucide="chevron-down" size="13"></i></div>
        <div class="mega-dropdown">
          <a href="../services/home-loan.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="home" size="18"></i></div><div><strong>Home Loan / Buy a Home</strong><span>Secure your dream home</span></div></a>
          <a href="../services/investment-property.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="building-2" size="18"></i></div><div><strong>Investment Property Loan</strong><span>Grow your portfolio</span></div></a>
          <a href="../services/refinance.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="refresh-cw" size="18"></i></div><div><strong>Refinance Mortgage</strong><span>Lower your rate &amp; save</span></div></a>
          <a href="../services/pre-approval.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="check-circle" size="18"></i></div><div><strong>Mortgage Pre-Approval</strong><span>Know your buying power</span></div></a>
          <a href="../services/first-home-buyer.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="key" size="18"></i></div><div><strong>First Home Buyer Mortgage</strong><span>Your first step</span></div></a>
          <a href="../services/next-home-buyer.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="compass" size="18"></i></div><div><strong>Next Home Buyer Mortgage</strong><span>Upgrade or move</span></div></a>
          <a href="../services/self-employed.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="briefcase" size="18"></i></div><div><strong>Self Employed Mortgage</strong><span>Flexible lending</span></div></a>
          <a href="../services/asset-finance.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="car" size="18"></i></div><div><strong>Asset Finance</strong><span>Vehicles &amp; Equipment</span></div></a>
          <a href="../services/commercial-property.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="store" size="18"></i></div><div><strong>Commercial Property Loan</strong><span>Commercial real estate</span></div></a>
          <a href="../services/construction-loan.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="hammer" size="18"></i></div><div><strong>Construction Loan</strong><span>Build from scratch</span></div></a>
        </div>
      </div>
      <div class="nav-item"><div class="dropdown-trigger nav-link">Calculators <i data-lucide="chevron-down" size="13"></i></div><div class="dropdown-menu"><a href="../calculators/mortgage-calculator.html" class="dropdown-item">Mortgage Calculator</a><a href="../calculators/borrowing-power.html" class="dropdown-item">Borrowing Power</a><a href="../calculators/refinance-savings.html" class="dropdown-item">Refinance Savings</a></div></div>
      <div class="nav-item"><div class="dropdown-trigger nav-link">Resources <i data-lucide="chevron-down" size="13"></i></div><div class="dropdown-menu" style="min-width:220px;"><div class="dropdown-label">Guides</div><a href="../guides/how-mortgage-works.html" class="dropdown-item">How Mortgage Works</a><a href="../guides/first-home-guide.html" class="dropdown-item">First Home Guide</a><div class="dropdown-divider"></div><div class="dropdown-label">Market</div><a href="../market-report.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#128202; Market Report</a><a href="../lenders.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#127976; Lenders</a><div class="dropdown-divider"></div><div class="dropdown-label">Stories</div><a href="../testimonials/reviews.html" class="dropdown-item">Client Reviews</a><a href="../testimonials/success-stories.html" class="dropdown-item">Success Stories</a><div class="dropdown-divider"></div><a href="../faq.html" class="dropdown-item">FAQ</a><a href="../blog.html" class="dropdown-item">Blog</a></div></div>
      <a href="../about.html" class="nav-link">About</a><a href="../contact.html" class="nav-link">Contact</a>
      <a href="../services/pre-approval.html" class="btn-nav-cta">Get Pre-Approved &#x2192;</a>
    </nav>
    <button id="mobile-menu-btn" class="md-hidden" style="background:none;border:1px solid rgba(181,206,176,0.5);padding:0.5rem 1rem;border-radius:0.5rem;cursor:pointer;display:flex;align-items:center;gap:0.5rem;"><i data-lucide="menu"></i><span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;">Menu</span></button>
  </div>
</header>
<div id="fullscreen-menu" style="display:none;position:fixed;inset:0;background:rgba(255,255,255,0.98);z-index:999;opacity:0;transition:opacity 0.3s ease;overflow-y:auto;padding-bottom:4rem;">
  <div class="container" style="display:flex;justify-content:flex-end;padding-top:1.5rem;">
    <button id="close-menu-btn" style="background:none;border:none;cursor:pointer;padding:0.5rem;display:flex;align-items:center;gap:0.5rem;"><span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;">Close</span><i data-lucide="x" size="24"></i></button>
  </div>
  <div class="container" style="display:flex;flex-direction:column;align-items:center;padding-top:2rem;gap:1.5rem;text-align:center;">
    <a href="../index.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Home</a>
    <div style="width:100%;max-width:300px;">
      <div class="mobile-dropdown-trigger" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:0.5rem;padding:0.5rem 0;">Services <i data-lucide="chevron-down" size="20"></i></div>
      <div class="mobile-dropdown-menu" style="display:none;flex-direction:column;gap:1rem;background:var(--finch-mist);padding:1.5rem;border-radius:1rem;margin-top:0.5rem;">
        <a href="../services/home-loan.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Home Loan</a>
        <a href="../services/first-home-buyer.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">First Home Buyer</a>
        <a href="../services/investment-property.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Investment Property</a>
        <a href="../services/refinance.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Refinance</a>
        <a href="../services/pre-approval.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Pre-Approval</a>
      </div>
    </div>
    <a href="../calculators.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Calculators</a>
    <a href="../lenders.html" style="font-size:1.5rem;font-weight:700;color:var(--finch-forest);text-decoration:none;">&#127976; Lenders</a>
    <a href="../about.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">About</a>
    <a href="../contact.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Contact</a>
    <a href="../services/pre-approval.html" class="btn-primary" style="margin-top:1rem;width:100%;max-width:300px;">Get Pre-Approved</a>
  </div>
</div>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="../index.html">Finch<span>.</span></a><p>New Zealand's trusted independent mortgage broker. Expert advice, 20+ lenders, fast approvals.</p></div>
      <div class="footer-col"><h4>Services</h4><a href="../services/home-loan.html">Home Loan</a><a href="../services/investment-property.html">Investment Property</a><a href="../services/refinance.html">Refinance</a><a href="../services/pre-approval.html">Pre-Approval</a><a href="../services/first-home-buyer.html">First Home Buyer</a><a href="../services/self-employed.html">Self Employed</a></div>
      <div class="footer-col"><h4>Resources</h4><a href="../market-report.html">Market Report</a><a href="../lenders.html">Lenders</a><a href="../guides/how-mortgage-works.html">How Mortgages Work</a><a href="../guides/first-home-guide.html">First Home Guide</a><a href="../faq.html">FAQ</a><a href="../blog.html">Blog</a></div>
      <div class="footer-col"><h4>Company</h4><a href="../about.html">About Us</a><a href="../contact.html">Contact</a><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a></div>
    </div>
    <div class="footer-bottom"><span>&#169; 2026 Finch Mortgages Limited. FSP1011206 | FSPR FSP1011125. All rights reserved.</span><div style="display:flex;gap:1.5rem;"><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a></div></div>
  </div>
</footer>"""

CATEGORIES = [
    {
        "file": "major-banks.html",
        "title": "Major Banks (Tier 1)",
        "badge": "Core Lending",
        "intro": "The cornerstone of New Zealand lending. Major banks offer the most competitive headline rates and cater perfectly to standard mortgage applications. Here is an expanded, brutally honest analysis of how each tier-one bank operates and their internal risk appetites.",
        "lenders": [
            {"initial": "A", "name": "ANZ", "desc": "As New Zealand's undisputed largest mortgage lender, ANZ commands an enormous share of the retail market. They leverage this immense capital base to consistently offer highly aggressive pricing on 1-year and 2-year fixed rates. Beyond raw interest rates, ANZ is particularly renowned for its incredibly strong property investor packages. They frequently lead the market in recognizing rental income efficiently, allowing investors to push their borrowing capacities further than smaller competitors. For first home buyers, ANZ's Blueprint to Build product offers aggressively discounted sub-market floating rates for new builds, completely shifting the mathematical feasibility of constructing versus buying existing homes. However, their strict automated credit scoring means that ANY historical defaulted payments (even minor telco bills) trigger extreme scrutiny, demanding an expert broker to mediate.", "url": "https://www.anz.co.nz/", "display_url": "www.anz.co.nz"},
            {"initial": "AS", "name": "ASB", "desc": "ASB is legendary in the broker sphere for maintaining arguably the most sophisticated and robust construction lending policies in the country. If you are undertaking a progressive drawdown build, ASB's dedicated construction teams offer unparalleled turn-around times and logistical flexibility that other banks simply cannot match. From an economic forecasting perspective, ASB frequently operates as the primary market aggressor; they are almost invariably the very first major bank to announce highly publicized rate cuts during a falling OCR cycle, forcing the rest of the syndicate to match them to prevent massive customer hemorrhage. They also possess an extremely strong appetite for rural and lifestyle blocks, frequently accepting slightly lower deposits for properties situated outside deeply urbanized zones compared to their immediate Tier 1 rivals.", "url": "https://www.asb.co.nz/", "display_url": "www.asb.co.nz"},
            {"initial": "B", "name": "BNZ", "desc": "The Bank of New Zealand fundamentally differentiates itself via its hyper-focus on structural flexibility and white-glove treatment for complex applicants. BNZ is the absolute gold standard for self-employed professionals, specialized medical practitioners, and SME business owners. Where other banks rigidly demand two full, unblemished years of finalized accountant-prepared financial statements, BNZ credit assessors frequently adopt a significantly more pragmatic, 'common-sense' approach, particularly if your business possesses strong forward-contracted revenue. Furthermore, they are one of the only major banks to offer entirely customizable 'TotalMoney' offset structures. This allows you to aggressively link up to 50 disparate family or business transaction accounts against a single floating mortgage facility, utilizing every single cent of dormant cash to violently suppress daily compounding interest charges without executing formal principal payments.", "url": "https://www.bnz.co.nz/", "display_url": "www.bnz.co.nz"},
            {"initial": "W", "name": "Westpac", "desc": "Westpac has heavily anchored its modern lending philosophy around environmental sustainability and aggressive green-financing. They consistently offer absolute zero-percent (interest-free) loans—currently up to $40,000 natively bolted onto your existing mortgage—exclusively utilized to fund warm, healthy home upgrades (like solar arrays, double glazing, and heat pumps) or the purchase of full Electric Vehicles (EVs). From a credit perspective, Westpac tends to adopt a highly favorable stance toward multi-generational lending. They are distinctly proactive in structuring parental guarantees and 'Springboard' family-link loans, actively recognizing the massive equity held by baby-boomer parents and deploying it surgically to bypass the crushing 20% deposit requirements for their children attempting to breach the first home threshold.", "url": "https://www.westpac.co.nz/", "display_url": "www.westpac.co.nz"},
            {"initial": "K", "name": "Kiwibank", "desc": "As the singular 100% locally owned retail bank within the Big Five, Kiwibank operates an entirely distinct Treasury model. Because their profits strictly remain localized within the New Zealand economy rather than hemorrhaging to Australian parent groups, Kiwibank frequently executes guerrilla-style market capture strategies. They are notorious for abruptly offering spectacular, short-term 'special' fixed rates that ruthlessly undercut the Australian giants, often coupled with some of the most aggressive cash-back switching contributions in the industry (frequently reaching 1% of total loan volume). Their primary weakness lies in somewhat elongated manual processing times during market peaks; however, an experienced broker leverages their VIP channels to bypass external queues, capturing their incredible domestic pricing without suffering the standard retail wait periods.", "url": "https://www.kiwibank.co.nz/", "display_url": "www.kiwibank.co.nz"}
        ],
        "faqs": [
            {"q": "How much deposit do I need for a major bank?", "a": "Under current RBNZ rules, banks generally require a 20% deposit for an owner-occupied existing home, though they can lend to a small proportion of borrowers with as little as 5-10%. For new builds, 10% is usually sufficient. Investors typically need 35%."},
            {"q": "Are major bank rates negotiable?", "a": "Yes. While the advertised 'special' rate is often the baseline, Finch advisors frequently negotiate unadvertised discounts (5-15bps) or superior cash contributions for strong applications."},
            {"q": "What happens if a major bank declines me?", "a": "A decline from one major bank does not mean a decline from all. Banks have different risk appetites. If all major banks decline, we pivot to a non-bank lender structured to suit your profile."}
        ]
    },
    {
        "file": "non-bank-lenders.html",
        "title": "Non-Bank Lenders",
        "badge": "Flexible Lending",
        "intro": "Regulated financial institutions that offer mortgages but don't hold banking licenses or offer standard checking accounts. Non-banks are vital because they assess risk differently. They are ideal for self-employed individuals without 2 years of financials, borrowers with past credit issues, or property investors who have hit bank lending caps.",
        "lenders": [
            {"initial": "R", "name": "Resimac", "desc": "Resimac stands as an absolute titan within the Tier-2 alternative lending space. Their primary dominance is rooted in their incredibly sophisticated 'Alternative Documentation' (Alt-Doc) loan products. For countless self-employed contractors, freelancers, or sole traders, generating two contiguous years of pristine, finalized accountant financials is operationally impossible, especially in volatile post-pandemic economic cycles. Resimac fundamentally bypasses this requirement. Instead of demanding historical tax returns, their credit panels will frequently approve massive mortgages based purely on 6 months of live Business Bank Statements or a singular declaration from your accountant verifying current cashflow viability. This allows entrepreneurs to leverage their true, real-time economic power to secure prime residential property long before high-street retail banks are willing to even open their file.", "url": "https://www.resimac.co.nz/", "display_url": "www.resimac.co.nz"},
            {"initial": "B", "name": "Bluestone", "desc": "Bluestone executes a highly surgical, clear-cut mandate within the lending ecosystem: rehabilitating chemically complex or damaged credit profiles. When a pristine applicant misses a few telecommunications payments, or suffers a minor, localized default due to a sudden medical emergency or brutal divorce, retail banks will frequently trigger an automated instant-decline algorithm, entirely unconcerned with the human context. Bluestone operates exclusively on human context. Their credit assessors ruthlessly discard the automated 'score' in favor of understanding the narrative. If the default is historically isolated and your current income is highly robust, Bluestone will issue immediate capital. We routinely utilize Bluestone as a highly strategic, 12-to-18-month 'parking facility', securing the home immediately while the credit file organically heals, before executing a rapid refinance back to a prime tier-one bank.", "url": "https://www.bluestone.net.nz/", "display_url": "www.bluestone.net.nz"},
            {"initial": "P", "name": "Pepper Money", "desc": "Pepper Money provides an incredibly refreshing, 'common-sense' lending approach designed explicitly to capture prime and near-prime borrowers who have been unfairly marginalized by the brutal rigidity of modern CCCFA (Credit Contracts and Consumer Finance Act) regulations. Over the past few years, countless high-income Kiwi families were declined mortgages simply because they spent money at Kmart or bought coffees too frequently, failing the bank's automated 'uncommitted monthly income' stress tests. Pepper Money aggressively strips away this micro-management. They assess applications on their overarching, fundamental merits. If you possess massive equity, a fundamentally strong salary, and exhibit sensible overarching financial control, Pepper Money will green-light the mortgage. They are the ultimate antidote to the algorithmic tyranny deployed by major retail corporations.", "url": "https://www.peppermoney.co.nz/", "display_url": "www.peppermoney.co.nz"},
            {"initial": "L", "name": "Liberty", "desc": "Liberty Financial is objectively one of the most versatile and highly hybridized lending institutions operating in Australasia. While other non-banks specialize aggressively in a single narrow niche (like credit repair), Liberty casts a phenomenally wide net. They actively issue prime residential mortgages that mathematically rival tier-one banks in cost, but simultaneously possess heavily specialized divisions granting custom loans for wildly unconventional properties. If you are attempting to purchase a uniquely constructed geodesic dome in an extreme rural zone, a multi-key dwelling that retail banks flag as 'commercial', or a property requiring immediate, chaotic remediation work before it can even secure basic hazard insurance, Liberty's bespoke risk-assessment panels are fundamentally structured to underwrite and fund these fringe scenarios securely and effectively.", "url": "https://www.liberty.co.nz/", "display_url": "www.liberty.co.nz"}
        ],
        "faqs": [
            {"q": "Are non-bank lenders safe?", "a": "Absolutely. While they aren't registered banks, they are heavily regulated by the Financial Markets Authority (FMA) and must adhere to the Credit Contracts and Consumer Finance Act (CCCFA). Since you owe them money (not the other way around), your risk is minimal."},
            {"q": "Are non-bank rates much higher than major banks?", "a": "It depends on the product. Some 'prime' non-bank products offer rates identical to or even lower than major banks. 'Specialist' products for credit impairment naturally carry a risk premium, often 1-3% higher than bank specials."},
            {"q": "Can I refinance from a non-bank to a major bank later?", "a": "Yes, this is a very common strategy. We often use a non-bank lender as a 12-24 month stepping stone (e.g., while waiting for a credit mark to clear or 2 years of business financials to accrue), and then refinance you to a lower major bank rate when eligible."}
        ]
    },
    {
        "file": "specialist-lenders.html",
        "title": "Specialist Lenders",
        "badge": "Niche Solutions",
        "intro": "Specialist lenders fill the gaps where traditional lending falls short. They focus heavily on the quality of the property asset rather than purely relying on borrower income. These lenders are essential for short-term bridging finance, rapid property flips, developing bare land, or complex commercial-residential overlaps.",
        "lenders": [
            {"initial": "A", "name": "Avanti Finance", "desc": "Avanti Finance is an incredibly potent, profoundly agile New Zealand-based lender specializing in executing transactions that inherently require ferocious speed and total flexibility. When securing a major retail bank mortgage takes an agonizing 15 working days of bureaucratic ping-pong, Avanti can routinely structure, underwrite, and issue formal unconditional lending contracts within a staggering 48-hour window. This blinding speed is strictly reserved for the deployment of advanced bridging finance (allowing you to impulsively buy an auction property before selling your current home) or intensely aggressive property speculation and flipping. Avanti fundamentally focuses their risk assessment upon the underlying physical asset value rather than torturing the applicant's historical PAYE income streams. If the property's mathematical equity stack works, Avanti will fund the deal.", "url": "https://www.avantifinance.co.nz/", "display_url": "www.avantifinance.co.nz"},
            {"initial": "B", "name": "Basecorp Finance", "desc": "Basecorp operates exclusively within the realm of high-velocity, short-to-medium-term property-backed lending. They are the absolute weapon of choice for highly sophisticated property investor syndicates, developers tackling complex sub-divisions, or individuals trapped in sudden, terrifying settlement failures. If an individual is legally bound to settle a multi-million-dollar property tomorrow, but their primary bank inexplicably withdraws funding at the eleventh hour, Basecorp possesses the private capital reserves and flat management hierarchy to step in, evaluate the asset's raw registered valuation, and aggressively front the capital required to prevent the client from suffering catastrophic default penalties. Their interest rates reflect this extreme, immediate access to capital, but their utility in saving unanchored deals is undeniably unparalleled in the New Zealand ecosystem.", "url": "https://www.basecorp.co.nz/", "display_url": "www.basecorp.co.nz"},
            {"initial": "P", "name": "Prospa", "desc": "While Prospa is deeply and intrinsically renowned throughout Australasia as an elite provider of unsecured Small-to-Medium Enterprise (SME) business lending, they offer vital, highly integrated commercial financing mechanics that heavily overlap with massive personal property portfolios. Frequently, elite self-employed borrowers discover that their personal residential borrowing capacity is artificially crippled because they cannot organically extract cash from their business without triggering massive, highly punitive corporate tax events. Prospa solves this by rapidly injecting high-volume commercial capital straight into the business's operational core. This entirely frees up the director's personal capital reserves, allowing them to independently formulate deposits for residential holdings. Utilizing Prospa requires highly sophisticated, macro-level structuring that flawlessly balances aggressive commercial debt against safe, low-interest residential lending.", "url": "https://www.prospa.co.nz/", "display_url": "www.prospa.co.nz"}
        ],
        "faqs": [
            {"q": "What is bridging finance?", "a": "Bridging finance is a short-term loan used to cover the gap when buying a new property before your existing property has sold. Specialist lenders are often much more accommodating with bridging loans than major banks."},
            {"q": "How fast can a specialist lender approve a loan?", "a": "Because they don't rely heavily on automated scoring and have flatter management structures, some specialist lenders can grant conditional approval within 24-48 hours if the property asset is strong."},
            {"q": "Do I need proof of income for specialist lenders?", "a": "While you must still demonstrate borrowing capacity under the CCCFA, specialist lenders offer 'asset-lend' or 'low-doc' products. This means if you have substantial equity in a property, the income verification requirements are significantly lower."}
        ]
    },
    {
        "file": "credit-unions.html",
        "title": "Credit Unions",
        "badge": "Community Focused",
        "intro": "Unlike major banks which must maximize profits for external shareholders, Credit Unions are 100% owned by their members (customers). They reinvest their profits to offer competitive rates and lower fees. They offer a highly personalized, human approach to underwriting—ideal for borrowers who fall slightly outside the strict algorithms of large banks.",
        "lenders": [
            {"initial": "U", "name": "Unity (formerly NZCU)", "desc": "The organization formerly operating as the New Zealand Credit Union (now comprehensively rebranded as Unity) represents arguably the most formidable, wide-reaching member-owned financial institution currently battling in the domestic mortgage market. Unity completely subverts the traditional, hyper-capitalist banking model. Because they harbor absolutely zero legal or moral obligation to harvest billions in dividends for foreign shareholders across the Tasman, Unity systematically reinvests nearly the entirety of its annual operating surplus directly back into aggressively subsidizing its member rate offerings. Consequently, they frequently deploy 2-year and 3-year fixed mortgage rates that noticeably undercut the heavily publicized 'specials' launched by the Big Four banks. Furthermore, Unity refuses to brutalize applicants with the myriad of opaque application, establishment, and monthly account-keeping fees that plague tier-one lending, offering a genuinely transparent, deeply ethical alternative for First Home Buyers.", "url": "https://unitymoney.co.nz/", "display_url": "www.unitymoney.co.nz"},
            {"initial": "F", "name": "First Credit Union", "desc": "Holding the distinguished title of New Zealand's absolute largest organically unified credit union, First Credit Union operates with a fiercely guarded independence. They execute intensely straightforward, radically simplified mortgage products meticulously designed to entirely strip away the confusing corporate engineering endemic to major retail banks. Where a tier-one bank might subject a mathematically sound applicant to weeks of automated stress-test algorithms and impersonal, overseas call-center bureaucracy, First Credit Union maintains localized, fiercely human credit panels. Their lending managers are heavily entrenched within their local communities. They physically review your localized circumstances, analyze your holistic, decade-long savings character, and happily approve 'common-sense' loans that standard institutional algorithms incorrectly flag as high-risk, making them an indispensable ally for slightly complex blue-collar regional borrowers.", "url": "https://www.firstcreditunion.co.nz/", "display_url": "www.firstcreditunion.co.nz"},
            {"initial": "P", "name": "Police Credit Union", "desc": "The Police Credit Union is an incredibly specialized, structurally closed-loop community lender offering utterly exceptional, highly exclusive rates dedicated strictly to active members of the New Zealand Police Force and their immediate localized families. Because police officers universally boast unassailable job security—effectively backed by the sovereign stability of the New Zealand Government—and represent the absolute lowest conceivable statistical risk of catastrophic loan default, this internal credit union can offer aggressively slashed wholesale interest rates. They also offer highly specialized shift-worker income assessments, heavily factoring in complex, fluctuating overtime rosters and danger-pay allowances that standard civilian banks routinely miscalculate or aggressively discount. If an applicant has any familial tie to the force, unlocking access to this hyper-exclusive syndicate is an absolute, undeniable mathematical priority.", "url": "https://www.policecu.org.nz/", "display_url": "www.policecu.org.nz"}
        ],
        "faqs": [
            {"q": "Do I have to belong to a specific group to join a Credit Union?", "a": "Some are restricted by profession (like the Police Credit Union), but many broad credit unions (like Unity or First Credit Union) are open to the general public. We manage the eligibility checking for you."},
            {"q": "Are their mortgage rates better than major banks?", "a": "Often, yes. Because they do not have to pay large dividends to external shareholders, Credit Unions can frequently undercut major bank fixed rates by 10-20 basis points, and they heavily discount or waive loan application fees."},
            {"q": "Is the application process different?", "a": "It's more human. Credit union lending managers often look at your overall character, savings history, and localized circumstances rather than just running an automated credit score. This makes them fantastic for borrowers needing a 'common sense' review."}
        ]
    }
]

def make_page(c):
    # Build lender cards
    lender_cards = ""
    for l in c["lenders"]:
        lender_cards += f"""
        <div style="background:white;border:1px solid rgba(181,206,176,0.4);border-radius:1rem;padding:2rem;display:flex;flex-direction:column;gap:1.25rem;">
          <div style="width:64px;height:64px;background:var(--finch-mist);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--finch-forest);font-weight:800;font-size:1.5rem;border:1px solid rgba(181,206,176,0.5);">{l['initial']}</div>
          <h3 style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);">{l['name']}</h3>
          <p style="font-size:1rem;color:var(--neutral-medGray);line-height:1.75;flex-grow:1;">{l['desc']}</p>
          <div style="font-size:0.95rem;font-weight:700;color:var(--finch-forest);display:inline-flex;align-items:center;gap:0.4rem;margin-top:0.5rem;word-break:break-all;">{l['display_url']}</div>
        </div>"""
    
    # Build FAQs
    faq_html = ""
    for idx, f in enumerate(c["faqs"]):
        border = 'border-bottom:1px solid rgba(181,206,176,0.4);' if idx < len(c["faqs"])-1 else ''
        faq_html += f"""
        <div style="{border}">
          <button onclick="toggleFaq(this)" style="width:100%;text-align:left;background:none;border:none;padding:1.5rem 0;display:flex;align-items:center;justify-content:space-between;cursor:pointer;gap:1rem;">
            <span style="font-size:1rem;font-weight:700;color:var(--neutral-black);line-height:1.4;">{f['q']}</span>
            <span class="faq-icon" style="color:var(--finch-forest);flex-shrink:0;font-size:1.25rem;font-weight:300;transition:transform 0.3s;">+</span>
          </button>
          <div class="faq-body" style="display:none;padding-bottom:1.5rem;">
            <p style="color:var(--neutral-medGray);line-height:1.75;">{f['a']}</p>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c['title']} in NZ | Finch Mortgage</title>
  <meta name="description" content="Detailed guide to {c['title']} in New Zealand. Compare partners, understand policies, and find out if this lender type matches your mortgage needs.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
{NAV}
<main style="padding-top:80px;">

  <!-- Hero Start -->
  <section style="background:var(--finch-forest);padding:4rem 0 5rem;position:relative;overflow:hidden;">
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 50%,rgba(181,206,176,0.15) 0%,transparent 65%);pointer-events:none;"></div>
    <div class="container">
      <nav class="breadcrumb" style="margin-bottom:1.5rem;">
        <a href="../index.html" style="color:rgba(255,255,255,0.65);">Home</a>
        <span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span>
        <a href="../lenders.html" style="color:rgba(255,255,255,0.65);">Lenders Hub</a>
        <span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span>
        <span style="color:white;">{c['title']}</span>
      </nav>
      <div style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);color:var(--finch-sage);border-radius:999px;padding:0.25rem 0.9rem;font-size:0.65rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.25rem;border:1px solid rgba(181,206,176,0.3);">{c['badge']}</div>
      <h1 style="color:white;font-family:var(--font-display);font-size:clamp(2rem,4vw,3.2rem);font-weight:700;line-height:1.15;margin-bottom:1.25rem;max-width:780px;">{c['title']}</h1>
      <p style="color:rgba(255,255,255,0.8);max-width:680px;line-height:1.75;font-size:1.05rem;">{c['intro']}</p>
    </div>
  </section>

  <!-- Lenders Grid -->
  <section style="padding:5rem 0;background:var(--finch-mist);">
    <div class="container">
      <div class="section-label"><span>Our Partners</span></div>
      <h2 class="section-heading" style="margin-top:0.75rem;margin-bottom:2.5rem;">Finch's {c['title']}<br><em>Network.</em></h2>
      <div style="display:grid;grid-template-columns:1fr;gap:2.5rem;max-width:900px;margin:0 auto;">
        {lender_cards}
      </div>
    </div>
  </section>

  <!-- FAQs -->
  <section style="padding:5rem 0;background:white;">
    <div class="container">
      <div style="max-width:820px;margin:0 auto;">
        <div class="section-label"><span>FAQs</span></div>
        <h2 class="section-heading" style="margin-top:0.75rem;margin-bottom:2.5rem;">Questions About<br><em>{c['title']}</em></h2>
        <div style="display:flex;flex-direction:column;gap:0;">
          {faq_html}
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section style="padding:5rem 0;background:var(--finch-forest);text-align:center;">
    <div class="container">
      <div style="max-width:600px;margin:0 auto;">
        <h2 style="color:white;font-size:clamp(1.75rem,3.5vw,2.5rem);font-weight:700;margin-bottom:1rem;">Match with the perfect lender today.</h2>
        <p style="color:rgba(255,255,255,0.75);line-height:1.75;margin-bottom:2rem;">Speak to an advisor. We'll assess your situation and recommend exactly which lenders will approve your loan at the best terms.</p>
        <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
          <a href="../services/pre-approval.html" class="btn-primary" style="background:white;color:var(--finch-forest);">Get Pre-Approved →</a>
          <a href="../contact.html" class="btn-cta-outline">Contact Us</a>
        </div>
      </div>
    </div>
  </section>

</main>
{FOOTER}
<script src="../script.js"></script>
<script>
  if (typeof lucide !== 'undefined') lucide.createIcons();
  function toggleFaq(btn) {{
    const body = btn.nextElementSibling;
    const icon = btn.querySelector('.faq-icon');
    const isOpen = body.style.display === 'block';
    
    // Select siblings inside the parent container to close
    const allBodies = btn.closest('div').parentElement.querySelectorAll('.faq-body');
    const allIcons = btn.closest('div').parentElement.querySelectorAll('.faq-icon');
    
    allBodies.forEach(b => b.style.display = 'none');
    allIcons.forEach(i => {{ i.textContent = '+'; i.style.transform = 'rotate(0deg)'; }});
    
    if (!isOpen) {{
      body.style.display = 'block';
      icon.textContent = '−';
      icon.style.transform = 'rotate(180deg)';
    }}
  }}
</script>
</body>
</html>"""

for c in CATEGORIES:
    path = os.path.join(OUT, c["file"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(make_page(c))
    print(f"  CREATED: lenders/{c['file']}")

print("Done generating 4 category pages.")
