#!/usr/bin/env python3
"""One-off fix for meta descriptions outside the ~120-158 char SERP-safe
range (measured after HTML-entity decoding). Updates name="description",
og:description, and twitter:description together, plus any JSON-LD
"description" field that exactly matched the old text.

Run once.
"""

FIXES = {
    "index.html": (
        "NZ's trusted mortgage broker — compare 20+ lenders, get expert home loan advice, and secure pre-approval. $0 broker fee. First home buyers welcome. Free consultation.",
        "NZ's trusted mortgage broker — compare 20+ lenders, get expert home loan advice, and secure pre-approval. $0 broker fee. Free consultation.",
    ),
    "case-studies/family-guarantee-first-home.html": (
        "A young Christchurch couple bought their first home with just 8% saved, using a family guarantee from her parents to bridge the deposit gap without injecting fresh cash.",
        "A young Christchurch couple bought their first home with 8% saved, using a family guarantee from her parents to bridge the deposit gap.",
    ),
    "case-studies/new-migrant-first-mortgage.html": (
        "A UK-trained engineer who moved to Auckland 14 months earlier had no NZ credit history but strong income. Finch matched him to a lender comfortable with short residency.",
        "A UK-trained engineer who moved to Auckland 14 months earlier had no NZ credit history but strong income. Finch found a lender comfortable with short residency.",
    ),
    "services/commercial-property.html": (
        "Need a commercial property loan in NZ? Our commercial mortgage broker compares lenders for retail, office, and industrial finance. Competitive rates. Free consultation.",
        "Need a commercial property loan in NZ? We compare lenders for retail, office, and industrial finance. Competitive rates, free consultation.",
    ),
    "blog/first-home-partner-scheme-explained.html": (
        "Kāinga Ora's First Home Partner shared-ownership scheme is closed to new applicants. How it worked, what existing participants should know, and the 2026 alternatives.",
        "Kāinga Ora's First Home Partner scheme is closed to new applicants. How it worked and what 2026 alternatives exist for first home buyers.",
    ),
    "case-studies/self-employed-approval.html": (
        "Self-employed with only 14 months trading history — how Finch got this mortgage approved. Real NZ case study.",
        "Self-employed with only 14 months trading history — how Finch got this NZ mortgage approved despite the bank's standard 2-year policy. Real client case study.",
    ),
    "terms.html": (
        "Finch Mortgages NZ terms and conditions of service. Read our terms before using our mortgage advisory services.",
        "Finch Mortgages NZ terms and conditions of service — read our terms of use before engaging our independent mortgage advisory and broking services.",
    ),
}

for path, (old, new) in FIXES.items():
    with open(path, encoding="utf-8") as f:
        content = f.read()
    n = content.count(old)
    content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {path} -> {n} replacement(s)")
