"""Remove North Shore template leftovers from the head of blog/mortgage-broker-*.html pages.

generate_city_broker_pages.py clones the North Shore page's <head>, which left every
generated city page with hreflang pointing at North Shore, Auckland geo metas, a North
Shore BlogPosting block, and FAQPage markup for FAQs that aren't on the page.
Head-only and idempotent. Run with --apply to write; default is a dry run.
"""
import html as htmllib
import json
import re
import sys
from pathlib import Path

from city_data import CITIES

ROOT = Path(__file__).parent
SITE = "https://www.finchmortgages.co.nz"
APPLY = "--apply" in sys.argv

AUK = "NZ-AUK"
REGION_CODE = {
    "nz": None,
    "auckland-city": AUK, "te-atatu": AUK, "henderson": AUK, "glenfield": AUK, "flat-bush": AUK,
    "albany": AUK, "massey": AUK, "hobsonville": AUK, "new-lynn": AUK, "mt-roskill": AUK,
    "manukau": AUK, "papakura": AUK, "botany": AUK, "howick": AUK, "takapuna": AUK,
    "pukekohe-franklin": AUK, "orewa-hibiscus-coast": AUK, "north-shore": AUK,
    "east-auckland": AUK, "south-auckland": AUK, "west-auckland": AUK,
    "wellington": "NZ-WGN", "lower-hutt": "NZ-WGN", "upper-hutt": "NZ-WGN", "porirua": "NZ-WGN",
    "kapiti-coast": "NZ-WGN", "masterton-wairarapa": "NZ-WGN",
    "christchurch": "NZ-CAN", "timaru": "NZ-CAN", "rolleston-selwyn": "NZ-CAN",
    "rangiora-kaiapoi": "NZ-CAN",
    "hamilton": "NZ-WKO", "cambridge": "NZ-WKO", "taupo": "NZ-WKO",
    "tauranga": "NZ-BOP", "rotorua": "NZ-BOP", "mount-maunganui-papamoa": "NZ-BOP",
    "dunedin": "NZ-OTA", "queenstown": "NZ-OTA",
    "napier-hawkes-bay": "NZ-HKB", "hastings": "NZ-HKB",
    "palmerston-north": "NZ-MWT", "whanganui": "NZ-MWT",
    "nelson": "NZ-NSN", "blenheim-marlborough": "NZ-MBH",
    "whangarei-northland": "NZ-NTL", "new-plymouth-taranaki": "NZ-TKI",
    "invercargill-southland": "NZ-STL", "gisborne": "NZ-GIS",
}
SKIP = {"mortgage-broker-fees-nz.html", "mortgage-broker-vs-bank-nz.html"}
GENERIC_FAQ_Q = "How does a local mortgage broker help me in my region?"
LDJSON = re.compile(r'<script type="application/ld\+json">(.*?)</script>\n?', re.S)


def place_name(fn, src):
    by_slug = {c["slug"]: c for c in CITIES}
    c = by_slug.get(fn[:-5])
    if c:
        return htmllib.unescape(c["city"])
    m = re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S)
    txt = htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(1))) if m else ""
    txt = re.sub(r"^\s*Mortgage\s*Broker\s*", "", " ".join(txt.split()), flags=re.I)
    return txt.split(":")[0].rstrip(".").strip()


def fix_head(src, fn):
    head_end = src.find("</head>")
    head, rest = src[:head_end], src[head_end:]
    url = f"{SITE}/blog/{fn}"
    slug = fn[len("mortgage-broker-"):-5]

    head = re.sub(r'<link href="[^"]*" hreflang="(en-NZ|x-default)" rel="alternate"/>',
                  lambda m: f'<link href="{url}" hreflang="{m.group(1)}" rel="alternate"/>', head)

    if slug in REGION_CODE:
        code = REGION_CODE[slug]
        place = place_name(fn, src)
        head = re.sub(r'<meta content="[^"]*" name="geo\.(position)"/>\n?', "", head)
        head = re.sub(r'<meta content="[^"]*" name="ICBM"/>\n?', "", head)
        if code:
            head = re.sub(r'<meta content="[^"]*" name="geo\.region"/>',
                          f'<meta content="{code}" name="geo.region"/>', head)
            head = re.sub(r'<meta content="[^"]*" name="geo\.placename"/>',
                          f'<meta content="{htmllib.escape(place)}, New Zealand" name="geo.placename"/>', head)
        else:
            head = re.sub(r'<meta content="[^"]*" name="geo\.(region|placename)"/>\n?', "", head)

    visible_faq = "faq-item" in rest
    blocks = [(m, json.loads(m.group(1))) for m in LDJSON.finditer(head)]
    has_article = any(d.get("@type") == "Article" for _, d in blocks)
    drop = []
    kept_faq = False
    for m, d in blocks:
        t = d.get("@type")
        if t == "BlogPosting" and has_article:
            drop.append(m)
        elif t == "FAQPage":
            qs = [q.get("name") for q in d.get("mainEntity", [])]
            if kept_faq or not visible_faq or (GENERIC_FAQ_Q in qs and GENERIC_FAQ_Q not in rest):
                drop.append(m)
            else:
                kept_faq = True
    for m in sorted(drop, key=lambda m: m.start(), reverse=True):
        head = head[:m.start()] + head[m.end():]
    return head + rest


def main():
    changed = 0
    for path in sorted((ROOT / "blog").glob("mortgage-broker-*.html")):
        if path.name in SKIP:
            continue
        src = path.read_text(encoding="utf-8")
        out = fix_head(src, path.name)
        if out != src:
            changed += 1
            if APPLY:
                path.write_text(out, encoding="utf-8")
    print(f"changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
