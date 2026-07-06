#!/usr/bin/env python3
"""Generate location-based 'service-city' pages for SEO.

Builds 72 new pages under locations/ (e.g. locations/refinance-auckland.html)
and a directory index page at locations/index.html.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from city_data import CITIES

ROOT = Path(__file__).parent
TEMPLATE_PATH = ROOT / "blog/mortgage-broker-north-shore.html"
OUT_DIR = ROOT / "locations"
BASE_URL = "https://www.finchmortgages.co.nz"

# Filtering the 12 cities requested by the user
TARGET_CITY_SLUGS = {
    "mortgage-broker-auckland-city",
    "mortgage-broker-wellington",
    "mortgage-broker-christchurch",
    "mortgage-broker-hamilton",
    "mortgage-broker-tauranga",
    "mortgage-broker-dunedin",
    "mortgage-broker-queenstown",
    "mortgage-broker-napier-hawkes-bay",
    "mortgage-broker-palmerston-north",
    "mortgage-broker-nelson",
    "mortgage-broker-whangarei-northland",
    "mortgage-broker-manukau",
}

CITIES_FILTERED = [c for c in CITIES if c["slug"] in TARGET_CITY_SLUGS]

SERVICES = [
    {
        "slug": "home-loan",
        "name": "Home Loan",
        "title": "Home Loans & Buying a Home",
        "tagline": "Secure your next residential property with NZ's best lending structures.",
    },
    {
        "slug": "first-home-buyer",
        "name": "First Home Buyer",
        "title": "First Home Buyer Mortgages",
        "tagline": "Navigate KiwiSaver, Home Start grants, and low-deposit options easily.",
    },
    {
        "slug": "refinance",
        "name": "Refinance",
        "title": "Refinance & Restructure Mortgage",
        "tagline": "Save on interest and unlock bank cashback by restructuring your home loan.",
    },
    {
        "slug": "investment-property",
        "name": "Investment Property",
        "title": "Investment Property Loans",
        "tagline": "Maximize leverage and structure portfolio lending tax-effectively.",
    },
    {
        "slug": "self-employed",
        "name": "Self-Employed Mortgage",
        "title": "Self-Employed Home Loans",
        "tagline": "Secure finance using smart profit declarations and low-doc pathways.",
    },
    {
        "slug": "pre-approval",
        "name": "Pre-Approval",
        "title": "Mortgage Pre-Approvals",
        "tagline": "Know your borrowing capacity and bid at auction with absolute confidence.",
    },
]

# Expanded service-specific content generators (humanized Kiwi English copy blocks)
def get_service_prose(service_slug: str, city_name: str, suburbs: str, price_band: str, market_note: str) -> dict:
    clean_city = city_name.replace("&amp;", "&")
    
    if service_slug == "home-loan":
        return {
            "intro": f"Buying a residential home in {clean_city} is a major milestone, but navigating bank scorecards requires a strategic approach. With the Reserve Bank of New Zealand (RBNZ) defining strict lending limits and interest rates shifting, securing a competitive mortgage requires matching your unique financial profile to the right lender. At Finch, we compare your application across 20+ NZ bank and non-bank lenders to construct the sharpest pricing and structure for your new home.",
            "market_angle": f"The local property market in {clean_city} requires a tailored approach depending on the property type. {market_note} Because banks assess older homes, new builds, cross-leases, and lifestyle blocks under completely different policies, securing an independent review of your contract and the property's lendability is essential before making an offer.",
            "eligibility_process": f"To secure a home loan in {clean_city}, banks typically require a 20% deposit, though deposit options as low as 10% (or even 5% for first home buyers) are possible. We analyze your monthly servicing capacity at current bank 'test rates' (often 1.5% to 2% above actual rates) to confirm what you can borrow. The process is straightforward: we complete a discovery call, organize your documents (payslips, tax portals, and bank statement downloads), select the matching lenders, and secure your pre-approval so you can shop with confidence across suburbs like {suburbs}.",
            "extra_sections_html": f"""
            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Understanding Mortgage Structures in {clean_city}</h2>
            <p style="margin-bottom:1rem;">Choosing the right mortgage structure is just as important as securing a low interest rate. A poorly structured home loan can cost you tens of thousands of dollars in unnecessary interest over the life of the loan. When we design your loan, we assess several options:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Fixed-Rate Loans:</strong> Lock in your interest rate for 1 to 5 years. This provides repayment certainty and protects you from rate hikes, which is ideal for budgeting in {clean_city}'s active market.</li>
              <li style="margin-bottom:0.75rem;"><strong>Floating / Variable Loans:</strong> These rates track bank funding costs. While generally higher than fixed rates, floating loans offer maximum flexibility, allowing you to make unlimited extra repayments without penalty.</li>
              <li style="margin-bottom:0.75rem;"><strong>Offset Mortgages:</strong> Link your home loan to your daily savings and transaction accounts. You only pay interest on the net balance, meaning your cash works actively to reduce your mortgage balance every single day.</li>
              <li style="margin-bottom:0.75rem;"><strong>Revolving Credit:</strong> A large overdraft account where your income is deposited directly, keeping your loan balance as low as possible and saving interest on a daily basis.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Our Step-by-Step Home Loan Process</h2>
            <p style="margin-bottom:1.5rem;">Securing a home loan in {clean_city} involves a structured pathway. We guide you through every step to ensure a smooth transaction:</p>
            <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:decimal;color:var(--neutral-medGray);">
              <li style="margin-bottom:1rem;"><strong>Financial Review &amp; Strategy:</strong> We analyze your current income, expenses, debts, and assets to determine your maximum borrowing capacity under current bank stress-testing criteria.</li>
              <li style="margin-bottom:1rem;"><strong>Document Collection:</strong> We help you gather the standard checklist required by lenders: 3 months of bank statements, proof of deposit (KiwiSaver, savings, or gift letters), photo ID, and employment contracts.</li>
              <li style="margin-bottom:1rem;"><strong>Lender Selection &amp; Submission:</strong> We compare your scenario against 20+ NZ bank and non-bank lenders, package your application to highlight its strengths, and submit it to the lenders offering the best terms.</li>
              <li style="margin-bottom:1rem;"><strong>Pre-Approval Secured:</strong> Once the bank issues a pre-approval, you know your exact buying limits, allowing you to bid at auctions or make conditional offers with confidence.</li>
              <li style="margin-bottom:1rem;"><strong>Property Due Diligence:</strong> Before you sign a sale and purchase agreement, we check that the bank accepts the specific property type (e.g. cross-lease, plaster finish, or townhouse zoning).</li>
              <li style="margin-bottom:1rem;"><strong>Loan Structuring &amp; Settlement:</strong> We customize your fixed and floating splits, arrange bank cashbacks, coordinate with your solicitor, and finalize the draw-down on settlement day.</li>
            </ol>
            """,
            "faqs": [
                {
                    "q": f"What deposit do I need to buy a home in {clean_city}?",
                    "a": f"For standard existing homes, a 20% deposit is standard. However, new-build properties across {clean_city} qualify for the main-bank LVR exemption, meaning you may only need a 10% deposit. First home buyers can also access Kāinga Ora programs with as little as 5%."
                },
                {
                    "q": f"How does bank stress-testing affect my borrowing power?",
                    "a": f"When you apply, banks don't test your ability to pay at the current interest rate (e.g., 6.2%). Instead, they stress-test your income at a higher rate (usually 7.5% to 8.0%) to ensure you can handle future rate hikes. Finch knows which lenders have the lowest test rates, which can increase your borrowing capacity."
                },
                {
                    "q": "Are there broker fees for arranging a home loan?",
                    "a": "No, our service is 100% free to you. For standard residential mortgages, the lender pays us a commission upon settlement. This commission does not affect your interest rates or loan terms."
                }
            ]
        }
        
    elif service_slug == "first-home-buyer":
        return {
            "intro": f"Getting onto the property ladder as a first home buyer in {clean_city} can feel daunting with entry-level prices at historical highs. However, Kiwi buyers have access to unique support systems — including KiwiSaver first-home withdrawals, Kāinga Ora First Home Loans, and parental guarantee options. Finch specializes in linking these pathways together, helping first-home buyers secure pre-approvals even with smaller deposits.",
            "market_angle": f"In {clean_city}, entry-level price points vary widely, but new-build townhouses and apartments offer excellent entry opportunities due to lower deposit requirements. {market_note} Understanding how new-build LVR exemptions apply to local developments is a critical shortcut to buying your first home.",
            "eligibility_process": f"First home buyers in {clean_city} should target a minimum 5% deposit for a First Home Loan (available through select lenders like Westpac, Kiwibank, or SBS) or a 10% deposit for new builds. You must have contributed to KiwiSaver for at least 3 years to withdraw your funds, and any parental guarantee must be backed by equity in a NZ residential property. We'll guide you step-by-step: checking your KiwiSaver balances, structuring a family guarantee if needed, packaging your application to demonstrate clean account conduct, and securing a pre-approval so you can negotiate actively.",
            "extra_sections_html": f"""
            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Unlocking Government Support Schemes in {clean_city}</h2>
            <p style="margin-bottom:1rem;">Many first home buyers are unaware of the full range of government support options designed to bridge the deposit gap. We help you check your eligibility for these key programs:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>KiwiSaver First-Home Withdrawal:</strong> If you've been in KiwiSaver for 3+ years, you can withdraw almost all your balance (including tax credits and employer contributions, leaving a $1,000 reserve) to put toward your deposit.</li>
              <li style="margin-bottom:0.75rem;"><strong>Kāinga Ora First Home Loan:</strong> Under this program, the government underwrites your mortgage, allowing participating banks to approve your home loan with just a 5% deposit. Income thresholds apply ($95,000 for single buyers, $150,000 for joint buyers).</li>
              <li style="margin-bottom:0.75rem;"><strong>First Home Partner:</strong> A shared-ownership scheme where Kāinga Ora co-purchases the home with you, taking an equity share of up to 25% or $200,000, which you can buy back over time.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Using a Parental or Family Guarantee</h2>
            <p style="margin-bottom:1.25rem;">If you don't have a 20% deposit and want to avoid high bank low-equity margins (LEMs), a family guarantee is a highly effective option. Here is how we structure guarantees to protect your family while securing your home loan:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Limited Guarantee:</strong> Your parents do not guarantee the entire loan. Instead, they guarantee a specific limited amount (usually the 10% to 15% deposit gap).</li>
              <li style="margin-bottom:0.75rem;"><strong>Security Only:</strong> Lenders secure the guaranteed portion against a limited mortgage on your parents' property, meaning no cash needs to change hands.</li>
              <li style="margin-bottom:0.75rem;"><strong>Exit Strategy:</strong> We map out a plan to release the guarantee as soon as your property value increases or your loan balance decreases to an 80% LVR.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">First Home Buyer Preparation Guide</h2>
            <p style="margin-bottom:1.5rem;">To give yourself the absolute best chance of bank approval, we recommend implementing the following checklist 3 to 6 months before applying:</p>
            <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:decimal;color:var(--neutral-medGray);">
              <li style="margin-bottom:1rem;"><strong>Eliminate Short-Term Debt:</strong> Pay off any hire purchases, credit cards, buy-now-pay-later accounts (like Afterpay), and personal loans. Banks subtract these limits directly from your borrowing capacity.</li>
              <li style="margin-bottom:1rem;"><strong>Show Clean Account Conduct:</strong> Avoid unauthorized overdrafts or unarranged bank fees. Lenders scrutinize every transaction on your last 3 months of bank statements.</li>
              <li style="margin-bottom:1rem;"><strong>Establish a Savings Record:</strong> Regular deposits into a savings account demonstrate to the lender that you have the financial discipline to manage future mortgage repayments.</li>
            </ol>
            """,
            "faqs": [
                {
                    "q": f"Can I use my KiwiSaver as my deposit in {clean_city}?",
                    "a": "Yes! You can withdraw your KiwiSaver contributions, employer contributions, and investment returns (leaving a $1,000 minimum balance) to use as your deposit, provided you have been a member for at least three years."
                },
                {
                    "q": "How does a family guarantee work to bridge the deposit gap?",
                    "a": "A parent or family member can act as a guarantor by securing a portion of your loan (typically up to 20%) against the equity in their own property. This avoids expensive low-equity bank fees and lets you purchase a home without saving a full 20% cash deposit."
                },
                {
                    "q": "What is the Kāinga Ora First Home Loan?",
                    "a": "It is a government-backed program that enables qualified buyers to purchase a home with only a 5% deposit. Income caps apply ($95,000 for single buyers, $150,000 for multiple buyers), and the application must be processed through an approved participating lender."
                }
            ]
        }
        
    elif service_slug == "refinance":
        return {
            "intro": f"Refinancing or restructuring your mortgage in {clean_city} is one of the easiest ways to unlock cashflow savings, but loyalty to a single bank often costs homeowners thousands. NZ lenders constantly offer competitive rate specials and cash incentives to attract existing borrowers. Finch analyzes your current mortgage structure to see if refinancing to another lender makes financial sense once all costs and clawbacks are factored in.",
            "market_angle": f"As {clean_city} property values adjust, refinancing requires an accurate understanding of your current home equity. {market_note} Knowing which lenders accept automated desktop valuations (AVMs) versus which require full registered valuations is crucial to securing a clean restructure without unexpected costs.",
            "eligibility_process": f"To qualify for a premium refinance offer, you generally need at least 20% equity in your property and a clean repayment history for the last 3-6 months. NZ banks regularly offer cash incentives of 0.5% to 0.9% of the total loan amount (up to $10,000 or more) to switch. We model your refinance economics: subtracting bank break fees, existing cashback clawbacks, and legal fees from the new bank's cashback and interest savings to prove your net benefit before any paperwork is signed.",
            "extra_sections_html": f"""
            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Top Reasons to Refinance Your {clean_city} Mortgage</h2>
            <p style="margin-bottom:1rem;">Refinancing is not just about chasing the lowest headline interest rate. We restructure mortgages for clients in {clean_city} to achieve a variety of financial goals:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Securing Bank Cashbacks:</strong> Banks regularly pay cash incentives (typically $2,000 to $8,000+) to switch your loan to them. This cash can cover legal fees and leave you with substantial surplus funds.</li>
              <li style="margin-bottom:0.75rem;"><strong>Debt Consolidation:</strong> If you have short-term debt (credit cards, car loans, or personal loans), we can consolidate them into your home loan, reducing your total monthly payments significantly.</li>
              <li style="margin-bottom:0.75rem;"><strong>Unlocking Equity for Renovations:</strong> Refinancing allows you to top up your loan to fund home improvements, extensions, or landscaping, using your home's capital growth.</li>
              <li style="margin-bottom:0.75rem;"><strong>Altering Loan Terms:</strong> Shortening your term saves thousands in long-term interest, while extending your term reduces your monthly commitment to free up cashflow.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">How We Compute Your Net Refinance Benefit</h2>
            <p style="margin-bottom:1.25rem;">Before making any switch, it is critical to perform a detailed cost-benefit calculation. We map out the exact numbers so you can make an informed decision:</p>
            <div style="background:white;padding:1.5rem;border-radius:1rem;border:1px solid rgba(181,206,176,0.3);margin-bottom:2rem;color:var(--neutral-medGray);">
              <p style="margin-bottom:0.5rem;font-weight:700;color:var(--finch-forest);">The Refinance Formula:</p>
              <p style="font-size:0.95rem;line-height:1.6;font-family:monospace;color:var(--neutral-black);">Net Benefit = (New Bank Cashback + Annual Interest Savings) - (Old Bank Break Fees + Solicitor Fees + Existing Cashback Clawback)</p>
              <p style="margin-top:0.75rem;font-size:0.9rem;">We perform this calculation for you, ensuring that if you switch, you are guaranteed a positive return on your decision.</p>
            </div>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">The Refinancing Process Timeline</h2>
            <p style="margin-bottom:1.5rem;">Switching banks is a straightforward process that typically takes 2 to 4 weeks from submission to settlement. Here is what to expect:</p>
            <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:decimal;color:var(--neutral-medGray);">
              <li style="margin-bottom:1rem;"><strong>Application Packaging:</strong> We collect your current mortgage statements, income verification (payslips/financials), and daily bank statements.</li>
              <li style="margin-bottom:1rem;"><strong>Lender Pricing Negotiation:</strong> We present your file to target lenders, negotiating fixed-rate pricing and cashback offers on your behalf.</li>
              <li style="margin-bottom:1rem;"><strong>Approval &amp; Loan Documents:</strong> Once approved, the new bank issues loan documents which you will sign with your chosen solicitor.</li>
              <li style="margin-bottom:1rem;"><strong>Old Loan Discharge:</strong> Your solicitor requests a discharge of the mortgage from your old bank and coordinates the transfer of funds.</li>
            </ol>
            """,
            "faqs": [
                {
                    "q": "Should I refinance if my fixed term is ending?",
                    "a": f"Absolutely. You should check your refinancing options at least 60 days before your fixed rate rolls off. This gives you time to compare rates across 20+ lenders and negotiate a competitive deal, rather than simply accepting the bank's default roll-over rate."
                },
                {
                    "q": "What is a bank cashback clawback?",
                    "a": "Most banks include a clause stating that if you pay off or move your loan within 3 to 4 years of settlement, you must pay back all or a portion of the cash incentive they gave you. We compute this clawback to ensure your refinance interest savings outweigh any penalty."
                },
                {
                    "q": "Can I consolidate other personal debts into my mortgage refinance?",
                    "a": "Yes. If you have high-interest car loans, credit cards, or personal loans, we can structure your refinance to merge these debts into your mortgage, reducing your overall monthly payments significantly. However, you should aim to pay off this portion faster to avoid paying long-term interest."
                }
            ]
        }
        
    elif service_slug == "investment-property":
        return {
            "intro": f"Building a residential property portfolio in {clean_city} requires a deep understanding of tax structures, equity release, and credit policy. NZ lending rules for investment property are dynamic, with the Reserve Bank's LVR guidelines applying differently depending on whether you are buying an existing rental or a brand-new build. Finch helps investors design optimal multi-lender structures to maximize borrowing capacity and keep investments separate from home equity.",
            "market_angle": f"The local investment environment in {clean_city} highlights unique suburb yields and capital growth profiles. {market_note} Understanding which property types attract rental premiums and how local zoning rules apply is the foundation of a successful investment strategy.",
            "eligibility_process": f"For existing residential investments, NZ banks typically require a 35% or 40% deposit (LVR of 60-65%), whereas new-build investments only require a 20% deposit. Banks assess servicing by applying a 'haircut' (usually counting 70% to 75% of gross rental income) and stress-testing it at current test rates. We help you unlock equity in your owner-occupied home to fund the deposit, set up interest-only terms to optimize tax deductibility, and select lenders that don't cross-collateralize your family home.",
            "extra_sections_html": f"""
            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Structuring Investment Loans for Long-Term Success</h2>
            <p style="margin-bottom:1rem;">How your investment loans are structured is far more important than just interest rates. Proper structuring protects your personal home and ensures your investment is tax-effective:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Avoiding Cross-Collateralisation:</strong> Lenders prefer to secure all your properties under a single mortgage. We structure your loans across different banks so that a sale or valuation change on one property does not freeze funds on the other.</li>
              <li style="margin-bottom:0.75rem;"><strong>Interest-Only Terms:</strong> Paying only the interest portion on your investment properties maximizes tax deductions (where applicable) and frees up cashflow to pay down your non-deductible personal home mortgage.</li>
              <li style="margin-bottom:0.75rem;"><strong>Entity Selection:</strong> We coordinate with your accountant to structure loans under Look-Through Companies (LTCs), family trusts, or partnership entities to optimize tax efficiency and asset protection.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Releasing Equity to Fund Your Deposit</h2>
            <p style="margin-bottom:1.25rem;">Experienced investors rarely fund deposits with cash. Instead, they unlock the equity accumulated in their owner-occupied homes. Here is how we compute usable equity:</p>
            <div style="background:white;padding:1.5rem;border-radius:1rem;border:1px solid rgba(181,206,176,0.3);margin-bottom:2rem;color:var(--neutral-medGray);">
              <p style="margin-bottom:0.5rem;font-weight:700;color:var(--finch-forest);">Usable Equity Calculation:</p>
              <p style="font-size:0.95rem;line-height:1.6;font-family:monospace;color:var(--neutral-black);">Usable Equity = (Current Property Value * 80%) - Existing Mortgage Balance</p>
              <p style="margin-top:0.75rem;font-size:0.9rem;">For example, if your home is worth $1,000,000 and your mortgage is $400,000, your 80% value limit is $800,000, giving you $400,000 in usable equity. This can be topped up to fund the required deposits for new acquisitions.</p>
            </div>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Managing Servicing &amp; LVR Rules in {clean_city}</h2>
            <p style="margin-bottom:1.5rem;">NZ banks analyze your portfolio servicing stringently. We help you package your servicing calculations by optimizing the variables lenders look at:</p>
            <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:decimal;color:var(--neutral-medGray);">
              <li style="margin-bottom:1rem;"><strong>Rental Income Haircuts:</strong> Banks discount your rental income by 25-30% to account for rates, insurance, maintenance, and vacancy. We select lenders that apply the lowest discount.</li>
              <li style="margin-bottom:1rem;"><strong>New Build LVR Exemptions:</strong> Purchasing new-build investment properties exempts you from the strict RBNZ 60-65% LVR limit on existing homes, allowing you to secure investment properties with only a 20% deposit.</li>
              <li style="margin-bottom:1rem;"><strong>Non-Bank Servicing Options:</strong> If main banks decline your application due to debt-to-income (DTI) caps, we access non-bank lenders who test servicing under more flexible parameters.</li>
            </ol>
            """,
            "faqs": [
                {
                    "q": f"What deposit is required for an investment property in {clean_city}?",
                    "a": "Existing houses require a 35% to 40% deposit. However, brand-new builds (including off-the-plan townhouses) are exempt from LVR restrictions, allowing you to secure an investment property with only a 20% deposit."
                },
                {
                    "q": "How do banks calculate rental income for mortgage servicing?",
                    "a": "Banks do not count 100% of your rent. They apply a haircut (typically 25% to 30%) to cover maintenance, rates, insurance, and vacancies, meaning they count 70% to 75% of the gross rent toward your borrowing capacity."
                },
                {
                    "q": "What is cross-collateralisation and why should investors avoid it?",
                    "a": "Cross-collateralisation occurs when a bank uses one mortgage to secure multiple properties (e.g., your home and your investment). If you sell one property, the bank can force you to use the sales proceeds to pay down the other loan. We structure loans across different lenders to prevent this and protect your assets."
                }
            ]
        }
        
    elif service_slug == "self-employed":
        return {
            "intro": f"Being self-employed in {clean_city} comes with business freedom, but securing a home loan can be notoriously difficult. Mainstream banks favor standard PAYE payslips and often struggle to interpret self-employed income statements, shareholder salaries, or company trusts. Finch specializes in self-employed mortgages, packaging complex financials to present the cleanest possible income profile to both main-bank and specialist lenders.",
            "market_angle": f"The self-employed business community in {clean_city} spans construction trades, professional contractors, and retail operators. {market_note} Understanding which NZ lenders assess your business structure favorably is the key to unlocking the borrowing power you've earned.",
            "eligibility_process": f"To secure a standard main-bank loan, you generally need 1 to 2 years of accountant-prepared financial statements, including profit and loss accounts, balance sheets, and personal tax returns (IR3s). However, if you have been trading for less than a year or have complex income splits, we can utilize 'low-doc' pathways with select non-bank lenders who accept GST returns or 6 months of business bank statements. We package your business tax portals, explain any one-off expenses that artificially lower your net profit, and secure pre-approval without forcing you to wait for another financial year.",
            "extra_sections_html": f"""
            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">How NZ Banks Assess Self-Employed Income</h2>
            <p style="margin-bottom:1rem;">Underwriters look at self-employed files with caution because business income can fluctuate. We package your accounts using advanced techniques to ensure banks understand your true earning capacity:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Add-Backs:</strong> We identify non-cash expenses (like vehicle depreciation, home office allowances, or one-off business startup costs) and add them back to your net profit to increase your borrowing power.</li>
              <li style="margin-bottom:0.75rem;"><strong>Shareholder Salary vs. Company Profit:</strong> Main banks assess both your personal salary and your company's retained earnings. We package these together to represent your business's complete servicing strength.</li>
              <li style="margin-bottom:0.75rem;"><strong>Interim Accounts:</strong> If you are applying mid-way through a financial year, we coordinate with your accountant to draft up-to-date profit &amp; loss statements, ensuring the bank sees your current trading volume.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Alternative/Low-Doc Home Loan Options</h2>
            <p style="margin-bottom:1.25rem;">If your tax accounts are not finalized, or you have optimized your business profit to minimize tax, a standard main-bank loan may not be viable. In these scenarios, we utilize low-doc (low-documentation) lending options:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Accountant Declarations:</strong> Select non-bank lenders accept a simple certificate signed by your chartered accountant confirming your business's turnover and estimated profit margin.</li>
              <li style="margin-bottom:0.75rem;"><strong>GST Return Verification:</strong> We can verify your income by submitting your last 12 months of GST returns to the lender, establishing a reliable trend of business activity.</li>
              <li style="margin-bottom:0.75rem;"><strong>Business Bank Statements:</strong> We use your business account statements to analyze cash flow deposits, proving servicing capacity without tax portals.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Document Checklist for Self-Employed Borrowers</h2>
            <p style="margin-bottom:1.5rem;">To speed up your application, we recommend organizing the following financial documents before our consultation:</p>
            <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:decimal;color:var(--neutral-medGray);">
              <li style="margin-bottom:1rem;"><strong>Company Financials:</strong> Last 2 years of Company Profit &amp; Loss Statements and Balance Sheets (prepared by a qualified accountant).</li>
              <li style="margin-bottom:1rem;"><strong>Tax Portals:</strong> Last 2 years of personal IR3 tax returns and your IRD income summaries.</li>
              <li style="margin-bottom:1rem;"><strong>Daily Statements:</strong> 3 months of personal bank statements and 3-6 months of business transaction history to verify account conduct.</li>
            </ol>
            """,
            "faqs": [
                {
                    "q": "What financial records do I need if I'm self-employed?",
                    "a": "Generally, you need the last 2 years of company financial accounts, tax returns (IR3 for individuals, IR4 for companies), and personal tax summaries. However, if these aren't finalized, we can work with interim accounts or GST returns depending on the lender."
                },
                {
                    "q": "Can I get a home loan if I've only been self-employed for one year?",
                    "a": "Yes. While main banks typically require a 2-year history, several non-bank and specialist lenders are comfortable offering home loans with only 12 months of trading history, provided you have a clean credit profile and a solid deposit."
                },
                {
                    "q": "What is a self-employed 'low-doc' home loan?",
                    "a": "A low-documentation (low-doc) loan is designed for self-employed borrowers who do not have fully completed tax accounts. Lenders verify income using alternative methods, such as an accountant declaration, GST returns, or business bank statements. These loans typically require a 20% deposit."
                }
            ]
        }
        
    elif service_slug == "pre-approval":
        return {
            "intro": f"Entering the {clean_city} real estate market without a binding mortgage pre-approval is like bidding at an auction blindfolded. In a fast-paced market where conditional offers are routinely rejected in favor of unconditional buyers, having a pre-approval gives you the leverage to negotiate with certainty. Finch coordinates with 20+ NZ lenders to secure pre-approvals quickly, keeping you ahead of the competition.",
            "market_angle": f"With auctions and quick tenders dominating the {clean_city} sales landscape, a pre-approval is your ticket to participate. {market_note} Knowing your buying capacity and deposit rules before you start visiting open homes is the best way to avoid missing out.",
            "eligibility_process": f"To qualify for a pre-approval, you must submit a complete financial profile demonstrating servicing capacity and a verified deposit source (cash, KiwiSaver, or equity). Pre-approvals are generally valid for 90 days, allowing you to bid at auction or make unconditional offers. The process involves organizing your checklist, matching your files to the right bank's scorecard, and securing the approval letter. We will review any property you want to offer on to ensure the bank accepts that specific property type.",
            "extra_sections_html": f"""
            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Why Pre-Approval is Critical in {clean_city}</h2>
            <p style="margin-bottom:1rem;">In New Zealand, many properties are sold via auction or deadline sale. If you bid at auction, your bid is legally binding and completely unconditional. Without pre-approval, bidding is extremely risky:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Auction Ready:</strong> A pre-approval allows you to complete due diligence on the property (such as building reports and title checks) and bid unconditionally on auction day.</li>
              <li style="margin-bottom:0.75rem;"><strong>Negotiation Power:</strong> Sellers prefer cash buyers or unconditional offers. A pre-approved buyer can negotiate a lower purchase price by offering a quick, hassle-free settlement.</li>
              <li style="margin-bottom:0.75rem;"><strong>Budget Security:</strong> Knowing your exact spending limit stops you from falling in love with properties that exceed your bank's borrowing criteria.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Common Conditions on Pre-Approvals</h2>
            <p style="margin-bottom:1.25rem;">A pre-approval is rarely unconditional. Lenders issue them with a list of conditions that must be met before they release the funds. We work with you to clear these conditions systematically:</p>
            <ul style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:disc;color:var(--neutral-medGray);">
              <li style="margin-bottom:0.75rem;"><strong>Registered Valuation:</strong> Lenders may require a valuation from an approved panel (like Valocity or CoreLogic) to confirm the property matches the purchase price.</li>
              <li style="margin-bottom:0.75rem;"><strong>Building Report:</strong> For older properties, plaster finishes, or suspected weather-tightness issues, banks require a comprehensive invasive or non-invasive moisture test report.</li>
              <li style="margin-bottom:0.75rem;"><strong>KiwiSaver Withdrawal Confirmation:</strong> Proof that your KiwiSaver funds have been approved for release by your provider.</li>
              <li style="margin-bottom:0.75rem;"><strong>Clean Title Review:</strong> The bank's legal department must review the title (e.g. fee simple, cross-lease, or unit title) to ensure no restrictive easements exist.</li>
            </ul>

            <h2 style="font-size:1.75rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.25rem;margin-top:2.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">How to Maintain Your Pre-Approval Status</h2>
            <p style="margin-bottom:1.5rem;">Once your pre-approval is issued, it is valid for 90 days. However, the bank can revoke it if your financial situation changes. To protect your approval, follow these guidelines:</p>
            <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style-type:decimal;color:var(--neutral-medGray);">
              <li style="margin-bottom:1rem;"><strong>Do Not Take on New Debt:</strong> Avoid buying new cars, opening store credit accounts, or signing up for interest-free hire purchases.</li>
              <li style="margin-bottom:1rem;"><strong>Maintain Your Current Employment:</strong> Do not change jobs, resign to start a business, or transition to a commission-only role without consulting us first.</li>
              <li style="margin-bottom:1rem;"><strong>Protect Your Deposit:</strong> Keep your deposit funds safe in a savings account. Do not spend portion of your deposit or invest it in high-risk assets.</li>
            </ol>
            """,
            "faqs": [
                {
                    "q": "How long does it take to get a mortgage pre-approval?",
                    "a": f"For standard scenarios in {clean_city}, pre-approvals are typically processed in 3 to 5 working days. More complex files (self-employed or low-deposit) can take 7 to 10 working days. We recommend applying before you begin house hunting."
                },
                {
                    "q": "What does a pre-approval 'condition' mean?",
                    "a": "Almost all pre-approvals are issued with conditions, such as obtaining a registered valuation, confirming clean building reports, or providing updated bank statements. You must satisfy these conditions before the bank makes the loan unconditional."
                },
                {
                    "q": "Can I bid at an auction with a pre-approval?",
                    "a": "Yes, but you must ensure the bank has approved the specific property you are bidding on and that any conditions on your pre-approval have been resolved. Bidding at auction commits you unconditionally, so you must have the bank's final sign-off before raising your hand."
                }
            ]
        }
    return {}

def build_page_html(c: dict, s: dict, template_text: str) -> str:
    city = c["city"]
    region = c["region"]
    service_name = s["name"]
    service_title = s["title"]
    
    slug = f"{s['slug']}-{c['slug'].replace('mortgage-broker-', '')}"
    canonical = f"{BASE_URL}/locations/{slug}.html"
    
    article = "an" if service_name[0] in "AEIOU" else "a"
    title = f"{service_name} in {city.replace('&amp;', '&')} | Finch Mortgages NZ"
    description = f"Looking for {article} {service_name} in {city.replace('&amp;', '&')}? Finch compares 20+ NZ lenders to get you approved fast. $0 broker fee. Secure your loan →"
    
    prose = get_service_prose(s["slug"], city, c["suburbs"], c["price_band"], c["market_note"])
    
    # 1. Update Head Section
    head_close = template_text.find("</head>")
    head = template_text[:head_close]
    
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
    
    # Build Schemas
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Locations", "item": f"{BASE_URL}/locations/index.html"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{service_name} in {city.replace('&amp;', '&')}",
                "item": canonical,
            },
        ],
    }
    
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{service_name} Brokerage in {city.replace('&amp;', '&')}",
        "provider": {
            "@type": "MortgageBroker",
            "name": "Finch Mortgages",
            "url": f"{BASE_URL}/",
            "logo": f"{BASE_URL}/images/finch-logo.png",
        },
        "areaServed": {"@type": "Place", "name": region.replace("&amp;", "&")},
        "description": description,
    }
    
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
            }
            for faq in prose["faqs"]
        ],
    }
    
    schemas_html = f"""<script type="application/ld+json">
{json.dumps(breadcrumb_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(service_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
</script>"""

    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        lambda _m: schemas_html,
        head,
        count=1,
        flags=re.S,
    )
    # Remove second schema script block if present in template head to keep it clean
    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        "",
        head,
        flags=re.S,
    )
    head += "</head>"

    # 2. Get Footer wrapper from template
    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]
    
    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]
    
    # FAQ Accordion HTML builder
    faq_items_html = ""
    for faq in prose["faqs"]:
        faq_items_html += f"""
        <div class="faq-item" style="border:1px solid rgba(180,178,169,0.2);border-radius:1rem;background:white;overflow:hidden;">
          <button class="faq-trigger" style="width:100%;text-align:left;padding:1.25rem 1.5rem;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:1.05rem;background:none;border:none;cursor:pointer;color:var(--neutral-black);">
            <span>{faq['q']}</span>
            <svg fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" style="transition:transform 0.3s;" viewbox="0 0 24 24" width="16"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
          <div class="faq-content" style="display:none;padding:0 1.5rem 1.25rem 1.5rem;color:var(--neutral-medGray);line-height:1.7;font-size:0.95rem;border-top:1px solid rgba(180,178,169,0.1);padding-top:1rem;">
            <p>{faq['a']}</p>
          </div>
        </div>"""

    # 3. Main body construction
    body_html = textwrap.dedent(f"""
    <main style="padding-top:80px;">
      <!-- Hero -->
      <section class="container page-hero" style="padding-top:4rem;padding-bottom:4rem;">
        <div class="reveal" style="max-width:800px;">
          <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="index.html">Locations</a><span class="breadcrumb-sep">/</span><span>{service_name} {city.replace('&amp;', '&')}</span></nav>
          <div class="page-hero-tag">Local NZ Coverage · {region}</div>
          <h1>{service_name}<br/><em style="font-style:italic;color:var(--finch-forest);">{city.replace('&amp;', '&')}.</em></h1>
          <p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: July 2026</p>
          <p>{s['tagline']}</p>
          <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
            <a class="btn-primary" href="../contact.html">Book a Free 15-Minute Call</a>
            <a class="btn-secondary" href="../mortgage-rates.html">View Live NZ Rates</a>
          </div>
        </div>
      </section>

      <!-- Body -->
      <section style="padding:4rem 0;background:var(--finch-mist);">
        <div class="container" style="max-width:800px;">
          <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
            <h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Expert {service_name} Advice in {city.replace('&amp;', '&')}</h2>
            <p style="margin-bottom:2rem;">{prose['intro']}</p>

            <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{city.replace('&amp;', '&')} Property Market Realities</h3>
            <p style="margin-bottom:2rem;">{prose['market_angle']}</p>

            <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Eligibility &amp; Mortgage Process</h3>
            <p style="margin-bottom:2rem;">{prose['eligibility_process']}</p>

            {prose['extra_sections_html']}

            <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Cost of Our Broker Services</h3>
            <p style="margin-bottom:2rem;">For residential mortgages and home loan restructuring in {city.replace('&amp;', '&')}, Finch charges you $0. We are compensated by the selected bank or lender upon settlement of your loan. Our independent status means we are regulated under the Financial Markets Conduct Act to act solely in your best interest, matching you to the ideal rate and structure across all major banks and non-bank lenders.</p>
          </div>
        </div>
      </section>

      <!-- Local FAQ Section -->
      <section style="padding:4rem 0;background:white;">
        <div class="container" style="max-width:800px;">
          <h2 id="faq-section" style="font-family:var(--font-display);font-size:2rem;color:var(--neutral-black);margin-bottom:1.5rem;text-align:center;">{service_name} FAQ for {city.replace('&amp;', '&')} Buyers</h2>
          <div class="faq-accordion" style="display:flex;flex-direction:column;gap:1rem;margin-bottom:2rem;">
            {faq_items_html}
          </div>
        </div>
      </section>

      <!-- Related NZ Resources -->
      <section style="padding:4rem 0;background:white;border-top:1px solid rgba(180,178,169,0.15);">
        <div class="container" style="max-width:1000px;">
          <div class="section-label"><span>Keep Reading</span></div>
          <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ mortgage resources</h2>
          <div class="cols-3" style="gap:1.5rem;">
            <a href="../services/home-loan.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Home Loan Service</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Independent advice across 20+ NZ lenders.</span></a>
            <a href="../calculators/borrowing-power.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Borrowing Power</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">See how much NZ banks will lend you.</span></a>
            <a href="../calculators/mortgage-calculator.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Mortgage Calculator</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Estimate repayments at NZ rates.</span></a>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section style="padding:5rem 0;background:var(--finch-mist);">
        <div class="container">
          <div class="cta-section reveal">
            <h2>Ready to talk to a local expert?</h2>
            <p>Book a free, no-obligation call with our advisers to discuss {service_name} solutions in {city.replace('&amp;', '&')}.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
              <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
              <a class="btn-cta-outline" href="../mortgage-rates.html">View Live NZ Rates</a>
            </div>
          </div>
        </div>
      </section>
    </main>
    """)

    return head + "\n" + body_open + body_html + footer

def generate_hub_html(template_text: str) -> str:
    title = "Our Service Locations | Finch Mortgages NZ"
    description = "Browse Finch Mortgages local home loan and advisory services across major New Zealand cities. $0 fee, independent advice."
    canonical = f"{BASE_URL}/locations/index.html"
    
    # Update Head
    head_close = template_text.find("</head>")
    head = template_text[:head_close]
    
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
    
    # Schema for Hub
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Locations", "item": canonical},
        ],
    }
    
    schemas_html = f"""<script type="application/ld+json">
{json.dumps(breadcrumb_schema, indent=2)}
</script>"""

    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        lambda _m: schemas_html,
        head,
        count=1,
        flags=re.S,
    )
    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        "",
        head,
        flags=re.S,
    )
    head += "</head>"

    # Get body open and footer
    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]
    
    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]

    # Generate Grid content
    grid_html = ""
    for s in SERVICES:
        links_html = ""
        for c in CITIES_FILTERED:
            city_display = c["city"].replace("&amp;", "&")
            slug = f"{s['slug']}-{c['slug'].replace('mortgage-broker-', '')}.html"
            links_html += f"""
            <a href="{slug}" style="display:block;padding:0.75rem 1rem;background:white;border:1px solid rgba(181,206,176,0.4);border-radius:0.5rem;text-decoration:none;color:var(--finch-forest);font-weight:600;font-size:0.9rem;transition:all 0.2s;" onmouseover="this.style.background='var(--finch-mist)'" onmouseout="this.style.background='white'">{s['name']} in {city_display}</a>"""
        
        grid_html += f"""
        <div style="background:var(--finch-mist);padding:2rem;border-radius:1rem;border:1px solid rgba(98,162,154,0.15);margin-bottom:2rem;">
          <h3 style="font-family:var(--font-display);font-size:1.25rem;font-weight:700;color:var(--neutral-black);margin-bottom:0.5rem;border-bottom:2px solid var(--finch-sage);padding-bottom:0.5rem;">{s['title']}</h3>
          <p style="font-size:0.85rem;color:var(--neutral-medGray);margin-bottom:1.5rem;line-height:1.4;">{s['tagline']}</p>
          <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));gap:0.75rem;">
            {links_html}
          </div>
        </div>"""

    body_html = textwrap.dedent(f"""
    <main style="padding-top:80px;">
      <section class="container page-hero" style="padding-top:4rem;padding-bottom:3rem;">
        <div class="reveal" style="max-width:800px;">
          <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><span>Locations</span></nav>
          <div class="page-hero-tag">NZ-Wide Expertise</div>
          <h1>Finch Service Locations</h1>
          <p style="font-size:1.15rem;color:var(--neutral-medGray);margin-top:1rem;line-height:1.7;">Independent, $0-fee mortgage advice blended with local market insights. Choose your service and city combination below to view detailed criteria, price bands, and local processes.</p>
        </div>
      </section>

      <section style="padding:4rem 0;background:white;">
        <div class="container">
          {grid_html}
        </div>
      </section>
    </main>
    """)
    
    return head + "\n" + body_open + body_html + footer

def main() -> None:
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for s in SERVICES:
        for c in CITIES_FILTERED:
            slug = f"{s['slug']}-{c['slug'].replace('mortgage-broker-', '')}.html"
            out_path = OUT_DIR / slug
            
            page_content = build_page_html(c, s, template_text)
            out_path.write_text(page_content, encoding="utf-8")
            count += 1
            
    # Generate the hub page
    hub_content = generate_hub_html(template_text)
    (OUT_DIR / "index.html").write_text(hub_content, encoding="utf-8")
    
    print(f"Generated {count} service-city location pages.")
    print("Generated locations/index.html hub page.")

if __name__ == "__main__":
    main()
