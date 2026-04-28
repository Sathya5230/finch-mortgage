#!/usr/bin/env python3
"""
Injects Market Report link into the Resources dropdown across all HTML pages.
Root pages use market-report.html, sub-pages use ../market-report.html
"""
import os, re

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"

# The OLD text to find (no market report link).
OLD_PATTERN = re.compile(
    r'(<div class="dropdown-divider"></div>)(<div class="dropdown-label">Stories</div>)',
    re.DOTALL
)

def inject(content, prefix):
    market_link = (
        f'<div class="dropdown-divider"></div>'
        f'<div class="dropdown-label">Market</div>'
        f'<a href="{prefix}market-report.html" class="dropdown-item" style="font-weight:700;color:var(--finch-forest);">&#128202; Market Report</a>'
    )
    replacement = market_link + r'\1\2'
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
        depth = rel.count(os.sep)
        prefix = "../" * depth  # root=0 levels deep, subdirs=1+

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if already has market-report link
        if "market-report.html" in content:
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
