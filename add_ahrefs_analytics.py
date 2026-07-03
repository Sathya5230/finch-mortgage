#!/usr/bin/env python3
"""Adds the Ahrefs Web Analytics tracking snippet to every page, right before
</head>, matching how the Meta Pixel is already installed sitewide.

Run once. Idempotent -- skips any file that already has it.
"""
import glob
import os

SNIPPET = '<script src="https://analytics.ahrefs.com/analytics.js" data-key="iBjgWVC1bS+2idlf74YVkA" async></script>\n'

ROOT = os.path.dirname(os.path.abspath(__file__))

changed = 0
skipped = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if "/.claude/" in path or "/node_modules/" in path or "/scratch/" in path:
        continue
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if "analytics.ahrefs.com" in content:
        skipped += 1
        continue

    if "</head>" not in content:
        print(f"  ! no </head> found, skipped: {path}")
        continue

    content = content.replace("</head>", SNIPPET + "</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    changed += 1

print(f"\nAdded Ahrefs Analytics to {changed} files ({skipped} already had it).")
