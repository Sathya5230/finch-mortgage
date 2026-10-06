#!/usr/bin/env python3
"""Refinance posts for generate_local_intent_blogs.py.

Fills refinance gaps not covered by services/refinance.html, guides/refinance-guide.html
and the refix / break-fee / cashback / top-up posts: a "Finch refinance" brand page,
separation buy-outs, being declined by a new lender, and rental portfolios.

Same content rules as local_intent_posts.py: explain mechanisms, never invent
rates, named lender policies or approval odds.

Run:  python3 generate_local_intent_blogs.py refinance_posts
"""

from generate_local_intent_blogs import callout, link, ol, p, table, ul

PUBLISHED = "2026-10-06"

REL_REFI = [
    ("../services/refinance.html", "Refinance Your Mortgage",
     "Independent refinance advice across 20+ NZ lenders."),
    ("../calculators/refinance-savings.html", "Refinance Savings Calculator",
     "Estimate what switching could save."),
    ("../guides/refinance-guide.html", "NZ Refinance Guide",
     "Step-by-step: when and how to refinance."),
]

RBNZ_LVR = "https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions"

POSTS = [
    {
        "slug": "finch-refinance-mortgage-review-nz",
        "published": PUBLISHED,
        "title": "Refinance with Finch | Free NZ Mortgage Review | Finch",
        "h1": "Refinancing with Finch: How Our Free Mortgage Review Works",
        "section_label": "Finch Refinance",
        "region": "",
        "lead_service": "Refinance",
        "about": ["Finch Mortgages", "Mortgage refinancing", "Mortgage review", "New Zealand home loans"],
        "intro_pull": "Thinking of refinancing with Finch? Here's exactly what we check, what it costs you, how long it takes — and when we'll tell you that staying with your current bank is the better move.",
        "description": "Refinancing with Finch: what our free NZ mortgage review checks, the real costs of switching, how long it takes, and when staying with your bank wins.",
        "keywords": [
            "Finch refinance",
            "Finch refinancing",
            "refinance mortgage NZ",
            "mortgage review NZ",
            "refinance broker NZ",
            "switch mortgage lender NZ",
        ],
        "cta_heading": "Want a free review of your mortgage?",
        "cta_sub": "Tell us your lender, loan balance and when your fixed terms end. We'll show you whether refinancing, refixing or restructuring makes the most sense.",
        "sections": [
            ("Refinancing doesn't always mean switching banks", (
                p("When people contact Finch about refinancing, they usually expect us to move them to a new bank. Sometimes that's right. Often the better result is a sharper offer from the bank you're already with, or a better structure for the loan you already have. Our review compares all three options and recommends whichever leaves you better off after costs.")
                + table(
                    ["Option", "What it means", "When it tends to win"],
                    [
                        ["Refix with your current lender", "Stay put, and negotiate the rate and structure for your next fixed term.", "Your bank matches the market and there's no reason to move."],
                        ["Restructure", "Same lender, different set-up: splits, offset or revolving credit, loan term, or interest-only on rentals.", "The rate is fine but the structure isn't working for you."],
                        ["Refinance to a new lender", "Move the loan to a different lender.", "A better rate, cashback, or policy fit that outweighs the costs of moving."],
                    ],
                )
            )),
            ("What we check in a refinance review", (
                ul([
                    "<strong>Your current rates and fixed-term end dates.</strong> Each part of a split loan has its own end date, and the best time to move is usually when a fixed term ends.",
                    "<strong>Break costs.</strong> If you're partway through a fixed term, we get the actual break-fee quote from your bank rather than guessing. See " + link("break-fixed-mortgage-break-fees-nz.html", "how break fees work") + ".",
                    "<strong>Cashback clawback.</strong> If your current lender paid you a cashback, leaving within the agreed period usually means repaying some or all of it. We check your loan documents.",
                    "<strong>What new lenders will offer you.</strong> Rate, cashback or legal contribution, and whether their lending policy fits your income and property today — not just when you first borrowed.",
                    "<strong>Structure.</strong> Whether your fixed and floating split, offset or revolving credit, and loan term still suit your plans.",
                    "<strong>Your goals.</strong> Paying it off faster, freeing up cash flow, renovating, investing or consolidating debt all point to different structures.",
                ])
            )),
            ("The real cost of switching", (
                p("Refinancing is only worth it if what you save is more than what it costs to move. The costs to weigh up:")
                + ul([
                    "<strong>Break fees</strong> on any fixed portion you leave early.",
                    "<strong>Cashback clawback</strong> from your current lender, if you're still inside their minimum period.",
                    "<strong>Discharge fee</strong> charged by your current lender to release its mortgage.",
                    "<strong>Legal fees</strong> for the new mortgage. Many lenders contribute to these, or offer a cashback that covers them.",
                    "<strong>Valuation</strong>, if the new lender needs one.",
                ])
                + p("Against those, count the interest saved over the period you'd realistically stay, plus any new cashback. Our " + link("../calculators/refinance-savings.html", "refinance savings calculator") + " helps you check the numbers.")
                + callout("When we'll tell you not to switch", "If the savings don't clearly beat the costs, or your bank offers a competitive retention rate once we've shown them what the market is offering, we'll recommend staying. There's no fee for the review, and we'd rather you stay with your bank than make a move that doesn't pay off.")
            )),
            ("How long it takes", (
                ol([
                    "<strong>Review call</strong> — about 15 minutes. We collect your current loan details and goals.",
                    "<strong>Documents</strong> — recent payslips or financial statements, bank statements and your current loan statement.",
                    "<strong>Recommendation</strong> — we compare refixing, restructuring and refinancing, with the costs set out.",
                    "<strong>Approval</strong> — if moving makes sense, we apply to the lender that suits you best.",
                    "<strong>Settlement</strong> — your solicitor handles the switch. We time it for when your fixed term ends wherever possible, to avoid break fees.",
                ])
                + p("The best time to start is about 60–90 days before a fixed term ends. That gives enough time to compare options without a deadline forcing your hand. Our " + link("fixed-rate-ending-refix-guide-nz.html", "refix playbook") + " covers the timeline in detail.")
            )),
        ],
        "faqs": [
            ("Does Finch charge a fee to refinance my mortgage?",
             "Not for standard residential refinancing. The new lender pays our commission when the loan settles. If we recommend staying with your current bank, the review is still free."),
            ("Can Finch get me a better rate from my current bank?",
             "Often, yes. Many banks have a retention team that can match competitive offers. Showing them what other lenders would offer gives you leverage, even if you don't move."),
            ("When is the best time to refinance?",
             "Usually when a fixed term is ending, because there's no break fee. Start comparing 60 to 90 days beforehand. Refinancing partway through a fixed term can still be worth it, but only if the savings outweigh the break fee."),
            ("Will refinancing affect my credit score?",
             "Applying for credit leaves an enquiry on your credit file, and multiple applications in a short time can count against you. We assess which lenders suit you before applying, so you avoid applications that are likely to be declined."),
        ],
        "faq_heading": "Refinancing with Finch: common questions",
        "related": REL_REFI,
    },

    {
        "slug": "refinance-after-separation-buy-out-partner-nz",
        "published": PUBLISHED,
        "title": "Refinance After Separation NZ: Buying Out a Partner | Finch",
        "h1": "Refinancing After a Separation: Buying Out Your Partner's Share",
        "section_label": "Refinance",
        "region": "",
        "lead_service": "Refinance",
        "about": ["Refinancing", "Separation", "Relationship property", "Home loans"],
        "intro_pull": "Keeping the house after a separation usually means refinancing the mortgage into your name alone and paying out your former partner's share. Here's how NZ lenders assess it, and the order to do things in.",
        "description": "How to refinance after a separation in NZ: buying out a partner's share, what lenders need, counting child support, and the relationship property agreement.",
        "keywords": [
            "refinance after separation NZ",
            "buy out partner mortgage NZ",
            "keep the house after separation NZ",
            "remove name from mortgage NZ",
            "relationship property home loan NZ",
            "divorce refinance NZ",
        ],
        "cta_heading": "Want to keep the house?",
        "cta_sub": "Tell us the property value, the current mortgage and roughly what you'd need to pay out. We'll tell you confidentially whether the numbers are likely to work, before you commit to anything.",
        "sections": [
            ("What 'buying out' actually involves", (
                p("When a couple who own a home together separate and one person wants to keep it, three things usually happen at once: the departing partner's share is paid out, their name comes off the title, and they're released from the mortgage. The remaining owner then has to carry the whole loan on their own income.")
                + p("Paying out the share is usually funded by increasing the mortgage. For example, on a $900,000 home with a $500,000 mortgage, there's $400,000 of equity. If it's split equally, the person keeping the home needs to borrow enough to repay the $500,000 and pay out $200,000 — a $700,000 loan, on one income.")
                + callout("The lender can't remove one name on its own", "Taking a borrower off a joint mortgage needs the lender's consent, and the lender will only agree if the remaining borrower can service the whole loan alone. If your current lender says no, another lender may say yes, so it's worth comparing.")
            )),
            ("Relationship property comes first", (
                p("In New Zealand, the " + link("https://www.justice.govt.nz/family/", "Property (Relationships) Act 1976") + " generally presumes that relationship property, including the family home, is shared equally once a relationship has lasted three years or more. There are exceptions, and how your property is divided is a legal question for your lawyers, not your mortgage adviser.")
                + p("What matters for the refinance is that lenders want to see the agreed split in writing. For an agreement under the Act to be binding, each person generally needs independent legal advice and the agreement must be signed and witnessed in line with the Act's requirements. Most lenders want to see the signed agreement, or at least a solicitor's confirmation of the terms, before they approve the final loan.")
            )),
            ("How lenders assess you as a single borrower", (
                ul([
                    "<strong>Income.</strong> Your income now has to cover the full loan on its own, tested at the lender's assessment rate rather than today's rate.",
                    "<strong>Child support and Working for Families.</strong> Some lenders count child support you receive, and Working for Families tax credits, as income, usually with evidence that payments are regular. Others count them partially or not at all. This is one of the biggest differences between lenders for separating parents.",
                    "<strong>Child support you pay.</strong> If you pay child support, lenders treat it as an ongoing expense.",
                    "<strong>Your new budget.</strong> Expenses for one household on one income are reassessed from scratch.",
                    "<strong>Loan-to-value ratio.</strong> Borrowing to pay out a share increases the loan against the same property. If it pushes the loan above 80% of the home's value, fewer lenders will consider it and the cost of borrowing may rise.",
                    "<strong>Debt-to-income ratio.</strong> The larger single-income loan is assessed against the Reserve Bank's DTI settings and the lender's own limits.",
                ])
            )),
            ("The order that avoids problems", (
                ol([
                    "<strong>Get an early read on what you can borrow</strong> — before you agree a payout figure. There's no point agreeing to buy out your partner if you can't fund it.",
                    "<strong>Agree the split with legal advice on both sides</strong>, and put it in writing.",
                    "<strong>Get the property valued.</strong> Many lenders will need a registered valuation, and it also supports the payout figure.",
                    "<strong>Apply for the refinance</strong>, with the signed agreement and your updated income and expense documents.",
                    "<strong>Settle.</strong> Your solicitor repays the joint loan, pays your former partner their share and arranges the title transfer.",
                ])
                + p("If the numbers don't work on one income, a " + link("co-owning-home-friends-family-nz.html", "family guarantee or co-ownership") + " arrangement, or a lender with a broader view of your income, may make a difference.")
            )),
            ("If you can't keep the house", (
                p("Sometimes the right answer is to sell and split the proceeds. That's often easier on both of you than one person stretching to take on a loan they'll struggle to afford. If you're selling, check break fees and any cashback clawback on the existing loan, and plan your next purchase so your share of the proceeds becomes your deposit.")
                + p("Whatever you decide, we can show you confidentially what you could borrow on your own, so you can negotiate knowing the numbers.")
            )),
        ],
        "faqs": [
            ("Can I take my ex-partner's name off our mortgage?",
             "Only with the lender's consent, and only if you can service the full loan on your own. The lender reassesses you as a single borrower. If your current lender won't agree, refinancing to another lender is often an option."),
            ("Do lenders count child support as income in NZ?",
             "Some do, usually with evidence that payments are regular, for example an Inland Revenue statement. Others count it partially or not at all. Lender policy varies a lot here, so it's worth comparing lenders if child support is a meaningful part of your income."),
            ("Do I need a relationship property agreement to refinance?",
             "Most lenders want to see the agreed division in writing before approving the final loan, usually as a signed relationship property agreement or a solicitor's confirmation. Each person should get independent legal advice."),
            ("Can I buy out my partner with less than 20% equity left?",
             "Possibly, but fewer lenders will consider it, and it may cost more. Borrowing to pay out a share raises the loan against the same property, so check your likely loan-to-value ratio early."),
        ],
        "faq_heading": "Refinancing after separation: common questions",
        "related": REL_REFI,
    },

    {
        "slug": "new-bank-wont-refinance-mortgage-nz",
        "published": PUBLISHED,
        "title": "New Bank Won't Refinance Your Mortgage? NZ Options | Finch",
        "h1": "When a New Bank Won't Refinance You: Your Options in NZ",
        "section_label": "Refinance",
        "region": "",
        "lead_service": "Refinance",
        "about": ["Refinancing", "Mortgage serviceability", "Debt-to-income ratio", "Home loans"],
        "intro_pull": "You've paid your mortgage on time for years, but a new lender says you don't qualify for the same loan. It happens more than people think. Here's why — and what you can still do.",
        "description": "Declined when refinancing in NZ? Why a new lender may not approve the same loan, and your options: retention offers, restructuring and other lenders.",
        "keywords": [
            "can't refinance mortgage NZ",
            "refinance declined NZ",
            "new bank won't lend me NZ",
            "mortgage prisoner NZ",
            "refinance serviceability NZ",
            "switch bank mortgage declined",
        ],
        "cta_heading": "Been declined, or worried you will be?",
        "cta_sub": "Tell us your loan, income and lender. We'll check which lenders' policies fit your situation before anything goes on your credit file.",
        "sections": [
            ("Why a perfect repayment record isn't enough", (
                p("Your current bank already has your loan. A new lender is making a fresh lending decision, so it assesses you as if you were borrowing for the first time — at its own assessment rate, against today's income and expenses, and under today's rules.")
                + p("So someone who has never missed a payment can still fail a new lender's test. Common reasons:")
                + ul([
                    "<strong>Assessment rates.</strong> Lenders test whether you could afford repayments at a rate above what you'd actually pay. If that buffer is large, your loan might not pass even though you're paying it comfortably.",
                    "<strong>Your circumstances have changed.</strong> Less income, a new baby, a move to self-employment, a car loan or a credit card limit all reduce what you can borrow.",
                    "<strong>Debt-to-income limits.</strong> The Reserve Bank's DTI settings, and each lender's own limits, cap borrowing relative to income.",
                    "<strong>Property policy.</strong> The lender may not like the property type — a small apartment, leasehold land, a cross-lease with title issues, or a building with weathertightness or earthquake concerns.",
                    "<strong>Credit history.</strong> Recent missed payments, defaults or several credit enquiries in a short time.",
                ])
            )),
            ("What the rules actually say about refinancing", (
                p("Refinancing an existing loan <em>without increasing the amount</em> is generally treated differently from new borrowing under the Reserve Bank's LVR and DTI settings. Check the " + link(RBNZ_LVR, "Reserve Bank's current settings") + " for the details. But that doesn't oblige any lender to take you on. Each lender still applies its own credit policy and its responsible lending obligations under the Credit Contracts and Consumer Finance Act (CCCFA).")
                + callout("Topping up changes the picture", "If you add money to the loan when you refinance — for renovations, a car or debt consolidation — it's assessed as new lending. That's often what turns an easy switch into a decline. Consider separating the two decisions.")
            )),
            ("Your options", (
                table(
                    ["Option", "How it helps"],
                    [
                        ["Negotiate with your current bank", "Your bank doesn't need to reassess you to change your interest rate at the end of a fixed term. Show them what the market is offering and ask for a retention rate. This alone often closes most of the gap."],
                        ["Restructure, don't refinance", "A longer remaining term, different fixed and floating splits, or an offset account can improve cash flow without a new lender's approval."],
                        ["Try a lender whose policy fits", "Lenders differ in their assessment rates, how they treat bonuses, overtime, self-employed and rental income, and which properties they'll lend on. A decline at one lender doesn't mean a decline everywhere."],
                        ["Reduce other debts first", "Closing unused credit cards, reducing card limits and paying off small loans can lift what you can borrow noticeably. See " + link("car-loan-personal-debt-borrowing-power-nz.html", "how personal debt affects borrowing") + "."],
                        ["Non-bank lenders", "Specialist lenders may accept situations the banks won't, usually at a higher cost. Best seen as a stepping stone, with a plan to move back to a bank later."],
                        ["Wait and rebuild", "If your credit file or income is the issue, a few months of clean history or confirmed income can change the answer."],
                    ],
                )
            )),
            ("Avoid collecting declines", (
                p("Every credit application leaves an enquiry on your credit file, and several in a short time can look like financial stress to the next lender. Applying to bank after bank hoping one says yes can make things worse.")
                + p("A broker can check which lenders' policies fit your situation before anything is submitted, so the application that goes in is the one most likely to succeed. See also: " + link("loan-declined-what-next-nz.html", "what to do after a loan is declined") + " and " + link("improve-credit-score-mortgage-nz.html", "improving your credit score") + ".")
            )),
        ],
        "faqs": [
            ("Why would a new bank decline my refinance if I've never missed a payment?",
             "A new lender assesses you from scratch, at its own assessment rate and against your current income, expenses and debts. Your repayment history helps, but it doesn't replace the serviceability test. Changes since you first borrowed, such as new debts or lower income, are a common reason."),
            ("Are refinances exempt from the Reserve Bank's DTI and LVR rules?",
             "Refinancing an existing loan without increasing the amount is generally treated differently from new lending under the Reserve Bank's settings. Lenders still apply their own credit policies and responsible lending checks, so an exemption from the speed limits isn't the same as an approval."),
            ("Can my current bank still lower my rate if I can't move?",
             "Yes. At the end of a fixed term your bank can offer you a new rate without reassessing your loan. Ask for a retention rate and show them what other lenders are offering. Banks often move further than their advertised rates."),
            ("Do multiple refinance applications hurt my credit score?",
             "They can. Each application usually records an enquiry, and several in a short time can count against you. It's better to identify the right lender first and make one well-prepared application."),
        ],
        "faq_heading": "Refinance declined: common questions",
        "related": REL_REFI,
    },

    {
        "slug": "refinance-rental-property-investment-loans-nz",
        "published": PUBLISHED,
        "title": "Refinancing Rental Property Loans NZ: Investor Guide | Finch",
        "h1": "Refinancing Rental Property Loans in NZ: An Investor's Guide",
        "section_label": "Property Investment",
        "region": "",
        "lead_service": "Refinance",
        "about": ["Refinancing", "Investment property", "Rental property loans", "Property investors"],
        "intro_pull": "For investors, refinancing is about more than the rate. How your rental loans are structured, which properties secure which loans, and how much equity you can access all decide how easily you can buy, sell or restructure later.",
        "description": "Refinancing rental property in NZ: untangling cross-collateralised loans, releasing equity, interest-only terms, interest deductibility and investor LVR rules.",
        "keywords": [
            "refinance rental property NZ",
            "refinance investment property NZ",
            "cross collateralisation NZ",
            "release equity rental property NZ",
            "interest only investment loan NZ",
            "property investor refinance NZ",
        ],
        "cta_heading": "Want a review of your rental lending?",
        "cta_sub": "Send us your properties and loans, and which lender holds each. We'll show you how the structure could work harder for you.",
        "sections": [
            ("Why investors refinance", (
                ul([
                    "<strong>Rate and cashback</strong> — the same reasons as homeowners, multiplied across several loans.",
                    "<strong>Releasing equity</strong> to fund a deposit on the next property.",
                    "<strong>Separating securities</strong> so one lender doesn't hold every property.",
                    "<strong>Restructuring repayments</strong> — interest-only periods, or separate loans for each property.",
                    "<strong>Preparing to sell</strong> a property without disrupting the rest of the portfolio.",
                ])
            )),
            ("Cross-collateralisation: the issue most investors don't see", (
                p("When one lender holds several of your properties, it often takes all of them as security for all of your loans. That's called cross-collateralisation. It's convenient while you're building a portfolio, but it gives that lender a say over every move you make.")
                + table(
                    ["", "All properties with one lender (crossed)", "Split across lenders, each loan secured on its own property"],
                    [
                        ["Selling one property", "The lender can require some of the sale proceeds to reduce other loans before releasing its security.", "Sell it, repay that loan, keep the proceeds."],
                        ["Buying the next one", "Depends on one lender's appetite and its valuation of your whole portfolio.", "You can choose the lender that suits each purchase."],
                        ["If values fall", "One property's drop can affect the security position across everything.", "Each loan is assessed on its own property."],
                        ["Admin", "Simpler — one lender, one relationship.", "More lenders to manage, though often worth it for the flexibility."],
                    ],
                )
                + p("Refinancing part of a portfolio to a second lender is often the cleanest way to untangle this. It needs planning, because each property needs to support its own loan.")
            )),
            ("Releasing equity for the next purchase", (
                p("If your properties have gone up in value or your loans have come down, you may be able to borrow against that equity for your next deposit. Lenders work out how much they'll lend against existing property using their own LVR limits for investment property, and the Reserve Bank's LVR settings require a larger deposit for investors than for owner-occupiers. Check the " + link(RBNZ_LVR, "Reserve Bank's current settings") + ".")
                + p("Rental income is also usually counted at less than 100% when lenders assess serviceability, to allow for vacancies and costs. How much they discount it varies between lenders and is one of the main reasons a broker can find more borrowing capacity for investors. See " + link("using-home-equity-investment-property-nz.html", "using home equity to buy an investment property") + ".")
            )),
            ("Tax points to check with your accountant", (
                ul([
                    "<strong>Interest deductibility.</strong> For residential rental property, interest deductions were phased back in and have been fully deductible again from 1 April 2025. If you refinance to release equity, what the borrowed money is used for generally determines whether the interest is deductible — not which property secures it. Keep the purposes of each loan clearly separate.",
                    "<strong>Bright-line test.</strong> Refinancing a property is not selling it, so on its own it doesn't trigger the bright-line test. Selling within the bright-line period might.",
                    "<strong>Loan structure.</strong> Mixing personal and investment borrowing in one loan makes deductions harder to track. Refinancing is a good opportunity to separate them.",
                ])
                + p("Inland Revenue's " + link("https://www.ird.govt.nz/property/renting-out-residential-property", "guidance for residential landlords") + " is the official source. Tax settings change, so confirm the current position with your accountant.")
            )),
            ("Interest-only and repayment structure", (
                p("Many investors use interest-only periods on rental loans to improve cash flow, while paying down their home loan, where interest isn't deductible, faster. Lenders limit how long interest-only terms run and reassess at the end, so plan for the switch to principal-and-interest repayments.")
                + p("Splitting loans by property, and between fixed and floating, also makes it easier to sell or pay down one property without break fees on the rest.")
            )),
            ("How we help investors", (
                p("We review the whole portfolio, not just the next fixed term: which lender holds which security, where equity can be released, how rental income is being assessed, and how to structure things so your next purchase or sale isn't held up by your current set-up. We work alongside your accountant on the tax side.")
                + p("More on the service: " + link("../services/investment-property.html", "investment property loans") + ".")
            )),
        ],
        "faqs": [
            ("What is cross-collateralisation?",
             "It's when one lender uses several of your properties as security for all of your loans together. It can make selling one property or buying another harder, because the lender has a say over the whole portfolio. Spreading loans across lenders, with each secured on its own property, gives you more flexibility."),
            ("Can I refinance to release equity from my rental property?",
             "Often, yes, if the property's value has risen or the loan has reduced. The lender applies its own investment LVR limit and assesses whether you can service the extra borrowing, usually counting only part of your rental income."),
            ("Is mortgage interest on rental property tax deductible in NZ?",
             "For residential rental property, interest has been fully deductible again from 1 April 2025, after being phased back in. Whether interest on a particular loan is deductible depends on what the money was used for. Confirm your situation with your accountant."),
            ("Does refinancing a rental trigger the bright-line test?",
             "No. Refinancing isn't selling, so on its own it doesn't trigger the bright-line test. The test applies to selling residential property within the bright-line period."),
        ],
        "faq_heading": "Refinancing rental property: common questions",
        "related": [
            ("../services/investment-property.html", "Investment Property Loans",
             "Structure and lender matching for investors."),
            ("../services/refinance.html", "Refinance Your Mortgage",
             "Independent refinance advice across 20+ NZ lenders."),
            ("bright-line-test-nz-2026.html", "Bright-Line Test NZ",
             "When selling triggers tax."),
        ],
    },
]
