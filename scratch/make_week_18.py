import os
import re

with open("weekly-reports/week-17-autumn-update.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace meta tags and title
html = html.replace("Week 17: Autumn Market Update", "Week 18: Winter Mortgage Strategies")
html = html.replace("Banks pause rate cuts ahead of May OCR announcement.", "Discover essential strategies for navigating the New Zealand mortgage market this winter. Learn how to secure the best rates.")
html = html.replace("week-17-autumn-update.html", "week-18-winter-strategies.html")
html = html.replace("autumn 2026", "winter 2026").replace("April 2026", "May 2026")

# Replace header details
html = html.replace("Week 17", "Week 18")
html = html.replace("Autumn Market Update: Banks Hold Steady", "Winter Mortgage Strategies: Positioning for Pre-Approvals")
html = html.replace("28 April 2026", "5 May 2026")

# Replace article content
new_article = """<p style="font-size:1.25rem;color:var(--neutral-black);font-weight:600;line-height:1.6;margin-bottom:2.5rem;font-style:italic;">
          "As the colder months approach, the New Zealand property market historically experiences a cooling in listing volumes. However, for well-prepared buyers and astute investors, winter presents a unique strategic window. With less competition at open homes and sellers often more motivated, having a robust pre-approval in place is your strongest leverage."
        </p>
<div style="background:var(--finch-mist);padding:2rem;border-radius:1rem;margin-bottom:3rem;display:flex;align-items:center;justify-content:space-between;border-left:4px solid var(--finch-forest);">
<div>
<div style="font-size:0.75rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;color:var(--finch-sage);margin-bottom:0.5rem;">Key Metric · Week 18</div>
<div style="font-size:1.1rem;font-weight:700;color:var(--neutral-black);">Pre-Approval Volume</div>
</div>
<div style="font-size:2rem;font-weight:700;color:var(--finch-forest);font-family:var(--font-display);">
            +5.2% MoM
          </div>
</div>
<h3>The Winter Strategic Window</h3>
<p>Historically, May signals the beginning of the winter slowdown in the New Zealand housing market. New listing volumes typically contract as vendors prefer to wait for the 'spring flush' to showcase their properties. While inventory might be lower, the quality of opportunity for buyers often increases. Sellers who list or remain on the market during winter are typically highly motivated, whether due to changing family circumstances, relocation, or financial necessity. This creates an environment where 'cheeky' offers are more likely to be entertained, provided they are backed by solid financing.</p>
<h3>Pre-Approval is Your Winter Superpower</h3>
<p>In a market with fewer buyers actively attending open homes, the ability to move quickly and unconditionally is paramount. We have observed a 5.2% month-on-month increase in pre-approval applications across our network. This indicates that savvy buyers are getting their ducks in a row. A full, underwritten pre-approval allows you to negotiate with confidence, potentially knocking thousands off the asking price by offering the vendor absolute certainty of sale.</p>
<h3>Rate Lock Strategies</h3>
<p>While the broader expectation is that the RBNZ will cut the OCR in the coming months, waiting on the sidelines for rates to drop can be a costly mistake if the right property appears. Many lenders offer rate lock facilities for up to 60 days on pre-approvals. This means if rates go up, you are protected; if they go down, you can usually secure the lower rate before settlement. We are actively advising clients to secure their pre-approvals now and utilize these rate lock features to hedge against any unexpected wholesale market volatility.</p>
<h3>Refinancing Before the Winter Heating Bills Hit</h3>
<p>For existing homeowners, May is the optimal time to review your mortgage structure before the heightened utility costs of winter set in. If you have equity in your home and are looking at installing double glazing, a heat pump, or upgrading insulation, many major banks are currently offering highly subsidized 'Green Loans' or 'Healthy Home' top-ups at rates as low as 0% to 1% for up to three years. Restructuring your primary mortgage while taking advantage of these heavily discounted green facilities can significantly improve your home's energy efficiency and your monthly cash flow.</p>
<h3>Looking Ahead</h3>
<p>As we navigate through May, we anticipate a steady, if quiet, market. The focus should shift from macro-level market watching to micro-level personal preparation. Ensuring your financial documentation is up-to-date, your pre-approval is active, and your rate strategy is defined will put you in the prime position to capitalize on winter opportunities.</p>
<!-- Post-article Navigation -->
<div style="display:flex;align-items:center;justify-content:space-between;margin-top:4rem;padding-top:2rem;border-top:1px solid rgba(98,162,154,0.4);">
<a href="week-17-autumn-update.html" style="color:var(--finch-forest);font-weight:700;font-size:0.85rem;text-decoration:none;">← Older: Week 17</a>
<span></span>
</div>"""

# Replace the article content using regex
html = re.sub(r'<p style="font-size:1.25rem;.*?</div>', new_article, html, flags=re.DOTALL)

# Add week 18 to the sidebar links
new_sidebar_link = '<a href="week-18-winter-strategies.html" style="display:block;font-size:0.85rem;text-decoration:none;transition:color 0.2s;margin-bottom:0.75rem;color:var(--finch-forest);font-weight:700;border-left:2px solid var(--finch-forest);padding-left:0.75rem;">Week 18: Winter Mortgage Strategies</a>\n'
html = html.replace('<div style="display:flex;flex-direction:column;">', '<div style="display:flex;flex-direction:column;">\n' + new_sidebar_link)

# We need to make Week 17 not active in the sidebar of Week 18
html = html.replace('Week 17: Autumn Market Update: Banks Hold Steady</a>', 'Week 17: Autumn Market Update</a>')
html = html.replace('<a href="week-17-autumn-update.html" style="display:block;font-size:0.85rem;text-decoration:none;transition:color 0.2s;margin-bottom:0.75rem;color:var(--finch-forest);font-weight:700;border-left:2px solid var(--finch-forest);padding-left:0.75rem;">', '<a href="week-17-autumn-update.html" style="display:block;font-size:0.85rem;text-decoration:none;transition:color 0.2s;margin-bottom:0.75rem;color:var(--neutral-medGray);border-left:2px solid transparent;padding-left:0.75rem;">')

with open("weekly-reports/week-18-winter-strategies.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Created week-18-winter-strategies.html")
