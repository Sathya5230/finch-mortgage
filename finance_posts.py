#!/usr/bin/env python3
"""Finance and loan-type posts for generate_local_intent_blogs.py.

A brand hub for "Finch finance / Finch loans" searches, plus guides for the
lending Finch arranges that had no blog coverage: asset finance, commercial
property and construction drawdowns.

Same content rules as local_intent_posts.py: explain mechanisms, never invent
rates, named lender policies or approval odds. Finch's disclosure statement
scopes its licensed advice to mortgages, so asset finance is described as
something Finch arranges, not as regulated financial advice.

Run:  python3 generate_local_intent_blogs.py finance_posts
"""

from generate_local_intent_blogs import callout, link, ol, p, table, ul
from local_intent_posts import REL_CORE

PUBLISHED = "2026-10-06"

REL_BUSINESS = [
    ("../services/asset-finance.html", "Asset &amp; Equipment Finance",
     "Vehicles, machinery and fleets for NZ businesses."),
    ("../services/commercial-property.html", "Commercial Property Loans",
     "Retail, industrial, office and mixed-use."),
    ("../services/self-employed.html", "Self-Employed Mortgages",
     "For business owners and contractors."),
]

POSTS = [
    {
        "slug": "finch-finance-loans-nz",
        "published": PUBLISHED,
        "title": "Finch Finance &amp; Loans NZ | Home, Business &amp; Asset Loans",
        "h1": "Finch Finance &amp; Loans: Every Loan Type We Arrange",
        "section_label": "Finch Finance &amp; Loans",
        "region": "",
        "lead_service": "Home Loan",
        "about": ["Finch Mortgages", "Home loans", "Business finance", "New Zealand lending"],
        "intro_pull": "Searching for Finch Finance or Finch Loans? You are in the right place. Finch Mortgages is an independent NZ broker, and this page sets out every type of lending we arrange — and where to start for each one.",
        "description": "Finch Finance &amp; Loans: home loans, construction, bridging, commercial property and asset finance arranged across 20+ NZ lenders. $0 broker fee.",
        "keywords": [
            "Finch finance",
            "Finch loans",
            "Finch Mortgages",
            "Finch home loans",
            "Finch mortgage NZ",
            "Finch finance NZ",
        ],
        "cta_heading": "Not sure which loan you need?",
        "cta_sub": "Tell us what you're trying to buy, build or refinance. We will point you at the right lending type and the lenders most likely to approve it.",
        "sections": [
            ("One business, a few names", (
                p("People find us as Finch, Finch Finance, Finch Loans, Finch Mortgage and Finch Mortgages. It is the same business: <strong>Finch Mortgages Limited</strong>, an independent New Zealand mortgage broker founded by Mukhtar Kiyani and based in Te Atatu South, Auckland. We work with clients across the country by phone, video and in person.")
                + p("Finch Mortgages (FSP1011125) is an Authorised Body operating under the Financial Advice Provider licence held by Finsure New Zealand Limited (FSP1005389). You can check this on the " + link("https://fsp-register.companiesoffice.govt.nz/", "Financial Service Providers Register") + ", and our full " + link("../disclosure.html", "disclosure statement") + " sets out the scope of our advice.")
                + callout("What it costs you", "For standard residential home loans there is no broker fee. The lender pays us a commission when your loan settles, and that does not increase your rate. Where a different fee arrangement applies — for example on some commercial or specialist lending — we tell you up front, in writing, before you commit.")
            )),
            ("The loans we arrange", (
                p("Most of what we do is residential mortgage lending, but clients often come to us for more than one thing over the years — a first home, then a refinance, then a rental, then finance for the business. This is the full range:")
                + table(
                    ["Loan type", "Who it's for", "Start here"],
                    [
                        ["Home loans", "Buying your own home, at any stage.", link("../services/home-loan.html", "Home loans")],
                        ["First home loans", "First home buyers using KiwiSaver, a low deposit or a family guarantee.", link("../services/first-home-buyer.html", "First home buyers")],
                        ["Next home loans", "Selling and buying, upsizing or downsizing.", link("../services/next-home-buyer.html", "Next home buyers")],
                        ["Refinancing", "Moving lender, restructuring or consolidating debt into your mortgage.", link("../services/refinance.html", "Refinance")],
                        ["Investment property loans", "Buying and structuring rental property.", link("../services/investment-property.html", "Investment property")],
                        ["Self-employed loans", "Business owners, contractors and sole traders.", link("../services/self-employed.html", "Self-employed")],
                        ["Pre-approval", "Knowing your budget before you bid or make an offer.", link("../services/pre-approval.html", "Pre-approval")],
                        ["Construction loans", "Building a new home, or a house-and-land package.", link("../services/construction-loan.html", "Construction loans")],
                        ["Bridging finance", "Buying your next home before the current one sells.", link("bridging-finance-guide-nz.html", "Bridging finance guide")],
                        ["Commercial property loans", "Buying premises for your business, or commercial investment property.", link("../services/commercial-property.html", "Commercial property")],
                        ["Asset &amp; equipment finance", "Vehicles, fleets, machinery and equipment for businesses.", link("../services/asset-finance.html", "Asset finance")],
                    ],
                )
            )),
            ("Why a broker rather than going straight to a bank", (
                p("A bank can only offer you its own products, assessed against its own policy. We compare your situation across a panel of more than 20 lenders — the main banks, smaller banks and specialist non-bank lenders — and recommend the ones whose policy actually fits your situation.")
                + p("That matters most when your situation is not perfectly standard: self-employed income, a small deposit, a property type some lenders avoid, a past credit issue, or a mix of home and business borrowing. The same application can be declined by one lender and approved by another, and every unnecessary application leaves a mark on your credit file. Checking which lenders are a fit before applying is a large part of what we do.")
                + ul([
                    "<strong>One conversation, many lenders.</strong> You don't repeat your story to five banks.",
                    "<strong>Structure, not just rate.</strong> Fixed and floating splits, offset or revolving credit, loan terms and how rentals sit alongside your home loan.",
                    "<strong>Ongoing reviews.</strong> We contact you before each fixed term ends so you aren't rolled onto whatever rate is offered.",
                ])
            )),
            ("How it works", (
                ol([
                    "<strong>Free discovery call.</strong> Fifteen minutes by phone or video to understand what you're trying to do.",
                    "<strong>Documents.</strong> We send a checklist that matches your situation — payslips for PAYE earners, financial statements for business owners.",
                    "<strong>Lender match.</strong> We assess your situation against our lender panel and explain the options, including the trade-offs.",
                    "<strong>Application and approval.</strong> We prepare and submit the application, and deal with the lender's questions.",
                    "<strong>Settlement and beyond.</strong> We work with your solicitor through settlement, then review your lending at every fixed-rate expiry.",
                ])
                + p("Want a rough number first? Try the " + link("../calculators/borrowing-power.html", "borrowing power calculator") + " or the " + link("../calculators/mortgage-calculator.html", "mortgage repayment calculator") + ".")
            )),
        ],
        "faqs": [
            ("Is Finch Finance the same as Finch Mortgages?",
             "Yes. Finch Finance, Finch Loans and Finch Mortgage are all names people use to search for Finch Mortgages Limited, the independent NZ mortgage broker that runs this website. There is one business."),
            ("Does Finch charge a fee for home loans?",
             "Not for standard residential home loans. The lender pays our commission when the loan settles, and it does not change your interest rate. If a different fee arrangement applies to a particular type of lending, we tell you in writing before you go ahead."),
            ("Does Finch only help people in Auckland?",
             "No. We are based in Te Atatu South, Auckland, but we arrange lending for clients throughout New Zealand by phone and video, with documents handled through a secure online portal."),
            ("Can Finch help with business or commercial lending?",
             "Yes. As well as home loans, we arrange commercial property loans and asset and equipment finance for businesses. Contact us with what you're looking to finance and we'll explain the options."),
        ],
        "faq_heading": "Finch Finance &amp; Loans: common questions",
        "related": REL_CORE + [
            ("../about.html", "About Finch Mortgages", "Who we are and how we work."),
            ("mortgage-broker-fees-nz.html", "Mortgage Broker Fees in NZ", "How brokers are paid, explained."),
            ("mortgage-broker-vs-bank-nz.html", "Broker vs Going Direct", "When a broker adds value."),
        ],
    },

    {
        "slug": "asset-finance-chattel-mortgage-lease-hire-purchase-nz",
        "published": PUBLISHED,
        "title": "Asset Finance NZ: Loan vs Lease vs Hire Purchase | Finch",
        "h1": "Asset Finance in NZ: Secured Loan, Lease or Hire Purchase?",
        "section_label": "Business Finance",
        "region": "",
        "lead_service": "Asset Finance",
        "about": ["Asset finance", "Equipment finance", "Vehicle finance", "Hire purchase"],
        "intro_pull": "Buying a ute, a truck or a piece of machinery for your business? How you finance it changes who owns it, how it's treated for tax, and what it does to your cash flow. Here is how the main structures compare.",
        "description": "Business asset finance in NZ explained: secured loans (chattel mortgages), leases and hire purchase compared — ownership, GST, tax treatment and cash flow.",
        "keywords": [
            "asset finance NZ",
            "equipment finance NZ",
            "chattel mortgage NZ",
            "business vehicle finance NZ",
            "hire purchase vs lease NZ",
            "ute finance for business NZ",
        ],
        "cta_heading": "Financing a vehicle or equipment for your business?",
        "cta_sub": "Tell us what you're buying, roughly what it costs and how long you've been trading. We'll come back with the structure and lenders that suit.",
        "sections": [
            ("Why businesses finance assets instead of paying cash", (
                p("Paying cash for a vehicle or machine is simple, but it ties up working capital in an asset that loses value from the day you buy it. Asset finance spreads the cost over the asset's useful life, so the machine pays for itself out of the work it does — and the cash stays in the business for wages, stock and the months when invoices are paid late.")
                + p("The question is less <em>whether</em> to finance and more <em>which structure</em>. In New Zealand the three you'll most often be offered are a secured loan (often called a chattel mortgage), a lease, and hire purchase.")
            )),
            ("The three structures at a glance", (
                table(
                    ["", "Secured loan (chattel mortgage)", "Lease", "Hire purchase"],
                    [
                        ["Who owns the asset", "Your business, from day one. The lender holds security over it.", "The lender (lessor). You have the right to use it.", "The lender, until the final payment. Then it passes to you."],
                        ["At the end", "Loan repaid, asset is yours outright.", "Return it, extend, upgrade or sometimes buy it — depending on the lease.", "You own it once all payments are made."],
                        ["Typical fit", "Assets you plan to keep for their working life.", "Assets you replace regularly, like fleet cars or technology.", "Businesses that want to own the asset but prefer an instalment structure."],
                        ["Balance sheet", "Asset and loan both on your books.", "Depends on the lease type and your accounting standards.", "Generally treated like an asset you're buying."],
                    ],
                )
                + p("Names vary between lenders, and some products blend features. Read what the contract says about ownership and the end of the term, not just the product name.")
            )),
            ("Tax and GST: ask your accountant, but know the questions", (
                p("Tax treatment is often what decides the structure, and it depends on your business, the asset and the exact contract. We work alongside your accountant on this rather than in place of them. These are the questions worth asking:")
                + ul([
                    "<strong>Can I claim depreciation and interest?</strong> When your business owns the asset, depreciation and interest are generally the deductions. With an operating lease, the lease payments themselves are usually the deduction instead.",
                    "<strong>When do I claim the GST?</strong> If you're GST-registered and buy the asset, you can generally claim GST on the purchase price up front. Under a lease, GST is typically charged on each payment instead.",
                    "<strong>Is this lease treated as a lease for tax?</strong> Some leases are treated by Inland Revenue as if you'd bought the asset, which changes the deductions. Your accountant can tell you which side of the line a contract falls on.",
                    "<strong>What happens if I sell the asset early?</strong> Depreciation recovered on sale, payout figures and any break costs all affect the real cost.",
                ])
                + p("Inland Revenue's " + link("https://www.ird.govt.nz/", "guidance on business assets and depreciation") + " is the official reference.")
            )),
            ("What lenders look at", (
                p("Asset finance is assessed differently from a home loan. The asset itself is security, so its type, age and resale value matter as much as your income.")
                + ul([
                    "<strong>Trading history.</strong> How long the business has been operating, and its recent financial statements. Newer businesses can still get finance, but usually with fewer lenders to choose from.",
                    "<strong>The asset.</strong> Mainstream vehicles and equipment with an active resale market are easier to finance than specialised or very old machinery.",
                    "<strong>New or used, dealer or private.</strong> Some lenders are more comfortable with dealer sales; private purchases may need extra checks on ownership.",
                    "<strong>Deposit or trade-in.</strong> Not always required, but it can widen your lender options and improve your terms.",
                    "<strong>Your other borrowing.</strong> Existing business debt, tax arrears and personal guarantees all feature in the assessment.",
                ])
                + callout("Security is registered", "Lenders register their security interest over the asset on the " + link("https://ppsr.companiesoffice.govt.nz/", "Personal Property Securities Register (PPSR)") + ". If you're buying second-hand, a PPSR search tells you whether someone else already has a security interest over it.")
            )),
            ("Matching the term to the asset", (
                p("A common mistake is choosing the longest term to get the lowest repayment, then still paying for a vehicle years after it has been replaced. As a rule of thumb, the finance should finish before the asset stops earning its keep.")
                + p("Some loans offer a <strong>balloon or residual</strong> — a lump sum due at the end — to reduce the regular repayments. That helps cash flow, but plan for the lump sum: you'll need to pay it, refinance it, or sell or trade the asset to clear it.")
            )),
            ("How we help", (
                p("We arrange asset and equipment finance for NZ businesses alongside their property lending, so the full picture — business debt, home loan and any rentals — is considered together. Tell us what you're buying and we'll explain which structures make sense and which lenders suit your trading history, then work with your accountant to settle the tax side.")
                + p("More on the service: " + link("../services/asset-finance.html", "asset and equipment finance") + ".")
            )),
        ],
        "faqs": [
            ("What is a chattel mortgage in NZ?",
             "It's a common name for a secured business loan used to buy a vehicle or equipment. Your business owns the asset from the start, and the lender takes security over it, registered on the Personal Property Securities Register, until the loan is repaid."),
            ("Is it better to lease or buy business equipment?",
             "It depends on how long you'll keep the asset and how your accountant wants it treated for tax. Buying, with a loan or hire purchase, usually suits assets you'll use for their working life. Leasing often suits assets you replace regularly. Ask your accountant to compare the after-tax cost of each."),
            ("Can a new business get asset finance?",
             "Often yes, but with fewer lenders to choose from. Lenders look at trading history, the asset, any deposit or trade-in, and the owners' personal position. A recently started business buying a mainstream vehicle is a very different proposition from one buying specialised machinery."),
            ("Can I claim GST on a vehicle bought with finance?",
             "If your business is GST-registered and buys the vehicle, you can generally claim the GST on the purchase, subject to how much the vehicle is used for business. Under a lease, GST is usually charged on each payment instead. Confirm the details for your situation with your accountant."),
        ],
        "faq_heading": "Asset finance: common questions",
        "related": REL_BUSINESS,
    },

    {
        "slug": "commercial-property-loan-nz-how-lenders-assess",
        "published": PUBLISHED,
        "title": "Commercial Property Loans NZ: How Lenders Assess | Finch",
        "h1": "Commercial Property Loans in NZ: How Lenders Assess Your Deal",
        "section_label": "Commercial Property",
        "region": "",
        "lead_service": "Commercial Property",
        "about": ["Commercial property loans", "Commercial mortgages", "Commercial real estate", "New Zealand lending"],
        "intro_pull": "Commercial lending works on different rules from home loans. The property's income matters as much as yours, deposits are larger, and loan terms are shorter. Here is what NZ lenders look at, and how to put forward a strong application.",
        "description": "How NZ lenders assess commercial property loans: LVR, interest cover, lease terms, tenant strength and GST, for owner-occupiers and investors.",
        "keywords": [
            "commercial property loan NZ",
            "commercial mortgage NZ",
            "buying commercial property NZ",
            "commercial property LVR NZ",
            "owner occupier commercial loan NZ",
            "commercial property finance NZ",
        ],
        "cta_heading": "Looking at a commercial property?",
        "cta_sub": "Send us the listing or information memorandum. We'll tell you how lenders are likely to view it and what deposit to plan for.",
        "sections": [
            ("How commercial lending differs from a home loan", (
                p("A home loan is assessed mainly on you — your income, your expenses and your deposit. A commercial loan is assessed on the <strong>property as a business</strong>: the rent it earns, how secure that rent is, and what the building would be worth if a tenant left. Your own finances still matter, but they are only part of the picture.")
                + table(
                    ["", "Residential home loan", "Commercial property loan"],
                    [
                        ["Deposit", "Set within the Reserve Bank's LVR and DTI settings.", "Usually considerably larger. Lenders commonly cap commercial lending at a lower LVR, and it varies with the asset and tenant."],
                        ["Loan term", "Typically up to 30 years.", "Often a shorter facility term, reviewed and renewed, sometimes with a shorter repayment schedule."],
                        ["Main test", "Your ability to service the loan from your income.", "The property's rental income covering the interest, plus the strength of the borrower and any guarantors."],
                        ["Who you deal with", "Retail lending.", "Commercial or business banking managers, and specialist non-bank lenders."],
                    ],
                )
            )),
            ("The numbers lenders focus on", (
                ul([
                    "<strong>Loan-to-value ratio (LVR).</strong> How much is borrowed against the registered valuation. Expect lower maximums than for residential property, with the limit tightening for specialised or secondary buildings.",
                    "<strong>Interest cover ratio (ICR).</strong> Net rental income divided by the interest cost. Lenders want a buffer, so the rent covers the interest comfortably, not just exactly.",
                    "<strong>Weighted average lease term (WALT).</strong> How long the existing leases run, weighted by rent. A long WALT with reliable tenants is much easier to finance than a building with leases ending soon.",
                    "<strong>Tenant strength.</strong> A national chain or government tenant is assessed very differently from a new local business. Lenders look at who pays the rent, not just how much.",
                    "<strong>Vacancy and re-letting risk.</strong> How easily the space would let again if a tenant left, and at what rent.",
                ])
                + callout("Read the leases before the lender does", "The leases are effectively the income statement for the property. Review terms, rent reviews, renewal rights, who pays outgoings and any break clauses. A lender will scrutinise them closely — and so should you, before you go unconditional.")
            )),
            ("Owner-occupier or investor?", (
                p("Buying premises for your own business is assessed differently from buying commercial property as an investment.")
                + ul([
                    "<strong>Owner-occupiers</strong> are assessed mostly on the operating business — its profits, history and ability to pay rent to the property-owning entity. Many business owners hold the property in a separate company or trust that leases it to the trading business, and the lender looks at both.",
                    "<strong>Investors</strong> are assessed mostly on the property's income from third-party tenants, supported by the investor's wider financial position and other holdings.",
                ])
                + p("Either way, how the purchase is structured — personally, through a company, or through a trust — affects guarantees, tax and future flexibility. Get your accountant and solicitor involved early.")
            )),
            ("GST on commercial property", (
                p("GST often catches first-time commercial buyers out. When land is sold between two GST-registered parties and the buyer intends to use it to make taxable supplies, the sale is generally <strong>zero-rated</strong> — meaning no GST is charged. If the conditions aren't met, GST may be payable on top of the price, which can significantly change how much you need to fund on settlement.")
                + p("Your solicitor should confirm the GST position in the sale and purchase agreement, and your accountant should confirm your registration. See " + link("https://www.ird.govt.nz/gst", "Inland Revenue's GST guidance") + " for the official rules.")
            )),
            ("Putting together a strong application", (
                ol([
                    "Information memorandum or listing details, including the rent roll.",
                    "Copies of all current leases and any variations.",
                    "A registered valuation addressed to the lender (we'll tell you when to order it).",
                    "Recent financial statements for the buying entity, and for the trading business if you're an owner-occupier.",
                    "Details of your other assets and debts, including residential property.",
                    "A brief summary of your plans for the property — holding, improving, or occupying it.",
                ])
                + p("A clear, complete application helps, because commercial credit decisions take longer than residential ones. Allow enough time for finance in your conditional period.")
            )),
            ("How we help", (
                p("Commercial lenders' appetite varies a lot by asset class, location, tenant and borrower. We put your deal forward to the commercial lenders whose appetite suits it, present the lease profile and borrower strength clearly, and manage the process through to settlement. For investors who also hold residential property, we look at the whole portfolio so one purchase doesn't restrict the next.")
                + p("More on the service: " + link("../services/commercial-property.html", "commercial property loans") + ".")
            )),
        ],
        "faqs": [
            ("How much deposit do I need for commercial property in NZ?",
             "Usually considerably more than for a home. Lenders set their own maximum loan-to-value ratio for commercial property, and it tightens for specialised buildings, weaker tenants or short leases. The exact figure depends on the property, the tenant and the borrower, so it's best confirmed against the specific deal."),
            ("What is an interest cover ratio?",
             "It's the property's net rental income divided by the interest on the loan. Lenders want rent to cover the interest with a margin to spare, so a property earning only just enough to meet the interest will struggle to support the loan amount you're asking for."),
            ("Is GST charged when buying commercial property?",
             "If both buyer and seller are GST-registered and the buyer will use the property to make taxable supplies, the sale is generally zero-rated, so no GST is charged. If those conditions aren't met, GST may apply. Your solicitor and accountant should confirm the position before you sign."),
            ("Can I buy my business premises through my company?",
             "Often yes. Many business owners hold the property in a separate company or trust that leases it to the trading business. Lenders then assess both entities and usually ask for personal guarantees. Get advice on the structure before you buy."),
        ],
        "faq_heading": "Commercial property loans: common questions",
        "related": [
            ("../services/commercial-property.html", "Commercial Property Loans",
             "Retail, industrial, office and mixed-use."),
            ("../services/investment-property.html", "Investment Property Loans",
             "Structure and lender matching for investors."),
            ("using-home-equity-investment-property-nz.html", "Using Home Equity",
             "Turn equity into your next purchase."),
        ],
    },

    {
        "slug": "construction-loan-progress-payments-nz",
        "published": PUBLISHED,
        "title": "Construction Loans NZ: How Progress Payments Work | Finch",
        "h1": "Construction Loans in NZ: How Progress Payments Work",
        "section_label": "Building a Home",
        "region": "",
        "lead_service": "Construction Loan",
        "about": ["Construction loans", "Building a house", "New build finance", "Progress payments"],
        "intro_pull": "A construction loan doesn't pay out all at once. The lender releases money in stages as your build progresses, and you pay interest only on what's been drawn. Here's how it works from deposit to code compliance certificate.",
        "description": "How construction loans work in NZ: progress payments, drawdown stages, interest during the build, fixed-price contracts and the new-build LVR exemption.",
        "keywords": [
            "construction loan NZ",
            "progress payments building NZ",
            "new build mortgage NZ",
            "building a house finance NZ",
            "house and land package finance NZ",
            "construction loan drawdown NZ",
        ],
        "cta_heading": "Planning a build?",
        "cta_sub": "Send us your build contract or quote and the land details. We'll explain how lenders will structure the drawdowns and what deposit you'll need.",
        "sections": [
            ("How a construction loan differs from a standard mortgage", (
                p("With a standard purchase, the lender pays the full price on settlement day and your loan starts in full. A construction loan works differently: the lender approves the total amount at the start, but releases it in <strong>stages</strong> as the build reaches agreed milestones. Each stage is called a progress payment or drawdown.")
                + p("This protects both you and the lender — money only goes out for work that has actually been done, and the lender's security (the partly built house) grows as the loan does.")
                + callout("Interest only on what's drawn", "During the build you usually pay interest only on the amount drawn so far, not on the full approved loan. Repayments are low early on and rise as each stage is paid. Once the build is finished, the loan normally converts to standard principal-and-interest repayments.")
            )),
            ("A typical drawdown schedule", (
                p("Every builder's contract sets its own payment schedule, and lenders match drawdowns to it. A common pattern looks like this:")
                + table(
                    ["Stage", "What's been done", "What the lender usually wants"],
                    [
                        ["Land / deposit", "Land purchase settles, or the builder's deposit is paid.", "Signed build contract, plans and specifications, and an 'as if complete' valuation."],
                        ["Foundations / floor", "Site works and floor slab completed.", "Builder's invoice; some lenders also want a progress inspection."],
                        ["Frame", "Wall and roof framing up.", "Invoice and, where required, a valuer's progress report."],
                        ["Closed in", "Roof on, windows and exterior cladding done — weathertight.", "Invoice and progress report."],
                        ["Linings / fit-out", "Interior linings, joinery and fixtures going in.", "Invoice and progress report."],
                        ["Practical completion", "Build finished.", "Final invoice, final valuation, and usually the code compliance certificate (CCC) before the last payment."],
                    ],
                )
                + p("Your own deposit is usually used first, then the lender's funds. Keep a buffer for variations — changes you make during the build that weren't in the original contract.")
            )),
            ("Fixed-price contracts make finance easier", (
                p("Lenders are much more comfortable with a <strong>fixed-price contract</strong> from an established builder than with a cost-plus or labour-only arrangement, because the total cost is known at the start. Cost-plus and owner-builder projects can still be financed, but with fewer lenders and usually a larger contingency requirement.")
                + ul([
                    "Under the Building Act, residential building work costing $30,000 or more (including GST) must have a written contract, and the builder must give you a disclosure statement and checklist before you sign.",
                    "Check whether the builder offers a build guarantee, and what it covers if the builder can't finish.",
                    "Make sure the contract's payment schedule doesn't ask for money ahead of the work done. Lenders often won't advance funds before the matching stage is complete.",
                ])
                + p("MBIE's " + link("https://www.building.govt.nz/", "building.govt.nz") + " has plain-English guidance on contracts and your rights as a homeowner.")
            )),
            ("Deposits and the new-build exemption", (
                p("Under the Reserve Bank's LVR settings, lending on new builds is <strong>exempt</strong> from the low-deposit speed limits that apply to existing homes. That exemption is why building or buying off the plans can be a lower-deposit route into home ownership, particularly for first home buyers.")
                + p("Being exempt from the speed limit doesn't mean every lender offers low-deposit construction lending, or offers it on the same terms. Each lender sets its own policy on deposit, builder type and contract type. See " + link("what-is-lvr-nz-mortgage.html", "what LVR means for your deposit") + " and the " + link("https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions", "Reserve Bank's LVR page") + " for the current settings.")
            )),
            ("House-and-land packages vs building on your own land", (
                ul([
                    "<strong>House-and-land package:</strong> you buy a section and sign a build contract with the developer's builder, often together. Settlement on the land may happen at title, with the build starting afterwards. Be clear on when each payment is due.",
                    "<strong>Your own land:</strong> if you already own the section, its equity can count towards your deposit. If the land is still being paid off, the land loan and construction loan are usually combined.",
                    "<strong>Turnkey:</strong> the builder funds the build and you pay most of the price on completion. This is closer to a standard purchase, but check what deposit is held and how it's protected.",
                ])
                + p("Comparing options? Our guide to " + link("build-vs-buy-nz.html", "building vs buying in NZ") + " and " + link("buying-off-the-plans-finance-nz.html", "buying off the plans") + " covers the trade-offs.")
            )),
            ("How we help", (
                p("Construction lending is where lender policy differs most — on contract type, builder, deposit and how drawdowns are managed. We match your build to lenders whose policy fits it, sort out the drawdown schedule with your builder before you sign, and manage each progress payment so the build isn't held up by paperwork.")
                + p("More on the service: " + link("../services/construction-loan.html", "construction loans") + ".")
            )),
        ],
        "faqs": [
            ("Do I pay interest on the full construction loan from day one?",
             "Usually not. During the build you generally pay interest only on the amount drawn down so far. Repayments grow as each progress payment is released, and once the build is complete the loan normally moves to standard principal-and-interest repayments."),
            ("What is a progress payment?",
             "A progress payment is a staged release of your construction loan when the build reaches an agreed milestone, such as foundations, framing or closed in. The lender typically wants the builder's invoice and, often, a valuer's progress report before releasing each payment."),
            ("Can I build with a small deposit in NZ?",
             "New builds are exempt from the Reserve Bank's low-deposit speed limits, so some lenders offer construction lending with a smaller deposit than for an existing home. Each lender sets its own criteria for deposit, builder and contract type, so options vary."),
            ("Do I need a code compliance certificate before the final payment?",
             "Most lenders require the code compliance certificate, or at least practical completion and a final valuation, before releasing the last progress payment. Check your lender's requirements and your builder's contract so the final payment isn't delayed."),
        ],
        "faq_heading": "Construction loans: common questions",
        "related": [
            ("../services/construction-loan.html", "Construction Loans",
             "Finance for building a new home."),
            ("build-vs-buy-nz.html", "Build vs Buy in NZ",
             "The trade-offs, side by side."),
            ("buying-off-the-plans-finance-nz.html", "Buying Off the Plans",
             "Finance for pre-sale purchases."),
        ],
    },
]
