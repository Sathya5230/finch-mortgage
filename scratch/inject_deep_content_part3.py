import os

content_data = {
    "investment-property.html": {
        "title": "Strategic Property Investment Lending in New Zealand",
        "p1": "Building a robust residential property portfolio in New Zealand requires a highly strategic approach to leverage, tax structuring, and cash flow management. The regulatory environment surrounding property investment has evolved significantly, with changes to interest deductibility rules, bright-line tests, and stringent Loan-to-Value Ratio (LVR) restrictions designed to cool speculative buying. For investors in 2026, securing the right mortgage is not just about the lowest interest rate; it is about establishing a sustainable credit architecture that allows for future scalability and risk mitigation.",
        "h2": "Leveraging Usable Equity and Navigating LVRs",
        "p2": "Under current RBNZ guidelines, most investors require a 30% to 35% deposit for existing residential investment properties. However, astute investors rarely use cash for this deposit. Instead, they leverage the 'usable equity' accumulated in their primary residence or existing portfolio. This involves restructuring current mortgages to release capital without needing to sell the underlying asset. Crucially, exemptions to high LVR restrictions still exist for 'new build' investments, which often only require a 20% deposit and enjoy preferential tax treatment regarding interest deductibility. We guide investors through these nuances, identifying which asset classes align best with their capital position.",
        "h3": "Yield vs. Capital Growth and Debt Structuring",
        "p3": "Every investment property serves a specific purpose—whether it is generating high rental yield to support holding costs, or prioritizing long-term capital growth in blue-chip suburbs. Consequently, the loan structure must match the asset's purpose. We provide expert advice on the implementation of interest-only loan terms versus principal and interest repayments, helping you optimize your cash flow and tax position. By segregating your owner-occupied debt from your deductible investment debt, we ensure you remain compliant while maximizing your financial efficiency."
    },
    "self-employed.html": {
        "title": "Comprehensive Mortgage Solutions for the Self-Employed",
        "p1": "Securing a mortgage as a self-employed individual, freelancer, or small business owner in New Zealand presents unique challenges. Traditional banking algorithms are designed for PAYE employees with predictable, linear income streams. Consequently, self-employed applicants often face intense scrutiny, higher administrative burdens, and frustrating rejections from mainstream banks, even when their businesses are highly profitable. Navigating this landscape requires a broker who understands commercial financials and can accurately translate business success into borrowing power.",
        "h2": "Translating Financial Statements into Borrowing Capacity",
        "p2": "When assessing self-employed income, lenders do not simply look at your top-line revenue; they meticulously analyze your net profit before tax, add back certain non-cash deductions (like depreciation), and scrutinize your balance sheet for underlying stability. Typically, banks require two years of finalized financial statements prepared by a chartered accountant. We work collaboratively with your accountant to present your financials in the most favorable light. If your business has experienced rapid recent growth that is not fully reflected in historical averages, we advocate on your behalf, utilizing projected cash flows and interim management accounts to justify a higher borrowing limit.",
        "h3": "Alternative Lending and Low-Doc Options",
        "p3": "For business owners who do not possess two years of standardized financials—perhaps due to recent establishment or complex trust structures—traditional bank lending may prove inaccessible. Fortunately, the New Zealand market features robust tier-two and non-bank lenders that specialize in self-employed mortgages. These institutions offer 'low-doc' or alternative income verification loans, assessing serviceability based on GST returns, business bank statements, or accountant declarations rather than historical tax returns. We possess deep relationships with these specialized lenders, ensuring your entrepreneurial spirit is not a barrier to homeownership."
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

"""

def main():
    repo_dir = "/Users/sathyamoorthy/Desktop/finch mortgage/services"
    
    for filename, content in content_data.items():
        filepath = os.path.join(repo_dir, filename)
            
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        if "Comprehensive Overview" in html:
            continue
            
        injected_html = html_template.format(**content)
        
        target_tag = '<section style="padding:4rem 0;">'
        if target_tag in html:
            new_html = html.replace(target_tag, injected_html + target_tag)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Successfully updated {filename}")
        else:
            print(f"Could not find target tag in {filename}")

if __name__ == "__main__":
    main()
