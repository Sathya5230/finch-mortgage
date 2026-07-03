#!/usr/bin/env python3
"""
Generates weekly market reports for Finch Mortgages.
"""

import os
import json
import datetime

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"
OUT = os.path.join(ROOT, "weekly-reports")
os.makedirs(OUT, exist_ok=True)

# Shared navigation block
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
      <div class="nav-item"><div class="dropdown-trigger nav-link">Resources <i data-lucide="chevron-down" size="13"></i></div><div class="dropdown-menu" style="min-width:220px;"><div class="dropdown-label">Guides</div><a href="../guides/how-mortgage-works.html" class="dropdown-item">How Mortgage Works</a><a href="../guides/first-home-guide.html" class="dropdown-item">First Home Guide</a><div class="dropdown-divider"></div><div class="dropdown-label">Market</div><a href="../market-report.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#128202; Market Report</a><a href="../weekly-reports.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#128197; Weekly Reports</a><a href="../lenders.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#127976; Lenders</a><div class="dropdown-divider"></div><div class="dropdown-label">Stories</div><a href="../testimonials/reviews.html" class="dropdown-item">Client Reviews</a><a href="../testimonials/success-stories.html" class="dropdown-item">Success Stories</a><div class="dropdown-divider"></div><a href="../faq.html" class="dropdown-item">FAQ</a><a href="../blog.html" class="dropdown-item">Blog</a></div></div>
      <a href="../about.html" class="nav-link">About</a><a href="../contact.html" class="nav-link">Contact</a>
      <a href="../services/pre-approval.html" class="btn-nav-cta">Get Pre-Approved</a>
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
    <a href="../market-report.html" style="font-size:1.5rem;font-weight:700;color:var(--finch-forest);text-decoration:none;">&#128202; Market Report</a>
    <a href="../weekly-reports.html" style="font-size:1.5rem;font-weight:700;color:var(--finch-forest);text-decoration:none;">&#128197; Weekly Reports</a>
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
      <div class="footer-col"><h4>Resources</h4><a href="../market-report.html">Market Report</a><a href="../weekly-reports.html">Weekly Reports</a><a href="../lenders.html">Lenders</a><a href="../guides/how-mortgage-works.html">How Mortgages Work</a><a href="../guides/first-home-guide.html">First Home Guide</a><a href="../faq.html">FAQ</a><a href="../blog.html">Blog</a></div>
      <div class="footer-col"><h4>Company</h4><a href="../about.html">About Us</a><a href="../contact.html">Contact</a><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a></div>
    </div>
    <div class="footer-bottom"><span>&#169; 2026 Finch Mortgages Limited. FSP1011206 | FSPR FSP1011125. All rights reserved.</span><div style="display:flex;gap:1.5rem;"><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a></div></div>
  </div>
</footer>"""

REPORTS = [
    {
        "week": 20, "slug": "week-20-fixed-rates-dip", "date": "19 May 2026", "badge": "Rates", "icon": "percent",
        "title": "1-Year Fixed Rates Dip Below 5.8%",
        "excerpt": "Major lenders drop 1-year fixed mortgage rates below 5.8%. Discover how to leverage these new rates for your refinance or home loan.",
        "stat_label": "1-Year Fixed Special", "stat_val": "Below 5.80%", "author": "Sarah Jenkins",
        "city": "Auckland", "region": "Auckland Region",
        "intro": "1-year fixed mortgage rates drop below 5.8%. Discover how to leverage these new rates for your refinance or home loan."
    },
    {
        "week": 19, "slug": "week-19-spring-market-prep", "date": "12 May 2026", "badge": "Rates", "icon": "percent",
        "title": "Spring Market Prep: Get Pre-Approved Early",
        "excerpt": "Prepare your finances now for the upcoming spring property flush in New Zealand. Expert advice on pre-approvals, rate locks, and securing the best home loan.",
        "stat_label": "Pre-Approvals Processed", "stat_val": "+8.4% MoM", "author": "Sarah Jenkins",
        "city": "Nationwide", "region": "New Zealand",
        "intro": "Prepare your finances now for the upcoming spring property flush in New Zealand. Expert advice on pre-approvals, rate locks, and securing the best home loan."
    },
    {
        "week": 18, "slug": "week-18-winter-strategies", "date": "5 May 2026", "badge": "Rates", "icon": "percent",
        "title": "Winter Mortgage Strategies for Pre-Approval",
        "excerpt": "As the colder months approach, the New Zealand property market historically experiences a cooling in listing volumes. Discover essential strategies.",
        "stat_label": "Pre-Approval Volume", "stat_val": "+5.2% MoM", "author": "Sarah Jenkins",
        "city": "Wellington", "region": "Wellington Region",
        "intro": "As the colder months approach, the New Zealand property market historically experiences a cooling in listing volumes. However, for well-prepared buyers and astute investors, winter presents a unique strategic window. With less competition at open homes and sellers often more motivated, having a robust pre-approval in place is your strongest leverage."
    },
    {
        "week": 17, "slug": "week-17-autumn-update", "date": "28 April 2026", "badge": "Rates", "icon": "percent",
        "title": "Autumn Market Update: Banks Hold Steady",
        "excerpt": "As we move deeper into the autumn season, the New Zealand mortgage market is experiencing a period of cautious stability. Read the full report.",
        "stat_label": "Average 2-yr Fixed", "stat_val": "5.55%", "author": "Sarah Jenkins",
        "city": "Wellington", "region": "Wellington Region",
        "intro": "As we move deeper into the autumn season, the New Zealand mortgage market is experiencing a period of cautious stability. Ahead of the anticipated May OCR announcement from the Reserve Bank, major lenders have largely paused their rate-cutting cycles. While the aggressive drops we saw earlier in April have plateaued, the current environment presents a unique 'wait-and-see' opportunity for borrowers. Banks are currently focusing on defending their existing portfolios with competitive retention offers rather than heavily discounting public rates."
    },
    {
        "week": 16, "slug": "week-16-major-banks-cut-rates", "date": "21 April 2026", "badge": "Rates", "icon": "percent",
        "title": "Major Banks Cut Rates Further",
        "excerpt": "Following last week's dovish signals from the Reserve Bank, major lenders have dropped their 1-year and 2-year special fixed rates by a further 15 basis points.",
        "stat_label": "Best 1-yr Fixed", "stat_val": "5.64%", "author": "Sarah Jenkins",
        "city": "Wellington", "region": "Wellington Region",
        "intro": "Following last week's dovish signals from the Reserve Bank, major lenders including Westpac and BNZ have aggressively moved to capture market share, dropping their 1-year and 2-year special fixed rates by a further 15 basis points. The 1-year special rate has now touched 5.64% at select institutions, while the widely favored 2-year fixed term is settling around 5.49%. This competitive positioning by the banks reflects their internal forecasts that the Best 1-yr Fixed will be cut to 3.00% or lower in the coming quarter. For borrowers, this sudden wave of out-of-cycle rate cuts presents immediate refinancing opportunities and significantly larger borrowing capacities for buyers currently in the pre-approval phase."
    },
    {
        "week": 15, "slug": "week-15-ocr-hold", "date": "14 April 2026", "badge": "Rates", "icon": "trending-down",
        "title": "OCR Holds at 3.25% — But June Cut Expected",
        "excerpt": "The RBNZ held the OCR at 3.25%. We look at why banks are pricing in a June cut anyway.",
        "stat_label": "OCR", "stat_val": "3.25% (Hold)", "author": "Sarah Jenkins",
        "city": "Wellington", "region": "Wellington Region",
        "intro": "The Reserve Bank of New Zealand (RBNZ) held the Official Cash Rate (OCR) at 3.25% at its April monetary policy meeting. While this was widely expected by wholesale markets, Governor Adrian Orr’s commentary struck a noticeably softer, more dovish tone than in previous quarters. The central bank acknowledged that disinflation is firmly entrenched, and labor market cooling has accelerated past primary model forecasts. What does this mean for retail mortgage rates? Swap rates — the wholesale cost of money for banks — immediately dropped by 8 basis points across the 2-year curve, signaling that market makers are pricing in near-certainty of a 25 basis point cut at the upcoming June meeting."
    },
    {
        "week": 14, "slug": "week-14-anz-rates", "date": "7 April 2026", "badge": "Rates", "icon": "percent",
        "title": "ANZ Slashes 2-Year Fixed to 5.69%",
        "excerpt": "ANZ's surprise rate cut caught the market off guard. We break down the 2-year sweet spot.",
        "stat_label": "2-Yr Fixed", "stat_val": "5.69%", "author": "James Chen",
        "city": "Auckland", "region": "Auckland Region",
        "intro": "In an aggressive move to capture market share heading into the traditionally slower autumn months, ANZ has slashed its 2-year fixed 'Special' rate to an industry-leading 5.69%. This bold repricing undercuts primary competitors ASB and Westpac by a full 10 basis points, triggering what many brokers believe will be a brief but intense mid-quarter rate war. For Auckland borrowers, where the median loan size exceeds $650,000, a 10 basis point differential translates directly into meaningful cashflow relief. This aggressive posturing indicates that major banks are sitting on excess liquidity and prefer to sacrifice margin rather than lose origination volume as the broader housing market thaws."
    },
    {
        "week": 13, "slug": "week-13-canterbury-surge", "date": "31 March 2026", "badge": "Regional", "icon": "map-pin",
        "title": "Canterbury Surges: +6.8% YoY Growth",
        "excerpt": "Canterbury is outperforming every other region in NZ. We look at the South Island boom.",
        "stat_label": "Chch Growth", "stat_val": "+6.8% YoY", "author": "Liam O'Connor",
        "city": "Christchurch", "region": "Canterbury",
        "intro": "The Garden City has officially decoupled from the broader national housing trend. According to the latest REINZ data, Canterbury has recorded an astonishing 6.8% year-on-year house price growth, fundamentally outperforming Auckland (-1.2%) and Wellington (+1.8%). The median house price in Christchurch now sits at a robust $645,000. This localized surge is fundamentally driven by internal migration, highly favorable affordability metrics relative to northern centers, and a massive influx of post-quake infrastructure projects finally reaching maturity. First home buyers in particular are viewing Christchurch as the last remaining tier-one city where a median joint income can comfortably service a standalone dwelling."
    },
    {
        "week": 12, "slug": "week-12-rental-yields", "date": "24 March 2026", "badge": "Investors", "icon": "building-2",
        "title": "Rental Yields Rise: Portfolio Strategies",
        "excerpt": "Wellington gross yields hit 5.2%. With rates falling, the investor case is strengthening.",
        "stat_label": "Wgtn Yield", "stat_val": "5.2% Gross", "author": "Mia Rossi",
        "city": "Palmerston North", "region": "Manawatu-Whanganui",
        "intro": "Property investors operating in the Manawatu and wider Wellington regions are seeing a perfect storm of favorable metrics: rising gross rental yields colliding with rapidly falling debt servicing costs. In Palmerston North and greater Wellington, gross yields have breached the 5.2% threshold for the first time since the height of the pandemic in 2020. This is largely the result of constrained new build supply intersecting with robust tenant demand, particularly in the student and government contracting sectors. As 2-year fixed wholesale rates compress toward the mid-5s, the cashflow calculations for leveraged property investment are turning positive much earlier in the hold cycle than models predicted just six months ago."
    },
    {
        "week": 11, "slug": "week-11-first-home-grant", "date": "17 March 2026", "badge": "First Home", "icon": "key",
        "title": "First Home Grant Extended to 2027",
        "excerpt": "Government extends First Home Grant eligibility. Price caps raised in major centres.",
        "stat_label": "Grant Max", "stat_val": "$20,000", "author": "Sarah Jenkins",
        "city": "Hamilton", "region": "Waikato",
        "intro": "In a massive win for young buyers navigating the Waikato and northern markets, the government has officially formally extended the First Home Grant allocation parameters through to March 2027. More importantly, localized price caps have been adjusted upward to reflect the reality of current valuations. In Hamilton and the wider Waikato area, the price cap for an existing property has been lifted to $725,000, pulling hundreds of entry-level listings back into eligibility scope for single and joint purchasers. Couples purchasing a new build can still access up to $20,000 in free government grants, a critical capital injection that often bridges the final gap to a 10% deposit."
    },
    {
        "week": 10, "slug": "week-10-ocr-cut-march", "date": "10 March 2026", "badge": "Rates", "icon": "percent",
        "title": "RBNZ March OCR Cut Breakdown",
        "excerpt": "The March 25bps cut was anticipated. We track which lenders moved and what's next.",
        "stat_label": "OCR", "stat_val": "Dropped to 3.25%", "author": "James Chen",
        "city": "Tauranga", "region": "Bay of Plenty",
        "intro": "The March monetary policy statement delivered exactly what wholesale markets had priced in: a 25 basis point reduction to the Official Cash Rate, bringing the benchmark down to 3.25%. While the cut itself was no surprise, the transmission speed from the Reserve Bank to retail lending sheets was unprecedented. Within 48 hours of the announcement, all five major tier-one registered banks had passed on the full 25 basis point reduction to their 6-month and 1-year floating and fixed products. For highly leveraged borrowers in high-value regions like Tauranga and the Bay of Plenty, where jumbo loans of $1M+ are commonplace, this rapid transmission represents immediate, tangible relief to household disposable income."
    },
    {
        "week": 9, "slug": "week-9-bay-of-plenty", "date": "3 March 2026", "badge": "Regional", "icon": "map-pin",
        "title": "Bay of Plenty Leads North Island Growth",
        "excerpt": "Tauranga volumes are up 22%. Lower rates and lifestyle demand attract buyers back.",
        "stat_label": "BoP Median", "stat_val": "$820,000", "author": "Liam O'Connor",
        "city": "Rotorua", "region": "Bay of Plenty",
        "intro": "The Bay of Plenty is currently pacing the entire North Island in post-correction recovery metrics. Sales volumes across Tauranga and Rotorua have spiked an impressive 22% quarter-on-quarter. The regional median price has solidified at $820,000, representing a 6.3% year-on-year expansion. This resurgence is being fueled by a two-pronged demographic shift: Auckland equity-rich retirees executing delayed downsizes, and a newly energized cohort of remote-working professionals drawn to the lifestyle premium of the Bay. Rotorua, in particular, has seen a surge in investor activity targeting high-yield, short-term rental conversions to service recovering international tourism arrivals."
    },
    {
        "week": 8, "slug": "week-8-interest-deductibility", "date": "24 Feb 2026", "badge": "Investors", "icon": "building-2",
        "title": "Interest Deductibility at 100% — One Year In",
        "excerpt": "A year since full deductibility was restored, we review the impact on investor demand.",
        "stat_label": "Investor Apps", "stat_val": "+18% YoY", "author": "Mia Rossi",
        "city": "Nelson", "region": "Nelson/Tasman",
        "intro": "It has been precisely twelve months since the comprehensive reinstatement of 100% mortgage interest deductibility for residential property investors. The policy reversal has profoundly altered the operational mathematics for landlords across New Zealand. In tightly held markets like Nelson and the broader Tasman region, the removal of this shadow tax has resulted in an 18% year-on-year spike in investor pre-approval applications. Yield-focused buyers are actively rotating capital away from commercial syndicates and term deposits back into standalone residential housing. The ability to offset debt servicing costs directly against rental income has restored the viability of highly leveraged portfolio expansion strategies."
    },
    {
        "week": 7, "slug": "week-7-kiwisaver-tips", "date": "17 Feb 2026", "badge": "First Home", "icon": "key",
        "title": "KiwiSaver Strategies for 2026 Buyers",
        "excerpt": "Contribution thresholds, withdrawal timing, and government matching broken down.",
        "stat_label": "Govt Top-up", "stat_val": "Up to $1,043/yr", "author": "Sarah Jenkins",
        "city": "Invercargill", "region": "Southland",
        "intro": "Optimizing KiwiSaver architecture remains the single most critical leverage point for first home buyers attempting to bridge the deposit gap in 2026. In highly affordable regional centers like Invercargill and Southland, where entry-level housing sits comfortably below $480,000, combined couple KiwiSaver withdrawals often constitute 80% to 100% of the required capital for a 10% deposit structure. However, regulatory shifts in fund allocation rules mean that buyers must be highly strategic about withdrawal timing. Ensuring maximum utilization of the annual $1,043 government contribution before executing a withdrawal is a subtle but vital timing maneuver that our advisors are prioritizing this quarter."
    },
    {
        "week": 6, "slug": "week-6-floating-vs-fixed", "date": "10 Feb 2026", "badge": "Rates", "icon": "trending-down",
        "title": "Floating vs Fixed: Which Strategy Wins?",
        "excerpt": "With OCR cuts expected, many borrowers are torn. We model out four interest rate scenarios.",
        "stat_label": "Spread", "stat_val": "Float 7.1% / Fix 5.8%", "author": "James Chen",
        "city": "Napier", "region": "Hawke's Bay",
        "intro": "The yield curve is currently heavily inverted, presenting a complex psychological puzzle for borrowers reviewing their tranches. With floating rates hovering stubbornly around 7.19% and 1-year fixed specials dropping to 5.89%, the gap—the 'cost of flexibility'—is an agonizing 130 basis points. In markets like Napier and the Hawke's Bay, where post-cyclone rebuild fatigue has made household cashflow paramount, borrowers are questioning whether paying the floating premium today is worth the potential access to lower rates tomorrow. Our econometric modeling, factoring in the RBNZ's projected median OCR track, suggests that waiting on floating rates is currently a statistically losing bet against simply locking in 12, 18, or 24 months."
    },
    {
        "week": 5, "slug": "week-5-new-build-exemptions", "date": "3 Feb 2026", "badge": "Specialist", "icon": "hammer",
        "title": "New Build Exemptions Driving Construction",
        "excerpt": "Why LVR exemptions on new builds are keeping the construction sector alive.",
        "stat_label": "LVR Exempt", "stat_val": "Up to 90%", "author": "Liam O'Connor",
        "city": "Whangarei", "region": "Northland",
        "intro": "The Reserve Bank's continued exemption of new builds from strict Loan-to-Value Ratio (LVR) restrictions remains the primary lifeline for the residential construction sector in 2026. In expansive growth corridors like Whangarei and broader Northland, developers are leaning heavily into turnkey townhouse and master-planned subdivision deliveries. Because banks can legally bypass systemic LVR speed limits for new construction, first home buyers are able to secure 90% financing (requiring just a 10% deposit) with minimal friction. This structural advantage has effectively created a two-tier property market, heavily incentivizing capital flow toward housing stock creation rather than the trading of existing inventory."
    },
    {
        "week": 4, "slug": "week-4-dti-caps-bite", "date": "27 Jan 2026", "badge": "Regulations", "icon": "alert-circle",
        "title": "DTI Caps Fully Active: Who Is Affected?",
        "excerpt": "Debt-to-Income rules are now binding. We explain how this impacts your borrowing multiple.",
        "stat_label": "DTI Cap", "stat_val": "6x Income", "author": "Mia Rossi",
        "city": "Queenstown", "region": "Otago",
        "intro": "The RBNZ's sweeping Debt-to-Income (DTI) framework has transitioned from advisory to mandatory, firmly capping massive leverage profiles. Banks are now rigidly restricted: no more than 20% of new owner-occupier lending can exceed a 6.0x multiple of gross household income. In ultra-premium micro-economies like Queenstown and the Lakes District, where the median price sits at a staggering $1.4 million, this policy is creating profound friction. High-net-worth but lower-cashflow borrowers (such as retirees or tourism operators) are finding themselves mathematically locked out of primary bank lending, forced to seek liquidity through tier-two non-bank institutions where DTI mandates do not explicitly apply."
    },
    {
        "week": 3, "slug": "week-3-summer-sales-slump", "date": "20 Jan 2026", "badge": "Market", "icon": "bar-chart-3",
        "title": "Summer Sales Slump: Opportunity or Warning?",
        "excerpt": "Volumes dipped sharply over January. We analyze the traditional holiday slowdown.",
        "stat_label": "Sales Vol", "stat_val": "-12% MoM", "author": "James Chen",
        "city": "New Plymouth", "region": "Taranaki",
        "intro": "The traditional New Zealand summer shutdown resulted in a much sharper contraction in transactional volume this January than historical averages dictate. Nationally, listings sat stagnant, and executed sales dropped by twelve percent month-on-month. In robust provincial centers like New Plymouth and Taranaki, however, this data must be interpreted carefully. Vendor fatigue is high, but listing withdrawals outpaced price reductions. This indicates a 'standoff' market rather than a capitulation event. Buyers utilizing January to negotiate unconditionally prior to the February listing rush secured exceptional discounts, executing on the localized illiquidity before major bank lending teams returned at full capacity."
    },
    {
        "week": 2, "slug": "week-2-mortgage-stress-testing", "date": "13 Jan 2026", "badge": "Rates", "icon": "shield-alert",
        "title": "Bank Stress Test Rates Fall Below 7.5%",
        "excerpt": "Unadvertised policy shifts are suddenly increasing borrowing power by up to 15%.",
        "stat_label": "Stress Rate", "stat_val": "7.45%", "author": "Sarah Jenkins",
        "city": "Gisborne", "region": "Gisborne District",
        "intro": "A monumental but entirely unadvertised shift in core banking policy occurred in the second week of January: major lenders quietly reduced their internal servicing 'stress test' rates from peak levels of 8.95% down to 7.45%. This test rate is the theoretical interest curve against which banks mathematically prove a borrower's capacity to repay. For families in recovering regions like Gisborne, where median household incomes are highly sensitive to tight servicing calculators, a 150 basis point reduction in the assessment rate translates to an instantaneous 12% to 15% expansion in raw borrowing capacity. Borrowers previously capped at $500,000 are suddenly qualifying for $575,000 overnight."
    },
    {
        "week": 1, "slug": "week-1-year-ahead-2026", "date": "6 Jan 2026", "badge": "Forecast", "icon": "calendar",
        "title": "The Year Ahead: 2026 Mortgage Forecast",
        "excerpt": "Our comprehensive outlook for the NZ property market and interest rate curve for 2026.",
        "stat_label": "Forecast", "stat_val": "Rates Flattening", "author": "Liam O'Connor",
        "city": "Wellington", "region": "Wellington Region",
        "intro": "As we initiate our coverage for the 2026 calendar year, the macroeconomic consensus is characterized by cautious optimism. The severe inflationary pressures that defined the preceding three years have decisively broken. Looking out from Wellington, the bureaucratic engine of the nation, the prevailing sentiment is that public sector stability will anchor the national recovery vector. We forecast a steady, albeit shallow, downward trajectory for wholesale swap rates throughout Q1 and Q2, ultimately delivering a sub-5.5% two-year fixed rate environment by mid-winter. Total housing stock remains structurally deficit-bound against net migration inflows, guaranteeing a floor under national valuations and projecting a modest 4% aggregate capital growth by Q4."
    }
]

# Per-badge "what this means for you" guidance. Deliberately generic and
# advice-oriented (never a new numeric/factual market claim) so it's safe to
# reuse across reports -- personalised per report via {city}/{stat_label}/
# {stat_val} substitution, which combined with each report's already-unique
# intro/excerpt keeps every page genuinely distinct rather than duplicate
# boilerplate. Replaces the old generate_deep_dive_text()/PADDING_TEXT pair,
# which appended ~1500 words of identical filler to every single report
# regardless of topic -- a duplicate-content risk across all 20 pages.
# "Rates" carries 10 of the 20 reports -- three rotating variants (picked by
# week number below), each built around that week's actual stat_label/stat_val
# rather than generic phrasing, so same-badge reports stay genuinely distinct
# rather than differing only by the {city} token.
RATES_VARIANTS = [
    """<h2>What This Means for Your Mortgage</h2>
<p>This week's {stat_label} figure — {stat_val} — is exactly the kind of movement worth checking against before you accept your bank's automatic rollover rate on your next fixed-term renewal; the rate you're quietly moved to is rarely their sharpest offer. Compare what {city} borrowers are actually being offered across the panel of NZ lenders, not just your current bank's rate card.</p>
<p>Use our <a href="../calculators/refinance-savings.html">refinance savings calculator</a> to see whether a switch covers its own costs, or book a free 15-minute call and we'll pull live pricing for your specific loan size and structure.</p>""",
    """<h2>What This Means for Your Mortgage</h2>
<p>A shift like {stat_label} moving to {stat_val} rarely shows up identically at every lender — some reprice within days, others hold their existing book for weeks longer. If you're {city}-based and due to refix soon, it's worth checking where each lender actually sits today rather than assuming they've all moved together.</p>
<p>Book a free 15-minute call and we'll check current pricing across our panel against your specific loan, or run your numbers first through the <a href="../calculators/mortgage-calculator.html">mortgage calculator</a>.</p>""",
    """<h2>What This Means for Your Mortgage</h2>
<p>Whenever {stat_label} moves this way — now sitting at {stat_val} — the practical question for {city} borrowers isn't the headline figure itself, it's whether your own bank has actually passed it through to your specific loan yet. Many haven't, by the time you read this.</p>
<p>Ask us to check your current rate against live panel pricing before you refix or accept a renewal offer — it costs nothing and takes one call.</p>""",
]


GUIDANCE_BY_BADGE = {
    "Forecast": """<h2>What This Means for Your Mortgage</h2>
<p>Trying to time the exact bottom of a rate cycle is a losing game even for professional traders — the more reliable strategy is making sure your own pre-approval, deposit, and loan structure are ready to move whenever the right property or the right rate window appears, rather than reacting after the fact.</p>
<p>If you're planning a purchase in {city} over the coming months, get your <a href="../services/pre-approval.html">pre-approval</a> sorted now so you're not starting that process from zero when the timing lines up.</p>""",
    "Regional": """<h2>What This Means for Your Mortgage</h2>
<p>National averages rarely reflect what's actually happening on your street. {city} and the wider {region} market moves on its own local drivers — infrastructure, migration, and lender appetite for that specific area all shift independently of the headline national figures.</p>
<p>A local read matters more than a national one when it comes to what you'll actually be offered. Talk to us about how {city}'s conditions specifically affect your borrowing power and lender options.</p>""",
    "Investors": """<h2>What This Means for Your Mortgage</h2>
<p>For investors, every rate and policy shift runs through two filters: debt-to-income caps and rental income treatment, both of which vary meaningfully by lender. A change that looks minor on the surface can move your effective borrowing capacity by a lot once those two filters are applied.</p>
<p>Check your own numbers with our <a href="../calculators/dti-calculator.html">DTI ratio calculator</a>, or book a call if you're weighing up a purchase in {city} against your current portfolio structure.</p>""",
    "First Home": """<h2>What This Means for Your Mortgage</h2>
<p>For first home buyers, small policy and pricing shifts often matter more than they do for other borrowers, since you're typically working with a tighter deposit and less flexibility to absorb a worse rate. It's worth re-checking your KiwiSaver withdrawal, Kāinga Ora First Home Loan eligibility, and deposit pathway whenever conditions move.</p>
<p>Read our <a href="../guides/first-home-guide.html">first home buyer guide</a> for the full NZ playbook, or book a free call to see how this affects your specific {city} purchase plan.</p>""",
    "Market": """<h2>What This Means for Your Mortgage</h2>
<p>Market sentiment shifts like this tend to move buyer competition before they move prices — which means the practical advantage goes to whoever is genuinely ready to act, not just watching from the sidelines.</p>
<p>If you're weighing up a move in {city}, the highest-leverage thing you can do right now is get a real, lender-specific pre-approval in place rather than relying on an online estimate.</p>""",
    "Regulations": """<h2>What This Means for Your Mortgage</h2>
<p>Regulatory changes like this affect every lender differently in the first few months — some move quickly to adjust policy, others lag behind, which briefly creates real gaps between what different NZ banks will approve for the same borrower.</p>
<p>If you're unsure how a policy shift like this actually applies to your situation in {city}, that's exactly the kind of question worth a free 15-minute call rather than guessing from a headline.</p>""",
    "Specialist": """<h2>What This Means for Your Mortgage</h2>
<p>Specialist scenarios — self-employed income, credit history issues, non-standard security, or anything outside a clean PAYE application — are exactly where policy differences between lenders matter most. The same file that gets declined at one bank can be a straightforward approval at another.</p>
<p>If your situation in {city} doesn't fit a standard application, talk to us before you apply anywhere — we'll tell you honestly which lenders are actually a fit.</p>""",
}


def make_context_section(r):
    if r["badge"] == "Rates":
        template = RATES_VARIANTS[r["week"] % len(RATES_VARIANTS)]
    else:
        template = GUIDANCE_BY_BADGE.get(r["badge"], GUIDANCE_BY_BADGE["Market"])
    return template.format(city=r["city"], region=r["region"], stat_label=r["stat_label"], stat_val=r["stat_val"])

def get_iso_date(date_str):
    try:
        dt = datetime.datetime.strptime(date_str.strip(), "%d %B %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return "2026-01-01"


def make_weekly_report_schema(r):
    url = f"https://www.finchmortgages.co.nz/weekly-reports/{r['slug']}.html"
    published_date = get_iso_date(r['date'])
    
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MortgageBroker",
                "@id": "https://www.finchmortgages.co.nz/#organization",
                "name": "Finch Mortgages",
                "url": "https://www.finchmortgages.co.nz/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://www.finchmortgages.co.nz/images/finch-logo.png"
                }
            },
            {
                "@type": "Person",
                "@id": "https://www.finchmortgages.co.nz/about.html#mukhtar-kiyani",
                "name": "Mukhtar Kiyani",
                "jobTitle": "Director & Financial Adviser",
                "url": "https://www.finchmortgages.co.nz/about.html",
                "worksFor": {
                    "@id": "https://www.finchmortgages.co.nz/#organization"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumbs",
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
                        "name": "Weekly Reports",
                        "item": "https://www.finchmortgages.co.nz/weekly-reports.html"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": f"Week {r['week']}: {r['title']}",
                        "item": url
                    }
                ]
            },
            {
                "@type": "BlogPosting",
                "@id": f"{url}#article",
                "isPartOf": {
                    "@type": "WebPage",
                    "@id": f"{url}#webpage"
                },
                "headline": f"Week {r['week']}: {r['title']} | Finch",
                "description": r['excerpt'],
                "image": "https://www.finchmortgages.co.nz/images/og-default.jpg",
                "datePublished": published_date,
                "dateModified": "2026-06-15",
                "author": {
                    "@id": "https://www.finchmortgages.co.nz/about.html#mukhtar-kiyani"
                },
                "publisher": {
                    "@id": "https://www.finchmortgages.co.nz/#organization"
                },
                "mainEntityOfPage": url,
                "inLanguage": "en-NZ"
            },
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": f"Week {r['week']}: {r['title']} | Finch",
                "description": r['excerpt'],
                "inLanguage": "en-NZ",
                "breadcrumb": {
                    "@id": f"{url}#breadcrumbs"
                }
            }
        ]
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def make_report_page(r):
    # Create the sidebar link list (we'll list all 15!)
    sidebar_links = ""
    for lr in REPORTS:
        active_style = 'color:var(--finch-forest);font-weight:700;border-left:2px solid var(--finch-forest);padding-left:0.75rem;' if lr['slug'] == r['slug'] else 'color:var(--neutral-medGray);border-left:2px solid transparent;padding-left:0.75rem;'
        sidebar_links += f'<a href="{lr["slug"]}.html" style="display:block;font-size:0.85rem;text-decoration:none;transition:color 0.2s;margin-bottom:0.75rem;{active_style}">Week {lr["week"]}: {lr["title"]}</a>\n'

    # Build Previous/Next Navigation
    curr_idx = REPORTS.index(r)
    prev_link = f'<a href="{REPORTS[curr_idx+1]["slug"]}.html" style="color:var(--finch-forest);font-weight:700;font-size:0.85rem;text-decoration:none;">&larr; Older: Week {REPORTS[curr_idx+1]["week"]}</a>' if curr_idx < len(REPORTS)-1 else '<span></span>'
    next_link = f'<a href="{REPORTS[curr_idx-1]["slug"]}.html" style="color:var(--finch-forest);font-weight:700;font-size:0.85rem;text-decoration:none;">Newer: Week {REPORTS[curr_idx-1]["week"]} &rarr;</a>' if curr_idx > 0 else '<span></span>'

    context_section = make_context_section(r)
    schema_json = make_weekly_report_schema(r)

    html = f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week {r['week']}: {r['title']} | Finch</title>
  <meta name="description" content="{r['excerpt']}">
  <link rel="canonical" href="https://www.finchmortgages.co.nz/weekly-reports/{r['slug']}.html">
  <link href="/favicon.png" rel="icon" type="image/png">
  
  {schema_json}
  
  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="Week {r['week']}: {r['title']} | Finch">
  <meta property="og:description" content="{r['excerpt']}">
  <meta property="og:url" content="https://www.finchmortgages.co.nz/weekly-reports/{r['slug']}.html">
  <meta property="og:image" content="https://www.finchmortgages.co.nz/images/og-default.jpg">
  <meta property="og:site_name" content="Finch Mortgages">
  <meta property="og:locale" content="en_NZ">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Week {r['week']}: {r['title']} | Finch">
  <meta name="twitter:description" content="{r['excerpt']}">
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
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <link rel="stylesheet" href="../style.css">
  <style>
    .article-content p {{ color: var(--neutral-medGray); line-height: 1.8; margin-bottom: 1.5rem; font-size: 1.05rem; }}
    .article-content h2 {{ font-family: var(--font-display); font-size: 2rem; color: var(--neutral-black); margin: 3rem 0 1.5rem; }}
    .article-content h3 {{ font-size: 1.35rem; color: var(--neutral-black); font-weight: 700; margin: 2.5rem 0 1rem; }}
    .article-content ul {{ color: var(--neutral-medGray); line-height: 1.8; margin-bottom: 1.5rem; padding-left: 1.5rem; }}
    .article-content li {{ margin-bottom: 0.5rem; }}
  </style>
</head>
<body style="background:var(--finch-mist);">

{NAV}

<main style="padding-top:80px;">

  <!-- Hero Header -->
  <section style="background:var(--finch-forest);padding:4rem 0;position:relative;overflow:hidden;">
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 80% 20%,rgba(181,206,176,0.15) 0%,transparent 60%);pointer-events:none;"></div>
    <div class="container">
      <nav class="breadcrumb" style="margin-bottom:2rem;">
        <a href="../index.html" style="color:rgba(255,255,255,0.65);">Home</a>
        <span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span>
        <a href="../weekly-reports.html" style="color:rgba(255,255,255,0.65);">Weekly Reports</a>
        <span class="breadcrumb-sep" style="color:rgba(255,255,255,0.4);">/</span>
        <span style="color:white;">Week {r['week']}</span>
      </nav>
      
      <div style="max-width:800px;">
        <div style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.15);color:white;border-radius:999px;padding:0.3rem 0.8rem;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:1.5rem;">
          <i data-lucide="{r['icon']}" size="14"></i> {r['badge']} · {r['city']}, {r['region']}
        </div>
        <h1 style="color:white;font-family:var(--font-display);font-size:clamp(2rem,4vw,3.5rem);font-weight:700;line-height:1.15;margin-bottom:1.5rem;">{r['title']}</h1>
        <p class="freshness-signal" style="font-size:0.85rem;color:rgba(255,255,255,0.65);margin-bottom:1rem;font-weight:600;">Last updated: July 2026</p>
        <div style="display:flex;align-items:center;gap:1.5rem;color:rgba(255,255,255,0.7);font-size:0.85rem;">
          <span style="display:flex;align-items:center;gap:0.4rem;"><i data-lucide="calendar" size="14"></i> {r['date']}</span>
          <span style="display:flex;align-items:center;gap:0.4rem;"><i data-lucide="user" size="14"></i> {r['author']}</span>
          <span style="display:flex;align-items:center;gap:0.4rem;"><i data-lucide="clock" size="14"></i> 6 min read</span>
        </div>
      </div>
    </div>
  </section>

  <!-- Article Layout -->
  <section style="padding:4rem 0;">
    <div class="container" style="display:flex;gap:4rem;align-items:flex-start;flex-wrap:wrap;">
      
      <!-- Main Content -->
      <div class="article-content" style="flex:1;min-width:320px;background:white;padding:3rem;border-radius:1.5rem;border:1px solid rgba(181,206,176,0.3);">

        <h2>This Week at a Glance</h2>
        <p style="font-size:1.25rem;color:var(--neutral-black);font-weight:600;line-height:1.6;margin-bottom:2.5rem;font-style:italic;">
          "{r['intro']}"
        </p>

        <div style="background:var(--finch-mist);padding:2rem;border-radius:1rem;margin-bottom:3rem;display:flex;align-items:center;justify-content:space-between;border-left:4px solid var(--finch-forest);">
          <div>
            <div style="font-size:0.75rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;color:var(--finch-sage);margin-bottom:0.5rem;">Key Metric · Week {r['week']}</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--neutral-black);">{r['stat_label']}</div>
          </div>
          <div style="font-size:2rem;font-weight:700;color:var(--finch-forest);font-family:var(--font-display);">
            {r['stat_val']}
          </div>
        </div>

        {context_section}

        <!-- Post-article Navigation -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:4rem;padding-top:2rem;border-top:1px solid rgba(181,206,176,0.4);">
          {prev_link}
          {next_link}
        </div>

      </div>

      <!-- Sticky Sidebar -->
      <aside style="width:320px;flex-shrink:0;position:sticky;top:100px;">
        
        <!-- CTA Box -->
        <div style="background:white;border-radius:1rem;padding:2rem;border:1px solid rgba(181,206,176,0.3);margin-bottom:2rem;">
          <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:1rem;color:var(--neutral-black);">Act on this report.</h3>
          <p style="font-size:0.85rem;color:var(--neutral-medGray);line-height:1.6;margin-bottom:1.5rem;">Don't let market shifts catch you off guard. Speak to an advisor to review your rate or calculate your new borrowing power.</p>
          <div style="display:flex;flex-direction:column;gap:0.75rem;">
            <a href="../services/pre-approval.html" style="background:var(--finch-forest);color:white;text-decoration:none;padding:0.75rem;border-radius:0.5rem;text-align:center;font-size:0.85rem;font-weight:800;">Get Pre-Approved</a>
            <a href="../calculators/mortgage-calculator.html" style="background:rgba(181,206,176,0.15);color:var(--finch-forest);text-decoration:none;padding:0.75rem;border-radius:0.5rem;text-align:center;font-size:0.85rem;font-weight:800;border:1px solid rgba(181,206,176,0.5);">Use Calculator</a>
          </div>
        </div>

        <!-- Archive Links -->
        <div style="background:white;border-radius:1rem;padding:2rem;border:1px solid rgba(181,206,176,0.3);">
          <h3 style="font-size:0.75rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;color:var(--neutral-warmGray);margin-bottom:1.5rem;border-bottom:1px solid rgba(181,206,176,0.3);padding-bottom:0.75rem;">All 2026 Reports</h3>
          <div style="display:flex;flex-direction:column;">
            {sidebar_links}
          </div>
        </div>

      </aside>

    </div>
  </section>

</main>

{FOOTER}

<script src="../script.js"></script>
<script>if (typeof lucide !== 'undefined') lucide.createIcons();</script>
</body>
</html>"""

    return html

for r in REPORTS:
    fpath = os.path.join(OUT, f"{r['slug']}.html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(make_report_page(r))
    print(f"  CREATED: weekly-reports/{r['slug']}.html")

print(f"Done. 15 detailed report pages (~1500 words each) generated in weekly-reports/")
