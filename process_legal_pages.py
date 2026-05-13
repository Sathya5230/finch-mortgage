import os
import re

files_to_process = ['privacy.html', 'terms.html', 'disclaimer.html', 'disclosure.html']

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

for filename in files_to_process:
    filepath = os.path.join('/Users/sathyamoorthy/Desktop/finch mortgage', filename)
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove main header and full screen menu
    # Using regex to find <header id="main-header">...</header>
    content = re.sub(r'<header id="main-header">.*?</header>', '', content, flags=re.DOTALL)
    
    # Using regex to find <div id="fullscreen-menu"...</div> where </div> is before <main class="main-content container pb-32">
    # A safe way is to find from <div id="fullscreen-menu" up to the start of <main
    content = re.sub(r'<div id="fullscreen-menu".*?(?=<main)', '', content, flags=re.DOTALL)
    
    # Replace footer
    content = re.sub(r'<footer class="site-footer">.*?</footer>', footer_html, content, flags=re.DOTALL)
    
    # Insert minimal header right after <body> or <body class="...">
    content = re.sub(r'(<body[^>]*>)', r'\1\n' + header_html, content, count=1)
    
    # Remove link tags to main css from privacy pages if they have bad paths? No, paths are fine.
    # Update title
    # content = re.sub(r'<title>(.*?)</title>', r'<title>\1 (First Home Buyers)</title>', content)
    
    # Save to fhb-* file
    out_filename = 'fhb-' + filename
    out_filepath = os.path.join('/Users/sathyamoorthy/Desktop/finch mortgage', out_filename)
    
    with open(out_filepath, 'w') as f:
        f.write(content)
    print(f"Created {out_filename}")
