#!/usr/bin/env python3
"""Generate the town and region pages under locations/ from town_data.py.

Each town page combines a hand-written local note and FAQs with lending factors
chosen by tag and filled with the town's own details, so pages don't read as one
template with the name swapped. Pages are rebuilt from data on every run: edit
town_data.py, not the HTML.

Also links the new pages in from the rest of the site, idempotently:
  - FINCH-TOWNS block on each existing blog/mortgage-broker-{city} page
  - FINCH-TOWNDIR directory on locations/index.html
  - FINCH-TOWNS section in sitemap.xml

Run: python3 generate_town_pages.py   (then the post-generation fix pipeline)
"""
import datetime
import json
import math
import os
import re
from html import escape

import town_data as td
from inject_local_seo import (BIZ, SITE, FAQ_ITEM_HTML, insert_before, org_node,
                              refinance_form_block, trust_badges_block, trust_strip_block)

ROOT = os.path.dirname(os.path.abspath(__file__))
LOC_DIR = os.path.join(ROOT, "locations")
TEMPLATE = os.path.join(LOC_DIR, "refinance-hamilton.html")
PREFIX = "mortgage-broker-"
TODAY = datetime.date.today()
UPDATED = TODAY.strftime("%B %Y")
ORG_ID = f"{SITE}/#organization"
PERSON_ID = f"{SITE}/#mukhtar-kiyani"
LINK = 'style="color:var(--finch-forest);font-weight:600;text-decoration:underline;"'
EXT = 'rel="noopener" target="_blank"'

# --------------------------------------------------------------------------
# Shared copy, keyed by tag. {v} is the town's own tag detail.
# --------------------------------------------------------------------------
FACTORS = {
    "lifestyle": ("Lifestyle blocks and rural-residential land",
                  "Plenty of {town} buyers are looking at land {v}. Lenders treat a block as residential only up to a set land area and use, and look harder at farm income, tank water and septic systems, so the right lender matters."),
    "holiday": ("Holiday homes and baches",
                "Holiday homes and baches are a big part of the market {v}. Most lenders treat a second home like an investment, with a bigger deposit, and each counts short-stay income differently."),
    "commuter": ("Commuting from {town}",
                 "Many {town} households commute to {v}. Lenders assess the whole household budget, travel costs included, rather than pricing the commute itself."),
    "newbuild": ("New subdivisions and new builds",
                 "New housing is going up {v}. New builds are exempt from the Reserve Bank's LVR restrictions, so some lenders accept a smaller deposit, but the bank values the home at completion."),
    "seasonal": ("{label} incomes",
                 "A lot of local income comes from {detail}. Lenders want seasonal, contract or self-employed income shown over a full year or two, and each counts overtime, bonuses and piece rates differently."),
    "flood": ("Flood history and insurance",
              "{v} Lenders need full replacement insurance before they settle or refinance, so get an insurance indication early."),
    "quake": ("Earthquake risk and building checks",
              "{v} Lenders need full replacement insurance, and unrepaired damage or open claims can hold up an approval."),
    "coastal": ("Coastal hazards",
                "{v} These notations show on LIM reports and can affect insurance and valuations, so check them before you commit."),
    "maori_land": ("Whenua Māori and multiply-owned land",
                   "{v} Mainstream lenders generally can't lend on multiply-owned land; Kāinga Ora's Kāinga Whenua scheme is the usual route, and its lender isn't on our panel."),
    "remote": ("Lending in a smaller town",
               "Some lenders set tighter limits for smaller towns, such as a lower maximum loan-to-value ratio or a minimum property value. Others lend in {town} on standard terms, and we check which before you apply."),
    "older_homes": ("Older homes, repairs and upgrades",
                    "{v} A mortgage top-up is usually a cheaper way to fund insulation, heating or repairs than personal lending, if you repay it over a short term."),
    "investor": ("Rental investors",
                 "{v} Investors are tested against the Reserve Bank's debt-to-income settings, and lenders count only part of the rent."),
    "retirement": ("Downsizing and later-life borrowing",
                   "{town} draws plenty of retirees and downsizers. Lenders still lend to older borrowers, but want a clear plan to repay within the loan term."),
    "leasehold": ("Leasehold and freehold land",
                  "{v} Many lenders restrict leasehold security, so buying the freehold can widen your choice of lender, and a loan can often fund it."),
    "geothermal": ("Geothermal ground",
                   "{v} A notation can mean extra checks or reports, so read the LIM before you go unconditional."),
    "mining_ground": ("Old mine workings",
                      "{v} These areas show in council hazard information and on LIM reports, and lenders and insurers look at them closely."),
    "defence": ("Defence force incomes and postings",
                "{v} Lenders regard NZDF pay well, but if a posting could turn your home into a rental, we structure the loan with that in mind."),
    "heritage": ("Heritage and character homes",
                 "{v} Heritage rules can limit changes and older construction can cost more to insure, so get an insurance quote early."),
}

REFI_ANGLES = {
    "lifestyle": "Refinancing a lifestyle block means a fresh valuation, and the new lender's own land-size and water rules apply, so we check those before you apply.",
    "holiday": "Refinancing a bach or holiday home? The new lender will treat it as an investment-type loan and decide how much, if any, short-stay income to count.",
    "commuter": "If you moved here from a bigger centre, a refinance is a chance to tidy up the structure: clear any bridging finance, split your fixed terms or add an offset.",
    "newbuild": "If you built or bought new, the end of your first fixed term is often the best moment to compare lenders, because your home's value and your equity may have changed.",
    "seasonal": "Seasonal and self-employed borrowers usually refinance most smoothly straight after the year's accounts are finalised, when lenders can see the newest numbers.",
    "flood": "Before you switch lenders, confirm your insurer will keep covering the house; the new lender needs its interest noted on the policy before settlement.",
    "quake": "A refinance valuation may pick up unrepaired earthquake damage, so settle any open claims before you switch.",
    "coastal": "Switching lenders triggers a new valuation, and coastal-hazard notations can affect how the valuer and the new lender see the property.",
    "maori_land": "Refinancing a general-title home works like anywhere else; homes on multiply-owned whenua usually stay with a specialist scheme lender.",
    "remote": "Because lender appetite is narrower in smaller towns, check that the lender you're moving to will lend on {town} property at your loan-to-value ratio before you give notice to your current bank.",
    "older_homes": "A refinance with a top-up can fund insulation, heating or a re-roof at a mortgage rate rather than through a higher-cost loan.",
    "investor": "Investors often refinance to restructure: splitting loans, using interest-only periods or releasing equity for the next purchase.",
    "retirement": "Nearing retirement? A refinance is a chance to agree a repayment plan your lender will accept and to shorten the term where you can.",
    "leasehold": "If you've bought the freehold of a leasehold section, a refinance can open up lenders that wouldn't consider the property before.",
    "geothermal": "A new lender reads the LIM again when you refinance, so have any geothermal reports to hand.",
    "mining_ground": "A new lender looks at mine-workings notations again when you refinance, so confirm your insurer's position first.",
    "defence": "If a posting means your home becomes a rental, tell your lender; it can be a good moment to restructure or move to a lender that handles the switch well.",
    "heritage": "Refinancing a heritage home means a fresh valuation and confirming insurance, which can cost more for older construction.",
}

TAG_FAQS = {
    "lifestyle": ("Will a bank lend on a lifestyle block near {town}?",
                  "Usually, if the block is mainly residential. Lenders set limits on land area, farming income and services like water and wastewater, and those limits vary between lenders. Larger or income-producing blocks may need rural lending instead. Tell us the land size and how it's used and we'll tell you which lenders will look at it."),
    "holiday": ("Can I get a mortgage on a holiday home in {town}?",
                "Yes. Most lenders treat a holiday home like an investment property, so expect a bigger deposit than for your own home. If you plan to rent it out short-term, some lenders will count part of that income and some won't count it at all, so the lender choice matters."),
    "flood": ("Can I refinance a {town} home that has flooded before?",
              "Often, yes. The new lender needs full replacement insurance in place, so the first step is confirming your insurer will continue cover and that any repairs are complete. We check the LIM notes and insurance position before applying, so the switch doesn't stall at the last step."),
    "quake": ("Does earthquake risk affect getting a mortgage in {town}?",
              "Not for most homes. Lenders need full replacement insurance and a satisfactory valuation. Homes with unrepaired damage, land-damage history or foundation problems can need engineering reports first, so mention any history at the start."),
    "maori_land": ("Can I get a mortgage for a home on Māori land near {town}?",
                   "Not from most mainstream lenders, because they can't take a standard mortgage over multiply-owned Māori land. Kāinga Ora's Kāinga Whenua loans are designed for this; the scheme's lender isn't on our panel, so we'll point you there. If the house is on general title, we can compare our full panel."),
    "remote": ("Do banks lend on houses in small towns like {town}?",
               "Yes, but not all of them on the same terms. Some lenders cap the loan-to-value ratio lower for smaller towns or limit which properties they'll take as security. We check each lender's location policy for {town} before applying, so you don't use up a credit enquiry on a lender that won't help."),
    "newbuild": ("Can I buy a new build in {town} with a smaller deposit?",
                 "Possibly. New builds are exempt from the Reserve Bank's LVR restrictions, so some lenders accept less than the usual 20% deposit. You still need to meet the lender's income and debt-to-income tests, and the bank values the home at completion, so plan for a buffer."),
    "commuter": ("Can I buy in {town} before I sell my current home?",
                 "Yes. Bridging finance lets you buy in {town} before your current home sells, and some lenders will lend against a conditional sale. Bridging costs more, so we keep the bridge as short as possible and line up the end loan at the same time."),
    "seasonal": ("Will lenders count my seasonal or contract income?",
                 "Most will, but they need to see it's reliable: usually two years of history for self-employed or contract income, and payslips plus a letter for seasonal employees. Lenders differ a lot on overtime, piece rates and bonuses, so we pick the lender that counts your income most fairly."),
    "older_homes": ("Can I add renovation costs to my mortgage in {town}?",
                    "Usually, if you have the equity. A top-up for insulation, heating or repairs is normally cheaper than a personal loan. For larger renovations, lenders may want a builder's quote or an 'as if complete' valuation before releasing the funds."),
    "investor": ("Is {town} a good place for a rental investment?",
                 "We don't give property investment advice, but we can show you how lenders will assess a {town} rental: how much of the rent they count, how the debt-to-income limits apply, and what deposit you'll need. That tells you whether the numbers work before you buy."),
    "retirement": ("Can I get a mortgage in my 60s in {town}?",
                   "Yes, many lenders will lend to older borrowers. They'll ask how the loan will be repaid within the term, from income, savings or a planned downsize, and may offer a shorter term. A smaller loan with a clear exit is usually approved more easily."),
    "geothermal": ("Does geothermal activity affect buying in {town}?",
                   "It can add steps. If the LIM shows a geothermal hazard note, lenders and insurers may ask questions or want a report. Most homes are financed without problems, but read the LIM early."),
    "coastal": ("Will a lender finance a beachfront home in {town}?",
                "Usually, but coastal-hazard notations can narrow the lender list and affect insurance. We check the LIM and insurance position first, then approach lenders comfortable with the property."),
    "heritage": ("Can I get a mortgage on a heritage home in {town}?",
                 "Usually, yes. Lenders lend on older and heritage homes; they'll want a satisfactory valuation and full replacement insurance, which can cost more for heritage buildings. Get an insurance quote before you go unconditional."),
}

GENERIC_FAQS = [
    ("Do I need to meet a mortgage broker in person in {town}?",
     "No. We work with {town} clients by phone, video call and secure online document upload. Valuations are done by registered valuers who cover the area, and you can use any local lawyer for the legal work."),
]

REFI_STEPS = [
    ("Start four to six weeks before your fixed term ends",
     "There's no break fee at the end of a fixed term, so that's the cleanest moment to switch or renegotiate."),
    ("Know your break fee if you're mid-term",
     "Your bank can quote it. We only recommend breaking a fixed rate when the saving clearly beats the cost."),
    ("Check for a cashback clawback",
     "If your current lender paid you a cash contribution in the last few years, some or all of it may have to be repaid if you leave."),
    ("Count the switching costs",
     "Expect legal fees for the new mortgage and sometimes a valuation. Some lenders contribute towards these."),
    ("Compare your own bank's offer too",
     "Sometimes the best result is a better deal from the lender you're already with, and we'll tell you if that's the case."),
]

PROPERTY_WORDS = [("newbuild", "new builds"), ("lifestyle", "lifestyle blocks"),
                  ("holiday", "holiday homes and baches"), ("older_homes", "older villas and cottages"),
                  ("coastal", "coastal homes"), ("heritage", "character and heritage homes"),
                  ("investor", "rental properties"), ("leasehold", "leasehold and freehold sections"),
                  ("maori_land", "homes on whenua Māori")]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def tag_text(template, town, tags, key):
    v = tags.get(key)
    if key == "seasonal":
        label, detail = v
        return template.format(town=town["prose"], label=label, detail=detail)
    return template.format(town=town["prose"], v=v if isinstance(v, str) else "")


def factors_for(town, limit=4):
    out = []
    for key in town["tags"]:
        if key in FACTORS and len(out) < limit:
            h, p = FACTORS[key]
            out.append((tag_text(h, town, town["tags"], key), tag_text(p, town, town["tags"], key)))
    return out


def faqs_for(town):
    local = [(f[0], f[1]) for f in town["faqs"]]
    covered = {f[2] for f in town["faqs"] if len(f) > 2}
    options = [k for k in town["tags"] if k in TAG_FAQS and k not in covered]
    tagged = []
    if options:
        # Towns with the same tags would otherwise get the same FAQ; spread the choice.
        key = options[sum(map(ord, town["slug"])) % len(options)]
        q, a = TAG_FAQS[key]
        tagged.append((tag_text(q, town, town["tags"], key), tag_text(a, town, town["tags"], key)))
    generic = [(q.format(town=town["prose"]), a.format(town=town["prose"])) for q, a in GENERIC_FAQS]
    return (local + tagged + generic)[:7]


def refi_angles(town, limit=2):
    out = []
    for key in town["tags"]:
        if key in REFI_ANGLES and len(out) < limit:
            out.append(tag_text(REFI_ANGLES[key], town, town["tags"], key))
    return out


def property_mix(town):
    words = ["town sections"] + [w for k, w in PROPERTY_WORDS if k in town["tags"]]
    return ", ".join(words[:-1]) + " and " + words[-1] if len(words) > 1 else words[0]


def district_name(town):
    return td.COUNCILS[town["council"]][0].replace(" Council", "")


def district_label(town):
    return town.get("district") or district_name(town)


def km(a, b):
    la1, lo1 = map(float, td.COORDS[a])
    la2, lo2 = map(float, td.COORDS[b])
    p1, p2 = math.radians(la1), math.radians(la2)
    dphi, dl = math.radians(la2 - la1), math.radians(lo2 - lo1)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def nearest(town, n=6):
    others = [t for t in td.TOWNS if t["slug"] != town["slug"] and t["region"] != "chatham-islands"]
    return sorted(others, key=lambda t: km(town["slug"], t["slug"]))[:n]


def title_for(name, kind="town"):
    base = f"Mortgage Broker {name}"
    suffixes = [" | Refinance & Home Loans | Finch", " | Refinance & Loans | Finch",
                " | Refinancing | Finch", " | Finch Mortgages", " | Finch"]
    for s in suffixes:
        if len(base + s) <= 60:
            return base + s
    return base


def desc_for(town):
    mix = [w for k, w in PROPERTY_WORDS if k in town["tags"]]
    tail = " Compare 23 lenders by phone or video, with no fee on residential home loans."
    for n in (2, 1, 0):
        items = ["refinancing", "home loans"] + mix[:n]
        body = f"Mortgage broker for {town['prose']}: " + ", ".join(items[:-1]) + " and " + items[-1] + "."
        if len(body + tail) <= 158:
            break
    return body + tail


def faq_html(faqs):
    return "\n".join(FAQ_ITEM_HTML.format(q=escape(q, False), a=escape(a, False)) for q, a in faqs)


def card(h, p):
    return ('<div style="background:white;border-radius:1rem;padding:1.5rem;border:1px solid rgba(181,206,176,0.4);">'
            f'<h3 style="font-size:1.05rem;margin-bottom:0.75rem;color:var(--finch-forest);">{escape(h, False)}</h3>'
            f'<p style="font-size:0.95rem;line-height:1.75;color:var(--neutral-medGray);margin:0;">{escape(p, False)}</p></div>')


def chip(href, text):
    return (f'<a href="{href}" style="display:inline-block;background:white;border:1px solid rgba(181,206,176,0.5);'
            f'border-radius:999px;padding:0.5rem 1rem;font-size:0.85rem;font-weight:600;color:var(--finch-forest);'
            f'text-decoration:none;">{escape(text, False)}</a>')


def region_link(region_key):
    """(href, label) for the best page covering a region, relative to locations/."""
    r = td.REGIONS[region_key]
    if r["hub_page"]:
        return f"{r['hub_page']}.html", f"Mortgage broker {r['name']}"
    return None


def adviser_block(place):
    return f"""<section style="padding:3.5rem 0;background:white;border-top:1px solid rgba(180,178,169,0.15);">
<div class="container" style="max-width:900px;">
<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;">
<img src="../images/mukhtar-kiyani.webp" alt="Mukhtar Kiyani, Director and Financial Adviser at Finch Mortgages" width="120" height="120" loading="lazy" decoding="async" style="width:120px;height:120px;border-radius:50%;object-fit:cover;object-position:top;flex-shrink:0;"/>
<div style="flex:1;min-width:240px;">
<p style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;color:var(--finch-forest);margin:0 0 0.35rem;">Your adviser</p>
<h2 style="font-size:1.5rem;margin:0 0 0.5rem;">Mukhtar Kiyani</h2>
<p style="color:var(--neutral-medGray);line-height:1.75;margin:0 0 0.75rem;">Director and Financial Adviser, with over 15 years of lending experience across ASB, Westpac and BNZ. Mukhtar works with {escape(place, False)} clients by phone and video, from first call to settlement.</p>
<p style="margin:0;font-size:0.9rem;"><a href="../about.html" {LINK}>About Mukhtar</a> · <a href="../disclosure.html" {LINK}>Disclosure statement</a> · <a href="tel:{BIZ['phone_e164']}" data-cta="adviser-call" {LINK}>Call {BIZ['phone_display']}</a></p>
</div>
</div>
</div>
</section>"""


# --------------------------------------------------------------------------
# Page shell: head, nav and footer come from an existing location page.
# --------------------------------------------------------------------------

def load_shell():
    s = open(TEMPLATE, encoding="utf-8").read()
    head = s[: s.index("</head>")]
    body_start = s[s.index("</head>"): s.index("<main")]
    tail = s[s.index("</main>"):]
    tail = re.sub(r"<!-- INTERNAL-LINKS:START -->.*?<!-- INTERNAL-LINKS:END -->\n?", "", tail, flags=re.S)
    return head, body_start, tail


def sub_once(pattern, repl, text, label):
    new, n = re.subn(pattern, lambda _: repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"template changed: could not replace {label}")
    return new


def build_head(head, title, desc, url, geo, schema):
    t, d = escape(title), escape(desc)
    head = sub_once(r"<title>.*?</title>", f"<title>{t}</title>", head, "title")
    head = sub_once(r'<meta content="[^"]*" name="description"/>', f'<meta content="{d}" name="description"/>', head, "description")
    head = sub_once(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{url}" rel="canonical"/>', head, "canonical")
    head = sub_once(r'<link href="[^"]*" hreflang="en-NZ" rel="alternate"/>', f'<link href="{url}" hreflang="en-NZ" rel="alternate"/>', head, "hreflang en-NZ")
    head = sub_once(r'<link href="[^"]*" hreflang="x-default" rel="alternate"/>', f'<link href="{url}" hreflang="x-default" rel="alternate"/>', head, "hreflang x-default")
    head = sub_once(r'<meta content="[^"]*" property="og:type"/>', '<meta content="website" property="og:type"/>', head, "og:type")
    head = sub_once(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{t}" property="og:title"/>', head, "og:title")
    head = sub_once(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{d}" property="og:description"/>', head, "og:description")
    head = sub_once(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', head, "og:url")
    head = sub_once(r'<meta content="[^"]*" name="twitter:title"/>', f'<meta content="{t}" name="twitter:title"/>', head, "twitter:title")
    head = sub_once(r'<meta content="[^"]*" name="twitter:description"/>', f'<meta content="{d}" name="twitter:description"/>', head, "twitter:description")
    head = sub_once(r"<!-- FINCH-GEO:START -->.*?<!-- FINCH-GEO:END -->",
                    f"<!-- FINCH-GEO:START -->\n{geo}\n<!-- FINCH-GEO:END -->", head, "geo")
    head = sub_once(r"<!-- FINCH-SCHEMA:START -->.*?<!-- FINCH-SCHEMA:END -->",
                    f"<!-- FINCH-SCHEMA:START -->\n{schema}\n<!-- FINCH-SCHEMA:END -->", head, "schema")
    return head


def geo_meta(iso, place, lat, lng, city):
    lines = [f'<meta content="{iso}" name="geo.region"/>',
             f'<meta content="{escape(place)}, New Zealand" name="geo.placename"/>']
    if lat:
        lines += [f'<meta content="{lat};{lng}" name="geo.position"/>', f'<meta content="{lat}, {lng}" name="ICBM"/>']
    lines += ['<meta content="Mortgage Broker" name="finch:service"/>', f'<meta content="{escape(city)}" name="finch:city"/>']
    return "\n".join(lines)


def ld(graph):
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
            + "</script>")


def person_node():
    return {"@type": "Person", "@id": PERSON_ID, "name": "Mukhtar Kiyani",
            "jobTitle": "Director & Financial Adviser", "url": f"{SITE}/about.html",
            "image": f"{SITE}/images/mukhtar-kiyani.webp", "worksFor": {"@id": ORG_ID}}


def page_nodes(url, title, desc, about_id, crumbs, faqs):
    nodes = [{
        "@type": "BreadcrumbList", "@id": f"{url}#breadcrumb",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                            for i, (n, u) in enumerate(crumbs)],
    }, {
        "@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title,
        "description": desc, "inLanguage": "en-NZ", "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": about_id}, "breadcrumb": {"@id": f"{url}#breadcrumb"},
        "publisher": {"@id": ORG_ID}, "dateModified": TODAY.isoformat(),
    }]
    if faqs:
        nodes.append({"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    return nodes


def channel(url):
    return {"@type": "ServiceChannel", "serviceUrl": url,
            "servicePhone": {"@type": "ContactPoint", "telephone": BIZ["phone_e164"],
                             "contactType": "sales", "areaServed": "NZ", "availableLanguage": "en"}}


OFFER = {"@type": "Offer", "price": "0", "priceCurrency": "NZD",
         "description": "No broker fee on residential home loans; the lender pays our commission on settlement."}


# --------------------------------------------------------------------------
# Town page
# --------------------------------------------------------------------------

def town_page(town, shell):
    head, body_start, tail = shell
    name, slug, prose = town["name"], town["slug"], town["prose"]
    region = td.REGIONS[town["region"]]
    council_name, council_url = td.COUNCILS[town["council"]]
    district = district_label(town)
    lat, lng = td.COORDS[slug]
    fn = f"{PREFIX}{slug}.html"
    url = f"{SITE}/locations/{fn}"
    title, desc = title_for(name), desc_for(town)
    factors = factors_for(town)
    faqs = faqs_for(town)
    hub = td.CITY_PAGES.get(town["hub"]) if town["hub"] else None
    reg = region_link(town["region"])

    # Breadcrumb: Home > Locations > region page (if any) > town
    crumbs = [("Home", f"{SITE}/"), ("Locations", f"{SITE}/locations/index.html")]
    crumb_html = '<a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="index.html">Locations</a>'
    if reg:
        crumbs.append((region["name"], f"{SITE}/locations/{reg[0]}"))
        crumb_html += f'<span class="breadcrumb-sep">/</span><a href="{reg[0]}">{escape(region["name"], False)}</a>'
    elif hub:
        crumbs.append((hub[0], f"{SITE}/blog/mortgage-broker-{town['hub']}.html"))
        crumb_html += f'<span class="breadcrumb-sep">/</span><a href="../blog/mortgage-broker-{town["hub"]}.html">{escape(hub[0], False)}</a>'
    crumbs.append((name, url))
    crumb_html += f'<span class="breadcrumb-sep">/</span><span>{escape(name, False)}</span>'

    service = {
        "@type": "Service", "@id": f"{url}#service", "name": f"Mortgage broker services in {name}",
        "serviceType": "Mortgage brokerage", "description": desc, "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "City", "name": name,
                       "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
                       "containedInPlace": {"@type": "AdministrativeArea", "name": district_name(town),
                                            "containedInPlace": {"@type": "AdministrativeArea", "name": region["name"]}}},
        "availableChannel": channel(url), "offers": OFFER,
    }
    schema = ld([org_node(), person_node(), service] + page_nodes(url, title, desc, f"{url}#service", crumbs, faqs))
    geo = geo_meta(region["iso"], name, lat, lng, name)

    points = "".join(f"<li>{escape(h, False)}</li>" for h, _ in factors[:3])
    note = "".join(f'<p style="color:var(--neutral-medGray);line-height:1.85;margin:0 0 1.1rem;">{escape(p, False)}</p>'
                   for p in town["note"])
    factor_cards = "\n".join(card(h, p) for h, p in factors)
    angles = "".join(f'<li style="margin-bottom:0.65rem;">{escape(a, False)}</li>' for a in refi_angles(town))

    glance = [("Region", (f'<a href="{reg[0]}" {LINK}>{escape(region["name"], False)}</a>' if reg
                          else escape(region["name"], False))),
              ("District", f'<a href="{council_url}" {EXT} {LINK}>{escape(council_name, False)}</a>'),
              ("Areas around {0}".format(escape(name, False)), escape(town["near"], False)),
              ("Property you'll find here", escape(property_mix(town), False)),
              ("How we work with you", "Phone, video call and secure online document upload. No need to travel.")]
    if hub:
        glance.insert(2, ("Nearest Finch city guide",
                          f'<a href="../blog/mortgage-broker-{town["hub"]}.html" {LINK}>Mortgage broker {escape(hub[0], False)}</a>'))
    near = nearest(town)
    if near:
        glance.append(("Closest towns we cover",
                       escape(", ".join(f"{t['name']} (about {round(km(slug, t['slug']))} km)" for t in near[:3]), False)))
    glance_rows = "".join(
        f'<tr><th scope="row" style="text-align:left;padding:0.8rem 1rem;border-bottom:1px solid rgba(180,178,169,0.25);'
        f'width:34%;font-size:0.9rem;color:var(--neutral-black);vertical-align:top;">{k}</th>'
        f'<td style="padding:0.8rem 1rem;border-bottom:1px solid rgba(180,178,169,0.25);font-size:0.92rem;'
        f'color:var(--neutral-medGray);line-height:1.6;">{v}</td></tr>' for k, v in glance)

    checks = [(council_url, f"{council_name}: LIM reports, the district plan and hazard maps")]
    if region["rc"]:
        checks.append((region["rc"][1], f"{region['rc'][0]}: regional flood and natural hazard information"))
    checks.append(("https://www.naturalhazards.govt.nz/", "Natural Hazards Commission: what NHCover includes and how claims work"))
    if "investor" in town["tags"]:
        checks.append(("https://www.tenancy.govt.nz/healthy-homes/", "Tenancy Services: the Healthy Homes standards for rentals"))
    if "maori_land" in town["tags"]:
        checks.append(("https://www.kaingaora.govt.nz/home-ownership/kainga-whenua/", "Kāinga Ora: Kāinga Whenua loans for building on Māori land"))
    check_items = "".join(f'<li style="margin-bottom:0.6rem;"><a href="{u}" {EXT} {LINK}>{escape(t, False)}</a></li>'
                          for u, t in checks)

    near_chips = [chip(f"{PREFIX}{t['slug']}.html", f"Mortgage broker {t['name']}") for t in near]
    up_chips = []
    if reg:
        up_chips.append(chip(reg[0], f"All {region['name']} towns"))
    if hub:
        up_chips.append(chip(f"../blog/mortgage-broker-{town['hub']}.html", f"Mortgage broker {hub[0]}"))
    up_chips.append(chip("index.html", "Every NZ location we cover"))

    form = refinance_form_block(f"See what refinancing could save you in {escape(prose, False)}",
                                "Tell us when your fixed rate ends and roughly what you owe. We'll compare your bank's offer with other lenders and show you the numbers, including break fees and any cashback.",
                                name, f"town-{slug}")

    main = f"""<main style="padding-top:80px;">
  <!-- Hero -->
  <section class="container page-hero" style="padding-top:4rem;padding-bottom:3rem;">
    <div style="max-width:820px;">
      <nav class="breadcrumb">{crumb_html}</nav>
      <div class="page-hero-tag">{escape(district, False)} · {escape(region['name'], False)}</div>
      <h1>Mortgage Broker<br/><em style="font-style:italic;color:var(--finch-forest);">{escape(name, False)}.</em></h1>
      <p style="font-size:1.1rem;line-height:1.7;color:var(--neutral-medGray);margin-top:0.75rem;">Refinancing, first homes and home loans for {escape(prose, False)}, {escape(town['near'], False)}, compared across 23 lenders by phone, video or email.</p>
      <p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: {UPDATED}</p>
      <div class="answer-first" style="margin-top:1.25rem;padding:1.1rem 1.25rem;border-left:4px solid var(--finch-forest);background:var(--finch-mist);border-radius:0.75rem;"><p style="margin:0 0 0.6rem;line-height:1.7;"><strong>Mortgage broker in {escape(prose, False)}, in short:</strong> we compare 23 lenders for {escape(name, False)} buyers and homeowners by phone and video, with no fee on residential home loans.</p><p style="margin:0 0 0.35rem;font-weight:700;font-size:0.9rem;color:var(--finch-forest);">What shapes lending in {escape(prose, False)}</p><ul style="margin:0;padding-left:1.2rem;list-style:disc;line-height:1.7;">{points}</ul></div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
        <a class="btn-primary" href="#enquire" data-cta="town-hero-refi">Check my refinance options</a>
        <a class="btn-secondary" href="tel:{BIZ['phone_e164']}" data-cta="town-hero-call">Call {BIZ['phone_display']}</a>
      </div>
    </div>
  </section>

{trust_badges_block()}

  <section style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:820px;">
      <div class="section-label"><span>Local knowledge</span></div>
      <h2 class="section-heading" style="margin-bottom:1.25rem;">Buying and refinancing in {escape(prose, False)}</h2>
      {note}
    </div>
  </section>

  <section style="padding:4rem 0;background:var(--finch-mist);">
    <div class="container" style="max-width:900px;">
      <h2 class="section-heading" style="margin-bottom:1rem;">What lenders look at in {escape(prose, False)}</h2>
      <p style="color:var(--neutral-medGray);line-height:1.8;margin-bottom:2rem;">The local details most likely to decide which lender says yes.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;">
{factor_cards}
      </div>
    </div>
  </section>

  <section style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:820px;">
      <h2 class="section-heading" style="margin-bottom:1rem;">Refinancing your {escape(name, False)} home</h2>
      <ul style="padding-left:1.25rem;list-style:disc;color:var(--neutral-medGray);line-height:1.75;margin-bottom:1.25rem;">{angles}</ul>
      <p style="margin:0;color:var(--neutral-medGray);line-height:1.8;">The usual checks still apply: your fixed-term end date, any break fee and any cashback clawback. The <a href="../guides/refinance-guide.html" {LINK}>NZ refinance guide</a> walks through them, and the <a href="../calculators/refinance-savings.html" {LINK}>refinance savings calculator</a> shows what a lower rate is worth.</p>
    </div>
  </section>

  <section style="padding:4rem 0;background:var(--finch-mist);">
    <div class="container" style="max-width:900px;">
      <h2 class="section-heading" style="margin-bottom:1.5rem;">{escape(name, False)} at a glance</h2>
      <div style="background:white;border-radius:1rem;overflow:hidden;border:1px solid rgba(181,206,176,0.4);">
        <table style="width:100%;border-collapse:collapse;">{glance_rows}</table>
      </div>
      <h3 style="font-size:1.1rem;color:var(--finch-forest);margin:2rem 0 0.75rem;">Before you buy or switch: local checks</h3>
      <ul style="padding-left:1.25rem;list-style:disc;line-height:1.7;margin:0;">{check_items}</ul>
    </div>
  </section>

  <section style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:800px;">
      <h2 id="faq-section" style="font-family:var(--font-display);font-size:2rem;color:var(--neutral-black);margin-bottom:1.5rem;text-align:center;">Mortgage questions from {escape(prose, False)}</h2>
      <div class="faq-accordion" style="display:flex;flex-direction:column;gap:1rem;">
{faq_html(faqs)}
      </div>
    </div>
  </section>

<!-- FINCH-LEADFORM:START -->
{form}
<!-- FINCH-LEADFORM:END -->

{adviser_block(name)}

  <section style="padding:3.5rem 0;background:var(--finch-mist);">
    <div class="container">
      <h2 style="font-family:var(--font-display);font-size:clamp(1.4rem,3vw,1.8rem);margin-bottom:0.5rem;">Nearby towns we also cover</h2>
      <p style="color:var(--neutral-medGray);max-width:680px;line-height:1.7;margin-bottom:1.25rem;">Closest to {escape(prose, False)}:</p>
      <div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1rem;">{''.join(near_chips)}</div>
      <div style="display:flex;flex-wrap:wrap;gap:0.6rem;">{''.join(up_chips)}</div>
    </div>
  </section>
"""
    page = build_head(head, title, desc, url, geo, schema) + body_start + main + tail
    return fn, page, title, desc


# --------------------------------------------------------------------------
# Region hub page
# --------------------------------------------------------------------------

def region_page(key, shell):
    head, body_start, tail = shell
    r, hub = td.REGIONS[key], td.REGION_HUBS[key]
    name = r["name"]
    fn = f"{r['hub_page']}.html"
    url = f"{SITE}/locations/{fn}"
    towns = [t for t in td.TOWNS if t["region"] == key]
    cities = [(k, v[0]) for k, v in td.CITY_PAGES.items() if v[1] == key]
    title, desc = hub["title"], hub["desc"]
    faqs = hub["faqs"]
    crumbs = [("Home", f"{SITE}/"), ("Locations", f"{SITE}/locations/index.html"), (name, url)]

    service = {
        "@type": "Service", "@id": f"{url}#service", "name": f"Mortgage broker services in {name}",
        "serviceType": "Mortgage brokerage", "description": desc, "provider": {"@id": ORG_ID},
        "areaServed": [{"@type": "AdministrativeArea", "name": name}]
                      + [{"@type": "City", "name": t["name"]} for t in towns],
        "availableChannel": channel(url), "offers": OFFER,
    }
    itemlist = {"@type": "ItemList", "@id": f"{url}#towns", "name": f"Towns we cover in {name}",
                "numberOfItems": len(towns),
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"Mortgage broker in {t['name']}",
                                     "url": f"{SITE}/locations/{PREFIX}{t['slug']}.html"} for i, t in enumerate(towns)]}
    schema = ld([org_node(), service, itemlist] + page_nodes(url, title, desc, f"{url}#service", crumbs, faqs))
    geo = geo_meta(r["iso"], name, None, None, name)

    intro = "".join(f'<p style="color:var(--neutral-medGray);line-height:1.85;margin:0 0 1.1rem;">{escape(p, False)}</p>'
                    for p in hub["intro"])
    point_cards = "\n".join(card(h, p) for h, p in hub["points"])
    town_cards = "\n".join(
        f'<a href="{PREFIX}{t["slug"]}.html" style="display:block;background:white;border-radius:1rem;padding:1.1rem 1.25rem;'
        f'border:1px solid rgba(181,206,176,0.45);text-decoration:none;color:var(--neutral-black);">'
        f'<strong style="display:block;color:var(--finch-forest);margin-bottom:0.3rem;">Mortgage broker {escape(t["name"], False)}</strong>'
        f'<span style="font-size:0.85rem;color:var(--neutral-medGray);line-height:1.55;">'
        f'{escape(" · ".join(h for h, _ in factors_for(t, 2)), False)}</span></a>' for t in towns)
    city_chips = "".join(chip(f"../blog/mortgage-broker-{k}.html", f"Mortgage broker {v}") for k, v in cities)
    other = [(k, v) for k, v in td.REGIONS.items() if v["hub_page"] and k != key]
    other_chips = "".join(chip(f"{v['hub_page']}.html", f"Mortgage broker {v['name']}") for k, v in other)
    steps = "".join(f'<li style="margin-bottom:0.65rem;"><strong>{escape(h, False)}.</strong> {escape(p, False)}</li>'
                    for h, p in REFI_STEPS)
    points = "".join(f"<li>{escape(h, False)}</li>" for h, _ in hub["points"][:3])
    form = refinance_form_block(f"See what refinancing could save you in {escape(name, False)}",
                                "Tell us when your fixed rate ends and roughly what you owe. We'll compare your bank's offer with other lenders and show you the numbers, including break fees and any cashback.",
                                name, f"region-{key}")

    main = f"""<main style="padding-top:80px;">
  <!-- Hero -->
  <section class="container page-hero" style="padding-top:4rem;padding-bottom:3rem;">
    <div style="max-width:820px;">
      <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="index.html">Locations</a><span class="breadcrumb-sep">/</span><span>{escape(name, False)}</span></nav>
      <div class="page-hero-tag">Local NZ coverage · {len(towns)} {escape(name, False)} towns</div>
      <h1>Mortgage Broker<br/><em style="font-style:italic;color:var(--finch-forest);">{escape(name, False)}.</em></h1>
      <p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: {UPDATED}</p>
      <div class="answer-first" style="margin-top:1.25rem;padding:1.1rem 1.25rem;border-left:4px solid var(--finch-forest);background:var(--finch-mist);border-radius:0.75rem;"><p style="margin:0 0 0.6rem;line-height:1.7;"><strong>Mortgage broker in {escape(name, False)}, in short:</strong> Finch is an independent mortgage broker based in Te Atatu South, Auckland, working with clients across {escape(name, False)} by phone, video and secure online document upload. We compare 23 lenders, and for residential home loans our advice is free because the lender pays us when your loan settles.</p><p style="margin:0 0 0.35rem;font-weight:700;font-size:0.9rem;color:var(--finch-forest);">What matters locally in {escape(name, False)}</p><ul style="margin:0;padding-left:1.2rem;list-style:disc;line-height:1.7;">{points}</ul></div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
        <a class="btn-primary" href="#enquire" data-cta="region-hero-refi">Check my refinance options</a>
        <a class="btn-secondary" href="#towns">Find your town</a>
      </div>
    </div>
  </section>

{trust_strip_block()}

  <section style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:820px;">
      <div class="section-label"><span>Local knowledge</span></div>
      <h2 class="section-heading" style="margin-bottom:1.25rem;">Home loans and refinancing across {escape(name, False)}</h2>
      {intro}
    </div>
  </section>

  <section style="padding:4rem 0;background:var(--finch-mist);">
    <div class="container" style="max-width:900px;">
      <h2 class="section-heading" style="margin-bottom:2rem;">What lenders look at in {escape(name, False)}</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;">
{point_cards}
      </div>
    </div>
  </section>

  <section id="towns" style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:1100px;">
      <h2 class="section-heading" style="margin-bottom:1rem;">Towns we cover in {escape(name, False)}</h2>
      <p style="color:var(--neutral-medGray);line-height:1.8;margin-bottom:2rem;">Each town page covers the local lending details that matter there, from property types to incomes and hazards.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem;margin-bottom:2rem;">
{town_cards}
      </div>
      {('<h3 style="font-size:1.1rem;color:var(--finch-forest);margin-bottom:0.75rem;">City guides in ' + escape(name, False) + '</h3><div style="display:flex;flex-wrap:wrap;gap:0.6rem;">' + city_chips + '</div>') if city_chips else ''}
    </div>
  </section>

  <section style="padding:4rem 0;background:var(--finch-mist);">
    <div class="container" style="max-width:820px;">
      <h2 class="section-heading" style="margin-bottom:1rem;">Refinancing in {escape(name, False)}: five checks first</h2>
      <ol style="padding-left:1.25rem;color:var(--neutral-medGray);line-height:1.75;margin-bottom:1.25rem;">{steps}</ol>
      <p style="margin:0;color:var(--neutral-medGray);line-height:1.8;">Run your numbers in the <a href="../calculators/refinance-savings.html" {LINK}>refinance savings calculator</a> or read the <a href="../guides/refinance-guide.html" {LINK}>NZ refinance guide</a>.</p>
    </div>
  </section>

  <section style="padding:4rem 0;background:white;">
    <div class="container" style="max-width:800px;">
      <h2 id="faq-section" style="font-family:var(--font-display);font-size:2rem;color:var(--neutral-black);margin-bottom:1.5rem;text-align:center;">{escape(name, False)} mortgage questions</h2>
      <div class="faq-accordion" style="display:flex;flex-direction:column;gap:1rem;">
{faq_html(faqs)}
      </div>
    </div>
  </section>

<!-- FINCH-LEADFORM:START -->
{form}
<!-- FINCH-LEADFORM:END -->

{adviser_block(name)}

  <section style="padding:3.5rem 0;background:var(--finch-mist);">
    <div class="container">
      <h2 style="font-family:var(--font-display);font-size:clamp(1.4rem,3vw,1.8rem);margin-bottom:1.25rem;">Other regions we cover</h2>
      <div style="display:flex;flex-wrap:wrap;gap:0.6rem;">{other_chips}{chip("index.html", "Every NZ location we cover")}</div>
    </div>
  </section>
"""
    page = build_head(head, title, desc, url, geo, schema) + body_start + main + tail
    return fn, page, title, desc


# --------------------------------------------------------------------------
# Links from existing pages, and the sitemap
# --------------------------------------------------------------------------

def towns_block_for_city(key):
    label, region_key = td.CITY_PAGES[key]
    towns = [t for t in td.TOWNS if t["hub"] == key]
    if not towns:
        return None
    reg = region_link(region_key)
    chips = "".join(chip(f"../locations/{PREFIX}{t['slug']}.html", f"Mortgage broker {t['name']}") for t in towns)
    if reg:
        chips += chip(f"../locations/{reg[0]}", f"All {td.REGIONS[region_key]['name']} towns")
    return f"""<section style="padding:3.5rem 0;background:white;border-top:1px solid rgba(180,178,169,0.15);">
<div class="container">
<h2 style="font-family:var(--font-display);font-size:clamp(1.4rem,3vw,1.8rem);margin-bottom:0.5rem;">Towns we also cover near {escape(label, False)}</h2>
<p style="color:var(--neutral-medGray);max-width:680px;line-height:1.7;margin-bottom:1.25rem;">Local guides with the lending details that matter in each town.</p>
<div style="display:flex;flex-wrap:wrap;gap:0.6rem;">{chips}</div>
</div>
</section>"""


def pass_city_pages():
    count = 0
    for key in td.CITY_PAGES:
        fp = os.path.join(ROOT, "blog", f"mortgage-broker-{key}.html")
        block = towns_block_for_city(key)
        if not block or not os.path.exists(fp):
            continue
        html = open(fp, encoding="utf-8").read()
        anchor = "<!-- INTERNAL-LINKS:START -->" if "<!-- INTERNAL-LINKS:START -->" in html else '<footer class="site-footer">'
        new, did = insert_before(html, anchor, "TOWNS", block)
        if did:
            open(fp, "w", encoding="utf-8").write(new)
            count += 1
    return count


def directory_block():
    groups = []
    for key in td.REGION_ORDER:
        r = td.REGIONS[key]
        towns = [t for t in td.TOWNS if t["region"] == key]
        cities = [(k, v[0]) for k, v in td.CITY_PAGES.items() if v[1] == key]
        chips = [chip(f"../blog/mortgage-broker-{k}.html", v) for k, v in cities]
        chips += [chip(f"{PREFIX}{t['slug']}.html", t["name"]) for t in towns]
        heading = escape(r["name"], False)
        if r["hub_page"]:
            heading = f'<a href="{r["hub_page"]}.html" style="color:var(--finch-forest);">{heading} →</a>'
        groups.append(f'<div style="margin-bottom:1.75rem;"><h3 style="font-size:1.05rem;margin-bottom:0.6rem;">{heading}</h3>'
                      f'<div style="display:flex;flex-wrap:wrap;gap:0.5rem;">{"".join(chips)}</div></div>')
    return f"""<section id="all-towns" style="padding:4rem 0;background:white;">
<div class="container">
<h2 style="font-family:var(--font-display);font-size:clamp(1.6rem,3vw,2.2rem);margin-bottom:0.5rem;">Find a mortgage broker in your town</h2>
<p style="color:var(--neutral-medGray);max-width:720px;line-height:1.7;margin-bottom:2rem;">Every city and town we have a local guide for, by region. We work with clients anywhere in New Zealand by phone, video and secure online document upload.</p>
{''.join(groups)}
</div>
</section>"""


def pass_locations_hub():
    fp = os.path.join(LOC_DIR, "index.html")
    html = open(fp, encoding="utf-8").read()
    anchor = "<!-- INTERNAL-LINKS:START -->" if "<!-- INTERNAL-LINKS:START -->" in html else '<footer class="site-footer">'
    new, did = insert_before(html, anchor, "TOWNDIR", directory_block())
    if did:
        open(fp, "w", encoding="utf-8").write(new)
    return did


def pass_sitemap(files):
    fp = os.path.join(ROOT, "sitemap.xml")
    xml = open(fp, encoding="utf-8").read()
    entries = []
    for fn, priority in files:
        entries.append(f"  <url>\n    <loc>{SITE}/locations/{fn}</loc>\n    <lastmod>{TODAY.isoformat()}</lastmod>\n"
                       f"    <changefreq>monthly</changefreq>\n    <priority>{priority}</priority>\n  </url>")
    block = "\n".join(entries)
    start, end = "<!-- FINCH-TOWNS:START -->", "<!-- FINCH-TOWNS:END -->"
    wrapped = f"  {start}\n{block}\n  {end}"
    if start in xml:
        new = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: f"{start}\n{block}\n  {end}", xml, flags=re.S)
    else:
        new = xml.replace("</urlset>", wrapped + "\n</urlset>", 1)
    if new != xml:
        open(fp, "w", encoding="utf-8").write(new)
    return len(entries)


def main():
    shell = load_shell()
    written = []
    for key, r in td.REGIONS.items():
        if r["hub_page"]:
            fn, page, *_ = region_page(key, shell)
            open(os.path.join(LOC_DIR, fn), "w", encoding="utf-8").write(page)
            written.append((fn, "0.7"))
    for town in td.TOWNS:
        fn, page, *_ = town_page(town, shell)
        open(os.path.join(LOC_DIR, fn), "w", encoding="utf-8").write(page)
        written.append((fn, "0.6"))
    print(f"region hub pages ....... {sum(1 for f, p in written if p == '0.7')}")
    print(f"town pages ............. {sum(1 for f, p in written if p == '0.6')}")
    print(f"city pages linked ...... {pass_city_pages()}")
    print(f"locations hub directory  {'updated' if pass_locations_hub() else 'unchanged'}")
    print(f"sitemap entries ........ {pass_sitemap(written)}")


if __name__ == "__main__":
    main()
