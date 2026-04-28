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
        "title": "Major Banks (Tier 1)",
        "badge": "Core Lending",
        "intro": "The cornerstone of New Zealand lending. Major banks offer the most competitive headline rates and cater perfectly to standard mortgage applications (PAYE income, 20%+ deposit, strong credit). However, their policies can be rigid, meaning if you fall outside their standard criteria, approval can be difficult.",
        "lenders": [
            {"initial": "A", "name": "ANZ", "desc": "New Zealand's largest mortgage lender. Highly competitive on 1-year and 2-year fixed rates. Strong property investor packages.", "url": "https://www.anz.co.nz/"},
            {"initial": "AS", "name": "ASB", "desc": "Market leaders in construction lending and turnaround times. Often the first major bank to announce rate cuts in a falling market.", "url": "https://www.asb.co.nz/"},
            {"initial": "B", "name": "BNZ", "desc": "Excellent tailorable loan structures. Highly preferred for self-employed professionals, doctors, and small business owners.", "url": "https://www.bnz.co.nz/"},
            {"initial": "W", "name": "Westpac", "desc": "Focuses heavily on sustainable lending. Offers low or zero-interest loans for warm, healthy home upgrades and EVs.", "url": "https://www.westpac.co.nz/"},
            {"initial": "K", "name": "Kiwibank", "desc": "100% locally owned. Frequently presents excellent switching cash contributions and highly competitive short-term specials.", "url": "https://www.kiwibank.co.nz/"}
        ],
        "faqs": [
            {"q": "How much deposit do I need for a major bank?", "a": "Under current RBNZ rules, banks generally require a 20% deposit for an owner-occupied existing home, though they can lend to a small proportion of borrowers with as little as 5-10%. For new builds, 10% is usually sufficient. Investors typically need 35%."},
            {"q": "Are major bank rates negotiable?", "a": "Yes. While the advertised 'special' rate is often the baseline, Finch advisors frequently negotiate unadvertised discounts (5-15bps) or superior cash contributions for strong applications."},
            {"q": "What happens if a major bank declines me?", "a": "A decline from one major bank does not mean a decline from all. Banks have different risk appetites. If all major banks decline, we pivot to a non-bank lender structured to suit your profile."}
        ]
    },
    {
        "file": "non-bank-lenders.html",
        "title": "Non-Bank Lenders",
        "badge": "Flexible Lending",
        "intro": "Regulated financial institutions that offer mortgages but don't hold banking licenses or offer standard checking accounts. Non-banks are vital because they assess risk differently. They are ideal for self-employed individuals without 2 years of financials, borrowers with past credit issues, or property investors who have hit bank lending caps.",
        "lenders": [
            {"initial": "R", "name": "Resimac", "desc": "A leading non-bank offering alternative documentation loans. Perfect for self-employed borrowers or those with unique income streams.", "url": "https://www.resimac.co.nz/"},
            {"initial": "B", "name": "Bluestone", "desc": "Specialises in clear-cut solutions for borrowers with credit impairments or those needing rapid capital outside strict bank rules.", "url": "https://www.bluestone.net.nz/"},
            {"initial": "P", "name": "Pepper Money", "desc": "Provides common-sense lending approaches, assessing applications on their individual merits rather than rigid automated algorithms.", "url": "https://www.peppermoney.co.nz/"},
            {"initial": "L", "name": "Liberty", "desc": "A versatile lender supporting everything from prime mortgages to specialist custom loans for unconventional properties or situations.", "url": "https://www.liberty.co.nz/"}
        ],
        "faqs": [
            {"q": "Are non-bank lenders safe?", "a": "Absolutely. While they aren't registered banks, they are heavily regulated by the Financial Markets Authority (FMA) and must adhere to the Credit Contracts and Consumer Finance Act (CCCFA). Since you owe them money (not the other way around), your risk is minimal."},
            {"q": "Are non-bank rates much higher than major banks?", "a": "It depends on the product. Some 'prime' non-bank products offer rates identical to or even lower than major banks. 'Specialist' products for credit impairment naturally carry a risk premium, often 1-3% higher than bank specials."},
            {"q": "Can I refinance from a non-bank to a major bank later?", "a": "Yes, this is a very common strategy. We often use a non-bank lender as a 12-24 month stepping stone (e.g., while waiting for a credit mark to clear or 2 years of business financials to accrue), and then refinance you to a lower major bank rate when eligible."}
        ]
    },
    {
        "file": "specialist-lenders.html",
        "title": "Specialist Lenders",
        "badge": "Niche Solutions",
        "intro": "Specialist lenders fill the gaps where traditional lending falls short. They focus heavily on the quality of the property asset rather than purely relying on borrower income. These lenders are essential for short-term bridging finance, rapid property flips, developing bare land, or complex commercial-residential overlaps.",
        "lenders": [
            {"initial": "A", "name": "Avanti Finance", "desc": "Provides near-prime and specialist mortgages, bridging finance, and solutions for those needing quick turnarounds.", "url": "https://www.avantifinance.co.nz/"},
            {"initial": "B", "name": "Basecorp Finance", "desc": "A privately owned specialist lender known for ultra-fast approvals and short-to-medium term property-backed lending.", "url": "https://www.basecorp.co.nz/"},
            {"initial": "P", "name": "Prospa", "desc": "While primarily focused on SME lending, Prospa offers vital commercial financing solutions that integrate with personal property portfolios.", "url": "https://www.prospa.co.nz/"}
        ],
        "faqs": [
            {"q": "What is bridging finance?", "a": "Bridging finance is a short-term loan used to cover the gap when buying a new property before your existing property has sold. Specialist lenders are often much more accommodating with bridging loans than major banks."},
            {"q": "How fast can a specialist lender approve a loan?", "a": "Because they don't rely heavily on automated scoring and have flatter management structures, some specialist lenders can grant conditional approval within 24-48 hours if the property asset is strong."},
            {"q": "Do I need proof of income for specialist lenders?", "a": "While you must still demonstrate borrowing capacity under the CCCFA, specialist lenders offer 'asset-lend' or 'low-doc' products. This means if you have substantial equity in a property, the income verification requirements are significantly lower."}
        ]
    },
    {
        "file": "credit-unions.html",
        "title": "Credit Unions",
        "badge": "Community Focused",
        "intro": "Unlike major banks which must maximize profits for external shareholders, Credit Unions are 100% owned by their members (customers). They reinvest their profits to offer competitive rates and lower fees. They offer a highly personalized, human approach to underwriting—ideal for borrowers who fall slightly outside the strict algorithms of large banks.",
        "lenders": [
            {"initial": "U", "name": "Unity (formerly NZCU)", "desc": "A major member-owned credit union providing competitive home loans with a deeply personalized, community-focused approach to lending.", "url": "https://unitymoney.co.nz/"},
            {"initial": "F", "name": "First Credit Union", "desc": "New Zealand's largest credit union, offering straightforward mortgages without the rigid corporate structures of major banks.", "url": "https://www.firstcreditunion.co.nz/"},
            {"initial": "P", "name": "Police Credit Union", "desc": "Specialist community lender offering exceptional rates and dedicated service exclusively for members of the NZ Police and their families.", "url": "https://www.policecu.org.nz/"}
        ],
        "faqs": [
            {"q": "Do I have to belong to a specific group to join a Credit Union?", "a": "Some are restricted by profession (like the Police Credit Union), but many broad credit unions (like Unity or First Credit Union) are open to the general public. We manage the eligibility checking for you."},
            {"q": "Are their mortgage rates better than major banks?", "a": "Often, yes. Because they do not have to pay large dividends to external shareholders, Credit Unions can frequently undercut major bank fixed rates by 10-20 basis points, and they heavily discount or waive loan application fees."},
            {"q": "Is the application process different?", "a": "It's more human. Credit union lending managers often look at your overall character, savings history, and localized circumstances rather than just running an automated credit score. This makes them fantastic for borrowers needing a 'common sense' review."}
        ]
    }
]

def make_page(c):
    # Build lender cards
    lender_cards = ""
    for l in c["lenders"]:
        lender_cards += f"""
        <div style="background:white;border:1px solid rgba(181,206,176,0.4);border-radius:1rem;padding:2rem;display:flex;flex-direction:column;gap:1rem;">
          <div style="width:64px;height:64px;background:var(--finch-mist);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--finch-forest);font-weight:800;font-size:1.5rem;border:1px solid rgba(181,206,176,0.5);">{l['initial']}</div>
          <h3 style="font-size:1.25rem;font-weight:700;color:var(--neutral-black);">{l['name']}</h3>
          <p style="font-size:0.85rem;color:var(--neutral-medGray);line-height:1.6;flex-grow:1;">{l['desc']}</p>
          <a href="{l['url']}" target="_blank" rel="nofollow" style="font-size:0.85rem;font-weight:700;color:var(--finch-forest);text-decoration:none;display:inline-flex;align-items:center;gap:0.4rem;margin-top:0.5rem;">Visit Website <i data-lucide="external-link" size="14"></i></a>
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

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c['title']} in NZ | Finch Mortgage</title>
  <meta name="description" content="Detailed guide to {c['title']} in New Zealand. Compare partners, understand policies, and find out if this lender type matches your mortgage needs.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
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
<script src="../script.js"></script>
<script>
  if (typeof lucide !== 'undefined') lucide.createIcons();
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
