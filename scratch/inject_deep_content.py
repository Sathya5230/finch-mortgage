import os
import re

content_data = {
    "home-loan.html": {
        "title": "Comprehensive Guide to New Zealand Home Loans in 2026",
        "p1": "Navigating the New Zealand property market requires more than just finding a house you love; it demands a strategic approach to financing. As of 2026, the lending landscape dictated by the Reserve Bank of New Zealand (RBNZ) and major registered banks like ANZ, ASB, BNZ, and Westpac remains dynamic. Whether you are eyeing a suburban family home in Auckland, a lifestyle block in Canterbury, or a townhouse in Wellington, understanding the nuances of home loan structures—such as the balance between fixed and floating interest rates—is paramount to long-term financial stability.",
        "h2": "Understanding Debt-to-Income (DTI) and LVR Restrictions",
        "p2": "Recent regulatory shifts have heavily emphasized Debt-to-Income (DTI) ratios and Loan-to-Value Ratio (LVR) speed limits. Generally, owner-occupiers are expected to provide a 20% deposit, though exemptions exist for new builds and specific government-backed schemes. Lenders now rigorously stress-test applications, typically applying test rates several percentage points above the advertised market rates. This means your borrowing capacity is calculated not on what you pay today, but whether you could comfortably manage repayments if rates were to significantly rise. Our role at Finch Mortgages is to pre-calculate these metrics, ensuring your application is positioned perfectly before it ever reaches a bank assessor's desk.",
        "h3": "The Importance of Independent Mortgage Advice",
        "p3": "Walking directly into your everyday bank limits your options exclusively to their product suite. An independent mortgage broker acts as a vital intermediary, granting you access to wholesale rates and bespoke lending policies across over 20 New Zealand institutions, including tier-two lenders and credit unions. This wide-net approach often results in substantially lower interest rates, better cashback offers, and more flexible loan terms, ultimately saving you thousands of dollars over the lifetime of your mortgage."
    },
    "first-home-buyer.html": {
        "title": "A Complete Overview of the NZ First Home Buyer Landscape",
        "p1": "Stepping onto the New Zealand property ladder is a major milestone, but the path is often paved with complex financial jargon and rigorous lending criteria. For first home buyers in 2026, understanding how to leverage available resources—such as KiwiSaver and government grants—is critical. With median house prices demanding substantial deposits, navigating the difference between a standard 20% deposit requirement and the specialist low-deposit pathways (such as 5% or 10% options) can mean the difference between buying now or waiting another five years.",
        "h2": "Maximizing Your KiwiSaver and First Home Grants",
        "p2": "If you have been contributing to KiwiSaver for a minimum of three years, you are generally eligible to withdraw the majority of your balance (leaving a mandatory $1,000) to use toward your deposit. Furthermore, the Kāinga Ora First Home Grant offers up to $5,000 for purchasing an existing property, or up to $10,000 for a new build, provided you meet specific income and regional house price caps. Combining these funds with your personal savings forms the foundation of your deposit. Our brokers specialize in harmonizing these different capital streams, ensuring compliance with strict withdrawal timelines and solicitor requirements so your settlement day proceeds without a hitch.",
        "h3": "Low Deposit Lending and Welcome Home Loans",
        "p3": "Not having a 20% deposit does not lock you out of the market. The First Home Loan scheme, underwritten by Kāinga Ora, allows eligible buyers to purchase with just a 5% deposit. Additionally, some mainstream banks offer limited allocations for lending at 10% deposits, often applying a Low Equity Premium (LEP) or margin. We evaluate your financial profile to determine which of these low-deposit avenues offers the lowest overall cost, factoring in interest rate premiums and the potential for leveraging family guarantees to avoid low-equity fees entirely."
    },
    "investment-property.html": {
        "title": "Strategic Property Investment Lending in New Zealand",
        "p1": "Building a robust residential property portfolio in New Zealand requires a highly strategic approach to leverage, tax structuring, and cash flow management. The regulatory environment surrounding property investment has evolved significantly, with changes to interest deductibility rules, bright-line tests, and stringent Loan-to-Value Ratio (LVR) restrictions designed to cool speculative buying. For investors in 2026, securing the right mortgage is not just about the lowest interest rate; it is about establishing a sustainable credit architecture that allows for future scalability and risk mitigation.",
        "h2": "Leveraging Usable Equity and Navigating LVRs",
        "p2": "Under current RBNZ guidelines, most investors require a 30% to 35% deposit for existing residential investment properties. However, astute investors rarely use cash for this deposit. Instead, they leverage the 'usable equity' accumulated in their primary residence or existing portfolio. This involves restructuring current mortgages to release capital without needing to sell the underlying asset. Crucially, exemptions to high LVR restrictions still exist for 'new build' investments, which often only require a 20% deposit and enjoy preferential tax treatment regarding interest deductibility. We guide investors through these nuances, identifying which asset classes align best with their capital position.",
        "h3": "Yield vs. Capital Growth and Debt Structuring",
        "p3": "Every investment property serves a specific purpose—whether it is generating high rental yield to support holding costs, or prioritizing long-term capital growth in blue-chip suburbs. Consequently, the loan structure must match the asset's purpose. We provide expert advice on the implementation of interest-only loan terms versus principal and interest repayments, helping you optimize your cash flow and tax position. By segregating your owner-occupied debt from your deductible investment debt, we ensure you remain compliant while maximizing your financial efficiency."
    },
    "refinance.html": {
        "title": "The Strategic Guide to Refinancing Your Mortgage",
        "p1": "Refinancing your home loan is one of the most powerful financial levers available to New Zealand homeowners. It is not merely a defensive strategy to secure a lower interest rate when fixed terms expire; it is an offensive maneuver to restructure debt, release trapped equity, and aggressively reduce the total lifespan of your mortgage. In a fluctuating economic climate, complacency costs money. Failing to review your mortgage every two to three years often results in paying a 'loyalty tax' to your current bank, missing out on competitive market offers and substantial cashback incentives.",
        "h2": "Debt Consolidation and Cash Flow Optimization",
        "p2": "Beyond chasing lower interest rates, refinancing provides a strategic opportunity to consolidate high-interest short-term debt—such as credit cards, personal loans, or vehicle finance—into your primary mortgage. Because home loan rates are significantly lower than unsecured lending rates, this consolidation can instantly improve household cash flow by hundreds of dollars per month. However, it is vital to structurally separate this consolidated debt on a shorter amortization schedule so you do not end up paying for a car over 30 years. Our advisers expertly construct these split-loan facilities to balance immediate cash flow relief with long-term interest minimization.",
        "h3": "Breaking Fixed Rates and Cashback Clauses",
        "p3": "A common barrier to refinancing is the fear of early repayment adjustments (break fees) if you exit a fixed-term contract prematurely. We conduct comprehensive break-fee analyses to determine if the long-term interest savings outweigh the immediate penalty costs. Furthermore, we negotiate aggressively to secure cash contributions (cashbacks) from your new lender. These cashbacks, typically calculated as a percentage of your total loan amount, can be used to absorb any legal fees or break costs associated with the transition, ensuring that the decision to refinance is immediately financially positive."
    },
    "pre-approval.html": {
        "title": "Securing Mortgage Pre-Approval: Your Buyer's Passport",
        "p1": "In the highly competitive New Zealand property market, attempting to purchase a home without a formal mortgage pre-approval is a significant disadvantage. A pre-approval acts as a financial passport; it is a conditional commitment from a lender stating exactly how much they are willing to lend you based on a preliminary assessment of your income, expenses, and credit history. Whether you are bidding at an auction or negotiating a private treaty, holding a pre-approval demonstrates to vendors and real estate agents that you are a serious, qualified buyer capable of executing the transaction.",
        "h2": "The Anatomy of a Robust Pre-Approval Application",
        "p2": "Securing a reliable pre-approval requires more than a quick online calculator check. Banks utilize rigorous stress-testing methodologies, applying test interest rates that are significantly higher than the advertised rates to ensure you can absorb future economic shocks. Furthermore, the advent of the Credit Contracts and Consumer Finance Act (CCCFA) means lenders scrutinize discretionary spending and living expenses with unprecedented granularity. We preemptively audit your financial profile, identifying and mitigating any potential red flags—such as irregular income patterns or unmanaged short-term debt—before the application is submitted to a credit assessor.",
        "h3": "Auction Readiness and Unconditional Offers",
        "p3": "Many desirable properties in New Zealand are sold via auction, a process that requires buyers to bid on an unconditional basis. This means you cannot attach finance conditions to your offer; if the hammer falls, you are legally bound to purchase the property. Consequently, your pre-approval must be rock-solid. We work diligently to clear as many lender conditions as possible upfront, ensuring your finance is practically guaranteed subject only to the lender's valuation of the specific property you intend to buy. This meticulous preparation provides the confidence necessary to bid aggressively and secure your desired home."
    },
    "next-home-buyer.html": {
        "title": "Navigating the complexities of Upgrading Your Home",
        "p1": "Transitioning from your first home to your next property introduces a new layer of logistical and financial complexity. Unlike first home buyers, 'next home' buyers must navigate the intricate timing of selling an existing asset while simultaneously purchasing a new one. This process requires a sophisticated understanding of usable equity, bridging finance, and the sequential alignment of settlement dates to avoid costly delays or the stressful scenario of being temporarily without a home.",
        "h2": "Bridging Finance and Concurrent Settlements",
        "p2": "The ideal scenario involves a concurrent settlement, where the sale of your current home and the purchase of your new property occur on the exact same day. However, market realities often necessitate buying before you sell, or vice versa. In situations where you find your dream home before selling your current one, bridging finance becomes a vital tool. Bridging loans are short-term funding solutions that cover the financial gap between the two transactions. We specialize in negotiating these complex facilities, ensuring you have the capital necessary to secure your next property without being forced into a fire-sale of your existing home.",
        "h3": "Retaining Your First Home as an Investment",
        "p3": "A strategic option for many next home buyers is to retain their current residence and convert it into a rental investment, rather than selling it. This approach allows you to build a property portfolio and benefit from long-term capital growth across multiple assets. We evaluate your financial capacity to support two mortgages, advising on the necessary restructuring of debt to optimize tax deductibility and cash flow. By leveraging the equity in your first home, we can often facilitate the purchase of your next home while transforming your initial property into a lucrative wealth-building vehicle."
    },
    "self-employed.html": {
        "title": "Comprehensive Mortgage Solutions for the Self-Employed",
        "p1": "Securing a mortgage as a self-employed individual, freelancer, or small business owner in New Zealand presents unique challenges. Traditional banking algorithms are designed for PAYE employees with predictable, linear income streams. Consequently, self-employed applicants often face intense scrutiny, higher administrative burdens, and frustrating rejections from mainstream banks, even when their businesses are highly profitable. Navigating this landscape requires a broker who understands commercial financials and can accurately translate business success into borrowing power.",
        "h2": "Translating Financial Statements into Borrowing Capacity",
        "p2": "When assessing self-employed income, lenders do not simply look at your top-line revenue; they meticulously analyze your net profit before tax, add back certain non-cash deductions (like depreciation), and scrutinize your balance sheet for underlying stability. Typically, banks require two years of finalized financial statements prepared by a chartered accountant. We work collaboratively with your accountant to present your financials in the most favorable light. If your business has experienced rapid recent growth that is not fully reflected in historical averages, we advocate on your behalf, utilizing projected cash flows and interim management accounts to justify a higher borrowing limit.",
        "h3": "Alternative Lending and Low-Doc Options",
        "p3": "For business owners who do not possess two years of standardized financials—perhaps due to recent establishment or complex trust structures—traditional bank lending may prove inaccessible. Fortunately, the New Zealand market features robust tier-two and non-bank lenders that specialize in self-employed mortgages. These institutions offer 'low-doc' or alternative income verification loans, assessing serviceability based on GST returns, business bank statements, or accountant declarations rather than historical tax returns. We possess deep relationships with these specialized lenders, ensuring your entrepreneurial spirit is not a barrier to homeownership."
    },
    "asset-finance.html": {
        "title": "Strategic Asset and Equipment Finance in New Zealand",
        "p1": "For businesses operating in construction, transport, agriculture, or manufacturing, maintaining a modern and efficient fleet of vehicles and heavy machinery is critical to operational success. However, acquiring capital-intensive equipment out of pocket can severely deplete a company's cash reserves, stifling growth and limiting operational agility. Asset finance provides a strategic solution, allowing businesses to acquire the necessary tools immediately while amortizing the cost over the useful life of the asset, thereby preserving working capital for core business activities.",
        "h2": "Understanding Chattel Mortgages, Leases, and Hire Purchases",
        "p2": "The realm of asset finance encompasses a variety of structuring options, each with distinct tax, accounting, and cash flow implications. A Chattel Mortgage (or Specific Security Agreement) involves the business owning the asset from day one, with the lender taking a security interest over it. This allows the business to claim depreciation and interest deductions. Conversely, an Operating Lease is akin to renting; the financier retains ownership, and the business claims the lease payments as a fully deductible operational expense. We analyze your company's balance sheet and tax position to recommend the most efficient financing structure, ensuring your debt strategy aligns with your overarching financial objectives.",
        "h3": "Financing Heavy Machinery and Specialized Equipment",
        "p3": "Securing finance for specialized, 'yellow goods' (like excavators or cranes) or bespoke manufacturing equipment requires financiers who understand the inherent residual value and operational lifespan of these assets. Mainstream banks often struggle to accurately assess the collateral value of highly specialized machinery, leading to conservative lending limits or outright declines. We leverage our network of specialist commercial asset financiers who possess deep industry expertise. This ensures we can secure competitive interest rates, favorable balloon payment structures, and flexible seasonal repayment schedules tailored to the cash flow cycles of your specific industry."
    },
    "commercial-property.html": {
        "title": "Navigating Commercial Property Lending and Investment",
        "p1": "The commercial property market in New Zealand—encompassing retail, industrial, office, and specialized spaces—operates under fundamentally different financial principles than residential real estate. Commercial lending is inherently more complex, characterized by lower Loan-to-Value Ratios (LVRs), shorter loan terms, and a rigorous focus on the asset's income-generating potential (the 'yield') rather than purely the borrower's personal income. Whether you are an investor seeking a high-yielding warehouse or a business owner looking to purchase your own premises, securing optimal commercial finance requires sophisticated structuring.",
        "h2": "Owner-Occupier vs. Investment Commercial Mortgages",
        "p2": "Commercial lenders differentiate strongly between owner-occupied properties and pure investments. If your business intends to occupy the premises, lenders often view the transaction favorably, allowing for higher LVRs (sometimes up to 65% or 70%) because the business's operational cash flow directly services the debt. Conversely, investment properties rely on the strength of the lease agreement and the quality of the tenant. Lenders will heavily scrutinize the Weighted Average Lease Expiry (WALE), the tenant's corporate covenant, and the property's alternative use value. We specialize in building comprehensive credit submissions that highlight the strength of your tenancy schedule and mitigate perceived risks.",
        "h3": "Interest Cover Ratios and Capitalization Rates",
        "p3": "When evaluating a commercial loan application, assessors rely heavily on the Interest Cover Ratio (ICR)—a metric that ensures the property's net rental income comfortably exceeds the proposed interest expenses. Additionally, the property's value is often determined by the Capitalization Rate (Cap Rate) applied to its income stream, rather than direct market comparisons. Understanding these commercial valuation metrics is crucial for negotiating favorable loan terms. We act as your financial advocate, engaging with specialized commercial banking managers to secure extended interest-only periods, competitive margins, and flexible covenant structures that support your long-term commercial objectives."
    },
    "construction-loan.html": {
        "title": "A Complete Guide to Construction Finance in New Zealand",
        "p1": "Building a custom home or undertaking a major residential development in New Zealand is a complex endeavor that requires specialized financial architecture. Unlike purchasing an existing property where the funds are transferred in a single transaction upon settlement, construction finance involves releasing funds in sequential stages as the build progresses. This methodology mitigates risk for the lender but requires the borrower to navigate a labyrinth of fixed-price contracts, council consents, and progress valuations. Securing a construction loan demands a broker with deep expertise in development finance.",
        "h2": "Turnkey vs. Build-Only and Progress Payments",
        "p2": "It is essential to distinguish between a 'Turnkey' contract and a standard 'Build-Only' or progress payment contract. A turnkey property involves paying a small deposit upfront, with the remaining balance due only upon the home's completion and the issuance of a Code Compliance Certificate (CCC). This is relatively straightforward to finance. However, custom builds usually rely on progress payments. The lender will establish a drawdown schedule—typically comprising 5 to 6 stages (e.g., slab down, framing, roof on, lock-up, and practical completion). At each stage, the builder issues an invoice, and the lender may require a valuer's report before releasing funds. We manage this intricate drawdown process on your behalf, ensuring your builders are paid promptly and construction momentum is maintained.",
        "h3": "Managing Cost Overruns and Contingency Funds",
        "p3": "One of the most significant risks in construction lending is the potential for cost overruns due to material price escalations, variations in scope, or unforeseen site issues. Banks are acutely aware of this risk and will rigidly scrutinize your Registered Master Builder or Certified Builder contract. They typically require a fixed-price contract and will often mandate a 10% to 15% contingency fund to be held in reserve. We help you structure your application to account for these stringent requirements, ensuring you have sufficient capital buffers approved upfront so that unexpected expenses do not halt your project mid-build."
    }
}

html_template = """
<!-- Comprehensive Overview -->
<section style="padding:5rem 0;background:var(--finch-mist);">
<div class="container" style="max-width:800px;">
<div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
<h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">{title}</h2>
<p style="margin-bottom:2rem;">{p1}</p>

<h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{h2}</h3>
<p style="margin-bottom:2rem;">{p2}</p>

<h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{h3}</h3>
<p style="margin-bottom:1rem;">{p3}</p>
</div>
</div>
</section>

<!-- FAQ -->
"""

def main():
    repo_dir = "/Users/sathyamoorthy/Desktop/finch mortgage/services"
    
    for filename, content in content_data.items():
        filepath = os.path.join(repo_dir, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename}, not found.")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Check if already injected
        if "Comprehensive Overview" in html:
            print(f"Already injected in {filename}")
            continue
            
        # Format the block
        injected_html = html_template.format(
            title=content["title"],
            p1=content["p1"],
            h2=content["h2"],
            p2=content["p2"],
            h3=content["h3"],
            p3=content["p3"]
        )
        
        # Replace the exact FAQ comment
        if "<!-- FAQ -->" in html:
            new_html = html.replace("<!-- FAQ -->", injected_html)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Successfully updated {filename}")
        else:
            print(f"Could not find <!-- FAQ --> marker in {filename}")

if __name__ == "__main__":
    main()
