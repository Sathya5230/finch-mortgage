"""Generate new NZ case studies with diverse client scenarios.

Reuses the head + footer wrappers from an existing case study to keep
nav, styles, and breadcrumb structure consistent.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "case-studies/refinance-savings.html"
OUT_DIR = ROOT / "case-studies"
BASE_URL = "https://www.finchmortgages.co.nz"

# ISO 8601 dates for Article rich-result eligibility
ARTICLE_PUBLISHED = "2026-01-15"
ARTICLE_MODIFIED = "2026-07-04"

# Slugs to (re)generate when run directly. Keep this scoped to newly added
# entries plus the 4 known-broken ones (duplicated Article/FAQPage schema from
# a prior bug in build_page()) -- a full re-run would blow away hand edits on
# the other, already-clean existing case studies.
NEW_SLUGS = {
    "loan-declined-second-opinion",
    "bad-credit-defaults-approved",
    "contractor-fixed-term-income",
    "gifted-deposit-no-savings",
    "trust-structure-investment-purchase",
    "lifestyle-block-rural-purchase",
    "new-job-probation-period-approval",
    "non-bank-to-bank-refinance-credit-repair",
    "leaky-home-remediation-finance",
    "returning-kiwi-overseas-income",
    "buy-out-ex-partner-separation",
    "redundancy-income-recovery-approval",
    "second-home-holiday-home-purchase",
    "mortgagee-sale-purchase-finance",
    "high-dti-young-professional-approved",
    # Pre-existing pages with duplicated schema from the old build_page() bug:
    "new-migrant-first-mortgage",
    "single-parent-rebuilds",
    "apartment-investor-scaling",
    "family-guarantee-first-home",
}


CASE_STUDIES = [
    {
        "slug": "new-migrant-first-mortgage",
        "tag": "Migrant Buyer — Case Study",
        "title_short": "New Migrant Buys First Auckland Home",
        "h1_top": "New Zealand Migrant Buys",
        "h1_bottom": "Their First Auckland Home in 14 Months.",
        "summary": "A UK-trained engineer who moved to Auckland 14 months earlier had no NZ credit history but strong income. Finch found a lender comfortable with short residency.",
        "stats": [
            ("14 mo", "NZ Residency"),
            ("$120K", "Salary"),
            ("12%", "Deposit"),
            ("$780K", "Property"),
            ("21 days", "To Pre-Approval"),
        ],
        "situation": [
            "Daniel moved to Auckland from the UK in early 2025 on a Skilled Migrant pathway, working as a senior engineer for an Auckland infrastructure firm. By April 2026 he'd been in NZ 14 months on a permanent role with a clean local employment record. He had saved roughly $95,000 for a deposit (held partly in KiwiSaver from contributions during his first 12 months, partly in his personal savings account).",
            "When Daniel approached his own bank, they declined his application. Their stated reason: insufficient NZ credit history. He had no defaults, no missed payments, and a strong UK credit history — but the bank's automated scorecard required at least 2 years of NZ credit file activity before recommending approval. Daniel was frustrated and almost gave up on buying for another year.",
            "He reached Finch after a colleague mentioned that brokers can access lenders with more flexible migrant policies. We assessed his full position and confirmed several main banks (plus a strong non-bank option) would absolutely consider his application — the trick was selecting the right lender and presenting the file in the way each lender's credit team prefers.",
        ],
        "approach": [
            ("Migrant-friendly lender selection", "We identified three NZ lenders whose current scorecard treats Skilled Migrant residents favourably when they hold a permanent role and clean employment record — and one specialist non-bank as a back-up. Each had different documentation expectations for international applicants."),
            ("Cross-border income evidence", "We compiled Daniel's UK-employer reference letter, NZ employment contract, 6 months of NZ payslips, NZ IRD tax assessment, plus a UK credit reference report to demonstrate his repayment history overseas. This addressed every reasonable lender concern up front."),
            ("LVR-band optimisation", "With his $95K deposit plus KiwiSaver of $11K (after 12 months of contributions) at a $780,000 price point, his LVR sat at 86% — above the standard 80% main-bank threshold. We selected a lender whose Low Equity Premium pricing was sharpest for the 80-90% LVR band, saving ~0.35% versus other lenders' premiums."),
            ("Pre-approval before competing", "We secured the pre-approval before Daniel made his auction bid, giving him certainty on his upper limit and the confidence to bid against established Kiwi buyers without finance conditions."),
        ],
        "outcome": [
            "Daniel's pre-approval was issued within 21 days of full document submission, against an initial main-bank decline. He attended his second auction with a $780,000 ceiling and secured a 4-bedroom Papakura family home for $762,000 — under his ceiling and with $18,000 of his approved capacity unused.",
            "Settlement occurred 5 weeks after the auction, on time. Daniel's first NZ mortgage was structured as a 50/50 split between a 2-year fixed at 5.79% and a floating portion he plans to attack with extra repayments from his bonus and tax refund each year. Total cost to Daniel: $0 — the lender paid Finch on settlement.",
            "His feedback: \"My own bank told me I'd have to wait another year. Finch found me a lender comfortable with my situation and structured the loan in a way I'd never have known to ask for. The whole process was 6 weeks from first conversation to keys.\"",
        ],
    },
    {
        "slug": "single-parent-rebuilds",
        "tag": "Single Parent — Case Study",
        "title_short": "Single Parent Rebuilds After Divorce",
        "h1_top": "Single Parent",
        "h1_bottom": "Buys Back Into Wellington Post-Divorce.",
        "summary": "A Wellington physiotherapist with two children sold the family home in divorce settlement. Finch helped her re-enter the market on a single income.",
        "stats": [
            ("$95K", "Annual Income"),
            ("12%", "Deposit"),
            ("$680K", "Property"),
            ("17 days", "Pre-Approval"),
            ("0", "Compromises"),
        ],
        "situation": [
            "Rebecca is a 37-year-old senior physiotherapist working for a Wellington DHB. Following a divorce in late 2025, the family home in Karori was sold and the proceeds split — leaving Rebecca with $82,000 deposit savings plus her KiwiSaver balance of $26,000. She wanted to buy back into Wellington as quickly as possible to maintain stability for her two primary-school children.",
            "The challenges were significant: her income at $95,000 had to service a Wellington-priced mortgage on a single income; she'd been declared as a co-borrower on the prior mortgage, so her credit file showed the historic loan; and as the children's primary caregiver, she received Working for Families tax credits which her own bank refused to count toward serviceability.",
            "When she approached the bank she'd held the original mortgage with, they offered her borrowing capacity of just $480,000 — well short of what Wellington's market required even for a modest 3-bedroom home. She was advised to consider renting for 2-3 years before reapplying. Rebecca reached out to Finch as a second opinion before accepting that recommendation.",
        ],
        "approach": [
            ("Working for Families income inclusion", "Multiple NZ lenders accept Working for Families and Best Start payments as income for serviceability, where it's evidenced by IRD statements and projected to continue. We presented Rebecca's case to lenders who count this income, which lifted her borrowing capacity by ~$80,000 immediately."),
            ("Clean credit file presentation", "We worked with her to obtain a current Centrix and Equifax credit report, confirming her credit file was clean despite the divorce. The historic mortgage was correctly recorded as paid out at settlement, not as a default."),
            ("Lender match for single-parent scenarios", "Three NZ main banks plus one specialist non-bank each treat single-parent applications differently. We selected the lender whose stress-test rate and living-expense floor combination produced the most generous outcome for Rebecca's specific circumstances."),
            ("KiwiSaver + savings deposit stack", "Rebecca's $82,000 personal savings + $26,000 KiwiSaver withdrawal (she'd held KiwiSaver 8+ years and had repaid her previous first home withdrawal during her marriage) combined to give her a 16% deposit on a $680,000 property — close to the standard 20% threshold with a manageable Low Equity Premium."),
        ],
        "outcome": [
            "Rebecca secured pre-approval of $570,000 — almost $90,000 above her own bank's offer — within 17 days of submission. She purchased a 3-bedroom townhouse in Newtown for $678,000 (close to school and her workplace), settling 6 weeks later.",
            "Her loan was structured as a 70/30 split: 70% on a 2-year fixed at 5.69%, 30% floating so she could attack the principal with annual tax refunds and bonus income. She also captured a $4,200 cashback contribution from the new lender, which fully covered her solicitor and moving costs.",
            "Rebecca's feedback: \"Three months earlier I was told I'd have to rent for years. Finch took my actual situation seriously instead of plugging me into a single bank's tick-box calculator. The kids are settled in our own home and life is moving forward again.\"",
        ],
    },
    {
        "slug": "apartment-investor-scaling",
        "tag": "Investor Scaling — Case Study",
        "title_short": "Apartment Investor Scales to 5 Properties",
        "h1_top": "Apartment Investor",
        "h1_bottom": "Scales From 1 Property to 5 in 18 Months.",
        "summary": "A Hamilton-based investor used equity recycling, new-build LVR exemption, and a multi-lender structure to grow a portfolio of 5 income properties.",
        "stats": [
            ("1 → 5", "Properties"),
            ("18 mo", "Timeframe"),
            ("$2.1M", "Portfolio Value"),
            ("3 lenders", "Diversified"),
            ("$0", "Fresh Cash"),
        ],
        "situation": [
            "James, a 41-year-old Hamilton engineer earning $145,000, owned a single investment property valued at $620,000 with a $310,000 mortgage. He had a clear goal: grow to 5 income properties within 2 years to support semi-retirement by age 50. His own bank told him he could potentially add one more property — but no more — using the equity in his existing property.",
            "His existing bank's serviceability calculation treated rental income at 70% shading and applied their high test rate to both his existing and any new debt. The combined assessment showed he'd reach his investor LVR cap quickly. James felt stuck — the path to 5 properties seemed mathematically impossible without significant cash injection.",
            "James met Finch through a referral from his accountant. We modelled his portfolio across the full NZ lender panel, including specialist non-banks comfortable with multi-property investors. The result: a sequencing strategy that would let him hit his target within his original timeframe without injecting fresh cash.",
        ],
        "approach": [
            ("Equity recycling from existing property", "We refinanced his existing investment property with a new lender at a sharper rate and split structure, releasing $124,000 of usable equity (within the 65% LVR investor cap) without selling the asset. That equity became the deposit for property #2."),
            ("New-build LVR exemption strategy", "Properties #2, #3, and #4 were all new-build purchases in growth Hamilton suburbs (Rototuna and Flagstaff). New builds are LVR-speed-limit exempt, allowing 80% LVR on each rather than the 65% investor cap — meaning his equity went much further per purchase."),
            ("Three-lender diversification", "Rather than concentrate all loans with one bank (which compounds serviceability constraints), we placed each property with a different lender — main bank for properties #1 and #2, a regional bank for #3 and #4, and a specialist non-bank for #5. This stand-alone structure preserved his serviceability headroom at each step."),
            ("Interest-only structuring on investment properties", "All five properties were structured with 2-5 year interest-only periods, maximising cash flow during the scaling phase. With interest deductibility restored from April 2025, the strategy is tax-efficient and supports continued portfolio growth."),
        ],
        "outcome": [
            "James reached 5 properties exactly 18 months after his first conversation with Finch. Combined portfolio value: $2,100,000. Combined borrowings: $1,540,000. Combined gross rent: ~$2,650/week. He invested $0 of fresh cash — every purchase was funded through equity recycling and the new-build LVR exemption.",
            "His existing property (now property #1) was refinanced again at month 12 of the journey to capture continued equity growth and a $4,800 cashback contribution. His total cashback collected across the 5 transactions: $18,400.",
            "James's feedback: \"My existing bank told me one more was the limit. Working with Finch and structuring across multiple lenders meant the limit was actually about 5 — and I got there inside the timeframe I set. The semi-retirement plan is now well on track.\"",
        ],
    },
    {
        "slug": "family-guarantee-first-home",
        "tag": "Low-Deposit FHB — Case Study",
        "title_short": "First Home With 8% Deposit Plus Family Guarantee",
        "h1_top": "First Home Buyer",
        "h1_bottom": "Crosses the Line with an 8% Deposit + Family Guarantee.",
        "summary": "A young Christchurch couple bought their first home with 8% saved, using a family guarantee from her parents to bridge the deposit gap.",
        "stats": [
            ("8%", "Their Deposit"),
            ("$520K", "Property Price"),
            ("$0", "Family Cash"),
            ("$8K", "Cashback"),
            ("28 days", "To Pre-Approval"),
        ],
        "situation": [
            "Liam and Aroha are a young couple in their late 20s living in Christchurch — Liam works as an early-career civil engineer ($82,000) and Aroha as a registered nurse ($78,000). They'd been saving for 4 years and had $41,000 in savings plus $19,000 in combined KiwiSaver. On a $520,000 starter home in Halswell, that gave them an 11.5% deposit including KiwiSaver — well short of the 20% main-bank threshold.",
            "They'd been told repeatedly by Christchurch agents and one bank visit that they should keep saving for another 18-24 months. Aroha's parents, who owned their Hornby home mortgage-free, had offered to help — but Liam was uncomfortable with the idea of accepting cash from family, and her parents preferred not to liquidate any savings either.",
            "When they approached Finch, we explained that the family guarantee structure available across all main NZ banks allows family equity to support a deposit without requiring family cash. Aroha's parents would essentially co-pledge a portion of their home equity (which they'd never need to liquidate) to bridge the LVR gap for Liam and Aroha's loan — a clean, well-established NZ structure.",
        ],
        "approach": [
            ("Family Guarantee structure", "We explained the Family Guarantee facility to Aroha's parents in detail — including the strictly limited exposure (capped at the gap amount, ~$62,000, not the whole loan), the release mechanism once Liam and Aroha's equity grows to 20% of property value, and the requirement for independent legal advice for the guarantors. Aroha's parents agreed."),
            ("Independent legal advice for guarantors", "We coordinated with a solicitor to provide Aroha's parents independent legal advice on the guarantee — a regulatory requirement designed to protect family guarantors from undue pressure. The advice confirmed the guarantee was limited, well-structured, and unlikely to crystallise unless Liam and Aroha defaulted (which their serviceability comfortably supported)."),
            ("Lender selection for family guarantee", "Three of the main NZ banks offer family guarantee facilities under different brand names. We selected the lender whose family guarantee terms were cleanest, paired with the sharpest current 2-year fixed rate, and offered an $8,000 cashback contribution to cover Liam and Aroha's legal fees, valuation, and moving costs."),
            ("Release strategy planning", "We modelled the timeline for Aroha's parents' guarantee release. With expected Christchurch property growth plus principal repayment, Liam and Aroha's equity should cross the 20% LVR mark in approximately 3-4 years, at which point the family guarantee is fully released and Aroha's parents' home title is unencumbered again."),
        ],
        "outcome": [
            "Pre-approval was issued within 28 days. Liam and Aroha purchased a 3-bedroom Halswell home for $518,000, just under their $520,000 ceiling. Settlement occurred 5 weeks later. Their loan was structured 70/30 — 70% on a 2-year fixed at 5.69%, 30% floating to allow extra repayments.",
            "The $8,000 cashback contribution from the new lender fully covered their solicitor fees, valuation, and moving costs — meaning the move was effectively cost-neutral despite the lender requiring no fresh family cash. Aroha's parents' home title carries a strictly limited second mortgage that will release automatically once equity hits 20%.",
            "Liam's feedback: \"We were told to wait two more years. Two months later we had keys. Finch found a structure that worked for everyone — including Aroha's parents, who got proper legal advice and were genuinely comfortable with the protections built in.\"",
        ],
    },
    {
        "slug": "loan-declined-second-opinion",
        "tag": "Bank Decline — Case Study",
        "title_short": "Bank Declined, Second Opinion Gets Him Approved",
        "h1_top": "Bank Said No.",
        "h1_bottom": "A Second Opinion Got Him Approved in 12 Days.",
        "summary": "An Auckland IT manager was declined by his own bank with no clear reason given. Finch identified the real issue and secured approval with a different lender.",
        "stats": [
            ("1", "Bank Decline"),
            ("12 days", "To New Approval"),
            ("$640K", "Loan Approved"),
            ("2 lenders", "Compared"),
            ("$0", "Cost to Client"),
        ],
        "related": [
            ("blog/loan-declined-what-next-nz.html", "Loan Declined? What Next", "Your options after a bank says no."),
            ("blog/mortgage-broker-vs-bank-nz.html", "Broker vs Bank", "Why a second opinion often changes the outcome."),
            ("services/pre-approval.html", "Mortgage Pre-Approval", "Get a real answer before you make an offer."),
            ("blog/improve-credit-score-mortgage-nz.html", "Improve Your Credit Score", "Fix the file before you reapply."),
            ("calculators/borrowing-power.html", "Borrowing Power Calculator", "See what you could actually borrow."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Josh, a 34-year-old IT operations manager in Auckland, applied directly to his long-time bank for a $640,000 pre-approval. Three weeks later he received a one-line decline notice with no real explanation — just a generic reference to \"lending criteria.\" He assumed his application was simply too weak and started looking at renting for another year.",
            "When Josh came to Finch for a second opinion, we requested his full credit file and reviewed exactly what the bank's system had seen. The issue wasn't his income or deposit — both were solid. It was a $1,200 unpaid mobile phone bill from three years earlier that had gone to a debt collector, plus two credit cards with a combined $18,000 limit that the bank's scorecard was weighing heavily against him.",
            "Josh hadn't realised the phone bill dispute (which he believed was resolved) was still sitting on his file, and he'd never been told that unused credit card limits — not just balances — count against borrowing capacity at most NZ banks.",
        ],
        "approach": [
            ("Credit file diagnosis", "We pulled Josh's Centrix report and identified the exact default and its settlement status. He paid the $1,200 outstanding amount immediately and obtained written confirmation of settlement from the collection agency — something his original bank never suggested doing."),
            ("Credit card limit reduction", "We advised Josh to reduce his two credit card limits from $18,000 combined down to $4,000, which alone lifted his modelled borrowing capacity by roughly $55,000 under standard bank serviceability rules."),
            ("Lender selection around the settled default", "Not every NZ lender treats a recently settled default the same way. We identified a main bank whose credit policy allows a satisfactorily explained, settled default under $2,000 without an automatic decline, provided the rest of the file is clean."),
            ("Full file resubmission", "Rather than resubmitting to the bank that had already declined him, we lodged a fresh application with a different, better-suited lender — avoiding the flag that a second application to the same bank can sometimes trigger."),
        ],
        "outcome": [
            "Josh's new application was approved in 12 days, with the full $640,000 he originally needed. The lender's credit team specifically noted the settled default and confirmed it was not a barrier given the explanation and clean file otherwise.",
            "He purchased a 2-bedroom apartment in Kingsland for $615,000 the following month, fixed 2 years at 5.75%, with the remaining balance floating so he can pay down the debt faster using his annual bonus.",
            "Josh's feedback: \"I genuinely thought I wasn't ready to buy. Turns out it was one unpaid phone bill and some credit card limits I didn't even know mattered. Finch found the actual problem in a day — my bank never even told me what it was.\"",
        ],
    },
    {
        "slug": "bad-credit-defaults-approved",
        "tag": "Bad Credit — Case Study",
        "title_short": "Buyer With Two Defaults Still Gets Approved",
        "h1_top": "Two Defaults on File.",
        "h1_bottom": "Approved Anyway, Through the Right Lender.",
        "summary": "A Hamilton nurse with two historic defaults from a difficult period was declined by three banks. A specialist non-bank lender approved her within weeks.",
        "stats": [
            ("2", "Historic Defaults"),
            ("3", "Bank Declines First"),
            ("$540K", "Property Purchased"),
            ("15%", "Deposit"),
            ("19 days", "To Approval"),
        ],
        "related": [
            ("blog/bad-credit-mortgage-nz.html", "Bad Credit Mortgage NZ", "How defaults affect approval and what still works."),
            ("lenders/non-bank-lenders.html", "NZ Non-Bank Lenders", "Specialist lenders who look beyond a scorecard."),
            ("blog/improve-credit-score-mortgage-nz.html", "Improve Your Credit Score", "Steps to rebuild your file before reapplying."),
            ("blog/loan-declined-what-next-nz.html", "Loan Declined? What Next", "Your options after multiple declines."),
            ("guides/refinance-guide.html", "Refinance Guide", "Move to a main bank once your file is clean."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Priya, a 41-year-old ICU nurse in Hamilton, went through a difficult separation in 2023 that left her with two defaults — a $2,800 default on a joint credit card her ex-partner stopped paying, and a $650 default on a utility account during a period she describes as \"barely keeping the lights on.\" Both were eventually paid, but stayed on her credit file.",
            "By 2026 Priya was earning strong overtime-inclusive income, had saved a genuine 15% deposit, and wanted to buy a home for herself and her two children. She applied to three main banks. All three declined at initial scorecard stage — none of them even reached the point of assessing her income or deposit properly, because the automated system flagged the defaults and stopped the file there.",
            "Priya assumed bad credit meant she was locked out of home ownership for years. She'd read online that defaults take 5 years to clear and believed nothing could be done in the meantime.",
        ],
        "approach": [
            ("Default context and evidence pack", "We built a written explanation for each default — dates, amounts, root cause, and proof of payment — because specialist lenders assess defaults with context, not just a yes/no flag the way main-bank scorecards do."),
            ("Specialist non-bank lender match", "Several NZ non-bank lenders specifically price for exactly this scenario: strong current income and deposit, historic but resolved credit issues. We matched Priya to a lender whose policy explicitly allows settled defaults under $5,000 with a satisfactory explanation."),
            ("Structuring for a future refinance", "Non-bank rates run higher than main-bank rates, so we structured Priya's loan on a shorter 1-year fixed term specifically so she can refinance to a main bank once her file ages past both defaults — likely within 12-18 months."),
            ("Overtime income verification", "Priya's overtime and shift allowances made up nearly 20% of her income. We compiled 18 months of payslips and a roster letter from Waikato DHB to have this income counted at close to full value rather than heavily shaded."),
        ],
        "outcome": [
            "Priya's application was approved in 19 days by the specialist lender — a stark contrast to the same-day automated declines from the three main banks. She purchased a 3-bedroom home in Rototuna for $540,000, settling 6 weeks later.",
            "Her rate was higher than a clean-file main-bank rate, but manageable given her income, and she's already on track to refinance once her file clears — Finch has scheduled a free review at the 12-month mark to reassess.",
            "Priya's feedback: \"Three banks made me feel like home ownership was years away. Finch looked at the actual story behind the numbers, not just a red flag on a screen. I'm in my own home with my kids, and that's what mattered.\"",
        ],
    },
    {
        "slug": "contractor-fixed-term-income",
        "tag": "Contract Income — Case Study",
        "title_short": "Fixed-Term Contractor Approved, No Permanent Job",
        "h1_top": "No Permanent Job.",
        "h1_bottom": "Approved Anyway on Fixed-Term Contract Income.",
        "summary": "A Wellington IT contractor on rolling fixed-term contracts was told he needed a permanent role to qualify. Finch found lenders who see it differently.",
        "stats": [
            ("6 yrs", "Contracting History"),
            ("3", "Consecutive Contracts"),
            ("$610K", "Loan Approved"),
            ("18 days", "To Pre-Approval"),
            ("2 lenders", "Compared"),
        ],
        "related": [
            ("services/self-employed.html", "Self-Employed & Contractor Lending", "Flexible policy for non-PAYE-permanent income."),
            ("blog/how-much-can-i-borrow.html", "How Much Can I Borrow", "How contract income is assessed by NZ banks."),
            ("calculators/borrowing-power.html", "Borrowing Power Calculator", "Estimate your capacity on contract income."),
            ("blog/mortgage-broker-wellington.html", "Mortgage Broker Wellington", "Local advice for Wellington's contractor-heavy workforce."),
            ("services/pre-approval.html", "Mortgage Pre-Approval", "Know your ceiling before you make an offer."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Aaron, a 38-year-old senior software contractor, had worked continuously in Wellington's public and private sector IT market for 6 years — but always on 12-month fixed-term contracts, renewed or replaced with a new contract each time, never gaps of more than a week or two between them.",
            "His own bank's assessor told him plainly: \"We need to see permanent employment to lend at your income level.\" Despite earning $145,000 annually and having a strong 20% deposit saved, he was offered a borrowing capacity roughly 30% below what a permanent employee on the same income would receive — his contract income was being heavily shaded as though it were unreliable.",
            "Aaron found this frustrating given his continuous 6-year track record was, in his view, more stable than many permanent roles in a shrinking tech sector. He came to Finch to see if that history could actually be recognised properly.",
        ],
        "approach": [
            ("Contract history compilation", "We assembled Aaron's full 6-year contract history — three consecutive contracts, each renewed or replaced without a break, plus reference letters from two previous contract managers confirming consistent renewal expectations."),
            ("Lender policy matching", "NZ lender treatment of contractor income varies significantly. We identified two lenders whose policy treats a documented history of continuous contract renewal (rather than a single fixed-term contract) as equivalent to stable income, with minimal income shading."),
            ("Contract-end-date structuring", "We timed the application to align with Aaron having 9 months remaining on his current contract, which sat comfortably within both target lenders' minimum remaining-term requirements."),
            ("Full income, not shaded income", "Where his own bank had shaded his assessable income by roughly 25%, our selected lender assessed close to 95% of his actual contract rate, reflecting his genuine 6-year continuous history."),
        ],
        "outcome": [
            "Aaron's pre-approval came through in 18 days at $610,000 — roughly $140,000 more than his own bank had offered on the same income. He purchased a 2-bedroom townhouse in Johnsonville for $595,000, well-positioned for his commute into the CBD.",
            "His loan was fixed 18 months at 5.79%, chosen deliberately to realign with his next likely contract renewal date, at which point Finch will revisit his structure and refix.",
            "Aaron's feedback: \"I've been more consistently employed than most of my permanent-role friends, but my bank couldn't see past the word 'contract' on my payslip. Finch found lenders who actually looked at the pattern, not just the label.\"",
        ],
    },
    {
        "slug": "gifted-deposit-no-savings",
        "tag": "Gifted Deposit — Case Study",
        "title_short": "100% Gifted Deposit, No Savings History Needed",
        "h1_top": "No Savings History.",
        "h1_bottom": "A 100% Gifted Deposit Still Got Her Approved.",
        "summary": "A 26-year-old graduate with a strong income but no deposit savings used a fully gifted deposit from her parents to buy her first Auckland home.",
        "stats": [
            ("$78K", "Gifted Deposit"),
            ("0", "Personal Savings Used"),
            ("$650K", "Property Purchased"),
            ("16 days", "To Pre-Approval"),
            ("$0", "Broker Fee"),
        ],
        "related": [
            ("blog/kiwisaver-first-home-withdrawal.html", "KiwiSaver First Home Withdrawal", "Combine KiwiSaver with a gifted deposit."),
            ("blog/deposit-needed-home-loan-nz.html", "How Much Deposit Do You Need", "Deposit pathways for NZ first home buyers."),
            ("guides/first-home-guide.html", "First Home Buyer Guide", "The complete NZ first home buyer playbook."),
            ("services/first-home-buyer.html", "First Home Buyer Mortgage", "Your first step into the NZ property market."),
            ("case-studies/family-guarantee-first-home.html", "Family Guarantee Case Study", "Another way family support can help you buy."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Chloe, a 26-year-old marketing graduate earning $92,000 in Auckland, had a strong income but almost no savings — she'd been paying down student debt and covering high Auckland rent since graduating, with only $3,000 in her account. Her parents offered to gift her the full 12% deposit needed on a $650,000 first home.",
            "When Chloe approached her bank, the loan officer flagged a concern: with no personal savings track record, could the bank be confident she had the financial discipline to manage mortgage repayments? Some lenders specifically want to see 3+ months of genuine savings behaviour before approving a loan, regardless of deposit source.",
            "Chloe worried the entirely gifted nature of her deposit would work against her, even though her parents' gift was unconditional and clearly documented.",
        ],
        "approach": [
            ("Gifted deposit documentation", "We prepared a formal signed gifting letter from Chloe's parents confirming the funds were a genuine, non-repayable gift with no expectation of repayment — the exact documentation NZ lenders require to accept a gifted deposit at face value."),
            ("Lender selection for gift-only deposits", "Not all NZ lenders require a genuine savings history when the deposit is gifted. We identified lenders whose policy accepts a 100% gifted deposit provided the source is clearly evidenced and the applicant demonstrates strong ongoing serviceability — which Chloe's income comfortably supported."),
            ("Serviceability-first case", "Rather than relying on a savings track record to prove discipline, we built Chloe's case around her income-to-expense ratio and clean rental payment history (12 months of on-time rent, verified via bank statements), which several lenders accept as an alternative discipline signal."),
            ("Timing the funds transfer", "We coordinated the timing of the gift transfer with Chloe's parents' solicitor to ensure the funds were seasoned in her account for the minimum period each lender required before settlement, avoiding any last-minute documentation issues."),
        ],
        "outcome": [
            "Chloe's pre-approval was issued in 16 days. She purchased a 1-bedroom apartment with a study nook in Mount Eden for $648,000, settling 5 weeks later — her first home, entirely funded by her own income going forward despite starting with almost no savings.",
            "Her loan was fixed 2 years at 5.79%, and she's since set up an automatic extra-repayment plan to start building genuine savings discipline post-settlement, which Finch will factor into any future refinance or top-up.",
            "Chloe's feedback: \"I felt embarrassed that I didn't have savings of my own to show, even with my parents' gift ready to go. Finch explained exactly what lenders needed to see and found one that didn't need a savings history at all.\"",
        ],
    },
    {
        "slug": "trust-structure-investment-purchase",
        "tag": "Trust Structure — Case Study",
        "title_short": "Investor Buys Second Property Through a Family Trust",
        "h1_top": "Buying Through a Trust.",
        "h1_bottom": "Structured Right the First Time.",
        "summary": "A Tauranga business owner used an existing family trust to purchase an investment property, navigating trustee lending requirements most banks find complex.",
        "stats": [
            ("2nd", "Property in Trust"),
            ("$820K", "Purchase Price"),
            ("3", "Trustees"),
            ("24 days", "To Approval"),
            ("2 lenders", "Compared"),
        ],
        "related": [
            ("services/investment-property.html", "Investment Property Loan", "Grow your NZ property portfolio."),
            ("blog/using-home-equity-investment-property-nz.html", "Using Home Equity", "Fund a deposit from existing property equity."),
            ("case-studies/portfolio-growth.html", "Portfolio Growth Case Study", "Scaling an NZ investment portfolio."),
            ("case-studies/apartment-investor-scaling.html", "Apartment Investor Case Study", "Another investor's multi-property journey."),
            ("services/asset-finance.html", "Asset Finance", "Business and trust-related lending options."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Marcus, a 47-year-old business owner in Tauranga, held his family home in a trust established years earlier for asset-protection reasons on his accountant's advice. When he decided to buy a $820,000 investment property, he wanted it held in the same trust for consistency — but quickly found most bank branch staff weren't equipped to handle trust lending smoothly.",
            "Two initial enquiries stalled for weeks: one bank required all three trustees (Marcus, his wife, and an independent trustee) to attend an in-branch appointment together, which was near-impossible to coordinate; another wanted a level of trust-deed legal review that added significant delay and legal cost before even assessing the loan.",
            "Marcus was concerned the purchase — already under a tight due-diligence deadline — would fall through purely on lending-structure friction, not because the loan itself was unaffordable.",
        ],
        "approach": [
            ("Trust deed pre-review", "We had Marcus's solicitor confirm the trust deed's borrowing powers up front, producing a certificate of trust and trustee resolution ready to hand to any lender — removing the single biggest cause of trust-lending delay."),
            ("Lender selection for trust structures", "Some NZ lenders process trust lending routinely; others rarely see it and move slowly as a result. We selected a lender with a dedicated trust-lending process that doesn't require all trustees physically in-branch, accepting remote verification for the independent trustee."),
            ("Guarantor structuring", "Because trusts themselves don't have serviceability, Marcus and his wife were structured as personal guarantors behind the trust borrowing, with the trust's existing rental income and Marcus's business income both counted toward serviceability."),
            ("Timeline management against due diligence", "We ran the application in parallel with Marcus's due diligence period rather than sequentially, giving the lender everything needed to issue conditional approval before due diligence expired."),
        ],
        "outcome": [
            "Full approval was issued in 24 days — inside Marcus's due-diligence window with several days to spare. The trust settled on the $820,000 Tauranga rental property, adding to Marcus's existing portfolio held under the same structure.",
            "The loan was fixed 3 years at 5.89%, chosen for payment certainty across Marcus's business planning cycle, with rental income covering the majority of the repayment.",
            "Marcus's feedback: \"Every bank I called seemed unsure how to handle a trust purchase quickly. Finch had a lender and a process ready to go, and made sure our solicitor had everything sorted before we even needed it.\"",
        ],
    },
    {
        "slug": "lifestyle-block-rural-purchase",
        "tag": "Lifestyle Block — Case Study",
        "title_short": "Waikato Family Finances a 4-Hectare Lifestyle Block",
        "h1_top": "A Lifestyle Block Purchase.",
        "h1_bottom": "Financed Without a Standard Residential Policy.",
        "summary": "A Hamilton family wanted to move to a 4-hectare lifestyle block near Cambridge. Finch matched them to a lender comfortable with larger rural-residential land.",
        "stats": [
            ("4 ha", "Land Size"),
            ("$1.15M", "Purchase Price"),
            ("25%", "Deposit"),
            ("22 days", "To Approval"),
            ("3 lenders", "Compared"),
        ],
        "related": [
            ("blog/mortgage-broker-hamilton.html", "Mortgage Broker Hamilton", "Local advice across the wider Waikato region."),
            ("blog/build-vs-buy-nz.html", "Build vs Buy NZ", "Weighing a lifestyle build against buying existing."),
            ("services/home-loan.html", "NZ Home Loan Service", "Independent advice across 20+ NZ lenders."),
            ("services/construction-loan.html", "Construction Loan", "For lifestyle blocks needing a future build."),
            ("calculators/mortgage-calculator.html", "Mortgage Calculator", "Estimate repayments on a larger rural-residential loan."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "The Andersons, a family of four in Hamilton, wanted to move onto a 4-hectare lifestyle property near Cambridge for more space and to run a small hobby-farm operation alongside their day jobs. The property was priced at $1.15 million, and they had a strong 25% deposit from the sale of their existing home.",
            "Their first two lender enquiries were disappointing. Most main-bank standard residential lending policies cap out around 2-4 hectares before a property is reclassified as rural or lifestyle lending, triggering different valuation requirements, different servicing tests, and in some cases a requirement for a specialist rural valuer rather than a standard residential valuation — adding weeks and uncertainty.",
            "One bank declined outright, citing the land size and a small existing shed that could be interpreted as farm infrastructure requiring commercial-style assessment, despite the Andersons having no farming income and using the land purely for lifestyle purposes.",
        ],
        "approach": [
            ("Land-use clarification", "We worked with the Andersons to clearly document the property's purely residential/lifestyle use — no commercial farming income, no stock beyond a few family pets — which materially changes how several lenders classify and price the loan."),
            ("Lender selection for larger lifestyle blocks", "We identified a main bank and a specialist lender both comfortable lending on lifestyle blocks up to 10 hectares under standard residential policy, provided use is genuinely residential and the property doesn't derive farming income."),
            ("Valuation coordination", "We arranged a valuer experienced specifically with Waikato lifestyle properties, avoiding a generic rural valuation that can undervalue lifestyle-specific features like landscaping, fencing, and outbuildings relevant to resale value."),
            ("Serviceability on dual PAYE income", "With both Andersons on stable PAYE income and a strong deposit, the case for approval was straightforward once the land-size and use classification issue was resolved — the real blocker was never affordability."),
        ],
        "outcome": [
            "Approval was issued in 22 days once the correct lender and valuer were engaged — versus an outright decline elsewhere. The Andersons settled on the Cambridge lifestyle block, moving with their two children in time for the new school term.",
            "Their loan was structured 60/40 — 60% fixed 3 years at 5.85%, 40% floating to allow flexibility for future improvements to the property, including fencing upgrades they're planning in year two.",
            "Their feedback: \"We were told our dream block was 'too rural' for a normal home loan. Finch found lenders who saw it exactly as what it was — our family home with some extra land, not a farm.\"",
        ],
    },
    {
        "slug": "new-job-probation-period-approval",
        "tag": "New Job — Case Study",
        "title_short": "Approved on a New Job, Still Inside the Trial Period",
        "h1_top": "Still on a 90-Day Trial.",
        "h1_bottom": "Approved for a Home Loan Anyway.",
        "summary": "A Christchurch accountant who'd just started a new role was told to wait 6 months before applying. Finch found a lender that didn't require it.",
        "stats": [
            ("6 wks", "Into New Role"),
            ("$92K", "New Salary"),
            ("$530K", "Loan Approved"),
            ("2 lenders", "Compared"),
            ("20 days", "To Pre-Approval"),
        ],
        "related": [
            ("blog/how-long-mortgage-approval-takes-nz.html", "Mortgage Approval Timeline", "What lenders check and how long it takes."),
            ("calculators/borrowing-power.html", "Borrowing Power Calculator", "Estimate your capacity on a new salary."),
            ("services/home-loan.html", "NZ Home Loan Service", "Independent advice across 20+ NZ lenders."),
            ("blog/mortgage-broker-christchurch.html", "Mortgage Broker Christchurch", "Local Canterbury market advice."),
            ("services/pre-approval.html", "Mortgage Pre-Approval", "Know your ceiling before you make an offer."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Grace, a 29-year-old management accountant, had just accepted a $92,000 role at a larger Christchurch firm — a genuine step up from her previous $74,000 position in the same field. Six weeks into the new job, still technically inside her 90-day trial period, she found a townhouse she wanted to buy.",
            "Her bank's response was blunt: come back after 6 months in the role, once she was confirmed permanent past probation. This is a common, conservative default policy at several NZ banks, treating any employee still on a trial or probation period as higher risk regardless of their employment history.",
            "Grace had 7 years of continuous accounting employment before this role, with no gaps, and her new salary was well-documented in her signed employment agreement. She felt the blanket 6-month rule didn't reflect her actual risk profile.",
        ],
        "approach": [
            ("Employment continuity evidence", "We compiled Grace's full 7-year accounting employment history with no gaps, alongside her signed new employment agreement confirming salary, and a reference letter from her new employer confirming no performance concerns during her trial period so far."),
            ("Lender policy matching", "Several NZ lenders will assess a new role on a case-by-case basis rather than an automatic 6-month wait, particularly where the applicant is moving within the same profession with a continuous work history and no probation-related concerns flagged."),
            ("Same-industry salary continuity argument", "Because Grace's move was a lateral step-up within accounting rather than a career change, we framed the application around income continuity and professional stability, which several lenders' credit teams weight heavily over the technical probation-period status."),
            ("Conditional-offer safety net", "We structured the application with her previous role's income as a fallback reference point, giving the lender confidence that even a worst-case reversion to her prior salary would still comfortably service the loan."),
        ],
        "outcome": [
            "Grace's pre-approval was issued in 20 days, without waiting for her probation period to end. She purchased a 2-bedroom townhouse in Riccarton for $525,000, settling just after her 90-day trial period naturally concluded — with no lending impact either way.",
            "Her loan was fixed 2 years at 5.75%, and she's already received formal confirmation of permanency from her new employer, removing any residual uncertainty.",
            "Grace's feedback: \"I was ready to put my search on hold for six months over a technicality. Finch found a lender who actually looked at my career history instead of just the word 'probation' on my file.\"",
        ],
    },
    {
        "slug": "non-bank-to-bank-refinance-credit-repair",
        "tag": "Refinance — Case Study",
        "title_short": "From Non-Bank Lender Back to a Main Bank",
        "h1_top": "Started With a Non-Bank Lender.",
        "h1_bottom": "Refinanced to a Main Bank 18 Months Later.",
        "summary": "A couple who'd needed a non-bank lender due to past credit issues rebuilt their file and refinanced to a main bank, saving significantly on their rate.",
        "stats": [
            ("18 mo", "On Non-Bank Loan"),
            ("1.15%", "Rate Reduction"),
            ("$310/mo", "Repayment Saving"),
            ("$6,500", "Cashback Received"),
            ("3 wks", "Refinance Process"),
        ],
        "related": [
            ("services/refinance.html", "Refinance Mortgage", "Lower your rate and switch lenders."),
            ("calculators/refinance-savings.html", "Refinance Savings Calculator", "See how much switching could save you."),
            ("lenders/non-bank-lenders.html", "NZ Non-Bank Lenders", "When a non-bank lender makes sense short-term."),
            ("blog/improve-credit-score-mortgage-nz.html", "Improve Your Credit Score", "How the couple rebuilt their file."),
            ("case-studies/bad-credit-defaults-approved.html", "Bad Credit Case Study", "Another buyer who started with credit issues."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Ben and Sarah, a couple in their early 30s in Palmerston North, bought their first home 18 months ago through a specialist non-bank lender after Ben's credit file showed a default from a business venture that failed a few years earlier. At the time, it was the only realistic path to home ownership — but the rate was noticeably higher than main-bank pricing.",
            "Since settling, they'd made every repayment on time, Ben's default had aged off his credit file entirely, and their combined income had grown. They wanted to know whether it was worth refinancing to a main bank, but were unsure if 18 months was \"long enough\" or whether the switching costs would outweigh the benefit.",
            "Their existing non-bank lender hadn't proactively suggested a review, and Ben and Sarah weren't sure where to start comparing options themselves.",
        ],
        "approach": [
            ("Full credit file recheck", "We confirmed Ben's default had aged off both Centrix and Equifax entirely, and that 18 months of perfect repayment history on the non-bank loan was itself now a positive signal to a new lender, not a red flag."),
            ("Break-cost and cashback modelling", "We calculated the full economics of switching: any break fee on the existing loan, new lender legal and valuation costs, against the new lower rate and an available cashback contribution — confirming a clear net benefit within the first year alone."),
            ("Main-bank lender selection", "We matched Ben and Sarah to a main bank whose policy treats a clean 18-month repayment history on a prior non-bank loan as strong evidence of reliability, rather than requiring a longer standard credit-history window."),
            ("Structure refresh", "Beyond just the rate, we restructured their loan from a single floating facility into a 70/30 fixed/floating split, better matching their now-improved ability to make extra repayments."),
        ],
        "outcome": [
            "The refinance completed in 3 weeks. Ben and Sarah's new main-bank rate was 1.15 percentage points lower than their non-bank rate, cutting their monthly repayment by roughly $310 — savings they've redirected into extra principal repayments.",
            "They also received a $6,500 cashback contribution from the new lender, more than covering their legal and valuation costs with money left over.",
            "Sarah's feedback: \"Our non-bank lender got us into our home when nobody else would, and we're grateful for that — but nobody told us we could move on once our credit file cleared. Finch reviewed it without us even having to ask exactly the right question.\"",
        ],
    },
    {
        "slug": "leaky-home-remediation-finance",
        "tag": "Weathertightness — Case Study",
        "title_short": "Financing a Leaky Home With Remediation Built In",
        "h1_top": "A Home With Weathertightness Issues.",
        "h1_bottom": "Financed With Remediation Costs Included.",
        "summary": "An Auckland couple wanted a character 1990s home flagged for weathertightness risk. Finch structured finance covering both the purchase and the remediation.",
        "stats": [
            ("1998", "Build Year"),
            ("$95K", "Remediation Cost"),
            ("$780K", "Purchase Price"),
            ("2", "Lenders Assessed"),
            ("26 days", "To Approval"),
        ],
        "related": [
            ("guides/how-mortgage-works.html", "How Mortgages Work", "Understanding lender risk assessment on older builds."),
            ("blog/mortgage-document-checklist-nz.html", "Mortgage Document Checklist", "What lenders need for a complex purchase."),
            ("services/home-loan.html", "NZ Home Loan Service", "Independent advice across 20+ NZ lenders."),
            ("services/construction-loan.html", "Construction Loan", "For remediation and renovation-linked finance."),
            ("blog/hidden-costs-buying-house-nz.html", "Hidden Costs of Buying a House", "What else to budget for beyond the purchase price."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Nathan and Grace fell in love with a 1998-built monolithic-clad home in Auckland's Mount Albert — exactly the era and construction style associated with New Zealand's well-known weathertightness (\"leaky home\") issues. A pre-purchase building report confirmed moisture ingress risk and recommended a full re-clad, estimated at $95,000.",
            "Their first bank declined the application outright once the building report was disclosed — citing the property as an unacceptable security risk in its current condition, full stop, regardless of the couple's income or deposit strength.",
            "Nathan and Grace still wanted the property (priced accordingly below comparable weathertight homes in the same street) but needed a lender willing to finance both the purchase and the remediation as a combined package.",
        ],
        "approach": [
            ("Remediation scope and quote formalisation", "We had Nathan and Grace obtain a fixed-price quote from a qualified re-cladding specialist, converting the building report's estimate into a bankable, itemised scope of works — a requirement for any lender to consider remediation-inclusive lending."),
            ("Lender selection for as-if-complete valuation", "We identified a lender that will value a weathertightness-affected property on an \"as-if-remediated\" basis when a fixed-price contract and qualified building consent are in place, rather than only lending against the property's current, discounted condition."),
            ("Staged drawdown structuring", "The loan was structured with an initial drawdown to fund settlement at the discounted purchase price, and a second staged drawdown released against the remediation contract as work milestones were completed and signed off."),
            ("Council consent and LBP coordination", "We worked with Nathan and Grace's building consultant to ensure the remediation used a Licensed Building Practitioner and had council consent lodged before the lender would confirm the staged drawdown facility."),
        ],
        "outcome": [
            "Approval was issued in 26 days once the fixed-price remediation contract was in place — a deal the first bank had refused outright. Nathan and Grace settled on the $780,000 purchase, with remediation funded as part of the same facility rather than requiring separate finance.",
            "The re-clad was completed within 5 months, and the property was re-valued post-remediation at a level consistent with weathertight comparable sales in the same street, protecting their long-term equity position.",
            "Grace's feedback: \"We thought we'd lost the house the moment the first bank said no. Finch found a lender who understood exactly how to finance a property mid-remediation, not just a finished one.\"",
        ],
    },
    {
        "slug": "returning-kiwi-overseas-income",
        "tag": "Returning Kiwi — Case Study",
        "title_short": "Returning Kiwi Buys Using Overseas Income",
        "h1_top": "Still Earning Overseas.",
        "h1_bottom": "Approved for an NZ Home Loan Before Relocating.",
        "summary": "A New Zealander working in Australia wanted to secure a home loan before relocating home. Finch arranged approval based on her overseas employment income.",
        "stats": [
            ("AUD $118K", "Overseas Salary"),
            ("8 yrs", "Time Overseas"),
            ("$720K", "Property Purchased"),
            ("3 wks", "To Pre-Approval"),
            ("2 lenders", "Compared"),
        ],
        "related": [
            ("blog/work-visa-home-loan-nz.html", "Work Visa Home Loans", "How banks assess non-standard residency and income."),
            ("services/first-home-buyer.html", "First Home Buyer Mortgage", "Your first step into the NZ property market."),
            ("blog/mortgage-broker-nz.html", "Mortgage Broker NZ", "Independent NZ-wide broker support."),
            ("guides/first-home-guide.html", "First Home Buyer Guide", "The complete NZ first home buyer playbook."),
            ("blog/kiwisaver-first-home-withdrawal.html", "KiwiSaver First Home Withdrawal", "Using KiwiSaver on your return to NZ."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Emma, a 33-year-old New Zealander, had spent 8 years working in Sydney as a project manager, earning AUD $118,000. With a return to NZ planned within 4 months to be closer to family, she wanted to secure a home loan and have a property ready to move into, rather than arriving with nowhere to live and searching under time pressure.",
            "Her enquiry with an NZ bank stalled because she wasn't yet an NZ tax resident and her income was entirely overseas-sourced — some lenders' standard servicing calculators simply aren't set up to assess foreign-currency income cleanly, and staff weren't confident how to proceed.",
            "Emma had NZ citizenship, a clean NZ credit history from before she left, and $180,000 in savings (partly AUD, partly already converted to NZD) — but needed a lender comfortable assessing her Australian income and confirming approval before she'd landed back in the country.",
        ],
        "approach": [
            ("Overseas income verification package", "We compiled Emma's Australian payslips, employment contract, and Australian Tax Office assessment, converted at a conservative long-run AUD/NZD exchange rate buffer to protect against currency movement between application and settlement."),
            ("Lender selection for returning-Kiwi scenarios", "We identified NZ lenders with specific policy for citizens returning from overseas employment, who assess foreign income at a sensible conversion rate rather than declining on the basis of non-NZ income alone."),
            ("Settlement-date alignment", "We structured the pre-approval with a settlement date aligned to Emma's confirmed return date, giving her certainty to make an offer on a property before physically arriving in NZ."),
            ("NZ credit history reactivation", "Emma's NZ credit file was 8 years dormant. We confirmed with the lender that a dormant-but-clean file, combined with her citizenship and clear intent to reside, was treated the same as an active NZ credit history."),
        ],
        "outcome": [
            "Emma's pre-approval was issued within 3 weeks, entirely based on her Australian income and remote documentation. She purchased a 3-bedroom home in Hamilton for $720,000 sight-seen via video walkthrough with a trusted family member attending in person, settling the week after she landed back in NZ.",
            "Her loan was fixed 2 years at 5.79%, converted from her AUD savings at settlement with a small buffer intact from the conservative exchange-rate modelling used during the application.",
            "Emma's feedback: \"I didn't want to arrive back in New Zealand with nowhere to live and no idea if I'd even qualify for a loan. Finch had everything sorted before I'd even booked my flight home.\"",
        ],
    },
    {
        "slug": "buy-out-ex-partner-separation",
        "tag": "Separation — Case Study",
        "title_short": "Refinancing to Buy Out an Ex-Partner",
        "h1_top": "Buying Out an Ex-Partner.",
        "h1_bottom": "Keeping the Family Home After Separation.",
        "summary": "A Dunedin teacher refinanced solo to buy out her ex-partner's share of the family home, keeping stability for her children without needing to sell.",
        "stats": [
            ("50%", "Equity Bought Out"),
            ("$410K", "New Sole Loan"),
            ("1 income", "Serviced On"),
            ("17 days", "To Approval"),
            ("$0", "Cost to Client"),
        ],
        "related": [
            ("blog/bright-line-test-nz-2026.html", "Bright-Line Test Explained", "Tax implications when transferring property after separation."),
            ("services/refinance.html", "Refinance Mortgage", "Restructure your loan into your name alone."),
            ("case-studies/single-parent-rebuilds.html", "Single Parent Case Study", "Another parent's journey rebuilding after separation."),
            ("calculators/borrowing-power.html", "Borrowing Power Calculator", "Check your solo borrowing capacity."),
            ("blog/mortgage-broker-dunedin.html", "Mortgage Broker Dunedin", "Local Otago market advice."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Hannah, a 39-year-old secondary school teacher in Dunedin, separated from her partner after 11 years together, with two teenage children still in school. Rather than sell the family home and disrupt her children's schooling and routines, Hannah and her ex-partner agreed she would buy out his 50% share of the equity and keep the house in her name alone.",
            "The challenge was straightforward but significant: refinancing a jointly-owned mortgage into a single name, on a single teacher's income, while also raising the funds to pay out her ex-partner's equity share — without selling the property to do it.",
            "Hannah's existing joint-mortgage bank offered a borrowing capacity that fell short of what was needed to complete the buyout, and she was worried the arrangement with her ex-partner would collapse under financial pressure and force a sale after all.",
        ],
        "approach": [
            ("Property valuation and equity calculation", "We arranged an independent registered valuation to establish a fair current market value, from which the exact buyout figure owed to Hannah's ex-partner was calculated transparently for both parties and their respective solicitors."),
            ("Sole-income serviceability maximisation", "We reviewed every element of Hannah's income — base teaching salary, plus any allowances and holiday-period pay structures specific to teaching roles — to ensure her full servicing capacity was captured accurately rather than conservatively estimated."),
            ("Lender selection for separation-driven refinances", "We selected a lender whose policy and pricing were most favourable for a sole-income refinance of this size relative to Hannah's income, rather than defaulting to her existing joint-mortgage bank which had already indicated a shortfall."),
            ("Legal coordination with both parties", "We worked directly with Hannah's solicitor and her ex-partner's solicitor to align the refinance settlement date with the property transfer and payout, ensuring funds released to her ex-partner exactly when the ownership transfer completed."),
        ],
        "outcome": [
            "Approval for the $410,000 sole-name loan was issued in 17 days — enough to both refinance the existing joint mortgage and pay out her ex-partner's equity share in full. The transfer of ownership and mortgage refinance completed on the same day.",
            "Hannah's children stayed in the same home, same school, same routine throughout — the outcome she'd prioritised from the start. Her loan was fixed 2 years at 5.69%, with repayments comfortably within her sole teaching income.",
            "Hannah's feedback: \"Everyone kept telling me I'd have to sell on a single income. Finch found a way to make the numbers work so my kids didn't have to lose their home on top of everything else changing.\"",
        ],
    },
    {
        "slug": "redundancy-income-recovery-approval",
        "tag": "Post-Redundancy — Case Study",
        "title_short": "Approved 4 Months After Redundancy",
        "h1_top": "Made Redundant.",
        "h1_bottom": "Approved for a Mortgage 4 Months Later.",
        "summary": "An Auckland marketing manager made redundant re-entered the workforce quickly. Finch structured a strong case despite the recent income gap on his file.",
        "stats": [
            ("4 mo", "Since Redundancy"),
            ("6 wks", "Job Search Length"),
            ("$95K", "New Salary"),
            ("$560K", "Loan Approved"),
            ("21 days", "To Pre-Approval"),
        ],
        "related": [
            ("blog/loan-declined-what-next-nz.html", "Loan Declined? What Next", "Rebuilding a case after an income interruption."),
            ("calculators/borrowing-power.html", "Borrowing Power Calculator", "Check your capacity on a new salary."),
            ("services/home-loan.html", "NZ Home Loan Service", "Independent advice across 20+ NZ lenders."),
            ("blog/how-long-mortgage-approval-takes-nz.html", "Mortgage Approval Timeline", "What to expect after a recent job change."),
            ("services/pre-approval.html", "Mortgage Pre-Approval", "Know your ceiling before you make an offer."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Ryan, a 36-year-old marketing manager in Auckland, was made redundant in a company-wide restructure. After a 6-week job search, he secured a new role at a similar level and salary ($95,000) with a different employer. Four months after the redundancy, with 10 weeks into his new job, he and his partner found a home they wanted to buy.",
            "Their bank's automated system flagged the redundancy and recent employment gap immediately, treating it as a significant risk factor regardless of the fact Ryan was now settled in a new, equivalent role. The initial response suggested waiting a further 6 months of continuous new employment before reapplying.",
            "Ryan and his partner were concerned that waiting meant losing the specific property they'd found, in a market where good family homes in their target area were moving quickly.",
        ],
        "approach": [
            ("Redundancy context documentation", "We obtained Ryan's formal redundancy letter confirming it was a genuine company-wide restructure unrelated to his performance, plus his redundancy payment details — context that materially changes how lenders view an employment gap."),
            ("New role stability evidence", "We compiled his new employment agreement, an employer reference confirming strong early performance, and his first pay cycle's payslips to demonstrate the new role was genuine, ongoing, and at an equivalent salary to his prior position."),
            ("Lender selection around recent employment gaps", "We identified a lender whose policy assesses redundancy-driven gaps on their specific circumstances — genuine restructure, quick re-employment, comparable new salary — rather than applying a blanket minimum-tenure rule regardless of context."),
            ("Redundancy payout as a serviceability buffer", "Rather than treating Ryan's untouched redundancy payout as irrelevant, we presented it as an additional financial buffer strengthening the overall application, which several lenders view favourably as reduced risk."),
        ],
        "outcome": [
            "Pre-approval was issued in 21 days — well within the timeframe needed to secure the property they wanted. Ryan and his partner purchased a 4-bedroom home in Papatoetoe for $555,000, settling 6 weeks later.",
            "Their loan was fixed 2 years at 5.75%, and Ryan's redundancy payout was kept aside as a genuine emergency buffer rather than being used toward the deposit, exactly as structured in the application.",
            "Ryan's feedback: \"The word 'redundancy' seemed to shut every conversation down immediately. Finch looked at the full picture — a new job at the same level, a clean explanation, and money in the bank — and found a lender who agreed that mattered more than the gap itself.\"",
        ],
    },
    {
        "slug": "second-home-holiday-home-purchase",
        "tag": "Second Home — Case Study",
        "title_short": "Financing a Second Home at Lake Taupō",
        "h1_top": "A Second Home at the Lake.",
        "h1_bottom": "Financed Without Selling the First.",
        "summary": "An Auckland couple wanted a holiday home at Lake Taupō without selling their existing property. Finch structured lending using equity from both.",
        "stats": [
            ("2nd", "Property Financed"),
            ("$540K", "Taupō Purchase"),
            ("$0", "Existing Home Sold"),
            ("70%", "Equity Used"),
            ("20 days", "To Approval"),
        ],
        "related": [
            ("services/next-home-buyer.html", "Next Home Buyer Mortgage", "Upgrade, move, or add a second property."),
            ("blog/using-home-equity-investment-property-nz.html", "Using Home Equity", "Fund a second property from existing equity."),
            ("calculators/mortgage-calculator.html", "Mortgage Calculator", "Estimate repayments on a second property."),
            ("blog/mortgage-broker-nz.html", "Mortgage Broker NZ", "Independent advice for buyers anywhere in NZ."),
            ("services/investment-property.html", "Investment Property Loan", "If you're considering short-term rental income too."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Michael and Diane, both in their early 50s in Auckland, wanted to buy a $540,000 holiday home at Lake Taupō for family use and eventual retirement, without selling their existing debt-free Auckland home. Their own bank suggested a large lump-sum equity release against their Auckland property, structured as one combined facility.",
            "Michael and Diane were uneasy about that structure — they wanted the two properties kept financially distinct where possible, partly for future estate-planning clarity between their adult children, and partly so a future sale of either property wouldn't be entangled with the other's mortgage.",
            "They came to Finch to see whether a cleaner structure was possible while still using their Auckland equity to avoid a large cash outlay.",
        ],
        "approach": [
            ("Equity release sized precisely", "Rather than one large combined facility, we structured a defined equity-release loan secured against the Auckland property for exactly the deposit amount needed on the Taupō purchase, keeping the two debts conceptually and administratively separate."),
            ("Separate loan for the Taupō property", "The remaining balance of the Taupō purchase was financed as its own distinct mortgage secured against the new property itself, so each property carries security proportional to its own debt."),
            ("Lender selection for multi-property clarity", "We selected a lender whose systems and statements clearly separate multiple linked facilities, so Michael and Diane receive distinct, easy-to-follow statements for each property rather than one blended facility."),
            ("Retirement-horizon rate structuring", "With retirement in view within roughly a decade, we structured both facilities with a mix of fixed terms designed to allow orderly principal reduction well ahead of Michael and Diane's planned retirement date."),
        ],
        "outcome": [
            "Approval across both linked facilities was issued in 20 days. Michael and Diane purchased the Taupō property for $540,000, keeping their Auckland home entirely unencumbered beyond the specific equity-release amount used for the deposit.",
            "Both facilities were fixed 3 years — the Auckland equity-release portion at 5.79%, the Taupō property loan at 5.85% — with a clear, separate repayment plan for each ahead of their retirement timeline.",
            "Diane's feedback: \"We didn't want everything blended into one big loan against our home. Finch structured it so each property stands on its own, which matters a lot to us for the kids' sake down the track.\"",
        ],
    },
    {
        "slug": "mortgagee-sale-purchase-finance",
        "tag": "Mortgagee Sale — Case Study",
        "title_short": "Fast Finance to Secure a Mortgagee Sale",
        "h1_top": "A Mortgagee Sale.",
        "h1_bottom": "Finance Confirmed in Time to Bid.",
        "summary": "A first-home buyer wanted to bid on a mortgagee sale property with an unconditional deadline in 10 days. Finch delivered finance approval in time.",
        "stats": [
            ("10 days", "To Auction Deadline"),
            ("$490K", "Purchase Price"),
            ("Unconditional", "Bid Required"),
            ("8 days", "To Full Approval"),
            ("1", "Property Secured"),
        ],
        "related": [
            ("blog/buying-at-auction-nz-finance-ready.html", "Buying at Auction, Finance-Ready", "How to be ready to bid unconditionally."),
            ("case-studies/bridging-finance-lifestyle.html", "Bridging Finance Case Study", "Another time-pressured NZ purchase."),
            ("services/pre-approval.html", "Mortgage Pre-Approval", "Know your ceiling before a fast-moving sale."),
            ("guides/first-home-guide.html", "First Home Buyer Guide", "The complete NZ first home buyer playbook."),
            ("blog/how-long-mortgage-approval-takes-nz.html", "Mortgage Approval Timeline", "How fast NZ approvals can realistically move."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Tyler, a 31-year-old electrician, had been pre-approved and house-hunting for months when he found a 3-bedroom home in South Auckland listed as a mortgagee sale at $490,000 — priced attractively below comparable homes in the same street. Mortgagee sales move fast and almost always require an unconditional offer, with a firm auction date just 10 days away.",
            "Tyler's existing pre-approval was 4 months old and conditional on standard finance clauses — not the unconditional certainty a mortgagee sale demands. Bidding unconditionally without confirmed, finalised finance would have meant risking his deposit entirely if anything in the file changed.",
            "With the tight deadline, Tyler needed his finance fully finalised — not just pre-approved — before auction day, or he'd have to walk away from a property priced well under market value.",
        ],
        "approach": [
            ("Rapid document refresh", "We immediately refreshed Tyler's file — updated payslips, bank statements, and confirmation nothing material had changed since his original pre-approval — to avoid restarting the assessment from scratch."),
            ("Priority lender selection for speed", "We selected the lender in our panel with the fastest current turnaround for full (not just conditional) approval, based on real-time knowledge of which credit teams were moving quickest that week."),
            ("Registered valuation fast-tracked", "We engaged a valuer able to turn around a mortgagee-sale valuation within 48 hours, flagging the file as time-critical — mortgagee sale valuations can sometimes be more conservative, so timing and valuer choice both mattered."),
            ("Unconditional-ready loan documentation", "We ensured Tyler's full loan documents were prepared and ready to sign the moment formal approval came through, so there was zero lag between approval and being genuinely unconditional-ready to bid."),
        ],
        "outcome": [
            "Full, unconditional-ready approval was confirmed in 8 days — 2 days ahead of the auction deadline. Tyler bid with full confidence and secured the property at $490,000, with settlement occurring on the standard mortgagee-sale timeline.",
            "His loan was fixed 2 years at 5.75%, and the property's below-market purchase price gave him instant equity from day one, confirmed by the registered valuation completed during the approval process.",
            "Tyler's feedback: \"I almost didn't bid because I assumed there was no way finance could move fast enough. Finch had everything locked down two days before the deadline — I didn't have to gamble on it.\"",
        ],
    },
    {
        "slug": "high-dti-young-professional-approved",
        "tag": "DTI Cap — Case Study",
        "title_short": "Approved Despite Student Loan + Car Debt",
        "h1_top": "Student Loan Plus Car Debt.",
        "h1_bottom": "Approved Under the DTI Cap Anyway.",
        "summary": "A young Wellington professional with a student loan and car debt worried her DTI ratio would block her. Finch structured her file to fit under the cap.",
        "stats": [
            ("5.2x", "Final DTI Ratio"),
            ("6x", "Owner-Occupier Cap"),
            ("$620K", "Loan Approved"),
            ("$14K", "Debt Reduced First"),
            ("19 days", "To Pre-Approval"),
        ],
        "related": [
            ("calculators/dti-calculator.html", "DTI Ratio Calculator", "Check your own debt-to-income ratio before applying."),
            ("blog/dti-calculator-debt-to-income-nz.html", "DTI Rules NZ Explained", "How the Reserve Bank's DTI caps actually work."),
            ("calculators/borrowing-power.html", "Borrowing Power Calculator", "See how debt reduction changes your capacity."),
            ("blog/mortgage-broker-wellington.html", "Mortgage Broker Wellington", "Local Wellington market advice."),
            ("services/first-home-buyer.html", "First Home Buyer Mortgage", "Your first step into the NZ property market."),
            ("contact.html", "Book a Free Call", "15-min discovery, no obligation."),
        ],
        "situation": [
            "Amelia, a 27-year-old policy analyst in Wellington earning $105,000, had a $22,000 remaining student loan and a $28,000 car loan alongside a $9,000 credit card limit. When she started looking at a $620,000 first home, she'd read about the Reserve Bank's debt-to-income (DTI) restrictions and worried her existing debt load would push her over the 6x owner-occupier cap before she'd even applied.",
            "A rough calculation using her total debt (including the new mortgage) against her income put her uncomfortably close to the cap once her existing car loan and credit card limit were factored in alongside the new $620,000 mortgage — at real risk of landing above 6x depending on how conservatively each lender counted her credit card limit.",
            "Amelia wasn't sure whether to delay her purchase by a year to pay down debt first, or whether there was a way to structure things now.",
        ],
        "approach": [
            ("Full DTI recalculation", "We calculated Amelia's exact debt-to-income ratio the way lenders actually do it — total debt including the new mortgage, divided by gross income — rather than the rough estimate she'd worked out herself, which had overstated her credit card contribution."),
            ("Targeted debt reduction before applying", "We recommended Amelia use $14,000 of her existing savings, originally earmarked for a slightly larger deposit, to pay down her car loan instead — reducing total debt in a way that moved her DTI ratio more than an equivalent reduction in mortgage size would have."),
            ("Credit card limit reduction", "Amelia reduced her $9,000 credit card limit to $2,000, since DTI calculations count the full limit rather than the balance — a change that cost her nothing day-to-day but meaningfully improved her ratio."),
            ("Lender selection with DTI headroom", "Because the DTI restriction allows each bank a limited monthly quota of above-cap lending, we also confirmed which lender had exemption headroom available that month as a backup, even though Amelia's restructured file ultimately landed comfortably under the cap at 5.2x."),
        ],
        "outcome": [
            "Amelia's pre-approval was issued in 19 days at the full $620,000 she needed, with a final DTI ratio of 5.2x — comfortably under the 6x owner-occupier cap, with no need to draw on any lender's exemption quota.",
            "She purchased a 2-bedroom apartment in Kelburn for $610,000, fixed 2 years at 5.75%, and is continuing to pay down her remaining student loan and car debt ahead of schedule now that she's settled.",
            "Amelia's feedback: \"I was ready to put my search on hold for a year over the DTI rules. Finch showed me the actual math and a couple of small, practical changes that moved me from borderline to comfortably approved.\"",
        ],
    },
]


def schema_for(c: dict) -> str:
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": f"{BASE_URL}/case-studies.html"},
            {"@type": "ListItem", "position": 3, "name": c["title_short"], "item": f"{BASE_URL}/case-studies/{c['slug']}.html"},
        ],
    }
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": c["title_short"],
        "description": c["summary"],
        "url": f"{BASE_URL}/case-studies/{c['slug']}.html",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}/case-studies/{c['slug']}.html"},
        "inLanguage": "en-NZ",
        "image": f"{BASE_URL}/images/finch-logo.png",
        "datePublished": ARTICLE_PUBLISHED,
        "dateModified": ARTICLE_MODIFIED,
        "author": {
            "@type": "Person",
            "@id": f"{BASE_URL}/#mukhtar-kiyani",
            "name": "Mukhtar Kiyani",
            "jobTitle": "Founder & Mortgage Adviser",
            "url": f"{BASE_URL}/about.html",
        },
        "publisher": {
            "@type": "MortgageBroker",
            "@id": f"{BASE_URL}/#organization",
            "name": "Finch Mortgages",
            "url": f"{BASE_URL}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/finch-logo.png"},
        },
    }
    return (
        "<script type=\"application/ld+json\">"
        + json.dumps(breadcrumb, indent=2)
        + "</script>\n<script type=\"application/ld+json\">"
        + json.dumps(article, indent=2)
        + "</script>"
    )


def keywords_for(c: dict) -> str:
    base = [
        "NZ mortgage case study",
        c["title_short"].lower(),
        "NZ mortgage broker case study",
        "real NZ home loan story",
        "Finch Mortgages case study",
        "NZ home loan client story",
    ]
    return ", ".join(base)


def title_for(c: dict) -> str:
    # Kept under 60 characters so titles don't truncate in SERPs.
    return f"{c['title_short']} | Finch"


def main_body(c: dict) -> str:
    stats_html = "".join(
        textwrap.dedent(f"""
            <div style=\"text-align:center;\">
              <div style=\"font-size:2.5rem;font-weight:800;color:var(--finch-gold);line-height:1;\">{value}</div>
              <div style=\"font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.65);margin-top:0.3rem;\">{label}</div>
            </div>
        """)
        for value, label in c["stats"]
    )

    situation_html = "".join(f"<p style=\"color:var(--neutral-medGray);line-height:1.8;margin-bottom:1rem;\">{p}</p>" for p in c["situation"])

    approach_html = ""
    for idx, (heading, body) in enumerate(c["approach"], start=1):
        approach_html += textwrap.dedent(f"""
            <div style=\"display:flex;gap:1.25rem;align-items:flex-start;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;\">
              <div style=\"width:2rem;height:2rem;background:var(--finch-forest);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;\"><span style=\"color:white;font-size:0.7rem;font-weight:800;\">{idx}</span></div>
              <div><strong style=\"display:block;margin-bottom:0.3rem;color:var(--finch-forest);\">{heading}</strong><span style=\"color:var(--neutral-medGray);font-size:0.95rem;line-height:1.6;\">{body}</span></div>
            </div>
        """)

    outcome_html = "".join(f"<p style=\"color:var(--neutral-medGray);line-height:1.8;margin-bottom:1rem;\">{p}</p>" for p in c["outcome"])

    default_related = [
        ("../case-studies.html", "All NZ Case Studies", "Real client outcomes across scenarios."),
        ("../testimonials/reviews.html", "NZ Client Reviews", "5.0 star Google rating."),
        ("../testimonials/success-stories.html", "NZ Success Stories", "In-depth client journeys."),
        ("../calculators/borrowing-power.html", "Borrowing Power", "See your NZ borrowing capacity."),
        ("../services/home-loan.html", "NZ Home Loan Service", "Start your own approval."),
        ("../contact.html", "Book a Free Call", "15-min discovery, no obligation."),
    ]
    related_links = c.get("related")
    if related_links:
        related_links = [(f"../{href}" if not href.startswith("http") and not href.startswith("../") else href, label, desc) for href, label, desc in related_links]
    else:
        related_links = default_related
    related_html = "".join(
        f'<a href="{href}" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">{label}</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">{desc}</span></a>'
        for href, label, desc in related_links
    )

    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <section class="container page-hero" style="padding-bottom:3rem; max-width:780px;">
      <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../case-studies.html">Case Studies</a><span class="breadcrumb-sep">/</span><span>{c['title_short']}</span></nav>
      <div class="page-hero-tag">{c['tag']}</div>
      <h1>{c['h1_top']}<br/><em style="font-style:italic;color:var(--finch-forest);">{c['h1_bottom']}</em></h1>
      <p>{c['summary']}</p>
    </section>

    <section style="background:var(--finch-forest);padding:2.5rem 0;">
      <div class="container">
        <div style="display:flex;gap:3rem;flex-wrap:wrap;justify-content:center;">
          {stats_html}
        </div>
      </div>
    </section>

    <section style="padding:5rem 0;background:white;">
      <div class="container" style="max-width:780px;">
        <div style="margin-bottom:3.5rem;">
          <div class="section-label" style="margin-bottom:1rem;"><span>The Situation</span></div>
          <h2 class="section-heading" style="margin-bottom:1.5rem;">The problem.</h2>
          {situation_html}
        </div>

        <div style="margin-bottom:3.5rem;">
          <div class="section-label" style="margin-bottom:1rem;"><span>The Finch Approach</span></div>
          <h2 class="section-heading" style="margin-bottom:1.5rem;">How we solved it.</h2>
          <div style="display:flex;flex-direction:column;gap:1.25rem;">
            {approach_html}
          </div>
        </div>

        <div style="margin-bottom:1rem;">
          <div class="section-label" style="margin-bottom:1rem;"><span>The Outcome</span></div>
          <h2 class="section-heading" style="margin-bottom:1.5rem;">The result.</h2>
          {outcome_html}
          <p style="color:var(--neutral-medGray);line-height:1.8;margin-top:1.5rem;font-size:0.95rem;">Useful NZ sources: the <a href="https://www.rbnz.govt.nz/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Reserve Bank of New Zealand</a> for current lending policy, and <a href="https://kaingaora.govt.nz/en_NZ/home-ownership/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Kāinga Ora</a> for first-home support schemes.</p>
        </div>
      </div>
    </section>

    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>More NZ Stories</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ case studies &amp; tools</h2>
        <div class="cols-3" style="gap:1.5rem;">
          {related_html}
        </div>
      </div>
    </section>

    <section style="padding:5rem 0;">
      <div class="container">
        <div class="cta-section reveal">
          <h2>Could we help you<br/>get the same result?</h2>
          <p>Book a free 15-minute consultation. We compare your scenario across 20+ NZ lenders and structure the loan for the best outcome.</p>
          <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
            <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
            <a class="btn-cta-outline" href="../case-studies.html">More NZ Case Studies</a>
          </div>
        </div>
      </div>
    </section>
    </main>
    """)


def build_page(c: dict, template_text: str) -> str:
    head_close = template_text.find("</head>")
    head = template_text[:head_close]

    title = title_for(c)
    description = c["summary"]
    canonical = f"{BASE_URL}/case-studies/{c['slug']}.html"
    keywords = keywords_for(c)
    schema = schema_for(c)

    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"description\"/?>',
        f'<meta content="{description}" name="description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<link href=\"https://www\.finchmortgages\.co\.nz/case-studies/[^\"]+\" rel=\"canonical\"/?>',
        f'<link href="{canonical}" rel="canonical"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:title\"/?>',
        f'<meta content="{title}" property="og:title"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:description\"/?>',
        f'<meta content="{description}" property="og:description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:url\"/?>',
        f'<meta content="{canonical}" property="og:url"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"twitter:title\"/?>',
        f'<meta content="{title}" name="twitter:title"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"twitter:description\"/?>',
        f'<meta content="{description}" name="twitter:description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"keywords\"/?>',
        f'<meta content="{keywords}" name="keywords"/>',
        head,
    )
    # The template carries 3 JSON-LD blocks: BreadcrumbList, Article, and a
    # generic reusable FAQPage (market-conditions Q&A, deliberately identical
    # across case studies). Replace all of them with our clean breadcrumb +
    # article, then preserve the original FAQPage once -- a naive count=1
    # replace here previously left the template's own stale Article and a
    # duplicated FAQPage behind (see new-migrant-first-mortgage.html history).
    ld_blocks = re.findall(r"<script type=\"application/ld\+json\">.*?</script>", head, flags=re.S)
    faq_block = next((b for b in ld_blocks if "FAQPage" in b), "")
    head = re.sub(r"\s*<script type=\"application/ld\+json\">.*?</script>", "", head, flags=re.S)
    head = head.rstrip() + "\n" + schema + ("\n" + faq_block if faq_block else "") + "\n"
    head += "</head>"

    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]

    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]

    return head + "\n" + body_open + main_body(c) + footer


def main() -> None:
    template_text = TEMPLATE.read_text(encoding="utf-8")
    targets = [c for c in CASE_STUDIES if c["slug"] in NEW_SLUGS]
    for c in targets:
        out_path = OUT_DIR / f"{c['slug']}.html"
        out_path.write_text(build_page(c, template_text), encoding="utf-8")
        print(f"  + {out_path.relative_to(ROOT)}")
    print(f"\nGenerated {len(targets)} case studies.")


if __name__ == "__main__":
    main()
