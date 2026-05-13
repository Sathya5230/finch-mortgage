import os
import re

with open("weekly-reports.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update the top date
html = html.replace('Week of 28 April 2026', 'Week of 5 May 2026')

# 2. Update the featured card left side
old_featured = """<div>
<div class="report-badge badge-latest" style="margin-bottom:1.25rem;">🟢 Latest · Week 17, 2026</div>
<h2 style="color:white;font-size:1.6rem;font-weight:700;line-height:1.3;margin-bottom:1rem;"><a href="weekly-reports/week-17-autumn-update.html" style="color:inherit;text-decoration:none;">Autumn Market Update: Banks Hold Steady</a></h2>
<p style="color:rgba(255,255,255,0.8);line-height:1.75;margin-bottom:1.5rem;">As we move deeper into the autumn season, the New Zealand mortgage market is experiencing a period of cautious stability. Ahead of the anticipated May OCR announcement from the Reserve Bank, major lenders have largely paused their rate-cutting cycles.</p>
<p style="color:rgba(255,255,255,0.75);line-height:1.75;margin-bottom:2rem;">While the aggressive drops we saw earlier in April have plateaued, the current environment presents a unique 'wait-and-see' opportunity for borrowers. Banks are currently focusing on defending their existing portfolios with competitive retention offers rather than heavily discounting public rates.</p>
<div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
<a href="weekly-reports/week-17-autumn-update.html" style="display:inline-flex;align-items:center;gap:0.4rem;background:white;color:var(--finch-forest);padding:0.55rem 1.1rem;border-radius:0.5rem;font-size:0.8rem;font-weight:800;text-decoration:none;">Read full report →</a>
<a href="contact.html" style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);color:white;border:1px solid rgba(255,255,255,0.3);padding:0.55rem 1.1rem;border-radius:0.5rem;font-size:0.8rem;font-weight:700;text-decoration:none;">Get pre-approved</a>
</div>
</div>"""

new_featured = """<div>
<div class="report-badge badge-latest" style="margin-bottom:1.25rem;">🟢 Latest · Week 18, 2026</div>
<h2 style="color:white;font-size:1.6rem;font-weight:700;line-height:1.3;margin-bottom:1rem;"><a href="weekly-reports/week-18-winter-strategies.html" style="color:inherit;text-decoration:none;">Winter Mortgage Strategies: Positioning for Pre-Approvals</a></h2>
<p style="color:rgba(255,255,255,0.8);line-height:1.75;margin-bottom:1.5rem;">As the colder months approach, the New Zealand property market historically experiences a cooling in listing volumes. However, for well-prepared buyers and astute investors, winter presents a unique strategic window.</p>
<p style="color:rgba(255,255,255,0.75);line-height:1.75;margin-bottom:2rem;">With less competition at open homes and sellers often more motivated, having a robust pre-approval in place is your strongest leverage. Secure a rate lock and be ready to act when the right property appears.</p>
<div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
<a href="weekly-reports/week-18-winter-strategies.html" style="display:inline-flex;align-items:center;gap:0.4rem;background:white;color:var(--finch-forest);padding:0.55rem 1.1rem;border-radius:0.5rem;font-size:0.8rem;font-weight:800;text-decoration:none;">Read full report →</a>
<a href="contact.html" style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);color:white;border:1px solid rgba(255,255,255,0.3);padding:0.55rem 1.1rem;border-radius:0.5rem;font-size:0.8rem;font-weight:700;text-decoration:none;">Get pre-approved</a>
</div>
</div>"""

html = html.replace(old_featured, new_featured)

# 3. Update Key Numbers
html = html.replace('<strong style="color:white;">3.25% (hold)</strong>', '<strong style="color:white;">+5.2% MoM</strong>')
html = html.replace('<span style="color:rgba(255,255,255,0.7);">OCR</span>', '<span style="color:rgba(255,255,255,0.7);">Pre-Approvals</span>')

html = html.replace('<span style="color:rgba(255,255,255,0.7);">Market Activity</span><strong style="color:var(--finch-sage);">Cautious</strong>', '<span style="color:rgba(255,255,255,0.7);">Market Activity</span><strong style="color:var(--finch-sage);">Cooling</strong>')
html = html.replace('<span style="color:rgba(255,255,255,0.7);">NZ Inflation (CPI)</span><strong style="color:white;">2.3% YoY</strong>', '<span style="color:rgba(255,255,255,0.7);">Winter Refinances</span><strong style="color:white;">Up</strong>')


# 4. Insert Week 17 into the grid
week_17_card = """<a aria-label="Link icon" class="report-card" data-category="rates" href="weekly-reports/week-17-autumn-update.html">
<div class="report-badge badge-rates"><svg fill="none" height="11" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" style="display:inline-block;vertical-align:middle;flex-shrink:0;" viewbox="0 0 24 24" width="11"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg> Rates</div>
<div class="report-week">Week 17 · 28 April 2026</div>
<div class="report-title">Autumn Market Update: Banks Hold Steady</div>
<div class="report-excerpt">As we move deeper into the autumn season, the New Zealand mortgage market is experiencing a period of cautious stability.</div>
<div class="report-meta"><span><svg fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" style="display:inline-block;vertical-align:middle;flex-shrink:0;" viewbox="0 0 24 24" width="12"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg> 6 min read</span><strong>2-Yr Fixed: 5.55%</strong></div>
</a>
"""

html = html.replace('<div id="reports-grid" class="grid grid-cols-1 md-grid-cols-2 lg-grid-cols-3 gap-6">\n', '<div id="reports-grid" class="grid grid-cols-1 md-grid-cols-2 lg-grid-cols-3 gap-6">\n' + week_17_card)

with open("weekly-reports.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated weekly-reports.html")
