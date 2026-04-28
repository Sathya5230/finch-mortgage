#!/usr/bin/env python3
import os
import glob
import re

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"

# Regex patterns for NAV items
nav_re_root = re.compile(
    r'<div class="nav-item"><div class="dropdown-trigger nav-link">Calculators.*?</div>'
)
nav_repl_root = r'<a href="calculators.html" class="nav-link">Calculators</a>'

nav_re_sub = re.compile(
    r'<div class="nav-item"><div class="dropdown-trigger nav-link">Calculators.*?</div>'
)
nav_repl_sub = r'<a href="../calculators.html" class="nav-link">Calculators</a>'

# Update mobile menu items
mob_nav_re_root = re.compile(
    r'<div style="width:100%;max-width:300px;">\s*<div class="mobile-dropdown-trigger"[^>]*>Calculators.*?(?=</div>\s*</div>\s*<a href="about.html")</div>\s*</div>',
    re.DOTALL
)
mob_nav_repl_root = r'<a href="calculators.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Calculators</a>'

mob_nav_re_sub = re.compile(
    r'<div style="width:100%;max-width:300px;">\s*<div class="mobile-dropdown-trigger"[^>]*>Calculators.*?(?=</div>\s*</div>\s*<a href="../about.html")</div>\s*</div>',
    re.DOTALL
)
mob_nav_repl_sub = r'<a href="../calculators.html" style="font-size:1.5rem;font-weight:700;color:var(--neutral-black);text-decoration:none;">Calculators</a>'


# General href replacements for anchor tags in body (that are not inside calculators.html grid)
button_href_re_root = re.compile(r'href="calculators/[^"]+\.html"')
button_href_repl_root = r'href="calculators.html"'

button_href_re_sub = re.compile(r'href="\.\./calculators/[^"]+\.html"')
button_href_repl_sub = r'href="../calculators.html"'

# We use absolute paths. 
all_html = glob.glob(f"{ROOT}/**/*.html", recursive=True)

for path in all_html:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content
    is_sub_dir = "/" in path.replace(ROOT + "/", "")  # if there's a slash after relative to root

    # Skip calculators.html payload, but do its NAV? I'll do NAV for calculators.html, but NOT button link rewrites
    skip_body_rewrites = os.path.basename(path) == "calculators.html"

    # Step 1: Nav rewrites (Desktop)
    if is_sub_dir:
        content = nav_re_sub.sub(nav_repl_sub, content)
    else:
        content = nav_re_root.sub(nav_repl_root, content)

    # Step 2: Nav rewrites (Mobile)
    if is_sub_dir:
        content = mob_nav_re_sub.sub(mob_nav_repl_sub, content)
    else:
        content = mob_nav_re_root.sub(mob_nav_repl_root, content)

    # Step 3: Body rewrites
    if not skip_body_rewrites:
        # We need to skip the links inside files dynamically if they are part of the calculator themselves? 
        # Actually, if we are INSIDE a calculator (e.g. calculators/mortgage-calculator.html), we might break internal links. But those don't really cross-link to each other besides the nav.
        if is_sub_dir:
            content = button_href_re_sub.sub(button_href_repl_sub, content)
        else:
            content = button_href_re_root.sub(button_href_repl_root, content)

    if content != orig_content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {path}")

print("Calculation links updated successfully.")
