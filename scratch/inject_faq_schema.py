#!/usr/bin/env python3
"""Extract on-page Q&A from faq.html and inject FAQPage schema."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SITE = "https://www.finchmortgages.co.nz"

path = ROOT / "faq.html"
html = path.read_text(encoding="utf-8")

# Each FAQ block uses .faq-item with a <span> question inside .faq-trigger
# and a <p> answer inside .faq-content
items = re.findall(
    r'<div class="faq-item">\s*'
    r'<button[^>]*class="faq-trigger"[^>]*>\s*'
    r'<span>(.*?)</span>.*?'
    r'<div class="faq-content">\s*<p>(.*?)</p>\s*</div>',
    html, re.S | re.I,
)

qa_pairs = []
for q, a in items:
    qt = re.sub(r"<[^>]+>", " ", q)
    qt = re.sub(r"&amp;", "&", qt)
    qt = re.sub(r"\s+", " ", qt).strip()
    at = re.sub(r"<[^>]+>", " ", a)
    at = re.sub(r"&amp;", "&", at)
    at = re.sub(r"\s+", " ", at).strip()
    if qt and at:
        qa_pairs.append((qt, at))

print(f"Extracted {len(qa_pairs)} Q&A pairs.")

if not qa_pairs:
    raise SystemExit("No Q&A pairs found — schema not added.")

# Check if FAQPage schema already present and remove the stub one (only 1 Q&A)
existing = re.search(r'(<script[^>]+type="application/ld\+json"[^>]*>\s*)(\{[^<]*?"FAQPage"[^<]*?\})(\s*</script>)',
                     html, re.S)

faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "@id": f"{SITE}/faq.html#faq",
    "url": f"{SITE}/faq.html",
    "inLanguage": "en-NZ",
    "mainEntity": [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in qa_pairs
    ],
}

new_block = (
    '<script type="application/ld+json">\n'
    + json.dumps(faq_schema, indent=2, ensure_ascii=False)
    + "\n</script>"
)

if existing:
    html = html[: existing.start()] + new_block + html[existing.end():]
    print("REPLACED existing FAQPage schema.")
else:
    html = html.replace("</head>", new_block + "\n</head>", 1)
    print("INJECTED FAQPage schema.")

path.write_text(html, encoding="utf-8")
