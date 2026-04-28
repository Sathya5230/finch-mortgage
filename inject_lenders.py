#!/usr/bin/env python3
"""
Injects Lenders link into the Resources dropdown across all HTML pages.
Root pages use lenders.html, sub-pages use ../lenders.html
"""
import os, re

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"

# Look for the Market dropdown section end and Stories label start
OLD_PATTERN = re.compile(
    r'(<div class="dropdown-label">Market</div>.*?)(<div class="dropdown-divider"></div><div class="dropdown-label">Stories</div>)',
    re.DOTALL
)

def inject(content, prefix):
    lender_link = f'<a href="{prefix}lenders.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#127976; Lenders</a>'
    replacement = r'\1' + lender_link + r'\2'
    new_content, count = OLD_PATTERN.subn(replacement, content)
    return new_content, count

updated = 0
skipped = 0
for dirpath, _, files in os.walk(ROOT):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(dirpath, fname)
        rel = os.path.relpath(fpath, ROOT)
        
        # Don't inject into lenders.html since we hardcoded it during generation
        if fname == "lenders.html":
            continue

        depth = rel.count(os.sep)
        prefix = "../" * depth

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if already has lenders link
        if "lenders.html" in content and "Lenders" in content:
            print(f"  SKIP (already has link): {rel}")
            skipped += 1
            continue

        new_content, count = inject(content, prefix)

        if count > 0:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  UPDATED ({count} injection): {rel}")
            updated += 1
        else:
            print(f"  NO MATCH: {rel}")

print(f"\nDone. Updated: {updated}, Skipped (already had link): {skipped}")
