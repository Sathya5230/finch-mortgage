"""Build the break fee, LVR, interest-only and cashback clawback calculators.

Each page reuses the head, header and footer of calculators/dti-calculator.html
and swaps in its own metadata, schema, body and script, so sitewide injections
on that page carry over. Safe to re-run: pages are rebuilt from PAGES each time.
Edit the copy here, not in the generated HTML, then run the post-generation
pipeline (inject_local_seo.py, build_internal_links.py, strip_html_ext.py).

Figures to re-check yearly: the Reserve Bank LVR settings on the LVR page
(25% of owner-occupier lending above 80%, 10% of investor lending above 70%,
in place since 1 December 2025 and kept at the August 2026 review).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SHELL = ROOT / "calculators" / "dti-calculator.html"
BASE = "https://www.finchmortgages.co.nz"
TODAY = "2026-11-13"
UPDATED = "November 2026"

H3 = 'style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;"'
A = 'style="color:var(--finch-forest);text-decoration:underline;font-weight:600;"'
SELECT = 'style="width:100%;padding:0.75rem 1rem;border-radius:0.75rem;border:1px solid rgba(98,162,154,0.35);font-family:inherit;font-size:0.95rem;"'


def money(label, id_, value):
    return (f'<div class="calc-input-group">\n<label for="{id_}">{label}</label>\n'
            f'<div class="calc-input-row"><span>$</span><input id="{id_}" type="number" min="0" value="{value}"/></div>\n</div>')


def number(label, id_, value, unit, step="1"):
    return (f'<div class="calc-input-group">\n<label for="{id_}">{label}</label>\n'
            f'<div class="calc-input-row"><input id="{id_}" type="number" min="0" step="{step}" value="{value}"/><span>{unit}</span></div>\n</div>')


def select(label, id_, options):
    opts = "".join(f'<option value="{v}">{t}</option>' for v, t in options)
    return (f'<div class="calc-input-group">\n<label for="{id_}">{label}</label>\n'
            f'<select id="{id_}" {SELECT}>{opts}</select>\n</div>')


FMT = 'function $(i){return document.getElementById(i)}function v(i){return parseFloat($(i).value)||0}function m(n){return"$"+Math.round(Math.abs(n)).toLocaleString("en-NZ")}'

PAGES = [
    {
        "slug": "break-fee-calculator",
        "crumb": "Break Fee",
        "name": "Mortgage Break Fee Calculator NZ",
        "title": "Mortgage Break Fee Calculator NZ | Estimate the Cost | Finch",
        "desc": "Estimate the break fee on a fixed-rate NZ home loan, then see whether switching to a lower rate still leaves you ahead after legal fees and cashback.",
        "app_desc": "Estimates the early repayment charge for breaking a fixed-rate New Zealand home loan and the net result of switching to a lower rate.",
        "h1": "Mortgage Break Fee<br/><em style=\"font-style:italic;color:var(--finch-forest);\">Calculator NZ</em>",
        "intro": "Estimate what it could cost to break your fixed rate early, and whether moving to a lower rate would still leave you ahead once the fee, legal costs and any cashback are counted.",
        "widget_title": "Break fee estimator",
        "widget_sub": "An estimate only. Your bank's quote is the real figure.",
        "inputs": [
            money("Loan balance on this fixed rate", "bf-bal", 500000),
            number("Your current fixed rate", "bf-rate", "6.49", "% p.a.", "0.01"),
            number("Months left on the fixed term", "bf-months", 18, "months"),
            number("Your bank's rate today for a term close to the time you have left", "bf-cur", "4.99", "% p.a.", "0.01"),
            number("Rate you could move to", "bf-new", "4.89", "% p.a.", "0.01"),
            money("Legal fees if you change lender", "bf-legal", 1500),
            money("Cashback offered by the new lender", "bf-cash", 0),
        ],
        "button": "Estimate my break fee",
        "result_label": "Estimated break fee",
        "result_id": "bf-fee",
        "sub_id": "bf-sub",
        "rows": [("Interest saved at the new rate until your term would have ended", "bf-save"),
                 ("Legal fees less cashback", "bf-costs"),
                 ("Net result of breaking", "bf-net")],
        "note": "This estimate compares your fixed rate with your bank's current rate for the time you have left. Many banks work from wholesale rates instead, and include other factors, so their figure can be higher or lower. It assumes the balance stays the same over the remaining term. Ask your bank for a written break cost quote before you decide.",
        "side_title": "What moves a break fee",
        "side": [
            ("How far rates have fallen", "The fee reflects the gap between the rate you fixed at and the rate the bank could lend the same money at today. No fall usually means little or no fee."),
            ("How much is fixed", "The fee scales with the balance. If only part of your loan is on the fixed rate you want to break, enter that part."),
            ("How long is left", "Eighteen months left costs roughly three times as much as six months left on the same loan and rates."),
            ("Your bank's own method", "Banks must explain how they calculate the charge. The exact figure changes daily, so a quote is only good for a short time."),
        ],
        "cta_title": "Thinking about breaking a fixed rate?",
        "cta": "Send us your bank's break cost quote and we'll work through the numbers with you, including clawback on any cashback you've received. There's no fee for residential home loans.",
        "body": f"""
<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">How mortgage break fees work in NZ</h2>
<p style="margin-bottom:2rem;">A break fee, which banks call an early repayment charge or early repayment recovery, applies when you repay or refinance a fixed-rate loan before the fixed term ends. It can also apply to a large lump-sum repayment. The charge compensates the bank when interest rates have fallen since you fixed, because it can only re-lend your money at a lower rate.</p>
<h3 {H3}>How the fee is calculated</h3>
<p style="margin-bottom:2rem;">Early repayment charges on home loans are regulated by the Credit Contracts and Consumer Finance Act 2003. The regulations set out a formula lenders may use. A lender can use its own method instead, as long as the result is a reasonable estimate of its loss, and it has to tell you which method it uses and how the charge is worked out. The Banking Ombudsman notes that many banks base the charge on the difference between wholesale interest rates when you fixed and when you repay.</p>
<p style="margin-bottom:2rem;">You can't look up the wholesale rates a bank uses, so this calculator works from advertised rates: your fixed rate, less the bank's current rate for a term close to the time you have left, multiplied by the balance and the time remaining. On $500,000 fixed at 6.49% with 18 months to run, and a current 18-month rate of 4.99%, that comes to about $11,250. Treat it as a guide to the size of the number, then get the real one from your bank.</p>
<h3 {H3}>When there's no break fee</h3>
<ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">
<li style="margin-bottom:0.5rem;">Rates are the same or higher than when you fixed. The bank hasn't lost anything by getting its money back early.</li>
<li style="margin-bottom:0.5rem;">Your loan is floating or on revolving credit. Break fees apply only to fixed rates.</li>
<li style="margin-bottom:0.5rem;">You wait for the fixed term to end. Refinancing on the expiry date avoids the fee entirely.</li>
<li style="margin-bottom:0.5rem;">You stay within your bank's extra repayment allowance. Most banks let you pay a set amount off a fixed loan each year without a charge, and the amount differs by bank.</li>
</ul>
<h3 {H3}>Is breaking worth it?</h3>
<p style="margin-bottom:2rem;">Breaking pays only when what you gain is clearly more than what it costs. On the gain side are the interest you save at the lower rate until your old term would have ended, and any cashback from a new lender. On the cost side are the break fee, legal fees if you change lender, and any cashback you have to repay to your current bank. Our <a href="../calculators/cashback-clawback-calculator" {A}>cashback clawback calculator</a> estimates that last one.</p>
<p style="margin-bottom:2rem;">Because the fee is designed to recover the bank's loss, the interest you save by breaking is often close to the fee you pay. That's why the result above is frequently near zero. Breaking tends to make sense when you need to restructure or sell anyway, or when a new lender's offer tips the balance.</p>
<h3 {H3}>Getting your bank's figure</h3>
<p style="margin-bottom:0;">Ask your bank for a break cost quote in writing. It's free, and it's the only figure that counts. For the full picture, read our guide to <a href="../blog/break-fixed-mortgage-break-fees-nz" {A}>breaking a fixed mortgage in NZ</a>, or run a switch through the <a href="../calculators/refinance-savings" {A}>refinance savings calculator</a>.</p>
""",
        "faqs": [
            ("How much is a mortgage break fee in NZ?", "It depends on how far interest rates have fallen since you fixed, how much is fixed and how long is left on the term. If rates are the same or higher than when you fixed, the fee is usually small or nil. Only your bank can give the exact figure."),
            ("How do I find out my exact break fee?", "Ask your bank for a break cost quote in writing. Quotes are free. The figure changes daily with interest rates, so a quote is only valid for a short time."),
            ("Can a break fee be waived or negotiated?", "You can ask, but the bank doesn't have to agree. The Banking Ombudsman's guidance is to assume the charge will apply in full."),
            ("Does a break fee apply when I sell my house?", "It can, if you repay a fixed-rate loan before the term ends. If you're buying again, ask your bank whether the loan can be moved to the new property, which may avoid the charge."),
        ],
        "related": [
            ("../blog/break-fixed-mortgage-break-fees-nz", "Breaking a Fixed Mortgage", "When breaking early pays and when it doesn't."),
            ("../calculators/refinance-savings", "Refinance Savings Calculator", "Compare your current loan with a new one."),
            ("../calculators/cashback-clawback-calculator", "Cashback Clawback Calculator", "What you'd repay if you left today."),
            ("../blog/fixed-rate-ending-refix-guide-nz", "Fixed Rate Ending?", "Your options when a fixed term rolls off."),
            ("../blog/refinance-costs-nz", "Refinance Costs in NZ", "Every cost of switching lender."),
            ("../services/refinance", "Refinance With Finch", "We compare 23 lenders and handle the switch."),
        ],
        "script": FMT + 'function calcBF(){var b=v("bf-bal"),r=v("bf-rate"),mo=v("bf-months"),c=v("bf-cur"),n=v("bf-new"),l=v("bf-legal"),k=v("bf-cash"),fee=Math.max(0,(r-c)/100*b*mo/12),save=(r-n)/100*b*mo/12,net=save+k-fee-l;$("bf-fee").textContent="~"+m(fee);$("bf-sub").textContent=fee>0?"Based on a "+(r-c).toFixed(2)+" point fall in rates over "+mo+" months":"Rates haven\'t fallen since you fixed, so the fee is likely to be small or nil";$("bf-save").textContent=(save<0?"−":"")+m(save);$("bf-costs").textContent=(k-l<0?"−":"+")+m(k-l);$("bf-net").textContent=net>=0?"About "+m(net)+" ahead":"About "+m(net)+" behind";$("bf-net").style.color=net>=0?"var(--finch-forest)":"#b5462f"}calcBF();',
        "fn": "calcBF()",
    },
    {
        "slug": "lvr-calculator",
        "crumb": "LVR",
        "name": "LVR Calculator NZ",
        "title": "LVR Calculator NZ | Loan-to-Value Ratio & Deposit | Finch",
        "desc": "Work out your loan-to-value ratio (LVR) and deposit percentage, and see where you sit against the Reserve Bank's 80% and 70% LVR limits.",
        "app_desc": "Calculates loan-to-value ratio and deposit percentage against the Reserve Bank of New Zealand's LVR restrictions for owner-occupiers and investors.",
        "h1": "LVR Calculator<br/><em style=\"font-style:italic;color:var(--finch-forest);\">New Zealand</em>",
        "intro": "Enter the property value and your deposit or equity to see your loan-to-value ratio, and how much more you'd need to reach the 80% owner-occupier or 70% investor mark.",
        "widget_title": "LVR calculator",
        "widget_sub": "For a purchase, use the price. For a refinance, use the current value.",
        "inputs": [
            money("Property value or purchase price", "lv-val", 800000),
            money("Deposit or equity", "lv-dep", 120000),
            select("Buyer type", "lv-type", [("80", "Owner-occupier (80% LVR limit)"), ("70", "Investor (70% LVR limit)")]),
            select("Property type", "lv-new", [("0", "Existing home"), ("1", "New build")]),
        ],
        "button": "Calculate my LVR",
        "result_label": "Your LVR",
        "result_id": "lv-lvr",
        "sub_id": "lv-sub",
        "rows": [("Loan amount", "lv-loan"), ("Deposit", "lv-pct"), ("Extra deposit to reach the limit", "lv-gap")],
        "note": "A guide only. Lenders use the lower of the purchase price and their own valuation, and each sets its own maximum LVR for different property types. Being under the limit doesn't guarantee approval, which also depends on income, expenses and credit history.",
        "side_title": "Reading your result",
        "side": [
            ("LVR is loan divided by value", "Borrowing $680,000 against an $800,000 property is an LVR of 85%, which is the same as a 15% deposit."),
            ("80% for owner-occupiers", "Banks can make up to 25% of their new owner-occupier lending above 80% LVR, so low-deposit loans exist but are rationed."),
            ("70% for investors", "Banks can make up to 10% of their new investor lending above 70% LVR, so most investors need 30% equity in an existing property."),
            ("New builds are exempt", "Loans to buy or build a new home sit outside the Reserve Bank's LVR restrictions. Each lender still sets its own minimum deposit."),
        ],
        "cta_title": "Under 20% deposit?",
        "cta": "Lenders differ on how much low-deposit lending they will do and what they charge for it. We can tell you which of the 23 lenders on our panel suit your deposit, at no fee for residential home loans.",
        "body": f"""
<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">How LVR works in New Zealand</h2>
<p style="margin-bottom:2rem;">Loan-to-value ratio is the size of your loan as a percentage of the property's value. A $640,000 loan on an $800,000 home is an LVR of 80%. The lower the LVR, the more of the property you own outright, and the less risk the lender carries.</p>
<h3 {H3}>The Reserve Bank's current LVR limits</h3>
<p style="margin-bottom:1rem;">The Reserve Bank of New Zealand limits how much high-LVR lending each bank can do. The current settings have applied since 1 December 2025, and the Reserve Bank kept them unchanged at its review in August 2026:</p>
<ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">
<li style="margin-bottom:0.5rem;"><strong>Owner-occupiers:</strong> up to 25% of a bank's new lending can be above 80% LVR, meaning a deposit under 20%.</li>
<li style="margin-bottom:0.5rem;"><strong>Investors:</strong> up to 10% of a bank's new lending can be above 70% LVR, meaning a deposit under 30%.</li>
<li style="margin-bottom:0.5rem;"><strong>Exemptions:</strong> new builds and Kāinga Ora First Home Loans are among the loans that sit outside these limits.</li>
</ul>
<p style="margin-bottom:2rem;">These are limits on banks, not on borrowers. A bank that has used up its allowance for the month may decline a low-deposit application that another bank would accept. Non-bank lenders aren't covered by the restrictions and set their own limits.</p>
<h3 {H3}>What a high LVR costs</h3>
<p style="margin-bottom:2rem;">Borrowers above 80% LVR usually pay more. Depending on the lender, that's a margin added to the interest rate or a one-off fee, and the size goes up as the deposit gets smaller. You're also less likely to be offered a bank's sharpest rates or a cashback. Our guide to the <a href="../blog/low-equity-margin-fee-nz" {A}>low equity margin</a> explains how it's charged and how to get it removed.</p>
<h3 {H3}>Ways to lower your LVR</h3>
<ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">
<li style="margin-bottom:0.5rem;">Add to the deposit with a <a href="../blog/kiwisaver-first-home-withdrawal" {A}>KiwiSaver first-home withdrawal</a> or a <a href="../blog/gifted-deposit-home-loan-nz" {A}>gifted deposit</a>.</li>
<li style="margin-bottom:0.5rem;">Use a family member's equity as extra security through a <a href="../blog/guarantor-home-loan-nz" {A}>guarantee</a>.</li>
<li style="margin-bottom:0.5rem;">If you already own the property, pay down the loan or get an updated valuation once the value has risen.</li>
<li style="margin-bottom:0.5rem;">Buy a new build, which is exempt from the Reserve Bank's limits.</li>
</ul>
<h3 {H3}>LVR isn't the only test</h3>
<p style="margin-bottom:0;">A lender also checks that you can afford the repayments at a higher test rate, and that your total debt fits within the <a href="../calculators/dti-calculator" {A}>debt-to-income limits</a>. To see how the three fit together, read <a href="../blog/what-is-lvr-nz-mortgage" {A}>what LVR means for a NZ mortgage</a> or try the <a href="../calculators/borrowing-power" {A}>borrowing power calculator</a>.</p>
""",
        "faqs": [
            ("How do I calculate LVR?", "Divide the loan amount by the property's value and multiply by 100. A $640,000 loan on an $800,000 property is an LVR of 80%, which is the same as a 20% deposit."),
            ("What is the maximum LVR for a home loan in NZ?", "There's no single maximum. The Reserve Bank lets banks make up to 25% of their new owner-occupier lending above 80% LVR and up to 10% of new investor lending above 70% LVR. New builds and Kāinga Ora First Home Loans are exempt, and each lender sets its own upper limit."),
            ("What LVR do I need to avoid a low equity margin?", "Generally 80% or lower, which means a deposit or equity of at least 20%. Above that, most lenders add a margin to the rate or charge a fee."),
            ("Do LVR restrictions apply to new builds?", "No. Loans to buy or build a new home are exempt from the Reserve Bank's LVR restrictions, although every lender still sets its own minimum deposit."),
        ],
        "related": [
            ("../blog/what-is-lvr-nz-mortgage", "What Is LVR?", "How loan-to-value ratio affects your loan."),
            ("../blog/low-deposit-home-loan-nz", "Low Deposit Home Loans", "Buying with less than 20%."),
            ("../blog/low-equity-margin-fee-nz", "Low Equity Margin", "What it costs and how to remove it."),
            ("../calculators/borrowing-power", "Borrowing Power Calculator", "How much you may be able to borrow."),
            ("../calculators/dti-calculator", "DTI Calculator", "Check your debt against your income."),
            ("../services/first-home-buyer", "First Home Buyer Loans", "Advice on deposits, KiwiSaver and lenders."),
        ],
        "script": FMT + 'function calcLV(){var val=v("lv-val"),d=Math.min(v("lv-dep"),val),t=v("lv-type"),nb=$("lv-new").value==="1",loan=val-d,l=val>0?loan/val*100:0,gap=loan-val*t/100,r=$("lv-lvr"),s=$("lv-sub");r.textContent=val>0?l.toFixed(1)+"%":"0%";$("lv-loan").textContent=m(loan);$("lv-pct").textContent=m(d)+" ("+(val>0?(100-l).toFixed(1):"0")+"%)";if(l<=t){r.style.color="var(--finch-forest)";s.textContent="At or under the "+t+"% limit";$("lv-gap").textContent="None needed"}else if(nb){r.style.color="var(--finch-forest)";s.textContent="Above "+t+"%, but new builds are exempt from the Reserve Bank limit. The lender\'s own minimum deposit applies";$("lv-gap").textContent=m(gap)+" (not required for a new build)"}else{r.style.color="#b5462f";s.textContent="Above the "+t+"% limit, so this counts as high-LVR lending";$("lv-gap").textContent="About "+m(gap)}}calcLV();',
        "fn": "calcLV()",
    },
    {
        "slug": "interest-only-calculator",
        "crumb": "Interest-Only",
        "name": "Interest-Only Mortgage Calculator NZ",
        "title": "Interest-Only Mortgage Calculator NZ | Finch Mortgages",
        "desc": "See your interest-only repayments, what they jump to when the interest-only period ends, and the extra interest it costs over the life of a NZ home loan.",
        "app_desc": "Calculates interest-only repayments on a New Zealand home loan, the principal-and-interest repayments that follow, and the additional interest cost.",
        "h1": "Interest-Only Mortgage<br/><em style=\"font-style:italic;color:var(--finch-forest);\">Calculator NZ</em>",
        "intro": "Compare interest-only repayments with standard repayments, and see what you'd pay once the interest-only period ends and the same debt has fewer years to be repaid.",
        "widget_title": "Interest-only calculator",
        "widget_sub": "Assumes the interest rate stays the same throughout.",
        "inputs": [
            money("Loan amount", "io-loan", 600000),
            number("Interest rate", "io-rate", "5.50", "% p.a.", "0.01"),
            number("Interest-only period", "io-yrs", 5, "years"),
            number("Total loan term", "io-term", 30, "years"),
        ],
        "button": "Calculate repayments",
        "result_label": "Interest-only repayment",
        "result_id": "io-pay",
        "sub_id": "io-sub",
        "rows": [("Principal and interest from day one", "io-pi"),
                 ("Repayment after the interest-only period", "io-after"),
                 ("Extra interest over the life of the loan", "io-extra")],
        "note": "Monthly figures, rounded. The comparison holds the interest rate constant, which it won't be in practice, so use it to compare the two structures and not as a forecast. Lenders assess an interest-only application on the higher repayments that follow.",
        "side_title": "What the numbers show",
        "side": [
            ("Lower repayments now", "During the interest-only period you pay the interest and nothing off the loan, so the repayment is lower."),
            ("Higher repayments later", "When the period ends, the full balance has to be repaid over the years that are left, so repayments are higher than if you'd started on principal and interest."),
            ("More interest overall", "The balance doesn't fall during the interest-only years, so you pay interest on the full amount for longer."),
            ("The lender's test", "Lenders check that you can afford the principal-and-interest repayments over the shorter remaining term, not just the interest-only amount."),
        ],
        "cta_title": "Weighing up interest-only?",
        "cta": "Lenders differ on how long they'll allow and who qualifies. We can check which of the 23 lenders on our panel fit your plans, at no fee for residential home loans.",
        "body": f"""
<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">How interest-only home loans work in NZ</h2>
<p style="margin-bottom:2rem;">A standard repayment covers the interest and pays a little off the loan. On interest-only you pay just the interest for an agreed period, so the balance stays where it is. When the period ends, the loan switches to principal and interest over whatever term is left.</p>
<h3 {H3}>A worked example</h3>
<p style="margin-bottom:2rem;">Take $600,000 at 5.50% over 30 years. Interest-only costs about $2,750 a month, against about $3,407 on principal and interest. After five interest-only years you still owe $600,000 with 25 years left, and the repayment becomes about $3,685 a month. Over the whole term you'd pay about $44,000 more interest than on principal and interest from the start.</p>
<h3 {H3}>Who lenders approve</h3>
<ul style="margin-bottom:2rem;padding-left:1.5rem;list-style:disc;">
<li style="margin-bottom:0.5rem;"><strong>Property investors.</strong> The main users. Lenders commonly offer up to five years at a time on a rental.</li>
<li style="margin-bottom:0.5rem;"><strong>People building.</strong> Construction loans are normally interest-only until the build is finished.</li>
<li style="margin-bottom:0.5rem;"><strong>Buyers bridging between homes.</strong> For a short time, until the old house sells.</li>
<li style="margin-bottom:0.5rem;"><strong>Owner-occupiers with a reason.</strong> Parental leave or a temporary drop in income, usually for six to twelve months.</li>
</ul>
<h3 {H3}>When it helps and when it doesn't</h3>
<p style="margin-bottom:2rem;">Interest-only can suit an investor who also has a home loan. Paying interest-only on the rental frees up cash to pay down the home loan faster, and interest on a rental loan is generally deductible where interest on your own home isn't. Check the tax side with your accountant. It can also carry you through a short squeeze when there's a clear plan for what comes next.</p>
<p style="margin-bottom:2rem;">It's a poor way to afford a house you otherwise couldn't. It doesn't increase what you can borrow, because the lender tests the higher repayments that come later, and it leaves you with no extra equity if prices fall.</p>
<h3 {H3}>When the period ends</h3>
<p style="margin-bottom:0;">You can ask to extend, but the lender will reassess your income and the property as if it were a new application, and it can say no. Plan for the higher repayment before it arrives. Our guides to <a href="../blog/interest-only-home-loan-nz" {A}>interest-only home loans</a> and <a href="../blog/interest-only-ending-refinance-nz" {A}>an interest-only period ending</a> cover the options, and the <a href="../calculators/mortgage-calculator" {A}>mortgage repayment calculator</a> shows standard repayments weekly or fortnightly.</p>
""",
        "faqs": [
            ("How do I calculate interest-only mortgage repayments?", "Multiply the loan by the annual interest rate and divide by 12 for a monthly figure. On $600,000 at 5.50%, that's about $2,750 a month."),
            ("How long can a home loan be interest-only in NZ?", "It depends on the lender and the purpose. Lenders commonly offer up to five years at a time on a rental property, and usually six to twelve months for an owner-occupier with a specific reason such as parental leave."),
            ("Does interest-only let me borrow more?", "No. Lenders assess whether you could afford principal-and-interest repayments over the term left after the interest-only period, which makes the test harder, not easier."),
            ("What happens when the interest-only period ends?", "The loan switches to principal and interest over the remaining term, so repayments rise. You can apply to extend, but the lender reassesses your position and doesn't have to agree."),
        ],
        "related": [
            ("../blog/interest-only-home-loan-nz", "Interest-Only Home Loans", "How they work and who they suit."),
            ("../blog/interest-only-ending-refinance-nz", "Interest-Only Period Ending", "Your options before repayments jump."),
            ("../calculators/mortgage-calculator", "Mortgage Repayment Calculator", "Standard repayments at any rate and term."),
            ("../calculators/rental-yield-calculator", "Rental Yield Calculator", "Gross and net yield on a rental."),
            ("../blog/mortgage-interest-tax-deductible-nz", "Interest Deductibility", "When mortgage interest can be claimed."),
            ("../services/investment-property", "Investment Property Loans", "Structuring lending on a rental."),
        ],
        "script": FMT + 'function pmt(p,r,n){return r>0?p*r/(1-Math.pow(1+r,-n)):p/n}function calcIO(){var p=v("io-loan"),r=v("io-rate")/1200,y=v("io-yrs"),t=v("io-term");if(t<=y||t<=0){$("io-pay").textContent=m(p*r);$("io-sub").textContent="The loan term has to be longer than the interest-only period";$("io-pi").textContent=$("io-after").textContent=$("io-extra").textContent="";return}var io=p*r,n2=(t-y)*12,af=pmt(p,r,n2),pi=pmt(p,r,t*12),ex=io*y*12+af*n2-pi*t*12;$("io-pay").textContent=m(io)+" / month";$("io-sub").textContent="For the first "+y+" year"+(y===1?"":"s")+", about "+m(pi-io)+" a month less than principal and interest";$("io-pi").textContent=m(pi)+" / month";$("io-after").textContent=m(af)+" / month";$("io-extra").textContent="About "+m(ex)}calcIO();',
        "fn": "calcIO()",
    },
    {
        "slug": "cashback-clawback-calculator",
        "crumb": "Cashback Clawback",
        "name": "Mortgage Cashback Clawback Calculator NZ",
        "title": "Mortgage Cashback Clawback Calculator NZ | Finch",
        "desc": "Took a cashback with your NZ home loan? Estimate how much you'd repay if you refinanced or sold today, and when your clawback period ends.",
        "app_desc": "Estimates the cash contribution a New Zealand borrower would repay to their lender on refinancing or repaying inside the clawback period.",
        "h1": "Cashback Clawback<br/><em style=\"font-style:italic;color:var(--finch-forest);\">Calculator NZ</em>",
        "intro": "If your bank paid you a cash contribution, leaving early usually means paying some or all of it back. Estimate what you'd owe today and whether a new lender's offer covers it.",
        "widget_title": "Clawback estimator",
        "widget_sub": "Check your loan agreement for your actual terms.",
        "inputs": [
            money("Cashback you received", "cb-amt", 5000),
            number("Months since the loan was drawn down", "cb-mo", 20, "months"),
            select("Clawback period", "cb-per", [("36", "3 years"), ("48", "4 years"), ("24", "2 years"), ("60", "5 years")]),
            select("How the clawback works", "cb-type", [("p", "Pro-rata (reduces over time)"), ("f", "Full amount until the period ends")]),
            money("Cashback offered by a new lender", "cb-new", 0),
            money("Legal fees to switch", "cb-legal", 1500),
        ],
        "button": "Estimate my clawback",
        "result_label": "Estimated amount to repay today",
        "result_id": "cb-owe",
        "sub_id": "cb-sub",
        "rows": [("Clawback period ends in", "cb-left"), ("New cashback less clawback and legal fees", "cb-net")],
        "note": "An estimate based on the terms you enter. Lenders write clawback clauses differently, and some also claw back contributions to legal fees. Your loan agreement or letter of offer sets the real figure, and your lender can confirm it in writing. A break fee on a fixed rate is separate and isn't included here.",
        "side_title": "How clawback works",
        "side": [
            ("A condition of the cash", "When a lender pays a cash contribution, the loan agreement says how long you need to stay. Leave sooner and you repay some or all of it."),
            ("Pro-rata or in full", "Some agreements reduce the amount as time passes. Others ask for the whole amount back until the last day of the period."),
            ("What triggers it", "Refinancing to another lender, and often selling and repaying the loan without taking a new loan with the same lender."),
            ("Separate from a break fee", "A break fee is about leaving a fixed rate early. Clawback is about leaving the lender. You can owe one, both or neither."),
        ],
        "cta_title": "Not sure if you can switch yet?",
        "cta": "Send us your loan agreement and we'll work out the clawback, any break fee and whether a move stacks up. There's no fee for residential home loans.",
        "body": f"""
<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Cashback clawback on NZ home loans</h2>
<p style="margin-bottom:2rem;">Lenders often pay a cash contribution to win a home loan. The money comes with a condition: stay for a minimum period or pay it back. That condition is the clawback, and the Banking Ombudsman's guidance is that a lender's right to it has to be set out in your loan agreement or a separate contract.</p>
<h3 {H3}>How much, and for how long</h3>
<p style="margin-bottom:2rem;">Both depend on your agreement. The terms we see most often are a clawback period of three or four years from the date the loan was drawn, with either the full amount repayable throughout or a pro-rata amount that falls as time passes. As an illustration, a $5,000 contribution on a three-year pro-rata clause would cost about $1,667 to leave after two years. On a full-repayment clause it would cost all $5,000 until the day the period ends.</p>
<h3 {H3}>Where to find your terms</h3>
<p style="margin-bottom:2rem;">Look in the loan agreement or letter of offer from when the cash was paid, under a heading such as cash contribution, incentive or special conditions. If you can't find it, ask your lender in writing for the amount repayable on a given date.</p>
<h3 {H3}>Does a new cashback cancel it out?</h3>
<p style="margin-bottom:2rem;">Sometimes. If a new lender pays $6,000 and you repay $2,000 to the old one, you're $4,000 ahead before legal fees. A new clawback period then starts with the new lender. The interest rate matters more than the cash over any reasonable period, so compare the rates as well.</p>
<h3 {H3}>Selling and buying again</h3>
<p style="margin-bottom:2rem;">If you're selling and buying another home, ask your lender about keeping the lending with them for the next purchase. Most will carry the arrangement over, which avoids the clawback.</p>
<h3 {H3}>Clawback and break fees together</h3>
<p style="margin-bottom:0;">Refinancing on the day a fixed term ends avoids a break fee, but not a clawback if you're still inside the period. Count both before you move. The <a href="../calculators/break-fee-calculator" {A}>break fee calculator</a> estimates the first, and our guides to <a href="../blog/mortgage-cashback-clawback-nz" {A}>cashback clawback</a> and <a href="../blog/mortgage-cashback-offers-nz" {A}>mortgage cashback offers</a> explain the detail.</p>
""",
        "faqs": [
            ("What is a cashback clawback?", "It's the condition attached to a cash contribution from a home loan lender. If you refinance elsewhere or repay the loan within the clawback period, you repay some or all of the cash."),
            ("How long is the clawback period on a NZ mortgage?", "It depends on your loan agreement. Three or four years from the date the loan was drawn is common."),
            ("Do I have to repay cashback if I sell my house?", "Often yes, if you repay the loan inside the clawback period without taking a new loan with the same lender. If you're buying again, most lenders will carry the arrangement over to the new loan."),
            ("Will a new bank cover my clawback?", "A new lender's cash contribution can offset what you repay to the old one, but it isn't guaranteed, and a new clawback period starts with the new lender."),
        ],
        "related": [
            ("../blog/mortgage-cashback-clawback-nz", "Cashback Clawback Explained", "How to read your clawback clause."),
            ("../blog/mortgage-cashback-offers-nz", "Mortgage Cashback Offers", "How cash contributions work."),
            ("../calculators/break-fee-calculator", "Break Fee Calculator", "Estimate the cost of leaving a fixed rate."),
            ("../calculators/refinance-savings", "Refinance Savings Calculator", "Compare your loan with a new one."),
            ("../blog/is-it-worth-refinancing-mortgage-nz", "Is Refinancing Worth It?", "Weighing the savings against the costs."),
            ("../services/refinance", "Refinance With Finch", "We compare 23 lenders and handle the switch."),
        ],
        "script": FMT + 'function calcCB(){var a=v("cb-amt"),mo=v("cb-mo"),p=v("cb-per"),full=$("cb-type").value==="f",n=v("cb-new"),l=v("cb-legal"),left=Math.max(0,p-mo),owe=left<=0?0:full?a:a*left/p,net=n-owe-l;$("cb-owe").textContent="~"+m(owe);$("cb-sub").textContent=left<=0?"Your clawback period has ended on these terms":full?"The full amount is repayable until the period ends":"About "+Math.round(left/p*100)+"% of the cashback, falling each month";$("cb-left").textContent=left<=0?"Already ended":left+" month"+(left===1?"":"s");$("cb-net").textContent=net>=0?"About "+m(net)+" ahead":"About "+m(net)+" behind";$("cb-net").style.color=net>=0?"var(--finch-forest)":"#b5462f"}calcCB();',
        "fn": "calcCB()",
    },
]


def schema(p):
    url = f"{BASE}/calculators/{p['slug']}"
    graph = [
        {"@type": "FinancialService", "@id": f"{BASE}/#organization", "name": "Finch Mortgages", "url": f"{BASE}/",
         "logo": {"@type": "ImageObject", "url": f"{BASE}/images/finch-logo.png"}},
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Calculators", "item": f"{BASE}/calculators"},
            {"@type": "ListItem", "position": 3, "name": p["name"], "item": url}]},
        {"@type": "WebApplication", "@id": f"{url}#webapp", "url": url, "name": p["name"], "operatingSystem": "All",
         "applicationCategory": "FinanceApplication", "browserRequirements": "Requires JavaScript. Requires HTML5.",
         "description": p["app_desc"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NZD"},
         "publisher": {"@id": f"{BASE}/#organization"}, "datePublished": TODAY, "dateModified": TODAY,
         "author": {"@type": "Person", "@id": f"{BASE}/#mukhtar-kiyani", "name": "Mukhtar Kiyani",
                    "jobTitle": "Founder & Mortgage Adviser", "url": f"{BASE}/about"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def main_html(p):
    side = "".join(
        f'<div class="process-step" style="padding:1rem 0;{"border:none;" if i == len(p["side"]) else ""}"><div class="step-number" style="width:36px;height:36px;font-size:0.75rem;">{i}</div><div class="step-content"><h3>{h}</h3><p>{t}</p></div></div>\n'
        for i, (h, t) in enumerate(p["side"], 1))
    rows = "".join(f'<div class="calc-row"><span>{label}</span><span id="{id_}"></span></div>\n' for label, id_ in p["rows"])
    faqs = "".join(f'<h3 {H3}>{q}</h3>\n<p style="margin-bottom:1rem;">{a}</p>\n' for q, a in p["faqs"])
    related = "".join(
        f'<a href="{href}" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">{t}</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">{d}</span></a>\n'
        for href, t, d in p["related"])
    return f"""<main style="padding-top:80px;">
<section class="container" style="padding-top:5rem; padding-bottom:3rem;">
<nav class="breadcrumb"><a href="../">Home</a><span class="breadcrumb-sep">/</span><a href="../calculators">Calculators</a><span class="breadcrumb-sep">/</span><span>{p['crumb']}</span></nav>
<div class="page-hero-tag">{p['name']}</div>
<p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: {UPDATED}</p>
<h1 style="font-family:var(--font-display);font-size:clamp(2rem,4vw,3rem);margin-bottom:0.75rem;">{p['h1']}</h1>
<p style="color:var(--neutral-medGray);max-width:600px;">{p['intro']}</p>
</section>
<section class="container" style="padding-bottom:5rem;">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:3rem;align-items:start;">
<div class="calc-widget">
<h2>{p['widget_title']}</h2>
<p>{p['widget_sub']}</p>
{chr(10).join(p['inputs'])}
<button class="btn-primary" onclick="{p['fn']}" style="width:100%;justify-content:center;margin-bottom:1.25rem;">{p['button']}</button>
<div class="calc-result" aria-live="polite">
<div class="calc-result-label">{p['result_label']}</div>
<div class="calc-result-amount" id="{p['result_id']}"></div>
<div class="calc-result-sub" id="{p['sub_id']}"></div>
</div>
<div class="calc-breakdown" style="margin-top:1rem;">
{rows}</div>
<p style="font-size:0.75rem;color:var(--neutral-warmGray);margin-top:1rem;line-height:1.5;">{p['note']}</p>
</div>
<div>
<div style="background:white;border:1px solid rgba(98,162,154,0.25);border-radius:1.25rem;padding:2rem;margin-bottom:1.5rem;">
<h2 style="font-size:1.125rem;font-weight:700;color:var(--neutral-black);margin-bottom:1rem;">{p['side_title']}</h2>
{side}</div>
<div style="background:var(--finch-forest);border-radius:1.25rem;padding:2rem;color:white;">
<h2 style="color:white;font-size:1.125rem;font-weight:700;margin-bottom:0.75rem;">{p['cta_title']}</h2>
<p style="color:rgba(255,255,255,0.75);font-size:0.875rem;line-height:1.7;margin-bottom:1.25rem;">{p['cta']}</p>
<a class="btn-cta-white" href="../contact" style="font-size:0.875rem;padding:0.875rem 1.75rem;">Talk to an adviser →</a>
</div>
</div>
</div>
</section>
<section style="padding:5rem 0;background:var(--finch-mist);">
<div class="container" style="max-width:800px;">
<div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
{p['body'].strip()}
</div>
</div>
</section>
<section style="padding:5rem 0;background:white;">
<div class="container" style="max-width:800px;">
<div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:0.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Common questions</h2>
{faqs}<p style="margin-top:2rem;font-size:0.9rem;">By <a href="../about" {A}>Mukhtar Kiyani</a>, mortgage adviser at Finch Mortgages. General information only, not personalised financial advice.</p>
</div>
</div>
</section>
<section style="padding:4rem 0;background:var(--finch-mist);">
<div class="container" style="max-width:1000px;">
<div class="section-label"><span>Keep Reading</span></div>
<h2 class="section-heading" style="margin-bottom:2.5rem;">Related guides and calculators</h2>
<div class="cols-3" style="gap:1.5rem;">
{related}</div>
</div>
</section>
</main>"""


def build(p, shell):
    top, rest = shell.split('<main', 1)
    head, nav = top.split('</head>', 1)
    _, tail = rest.split('</main>', 1)
    old_title = re.search(r"<title>(.*?)</title>", head).group(1)
    old_desc = re.search(r'<meta content="([^"]*)" name="description"/>', head).group(1)
    head = head.replace(old_title, p["title"])
    head = head.replace(old_desc, p["desc"])
    head = head.replace("calculators/dti-calculator", f"calculators/{p['slug']}")
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda _: f'<script type="application/ld+json">{schema(p)}</script>', head, count=1, flags=re.S)
    tail = re.sub(r"<script>function calcDTI\(\).*?</script>", lambda _: f"<script>{p['script']}</script>", tail, count=1, flags=re.S)
    assert "calcDTI" not in tail and "DTI" not in head, p["slug"]
    head += '</head>' + nav
    return head + main_html(p) + tail


def main():
    shell = SHELL.read_text(encoding="utf-8")
    for p in PAGES:
        assert len(p["title"]) <= 62, (p["slug"], len(p["title"]))
        assert 110 <= len(p["desc"]) <= 160, (p["slug"], len(p["desc"]))
        out = ROOT / "calculators" / f"{p['slug']}.html"
        out.write_text(build(p, shell), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
