import os
import re

filepath = '/Users/sathyamoorthy/Desktop/finch mortgage/thank-you.html'
out_filepath = '/Users/sathyamoorthy/Desktop/finch mortgage/fhb-thank-you.html'

header_html = """<header style="position:fixed;top:0;left:0;right:0;z-index:100;background:#fff;border-bottom:0.5px solid rgba(98,162,154,0.2);height:72px;display:flex;align-items:center;">
<div style="max-width:1100px;margin:0 auto;padding:0 1.5rem;width:100%;display:flex;align-items:center;justify-content:space-between;">
  <a href="first-home-buyers.html"><img alt="Finch Mortgages" src="images/finch-logo.png" style="height:52px;width:auto;"/></a>
  <a href="tel:+64273433293" style="display:flex;align-items:center;gap:8px;font-size:14px;font-weight:600;color:var(--finch-forest);text-decoration:none;">
    <svg fill="none" width="16" height="16" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
    027 343 3293
  </a>
</div>
</header>
<div style="padding-top: 72px;"></div>
"""

footer_html = """<footer style="text-align:center; padding: 2rem 1.5rem; font-size: 13px; color: var(--neutral-medGray); border-top: 0.5px solid rgba(98,162,154,0.2);">
  <div style="display:flex; justify-content:center; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 1rem;">
    <a href="fhb-privacy.html" style="color: var(--neutral-medGray); text-decoration: none;">Privacy</a>
    <a href="fhb-terms.html" style="color: var(--neutral-medGray); text-decoration: none;">Terms</a>
    <a href="fhb-disclaimer.html" style="color: var(--neutral-medGray); text-decoration: none;">Disclaimer</a>
    <a href="fhb-disclosure.html" style="color: var(--neutral-medGray); text-decoration: none;">Disclosure</a>
  </div>
  <div style="font-size: 11px;">
    © 2026 Finch Mortgages Limited. All rights reserved.
  </div>
</footer>"""

with open(filepath, 'r') as f:
    content = f.read()

# Remove main header
content = re.sub(r'<header id="main-header">.*?</header>', '', content, flags=re.DOTALL)

# Remove fullscreen menu
content = re.sub(r'<div id="fullscreen-menu".*?(?=<main)', '', content, flags=re.DOTALL)

# Replace footer
content = re.sub(r'<footer class="site-footer">.*?</footer>', footer_html, content, flags=re.DOTALL)

# Insert minimal header right after <body> or <body class="...">
content = re.sub(r'(<body[^>]*>)', r'\1\n' + header_html, content, count=1)

# Change Return to Home link
content = content.replace('href="index.html" class="btn-primary inline-flex', 'href="first-home-buyers.html" class="btn-primary inline-flex')
content = content.replace('Return to Home', 'Return to Page')

with open(out_filepath, 'w') as f:
    f.write(content)

print(f"Created {out_filepath}")
