#!/usr/bin/env python3
"""Generates the 4 detailed lender category pages under lenders/"""
import os, textwrap

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"
OUT  = os.path.join(ROOT, "lenders")
os.makedirs(OUT, exist_ok=True)

NAV = """<header id="main-header">
  <div class="container" style="display:flex;align-items:center;justify-content:space-between;height:80px;">
    <a href="../index.html" class="nav-logo">Finch<span class="nav-logo-dot">.</span></a>
    <nav class="hidden md-flex items-center gap-6">
      <a href="../index.html" class="nav-link">Home</a>
      <div class="nav-item"><div class="dropdown-trigger nav-link">Services <i data-lucide="chevron-down" size="13"></i></div>
        <div class="mega-dropdown">
          <a href="../services/home-loan.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="home" size="18"></i></div><div><strong>Home Loan / Buy a Home</strong><span>Secure your dream home</span></div></a>
          <a href="../services/investment-property.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="building-2" size="18"></i></div><div><strong>Investment Property Loan</strong><span>Grow your portfolio</span></div></a>
          <a href="../services/refinance.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="refresh-cw" size="18"></i></div><div><strong>Refinance Mortgage</strong><span>Lower your rate &amp; save</span></div></a>
          <a href="../services/pre-approval.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="check-circle" size="18"></i></div><div><strong>Mortgage Pre-Approval</strong><span>Know your buying power</span></div></a>
          <a href="../services/first-home-buyer.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="key" size="18"></i></div><div><strong>First Home Buyer Mortgage</strong><span>Your first step</span></div></a>
          <a href="../services/next-home-buyer.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="compass" size="18"></i></div><div><strong>Next Home Buyer Mortgage</strong><span>Upgrade or move</span></div></a>
          <a href="../services/self-employed.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="briefcase" size="18"></i></div><div><strong>Self Employed Mortgage</strong><span>Flexible lending</span></div></a>
          <a href="../services/asset-finance.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="car" size="18"></i></div><div><strong>Asset Finance</strong><span>Vehicles &amp; Equipment</span></div></a>
          <a href="../services/commercial-property.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="store" size="18"></i></div><div><strong>Commercial Property Loan</strong><span>Commercial real estate</span></div></a>
          <a href="../services/construction-loan.html" class="mega-item"><div class="mega-item-icon"><i data-lucide="hammer" size="18"></i></div><div><strong>Construction Loan</strong><span>Build from scratch</span></div></a>
        </div>
      </div>
      <div class="nav-item"><div class="dropdown-trigger nav-link">Calculators <i data-lucide="chevron-down" size="13"></i></div><div class="dropdown-menu"><a href="../calculators/mortgage-calculator.html" class="dropdown-item">Mortgage Calculator</a><a href="../calculators/borrowing-power.html" class="dropdown-item">Borrowing Power</a><a href="../calculators/refinance-savings.html" class="dropdown-item">Refinance Savings</a></div></div>
      <div class="nav-item"><div class="dropdown-trigger nav-link">Resources <i data-lucide="chevron-down" size="13"></i></div><div class="dropdown-menu" style="min-width:220px;"><div class="dropdown-label">Guides</div><a href="../guides/how-mortgage-works.html" class="dropdown-item">How Mortgage Works</a><a href="../guides/first-home-guide.html" class="dropdown-item">First Home Guide</a><div class="dropdown-divider"></div><div class="dropdown-label">Market</div><a href="../market-report.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#128202; Market Report</a><a href="../lenders.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#127976; Lenders</a><div class="dropdown-divider"></div><div class="dropdown-label">Stories</div><a href="../testimonials/reviews.html" class="dropdown-item">Client Reviews</a><a href="../testimonials/success-stories.html" class="dropdown-item">Success Stories</a><div class="dropdown-divider"></div><a href="../faq.html" class="dropdown-item">FAQ</a><a href="../blog.html" class="dropdown-item">Blog</a></div></div>
      <a href="../about.html" class="nav-link">About</a><a href="../contact.html" class="nav-link">Contact</a>
      <a href="../services/pre-approval.html" class="btn-nav-cta">Get Pre-Approved &#x2192;</a>
    </nav>
    <button id="mobile-menu-btn" class="md-hidden" style="background:none;border:1px solid rgba(181,206,176,0.5);padding:0.5rem 1rem;border-radius:0.5rem;cursor:pointer;display:flex;align-items:center;gap:0.5rem;"><i data-lucide="menu"></i><span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;">Menu</span></button>
  </div>
</header>
<div id="fullscreen-menu" style="display:none;position:fixed;inset:0;background:rgba(255,255,255,0.98);z-index:999;opacity:0;transition:opacity 0.3s ease;overflow-y:auto;padding-bottom:4rem;">
  <div class="container" style="display:flex;justify-content:flex-end;padding-top:1.5rem;">
    <button id="close-menu-btn" style="background:none;border:none;cursor:pointer;padding:0.5rem;display:flex;align-items:center;gap:0.5rem;"><span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;">Close</span><i data-lucide="x" size="24"></i></button>
  </div>
  <div class="container" style="display:flex;flex-direction:column;align-items:center;padding-top:2rem;gap:1.5rem;text-align:center;">
    <a href="../index.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Home</a>
    <div style="width:100%;max-width:300px;">
      <div class="mobile-dropdown-trigger" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:0.5rem;padding:0.5rem 0;">Services <i data-lucide="chevron-down" size="20"></i></div>
      <div class="mobile-dropdown-menu" style="display:none;flex-direction:column;gap:1rem;background:var(--finch-mist);padding:1.5rem;border-radius:1rem;margin-top:0.5rem;">
        <a href="../services/home-loan.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Home Loan</a>
        <a href="../services/first-home-buyer.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">First Home Buyer</a>
        <a href="../services/investment-property.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Investment Property</a>
        <a href="../services/refinance.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Refinance</a>
        <a href="../services/pre-approval.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Pre-Approval</a>
      </div>
    </div>
    <a href="../calculators.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Calculators</a>
    <a href="../lenders.html" style="font-size:1.5rem;font-weight:700;color:var(--finch-forest);text-decoration:none;">&#127976; Lenders</a>
    <a href="../about.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">About</a>
    <a href="../contact.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Contact</a>
    <a href="../services/pre-approval.html" class="btn-primary" style="margin-top:1rem;width:100%;max-width:300px;">Get Pre-Approved</a>
  </div>
</div>"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="../index.html">Finch<span>.</span></a><p>New Zealand's trusted independent mortgage broker. Expert advice, 20+ lenders, fast approvals.</p></div>
      <div class="footer-col"><h4>Services</h4><a href="../services/home-loan.html">Home Loan</a><a href="../services/investment-property.html">Investment Property</a><a href="../services/refinance.html">Refinance</a><a href="../services/pre-approval.html">Pre-Approval</a><a href="../services/first-home-buyer.html">First Home Buyer</a><a href="../services/self-employed.html">Self Employed</a></div>
      <div class="footer-col"><h4>Resources</h4><a href="../market-report.html">Market Report</a><a href="../lenders.html">Lenders</a><a href="../guides/how-mortgage-works.html">How Mortgages Work</a><a href="../guides/first-home-guide.html">First Home Guide</a><a href="../faq.html">FAQ</a><a href="../blog.html">Blog</a></div>
      <div class="footer-col"><h4>Company</h4><a href="../about.html">About Us</a><a href="../contact.html">Contact</a><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a></div>
    </div>
    <div class="footer-bottom"><span>&#169; 2026 Finch Mortgages Limited. FSP1011206 | FSPR FSP1011125. All rights reserved.</span><div style="display:flex;gap:1.5rem;"><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a></div></div>
  </div>
</footer>"""

CATEGORIES = [
    {
        "file": "major-banks.html",
        "title": "Major & Registered Banks (Tier 1)",
        "badge": "Core Lending",
        "intro": "The cornerstone of New Zealand lending. Registered banks offer competitive carded interest rates, fixed-term structures, and cater to standard mortgage applications (PAYE income, 20%+ deposit, strong credit). However, their policies can be rigid, meaning if you fall outside their standard criteria, an approved non-bank partner may be recommended.",
        "lenders": [
            {"initial": "A", "name": "ANZ", "desc": "New Zealand's largest mortgage lender by book size. Highly competitive on 1-year and 2-year fixed rates with strong property investor packages.", "url": "https://www.anz.co.nz/", "review": "anz-home-loan-review.html"},
            {"initial": "B", "name": "BNZ", "desc": "Excellent tailorable TotalMoney offset structures linking up to 50 accounts. Highly preferred for self-employed professionals, doctors, and property investors.", "url": "https://www.bnz.co.nz/", "review": "bnz-home-loan-review.html"},
            {"initial": "CC", "name": "China Construction Bank", "desc": "Full registered bank in NZ backed by global institutional strength. Tailored residential mortgages, high-net-worth borrowing, and cross-border property finance.", "url": "https://nz.ccb.com/", "review": "china-construction-bank-mortgage-review.html"},
            {"initial": "H", "name": "Heartland Bank", "desc": "NZ-operated registered bank. Market leader in home equity release and reverse mortgages, alongside competitive digital home loans.", "url": "https://www.heartland.co.nz/", "review": "heartland-bank-mortgage-review.html"},
            {"initial": "S", "name": "SBS Bank", "desc": "New Zealand customer-owned mutual bank known for market-leading first home buyer combo packages, competitive rates, and personal service.", "url": "https://www.sbsbank.co.nz/", "review": "sbs-mortgage-review.html"},
            {"initial": "C", "name": "The Co-operative Bank", "desc": "Customer-owned registered bank sharing annual profits with borrowers as direct account rebates. Consistently tops trust and satisfaction surveys.", "url": "https://www.co-operativebank.co.nz/", "review": "co-operative-bank-mortgage-review.html"}
        ],
        "faqs": [
            {"q": "How much deposit do I need for a registered bank?", "a": "Under current RBNZ rules, banks generally require a 20% deposit for an owner-occupied existing home, though they can lend to a small proportion of borrowers with as little as 5-10%. For new builds, 10% is usually sufficient. Investors typically need 35%."},
            {"q": "Are bank mortgage rates negotiable?", "a": "Yes. While the advertised 'special' rate is often the baseline, Finch advisors frequently negotiate unadvertised discounts (5-15bps) or superior cash contributions for strong applications."},
            {"q": "What happens if a registered bank declines me?", "a": "A decline from one bank does not mean a decline from all. Banks have different risk appetites. If main banks decline, we pivot to an approved non-bank lender structured to suit your profile."}
        ]
    },
    {
        "file": "non-bank-lenders.html",
        "title": "Non-Bank Lenders",
        "badge": "Flexible Lending",
        "intro": "Regulated financial institutions that offer mortgages but don't hold full retail banking licenses. Non-banks assess risk differently and are vital for self-employed individuals without 2 years of financials, borrowers with past credit issues, or property investors who have hit bank lending caps.",
        "lenders": [
            {"initial": "A", "name": "Avanti Finance Property Loans", "desc": "Provides near-prime residential mortgages, fast bridging finance, second mortgages, and flexible solutions for self-employed borrowers.", "url": "https://www.avantifinance.co.nz/", "review": "avanti-finance-mortgage-review.html"},
            {"initial": "B", "name": "Basecorp Finance", "desc": "A premier privately owned specialist lender known for ultra-fast approvals (within 24 hours) and short-to-medium term property-backed lending.", "url": "https://www.basecorp.co.nz/", "review": "basecorp-mortgage-review.html"},
            {"initial": "F", "name": "First Mortgage Trust", "desc": "New Zealand's largest non-bank mortgage fund manager with over 28 years of trusted property lending across residential and commercial sectors.", "url": "https://www.fmt.co.nz/", "review": "first-mortgage-trust-review.html"},
            {"initial": "G", "name": "General Finance", "desc": "NZX-listed licensed Non-Bank Deposit Taker (NBDT) offering first and second residential mortgages with common-sense underwriting.", "url": "https://www.generalfinance.co.nz/", "review": "general-finance-mortgage-review.html"},
            {"initial": "L", "name": "Liberty Financial", "desc": "A versatile non-bank supporting everything from prime mortgages to specialist custom loans for self-employed or unconventional scenarios.", "url": "https://www.liberty.co.nz/", "review": "liberty-financial-mortgage-review.html"},
            {"initial": "P", "name": "Pepper Money", "desc": "Provides common-sense lending approaches, assessing applications on individual merit and offering market-leading Alt-Doc solutions.", "url": "https://www.peppermoney.co.nz/", "review": "pepper-money-mortgage-review.html"},
            {"initial": "S", "name": "Southern Cross Partners", "desc": "NZ peer-to-peer and mortgage specialist offering short-term property-backed finance, bridging, and equity release loans.", "url": "https://www.southerncrosspartners.co.nz/", "review": "southern-cross-partners-review.html"}
        ],
        "faqs": [
            {"q": "Are non-bank lenders safe?", "a": "Absolutely. While they aren't registered banks, they are heavily regulated by the Financial Markets Authority (FMA) and must adhere to the Credit Contracts and Consumer Finance Act (CCCFA). Since you owe them money (not the other way around), your risk is minimal."},
            {"q": "Are non-bank rates much higher than major banks?", "a": "It depends on the product. Some 'prime' non-bank products offer rates very close to major banks. 'Specialist' products for credit impairment or low-doc naturally carry a risk premium, often 1-3% higher than bank specials."},
            {"q": "Can I refinance from a non-bank to a registered bank later?", "a": "Yes, this is a very common strategy. We often use a non-bank lender as a 12-24 month stepping stone (e.g., while waiting for a credit mark to clear or 2 years of business financials to accrue), and then refinance you to a lower bank rate when eligible."}
        ]
    },
    {
        "file": "specialist-lenders.html",
        "title": "Specialist Lenders",
        "badge": "Niche Solutions",
        "intro": "Specialist lenders fill the gaps where traditional lending falls short. They focus heavily on property asset quality, speed of capital delivery, and bespoke structures. These lenders are essential for short-term bridging finance, rapid property flips, developing land, or commercial-residential overlaps.",
        "lenders": [
            {"initial": "C", "name": "CFML", "desc": "Established NZ mortgage fund manager providing tailored first mortgages, commercial property, and residential development loans.", "url": "https://www.cfml.nz/", "review": "cfml-mortgage-review.html"},
            {"initial": "CR", "name": "Cressida Capital", "desc": "Boutique property financiers specializing in bespoke short-term lending, mezzanine debt, bridging, and urgent settlement deadlines.", "url": "https://www.cressida.co.nz/", "review": "cressida-capital-mortgage-review.html"},
            {"initial": "D", "name": "DBR", "desc": "Experienced NZ property financiers providing short-to-medium term mortgage lending for residential bridging, refurbishment, and land.", "url": "https://www.dbr.co.nz/", "review": "dbr-property-financiers-review.html"},
            {"initial": "F", "name": "Finbase", "desc": "Modern technology-driven non-bank property lender delivering fast approvals and flexible criteria for self-employed and contract income.", "url": "https://www.finbase.co.nz/", "review": "finbase-mortgage-review.html"},
            {"initial": "FP", "name": "Funding Partners", "desc": "Private real estate funding specialist providing tailored private debt and equity solutions for property projects without bank friction.", "url": "https://www.fundingpartners.co.nz/", "review": "funding-partners-review.html"},
            {"initial": "G", "name": "GEM By Latitude", "desc": "Structured personal and property debt consolidation solutions helping borrowers tidy credit ahead of or alongside home loan borrowing.", "url": "https://www.gemfinance.co.nz/", "review": "gem-by-latitude-review.html"},
            {"initial": "PC", "name": "Pallas Capital", "desc": "Premier institutional non-bank real estate financier underwriting large commercial, development, and high-capacity bridging facilities.", "url": "https://www.pallascapital.co.nz/", "review": "pallas-capital-mortgage-review.html"},
            {"initial": "P", "name": "Prospa", "desc": "Australasia's leading small business finance specialist. Fast commercial capital keeping personal residential equity unencumbered.", "url": "https://www.prospa.co.nz/", "review": "prospa-finance-review.html"},
            {"initial": "X", "name": "Xceda Finance", "desc": "Over 35 years of non-bank property, bridging, and second mortgage finance with responsive preliminary approvals and flexible security.", "url": "https://www.xceda.co.nz/", "review": "xceda-finance-review.html"}
        ],
        "faqs": [
            {"q": "What is bridging finance?", "a": "Bridging finance is a short-term loan used to cover the gap when buying a new property before your existing property has sold. Specialist lenders are often much more accommodating with bridging loans than major banks."},
            {"q": "How fast can a specialist lender approve a loan?", "a": "Because they don't rely heavily on automated scoring and have flatter management structures, some specialist lenders can grant conditional approval within 24-48 hours if the property asset is strong."},
            {"q": "Do I need proof of income for specialist lenders?", "a": "While you must still demonstrate borrowing capacity under the CCCFA, specialist lenders offer asset-backed or low-doc products where substantial property equity simplifies income verification."}
        ]
    },
    {
        "file": "credit-unions.html",
        "title": "Credit Unions & Customer-Owned",
        "badge": "Community Focused",
        "intro": "Unlike corporate banks which prioritize profits for external shareholders, Credit Unions and mutual financial institutions are 100% owned by their members. They reinvest profits to offer competitive rates and lower fees. They offer a highly personalized, human approach to underwriting.",
        "lenders": [
            {"initial": "U", "name": "Unity Credit Union Home Loans", "desc": "New Zealand's leading member-owned financial cooperative providing accessible, human-led home loans with no profit extraction by overseas shareholders.", "url": "https://unitymoney.co.nz/", "review": "unity-credit-union-review.html"},
            {"initial": "S", "name": "SBS Bank (Customer-Owned)", "desc": "Customer-owned mutual building society offering personal service, competitive fixed home loans, and famous FirstHome Combo packages.", "url": "https://www.sbsbank.co.nz/", "review": "sbs-mortgage-review.html"},
            {"initial": "C", "name": "The Co-operative Bank (Mutual)", "desc": "New Zealand's customer-owned bank where borrower profits are returned annually as cash rebates directly to members.", "url": "https://www.co-operativebank.co.nz/", "review": "co-operative-bank-mortgage-review.html"}
        ],
        "faqs": [
            {"q": "Who can join Unity Credit Union?", "a": "Unity Credit Union is open to everyday New Zealanders nationwide. Anyone living in NZ can join and apply for a mortgage. We manage the application and onboarding for you."},
            {"q": "Are credit union mortgage rates competitive with major banks?", "a": "Often, yes. Because member-owned institutions do not extract large profits for offshore parent companies, they frequently offer fixed rates that match or undercut major bank specials, with lower account fees."},
            {"q": "How does underwriting differ?", "a": "Credit union underwriting is human-led. Lending managers evaluate overall character, savings history, and personal context rather than relying purely on automated algorithms."}
        ]
    }
]

def make_page(c):
    # Build lender cards
    lender_cards = ""
    for l in c["lenders"]:
        rev_btn = f'<a href="{l["review"]}" style="font-size:0.85rem;font-weight:700;color:var(--finch-forest);text-decoration:none;display:inline-flex;align-items:center;gap:0.4rem;">Read Review →</a>' if "review" in l else ""
        lender_cards += f"""
        <div style="background:white;border:1px solid rgba(181,206,176,0.4);border-radius:1rem;padding:2rem;display:flex;flex-direction:column;gap:1rem;">
          <div style="width:64px;height:64px;background:var(--finch-mist);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--finch-forest);font-weight:800;font-size:1.5rem;border:1px solid rgba(181,206,176,0.5);">{l['initial']}</div>
          <h3 style="font-size:1.25rem;font-weight:700;color:var(--neutral-black);">{l['name']}</h3>
          <p style="font-size:0.85rem;color:var(--neutral-medGray);line-height:1.6;flex-grow:1;">{l['desc']}</p>
          <div style="display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap;margin-top:0.5rem;">
            {rev_btn}
            <a href="{l['url']}" target="_blank" rel="noopener" style="font-size:0.85rem;font-weight:600;color:var(--neutral-medGray);text-decoration:none;display:inline-flex;align-items:center;gap:0.4rem;">Visit Website <i data-lucide="external-link" size="14"></i></a>
          </div>
        </div>"""
    
    # Build FAQs
    faq_html = ""
    for idx, f in enumerate(c["faqs"]):
        border = 'border-bottom:1px solid rgba(181,206,176,0.4);' if idx < len(c["faqs"])-1 else ''
        faq_html += f"""
        <div style="{border}">
          <button onclick="toggleFaq(this)" style="width:100%;text-align:left;background:none;border:none;padding:1.5rem 0;display:flex;align-items:center;justify-content:space-between;cursor:pointer;gap:1rem;">
            <span style="font-size:1rem;font-weight:700;color:var(--neutral-black);line-height:1.4;">{f['q']}</span>
            <span class="faq-icon" style="color:var(--finch-forest);flex-shrink:0;font-size:1.25rem;font-weight:300;transition:transform 0.3s;">+</span>
          </button>
          <div class="faq-body" style="display:none;padding-bottom:1.5rem;">
            <p style="color:var(--neutral-medGray);line-height:1.75;">{f['a']}</p>
          </div>
        </div>"""

    # Build Schema
    import json
    faq_entities = []
    for f in c["faqs"]:
        faq_entities.append({
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f["a"]
            }
        })
    schema_dict = {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "MortgageBroker",
          "@id": "https://www.finchmortgages.co.nz/#organization",
          "name": "Finch Mortgage",
          "alternateName": "Finch Mortgages",
          "url": "https://www.finchmortgages.co.nz/",
          "logo": "https://www.finchmortgages.co.nz/images/finch-logo.png",
          "image": "https://www.finchmortgages.co.nz/images/finch-logo.png",
          "telephone": "+64273433293",
          "email": "Mukhtar@finchmortgages.co.nz",
          "priceRange": "$0 broker fee",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "17a Marlene Ave",
            "addressLocality": "Te Atatu South",
            "addressRegion": "Auckland",
            "postalCode": "0610",
            "addressCountry": "NZ"
          },
          "areaServed": {
            "@type": "Country",
            "name": "New Zealand"
          },
          "founder": {
            "@type": "Person",
            "name": "Mukhtar Kiyani"
          },
          "foundingDate": "2010",
          "sameAs": [
            "https://www.finchmortgages.co.nz/about.html",
            "https://www.finchmortgages.co.nz/contact.html"
          ]
        },
        {
          "@type": "WebSite",
          "@id": "https://www.finchmortgages.co.nz/#website",
          "url": "https://www.finchmortgages.co.nz/",
          "name": "Finch Mortgage",
          "publisher": {
            "@id": "https://www.finchmortgages.co.nz/#organization"
          },
          "inLanguage": "en-NZ",
          "potentialAction": {
            "@type": "SearchAction",
            "target": {
              "@type": "EntryPoint",
              "urlTemplate": "https://www.finchmortgages.co.nz/blog.html?q={search_term_string}"
            },
            "query-input": "required name=search_term_string"
          }
        },
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Home",
              "item": "https://www.finchmortgages.co.nz/"
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": "Lenders",
              "item": "https://www.finchmortgages.co.nz/lenders.html"
            },
            {
              "@type": "ListItem",
              "position": 3,
              "name": c['title'],
              "item": f"https://www.finchmortgages.co.nz/lenders/{c['file']}"
            }
          ],
          "@id": f"https://www.finchmortgages.co.nz/lenders/{c['file']}#breadcrumbs"
        },
        {
          "@type": "WebPage",
          "@id": f"https://www.finchmortgages.co.nz/lenders/{c['file']}#webpage",
          "url": f"https://www.finchmortgages.co.nz/lenders/{c['file']}",
          "name": f"{c['title']} in NZ | Finch Mortgage",
          "description": f"Detailed guide to {c['title']} in New Zealand. Compare partners, understand policies, and find out if this lender type matches your mortgage needs.",
          "inLanguage": "en-NZ",
          "isPartOf": {
            "@id": "https://www.finchmortgages.co.nz/#website"
          },
          "publisher": {
            "@id": "https://www.finchmortgages.co.nz/#organization"
          },
          "breadcrumb": {
            "@id": f"https://www.finchmortgages.co.nz/lenders/{c['file']}#breadcrumbs"
          }
        }
      ]
    }
    if faq_entities:
        schema_dict["@graph"].append({
            "@type": "FAQPage",
            "mainEntity": faq_entities
        })
    schema_json = f'<script type="application/ld+json">\n{json.dumps(schema_dict, indent=2, ensure_ascii=False)}\n</script>'

    return f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c['title']} in NZ | Finch Mortgage</title>
  <meta name="description" content="Detailed guide to {c['title']} in New Zealand. Compare partners, understand policies, and find out if this lender type matches your mortgage needs.">
  <link rel="canonical" href="https://www.finchmortgages.co.nz/lenders/{c['file']}">
  <link href="/favicon.png" rel="icon" type="image/png">
  
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{c['title']} in NZ | Finch Mortgage">
  <meta property="og:description" content="Detailed guide to {c['title']} in New Zealand. Compare partners, understand policies, and find out if this lender type matches your mortgage needs.">
  <meta property="og:url" content="https://www.finchmortgages.co.nz/lenders/{c['file']}">
  <meta property="og:image" content="https://www.finchmortgages.co.nz/images/og-default.jpg">
  <meta property="og:site_name" content="Finch Mortgage">
  <meta property="og:locale" content="en_NZ">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{c['title']} in NZ | Finch Mortgage">
  <meta name="twitter:description" content="Detailed guide to {c['title']} in New Zealand. Compare partners, understand policies, and find out if this lender type matches your mortgage needs.">
  <meta name="twitter:image" content="https://www.finchmortgages.co.nz/images/og-default.jpg">

  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '984298931136124');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" alt="Facebook Pixel" src="https://www.facebook.com/tr?id=984298931136124&ev=PageView&noscript=1" /></noscript>
  <!-- End Meta Pixel Code -->

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap"></noscript>
  <script src="https://unpkg.com/lucide@latest" defer></script>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
{NAV}
<main style="padding-top:80px;">

  <!-- Hero Start -->
  <section style="background:var(--finch-forest);padding:4rem 0 5rem;position:relative;overflow:hidden;">
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 50%,rgba(181,206,176,0.15) 0%,transparent 65%);pointer-events:none;"></div>
    <div class="container">
      <nav class="breadcrumb" style="margin-bottom:1.5rem;">
        <a href="../index.html" style="color:rgba(255,255,255,0.65);">Home</a>
        <span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span>
        <a href="../lenders.html" style="color:rgba(255,255,255,0.65);">Lenders Hub</a>
        <span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span>
        <span style="color:white;">{c['title']}</span>
      </nav>
      <div style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);color:var(--finch-sage);border-radius:999px;padding:0.25rem 0.9rem;font-size:0.65rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.25rem;border:1px solid rgba(181,206,176,0.3);">{c['badge']}</div>
      <h1 style="color:white;font-family:var(--font-display);font-size:clamp(2rem,4vw,3.2rem);font-weight:700;line-height:1.15;margin-bottom:1.25rem;max-width:780px;">{c['title']}</h1>
      <p style="color:rgba(255,255,255,0.8);max-width:680px;line-height:1.75;font-size:1.05rem;">{c['intro']}</p>
    </div>
  </section>

  <!-- Lenders Grid -->
  <section style="padding:5rem 0;background:var(--finch-mist);">
    <div class="container">
      <div class="section-label"><span>Our Partners</span></div>
      <h2 class="section-heading" style="margin-top:0.75rem;margin-bottom:2.5rem;">Finch's {c['title']}<br><em>Network.</em></h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;">
        {lender_cards}
      </div>
    </div>
  </section>

  <!-- FAQs -->
  <section style="padding:5rem 0;background:white;">
    <div class="container">
      <div style="max-width:820px;margin:0 auto;">
        <div class="section-label"><span>FAQs</span></div>
        <h2 class="section-heading" style="margin-top:0.75rem;margin-bottom:2.5rem;">Questions About<br><em>{c['title']}</em></h2>
        <div style="display:flex;flex-direction:column;gap:0;">
          {faq_html}
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section style="padding:5rem 0;background:var(--finch-forest);text-align:center;">
    <div class="container">
      <div style="max-width:600px;margin:0 auto;">
        <h2 style="color:white;font-size:clamp(1.75rem,3.5vw,2.5rem);font-weight:700;margin-bottom:1rem;">Match with the perfect lender today.</h2>
        <p style="color:rgba(255,255,255,0.75);line-height:1.75;margin-bottom:2rem;">Speak to an advisor. We'll assess your situation and recommend exactly which lenders will approve your loan at the best terms.</p>
        <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
          <a href="../services/pre-approval.html" class="btn-primary" style="background:white;color:var(--finch-forest);">Get Pre-Approved →</a>
          <a href="../contact.html" class="btn-cta-outline">Contact Us</a>
        </div>
      </div>
    </div>
  </section>

</main>
{FOOTER}
<script src="../script.js" defer></script>
<script>
  document.addEventListener("DOMContentLoaded",function(){{if(typeof lucide!=="undefined")lucide.createIcons();}});
  function toggleFaq(btn) {{
    const body = btn.nextElementSibling;
    const icon = btn.querySelector('.faq-icon');
    const isOpen = body.style.display === 'block';
    
    // Select siblings inside the parent container to close
    const allBodies = btn.closest('div').parentElement.querySelectorAll('.faq-body');
    const allIcons = btn.closest('div').parentElement.querySelectorAll('.faq-icon');
    
    allBodies.forEach(b => b.style.display = 'none');
    allIcons.forEach(i => {{ i.textContent = '+'; i.style.transform = 'rotate(0deg)'; }});
    
    if (!isOpen) {{
      body.style.display = 'block';
      icon.textContent = '−';
      icon.style.transform = 'rotate(180deg)';
    }}
  }}
</script>
</body>
</html>"""

for c in CATEGORIES:
    path = os.path.join(OUT, c["file"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(make_page(c))
    print(f"  CREATED: lenders/{c['file']}")

print("Done generating 4 category pages.")
