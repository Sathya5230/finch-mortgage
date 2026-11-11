#!/usr/bin/env python3
"""Rewrite the templated middle of the ten service pages.

What was wrong (November 2026 audit):
  * The long "guide" section on each page was filler prose that also named
    lenders outside Finch's 23-lender panel, quoted cashback percentages and
    promised below-advertised rates.
  * Asset finance, commercial property, construction and next-home pages
    carried the first-home "how it works" steps and first-home FAQs
    (KiwiSaver, First Home Grant), copied from one template.
  * No service page had FAQPage structured data.

This replaces those three sections with page-specific copy held in SERVICES
below, inside FINCH-GUIDE / FINCH-STEPS / FINCH-FAQ markers, and adds a
FAQPage JSON-LD block built from the visible questions. Same rules as the
post modules: no rates, no named-lender policies, no approval promises.

Dry run by default; --apply to write. Idempotent.
"""

import json
import re
import sys
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
SITE = "https://www.finchmortgages.co.nz"
A = 'style="color:var(--finch-forest);font-weight:600;text-decoration:underline;"'
CHEV = ('<svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" '
        'stroke-width="2.5" style="display:inline-block;vertical-align:middle;flex-shrink:0;" viewbox="0 0 24 24" '
        'width="20"><polyline points="6 9 12 15 18 9"></polyline></svg>')


def a(href, text):
    return f'<a href="{href}" {A}>{text}</a>'


def b(slug, text):
    return a(f"../blog/{slug}", text)


FEE = "For residential home loans our advice costs you nothing. The lender pays us when the loan settles, and we disclose that in writing."
FEE_BIZ = "We'll tell you about any fee before you commit to anything. Commission paid by the lender is disclosed in writing."

HOME_STEPS = [
    ("A first conversation", "Fifteen minutes or so, by phone, video or in person. We ask about your income, deposit, debts and what you're trying to do. It's free and you're not committing to anything."),
    ("We check the lenders", "We compare your situation against the 23 lenders on our panel and tell you which ones fit, what you could borrow and what it would cost."),
    ("Application", "You upload documents once. We prepare the application and deal with the lender's questions. How quickly a decision comes back depends on the lender and how busy it is."),
    ("Approval and conditions", "You get the approval in writing. We explain every condition and help you meet them, including valuations and insurance."),
    ("Settlement", "We work with your solicitor through to settlement day, then check in before each fixed term ends."),
]

SERVICES = {
    "home-loan.html": {
        "h2": "How home loans work in New Zealand",
        "guide": [
            ("p", "Three numbers decide most home loan applications: your deposit, your income, and what you already owe. The rest is detail. Here's how lenders look at each one, and where an adviser changes the result."),
            ("h3", "Your deposit"),
            ("p", "Twenty per cent is the standard, because the Reserve Bank limits how much banks can lend to people with less. Less than 20% is possible through a bank's low-deposit allocation, a new build, the Kāinga Ora First Home Loan or a family guarantee. Each costs something extra. We compare them in our guide to " + b("low-deposit-home-loan-nz", "low deposit home loans") + ", and explain the extra charge in " + b("low-equity-margin-fee-nz", "low equity margins") + "."),
            ("h3", "Your income, and how it's tested"),
            ("p", "Lenders don't test whether you can afford the loan at today's rate. They test at a higher rate, and they count your credit card limits as if they were fully used. Two lenders can look at the same payslips and reach different answers, because each sets its own test rate and its own rules for overtime, bonuses, commission and boarder income. That gap is the main thing a broker works with. More in " + b("mortgage-stress-test-rate-nz", "how the stress test works") + "."),
            ("h3", "The type of property"),
            ("p", "A standalone house on its own title is the easy case. " + b("apartment-home-loan-nz", "Apartments") + ", " + b("home-loan-for-land-section-nz", "bare land") + ", " + b("turnkey-home-loan-nz", "turnkey new builds") + ", cross-leases and leasehold land each have their own lending rules, and some lenders won't touch some of them. Tell us what you're looking at before you make an offer."),
            ("h3", "Structure matters as much as rate"),
            ("p", "Fixed or floating, one loan or several, how long to fix for. There's no universally right answer, and nobody can predict rates. We set the loan up around what you expect to happen in your own life over the next few years. See " + b("how-to-structure-your-mortgage-nz", "how to structure your mortgage") + "."),
            ("p", FEE + " If your own bank turns out to be the best option, we'll say so."),
        ],
        "steps": HOME_STEPS,
        "faqs": [
            ("How much deposit do I need for a home loan in NZ?", "Usually 20% of the purchase price. Buyers with 10%, and sometimes 5%, can be approved through a bank's low-deposit allocation, a new build, the Kāinga Ora First Home Loan or a family guarantee. Low-deposit loans generally cost more until your equity reaches 20%."),
            ("How much can I borrow?", "It depends on your income, living costs, existing debts and the lender. Banks are restricted in lending above six times gross income for owner-occupiers, and each tests affordability at its own rate. We run your figures across several lenders to show the range."),
            ("Does it cost anything to use Finch?", "Not for residential home loans. The lender pays us a commission when your loan settles, and we disclose it in writing before you act on our advice."),
            ("Which lenders does Finch work with?", "We have 23 lenders on our panel: six registered banks, sixteen non-bank lenders and a credit union. The full list is on our lenders page. If a lender outside our panel would suit you better, we'll tell you."),
        ],
    },
    "first-home-buyer.html": {
        "h2": "Buying your first home in New Zealand",
        "guide": [
            ("p", "Most first home buyers we talk to have the same three questions. Is my deposit enough? How much can I borrow? What do I do first? The answers are more encouraging than people expect."),
            ("h3", "Is my deposit enough?"),
            ("p", "You don't need 20%. Plenty of first homes are bought with 10%, and the Kāinga Ora " + b("first-home-loan-kainga-ora-nz", "First Home Loan") + " allows 5% if your income is under its caps. Your deposit can be made up of savings, a " + b("kiwisaver-first-home-withdrawal", "KiwiSaver withdrawal") + " and a " + b("gifted-deposit-home-loan-nz", "gift from family") + ". If your parents own a home, a " + b("guarantor-home-loan-nz", "family guarantee") + " can stand in for the part you're missing. The First Home Grant closed in May 2024 and hasn't been replaced."),
            ("h3", "How much can I borrow?"),
            ("p", "Lenders look at income, living costs and existing debt, then test whether you could manage repayments at a rate above the real one. Small things move the answer a lot. Paying off a car loan, cutting an unused credit card limit or closing a buy-now-pay-later account can add tens of thousands to what a bank will lend. We go through that with you before you apply, not after."),
            ("p", "Buying alone? See " + b("buying-a-house-on-one-income-nz", "buying on one income") + ". Just changed jobs? See " + b("home-loan-new-job-probation-nz", "home loans on probation") + "."),
            ("h3", "What to do first"),
            ("p", "Get a pre-approval before you go to open homes. It tells you your real budget, lets you bid at auction, and shows agents you're serious. It costs nothing and commits you to nothing. From there the usual order is: find a house, get a building report and LIM, have your lawyer check the contract, confirm finance, settle."),
            ("p", FEE),
        ],
        "steps": [
            ("A first conversation", "We go through your income, savings, KiwiSaver and debts, and tell you roughly where you stand. Free, and no obligation."),
            ("We work out your options", "Which low-deposit routes you qualify for, what each would cost, and which of our 23 lenders suit you. We also tell you what to tidy up before applying."),
            ("Pre-approval", "We prepare the application and handle the lender's questions. You get a written pre-approval with a budget you can rely on."),
            ("House hunting", "When you find a place, send us the listing. We check the property suits the lender and help you with the conditions in your offer."),
            ("Settlement day", "We work with your solicitor on the KiwiSaver withdrawal, loan documents and insurance, through to the day you get the keys."),
        ],
        "faqs": [
            ("How much deposit do I need as a first home buyer?", "Most lenders want 20%, but first home buyers are regularly approved with 10%, and with 5% through the Kāinga Ora First Home Loan if they meet its criteria. A family guarantee can also cover a shortfall."),
            ("Can I use my KiwiSaver for a house deposit?", "Yes. If you've been a member for at least three years and it's your first home, you can usually withdraw most of your balance, leaving $1,000 in the account. Apply to your provider well before settlement."),
            ("Is the First Home Grant still available?", "No. It closed to new applications on 22 May 2024 and hasn't been replaced. The Kāinga Ora First Home Loan, which allows a 5% deposit, is still available to eligible buyers."),
            ("How long does pre-approval take?", "It depends on the lender and how complete your documents are. Allow a few working days to a couple of weeks. Having payslips, bank statements and ID ready at the start is the best way to speed it up."),
        ],
    },
    "next-home-buyer.html": {
        "h2": "Buying your next home: getting the timing right",
        "guide": [
            ("p", "Buying a second home is easier than the first in one way, because you have equity. It's harder in another: there are two transactions to line up, and they rarely fall on the same day without some planning."),
            ("h3", "Sell first or buy first?"),
            ("p", "Selling first is the safe option. You know exactly what you have to spend, and there's no risk of owning two houses. The cost is that you may need somewhere to live in between. Buying first means you don't miss the house you want, but you carry two properties until the old one sells."),
            ("p", "A third option is a long settlement on the purchase, or an offer conditional on selling your home. Sellers don't love conditional offers, so they work best in a quiet market."),
            ("h3", "Bridging finance"),
            ("p", "A bridging loan covers the gap when you buy before you sell. Lenders are much more comfortable when your current home is already sold unconditionally and the dates simply don't match. Bridging without a confirmed sale is harder to get and costs more, because nobody knows when it ends. Our " + b("bridging-finance-guide-nz", "bridging finance guide") + " goes through both kinds."),
            ("h3", "Keeping the first home as a rental"),
            ("p", "It's possible if you have enough equity across both properties and the income to carry both loans. The old loan was used to buy what is now a rental, so the tax treatment of its interest changes. Talk to an accountant before you move, and read " + b("mortgage-interest-tax-deductible-nz", "how interest deductibility works") + "."),
            ("h3", "Don't forget your existing loan"),
            ("p", "If you're on a fixed rate, repaying it when you sell can trigger a " + b("break-fixed-mortgage-break-fees-nz", "break fee") + ", and a cash contribution you received may have to be " + b("mortgage-cashback-clawback-nz", "paid back") + ". Often your lender will let you carry the loan over to the new property, which avoids both. We check that first."),
            ("p", FEE),
        ],
        "steps": [
            ("A first conversation", "We look at your current loan, your equity and what you want to buy. Free, and no obligation."),
            ("Work out the order", "Sell first, buy first or a long settlement. We cost each option, including break fees and any bridging finance."),
            ("Pre-approval", "We arrange approval for the new purchase, with bridging if you need it, so you can make an offer with confidence."),
            ("Line up the dates", "We work with your solicitor and agent to get the two settlements as close together as possible."),
            ("Settlement", "The old loan is repaid or moved across, the new one starts, and we set a structure for the years ahead."),
        ],
        "faqs": [
            ("Can I buy my next home before I sell my current one?", "Yes, with bridging finance. Lenders prefer that your current home has an unconditional sale agreement. Without one, approval is harder and the cost is higher, because the lender can't see when the bridge will end."),
            ("How much equity do I need to buy my next home?", "Your equity acts as the deposit. Most lenders want the new loan to be no more than 80% of the new home's value, though some will go higher. We work it out from your likely sale price and what you owe."),
            ("Will I pay a break fee when I sell?", "Only if you repay a fixed-rate loan before its term ends and rates have fallen since you fixed. Many lenders let you transfer the loan to your new property, which avoids the fee. Ask before you list your home."),
            ("Can I keep my current home as a rental?", "Yes, if you have enough combined equity and income to support both loans. Rental properties need more equity than owner-occupied homes, and lenders count only part of the rent."),
        ],
    },
    "refinance.html": {
        "h2": "When refinancing is worth it, and when it isn't",
        "guide": [
            ("p", "Refinancing pays when what you gain is clearly more than what it costs to move. That sounds obvious, but most of the work is in getting the real figures for each side."),
            ("h3", "What it costs to move"),
            ("p", "Legal fees and a small discharge fee, always. A break fee, if you leave a fixed rate early and rates have fallen. Repayment of any cash contribution your current lender gave you, if you're still inside its clawback period. We get the actual numbers from your bank. Full detail in " + b("refinance-costs-nz", "what refinancing costs") + " and " + b("mortgage-cashback-clawback-nz", "how clawback works") + "."),
            ("h3", "What you gain"),
            ("p", "A lower rate, sometimes a cash contribution from the new lender, and often a better structure: an offset account, a shorter term, or other debts brought under one loan. We weigh that against the costs over the time you're likely to stay. " + b("is-it-worth-refinancing-mortgage-nz", "Is it worth refinancing?") + " shows the sum."),
            ("h3", "The best time"),
            ("p", "The day a fixed term ends, because there's nothing to break. Start six to eight weeks earlier. If your loan is split across terms that end at different times, there may be no perfect date, and we'll work out the least costly one. See " + b("how-long-does-refinancing-take-nz", "how long refinancing takes") + "."),
            ("h3", "If you think you're stuck"),
            ("p", "Low equity, a non-bank loan, self-employed income or a past credit problem don't necessarily mean you can't move. A " + b("dollar-for-dollar-refinance-nz", "dollar-for-dollar refinance") + " is exempt from the Reserve Bank's loan-to-value restrictions, and there's a well-worn path " + b("non-bank-to-bank-refinance-nz", "from non-bank lenders back to banks") + "."),
            ("p", "Sometimes the right answer is to stay and get a better deal from your current bank. We'll tell you when that's the case. " + FEE),
        ],
    },
    "pre-approval.html": {
        "h2": "What a pre-approval is, and what it isn't",
        "guide": [
            ("p", "A pre-approval is a lender's written confirmation that it will lend you up to a stated amount, subject to conditions. It lets you bid at auction, make a firm offer and know your real budget. It costs nothing and doesn't oblige you to borrow."),
            ("h3", "It's conditional"),
            ("p", "Nearly every pre-approval depends on the property being acceptable to the lender and on your circumstances staying the same. The usual conditions are a valuation, insurance, and for some properties a building report or LIM. If you change jobs, take on debt or your income drops before you buy, tell us straight away. See " + b("home-loan-new-job-probation-nz", "changing jobs and home loans") + "."),
            ("h3", "It expires"),
            ("p", "Most pre-approvals last a few months. They can usually be renewed with updated payslips and statements, and the lender reassesses you each time. If yours has run out, read " + b("pre-approval-expired-nz", "what to do when a pre-approval expires") + "."),
            ("h3", "Auctions need extra care"),
            ("p", "An auction purchase is unconditional the moment the hammer falls. Before you bid, have the lender confirm it's happy with that specific property, and get your building report, LIM and legal checks done beforehand. A general pre-approval isn't enough for a leasehold apartment or a house with a weathertightness history. More in " + b("buying-at-auction-nz-finance-ready", "getting finance-ready for auction") + "."),
            ("h3", "What gets a stronger pre-approval"),
            ("p", "Three months of tidy bank statements, low credit card limits, no buy-now-pay-later accounts, and complete documents at the start. Lenders test your budget at a rate above the real one, so small debts matter more than you'd think. " + b("mortgage-stress-test-rate-nz", "How the stress test works") + " explains why."),
            ("p", FEE),
        ],
    },
    "investment-property.html": {
        "h2": "How lenders assess investment property",
        "guide": [
            ("p", "Buying a rental is assessed differently from buying a home. The deposit is bigger, less of the income counts, and the way the lending is set up affects your tax position for years."),
            ("h3", "Deposit and equity"),
            ("p", "The Reserve Bank's loan-to-value rules mean most lenders want around 30% for an existing rental. New builds are exempt and can need less. Most investors don't use cash. They borrow against equity in their own home, which is why a current valuation is often the first step. See " + b("using-home-equity-investment-property-nz", "using home equity to invest") + " and " + b("cash-out-refinance-nz", "releasing equity") + "."),
            ("h3", "Income and debt-to-income limits"),
            ("p", "Lenders count only part of the rent, to allow for vacancies and costs, and they test the loan at a rate above the real one. Banks are also restricted in lending to investors above seven times income. Investors with several properties usually hit the income test before they run out of equity."),
            ("h3", "Structure and tax"),
            ("p", "From 1 April 2025, interest on residential rental borrowing is fully deductible again, according to Inland Revenue. Deductibility follows what the money was used for, so keep rental borrowing in its own loan and never mix it with private spending. Many investors run the rental loan " + b("interest-only-home-loan-nz", "interest-only") + " and pay down their own home first. The bright-line test still applies to sales within two years. We arrange lending, not tax advice, so confirm the tax side with your accountant. Background in " + b("mortgage-interest-tax-deductible-nz", "is mortgage interest deductible?") + "."),
            ("h3", "The property itself"),
            ("p", "Rentals must meet the Healthy Homes standards. Small apartments, leasehold titles and short-stay properties are restricted by many lenders. We don't give advice on which property or area to buy. We can tell you how a lender will see the one you've found."),
            ("p", FEE),
        ],
    },
    "self-employed.html": {
        "h2": "How lenders read self-employed income",
        "guide": [
            ("p", "Being self-employed doesn't make you a worse borrower. It makes you harder to assess, because there's no payslip. The work is in presenting your income so a lender can see it clearly."),
            ("h3", "What lenders usually ask for"),
            ("p", "Two years of financial statements and tax returns, prepared by an accountant. Inland Revenue summaries showing tax and GST are up to date. Business and personal bank statements. Some lenders accept one year if you worked in the same field before going out on your own, which we cover in " + b("one-year-self-employed-mortgage-nz", "one year self-employed") + "."),
            ("h3", "How they calculate your income"),
            ("p", "Most average the last two years, or take the lower year if income has fallen. Many add back non-cash and one-off costs such as depreciation and home office claims. Lenders differ on company profits you haven't paid yourself, and on income split with a partner or trust. Those differences can change your borrowing power by a large amount."),
            ("p", "Accounts written to keep tax low also keep borrowing power low. If you're planning to buy next year, talk to your accountant and to us before the accounts are finalised."),
            ("h3", "When the paperwork doesn't tell the story"),
            ("p", "Some non-bank lenders on our panel assess income from bank statements, GST returns or an accountant's letter. The rates are higher than a bank's. It suits people whose real income is sound but whose accounts haven't caught up, and it should come with a plan to move to a bank later. See " + b("non-bank-to-bank-refinance-nz", "moving from a non-bank lender to a bank") + "."),
            ("h3", "Already have a loan?"),
            ("p", "A new lender will assess your business from scratch, while your current bank can refix you without doing so. That changes the refinance decision. Read " + b("refinance-self-employed-nz", "refinancing when self-employed") + "."),
            ("p", FEE),
        ],
    },
    "construction-loan.html": {
        "h2": "How construction finance works",
        "guide": [
            ("p", "A construction loan isn't paid out in one go. The lender releases money in stages as the build progresses, and you pay interest only on what's been drawn. That keeps costs down during the build. It also means more paperwork than a standard home loan."),
            ("h3", "Turnkey or progress payments"),
            ("p", "With a turnkey contract you pay a deposit and settle when the house is finished, so the builder carries the cost of construction. With a progress-payment build you fund each stage. Turnkey is simpler and you pay no interest until the end. A staged build can cost less and gives you more control. Compare them in " + b("turnkey-home-loan-nz", "turnkey home loans") + " and " + b("construction-loan-progress-payments-nz", "how progress payments work") + "."),
            ("h3", "What lenders want before they'll approve"),
            ("p", "A fixed-price contract with a licensed builder, building consent or consented plans, a valuation of the finished home, and a contingency for overruns. Lenders are cautious about labour-only contracts and owner-managed builds. If you already own the section, your equity in it counts towards your contribution. Buying the land first is covered in " + b("home-loan-for-land-section-nz", "getting a loan for land") + "."),
            ("h3", "Deposits on new builds"),
            ("p", "New builds are exempt from the Reserve Bank's loan-to-value restrictions, so lenders have more room to accept a deposit under 20%. Each sets its own limit, and low-deposit pricing may apply."),
            ("h3", "What goes wrong"),
            ("p", "Delays and cost increases, mostly. Builds take longer than the brochure says, and a pre-approval can expire before the house is finished, so the lender reassesses you at the end. Keep your job and debts steady while you build. Site costs on sloping or poor ground are the most common budget blowout, so get a geotechnical report early."),
            ("p", "Renovating instead of building? Large renovations are funded the same way. See " + b("refinance-for-renovations-nz", "funding a renovation") + ". " + FEE),
        ],
        "steps": [
            ("A first conversation", "We talk through the land, the build, your budget and your income. Free, and no obligation."),
            ("Check the numbers", "We test the whole project: land, build, site works, fees and a contingency. Then we tell you which lenders will fund it and what deposit they'd want."),
            ("Approval", "We submit the application with your plans, contract and valuation. The lender approves the total and the stages."),
            ("Progress payments", "As each stage is finished, the builder invoices, the lender checks the work and releases the payment. We manage the drawdown requests."),
            ("Completion", "Once the code compliance certificate is issued, the loan converts to a standard home loan and we set its long-term structure."),
        ],
        "faqs": [
            ("How much deposit do I need to build a house in NZ?", "Often less than for an existing home, because new builds are exempt from the Reserve Bank's loan-to-value restrictions. Many lenders accept 10% to 20% on a fixed-price contract. If you own the land, your equity in it counts."),
            ("Do I pay interest during the build?", "With a progress-payment loan, yes, but only on the amount drawn so far. With a turnkey contract you don't borrow until the house is finished, so there's no interest during construction."),
            ("What is a progress payment?", "It's a stage payment to your builder, released by the lender when a set part of the build is complete, such as the slab, the frame or the roof. The lender may inspect or ask for evidence before paying."),
            ("Can I get a construction loan for a kitset or relocatable home?", "Sometimes. Fewer lenders fund kitset, prefabricated and relocated homes, and they may release money later in the process. Tell us what you're planning and we'll check which lenders will consider it."),
        ],
    },
    "commercial-property.html": {
        "h2": "How commercial property lending works",
        "guide": [
            ("p", "Commercial lending follows different rules from home loans. Deposits are larger, terms are shorter, and the lender is as interested in the lease and the tenant as it is in you."),
            ("h3", "Deposit"),
            ("p", "Lenders generally advance a smaller share of a commercial property's value than they would for a house, so expect to put in more. The amount depends on the type of property, its location and the strength of the tenancy. You can often use equity in your home or other property towards it."),
            ("h3", "Owner-occupied or investment"),
            ("p", "If your own business will occupy the premises, the lender looks at the business: its accounts, its cash flow and how long it has traded. If you're buying to lease out, the lender looks at the lease. How long it has to run, who the tenant is, and whether the rent comfortably covers the interest all matter. A vacant building is the hardest to finance."),
            ("h3", "How the loan differs"),
            ("p", "Commercial loans are usually reviewed or renewed every few years, even when repayments are worked out over a longer period. Interest rates are set case by case. Lenders may set conditions on the property's value or income that they check during the loan. The consumer protections that apply to home loans mostly don't apply to business lending, so read the documents with your lawyer."),
            ("h3", "Before you sign"),
            ("p", "Get advice on GST, because it depends on whether the sale is a going concern and whether you're registered. Check the building's seismic rating, since many lenders have a minimum. And read the lease in full, including the rent review and renewal terms. Our article on " + b("commercial-property-loan-nz-how-lenders-assess", "how lenders assess commercial property") + " goes further."),
            ("p", FEE_BIZ),
        ],
        "steps": [
            ("A first conversation", "We talk through the property, the tenancy or your business, and what you have to put in. Free, and no obligation."),
            ("Lender options", "We identify which lenders on our panel finance that type of property and what they're likely to need."),
            ("Application", "We prepare the proposal: financial statements, the lease, the valuation and any building reports."),
            ("Offer and due diligence", "You receive the lender's terms. Your lawyer and accountant review them alongside the purchase contract."),
            ("Settlement", "We work with your solicitor to settlement, and note the loan's review date so it doesn't arrive as a surprise."),
        ],
        "faqs": [
            ("How much deposit do I need for commercial property in NZ?", "More than for a home. The amount depends on the property type, location and tenancy, and each lender sets its own maximum. Equity in other property can often be used as part of your contribution."),
            ("Can I use equity in my home to buy commercial property?", "Yes, in many cases. A lender can take security over your home as well as the commercial property. That puts your home at risk if the loan isn't repaid, so get legal advice first."),
            ("Are commercial loan terms shorter than home loans?", "Usually. Many commercial loans are reviewed or renewed every few years, even where repayments are calculated over a longer period. Plan for the review well before it falls due."),
            ("Does Finch charge a fee for commercial lending?", "It depends on the lender and the work involved. We'll tell you about any fee before you commit, and any commission paid by the lender is disclosed in writing."),
        ],
    },
    "asset-finance.html": {
        "h2": "How asset finance works",
        "guide": [
            ("p", "Asset finance pays for vehicles, machinery and equipment, with the item itself as security for the loan. Your cash stays in the business, and you don't need to mortgage your house to buy a truck."),
            ("h3", "The main types"),
            ("p", "With a secured loan, sometimes called a chattel mortgage, you own the asset from the start and the lender registers a security interest over it. With a finance lease, the lender owns it and you pay to use it, usually with the option to buy at the end. With an operating lease, you rent it and hand it back. Each is treated differently for tax and GST, so check with your accountant which suits you. Our article on " + b("asset-finance-chattel-mortgage-lease-hire-purchase-nz", "chattel mortgages, leases and hire purchase") + " compares them."),
            ("h3", "What lenders look at"),
            ("p", "The asset: its age, condition and how easily it could be resold. Common vehicles and equipment are the easiest to finance. Very specialised machinery has fewer willing lenders. And the business: how long it has traded, its accounts or bank statements, and its credit history. New businesses can still be financed, often with a larger deposit or a director's guarantee."),
            ("h3", "Terms"),
            ("p", "Terms usually run from two to five years, and shouldn't be longer than the working life of the asset. Some loans have a larger final payment, which lowers the regular ones and needs planning for. Rates depend on the asset, the term and the strength of the business, so we don't quote them here."),
            ("h3", "Before you sign with the dealer"),
            ("p", "Finance offered at the point of sale is convenient, and it isn't always the cheapest. Compare the total cost over the whole term, including fees and any final payment. If you also have a home loan application coming up, remember that " + b("car-loan-personal-debt-borrowing-power-nz", "vehicle finance reduces what you can borrow") + "."),
            ("p", FEE_BIZ),
        ],
        "steps": [
            ("A first conversation", "Tell us what you're buying, what it costs and a little about the business. Free, and no obligation."),
            ("Lender options", "We check which lenders on our panel finance that kind of asset and what structure suits you."),
            ("Application", "We collect the supplier's quote or invoice and your financial information, and submit the application."),
            ("Approval and documents", "You receive the terms. Once you've signed, the lender pays the supplier directly."),
            ("Delivery", "You take delivery, and repayments start on the agreed schedule."),
        ],
        "faqs": [
            ("What can I finance with asset finance?", "Cars, utes, vans and trucks, trailers, construction and farm machinery, manufacturing equipment, and some office and medical equipment. The easier an item is to value and resell, the more lenders will finance it."),
            ("Do I need a deposit for vehicle or equipment finance?", "Not always. Established businesses with good records can often finance the full price. Newer businesses, older assets and specialised equipment are more likely to need a deposit."),
            ("Can a new business get asset finance?", "Often, yes. Lenders may ask for a deposit, a director's guarantee or evidence of experience in the industry. Tell us how long you've been trading and we'll check which lenders will look at it."),
            ("Does Finch charge a fee for asset finance?", "It depends on the lender and the deal. We'll tell you about any fee before you commit, and any commission paid by the lender is disclosed in writing."),
        ],
    },
}

# Short card and CTA lines on the service pages (exact text nodes).
TEXT_FIXES = {
    "Comprehensive Options": "Fixed, Floating and Split",
    "Stress-Free Process": "We Do the Paperwork",
    "Leverage our broker network to secure rates that banks often don't advertise.": "We ask lenders for their sharpest pricing, not the rate on the website.",
    "Tailored Advice": "A Long-Term Plan",
    "Seamless Timing": "Timing the Two Sales",
    "Equity Unlocking": "Using Your Equity",
    "Leverage the equity built in your current home for your next deposit.": "Use the equity in your current home as the deposit on the next one.",
    "Whether you are up-sizing for a growing family or relocating, navigating the sale of one property while buying another requires precision. Finch handles it all seamlessly.": "Selling one home while buying another takes careful timing. We plan the order, the bridging and the loan so the two line up.",
    "Unlock equity for your upgrade purchase.": "Use your equity for the next purchase.",
    "Unlock equity from existing property to fund your next purchase.": "Use equity in property you already own to fund the next purchase.",
    "Equity Leverage": "Using Equity",
    "Fast NZ pre-approvals tailored for self-employed.": "Pre-approval for self-employed buyers.",
    "Lock in a better NZ rate at fixed-rate roll-off and unlock cashback.": "Compare lenders when your fixed rate ends.",
    "Unlock equity in your home to renovate, invest, or help a family member buy their first home.": "Borrow against your equity to renovate, invest or help a family member buy.",
    "Seamless Switch": "The Switch",
    "Your Journey": "The Process",
    "The whole NZ home loan journey, one stage at a time.": "The NZ home loan process, one stage at a time.",
    "Step-by-step NZ FHB journey.": "Buying a first home, step by step.",
    "Self-employed mortgages<br/><em>are our specialty.</em>": "Self-employed?<br/><em>Let's look at your numbers.</em>",
    "Ready to buy your<br/><em>dream home?</em>": "Ready to buy<br/><em>your home?</em>",
    "Stop overpaying your<br/><em>mortgage today.</em>": "Check what your mortgage<br/><em>should be costing you.</em>",
    "20+ Lenders Compared": "23 Lenders Compared",
}


def block(name, inner):
    return f"<!-- FINCH-{name}:START -->\n{inner}\n<!-- FINCH-{name}:END -->"


def guide_html(cfg):
    out = ""
    for kind, text in cfg["guide"]:
        if kind == "h3":
            out += (f'<h3 style="font-size:1.35rem;font-weight:700;color:var(--neutral-black);'
                    f'margin:2.25rem 0 0.75rem;font-family:var(--font-display);">{text}</h3>\n')
        else:
            out += f'<p style="margin-bottom:1.25rem;">{text}</p>\n'
    return (f'<section style="padding:5rem 0;background:var(--finch-mist);">\n'
            f'<div class="container" style="max-width:800px;">\n'
            f'<div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">\n'
            f'<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;'
            f'font-family:var(--font-display);letter-spacing:-0.02em;">{cfg["h2"]}</h2>\n{out}</div>\n</div>\n</section>')


def steps_html(steps):
    rows = "\n".join(
        f'<div class="process-step reveal"><div class="step-number">{i:02d}</div><div class="step-content">'
        f'<h3>{h}</h3><p>{p}</p></div></div>' for i, (h, p) in enumerate(steps, 1))
    return ('<section style="padding:5rem 0;">\n<div class="container" style="max-width:800px;">\n'
            '<div class="section-label"><span>The Process</span></div>\n'
            '<h2 class="section-heading" style="margin-bottom:3rem;">How it works<br/><em>step by step.</em></h2>\n'
            f'{rows}\n</div>\n</section>')


def faq_section(faqs):
    items = "\n".join(
        f'<div class="faq-item"><button aria-label="Show answer" class="faq-trigger">{escape(q, False)}{CHEV}</button>'
        f'<div class="faq-content">{escape(ans, False)}</div></div>' for q, ans in faqs)
    return ('<section style="padding:4rem 0;background:white;">\n<div class="container" style="max-width:800px;">\n'
            '<h2 class="section-heading" style="margin-bottom:2.5rem;">Common Questions</h2>\n'
            f'{items}\n</div>\n</section>')


def faq_schema(url, faqs):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "@id": f"{url}#faq",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faqs]}
    return ('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, indent=1) + "</script>")


SECTION = re.compile(r"<section\b.*?</section>", re.S)


def swap(html, name, new_inner, finder):
    """Replace an existing marker block, or the first <section> matching `finder`."""
    wrapped = block(name, new_inner)
    pat = re.compile(rf"<!-- FINCH-{name}:START -->.*?<!-- FINCH-{name}:END -->", re.S)
    if pat.search(html):
        return pat.sub(lambda _: wrapped, html, count=1)
    for m in SECTION.finditer(html):
        if finder(m.group(0)):
            return html[:m.start()] + wrapped + html[m.end():]
    raise SystemExit(f"section for {name} not found")


def visible_faqs(html):
    out = []
    for q, ans in re.findall(r'class="faq-trigger"[^>]*>(.*?)<svg.*?</button>\s*<div class="faq-content"[^>]*>(.*?)</div>',
                             html, re.S):
        clean = lambda s: re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", s))).strip()
        out.append((clean(q), clean(ans)))
    return out


def main():
    changed = 0
    for fn, cfg in SERVICES.items():
        path = ROOT / "services" / fn
        src = html = path.read_text(encoding="utf-8")
        url = f"{SITE}/services/{fn[:-5]}"

        html = swap(html, "GUIDE", guide_html(cfg),
                    lambda s: 'class="prose"' in s and len(re.sub(r"<[^>]+>", " ", s).split()) > 450)
        if "steps" in cfg:
            html = swap(html, "STEPS", steps_html(cfg["steps"]),
                        lambda s: "process-step" in s and "step by step" in s)
        if "faqs" in cfg:
            html = swap(html, "FAQ", faq_section(cfg["faqs"]),
                        lambda s: "faq-item" in s and "Common Questions" in s)
        for old, new in TEXT_FIXES.items():
            html = html.replace(f">{old}<", f">{new}<")

        faqs = cfg.get("faqs") or visible_faqs(html)
        if faqs:
            tag = block("FAQSCHEMA", faq_schema(url, faqs))
            pat = re.compile(r"<!-- FINCH-FAQSCHEMA:START -->.*?<!-- FINCH-FAQSCHEMA:END -->\n?", re.S)
            html = pat.sub("", html)
            html = html.replace("</head>", tag + "\n</head>", 1)

        if html != src:
            changed += 1
            if APPLY:
                path.write_text(html, encoding="utf-8")
        print(f"{'~' if html != src else ' '} services/{fn}  faqs in schema: {len(faqs)}")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
