#!/usr/bin/env python3
"""Standardises the brand name to "Finch Mortgages" (plural) everywhere.

The domain (finchmortgages.co.nz) and the legal entity in the footer
("Finch Mortgages Limited") are both plural, but ~619 instances of the
singular "Finch Mortgage" were scattered across titles, meta tags,
og:site_name, JSON-LD org names, and body copy -- including the homepage
<title>. This was diluting branded search signal by splitting the entity
name Google (and users) see for the business.

Order matters: fix the possessive form first ("Finch Mortgage's" ->
"Finch Mortgages'") before the general singular->plural fix, so the
general regex's negative lookahead for a trailing "s" doesn't collide
with it.

Run once. Idempotent -- re-running does nothing further.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

changed_files = 0
total_subs = 0

for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    orig = content

    content, n1 = re.subn(r"Finch Mortgage's", "Finch Mortgages'", content)
    content, n2 = re.subn(r"Finch Mortgage(?!s)", "Finch Mortgages", content)

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        changed_files += 1
        total_subs += n1 + n2

print(f"Fixed brand name in {changed_files} files, {total_subs} replacements.")
