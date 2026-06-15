import os
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SITE = "https://www.finchmortgages.co.nz"

# Custom unique metadata for pages that had thin or duplicate descriptions
CUSTOM_METADATA = {
    "first-home-buyers.html": {
        "title": "First Home Buyer Mortgage NZ | 5% Deposit Loans | Finch",
        "description": "NZ first home buyer mortgage advice — KiwiSaver withdrawal, First Home Grant, low-deposit lending, and expert pre-approval support from Finch Mortgage."
    },
    "thank-you.html": {
        "title": "Thank You for Your Inquiry | Finch Mortgage NZ",
        "description": "Thank you for contacting Finch Mortgage NZ. We have received your inquiry. Our expert NZ mortgage brokers will be in touch shortly to assist with your home loan."
    },
    "fhb-thank-you.html": {
        "title": "Thank You for Your Inquiry | Finch Mortgage NZ",
        "description": "Thank you for contacting Finch Mortgage NZ. We have received your inquiry. Our expert NZ mortgage brokers will be in touch shortly to assist with your home loan."
    },
    "fhb-disclaimer.html": {
        "title": "Website Disclaimer | Finch Mortgage NZ",
        "description": "Read the Finch Mortgage NZ website disclaimer and limitation of liability statement. Understand the terms, exclusions of liability, and copyright rules for our site."
    },
    "fhb-disclosure.html": {
        "title": "Publicly Available Disclosure Statement | Finch Mortgage NZ",
        "description": "Read the Publicly Available Disclosure Statement for Finch Mortgages, authorised under Finsure New Zealand Limited. Learn about our licensing, fees, and commissions."
    },
    "fhb-terms.html": {
        "title": "Terms & Conditions | Finch Mortgage NZ",
        "description": "Finch Mortgage NZ terms and conditions of service. Read our terms and policies before using our mortgage advisory services and website tools."
    }
}

def replace_meta_tag(html, name_attr, name_val, new_content):
    """Replaces or adds a meta tag in html. name_attr can be name or property."""
    pattern = rf'(<meta\b[^>]*?{name_attr}\s*=\s*["\']{re.escape(name_val)}["\'][^>]*?content\s*=\s*)(?:"[^"]*"|\'([^\']*)\')'
    html2, count = re.subn(pattern, lambda m: m.group(1) + f'"{new_content}"', html, count=1, flags=re.I)
    
    if count == 0:
        pattern2 = rf'(<meta\b[^>]*?content\s*=\s*)(?:"([^"]*)"|\'([^\']*)\')(?P<mid>[^>]*?{name_attr}\s*=\s*["\']{re.escape(name_val)}["\'][^>]*?>)'
        html2, count = re.subn(pattern2, lambda m: m.group(1) + f'"{new_content}"' + m.group("mid"), html, count=1, flags=re.I)
        
    if count == 0:
        # Tag doesn't exist, let's prepend it before </head> or after viewport
        meta_tag = f'\n<meta {name_attr}="{name_val}" content="{new_content}"/>'
        if "</head>" in html:
            html2 = html.replace("</head>", f"{meta_tag}\n</head>", 1)
        else:
            html2 = html + meta_tag
            
    return html2

def fix_facebook_pixel(html):
    """Fixes image tags inside noscript block for Facebook Pixel."""
    # Find <noscript><img ...></noscript>
    # If the img doesn't have an alt attribute, add alt=""
    def replacer(match):
        block = match.group(0)
        if 'alt=' not in block:
            # Insert alt="" into the img tag
            img_fixed = re.sub(r'<img\b', '<img alt=""', block, flags=re.I)
            return img_fixed
        return block
        
    html = re.sub(r'<noscript>.*?<img[^>]+>.*?</noscript>', replacer, html, flags=re.DOTALL | re.I)
    return html

def process_file(path: Path):
    rel = path.name
    html = path.read_text(encoding="utf-8")
    
    # Save original for checking changes
    orig = html
    
    # 1. Update Title and Description if in custom metadata
    title = None
    desc = None
    if rel in CUSTOM_METADATA:
        title = CUSTOM_METADATA[rel]["title"]
        desc = CUSTOM_METADATA[rel]["description"]
        
        # Replace title tag
        html, _ = re.subn(r"<title[^>]*>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S | re.I)
        
        # Replace meta description
        html = replace_meta_tag(html, "name", "description", desc)
    else:
        # Extract title and description
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        title = title_match.group(1).strip() if title_match else "Finch Mortgage"
        
        # Extract description
        for m in re.finditer(r"<meta\b([^>]*)>", html, re.I):
            attrs = m.group(1)
            if re.search(r'name\s*=\s*["\']description["\']', attrs, re.I):
                c = re.search(r'content\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', attrs, re.I)
                if c:
                    desc = (c.group(1) or c.group(2) or "").strip()
                    break
        if not desc:
            desc = "Independent NZ mortgage broker arranging home loans across every NZ city, town, and rural area."
            
    # 2. Ensure mobile viewport tag
    if 'name="viewport"' not in html and "name='viewport'" not in html:
        viewport_tag = '<meta content="width=device-width, initial-scale=1.0" name="viewport"/>'
        if "<head>" in html:
            html = html.replace("<head>", f"<head>\n{viewport_tag}", 1)
            
    # 3. Ensure favicon link
    if 'rel="icon"' not in html and 'rel="shortcut icon"' not in html:
        favicon_tag = '<link href="/favicon.png" rel="icon" type="image/png"/>'
        if "</head>" in html:
            html = html.replace("</head>", f"{favicon_tag}\n</head>", 1)
            
    # 4. Ensure canonical link
    expected_canon = f"{SITE}/" if rel == "index.html" else f"{SITE}/{rel}"
    # Replace or add canonical
    canon_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html, re.I)
    if canon_match:
        # Update href in canonical
        html = re.sub(r'(<link[^>]+rel=["\']canonical["\'][^>]+href=["\'])([^"\']+)', rf'\g<1>{expected_canon}', html, flags=re.I)
        html = re.sub(r'(<link[^>]+href=["\'])([^"\']+)(["\'][^>]+rel=["\']canonical["\'])', rf'\g<1>{expected_canon}\g<3>', html, flags=re.I)
    else:
        canon_tag = f'<link href="{expected_canon}" rel="canonical"/>'
        if "</head>" in html:
            html = html.replace("</head>", f"{canon_tag}\n</head>", 1)
            
    # 5. Open Graph & Twitter tags
    html = replace_meta_tag(html, "property", "og:type", "website")
    html = replace_meta_tag(html, "property", "og:title", title)
    html = replace_meta_tag(html, "property", "og:description", desc)
    html = replace_meta_tag(html, "property", "og:url", expected_canon)
    html = replace_meta_tag(html, "property", "og:image", f"{SITE}/images/og-default.jpg")
    html = replace_meta_tag(html, "property", "og:site_name", "Finch Mortgage")
    html = replace_meta_tag(html, "property", "og:locale", "en_NZ")
    
    html = replace_meta_tag(html, "name", "twitter:card", "summary_large_image")
    html = replace_meta_tag(html, "name", "twitter:title", title)
    html = replace_meta_tag(html, "name", "twitter:description", desc)
    html = replace_meta_tag(html, "name", "twitter:image", f"{SITE}/images/og-default.jpg")
    
    # 6. Fix facebook pixel alt
    html = fix_facebook_pixel(html)
    
    if html != orig:
        path.write_text(html, encoding="utf-8")
        print(f"Updated root page: {rel}")
    else:
        print(f"No changes for root page: {rel}")

def main():
    skip_dirs = {".git", "node_modules", "scratch", "logos", ".claude", ".vscode", "docs", "images", "weekly-reports", "lenders", "blog", "case-studies", "services", "calculators", "guides", "testimonials"}
    
    # Scan root level html files
    for path in sorted(ROOT.glob("*.html")):
        if path.is_file():
            process_file(path)

if __name__ == "__main__":
    main()
