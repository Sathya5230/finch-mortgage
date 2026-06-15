#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")

def fix_pixel_alt_in_content(content):
    # Match any noscript block with facebook pixel image
    def replacer(match):
        block = match.group(0)
        # Inside the block, find <img ...>
        if '<img' in block:
            # Check if there is an alt attribute
            if re.search(r'alt\s*=\s*["\'][^"\']*["\']', block, re.I):
                # Replace with alt="Facebook Pixel"
                block = re.sub(r'alt\s*=\s*["\'][^"\']*["\']', 'alt="Facebook Pixel"', block, flags=re.I)
            else:
                # Add alt="Facebook Pixel" right after <img
                block = re.sub(r'<img\b', '<img alt="Facebook Pixel"', block, flags=re.I)
        return block

    # Match noscript tags containing facebook.com/tr
    content = re.sub(
        r'<noscript>.*?facebook\.com/tr.*?<img[^>]*>.*?</noscript>|<noscript>.*?<img[^>]*?facebook\.com/tr[^>]*?>.*?</noscript>',
        replacer,
        content,
        flags=re.DOTALL | re.I
    )
    return content

def main():
    skip_dirs = {".git", "node_modules", "logos", ".claude", ".vscode", "docs", "images"}
    updated_count = 0
    
    # Process both html and python files
    for ext in ["*.html", "*.py"]:
        for path in sorted(ROOT.rglob(ext)):
            if any(p in skip_dirs for p in path.parts):
                continue
            if path.name == "fix_pixel_alt.py" or path.name == "seo_audit.py":
                continue
                
            try:
                orig_content = path.read_text(encoding="utf-8")
                fixed_content = fix_pixel_alt_in_content(orig_content)
                if fixed_content != orig_content:
                    path.write_text(fixed_content, encoding="utf-8")
                    print(f"Updated: {path.relative_to(ROOT)}")
                    updated_count += 1
            except Exception as e:
                print(f"Error reading {path}: {e}")
                
    print(f"\nDone! Updated {updated_count} files.")

if __name__ == "__main__":
    main()
