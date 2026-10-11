"""Consolidate the Finch Mortgages and Mukhtar Kiyani entities in structured data.

- "MortgageBroker" is not a schema.org type (schema.org/MortgageBroker is a 404;
  FinancialService's only subtypes are AccountingService, AutomatedTeller,
  BankOrCreditUnion and InsuranceAgency). 181 nodes used it alone, so Google saw an
  unknown type. They become FinancialService, in JSON-LD and footer microdata.
- Mukhtar had four identities: /#mukhtar-kiyani, /about.html#mukhtar,
  /about.html#mukhtar-kiyani and no @id. Author credit only accrues to one entity
  if every page uses the same @id.
- Finch publisher/worksFor stubs without an @id read as separate organisations;
  they now point at /#organization. The contact page's address used a different
  locality format from every other page (a NAP inconsistency).
- datePublished/dateModified are CreativeWork properties, invalid on Person and
  Organization nodes.
- Lender and weekly-report pages lacked the en-NZ / x-default hreflang pair the
  rest of the site carries.

Idempotent. Run with --apply to write; default is a dry run.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
SITE = "https://www.finchmortgages.co.nz"
ORG_ID = f"{SITE}/#organization"
PERSON_ID = f"{SITE}/#mukhtar-kiyani"
FINCH_NAMES = {"Finch Mortgages", "Finch Mortgages NZ", "Finch Mortgages Limited"}
ORG_TYPES = {"Organization", "FinancialService", "LocalBusiness"}
CANONICAL_ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "17a Marlene Ave",
    "addressLocality": "Te Atatu South",
    "addressRegion": "Auckland",
    "postalCode": "0610",
    "addressCountry": "NZ",
}

LDJSON = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
TYPE_LIST = re.compile(r'"@type":\s*\[\s*"(?:MortgageBroker|FinancialService)",\s*"(?:MortgageBroker|FinancialService)"\s*\]')
TYPE_SINGLE = re.compile(r'"@type":\s*"MortgageBroker"')
PERSON_URL = re.compile(re.escape(SITE) + r'/about\.html#mukhtar(?:-kiyani)?(?=")')
MICRODATA = 'itemtype="https://schema.org/MortgageBroker"'
CANONICAL_TAG = re.compile(r'<link (?:href="(?P<a>[^"]+)" rel="canonical"|rel="canonical" href="(?P<b>[^"]+)")\s*/?>')


def types(node):
    t = node.get("@type")
    return set(t if isinstance(t, list) else [t])


def fix_node(node, stats):
    changed = False
    ts = types(node)
    if "Person" in ts and node.get("name") == "Mukhtar Kiyani" and "@id" not in node:
        node["@id"] = PERSON_ID
        stats["person @id added"] += 1
        changed = True
    if ts & ORG_TYPES and node.get("name") in FINCH_NAMES and "@id" not in node:
        node["@id"] = ORG_ID
        stats["org @id added"] += 1
        changed = True
    if node.get("@id") == ORG_ID and isinstance(node.get("address"), dict) \
            and node["address"].get("addressLocality") == "Te Atatu South, Auckland":
        node["address"] = dict(CANONICAL_ADDRESS)
        stats["address normalised"] += 1
        changed = True
    action = node.get("potentialAction")
    if "WebSite" in ts and isinstance(action, dict) and action.get("@type") == "SearchAction":
        # The site has no search; Google also retired the sitelinks search box in 2024.
        del node["potentialAction"]
        stats["dead SearchAction removed"] += 1
        changed = True
    if ts & (ORG_TYPES | {"Person"}):
        for k in ("datePublished", "dateModified"):
            if k in node:
                del node[k]
                stats["invalid date prop removed"] += 1
                changed = True
    for v in node.values():
        changed |= walk(v, stats)
    return changed


def walk(x, stats):
    if isinstance(x, list):
        return any([walk(i, stats) for i in x])
    if isinstance(x, dict):
        return fix_node(x, stats)
    return False


def fix_jsonld(raw, stats):
    text = raw
    text, n1 = TYPE_LIST.subn('"@type": "FinancialService"', text)
    text, n2 = TYPE_SINGLE.subn('"@type": "FinancialService"', text)
    text, n3 = PERSON_URL.subn(PERSON_ID, text)
    stats["MortgageBroker type fixed"] += n1 + n2
    stats["person @id unified"] += n3
    data = json.loads(text)
    if walk(data, stats):
        return "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    return text


def add_hreflang(html, stats):
    if 'hreflang="en-NZ"' in html:
        return html
    m = CANONICAL_TAG.search(html)
    if not m:
        return html
    url = m.group("a") or m.group("b")
    tags =(f'\n<link href="{url}" hreflang="en-NZ" rel="alternate"/>'
            f'\n<link href="{url}" hreflang="x-default" rel="alternate"/>')
    stats["hreflang added"] += 1
    return html[:m.end()] + tags + html[m.end():]


def fix(html, stats):
    html = LDJSON.sub(lambda m: m.group(1) + fix_jsonld(m.group(2), stats) + m.group(3), html)
    if MICRODATA in html:
        stats["microdata type fixed"] += html.count(MICRODATA)
        html = html.replace(MICRODATA, 'itemtype="https://schema.org/FinancialService"')
    return add_hreflang(html, stats)


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    stats = dict.fromkeys(["MortgageBroker type fixed", "microdata type fixed", "person @id unified",
                           "person @id added", "org @id added", "address normalised",
                           "invalid date prop removed", "dead SearchAction removed", "hreflang added"], 0)
    changed = 0
    for f in files:
        p = ROOT / f
        src = p.read_text(encoding="utf-8")
        out = fix(src, stats)
        if out != src:
            changed += 1
            if APPLY:
                p.write_text(out, encoding="utf-8")
    for k, n in stats.items():
        print(f"{n:5}  {k}")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
