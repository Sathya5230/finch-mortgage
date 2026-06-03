"""Generate new topical NZ mortgage blog posts targeting high-search-volume queries.

Reuses head + footer wrappers from an existing blog page so styling and
navigation stay consistent with the rest of the site.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "blog/mortgage-tips.html"
OUT_DIR = ROOT / "blog"
BASE_URL = "https://www.finchmortgages.co.nz"

# ISO 8601 dates for Article rich-result eligibility
ARTICLE_PUBLISHED = "2026-01-15"
ARTICLE_MODIFIED = "2026-06-03"


POSTS = [
    {
        "slug": "how-long-mortgage-approval-takes-nz",
        "title": "How Long Does a Mortgage Approval Take in NZ? (2026)",
        "h1": "How Long Does a Mortgage Approval Take in NZ?",
        "intro_pull": "From first conversation to settlement day, the typical NZ mortgage approval moves through eight stages — and most are faster than buyers expect.",
        "description": "How long mortgage approval takes in NZ — full 2026 timeline from pre-approval (5-10 working days) to settlement (4-6 weeks). Bank-by-bank turnaround comparison.",
        "keywords": [
            "how long does mortgage approval take NZ",
            "NZ mortgage approval timeline",
            "mortgage pre-approval timeline NZ",
            "NZ mortgage settlement timeline",
            "ANZ ASB BNZ approval time",
            "mortgage broker turnaround NZ",
        ],
        "sections": [
            ("The Quick Answer", "<p style=\"margin-bottom:2rem;\">In New Zealand, a clean PAYE pre-approval typically takes <strong>5-10 working days</strong> from document submission. Full unconditional approval after an accepted offer is usually <strong>another 7-14 days</strong>. Settlement day, set by the sale and purchase agreement, is usually <strong>4-6 weeks after the offer is signed</strong>. Self-employed and non-bank applications run a few days longer at each stage.</p>"),
            ("Stage-by-Stage NZ Mortgage Timeline", textwrap.dedent("""
                <ol style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:decimal;\">
                  <li style=\"margin-bottom:0.75rem;\"><strong>Discovery call (Day 0)</strong> — free 15-minute strategy call with your broker.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>Document gathering (Day 1-3)</strong> — payslips, bank statements, KiwiSaver, ID. The client controls this stage; speed of submission directly affects total turnaround.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>Broker file build (Day 3-5)</strong> — Finch lender-matches your scenario, drafts the credit submission, and pre-flights the file.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>Pre-approval assessment (Day 5-10)</strong> — lender's credit team assesses. Conditional pre-approval issued.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>House hunting (variable)</strong> — pre-approval is valid 90 days; rate locks available.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>Offer accepted &amp; full assessment (Day 1-7 post-offer)</strong> — valuation ordered, conditions cleared, full unconditional approval issued.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>Loan documents &amp; solicitor (Week 2-4)</strong> — sign documents, solicitor coordination with LINZ.</li>
                  <li style=\"margin-bottom:0.75rem;\"><strong>Settlement day</strong> — funds transferred, title registered, keys collected.</li>
                </ol>
            """)),
            ("Approval Speed by NZ Lender", "<p style=\"margin-bottom:2rem;\">Lender-specific turnaround varies week to week and depends heavily on credit team workload. As a general 2026 guide: <strong>ANZ and ASB</strong> are usually the fastest for clean PAYE files (4-7 working days to pre-approval); <strong>BNZ and Westpac</strong> are typically 7-10 days; <strong>Kiwibank, TSB, SBS, The Co-operative Bank</strong> run 7-12 days. Specialist non-banks (<strong>Resimac, Pepper Money, Avanti, Liberty</strong>) often pre-approve within 5-7 working days because their broker channel teams are more streamlined.</p>"),
            ("What Slows NZ Mortgage Approvals Down", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>CCCFA living-expense mismatches</strong> — by far the most common cause of delay. If your declared expenses don't match your 90-day statements, the bank queries.</li><li style=\"margin-bottom:0.5rem;\"><strong>Incomplete document packs</strong> — missing one bank statement, no KiwiSaver summary, or expired employment letter resets the clock.</li><li style=\"margin-bottom:0.5rem;\"><strong>Variable income</strong> — bonuses, commissions, contract income, overtime all require 2-year averaging.</li><li style=\"margin-bottom:0.5rem;\"><strong>Recent credit enquiries</strong> — multiple recent applications, BNPL accounts, or recent personal loans need explaining.</li><li style=\"margin-bottom:0.5rem;\"><strong>Self-employed without finalised financials</strong> — 1-year financials require specialist or non-bank lending.</li><li style=\"margin-bottom:0.5rem;\"><strong>Complex property</strong> — leasehold, cross-lease, body corporate complexities, leaky-home risk all require extra valuation and legal time.</li></ul>"),
            ("How to Speed Up Your NZ Mortgage Approval", "<p style=\"margin-bottom:1rem;\">Practical accelerators we recommend to every Finch client:</p><ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\">Gather all documents <strong>before</strong> the first lender conversation, not during.</li><li style=\"margin-bottom:0.5rem;\">Clean up 90 days of spending statements ahead of CCCFA scrutiny.</li><li style=\"margin-bottom:0.5rem;\">Close unused credit cards (the limit, not the balance, reduces your borrowing power).</li><li style=\"margin-bottom:0.5rem;\">Pay down or close BNPL accounts (Afterpay, Laybuy, Zip).</li><li style=\"margin-bottom:0.5rem;\">Have your accountant pre-prepare current-year financials if self-employed.</li><li style=\"margin-bottom:0.5rem;\">Submit through a broker — Finch knows each lender's credit pipeline state and can route your file to the fastest desk.</li></ul>"),
            ("After Settlement: Ongoing Reviews", "<p style=\"margin-bottom:1rem;\">Your mortgage isn't a set-and-forget — every fixed-term roll-off is an opportunity to refinance for a sharper rate plus cashback contribution. Use our <a href=\"../calculators/refinance-savings.html\" style=\"color:var(--finch-forest);text-decoration:underline;font-weight:600;\">refinance savings calculator</a> at each roll-off, and book a free review with Finch annually.</p>"),
        ],
    },
    {
        "slug": "how-much-can-i-borrow-100k-salary-nz",
        "title": "How Much Can I Borrow on $100k Salary in NZ? (2026)",
        "h1": "How Much Can I Borrow on a $100k Salary in NZ?",
        "intro_pull": "On a $100k NZ salary, your borrowing capacity in 2026 sits between approximately $480k and $680k — and the spread between lenders is bigger than most buyers realise.",
        "description": "How much you can borrow on a $100k NZ salary in 2026 — comparing test rates, living expenses, and lender scorecards across ANZ, ASB, BNZ, Westpac, Kiwibank, and non-banks.",
        "keywords": [
            "how much can I borrow 100k salary NZ",
            "$100k salary mortgage NZ",
            "NZ borrowing power 100k",
            "borrowing power calculator NZ",
            "NZ mortgage on 100000 salary",
            "how much home loan 100k income NZ",
        ],
        "sections": [
            ("The Ballpark Numbers", "<p style=\"margin-bottom:2rem;\">A single applicant earning $100,000 gross in NZ with average living expenses, no other debts, and a clean credit file can typically borrow between <strong>$480,000 and $680,000</strong> in 2026. The exact figure depends on which lender's test rate is applied, how their CCCFA living-expense calculation lands, what your credit card limits look like, and whether you have student loan, hire purchase, or BNPL commitments. Couples earning $200k combined typically borrow $950k-$1.35m on the same logic.</p>"),
            ("Why Different NZ Lenders Quote Very Different Numbers", "<p style=\"margin-bottom:2rem;\">It's normal for ANZ to quote $620k while BNZ quotes $720k to the same applicant. The drivers:</p><ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Test rate</strong> — each lender uses a different stress-test rate (7.0%-9.0% range in 2026). Lower test rate = higher borrowing capacity.</li><li style=\"margin-bottom:0.5rem;\"><strong>Living expense floor</strong> — each lender applies a different minimum living-expense figure. Some use $1,400/month for a single applicant, others $1,800/month.</li><li style=\"margin-bottom:0.5rem;\"><strong>Credit card limit treatment</strong> — banks calculate serviceability against the <em>limit</em>, not the balance, but the % applied varies (3% to 4% of limit per month is common).</li><li style=\"margin-bottom:0.5rem;\"><strong>Non-base income shading</strong> — bonuses, overtime, commissions are typically counted at 70-100% of recent history; rental income at 70-80%.</li></ul>"),
            ("Lender-by-Lender Estimate on $100k Salary", "<p style=\"margin-bottom:2rem;\">As a 2026 guide (clean credit, no other debts, single applicant, 20% deposit assumed): <strong>ANZ</strong> ~$580-620k, <strong>ASB</strong> ~$570-610k, <strong>BNZ</strong> ~$620-680k, <strong>Westpac</strong> ~$580-630k, <strong>Kiwibank</strong> ~$560-600k, <strong>TSB / SBS / Co-operative Bank</strong> ~$540-600k. Specialist non-banks vary more widely. These are estimates only — Finch produces lender-specific quotes free of charge based on your real income and expenses.</p>"),
            ("How to Maximise Your $100k Salary Borrowing Power", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Close unused credit cards</strong> — every $5,000 of credit card limit reduces borrowing power by ~$25,000.</li><li style=\"margin-bottom:0.5rem;\"><strong>Pay off / close BNPL accounts</strong> — Afterpay, Laybuy, Zip, Klarna all reduce capacity.</li><li style=\"margin-bottom:0.5rem;\"><strong>Pay down personal loans &amp; hire purchase</strong> — these are deducted at full minimum repayment.</li><li style=\"margin-bottom:0.5rem;\"><strong>Clean up 90 days of spending</strong> — CCCFA scrutiny is intense; reduce restaurants, BNPL, Uber, streaming subs.</li><li style=\"margin-bottom:0.5rem;\"><strong>Verify all income sources</strong> — bonuses, secondary income, Working for Families, Best Start, rental income.</li><li style=\"margin-bottom:0.5rem;\"><strong>Use a broker</strong> — Finch matches you to the most generous lender for your specific profile.</li></ul>"),
            ("Couple Earning $200k vs Single on $100k", "<p style=\"margin-bottom:2rem;\">A couple on $200k combined borrows materially more than 2x a single on $100k, because the second applicant's expenses are shared. Typical couple capacity on $200k combined: $950k-$1.35m. The exact number depends on whether income is split evenly (highest capacity), or skewed (slightly lower due to KiwiSaver and PAYE banding).</p>"),
            ("Try the Calculator, Then Get a Real Quote", "<p style=\"margin-bottom:1rem;\">Use our <a href=\"../calculators/borrowing-power.html\" style=\"color:var(--finch-forest);text-decoration:underline;font-weight:600;\">NZ borrowing power calculator</a> for a quick ballpark, then book a free 15-minute call for a lender-specific figure. A real broker assessment takes about 20 minutes and is accurate within $5,000.</p>"),
        ],
    },
    {
        "slug": "mortgage-broker-vs-bank-nz",
        "title": "Mortgage Broker vs Bank in NZ — Which Is Better? (2026)",
        "h1": "Mortgage Broker vs Bank in NZ — Which is Better?",
        "intro_pull": "Going direct to your own bank limits you to one set of rates and one credit scorecard. A broker compares 20+ NZ lenders for free.",
        "description": "Mortgage broker vs bank in NZ — full 2026 comparison. Costs, lender access, approval rates, and which path delivers a sharper rate and faster approval.",
        "keywords": [
            "mortgage broker vs bank NZ",
            "use mortgage broker or bank NZ",
            "should I use a mortgage broker NZ",
            "broker or bank for mortgage NZ",
            "NZ mortgage broker comparison",
            "mortgage broker benefits NZ",
        ],
        "sections": [
            ("The Core Difference", "<p style=\"margin-bottom:2rem;\">Walking into your own bank gives you access to that bank's rates, scorecard, and product range — nothing more. A New Zealand mortgage broker (like Finch) compares your scenario across the full panel of <strong>ANZ, ASB, BNZ, Westpac, Kiwibank, TSB, SBS, The Co-operative Bank, Heartland</strong>, plus the specialist non-bank market (<strong>Resimac, Pepper Money, Avanti, Liberty, Basecorp, Bluestone</strong>). Because every lender's pricing, test rate, and credit appetite differs week to week, the spread between best and worst offer for the same client is usually <strong>0.30-0.60 percentage points</strong> — equivalent to $1,500-$3,000 of saving per year on a $500,000 loan.</p>"),
            ("Cost — Are NZ Mortgage Brokers Free?", "<p style=\"margin-bottom:2rem;\">For residential home loans, NZ mortgage brokers charge you <strong>$0</strong>. The lender pays the broker on settlement out of its distribution budget — money that would otherwise stay with the bank if you walked in direct. The broker fee does not increase your interest rate or fees; it's part of the lender's existing cost-of-acquisition. (Commercial and complex specialist loans sometimes do carry a broker fee disclosed up front.)</p>"),
            ("What a Mortgage Broker Does Better Than a Bank", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Lender comparison</strong> — every NZ bank's live policy + 6+ non-bank lenders in one assessment.</li><li style=\"margin-bottom:0.5rem;\"><strong>Pre-approval routing</strong> — broker knows which lender's credit team is currently fastest and most receptive.</li><li style=\"margin-bottom:0.5rem;\"><strong>Cashback negotiation</strong> — brokers actively negotiate cashback contributions; bank mobile managers often don't.</li><li style=\"margin-bottom:0.5rem;\"><strong>Complex scenarios</strong> — self-employed, low-deposit, credit-impaired, investor structures all benefit from broker-channel routing.</li><li style=\"margin-bottom:0.5rem;\"><strong>Ongoing reviews</strong> — brokers re-review at every fixed-term roll-off; bank staff usually don't proactively suggest moving.</li><li style=\"margin-bottom:0.5rem;\"><strong>Best-interest duty</strong> — registered NZ brokers are legally required to act in your best interest under the Financial Markets Conduct Act. Bank staff act in the bank's interest.</li></ul>"),
            ("What a Bank Does Better Than a Broker", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>If you already bank with them</strong> and your full financial relationship sits there, occasionally a relationship-based pricing exception will beat broker pricing.</li><li style=\"margin-bottom:0.5rem;\"><strong>Simple top-ups</strong> on an existing loan don't usually require broker involvement.</li><li style=\"margin-bottom:0.5rem;\"><strong>Branch network</strong> — banks have physical offices for in-person discussions (most brokers use phone, video, or office visits).</li></ul><p style=\"margin-bottom:2rem;\">Best practice: use both. Let your bank quote you first, then send the offer to a broker. The broker compares it across 20+ lenders and tells you honestly whether to stay or move.</p>"),
            ("Common Myths About NZ Mortgage Brokers", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>\"Brokers add to the cost.\"</strong> False. Lender pays, not you.</li><li style=\"margin-bottom:0.5rem;\"><strong>\"Brokers push you to the highest-paying lender.\"</strong> False. NZ regulation requires brokers to act in your best interest; conflict disclosures are mandatory.</li><li style=\"margin-bottom:0.5rem;\"><strong>\"Going direct to my bank gets a sharper deal.\"</strong> Usually false. Banks reserve their sharpest rates for new business sourced through brokers.</li><li style=\"margin-bottom:0.5rem;\"><strong>\"Brokers slow down approval.\"</strong> False. Brokers route to the fastest-decisioning credit team and prepare the file properly first time.</li></ul>"),
            ("How to Choose an NZ Mortgage Broker", "<p style=\"margin-bottom:1rem;\">Look for:</p><ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\">FSP-registered with a current FSPR listing (search fsp-register.companiesoffice.govt.nz)</li><li style=\"margin-bottom:0.5rem;\">Member of Financial Advice NZ or equivalent industry body</li><li style=\"margin-bottom:0.5rem;\">Panel of 15+ NZ lenders (not just 2-3 banks)</li><li style=\"margin-bottom:0.5rem;\">Clear disclosure of how they're paid (the lender, not you, for residential)</li><li style=\"margin-bottom:0.5rem;\">Independent of any single bank's ownership</li><li style=\"margin-bottom:0.5rem;\">Real client reviews on Google</li></ul><p style=\"margin-bottom:1rem;\">Finch is FSP1011206 / FSPR FSP1011125, independent, and works with 20+ NZ lenders.</p>"),
        ],
    },
    {
        "slug": "what-is-lvr-nz-mortgage",
        "title": "What is LVR in NZ? Loan-to-Value Ratio Explained for 2026",
        "h1": "What is LVR (Loan-to-Value Ratio) in NZ?",
        "intro_pull": "LVR is the ratio of your loan to the property's value — and it determines which NZ bank will lend to you, at which rate tier, with which conditions.",
        "description": "What is LVR in NZ mortgages? Full 2026 guide to Loan-to-Value Ratio, RBNZ speed limits, LVR tier pricing, and how to drop LVR bands to unlock sharper rates.",
        "keywords": [
            "what is LVR NZ",
            "loan to value ratio NZ",
            "LVR meaning NZ mortgage",
            "RBNZ LVR speed limit",
            "high LVR mortgage NZ",
            "LVR tier pricing NZ",
            "NZ LVR rules",
        ],
        "sections": [
            ("LVR Defined", "<p style=\"margin-bottom:2rem;\">Loan-to-Value Ratio (LVR) = loan amount ÷ property value, expressed as a percentage. If you're buying a $800,000 property and borrowing $640,000, your LVR is 80%. The lower your LVR, the lower the lender's risk — and the sharper the interest rate they'll offer. The Reserve Bank of New Zealand (RBNZ) sets LVR \"speed limits\" that cap how much new lending each bank can write above certain LVR thresholds.</p>"),
            ("Current RBNZ LVR Speed Limits (2026)", "<p style=\"margin-bottom:1rem;\">As of 2026:</p><ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Owner-occupier:</strong> maximum 20% of a bank's new lending can be above 80% LVR (i.e. with less than 20% deposit).</li><li style=\"margin-bottom:0.5rem;\"><strong>Investor:</strong> maximum 5% of a bank's new lending can be above 70% LVR (i.e. with less than 30% deposit).</li><li style=\"margin-bottom:0.5rem;\"><strong>New builds:</strong> exempt from LVR speed limits — banks can lend to new-build buyers at 90% LVR or even 95% LVR.</li><li style=\"margin-bottom:0.5rem;\"><strong>Kāinga Ora First Home Loan:</strong> exempt from main-bank speed limits — accepts 5% deposit.</li></ul>"),
            ("How LVR Tiers Affect NZ Mortgage Rates", "<p style=\"margin-bottom:2rem;\">Every NZ bank prices in tiers based on LVR. The sharpest carded rates are reserved for borrowers below 80% LVR (\"standard\" pricing). Borrowers above 80% LVR pay a \"Low Equity Premium\" or LEM/LEP — typically an additional 0.25%-1.20% on the rate. Banks set their LEPs differently — ASB and Westpac structure them as a margin on the rate; ANZ and BNZ structure them as a one-off fee. Either way, dropping below 80% LVR is the single biggest rate-saving lever a NZ homeowner has.</p>"),
            ("How to Drop an LVR Band (Practical NZ Tactics)", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Wait for property growth</strong> — if your property has appreciated since purchase, request a registered valuation. A higher value drops your LVR without you contributing more deposit.</li><li style=\"margin-bottom:0.5rem;\"><strong>Lump-sum extra repayment</strong> — paying down the loan principal lowers your LVR directly.</li><li style=\"margin-bottom:0.5rem;\"><strong>Refinance at the band crossing</strong> — when you cross from above-80% to below-80%, refinance to capture the standard-tier pricing (often with cashback contribution too).</li><li style=\"margin-bottom:0.5rem;\"><strong>Family guarantee</strong> — a family member's equity contribution can effectively reduce your LVR.</li><li style=\"margin-bottom:0.5rem;\"><strong>Combine with renovation</strong> — strategic improvements that increase the registered valuation can drop you a band.</li></ul>"),
            ("Special NZ LVR Pathways", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>New build LVR exemption</strong> — buyers of new builds can typically borrow at 85-90% LVR without speed-limit restriction.</li><li style=\"margin-bottom:0.5rem;\"><strong>Kāinga Ora First Home Loan</strong> — 5% deposit (95% LVR) accepted through Westpac, Kiwibank, SBS, The Co-operative Bank.</li><li style=\"margin-bottom:0.5rem;\"><strong>Specialist non-bank lenders</strong> — some accept 85-90% LVR for owner-occupiers (at a yield premium) without the main-bank speed-limit constraint.</li></ul>"),
            ("LVR in Plain English — Worked NZ Example", "<p style=\"margin-bottom:1rem;\">You're buying a $750,000 property with a $150,000 deposit. Your loan is $600,000. LVR = 600,000 ÷ 750,000 = <strong>80%</strong>. You qualify for standard carded rates from any main NZ bank. Three years later, the property is valued at $850,000, but your loan has paid down to $560,000. New LVR = 560,000 ÷ 850,000 = <strong>65.9%</strong>. You're now in a lower-risk tier — refinance to capture sharper pricing and any available cashback. Run the numbers in our <a href=\"../calculators/refinance-savings.html\" style=\"color:var(--finch-forest);text-decoration:underline;font-weight:600;\">refinance savings calculator</a>.</p>"),
        ],
    },
    {
        "slug": "mortgage-broker-fees-nz",
        "title": "Mortgage Broker Fees in NZ — Are Brokers Really Free? (2026)",
        "h1": "Mortgage Broker Fees in NZ — Are They Really Free?",
        "intro_pull": "For residential home loans in New Zealand, mortgage brokers don't charge you a fee — the lender pays them on settlement. Here's exactly how it works.",
        "description": "Are NZ mortgage brokers free? Full 2026 explanation of how brokers get paid, when fees apply, conflict-of-interest disclosures, and what to ask before signing up.",
        "keywords": [
            "mortgage broker fees NZ",
            "are mortgage brokers free NZ",
            "NZ mortgage broker cost",
            "how do mortgage brokers get paid NZ",
            "mortgage broker commission NZ",
            "broker fee disclosure NZ",
        ],
        "sections": [
            ("The Short Answer", "<p style=\"margin-bottom:2rem;\">For <strong>residential home loans</strong> in NZ, mortgage brokers like Finch typically charge you <strong>$0</strong>. The lender pays the broker a commission on settlement out of its distribution budget. That commission would otherwise stay with the bank if you walked in direct. It does <strong>not</strong> increase your interest rate, your loan fees, or your settlement costs. Commercial loans, complex specialist deals, and some non-bank scenarios may carry a disclosed broker fee — your broker is required to disclose this upfront in writing.</p>"),
            ("How NZ Mortgage Broker Commissions Work", "<p style=\"margin-bottom:1rem;\">The structure most main NZ banks use:</p><ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Upfront commission</strong> — typically 0.55% to 0.85% of the loan amount, paid to the broker on settlement. On a $600,000 loan that's $3,300-$5,100.</li><li style=\"margin-bottom:0.5rem;\"><strong>Trail commission</strong> — typically 0.15% to 0.20% per year of the outstanding loan balance, paid quarterly while the loan remains with the lender. On a $600,000 loan that's $900-$1,200/year.</li><li style=\"margin-bottom:0.5rem;\"><strong>Clawback</strong> — if the loan discharges within 2-3 years, the broker repays a portion of the upfront commission back to the lender.</li></ul>"),
            ("Who Pays for It in the End?", "<p style=\"margin-bottom:2rem;\">Banks build broker commission into their cost-of-acquisition budget — the same budget that funds branch staff salaries, marketing, and direct-to-consumer cashback campaigns. They don't recover the commission from your interest rate; the broker channel pricing is typically the <em>same</em> or <strong>sharper</strong> than the carded direct-to-consumer rate, because banks know broker-introduced borrowers are price-conscious. The broker's commission funds the broker's role in saving you the bank's customer-acquisition effort.</p>"),
            ("When NZ Brokers DO Charge a Fee", "<ul style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:disc;\"><li style=\"margin-bottom:0.5rem;\"><strong>Commercial property loans</strong> — typically 0.50%-1.00% of the loan, disclosed up front.</li><li style=\"margin-bottom:0.5rem;\"><strong>Asset finance / equipment finance</strong> — some specialist scenarios carry a small broker fee.</li><li style=\"margin-bottom:0.5rem;\"><strong>Highly complex specialist residential</strong> — extremely rare; disclosed before engagement.</li><li style=\"margin-bottom:0.5rem;\"><strong>Bridging finance</strong> — sometimes a small fee applies to the bridging facility itself.</li></ul><p style=\"margin-bottom:2rem;\">Any broker fee on a residential home loan must be disclosed in writing under the Financial Markets Conduct Act. Walk away from any broker who isn't transparent about how they're paid.</p>"),
            ("Conflict of Interest Disclosures", "<p style=\"margin-bottom:2rem;\">Under NZ regulation, brokers must disclose any conflict of interest before recommending a lender. The most common conflict to look for: brokers owned by a single bank (rare in NZ but exists). Independent brokers like Finch are not owned by any lender and our recommendations are not biased by ownership. Commission differences between lenders are also disclosed — and where two lenders offer similar value, the regulator expects the broker to recommend the one in your best interest, not the one paying highest commission.</p>"),
            ("Questions to Ask Before Signing Up With Any NZ Broker", "<ol style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:decimal;\"><li style=\"margin-bottom:0.5rem;\">Are you FSP-registered? (Verify on fsp-register.companiesoffice.govt.nz)</li><li style=\"margin-bottom:0.5rem;\">How many lenders are on your panel?</li><li style=\"margin-bottom:0.5rem;\">Who pays you, and at what rates?</li><li style=\"margin-bottom:0.5rem;\">Will you charge me directly for any reason?</li><li style=\"margin-bottom:0.5rem;\">Are you owned by or contracted to any single bank?</li><li style=\"margin-bottom:0.5rem;\">Can I see your written disclosure document?</li></ol><p style=\"margin-bottom:1rem;\">Finch is FSP1011206 / FSPR FSP1011125, independent, with a 20+ lender panel, and charges $0 on residential home loans.</p>"),
        ],
    },
    {
        "slug": "how-to-choose-mortgage-broker-nz",
        "title": "How to Choose a Mortgage Broker in NZ — Complete 2026 Guide",
        "h1": "How to Choose a Mortgage Broker in NZ",
        "intro_pull": "Choosing the right NZ mortgage broker matters because your broker decides which lender sees your file first, how it's pitched, and whether you capture the sharpest rate available.",
        "description": "How to choose a mortgage broker in NZ — what to verify, red flags to avoid, FSP register lookup, panel size, fee transparency, and the 10 questions to ask before engaging.",
        "keywords": [
            "how to choose a mortgage broker NZ",
            "best mortgage broker NZ",
            "find mortgage broker NZ",
            "questions to ask mortgage broker NZ",
            "NZ mortgage broker checklist",
            "trustworthy NZ broker",
        ],
        "sections": [
            ("Why Broker Choice Matters", "<p style=\"margin-bottom:2rem;\">A good NZ mortgage broker gets your file to the lender most likely to approve at the sharpest rate, prepares the credit submission so it lands first time, negotiates cashback contributions, and stays with you through ongoing fixed-term reviews. A poor broker copies your file across 2-3 lenders, doesn't pre-flight CCCFA living-expense issues, and disappears after settlement. The skill gap between good and average broker is larger than most clients realise.</p>"),
            ("Step 1 — Verify FSP Registration", "<p style=\"margin-bottom:2rem;\">Every NZ mortgage broker must be registered with the Financial Service Providers Register (FSPR). Search by name at <strong>fsp-register.companiesoffice.govt.nz</strong>. The registration confirms the broker is licensed to give regulated financial advice, has met the relevant qualification standards (typically Level 5 Certificate in Financial Services or equivalent), and is subject to NZ regulatory oversight. Finch's registration: FSP1011206 / FSPR FSP1011125.</p>"),
            ("Step 2 — Check Panel Size", "<p style=\"margin-bottom:2rem;\">Ask how many lenders the broker works with. A serious NZ mortgage broker should have at least 15 lenders on panel — all 5 main NZ banks (ANZ, ASB, BNZ, Westpac, Kiwibank), the major regional/registered banks (TSB, SBS, The Co-operative Bank, Heartland), and a healthy suite of specialist non-banks (Resimac, Pepper Money, Avanti, Liberty, Bluestone, Basecorp). A broker with only 2-3 lenders is functionally a bank salesperson.</p>"),
            ("Step 3 — Confirm Independence", "<p style=\"margin-bottom:2rem;\">Some NZ mortgage \"brokers\" are owned by, or are franchisees of, a specific bank or lender. Their recommendations skew toward their owner-lender. Truly independent brokers (like Finch) are not owned by any lender, are not bound to a single-lender franchise, and are paid only on settlement by whichever lender wins your scenario. Ask directly: \"Are you owned by any bank or lender?\"</p>"),
            ("Step 4 — Review the Disclosure Document", "<p style=\"margin-bottom:2rem;\">NZ brokers are required to provide a written disclosure document before giving regulated advice. It covers their licensing, panel, how they're paid, any conflicts of interest, and dispute resolution. Read it. Any broker who can't produce one is not properly compliant.</p>"),
            ("Step 5 — Check Real Reviews", "<p style=\"margin-bottom:2rem;\">Look at Google Business Profile reviews, Product Review NZ, and NoCowboys finance category. Read both the 5-star and the lower-rated reviews — the lower ones often reveal communication or follow-up issues. Aim for a broker with 20+ recent reviews averaging 4.7+ stars.</p>"),
            ("Step 6 — Test Their First Conversation", "<p style=\"margin-bottom:2rem;\">A good NZ broker spends the first 15-30 minutes <em>listening</em>: your income, your goals, your KiwiSaver, your existing debts. They explain CCCFA, LVR, test rates clearly and tailor the conversation to your level of mortgage knowledge. A poor broker jumps straight to \"send me your documents.\" Trust the first impression.</p>"),
            ("10 Questions to Ask Any NZ Mortgage Broker", "<ol style=\"margin-bottom:2rem;padding-left:1.5rem;list-style:decimal;\"><li style=\"margin-bottom:0.5rem;\">Are you FSP-registered? (Then verify it.)</li><li style=\"margin-bottom:0.5rem;\">How many lenders are on your panel?</li><li style=\"margin-bottom:0.5rem;\">Are you owned by any bank or lender?</li><li style=\"margin-bottom:0.5rem;\">How do you get paid?</li><li style=\"margin-bottom:0.5rem;\">Will you charge me anything directly?</li><li style=\"margin-bottom:0.5rem;\">What's your typical pre-approval turnaround?</li><li style=\"margin-bottom:0.5rem;\">Do you review my mortgage at every fixed-term roll-off?</li><li style=\"margin-bottom:0.5rem;\">Can I speak with a recent client as a reference?</li><li style=\"margin-bottom:0.5rem;\">What's your specialty? (First home, investment, refinance, self-employed)</li><li style=\"margin-bottom:0.5rem;\">Where's your written disclosure document?</li></ol>"),
        ],
    },
]


def keywords_string(post: dict) -> str:
    return ", ".join(post["keywords"])


def schema_for(post: dict) -> str:
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog.html"},
            {"@type": "ListItem", "position": 3, "name": post["h1"], "item": f"{BASE_URL}/blog/{post['slug']}.html"},
        ],
    }
    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "url": f"{BASE_URL}/blog/{post['slug']}.html",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}/blog/{post['slug']}.html"},
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


def main_body(post: dict) -> str:
    sections_html = ""
    for heading, body in post["sections"]:
        sections_html += textwrap.dedent(f"""
            <h2 style=\"font-size:1.6rem;font-weight:700;color:var(--neutral-black);margin-bottom:1rem;margin-top:2.5rem;font-family:var(--font-display);\">{heading}</h2>
            {body}
        """)

    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <section class="container page-hero" style="padding-top:4rem;padding-bottom:4rem;">
      <div class="reveal" style="max-width:800px;">
        <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../blog.html">Blog</a><span class="breadcrumb-sep">/</span><span>{post['h1']}</span></nav>
        <div class="page-hero-tag">NZ Mortgage Guide</div>
        <h1>{post['h1']}</h1>
        <p style="font-size:1.15rem;color:var(--neutral-medGray);line-height:1.7;margin-bottom:1.5rem;font-style:italic;">{post['intro_pull']}</p>
      </div>
    </section>

    <section style="padding:3rem 0;background:var(--finch-mist);">
      <div class="container" style="max-width:800px;">
        <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
          {sections_html}
          <p style="margin-top:2rem;font-size:0.95rem;">Official NZ sources: the <a href="https://www.rbnz.govt.nz/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Reserve Bank of New Zealand</a> for OCR and lending policy, and <a href="https://sorted.org.nz/guides/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Sorted.org.nz</a> for independent, government-backed money guidance.</p>
        </div>
      </div>
    </section>

    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>Keep Reading</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ mortgage resources</h2>
        <div class="cols-3" style="gap:1.5rem;">
          <a href="../services/home-loan.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Home Loan Service</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Independent advice across 20+ NZ lenders.</span></a>
          <a href="../calculators/borrowing-power.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Borrowing Power</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">See how much NZ banks will lend.</span></a>
          <a href="../calculators/mortgage-calculator.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Mortgage Calculator</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Estimate repayments at NZ rates.</span></a>
          <a href="../guides/first-home-guide.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">First Home Buyer Guide</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Complete NZ FHB playbook.</span></a>
          <a href="../mortgage-rates.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Live NZ Mortgage Rates</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Current carded and broker rates.</span></a>
          <a href="../lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Lender Directory</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">All 20+ NZ lenders reviewed.</span></a>
        </div>
      </div>
    </section>

    <section style="padding:5rem 0;">
      <div class="container">
        <div class="cta-section reveal">
          <h2>Talk to a free NZ<br/>mortgage adviser today.</h2>
          <p>Book a free 15-minute consultation. We compare your scenario across 20+ NZ lenders — no cost, no obligation.</p>
          <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
            <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
            <a class="btn-cta-outline" href="../mortgage-rates.html">View Live NZ Rates</a>
          </div>
        </div>
      </div>
    </section>
    </main>
    """)


def build_page(post: dict, template_text: str) -> str:
    head_close = template_text.find("</head>")
    head = template_text[:head_close]

    title = post["title"]
    description = post["description"]
    canonical = f"{BASE_URL}/blog/{post['slug']}.html"
    keywords = keywords_string(post)
    schema = schema_for(post)

    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"description\"/?>',
        f'<meta content="{description}" name="description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<link href=\"https://www\.finchmortgages\.co\.nz/blog/[^\"]+\" rel=\"canonical\"/?>',
        f'<link href="{canonical}" rel="canonical"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"keywords\"/?>',
        f'<meta content="{keywords}" name="keywords"/>',
        head,
    )
    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        lambda _m: schema,
        head,
        count=1,
        flags=re.S,
    )
    head += "</head>"

    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]

    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]

    return head + "\n" + body_open + main_body(post) + footer


def main() -> None:
    template_text = TEMPLATE.read_text(encoding="utf-8")
    for post in POSTS:
        out_path = OUT_DIR / f"{post['slug']}.html"
        out_path.write_text(build_page(post, template_text), encoding="utf-8")
        print(f"  + {out_path.relative_to(ROOT)}")
    print(f"\nGenerated {len(POSTS)} blog posts.")


if __name__ == "__main__":
    main()
