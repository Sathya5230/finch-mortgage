#!/usr/bin/env python3
"""Adds the new rental yield calculator and mortgage glossary to the sitewide
nav dropdown, Resources mega-menu, and footer, right after the existing last
item in each list. Idempotent: skips a page if it already links to the
relevant new page.

Run once after adding calculators/rental-yield-calculator.html and
guides/mortgage-glossary-nz.html.
"""
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

REPLACEMENTS_SUB = [  # for pages one directory deep (../ prefix)
    (
        '<a class="dropdown-item" href="../calculators/dti-calculator.html">DTI Ratio</a></div></div>',
        '<a class="dropdown-item" href="../calculators/dti-calculator.html">DTI Ratio</a><a class="dropdown-item" href="../calculators/rental-yield-calculator.html">Rental Yield</a></div></div>',
    ),
    (
        '<a class="res-mega-item" href="../guides/step-by-step.html">Step-by-Step Guide</a>',
        '<a class="res-mega-item" href="../guides/step-by-step.html">Step-by-Step Guide</a><a class="res-mega-item" href="../guides/mortgage-glossary-nz.html">Mortgage Glossary</a>',
    ),
    (
        '<a href="../calculators/dti-calculator.html">DTI Ratio</a></div>',
        '<a href="../calculators/dti-calculator.html">DTI Ratio</a><a href="../calculators/rental-yield-calculator.html">Rental Yield</a></div>',
    ),
    (
        '<a href="../guides/first-home-guide.html">First Home Guide</a>',
        '<a href="../guides/first-home-guide.html">First Home Guide</a><a href="../guides/mortgage-glossary-nz.html">Mortgage Glossary</a>',
    ),
]

REPLACEMENTS_ROOT = [  # for root-level pages (no prefix)
    (
        '<a class="dropdown-item" href="calculators/dti-calculator.html">DTI Ratio</a></div></div>',
        '<a class="dropdown-item" href="calculators/dti-calculator.html">DTI Ratio</a><a class="dropdown-item" href="calculators/rental-yield-calculator.html">Rental Yield</a></div></div>',
    ),
    (
        '<a class="res-mega-item" href="guides/step-by-step.html">Step-by-Step Guide</a>',
        '<a class="res-mega-item" href="guides/step-by-step.html">Step-by-Step Guide</a><a class="res-mega-item" href="guides/mortgage-glossary-nz.html">Mortgage Glossary</a>',
    ),
    (
        '<a href="calculators/dti-calculator.html">DTI Ratio</a></div>',
        '<a href="calculators/dti-calculator.html">DTI Ratio</a><a href="calculators/rental-yield-calculator.html">Rental Yield</a></div>',
    ),
    (
        '<a href="guides/first-home-guide.html">First Home Guide</a>',
        '<a href="guides/first-home-guide.html">First Home Guide</a><a href="guides/mortgage-glossary-nz.html">Mortgage Glossary</a>',
    ),
]

SKIP_BASENAMES = {"rental-yield-calculator.html", "mortgage-glossary-nz.html"}

changed = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if os.path.basename(path) in SKIP_BASENAMES:
        continue
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if "rental-yield-calculator.html" in content or "mortgage-glossary-nz.html" in content:
        continue  # already linked (e.g. calculators.html, handled by hand)

    orig = content
    rel_path = os.path.relpath(path, ROOT)
    is_sub_dir = os.sep in rel_path
    replacements = REPLACEMENTS_SUB if is_sub_dir else REPLACEMENTS_ROOT

    for old, new in replacements:
        content = content.replace(old, new)

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        changed += 1

print(f"Updated {changed} files with rental yield calculator + mortgage glossary links.")
