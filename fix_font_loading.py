#!/usr/bin/env python3
"""
Performance: convert the render-blocking @import in style.css into a parallel
<link> in each page <head>, and drop the unused Inter font from generated pages.
Idempotent. Run with: python3 fix_font_loading.py
Pair with: remove the @import line from style.css (this script does that too).
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:'
             'ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:'
             'ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet"/>')

# any existing google-fonts css <link> (e.g. the unused Inter one on generated pages)
EXISTING_FONT = re.compile(r'\s*<link[^>]*fonts\.googleapis\.com/css2[^>]*>')
# the style.css stylesheet link (root or ../, optional ?v=)
STYLE_LINK = re.compile(r'(<link href="(?:\.\./)?style\.css(?:\?v=\d+)?" rel="stylesheet"/>)')

changed = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if "node_modules" in f:
        continue
    s = open(f, encoding="utf-8").read()
    before = s
    # remove any existing google-fonts css link (dedupe / drop unused Inter)
    s = EXISTING_FONT.sub("", s)
    # insert canonical font link immediately before the style.css stylesheet link
    if FONT_LINK not in s:
        s = STYLE_LINK.sub(FONT_LINK + r"\n\1", s, count=1)
    if s != before:
        open(f, "w", encoding="utf-8").write(s)
        changed += 1
print(f"updated {changed} html files with parallel font <link>")

# remove the @import from style.css
css_path = os.path.join(ROOT, "style.css")
css = open(css_path, encoding="utf-8").read()
new_css = re.sub(r"^@import url\([^)]*\);\s*\n?", "", css, count=1)
if new_css != css:
    open(css_path, "w", encoding="utf-8").write(new_css)
    print("removed @import from style.css")
else:
    print("no @import found in style.css (already removed)")
