"""
Comprehensive meta keywords updater for Finch Mortgage website.
Replaces all existing meta keywords with targeted, high-intent NZ mortgage keywords.
"""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Keyword map: relative path → comma-separated keywords ──────────────────
KEYWORDS = {

    # ── Homepage ───────────────────────────────────────────────────────────
    "index.html": (
        "mortgage broker NZ, NZ mortgage broker, best mortgage broker New Zealand, "
        "home loan broker NZ, Auckland mortgage broker, Wellington mortgage broker, "
        "Christchurch mortgage broker, independent mortgage broker NZ, "
        "compare NZ mortgage lenders, best home loan rates NZ 2026, "
        "mortgage pre-approval NZ, first home buyer NZ, refinance home loan NZ, "
        "investment property loan NZ, KiwiSaver first home, "
        "NZ home loan advice, $0 broker fee NZ, Finch Mortgage, Finch Mortgages NZ, "
        "Mukhtar Kiyani mortgage broker, free mortgage consultation NZ"
    ),

    # ── About ──────────────────────────────────────────────────────────────
    "about.html": (
        "about Finch Mortgage NZ, Finch Mortgages team, Mukhtar Kiyani mortgage broker, "
        "independent NZ mortgage broker, trusted mortgage advisor NZ, "
        "Auckland mortgage broker team, FSPR licensed mortgage broker, "
        "FSP registered mortgage adviser NZ, experienced mortgage broker NZ, "
        "NZ mortgage broker credentials, $0 broker fee NZ, "
        "500 clients mortgage NZ, 2 billion loans settled NZ, Finch Mortgages history"
    ),

    # ── Contact ────────────────────────────────────────────────────────────
    "contact.html": (
        "contact Finch Mortgage NZ, free mortgage consultation NZ, "
        "book mortgage appointment Auckland, NZ mortgage broker enquiry, "
        "Mukhtar Kiyani contact, mortgage advice Auckland, "
        "free home loan advice NZ, speak to mortgage broker NZ, "
        "NZ mortgage broker phone number, finchmortgages.co.nz contact"
    ),

    # ── FAQ ────────────────────────────────────────────────────────────────
    "faq.html": (
        "mortgage FAQ NZ, NZ mortgage questions, common mortgage questions NZ, "
        "how much deposit do I need NZ, KiwiSaver first home FAQ, "
        "NZ home loan pre-approval questions, how does mortgage work NZ, "
        "mortgage broker FAQ NZ, is mortgage broker free NZ, "
        "how long does mortgage approval take NZ, NZ first home buyer FAQ, "
        "NZ mortgage credit check, best time to fix mortgage NZ, DTI rules NZ"
    ),

    # ── Blog hub ───────────────────────────────────────────────────────────
    "blog.html": (
        "NZ mortgage blog, home loan news New Zealand, NZ mortgage tips 2026, "
        "mortgage advice NZ, NZ housing market news, NZ interest rate news 2026, "
        "first home buyer tips NZ, investment property NZ blog, "
        "OCR NZ news, NZ mortgage rate updates, Finch Mortgage blog, "
        "home buying guide NZ, NZ property market 2026"
    ),

    # ── Calculators hub ────────────────────────────────────────────────────
    "calculators.html": (
        "NZ mortgage calculators, home loan calculator NZ, "
        "mortgage repayment calculator NZ, borrowing power calculator NZ, "
        "refinance savings calculator NZ, extra repayment calculator NZ, "
        "free mortgage tools NZ, NZ property calculator, home loan tools NZ, "
        "how much can I borrow NZ calculator, mortgage payment estimator NZ"
    ),

    # ── Lenders hub ────────────────────────────────────────────────────────
    "lenders.html": (
        "NZ mortgage lenders, compare NZ home loan lenders, "
        "ANZ mortgage NZ, ASB home loan NZ, BNZ mortgage NZ, "
        "Westpac home loan NZ, Kiwibank mortgage NZ, TSB mortgage NZ, "
        "non-bank mortgage lender NZ, specialist lender NZ, credit union mortgage NZ, "
        "best mortgage lender NZ 2026, NZ bank vs non-bank mortgage, "
        "SBS Bank mortgage NZ, Heartland Bank mortgage NZ, Resimac NZ"
    ),

    # ── Services overview ──────────────────────────────────────────────────
    "services-overview.html": (
        "NZ mortgage broker services, home loan services NZ, "
        "mortgage services Auckland, first home buyer service NZ, "
        "refinance service NZ, investment property mortgage NZ, "
        "pre-approval service NZ, self-employed mortgage service NZ, "
        "construction loan service NZ, commercial property loan NZ, "
        "asset finance NZ, NZ mortgage services 2026, Finch Mortgage services"
    ),

    # ── Mortgage rates ─────────────────────────────────────────────────────
    "mortgage-rates.html": (
        "NZ mortgage rates 2026, current mortgage rates NZ, "
        "home loan interest rates NZ today, ANZ mortgage rates 2026, "
        "ASB mortgage rates 2026, BNZ mortgage rates 2026, "
        "Westpac home loan rates 2026, Kiwibank mortgage rates 2026, "
        "NZ fixed mortgage rates, NZ floating mortgage rates, OCR NZ 2026, "
        "RBNZ interest rate, NZ 1 year fixed rate, NZ 2 year fixed rate, "
        "compare mortgage rates NZ, best mortgage rate NZ, NZ rate tracker"
    ),

    # ── Refinance hub ──────────────────────────────────────────────────────
    "refinance.html": (
        "refinance home loan NZ, mortgage refinance NZ, switch mortgage NZ, "
        "remortgage NZ, refinance rates NZ 2026, lower mortgage rate NZ, "
        "refinance savings NZ, NZ mortgage switch 2026, "
        "break mortgage early NZ, refinance fixed rate NZ, "
        "refinance Auckland, refinance Wellington, Finch refinance NZ, "
        "home loan rollover NZ, best refinance rates New Zealand"
    ),

    # ── Market report ──────────────────────────────────────────────────────
    "market-report.html": (
        "NZ mortgage market report 2026, NZ housing market analysis, "
        "NZ interest rate outlook 2026, RBNZ OCR forecast NZ, "
        "NZ property market trends, Auckland housing market 2026, "
        "NZ mortgage rate forecast, NZ real estate market report, "
        "weekly mortgage market update NZ, Finch market analysis"
    ),

    # ── Weekly reports hub ─────────────────────────────────────────────────
    "weekly-reports.html": (
        "NZ mortgage weekly report, NZ interest rate weekly update, "
        "NZ housing market weekly, OCR weekly NZ, "
        "mortgage rate news NZ, NZ home loan news weekly, "
        "RBNZ weekly update, NZ property market weekly, Finch weekly report"
    ),

    # ── Testimonials hub ───────────────────────────────────────────────────
    "testimonials.html": (
        "Finch Mortgage reviews NZ, NZ mortgage broker testimonials, "
        "Finch Mortgages client feedback, best mortgage broker reviews NZ, "
        "Auckland mortgage broker reviews, trusted NZ mortgage broker, "
        "Mukhtar Kiyani reviews, 5 star mortgage broker NZ, "
        "home loan broker testimonials NZ"
    ),

    # ── Case studies hub ───────────────────────────────────────────────────
    "case-studies.html": (
        "Finch Mortgage case studies, NZ mortgage success stories, "
        "first home buyer success NZ, mortgage broker results NZ, "
        "refinance case study NZ, investment property case study NZ, "
        "self-employed mortgage approval NZ, NZ home loan case studies, "
        "construction loan case study NZ, debt consolidation NZ story"
    ),

    # ── Map ────────────────────────────────────────────────────────────────
    "map.html": (
        "Finch Mortgage Auckland office, mortgage broker Auckland location, "
        "Auckland CBD mortgage broker, Finch Mortgages address, "
        "NZ mortgage broker near me, home loan broker Auckland location"
    ),

    # ── Legal pages ────────────────────────────────────────────────────────
    "privacy.html": (
        "Finch Mortgage privacy policy NZ, NZ mortgage broker privacy"
    ),
    "terms.html": (
        "Finch Mortgage terms of service NZ, mortgage broker terms NZ"
    ),
    "disclosure.html": (
        "Finch Mortgage disclosure NZ, FSPR disclosure NZ, "
        "mortgage broker disclosure statement NZ, FSP1011206 NZ"
    ),
    "disclaimer.html": (
        "Finch Mortgage disclaimer NZ, mortgage advice disclaimer NZ"
    ),

    # ── Service pages ──────────────────────────────────────────────────────
    "services/home-loan.html": (
        "home loan NZ, NZ home loan 2026, best home loan rates NZ, "
        "mortgage broker home loan NZ, buy a home NZ, "
        "home loan interest rates NZ, NZ mortgage comparison, "
        "owner-occupier mortgage NZ, home purchase loan NZ, "
        "NZ home loan pre-approval, low interest home loan NZ, "
        "home loan Auckland, home loan Wellington, home loan Christchurch, "
        "best NZ mortgage lender, NZ home loan broker, 20 lenders NZ"
    ),

    "services/first-home-buyer.html": (
        "first home buyer NZ 2026, first home buyer mortgage NZ, "
        "KiwiSaver first home withdrawal NZ, First Home Grant NZ, "
        "Kainga Ora first home buyer, low deposit home loan NZ, "
        "5% deposit home loan NZ, 10% deposit home loan NZ, "
        "Welcome Home Loan NZ, first home buyer Auckland 2026, "
        "first home buyer Wellington, first home buyer Christchurch, "
        "first home buyer pre-approval NZ, KiwiSaver withdrawal mortgage NZ, "
        "first home buyer advice NZ, Finch first home buyer NZ"
    ),

    "services/refinance.html": (
        "refinance home loan NZ, mortgage refinance NZ, switch mortgage NZ, "
        "remortgage NZ, lower mortgage rate NZ, refinance rates NZ 2026, "
        "break mortgage early NZ, refinance fixed rate NZ, "
        "best refinance rates NZ, NZ mortgage switch, "
        "refinance Auckland, refinance Wellington, refinance savings NZ, "
        "home loan rollover NZ, refinance mortgage broker NZ, "
        "reduce mortgage repayments NZ, $340 per month savings refinance"
    ),

    "services/investment-property.html": (
        "investment property loan NZ, rental property mortgage NZ, "
        "NZ property investor loan 2026, investment mortgage broker NZ, "
        "interest only mortgage NZ, NZ DTI rules investor, "
        "rental property loan rates NZ, investment property Auckland, "
        "NZ LVR rules investor, portfolio property loan NZ, "
        "investor home loan NZ, property investment financing NZ, "
        "NZ rental property finance 2026, 40% deposit investor NZ, "
        "multi-property mortgage NZ, landlord loan NZ"
    ),

    "services/pre-approval.html": (
        "mortgage pre-approval NZ, home loan pre-approval NZ, "
        "NZ pre-approval mortgage 2026, conditional approval NZ mortgage, "
        "mortgage approval NZ, how to get pre-approved NZ, "
        "pre-approval Auckland, pre-approval Wellington, "
        "auction bidding pre-approval NZ, bidding at auction NZ pre-approval, "
        "mortgage pre-approval 24 hours NZ, NZ borrowing power assessment, "
        "home loan pre-approval online NZ, fast mortgage pre-approval NZ"
    ),

    "services/self-employed.html": (
        "self-employed mortgage NZ, self-employed home loan NZ, "
        "low doc mortgage NZ, alt doc mortgage NZ, "
        "self-employed home loan Auckland, NZ mortgage for self-employed, "
        "business owner home loan NZ, contractor mortgage NZ, "
        "self-employed income mortgage NZ, specialist lender NZ self-employed, "
        "low document loan NZ, sole trader mortgage NZ, "
        "self-employed low deposit home loan NZ, company director mortgage NZ, "
        "2 year tax return mortgage NZ, self-employed pre-approval NZ"
    ),

    "services/construction-loan.html": (
        "construction loan NZ, new build loan NZ, NZ construction mortgage 2026, "
        "progressive drawdown loan NZ, new build finance NZ, "
        "construction home loan NZ, build your own home NZ finance, "
        "new build mortgage 2026 NZ, construction loan Auckland, "
        "construction loan broker NZ, new build LVR exemption NZ, "
        "Kainga Ora new build NZ, turnkey loan NZ, "
        "house and land package loan NZ, NZ new build grant, builder mortgage NZ"
    ),

    "services/commercial-property.html": (
        "commercial property loan NZ, commercial mortgage NZ, "
        "commercial mortgage broker NZ, NZ commercial real estate finance, "
        "retail property loan NZ, industrial property loan NZ, "
        "office property finance NZ, commercial lending NZ, "
        "NZ commercial property investment, business property loan NZ, "
        "commercial property Auckland, commercial property Wellington, "
        "commercial mortgage advisor NZ, NZ commercial mortgage rates 2026"
    ),

    "services/asset-finance.html": (
        "asset finance NZ, vehicle finance NZ, equipment finance NZ, "
        "business asset loan NZ, NZ vehicle loan, "
        "commercial vehicle finance NZ, plant and equipment finance NZ, "
        "asset finance broker NZ, NZ business finance, "
        "hire purchase NZ, chattel mortgage NZ, "
        "asset financing New Zealand, machinery finance NZ, "
        "truck finance NZ, fleet finance NZ"
    ),

    "services/next-home-buyer.html": (
        "next home buyer NZ, upgrading home NZ mortgage, "
        "sell and buy home simultaneously NZ, moving home NZ mortgage, "
        "next home mortgage NZ 2026, upgrading property NZ, "
        "NZ bridging finance, sell existing home buy new NZ, "
        "next home buyer broker NZ, simultaneous property purchase NZ, "
        "upsizing home loan NZ, equity release upgrade NZ, "
        "NZ property ladder next step"
    ),

    # ── Calculator pages ───────────────────────────────────────────────────
    "calculators/mortgage-calculator.html": (
        "mortgage repayment calculator NZ, NZ mortgage calculator 2026, "
        "home loan repayment calculator, weekly mortgage repayment NZ, "
        "fortnightly mortgage repayment NZ, monthly mortgage payment NZ, "
        "mortgage payment calculator NZ, principal and interest calculator NZ, "
        "interest only calculator NZ, NZ mortgage payment estimator, "
        "free mortgage calculator NZ, online mortgage calculator NZ"
    ),

    "calculators/borrowing-power.html": (
        "borrowing power calculator NZ, how much can I borrow NZ, "
        "NZ home loan borrowing capacity 2026, mortgage affordability NZ, "
        "NZ borrowing limit calculator, income vs mortgage NZ, "
        "maximum home loan NZ, NZ lending criteria calculator, "
        "how much mortgage can I get NZ, DTI calculator NZ, "
        "NZ bank borrowing capacity, free borrowing calculator NZ"
    ),

    "calculators/refinance-savings.html": (
        "refinance savings calculator NZ, NZ mortgage refinance calculator, "
        "home loan switch savings NZ, should I refinance NZ, "
        "refinance comparison tool NZ, lower mortgage rate savings NZ, "
        "refinance break even calculator NZ, mortgage saving calculator NZ, "
        "switch home loan savings NZ, free refinance calculator NZ"
    ),

    "calculators/extra-repayment.html": (
        "extra mortgage repayment calculator NZ, pay off home loan faster NZ, "
        "NZ lump sum mortgage calculator, overpayment calculator NZ, "
        "extra mortgage payments NZ, reduce mortgage term NZ, "
        "save interest home loan NZ, early mortgage payoff calculator NZ, "
        "NZ mortgage overpayment savings, free extra repayment calculator NZ"
    ),

    # ── Guide pages ────────────────────────────────────────────────────────
    "guides/how-mortgage-works.html": (
        "how does a mortgage work NZ, NZ mortgage explained, "
        "what is a home loan NZ, mortgage structure NZ, "
        "fixed vs floating rate NZ, NZ loan to value ratio, LVR NZ, "
        "interest rate NZ mortgage, principal and interest NZ, "
        "mortgage term NZ, NZ home loan process explained, "
        "amortisation mortgage NZ, how to get a mortgage NZ, "
        "revert rate NZ, offset mortgage NZ, floating rate NZ"
    ),

    "guides/first-home-guide.html": (
        "first home buyer guide NZ 2026, how to buy first home NZ, "
        "NZ first home buying steps, KiwiSaver first home guide, "
        "First Home Grant NZ guide, NZ deposit requirements first home, "
        "Welcome Home Loan guide NZ, first home buyer checklist NZ, "
        "buying first home Auckland, NZ first home stamp duty, "
        "property purchase guide NZ, first home conveyancing NZ, "
        "building inspection NZ, LIM report NZ, settlement NZ home"
    ),

    "guides/refinance-guide.html": (
        "mortgage refinance guide NZ 2026, how to refinance home loan NZ, "
        "NZ refinance process, when to refinance NZ, "
        "mortgage break cost NZ, NZ refinance documents required, "
        "refinancing guide New Zealand, home loan switch guide NZ, "
        "mortgage rollover NZ, refinance timeline NZ, "
        "fixed rate break fee NZ, refinance vs refix NZ"
    ),

    "guides/step-by-step.html": (
        "NZ home buying process step by step, buying a house NZ steps 2026, "
        "how to buy a house NZ, NZ mortgage process step by step, "
        "property settlement NZ, NZ home loan steps, "
        "sale and purchase agreement NZ, NZ property buying guide, "
        "pre-approval to settlement NZ, NZ first home process, "
        "auction bidding NZ, conditional offer NZ, conveyancing NZ"
    ),

    # ── Lender pages ───────────────────────────────────────────────────────
    "lenders/major-banks.html": (
        "NZ major bank mortgages, ANZ mortgage NZ 2026, ASB mortgage NZ 2026, "
        "BNZ mortgage NZ 2026, Westpac mortgage NZ 2026, Kiwibank mortgage NZ 2026, "
        "TSB mortgage NZ, big bank home loan NZ, "
        "NZ bank home loan comparison, ANZ vs ASB vs BNZ, "
        "bank mortgage rates NZ, major bank lending criteria NZ"
    ),

    "lenders/non-bank-lenders.html": (
        "non-bank lender NZ, NZ non-bank mortgage 2026, Resimac NZ mortgage, "
        "Pepper Money NZ home loan, Liberty Financial NZ, Avanti Finance NZ, "
        "non-bank home loan NZ, alternative mortgage lender NZ, "
        "NZ specialist mortgage lender, non-bank vs bank mortgage NZ, "
        "non-bank lending criteria NZ, NZ alternative home loan"
    ),

    "lenders/credit-unions.html": (
        "NZ credit union mortgage, NZCU mortgage, credit union home loan NZ, "
        "NZ credit union lending, Nelson Building Society mortgage NZ, "
        "SBS Bank mortgage NZ, cooperative bank NZ mortgage, "
        "credit union vs bank mortgage NZ, NZ mutual bank home loan"
    ),

    "lenders/specialist-lenders.html": (
        "specialist mortgage lender NZ, NZ low doc lender, "
        "bad credit home loan NZ, non-conforming loan NZ, "
        "specialist home loan NZ, NZ high LVR lender, "
        "low deposit specialist lender NZ, unconventional mortgage NZ, "
        "NZ alternative lending 2026, second chance mortgage NZ, "
        "credit impaired home loan NZ"
    ),

    # ── Testimonials ───────────────────────────────────────────────────────
    "testimonials/reviews.html": (
        "Finch Mortgage reviews, Finch Mortgages client reviews, "
        "NZ mortgage broker reviews, Auckland mortgage broker testimonials, "
        "best mortgage broker reviews NZ, Mukhtar Kiyani reviews, "
        "Finch Mortgage 5 star, trusted NZ mortgage broker reviews, "
        "home loan broker testimonials NZ, independent mortgage broker review NZ"
    ),

    "testimonials/success-stories.html": (
        "Finch Mortgage success stories, NZ first home buyer success, "
        "mortgage approval success NZ, refinance success story NZ, "
        "home loan success NZ, Finch Mortgages results, "
        "NZ home buyer story 2026, Auckland property purchase story, "
        "investment property success NZ"
    ),

    # ── Blog posts ─────────────────────────────────────────────────────────
    "blog/25-year-old-home-buyer-case-study.html": (
        "young home buyer NZ, first home at 25 NZ, "
        "millennial home buyer NZ, young first home buyer mortgage NZ, "
        "KiwiSaver first home young NZ, first home buyer case study NZ, "
        "young person home loan NZ 2026"
    ),

    "blog/bad-credit-mortgage-nz.html": (
        "bad credit mortgage NZ, bad credit home loan NZ, "
        "poor credit score home loan NZ, credit impaired mortgage NZ, "
        "non-conforming home loan NZ, NZ mortgage bad credit history, "
        "defaults mortgage approval NZ, specialist lender bad credit NZ, "
        "credit repair mortgage NZ"
    ),

    "blog/best-time-to-fix-mortgage-nz.html": (
        "best time to fix mortgage NZ, fix mortgage rate NZ 2026, "
        "when to fix home loan NZ, fixed vs floating NZ 2026, "
        "NZ mortgage rate prediction, 1 year vs 2 year fixed NZ, "
        "lock mortgage rate NZ, NZ interest rate forecast 2026"
    ),

    "blog/current-mortgage-rates-nz-explained.html": (
        "current mortgage rates NZ explained, NZ mortgage rates explained 2026, "
        "how NZ mortgage rates work, NZ interest rate explained, "
        "OCR and mortgage rates NZ, NZ fixed rate vs floating explained, "
        "NZ bank mortgage rate comparison"
    ),

    "blog/deposit-needed-home-loan-nz.html": (
        "how much deposit for home loan NZ, NZ home loan deposit 2026, "
        "minimum deposit home loan NZ, 10% deposit NZ, 5% deposit NZ home loan, "
        "20% deposit NZ mortgage, NZ LVR deposit requirement, "
        "KiwiSaver deposit NZ, first home deposit NZ"
    ),

    "blog/deposit-requirements-nz.html": (
        "NZ mortgage deposit requirements, home loan deposit NZ 2026, "
        "deposit to buy house NZ, NZ LVR rules 2026, "
        "how much to save for house NZ, 20% deposit NZ rule, "
        "NZ home deposit guide, first home deposit requirements NZ"
    ),

    "blog/first-home-buyer-guide-nz.html": (
        "first home buyer guide NZ 2026, first home NZ buying tips, "
        "NZ first home checklist, KiwiSaver first home NZ, "
        "First Home Grant NZ 2026, first home buyer steps NZ, "
        "Welcome Home Loan NZ, NZ first home process"
    ),

    "blog/fixed-vs-floating-mortgage-nz.html": (
        "fixed vs floating mortgage NZ 2026, NZ fixed rate vs floating rate, "
        "should I fix my mortgage NZ, NZ floating mortgage rate 2026, "
        "fixed mortgage term NZ, split loan NZ, variable rate NZ mortgage, "
        "fixed rate benefits NZ, NZ mortgage rate strategy"
    ),

    "blog/how-much-can-i-borrow.html": (
        "how much can I borrow NZ, NZ mortgage borrowing capacity 2026, "
        "NZ home loan income multiples, DTI limit NZ 2026, "
        "borrowing power NZ calculator, NZ bank lending criteria, "
        "maximum home loan NZ, income needed for mortgage NZ"
    ),

    "blog/how-ocr-affects-mortgages-nz.html": (
        "how OCR affects mortgage NZ, RBNZ OCR and home loans NZ, "
        "OCR interest rates NZ 2026, OCR cut NZ mortgage impact, "
        "RBNZ rate decision NZ, NZ interest rate cut mortgage, "
        "OCR hold NZ 2026, NZ Reserve Bank mortgage"
    ),

    "blog/improve-credit-score-mortgage-nz.html": (
        "improve credit score for mortgage NZ, NZ credit score home loan, "
        "credit score NZ mortgage approval, fix credit score NZ, "
        "NZ Equifax credit score, NZ credit report mortgage, "
        "how to improve credit rating NZ, credit score needed for home loan NZ"
    ),

    "blog/interest-rates-guide.html": (
        "NZ mortgage interest rates guide 2026, understanding NZ interest rates, "
        "NZ home loan interest rate explained, NZ bank interest rates comparison, "
        "RBNZ interest rate guide NZ, fixed interest rate NZ guide, "
        "NZ mortgage rate history"
    ),

    "blog/kiwisaver-first-home-withdrawal.html": (
        "KiwiSaver first home withdrawal NZ, KiwiSaver home deposit NZ, "
        "withdraw KiwiSaver for house NZ, KiwiSaver first home eligibility NZ, "
        "KiwiSaver balance first home NZ, KiwiSaver and First Home Grant, "
        "how much KiwiSaver for first home NZ, KiwiSaver 3 year rule NZ"
    ),

    "blog/loan-declined-what-next-nz.html": (
        "mortgage declined NZ, home loan rejected NZ, "
        "what to do if mortgage declined NZ, loan declined NZ options, "
        "NZ bank declined mortgage, non-bank lender after declined NZ, "
        "improve mortgage application NZ, reapply mortgage NZ"
    ),

    "blog/missed-payments-mortgage-rejection.html": (
        "missed payments mortgage rejection NZ, NZ mortgage with missed payments, "
        "late payments home loan NZ, defaults mortgage NZ, "
        "NZ credit history home loan, mortgage application credit defaults NZ, "
        "NZ mortgage with bad payment history"
    ),

    "blog/mortgage-broker-auckland-city.html": (
        "mortgage broker Auckland city, Auckland CBD mortgage broker, "
        "home loan broker Auckland city, Auckland mortgage advisor, "
        "best mortgage broker Auckland CBD, Auckland city home loan, "
        "central Auckland mortgage broker, NZ mortgage broker Auckland"
    ),

    "blog/mortgage-broker-east-auckland.html": (
        "mortgage broker East Auckland, East Auckland home loan, "
        "Howick mortgage broker, Botany mortgage advisor, "
        "Pakuranga home loan broker, Flatbush mortgage broker NZ, "
        "East Auckland first home buyer, Manukau mortgage broker"
    ),

    "blog/mortgage-broker-north-shore.html": (
        "mortgage broker North Shore Auckland, North Shore home loan, "
        "Takapuna mortgage broker, Albany mortgage advisor, "
        "Glenfield home loan broker, Devonport mortgage NZ, "
        "North Shore first home buyer, Browns Bay mortgage broker"
    ),

    "blog/mortgage-broker-south-auckland.html": (
        "mortgage broker South Auckland, South Auckland home loan, "
        "Manukau mortgage broker, Papakura home loan broker, "
        "Pukekohe mortgage advisor, Otahuhu mortgage NZ, "
        "South Auckland first home buyer, Counties Manukau mortgage"
    ),

    "blog/mortgage-broker-west-auckland.html": (
        "mortgage broker West Auckland, West Auckland home loan, "
        "Henderson mortgage broker, Waitakere home loan broker, "
        "New Lynn mortgage advisor, Titirangi mortgage NZ, "
        "West Auckland first home buyer, Massey mortgage broker"
    ),

    "blog/mortgage-pre-approval-timeline.html": (
        "mortgage pre-approval timeline NZ, how long does pre-approval take NZ, "
        "NZ pre-approval process time, 24 hour pre-approval NZ, "
        "mortgage pre-approval steps NZ, conditional approval timeline NZ, "
        "how quickly can I get mortgage approval NZ, NZ pre-approval valid how long"
    ),

    "blog/mortgage-tips.html": (
        "NZ mortgage tips 2026, home loan tips New Zealand, "
        "save money on mortgage NZ, mortgage strategy NZ, "
        "NZ home loan hacks, reduce mortgage interest NZ, "
        "pay off mortgage faster NZ, NZ mortgage advice 2026"
    ),

    "blog/renting-to-owning-journey.html": (
        "renting to owning NZ, rent to buy house NZ, "
        "first home buyer from renting NZ, stop renting buy home NZ, "
        "NZ renter buying first home, Auckland renter to homeowner, "
        "NZ first home journey, KiwiSaver while renting NZ"
    ),

    "blog/self-employed-low-deposit-approval.html": (
        "self-employed low deposit mortgage NZ, self-employed home loan low deposit NZ, "
        "self-employed 10% deposit NZ, low doc low deposit NZ, "
        "business owner low deposit home loan NZ, self-employed mortgage approval NZ, "
        "alt doc low deposit NZ, specialist lender self-employed NZ"
    ),

    "blog/will-mortgage-rates-drop-nz-2026.html": (
        "will mortgage rates drop NZ 2026, NZ interest rate forecast 2026, "
        "OCR cut predictions NZ 2026, NZ mortgage rate outlook 2026, "
        "RBNZ rate predictions 2026, will home loan rates fall NZ, "
        "NZ housing market forecast 2026, best time to fix mortgage NZ 2026"
    ),

    # ── Case studies ───────────────────────────────────────────────────────
    "case-studies/first-home-approval.html": (
        "first home buyer approval NZ case study, first home mortgage case study, "
        "KiwiSaver first home success NZ, first home buyer story NZ, "
        "mortgage approval first home NZ, Finch first home case study"
    ),

    "case-studies/refinance-savings.html": (
        "refinance savings case study NZ, mortgage refinance success NZ, "
        "switch home loan savings NZ, refinance $340 per month NZ, "
        "NZ refinance real example, Finch refinance case study"
    ),

    "case-studies/self-employed-approval.html": (
        "self-employed mortgage approval NZ case study, "
        "low doc mortgage success NZ, business owner home loan NZ story, "
        "self-employed approved NZ, alt doc approval case study NZ"
    ),

    "case-studies/portfolio-growth.html": (
        "property portfolio mortgage NZ case study, "
        "investment property growth NZ, multi-property loan NZ, "
        "property investor success NZ, portfolio lending NZ case study"
    ),

    "case-studies/construction-loan-turnkey.html": (
        "construction loan case study NZ, new build loan NZ success, "
        "turnkey loan NZ, construction finance NZ example, "
        "build home NZ mortgage story, new build case study NZ"
    ),

    "case-studies/debt-consolidation.html": (
        "debt consolidation mortgage NZ case study, "
        "consolidate debt home loan NZ, NZ mortgage debt consolidation, "
        "wrap debt into mortgage NZ, lower repayments debt NZ"
    ),

    "case-studies/commercial-warehouse.html": (
        "commercial property loan NZ case study, "
        "warehouse purchase finance NZ, commercial mortgage success NZ, "
        "NZ industrial property loan story, Finch commercial case study"
    ),

    "case-studies/bridging-finance-lifestyle.html": (
        "bridging finance NZ case study, bridging loan NZ, "
        "sell before buy bridging NZ, simultaneous property purchase NZ, "
        "NZ bridge loan story, bridging finance lifestyle block NZ"
    ),

    "case-studies/asset-finance-machinery.html": (
        "asset finance NZ case study, machinery finance NZ, "
        "equipment loan NZ success, business asset loan NZ story, "
        "NZ chattel mortgage case study, Finch asset finance NZ"
    ),

    # ── Weekly reports ─────────────────────────────────────────────────────
    "weekly-reports/week-1-year-ahead-2026.html": (
        "NZ mortgage outlook 2026, NZ interest rate forecast 2026, "
        "OCR predictions NZ 2026, NZ property market 2026 outlook, "
        "RBNZ 2026 forecast, NZ home loan rates 2026 prediction"
    ),

    "weekly-reports/week-2-mortgage-stress-testing.html": (
        "NZ mortgage stress test 2026, NZ bank stress test home loan, "
        "mortgage serviceability NZ, RBNZ stress test NZ, "
        "mortgage test rate NZ, can I afford mortgage NZ"
    ),

    "weekly-reports/week-3-summer-sales-slump.html": (
        "NZ summer property market 2026, Auckland sales slump NZ, "
        "NZ real estate summer 2026, property listings NZ January 2026, "
        "NZ housing market update January 2026"
    ),

    "weekly-reports/week-4-dti-caps-bite.html": (
        "DTI caps NZ 2026, debt-to-income ratio NZ, "
        "NZ DTI limit home loan, RBNZ DTI rules 2026, "
        "debt-to-income mortgage NZ, DTI cap effect NZ"
    ),

    "weekly-reports/week-5-new-build-exemptions.html": (
        "new build LVR exemption NZ 2026, new build mortgage exemption NZ, "
        "NZ new build investor rules, new build exempt LVR NZ, "
        "new build exemption RBNZ, NZ new build incentive 2026"
    ),

    "weekly-reports/week-6-floating-vs-fixed.html": (
        "floating vs fixed mortgage NZ 2026, NZ fixed or floating 2026, "
        "floating rate NZ home loan, NZ revert rate floating, "
        "NZ interest rate strategy 2026, fix or float NZ"
    ),

    "weekly-reports/week-7-kiwisaver-tips.html": (
        "KiwiSaver tips NZ 2026, KiwiSaver first home NZ tips, "
        "maximise KiwiSaver NZ, KiwiSaver balance home deposit, "
        "KiwiSaver fund selection NZ, KiwiSaver first home strategy"
    ),

    "weekly-reports/week-8-interest-deductibility.html": (
        "interest deductibility NZ 2026, landlord interest deduction NZ, "
        "rental property interest deductible NZ, NZ investor tax 2026, "
        "interest deductibility restored NZ, property investor tax NZ"
    ),

    "weekly-reports/week-9-bay-of-plenty.html": (
        "Bay of Plenty property market 2026, Tauranga real estate 2026, "
        "Bay of Plenty home prices NZ, Tauranga mortgage broker, "
        "NZ regional property market Bay of Plenty, Rotorua property 2026"
    ),

    "weekly-reports/week-10-ocr-cut-march.html": (
        "OCR cut March 2026 NZ, RBNZ OCR cut NZ, "
        "NZ interest rate cut March 2026, mortgage rates after OCR cut NZ, "
        "RBNZ rate reduction NZ, NZ home loan rate cut 2026"
    ),

    "weekly-reports/week-11-first-home-grant.html": (
        "First Home Grant NZ 2026, Kainga Ora First Home Grant update, "
        "NZ first home grant changes, first home grant eligibility NZ, "
        "first home grant amount NZ, KiwiSaver grant NZ 2026"
    ),

    "weekly-reports/week-12-rental-yields.html": (
        "NZ rental yields 2026, Auckland rental yield, "
        "NZ investment property rental return 2026, NZ gross yield property, "
        "rental property investment NZ 2026, NZ landlord returns"
    ),

    "weekly-reports/week-13-canterbury-surge.html": (
        "Canterbury property market 2026, Christchurch real estate surge, "
        "NZ Canterbury housing market, Christchurch property prices 2026, "
        "Canterbury mortgage broker, South Island property market NZ"
    ),

    "weekly-reports/week-14-anz-rates.html": (
        "ANZ mortgage rates 2026, ANZ rate cut NZ, "
        "ANZ home loan rate change 2026, ANZ NZ mortgage update, "
        "ANZ fixed rate 2026, compare ANZ vs other banks NZ"
    ),

    "weekly-reports/week-15-ocr-hold.html": (
        "OCR hold NZ 2026, RBNZ OCR hold February 2026, "
        "NZ interest rate hold 2026, mortgage rates after OCR hold NZ, "
        "RBNZ decision April 2026, NZ home loan rate hold"
    ),

    "weekly-reports/week-16-major-banks-cut-rates.html": (
        "NZ banks cut mortgage rates 2026, ANZ ASB BNZ cut rates NZ, "
        "major banks lower home loan rates NZ, NZ rate cut banks April 2026, "
        "best mortgage rate NZ April 2026, NZ bank rate war 2026"
    ),

    "weekly-reports/week-17-autumn-update.html": (
        "NZ property market autumn 2026, NZ housing market April 2026, "
        "autumn real estate NZ 2026, NZ mortgage market update autumn, "
        "NZ property prices April 2026, NZ home sales autumn 2026"
    ),
}


def update_keywords(filepath, keywords):
    """Replace or insert meta keywords in an HTML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  SKIP (not found): {filepath}")
        return 0

    new_tag = f'<meta content="{keywords}" name="keywords"/>'

    # Replace existing keywords tag
    pattern = r'<meta\s+content="[^"]*"\s+name="keywords"[^/]*/>'
    if re.search(pattern, content):
        new_content = re.sub(pattern, new_tag, content)
    else:
        # Also try alternate attribute order
        pattern2 = r'<meta\s+name="keywords"\s+content="[^"]*"[^/]*/>'
        if re.search(pattern2, content):
            new_content = re.sub(pattern2, new_tag, content)
        else:
            # Insert before </head>
            new_content = content.replace("</head>", f"{new_tag}\n</head>", 1)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        kw_count = len([k.strip() for k in keywords.split(",") if k.strip()])
        print(f"  OK ({kw_count} kw): {filepath}")
        return kw_count
    else:
        print(f"  UNCHANGED: {filepath}")
        return 0


def main():
    total_keywords = 0
    pages_updated = 0

    print(f"\nUpdating meta keywords for {len(KEYWORDS)} pages...\n")

    for rel_path, keywords in KEYWORDS.items():
        abs_path = os.path.join(BASE, rel_path)
        count = update_keywords(abs_path, keywords)
        if count > 0:
            total_keywords += count
            pages_updated += 1

    print(f"\n{'='*60}")
    print(f"Pages updated : {pages_updated}")
    print(f"TOTAL KEYWORDS: {total_keywords}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
