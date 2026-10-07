"""Rewrite title/description/og/twitter meta on city broker posts and location pages.

Head-only and per-page unique (city and, where relevant, suburbs differ on every page).
Never touches body content. Run with --apply to write; default is a dry run.
"""
import html
import re
import sys
from pathlib import Path

from city_data import CITIES

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

SERVICE_TITLES = {
    "home-loan": ["Home Loans {c} | Compare 20+ NZ Lenders | Finch", "Home Loans {c} | Compare 20+ Lenders", "Home Loans {c} | Finch"],
    "first-home-buyer": ["First Home Buyer {c} | KiwiSaver & Low Deposit | Finch", "First Home Buyer {c} | KiwiSaver & Low Deposit", "First Home Buyer {c} | Finch"],
    "refinance": ["Refinance Mortgage {c} | Compare 20+ Lenders | Finch", "Refinance Mortgage {c} | 20+ Lenders", "Refinance {c} | Finch"],
    "investment-property": ["Investment Property Loans {c} | Finch Mortgages", "Investment Property Loans {c} | Finch", "Investment Loans {c} | Finch"],
    "self-employed": ["Self-Employed Home Loans {c} | Low-Doc | Finch", "Self-Employed Home Loans {c} | Finch", "Self-Employed Loans {c} | Finch"],
    "pre-approval": ["Mortgage Pre-Approval {c} | $0 Broker Fee | Finch", "Mortgage Pre-Approval {c} | Finch", "Pre-Approval {c} | Finch"],
}

SERVICE_DESC = {
    "home-loan": "Buying in {c}? Finch compares 20+ NZ lenders for a home loan that suits buyers in {s}. Free advice, $0 broker fee.",
    "first-home-buyer": "First home in {c}? Finch explains KiwiSaver, First Home Loan and deposit options in {s}. Compare 20+ NZ lenders, $0 broker fee.",
    "refinance": "Refinancing in {c}? Finch compares 20+ NZ lenders to cut your rate, for homeowners in {s}. Free review, $0 broker fee.",
    "investment-property": "Investing in {c}? Finch structures rental and portfolio lending across 20+ NZ lenders for {s}. Free advice, $0 broker fee.",
    "self-employed": "Self-employed in {c}? Finch finds lenders who assess business owners fairly, from {s}. Low-doc options, $0 broker fee.",
    "pre-approval": "Get mortgage pre-approval in {c} before you bid. Finch compares 20+ NZ lenders for buyers in {s}. Free advice, $0 broker fee.",
}

# "Mortgage adviser {city}" is searched separately from "mortgage broker {city}" in NZ, so titles carry both.
BROKER_TITLES = ["Mortgage Broker {c} | $0 Fee Mortgage Adviser | Finch", "Mortgage Broker {c} | Mortgage Adviser | Finch", "Mortgage Broker {c} | $0 Fee | Finch", "Mortgage Broker {c} | Finch"]
BROKER_DESC = "Independent {c} mortgage broker and adviser covering {s}. Compare 20+ NZ lenders with Finch. $0 broker fee."
BROKER_DESC_NZ = "Online NZ mortgage broker and adviser. Finch arranges home loans by phone and video for buyers anywhere in New Zealand across 20+ lenders. $0 broker fee."
# The homepage targets "mortgage broker Auckland & NZ"; these pages take distinct angles so they don't compete with it.
CITY_LABEL = {"mortgage-broker-auckland-city": "Central Auckland"}


def fit(options, limit, **kw):
    for opt in options:
        text = html.unescape(opt.format(**kw))
        if len(text) <= limit:
            return text
    return html.unescape(options[-1].format(**kw))[:limit]


def suburbs(c, n):
    parts = [html.unescape(x).strip() for x in c["suburbs"].split(",")]
    parts = [p for p in parts if not p.lower().startswith("and ") and "wider" not in p.lower()]
    if n == 1:
        return parts[0]
    return ", ".join(parts[: n - 1]) + " and " + parts[n - 1]


def desc_fit(template, c, limit=160):
    city = html.unescape(c["city"])
    for n in (3, 2, 1):
        text = template.format(c=city, s=suburbs(c, n))
        if len(text) <= limit:
            return text
    raise ValueError(f"description too long for {city}: {text}")


def retag(src, title, desc):
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    subs = [
        (r"<title>.*?</title>", f"<title>{t}</title>"),
        (r'<meta content="[^"]*" name="description"/?>', f'<meta content="{d}" name="description"/>'),
        (r'<meta content="[^"]*" property="og:title"/?>', f'<meta content="{t}" property="og:title"/>'),
        (r'<meta content="[^"]*" property="og:description"/?>', f'<meta content="{d}" property="og:description"/>'),
        (r'<meta content="[^"]*" name="twitter:title"/?>', f'<meta content="{t}" name="twitter:title"/>'),
        (r'<meta content="[^"]*" name="twitter:description"/?>', f'<meta content="{d}" name="twitter:description"/>'),
    ]
    for pat, rep in subs:
        src, n = re.subn(pat, lambda m, r=rep: r, src, count=1, flags=re.S)
        if n != 1:
            return None
    return src


def main():
    jobs = []
    by_slug = {c["slug"]: c for c in CITIES}
    for c in CITIES:
        path = ROOT / "blog" / f"{c['slug']}.html"
        if not path.exists():
            continue
        city = CITY_LABEL.get(c["slug"], html.unescape(c["city"]))
        if c["slug"] == "mortgage-broker-nz":
            title, desc = "Online Mortgage Broker NZ | Nationwide, $0 Fee | Finch", BROKER_DESC_NZ
        else:
            title = fit(BROKER_TITLES, 60, c=city)
            desc = desc_fit(BROKER_DESC, dict(c, city=city))
        jobs.append((path, title, desc))

    for path in sorted((ROOT / "locations").glob("*.html")):
        stem = path.stem
        for svc in SERVICE_TITLES:
            if stem.startswith(svc + "-"):
                c = by_slug.get("mortgage-broker-" + stem[len(svc) + 1:])
                if not c:
                    break
                city = html.unescape(c["city"])
                jobs.append((path, fit(SERVICE_TITLES[svc], 60, c=city), desc_fit(SERVICE_DESC[svc], c)))
                break

    seen_t, seen_d, skipped, changed = {}, {}, [], 0
    for path, title, desc in jobs:
        seen_t.setdefault(title, []).append(path.name)
        seen_d.setdefault(desc, []).append(path.name)
        src = path.read_text(encoding="utf-8")
        out = retag(src, title, desc)
        if out is None:
            skipped.append(path.name)
            continue
        if out != src:
            changed += 1
            if APPLY:
                path.write_text(out, encoding="utf-8")
    dup_t = {k: v for k, v in seen_t.items() if len(v) > 1}
    dup_d = {k: v for k, v in seen_d.items() if len(v) > 1}
    print(f"pages: {len(jobs)}  changed: {changed}  skipped (tag mismatch): {skipped}")
    print(f"duplicate titles: {len(dup_t)}  duplicate descriptions: {len(dup_d)}")
    print(f"max title len: {max(len(html.unescape(t)) for t in seen_t)}  max desc len: {max(len(html.unescape(d)) for d in seen_d)}")
    for path, title, desc in jobs[:3] + jobs[40:44]:
        print(f"\n{path.name}\n  {title}\n  {desc}")
    print("\nAPPLIED" if APPLY else "\nDRY RUN (use --apply)")


main()
