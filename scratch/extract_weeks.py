import os
import re
from bs4 import BeautifulSoup
import json

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"
weekly_dir = os.path.join(ROOT, "weekly-reports")

reports_data = []

for w in range(16, 21):
    filename = f"week-{w}-"
    # Find matching file in directory
    matched_file = None
    for f in os.listdir(weekly_dir):
        if f.startswith(filename) and f.endswith(".html"):
            matched_file = os.path.join(weekly_dir, f)
            break
            
    if not matched_file:
        print(f"No file found for week {w}")
        continue
        
    with open(matched_file, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract details
    slug = os.path.basename(matched_file).replace(".html", "")
    
    # Title
    title = soup.title.string.split("|")[0].replace(f"Week {w}:", "").strip() if soup.title else ""
    
    # Description (excerpt)
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    excerpt = desc_tag['content'] if desc_tag else ""
    
    # Date, Author
    # Look for tags or spans containing "calendar" and "user"
    date_val = ""
    author_val = ""
    # In some templates, date/author are in icons or text
    # Let's search inside the hero section text
    text_content = soup.get_text()
    
    # Let's search for "April 2026", "May 2026", "June 2026", etc. in the HTML
    date_match = re.search(r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+2026\b', html)
    if date_match:
        date_val = date_match.group(0)
        
    author_match = re.search(r'Author:\s*([^<]+)', html, re.I)
    if not author_match:
        # Check standard author names like "Sarah Jenkins", "James Chen", "Liam O'Connor", "Mia Rossi", "Mukhtar Kiyani"
        for name in ["Sarah Jenkins", "James Chen", "Liam O'Connor", "Mia Rossi", "Mukhtar Kiyani"]:
            if name in html:
                author_val = name
                break
                
    # Intro (usually the italic paragraph)
    intro_p = soup.find('p', style=lambda s: s and 'font-style:italic' in s)
    intro = intro_p.get_text().strip().strip('"') if intro_p else ""
    
    # Key Metric
    metric_box = soup.find('div', style=lambda s: s and 'border-left:4px solid var(--finch-forest)' in s)
    stat_label = ""
    stat_val = ""
    if metric_box:
        divs = metric_box.find_all('div')
        # typically:
        # div 1: contains Key Metric title & label
        # div 2: contains stat value
        for d in divs:
            if d.find('div', style=lambda s: s and 'text-transform:uppercase' in s):
                # label is adjacent
                label_div = d.find(lambda tag: tag.name == 'div' and tag.get('style') is None)
                if not label_div:
                    label_div = d.find_all('div')[-1]
                stat_label = label_div.get_text().strip() if label_div else ""
            if d.get('style') and 'font-family:var(--font-display)' in d.get('style'):
                stat_val = d.get_text().strip()
                
    # badge & icon (Rates/Rates, percent/trending-down, etc.)
    badge = "Rates"
    icon = "percent"
    if "Canterbury" in title or "regional" in excerpt.lower() or "region" in excerpt.lower():
        badge = "Regional"
        icon = "map-pin"
    elif "investor" in excerpt.lower() or "yield" in excerpt.lower():
        badge = "Investors"
        icon = "building-2"
    elif "first home" in excerpt.lower() or "kiwisaver" in excerpt.lower():
        badge = "First Home"
        icon = "key"
        
    # Region and City from html (e.g., "Wellington, Wellington Region" or "Auckland, Auckland Region")
    city = "Auckland"
    region = "Auckland Region"
    location_match = re.search(r'·\s*([^,]+),\s*([^\n<]+)', html)
    if location_match:
        city = location_match.group(1).strip()
        region = location_match.group(2).strip()
        # Clean up any trailing badges
        if "·" in region:
            region = region.split("·")[0].strip()
            
    reports_data.append({
        "week": w,
        "slug": slug,
        "date": date_val,
        "badge": badge,
        "icon": icon,
        "title": title,
        "excerpt": excerpt,
        "stat_label": stat_label,
        "stat_val": stat_val,
        "author": author_val or "Mukhtar Kiyani",
        "city": city,
        "region": region,
        "intro": intro
    })

print(json.dumps(reports_data, indent=2))
