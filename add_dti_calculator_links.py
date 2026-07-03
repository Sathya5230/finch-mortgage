#!/usr/bin/env python3
"""Adds the new DTI Ratio calculator to the sitewide nav dropdown and footer
calculator lists, right after "Extra Repayment", on every page that has them.

Run once after adding calculators/dti-calculator.html. Idempotent: skips
pages that already link to dti-calculator.html.
"""
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV_OLD_ROOT = '<a class="dropdown-item" href="calculators/extra-repayment.html">Extra Repayment</a></div></div>'
NAV_NEW_ROOT = '<a class="dropdown-item" href="calculators/extra-repayment.html">Extra Repayment</a><a class="dropdown-item" href="calculators/dti-calculator.html">DTI Ratio</a></div></div>'

NAV_OLD_SUB = '<a class="dropdown-item" href="../calculators/extra-repayment.html">Extra Repayment</a></div></div>'
NAV_NEW_SUB = '<a class="dropdown-item" href="../calculators/extra-repayment.html">Extra Repayment</a><a class="dropdown-item" href="../calculators/dti-calculator.html">DTI Ratio</a></div></div>'

FOOTER_OLD_ROOT = '<a href="calculators/extra-repayment.html">Extra Repayment</a></div>'
FOOTER_NEW_ROOT = '<a href="calculators/extra-repayment.html">Extra Repayment</a><a href="calculators/dti-calculator.html">DTI Ratio</a></div>'

FOOTER_OLD_SUB = '<a href="../calculators/extra-repayment.html">Extra Repayment</a></div>'
FOOTER_NEW_SUB = '<a href="../calculators/extra-repayment.html">Extra Repayment</a><a href="../calculators/dti-calculator.html">DTI Ratio</a></div>'

changed = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if os.path.basename(path) == "dti-calculator.html":
        continue
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if "dti-calculator.html" in content:
        continue  # already linked

    orig = content
    content = content.replace(NAV_OLD_SUB, NAV_NEW_SUB)
    content = content.replace(NAV_OLD_ROOT, NAV_NEW_ROOT)
    content = content.replace(FOOTER_OLD_SUB, FOOTER_NEW_SUB)
    content = content.replace(FOOTER_OLD_ROOT, FOOTER_NEW_ROOT)

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        changed += 1

print(f"Updated {changed} files with DTI calculator links.")
