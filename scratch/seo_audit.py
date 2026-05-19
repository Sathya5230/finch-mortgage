#!/usr/bin/env python3
"""Read-only SEO/GEO/AEO audit. Does NOT modify any HTML files."""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/sathyamoorthy/Desktop/finch mortgage")
SITE = "https://www.finchmortgages.co.nz"


def extract(pattern, html, flags=re.IGNORECASE | re.DOTALL):
    m = re.search(pattern, html, flags)
    return m.group(1).strip() if m else None


def meta_by(html, attr, value):
    """Find <meta {attr}="{value}"> tag and return its content= value, regardless of order.
    Handles quote-aware matching so apostrophes inside double-quoted values don't break it."""
    for m in re.finditer(r"<meta\b([^>]*)>", html, re.IGNORECASE):
        attrs = m.group(1)
        if re.search(rf'{attr}\s*=\s*["\']{re.escape(value)}["\']', attrs, re.I):
            c = re.search(r'content\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', attrs, re.I)
            if c:
                return (c.group(1) or c.group(2) or "").strip()
    return None


def audit_page(path: Path):
    rel = path.relative_to(ROOT).as_posix()
    html = path.read_text(encoding="utf-8", errors="ignore")
    head = html.split("</head>")[0] if "</head>" in html else html[:8000]

    title = extract(r"<title[^>]*>(.*?)</title>", head)
    desc = meta_by(head, "name", "description")
    canonical = extract(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', head)
    if not canonical:
        canonical = extract(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', head)
    og_title = meta_by(head, "property", "og:title")
    og_desc = meta_by(head, "property", "og:description")
    og_url = meta_by(head, "property", "og:url")
    og_image = meta_by(head, "property", "og:image")
    tw_card = meta_by(head, "name", "twitter:card")
    robots = meta_by(head, "name", "robots")

    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    h1s = [re.sub(r"<[^>]+>", "", h).strip() for h in h1s]
    h1s = [h for h in h1s if h]

    jsonld_blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.IGNORECASE | re.DOTALL,
    )
    schema_types = []
    for block in jsonld_blocks:
        schema_types.extend(re.findall(r'"@type"\s*:\s*"([^"]+)"', block))

    images = re.findall(r"<img\b([^>]*)>", html, re.IGNORECASE)
    imgs_total = len(images)
    imgs_no_alt = sum(1 for attrs in images if not re.search(r'alt\s*=\s*["\'][^"\']+', attrs, re.I))

    if rel == "index.html":
        expected_canon = f"{SITE}/"
    else:
        expected_canon = f"{SITE}/{rel}"

    issues = []
    if not title: issues.append("missing-title")
    elif len(title) < 30: issues.append(f"short-title({len(title)})")
    elif len(title) > 65: issues.append(f"long-title({len(title)})")

    if not desc: issues.append("missing-description")
    elif len(desc) < 110: issues.append(f"short-desc({len(desc)})")
    elif len(desc) > 170: issues.append(f"long-desc({len(desc)})")

    if not canonical:
        issues.append("missing-canonical")
    elif canonical != expected_canon:
        if not (rel == "index.html" and canonical in (f"{SITE}/", f"{SITE}/index.html")):
            issues.append(f"wrong-canonical")

    if not og_title: issues.append("missing-og:title")
    if not og_desc: issues.append("missing-og:description")
    if not og_url:
        issues.append("missing-og:url")
    elif og_url != expected_canon and not (rel == "index.html" and og_url in (f"{SITE}/", f"{SITE}/index.html")):
        issues.append("wrong-og:url")
    if not og_image: issues.append("missing-og:image")
    if not tw_card: issues.append("missing-twitter:card")
    if len(h1s) == 0: issues.append("no-h1")
    elif len(h1s) > 1: issues.append(f"multi-h1({len(h1s)})")
    if not jsonld_blocks: issues.append("no-schema")
    if imgs_no_alt: issues.append(f"imgs-no-alt({imgs_no_alt}/{imgs_total})")

    return {
        "path": rel, "title": title, "desc": desc, "canonical": canonical,
        "og_title": og_title, "og_url": og_url, "og_image": og_image,
        "h1s": h1s, "schema_types": schema_types, "robots": robots,
        "issues": issues, "imgs_total": imgs_total, "imgs_no_alt": imgs_no_alt,
    }


def main():
    pages = []
    skip_dirs = {".git", "node_modules", "scratch", "logos", ".claude", ".vscode", "docs", "images"}
    for path in sorted(ROOT.rglob("*.html")):
        if any(p in skip_dirs for p in path.parts):
            continue
        pages.append(audit_page(path))

    print(f"PAGES AUDITED: {len(pages)}\n")

    titles = defaultdict(list)
    descs = defaultdict(list)
    canons = defaultdict(list)
    for p in pages:
        if p["title"]: titles[p["title"]].append(p["path"])
        if p["desc"]: descs[p["desc"]].append(p["path"])
        if p["canonical"]: canons[p["canonical"]].append(p["path"])

    print("=== DUPLICATE TITLES ===")
    dupe_titles = {t: ps for t, ps in titles.items() if len(ps) > 1}
    for t, ps in dupe_titles.items():
        print(f"  '{t}' ({len(ps)}): {ps}")
    if not dupe_titles: print("  (none)")

    print("\n=== DUPLICATE DESCRIPTIONS ===")
    dupe_descs = {d: ps for d, ps in descs.items() if len(ps) > 1}
    for d, ps in dupe_descs.items():
        print(f"  ({len(ps)}) {ps}\n     '{d[:100]}...'")
    if not dupe_descs: print("  (none)")

    print("\n=== DUPLICATE CANONICALS ===")
    dupe_canon = {c: ps for c, ps in canons.items() if len(ps) > 1}
    for c, ps in dupe_canon.items():
        print(f"  '{c}': {ps}")
    if not dupe_canon: print("  (none)")

    print("\n=== ISSUE FREQUENCY ===")
    freq = defaultdict(int)
    for p in pages:
        for issue in p["issues"]:
            key = re.sub(r"\(.+?\)", "", issue)
            freq[key] += 1
    for issue, count in sorted(freq.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}  {issue}")

    print("\n=== PAGES WITH ISSUES ===")
    pages_with_issues = [p for p in pages if p["issues"]]
    for p in sorted(pages_with_issues, key=lambda x: (-len(x["issues"]), x["path"])):
        print(f"  {p['path']}: {', '.join(p['issues'])}")
    if not pages_with_issues:
        print("  (none)")

    print("\n=== SCHEMA TYPE COVERAGE ===")
    schema_freq = defaultdict(int)
    no_schema = []
    for p in pages:
        if not p["schema_types"]:
            no_schema.append(p["path"])
        for t in set(p["schema_types"]):
            schema_freq[t] += 1
    for t, count in sorted(schema_freq.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}  {t}")
    print(f"\nPages WITHOUT any schema: {len(no_schema)}")
    for p in no_schema:
        print(f"  - {p}")

    print("\n=== H1 SUMMARY ===")
    no_h1 = [p["path"] for p in pages if len(p["h1s"]) == 0]
    multi_h1 = [(p["path"], len(p["h1s"])) for p in pages if len(p["h1s"]) > 1]
    print(f"  No H1: {len(no_h1)}")
    for p in no_h1: print(f"    - {p}")
    print(f"  Multiple H1: {len(multi_h1)}")
    for p, n in multi_h1: print(f"    - {p}  ({n} H1s)")

    print("\n=== IMAGES ===")
    total_imgs = sum(p["imgs_total"] for p in pages)
    total_no_alt = sum(p["imgs_no_alt"] for p in pages)
    print(f"  Total images across site: {total_imgs}")
    print(f"  Images without alt: {total_no_alt}")
    worst = sorted([p for p in pages if p["imgs_no_alt"] > 0], key=lambda x: -x["imgs_no_alt"])[:15]
    for p in worst:
        print(f"    {p['path']}: {p['imgs_no_alt']}/{p['imgs_total']}")


if __name__ == "__main__":
    main()
