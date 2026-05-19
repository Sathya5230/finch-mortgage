#!/usr/bin/env python3
"""Add <meta name="robots" content="noindex,follow"> to the fhb-* legal duplicates
and to thank-you pages. These pages already have canonicals pointing to the
non-fhb originals; noindex prevents indexing of the dupes entirely.
Idempotent.
"""
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")

TARGETS = [
    "fhb-disclaimer.html",
    "fhb-disclosure.html",
    "fhb-privacy.html",
    "fhb-terms.html",
    "fhb-thank-you.html",
    "thank-you.html",
]

NOINDEX = '<meta name="robots" content="noindex,follow"/>\n'

for rel in TARGETS:
    path = ROOT / rel
    if not path.exists():
        print(f"MISSING: {rel}")
        continue
    html = path.read_text(encoding="utf-8")
    if re.search(r'<meta[^>]+name=["\']robots["\']', html, re.I):
        # update existing robots tag
        new = re.sub(
            r'<meta[^>]+name=["\']robots["\'][^>]*>',
            '<meta name="robots" content="noindex,follow"/>',
            html, count=1, flags=re.I,
        )
        if new != html:
            path.write_text(new, encoding="utf-8")
            print(f"UPDATED robots meta: {rel}")
        else:
            print(f"NOCHANGE: {rel}")
    else:
        # insert just after <head>
        m = re.search(r"<head[^>]*>", html, re.I)
        if not m:
            print(f"NO <head>: {rel}")
            continue
        i = m.end()
        new = html[:i] + "\n" + NOINDEX + html[i:]
        path.write_text(new, encoding="utf-8")
        print(f"INJECTED robots meta: {rel}")
