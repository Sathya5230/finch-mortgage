#!/usr/bin/env python3
import os, re
from generate_weekly_reports import REPORTS

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"

def gen_card(r, link_prefix=""):
    # Determine the category tag based on badge
    cat_map = {"Rates": "rates", "Regional": "region", "Investors": "invest", "First Home": "first", "Specialist": "rates", "Regulations": "rates", "Market": "region", "Forecast": "region"}
    cat = cat_map.get(r['badge'], "rates")

    # Determine badge class
    bcls = "badge-rates"
    if r['badge'] == "Regional": bcls = "badge-region"
    elif r['badge'] == "Investors": bcls = "badge-invest"
    elif r['badge'] == "First Home": bcls = "badge-first"

    href = f"{link_prefix}weekly-reports/{r['slug']}.html"

    return f"""
        <a href="{href}" class="report-card" data-category="{cat}">
          <div class="report-badge {bcls}"><i data-lucide="{r['icon']}" size="11"></i> {r['badge']}</div>
          <div class="report-week">Week {r['week']} &middot; {r['date']}</div>
          <div class="report-title">{r['title']}</div>
          <div class="report-excerpt">{r['excerpt']}</div>
          <div class="report-meta"><span><i data-lucide="clock" size="12"></i> 6 min read</span><strong>{r['stat_label']}: {r['stat_val']}</strong></div>
        </a>"""

# -----------------------------------------------------
# 1. UPDATE weekly-reports.html (15 cards, no load more)
# -----------------------------------------------------
with open(os.path.join(ROOT, "weekly-reports.html"), "r", encoding="utf-8") as f:
    wr_html = f.read()

# Build 15 cards
all_cards = "".join([gen_card(r, "") for r in REPORTS])

# Replace the grid content
pattern = re.compile(r'(<div id="reports-grid"[^>]*>)(.*?)(</div>\s*<!-- Load more placeholder -->.*?</div>)', re.DOTALL)

def repl_wr(m):
    return m.group(1) + all_cards + "\n      </div>\n      <!-- All reports loaded -->"

new_wr_html = pattern.sub(repl_wr, wr_html)
with open(os.path.join(ROOT, "weekly-reports.html"), "w", encoding="utf-8") as f:
    f.write(new_wr_html)

# -----------------------------------------------------
# 2. UPDATE market-report.html (first 9 cards, with load more)
# -----------------------------------------------------
with open(os.path.join(ROOT, "market-report.html"), "r", encoding="utf-8") as f:
    mr_html = f.read()

# Build top 9 cards
nine_cards = "".join([gen_card(r, "") for r in REPORTS[:9]])  # they are already in the same dir for market-report

# Replace the grid content in market-report.html
pattern_mr = re.compile(r'(<div id="mr-reports-grid"[^>]*>)(.*?)(</div>\s*<div style="text-align:center;margin-top:3rem;">)', re.DOTALL)
def repl_mr(m):
    return m.group(1) + nine_cards + "\n      " + m.group(3)

# Update the "Showing X of Y" text in market-report.html
new_mr_html = pattern_mr.sub(repl_mr, mr_html)
new_mr_html = re.sub(r'Showing 9 of 14 reports in 2026', f'Showing 9 of {len(REPORTS)} reports in 2026', new_mr_html)

with open(os.path.join(ROOT, "market-report.html"), "w", encoding="utf-8") as f:
    f.write(new_mr_html)

print("Updated grids in weekly-reports.html and market-report.html.")
