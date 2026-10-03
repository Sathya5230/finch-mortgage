#!/usr/bin/env python3
"""Inject local-SEO and lead-capture blocks sitewide.

Idempotent: every block is wrapped in FINCH-*:START / FINCH-*:END markers and
re-running replaces the block rather than stacking a second copy.

Run:  python3 inject_local_seo.py
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.finchmortgages.co.nz"

# --------------------------------------------------------------------------
# Business NAP — single source of truth. Must match Google Business Profile
# character-for-character; any drift here becomes a NAP-consistency problem.
# --------------------------------------------------------------------------
BIZ = {
    "legal_name": "Finch Mortgages Limited",
    "name": "Finch Mortgages",
    "street": "17a Marlene Ave",
    "suburb": "Te Atatu South",
    "city": "Auckland",
    "postcode": "0610",
    "country": "NZ",
    "phone_display": "027 343 3293",
    "phone_e164": "+64273433293",
    "email": "Mukhtar@finchmortgages.co.nz",
    "lat": "-36.87450",
    "lng": "174.64830",
    "fsp": "FSP1011206",
    "fspr": "FSP1011125",
}

# --------------------------------------------------------------------------
# Google Business Profile — FILL THESE IN, then re-run this script.
# Left blank on purpose: review counts and ratings must never be invented
# (Google fake-engagement policy + FTC penalties for fabricated reviews).
# Once set, the footer gains a rating badge + "Leave a review" link and
# aggregateRating is added to the organisation schema.
# --------------------------------------------------------------------------
GBP_PROFILE_URL = ""   # e.g. "https://g.page/finchmortgages"
GBP_REVIEW_URL = ""    # e.g. "https://g.page/r/XXXXXXXXXXXX/review"
GBP_RATING = ""        # e.g. "4.9"  — must be the real figure shown on GBP
GBP_REVIEW_COUNT = ""  # e.g. "37"   — must be the real figure shown on GBP

OPENING_HOURS = [
    (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "09:00", "18:00"),
    (["Saturday"], "10:00", "14:00"),
]

WEB3FORMS_KEY = "d324f726-646c-4e0b-a1f2-7117480ff013"

# --------------------------------------------------------------------------
# Geography. Coordinates are city centroids; region codes are ISO 3166-2:NZ.
# --------------------------------------------------------------------------
CITIES = {
    "auckland-city":       ("Auckland",          "Auckland",             "NZ-AUK", "-36.85090", "174.76450"),
    "manukau":             ("Manukau",           "Auckland",             "NZ-AUK", "-36.99390", "174.87970"),
    "hamilton":            ("Hamilton",          "Waikato",              "NZ-WKO", "-37.78700", "175.27930"),
    "tauranga":            ("Tauranga",          "Bay of Plenty",        "NZ-BOP", "-37.68780", "176.16510"),
    "wellington":          ("Wellington",        "Wellington",           "NZ-WGN", "-41.28660", "174.77560"),
    "christchurch":        ("Christchurch",      "Canterbury",           "NZ-CAN", "-43.53210", "172.63620"),
    "dunedin":             ("Dunedin",           "Otago",                "NZ-OTA", "-45.87880", "170.50280"),
    "queenstown":          ("Queenstown",        "Otago",                "NZ-OTA", "-45.03120", "168.66260"),
    "nelson":              ("Nelson",            "Nelson",               "NZ-NSN", "-41.27060", "173.28400"),
    "napier-hawkes-bay":   ("Napier",            "Hawke's Bay",          "NZ-HKB", "-39.49280", "176.91200"),
    "palmerston-north":    ("Palmerston North",  "Manawatū-Whanganui",   "NZ-MWT", "-40.35230", "175.60820"),
    "whangarei-northland": ("Whangārei",         "Northland",            "NZ-NTL", "-35.72510", "174.32370"),
}

SERVICES = {
    "home-loan":          ("Home Loan",                 "Home loan brokerage"),
    "first-home-buyer":   ("First Home Buyer Mortgage", "First home buyer mortgage advice"),
    "investment-property":("Investment Property Loan",  "Investment property lending"),
    "pre-approval":       ("Mortgage Pre-Approval",     "Mortgage pre-approval"),
    "refinance":          ("Mortgage Refinance",        "Mortgage refinancing"),
    "self-employed":      ("Self-Employed Mortgage",    "Self-employed mortgage advice"),
}

# Hook the CTA copy to the intent behind each service keyword.
SERVICE_PITCH = {
    "home-loan":           ("Get your home loan sorted in {city}",
                            "Tell us what you're buying and we'll come back with the lenders most likely to say yes — and at what rate."),
    "first-home-buyer":    ("Buying your first home in {city}?",
                            "We'll check your KiwiSaver withdrawal, First Home Loan eligibility and real deposit gap before you talk to any bank."),
    "investment-property": ("Grow your {city} property portfolio",
                            "Send us your current position and we'll model the equity, DTI headroom and structure across 20+ lenders."),
    "pre-approval":        ("Get pre-approved before you bid in {city}",
                            "Auction-ready pre-approval, usually back within days. Tell us your situation and we'll start today."),
    "refinance":           ("See what refinancing saves you in {city}",
                            "Send your current rate and balance — we'll show you the switch, the cashback on offer and the break-fee maths."),
    "self-employed":       ("Self-employed in {city}? We know the lenders who get it",
                            "One or two years' trading, contractor or company income — tell us the shape of it and we'll find the right fit."),
}

ENQUIRY_OPTIONS = [
    "Buying my first home",
    "Buying my next home",
    "Mortgage pre-approval",
    "Refinancing / better rate",
    "Investment property",
    "Self-employed / contractor",
    "Construction or new build",
    "Something else",
]


# ==========================================================================
# Helpers
# ==========================================================================

def marker_replace(html, name, block):
    """Insert or replace a marker-wrapped block. Returns (html, changed)."""
    start, end = f"<!-- FINCH-{name}:START -->", f"<!-- FINCH-{name}:END -->"
    wrapped = f"{start}\n{block}\n{end}"
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pat.search(html):
        new = pat.sub(lambda _: wrapped, html, count=1)
        return new, new != html
    return None, False


def insert_before(html, anchor, name, block):
    """Place a marker block immediately before `anchor`, or replace in place."""
    replaced, changed = marker_replace(html, name, block)
    if replaced is not None:
        return replaced, changed
    if anchor not in html:
        return html, False
    start, end = f"<!-- FINCH-{name}:START -->", f"<!-- FINCH-{name}:END -->"
    wrapped = f"{start}\n{block}\n{end}\n"
    return html.replace(anchor, wrapped + anchor, 1), True


def html_pages():
    skip_dirs = {".git", "node_modules", ".venv-seomachine", "__pycache__",
                 ".claude", ".vscode", "docs", "drafts", "output", "research",
                 "published", "rewrites", "topics", "examples", "context",
                 "data_sources", "config"}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in sorted(filenames):
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def rating_available():
    return bool(GBP_RATING and GBP_REVIEW_COUNT)


# ==========================================================================
# 1. Footer NAP — visible Name/Address/Phone + click-to-call on every page
# ==========================================================================

def footer_nap_block():
    addr = (f'{BIZ["street"]}, {BIZ["suburb"]}, {BIZ["city"]} '
            f'{BIZ["postcode"]}, New Zealand')
    rating = ""
    if rating_available() and GBP_PROFILE_URL:
        rating = (
            f'<a href="{GBP_PROFILE_URL}" rel="noopener" target="_blank" '
            f'style="display:inline-flex;align-items:center;gap:0.4rem;margin-top:0.6rem;'
            f'font-size:0.82rem;font-weight:700;color:#b29361;">'
            f'<span>★★★★★</span><span>{GBP_RATING}/5 from {GBP_REVIEW_COUNT} Google reviews</span></a>'
        )
    return f"""<div class="footer-nap" itemscope itemtype="https://schema.org/MortgageBroker" style="border-top:1px solid rgba(255,255,255,0.12);margin-top:2rem;padding-top:1.75rem;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.5rem;font-size:0.88rem;line-height:1.7;">
<div>
<strong itemprop="name" style="display:block;font-size:0.95rem;margin-bottom:0.35rem;">{BIZ['legal_name']}</strong>
<span itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
<span itemprop="streetAddress">{BIZ['street']}</span>, <span itemprop="addressLocality">{BIZ['suburb']}</span>, <span itemprop="addressRegion">{BIZ['city']}</span> <span itemprop="postalCode">{BIZ['postcode']}</span><meta itemprop="addressCountry" content="{BIZ['country']}"/>
</span>
{rating}
</div>
<div>
<strong style="display:block;font-size:0.95rem;margin-bottom:0.35rem;">Talk to an adviser</strong>
<a href="tel:{BIZ['phone_e164']}" data-cta="footer-call" style="display:block;font-weight:700;">📞 {BIZ['phone_display']}</a>
<a href="mailto:{BIZ['email']}" style="display:block;">✉️ {BIZ['email']}</a>
<meta itemprop="telephone" content="{BIZ['phone_e164']}"/>
<meta itemprop="email" content="{BIZ['email']}"/>
</div>
<div>
<strong style="display:block;font-size:0.95rem;margin-bottom:0.35rem;">Opening hours</strong>
<span>Mon–Fri: 9:00am – 6:00pm</span><br/>
<span>Saturday: 10:00am – 2:00pm</span><br/>
<span>Sunday: Closed</span>
</div>
<div>
<strong style="display:block;font-size:0.95rem;margin-bottom:0.35rem;">Registered adviser</strong>
<span>FSP {BIZ['fsp']}</span><br/>
<span>FSPR {BIZ['fspr']}</span><br/>
<span>Serving all of New Zealand</span>
</div>
</div>"""


# ==========================================================================
# 2. Context-aware lead form for high-intent pages
# ==========================================================================

def lead_form_block(heading, sub, service_label, city_label, form_id):
    opts = "".join(
        f'<option value="{o}"{" selected" if o == service_label else ""}>{o}</option>'
        for o in ENQUIRY_OPTIONS
    )
    where = f" in {city_label}" if city_label else ""
    return f"""<section id="enquire" style="padding:4.5rem 0;background:linear-gradient(135deg,#10443e 0%,#1a5c54 100%);">
<div class="container" style="max-width:980px;">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2.5rem;align-items:start;">

<div style="color:#fff;">
<div style="font-size:0.7rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;color:#b5ceb0;margin-bottom:0.75rem;">Free · No obligation · $0 broker fee</div>
<h2 style="color:#fff;font-size:clamp(1.6rem,3.2vw,2.2rem);margin-bottom:0.9rem;">{heading}</h2>
<p style="color:rgba(255,255,255,0.82);line-height:1.75;margin-bottom:1.75rem;">{sub}</p>

<a href="tel:{BIZ['phone_e164']}" data-cta="leadform-call" style="display:inline-flex;align-items:center;gap:0.6rem;background:#b29361;color:#10443e;font-weight:800;padding:0.95rem 1.6rem;border-radius:999px;margin-bottom:1.25rem;">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
Call {BIZ['phone_display']} now
</a>
<ul style="list-style:none;padding:0;margin:0;color:rgba(255,255,255,0.78);font-size:0.9rem;line-height:2;">
<li>✓ We compare 20+ NZ banks and non-bank lenders</li>
<li>✓ The lender pays us — our advice costs you nothing</li>
<li>✓ Registered financial adviser, FSP {BIZ['fsp']}</li>
<li>✓ Same-day reply on weekdays</li>
</ul>
</div>

<div style="background:#fff;border-radius:1.25rem;padding:2rem;box-shadow:0 12px 40px rgba(0,0,0,0.18);">
<form action="https://api.web3forms.com/submit" method="POST" data-form-id="{form_id}">
<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}"/>
<input type="hidden" name="subject" value="New enquiry{where} — {service_label or 'Mortgage'} | Finch Mortgages"/>
<input type="hidden" name="from_name" value="Finch Mortgages Website"/>
<input type="hidden" name="service" value="{service_label}"/>
<input type="hidden" name="city" value="{city_label}"/>
<input type="hidden" name="redirect" value="{SITE}/thank-you.html"/>
<input type="checkbox" name="botcheck" style="display:none;" tabindex="-1" autocomplete="off"/>

<label style="display:block;font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;color:#7a9490;margin-bottom:0.4rem;">Your name</label>
<input class="contact-input-box" name="name" type="text" placeholder="Sarah" required="" style="margin-bottom:1rem;"/>

<label style="display:block;font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;color:#7a9490;margin-bottom:0.4rem;">Mobile</label>
<input class="contact-input-box" name="phone" type="tel" placeholder="021 000 0000" required="" style="margin-bottom:1rem;"/>

<label style="display:block;font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;color:#7a9490;margin-bottom:0.4rem;">Email</label>
<input class="contact-input-box" name="email" type="email" placeholder="sarah@example.com" required="" style="margin-bottom:1rem;"/>

<label style="display:block;font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;color:#7a9490;margin-bottom:0.4rem;">What do you need?</label>
<select class="contact-input-box" name="enquiry_type" style="margin-bottom:1.5rem;">{opts}</select>

<button class="contact-submit-btn" type="submit" data-cta="leadform-submit" style="width:100%;">GET MY FREE ASSESSMENT →</button>
<p style="font-size:0.72rem;color:#7a9490;text-align:center;margin:1rem 0 0;">No credit check. We never share your details.</p>
</form>
</div>

</div>
</div>
</section>"""


# ==========================================================================
# 3. JSON-LD for location pages
# ==========================================================================

def org_node():
    node = {
        "@type": ["MortgageBroker", "FinancialService"],
        "@id": f"{SITE}/#organization",
        "name": BIZ["name"],
        "legalName": BIZ["legal_name"],
        "url": f"{SITE}/",
        "logo": f"{SITE}/images/finch-logo.png",
        "image": f"{SITE}/images/finch-logo.png",
        "telephone": BIZ["phone_e164"],
        "email": BIZ["email"],
        "priceRange": "Free — no broker fee",
        "currenciesAccepted": "NZD",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["street"],
            "addressLocality": BIZ["suburb"],
            "addressRegion": BIZ["city"],
            "postalCode": BIZ["postcode"],
            "addressCountry": BIZ["country"],
        },
        "geo": {"@type": "GeoCoordinates",
                "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": days,
             "opens": o, "closes": c} for days, o, c in OPENING_HOURS
        ],
        "identifier": [
            {"@type": "PropertyValue", "name": "Financial Service Provider", "value": BIZ["fsp"]},
            {"@type": "PropertyValue", "name": "FSPR", "value": BIZ["fspr"]},
        ],
    }
    if GBP_PROFILE_URL:
        node["sameAs"] = [GBP_PROFILE_URL]
    if rating_available():
        node["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": GBP_RATING,
            "reviewCount": GBP_REVIEW_COUNT,
            "bestRating": "5",
        }
    return node


FAQ_ITEM = re.compile(
    r'<div class="faq-item".*?<span>(?P<q>.*?)</span>.*?'
    r'<div class="faq-content".*?>(?P<a>.*?)</div>\s*</div>',
    re.S,
)


def extract_faqs(html):
    out = []
    for m in FAQ_ITEM.finditer(html):
        q = re.sub(r"<[^>]+>", "", m.group("q")).strip()
        a = re.sub(r"<[^>]+>", " ", m.group("a"))
        a = re.sub(r"\s+", " ", a).strip()
        if q and a:
            out.append((q, a))
    return out


def location_schema(url, title, desc, service_label, service_type,
                    city_name, region, lat, lng, faqs):
    graph = [org_node()]

    graph.append({
        "@type": "Service",
        "@id": f"{url}#service",
        "name": f"{service_label} in {city_name}",
        "serviceType": service_type,
        "description": desc,
        "provider": {"@id": f"{SITE}/#organization"},
        "areaServed": [
            {"@type": "City", "name": city_name,
             "containedInPlace": {"@type": "AdministrativeArea", "name": region},
             "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}},
            {"@type": "AdministrativeArea", "name": region},
        ],
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": url,
            "servicePhone": {"@type": "ContactPoint",
                             "telephone": BIZ["phone_e164"],
                             "contactType": "sales",
                             "areaServed": "NZ",
                             "availableLanguage": "en"},
        },
        "offers": {"@type": "Offer", "price": "0",
                   "priceCurrency": "NZD",
                   "description": "No broker fee — the lender pays our commission on settlement."},
    })

    graph.append({
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Service Locations",
             "item": f"{SITE}/locations/index.html"},
            {"@type": "ListItem", "position": 3,
             "name": f"{service_label} in {city_name}", "item": url},
        ],
    })

    graph.append({
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": title,
        "description": desc,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{url}#service"},
        "breadcrumb": {"@id": f"{url}#breadcrumb"},
        "inLanguage": "en-NZ",
        "provider": {"@id": f"{SITE}/#organization"},
    })

    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    payload = {"@context": "https://schema.org", "@graph": graph}
    return ('<script type="application/ld+json">'
            + json.dumps(payload, ensure_ascii=False, indent=2)
            + "</script>")


# ==========================================================================
# Passes
# ==========================================================================

def pass_footer_nap():
    changed = 0
    block = footer_nap_block()
    for fp in html_pages():
        html = open(fp, encoding="utf-8").read()
        anchor = '<div class="footer-bottom">'
        if anchor not in html:
            anchor = "</footer>"
            if anchor not in html:
                continue
        new, did = insert_before(html, anchor, "NAP", block)
        if did:
            open(fp, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


def pass_leadtrack():
    changed = 0
    tag = '<script defer src="/leadtrack.js"></script>'
    for fp in html_pages():
        html = open(fp, encoding="utf-8").read()
        new, did = insert_before(html, "</body>", "LEADTRACK", tag)
        if did:
            open(fp, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


def parse_location_slug(fn):
    stem = fn[:-5]
    for svc in sorted(SERVICES, key=len, reverse=True):
        if stem.startswith(svc + "-"):
            city = stem[len(svc) + 1:]
            if city in CITIES:
                return svc, city
    return None, None


def pass_locations():
    loc_dir = os.path.join(ROOT, "locations")
    stats = {"schema": 0, "geo": 0, "form": 0, "skipped": []}
    for fn in sorted(os.listdir(loc_dir)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        svc, city = parse_location_slug(fn)
        if not svc:
            stats["skipped"].append(fn)
            continue
        fp = os.path.join(loc_dir, fn)
        html = open(fp, encoding="utf-8").read()
        service_label, service_type = SERVICES[svc]
        city_name, region, region_code, lat, lng = CITIES[city]
        url = f"{SITE}/locations/{fn}"

        tm = re.search(r"<title>(.*?)</title>", html, re.S)
        dm = re.search(r'<meta content="([^"]*)" name="description"', html)
        title = tm.group(1).strip() if tm else f"{service_label} in {city_name}"
        desc = dm.group(1).strip() if dm else title

        # --- per-city geo meta (every page previously claimed Auckland) ---
        geo_block = (
            f'<meta content="{region_code}" name="geo.region"/>\n'
            f'<meta content="{city_name}, New Zealand" name="geo.placename"/>\n'
            f'<meta content="{lat};{lng}" name="geo.position"/>\n'
            f'<meta content="{lat}, {lng}" name="ICBM"/>\n'
            f'<meta content="{service_label}" name="finch:service"/>\n'
            f'<meta content="{city_name}" name="finch:city"/>'
        )
        new, did = marker_replace(html, "GEO", geo_block)
        if new is not None:
            html = new
        else:
            old_geo = re.compile(
                r'<!-- Regional GEO -->\s*'
                r'<meta content="[^"]*" name="geo\.region"/>\s*'
                r'<meta content="[^"]*" name="geo\.placename"/>\s*'
                r'<meta content="[^"]*" name="geo\.position"/>\s*'
                r'<meta content="[^"]*" name="ICBM"/>'
            )
            wrapped = ("<!-- Regional GEO -->\n<!-- FINCH-GEO:START -->\n"
                       + geo_block + "\n<!-- FINCH-GEO:END -->")
            if old_geo.search(html):
                html = old_geo.sub(lambda _: wrapped, html, count=1)
                did = True
        if did:
            stats["geo"] += 1

        # --- JSON-LD graph (these pages had none at all) ---
        faqs = extract_faqs(html)
        schema = location_schema(url, title, desc, service_label, service_type,
                                 city_name, region, lat, lng, faqs)
        new, did = insert_before(html, "</head>", "SCHEMA", schema)
        if did:
            html = new
            stats["schema"] += 1

        # --- inline lead form ---
        head, sub = SERVICE_PITCH[svc]
        form = lead_form_block(head.format(city=city_name), sub,
                               service_label, city_name,
                               f"loc-{svc}-{city}")
        anchor = "</main>" if "</main>" in html else '<footer class="site-footer">'
        new, did = insert_before(html, anchor, "LEADFORM", form)
        if did:
            html = new
            stats["form"] += 1

        open(fp, "w", encoding="utf-8").write(html)
    return stats


SERVICE_PAGE_CITY = ""  # service pages are national, not city-scoped

SERVICE_PAGE_PITCH = {
    "home-loan":           ("Ready to get your home loan sorted?", "home-loan"),
    "first-home-buyer":    ("Buying your first home?", "first-home-buyer"),
    "investment-property": ("Building a property portfolio?", "investment-property"),
    "pre-approval":        ("Need pre-approval before you bid?", "pre-approval"),
    "refinance":           ("Paying more than you need to?", "refinance"),
    "self-employed":       ("Self-employed and tired of bank knock-backs?", "self-employed"),
    "next-home-buyer":     ("Moving to your next home?", "home-loan"),
    "construction-loan":   ("Building or renovating?", "home-loan"),
    "commercial-property": ("Buying commercial property?", "investment-property"),
    "asset-finance":       ("Need vehicle or equipment finance?", "home-loan"),
}


def pass_services():
    svc_dir = os.path.join(ROOT, "services")
    count = 0
    for fn in sorted(os.listdir(svc_dir)):
        if not fn.endswith(".html"):
            continue
        slug = fn[:-5]
        heading, pitch_key = SERVICE_PAGE_PITCH.get(
            slug, ("Talk to a mortgage adviser", "home-loan"))
        _, sub = SERVICE_PITCH[pitch_key]
        label = SERVICES.get(pitch_key, ("Mortgage", ""))[0]
        fp = os.path.join(svc_dir, fn)
        html = open(fp, encoding="utf-8").read()
        form = lead_form_block(heading, sub.format(city="New Zealand"),
                               label, SERVICE_PAGE_CITY, f"svc-{slug}")
        anchor = "</main>" if "</main>" in html else '<footer class="site-footer">'
        new, did = insert_before(html, anchor, "LEADFORM", form)
        if did:
            open(fp, "w", encoding="utf-8").write(new)
            count += 1
    return count


def pass_lender_schema():
    """The 4 lender hub pages carry no structured data at all."""
    targets = {
        "major-banks.html": ("Major Bank Home Loans NZ", "Compare New Zealand's major bank home loans."),
        "non-bank-lenders.html": ("Non-Bank Lenders NZ", "Compare New Zealand non-bank mortgage lenders."),
        "specialist-lenders.html": ("Specialist Lenders NZ", "Compare New Zealand specialist and asset finance lenders."),
        "credit-unions.html": ("Credit Unions NZ", "Compare New Zealand credit union mortgage options."),
    }
    count = 0
    for fn, (name, desc) in targets.items():
        fp = os.path.join(ROOT, "lenders", fn)
        if not os.path.exists(fp):
            continue
        html = open(fp, encoding="utf-8").read()
        tm = re.search(r"<title>(.*?)</title>", html, re.S)
        dm = re.search(r'<meta content="([^"]*)" name="description"', html)
        title = tm.group(1).strip() if tm else name
        description = dm.group(1).strip() if dm else desc
        url = f"{SITE}/lenders/{fn}"
        faqs = extract_faqs(html)
        graph = [org_node(), {
            "@type": "CollectionPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "en-NZ",
            "isPartOf": {"@id": f"{SITE}/#website"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
            "provider": {"@id": f"{SITE}/#organization"},
        }, {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Lenders", "item": f"{SITE}/lenders.html"},
                {"@type": "ListItem", "position": 3, "name": name, "item": url},
            ],
        }]
        if faqs:
            graph.append({
                "@type": "FAQPage", "@id": f"{url}#faq",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in faqs],
            })
        schema = ('<script type="application/ld+json">'
                  + json.dumps({"@context": "https://schema.org", "@graph": graph},
                               ensure_ascii=False, indent=2) + "</script>")
        new, did = insert_before(html, "</head>", "SCHEMA", schema)
        if did:
            open(fp, "w", encoding="utf-8").write(new)
            count += 1
    return count


# --------------------------------------------------------------------------
# Doorway-page remediation.
#
# The 72 locations/ pages measured 82-88% word-identical within each service
# template (92.7% after swapping the city name), which is the pattern Google's
# core updates treat as doorway pages. city_data.py already holds real,
# human-authored per-city detail that generate_service_city_pages.py never
# used, so we surface it rather than inventing anything.
# --------------------------------------------------------------------------
SERVICE_LOCAL_FRAME = {
    "home-loan": "What buying in {city} actually means for your home loan",
    "first-home-buyer": "What first home buyers in {city} are up against",
    "investment-property": "What investors need to know about {city}",
    "pre-approval": "Why pre-approval in {city} needs local knowledge",
    "refinance": "What refinancing looks like in {city}",
    "self-employed": "Self-employed borrowers in {city}: the local picture",
}

SERVICE_LOCAL_LEAD = {
    "home-loan": "Lender appetite is not uniform across New Zealand. Before we approach anyone on your behalf, here is the {city} detail that shapes which lender is likely to say yes.",
    "first-home-buyer": "Deposit requirements, LVR exemptions and First Home Grant eligibility all play out differently by region. Here is what matters in {city}.",
    "investment-property": "Yield, lender appetite and DTI treatment vary sharply by region. Here is the {city} context we work with.",
    "pre-approval": "A pre-approval is only as good as the lender behind it. Here is the {city} detail that decides which lender to approach first.",
    "refinance": "What you can switch to depends on your property type and location as much as your income. Here is the {city} picture.",
    "self-employed": "Self-employed lending is where lender choice matters most, and local property type feeds directly into it. Here is the {city} context.",
}


def _city_lookup():
    import city_data
    return {c["slug"].replace("mortgage-broker-", ""): c for c in city_data.CITIES}


def local_content_block(svc, city_slug, city_row):
    city = city_row["city"]
    frame = SERVICE_LOCAL_FRAME[svc].format(city=city)
    lead = SERVICE_LOCAL_LEAD[svc].format(city=city)
    return f"""<section style="padding:4rem 0;background:var(--finch-mist);border-top:1px solid rgba(180,178,169,0.15);">
<div class="container" style="max-width:1000px;">
<div class="section-label"><span>Local knowledge</span></div>
<h2 class="section-heading" style="margin-bottom:1.25rem;">{frame}</h2>
<p style="color:var(--neutral-medGray);line-height:1.8;margin-bottom:2rem;">{lead}</p>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;margin-bottom:2rem;">
<div style="background:white;border-radius:1rem;padding:1.5rem;border:1px solid rgba(181,206,176,0.4);">
<h3 style="font-size:1.05rem;margin-bottom:0.75rem;color:var(--finch-forest);">The {city} market</h3>
<p style="font-size:0.95rem;line-height:1.75;color:var(--neutral-medGray);margin:0;">{city_row['market_note']}</p>
</div>
<div style="background:white;border-radius:1rem;padding:1.5rem;border:1px solid rgba(181,206,176,0.4);">
<h3 style="font-size:1.05rem;margin-bottom:0.75rem;color:var(--finch-forest);">Typical {city} price bands</h3>
<p style="font-size:0.95rem;line-height:1.75;color:var(--neutral-medGray);margin:0;">Indicatively, {city_row['price_band']}.</p>
<p style="font-size:0.78rem;color:var(--neutral-warmGray);margin:0.75rem 0 0;">Indicative ranges only — not a valuation. Ask us for current figures for your target street.</p>
</div>
</div>

<div style="background:white;border-radius:1rem;padding:1.75rem;border:1px solid rgba(181,206,176,0.4);margin-bottom:1.5rem;">
<h3 style="font-size:1.05rem;margin-bottom:0.75rem;color:var(--finch-forest);">Who we typically help in {city}</h3>
<p style="font-size:0.95rem;line-height:1.75;color:var(--neutral-medGray);margin:0;">We regularly arrange finance for {city_row['common_buyers']}.</p>
</div>

<div style="background:white;border-radius:1rem;padding:1.75rem;border:1px solid rgba(181,206,176,0.4);">
<h3 style="font-size:1.05rem;margin-bottom:0.75rem;color:var(--finch-forest);">Areas we cover around {city}</h3>
<p style="font-size:0.95rem;line-height:1.75;color:var(--neutral-medGray);margin:0;">{city_row['suburbs']}.</p>
</div>
</div>
</section>"""


def pass_location_local_content():
    rows = _city_lookup()
    loc_dir = os.path.join(ROOT, "locations")
    count, missing = 0, set()
    for fn in sorted(os.listdir(loc_dir)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        svc, city = parse_location_slug(fn)
        if not svc:
            continue
        row = rows.get(city)
        if not row:
            missing.add(city)
            continue
        fp = os.path.join(loc_dir, fn)
        html = open(fp, encoding="utf-8").read()
        block = local_content_block(svc, city, row)
        # Sit it above the FAQ so the page leads with local substance.
        anchor = "<!-- Local FAQ Section -->"
        if anchor not in html:
            anchor = "<!-- FINCH-LEADFORM:START -->"
        new, did = insert_before(html, anchor, "LOCALCONTENT", block)
        if did:
            open(fp, "w", encoding="utf-8").write(new)
            count += 1
    return count, sorted(missing)


# "mortgage broker {place}" is the highest commercial-intent local query on the
# site, but these pages shipped as plain BlogPosting with no areaServed at all.
# Topic posts that merely match the filename prefix are excluded.
BROKER_PAGE_EXCLUDE = {
    "mortgage-broker-fees-nz.html",
    "mortgage-broker-vs-bank-nz.html",
}


def broker_place_name(html):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return ""
    txt = re.sub(r"<[^>]+>", "", m.group(1))
    txt = (txt.replace("&amp;", "&").replace("&#39;", "'")
              .replace("&rsquo;", "’").replace("&nbsp;", " "))
    txt = txt.split(":")[0]
    txt = re.sub(r"^\s*Mortgage\s*Broker\s*", "", txt, flags=re.I)
    return txt.strip().rstrip(".").strip()


def area_served_places(place):
    """'Invercargill & Southland' -> two named Places. No invented coordinates."""
    parts = [p.strip().removeprefix("the ").strip()
             for p in re.split(r"\s*&\s*", place) if p.strip()]
    out = []
    for p in parts:
        if p.lower() in ("new zealand", "nz"):
            out.append({"@type": "Country", "name": "New Zealand"})
        else:
            out.append({"@type": "Place", "name": p,
                        "containedInPlace": {"@type": "Country", "name": "New Zealand"}})
    return out or [{"@type": "Country", "name": "New Zealand"}]


def pass_broker_city_pages():
    blog_dir = os.path.join(ROOT, "blog")
    stats = {"schema": 0, "form": 0}
    for fn in sorted(os.listdir(blog_dir)):
        if not fn.startswith("mortgage-broker-") or not fn.endswith(".html"):
            continue
        if fn in BROKER_PAGE_EXCLUDE:
            continue
        fp = os.path.join(blog_dir, fn)
        html = open(fp, encoding="utf-8").read()
        place = broker_place_name(html)
        if not place:
            continue
        url = f"{SITE}/blog/{fn}"
        areas = area_served_places(place)

        # The page's existing publisher stub shares this @id, so defining the
        # organisation fully here merges NAP/geo/hours into the same entity.
        graph = [org_node(), {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": f"Mortgage Broker in {place}",
            "serviceType": "Mortgage brokerage",
            "provider": {"@id": f"{SITE}/#organization"},
            "areaServed": areas,
            "availableChannel": {
                "@type": "ServiceChannel",
                "serviceUrl": url,
                "servicePhone": {"@type": "ContactPoint",
                                 "telephone": BIZ["phone_e164"],
                                 "contactType": "sales",
                                 "areaServed": "NZ",
                                 "availableLanguage": "en"},
            },
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NZD",
                       "description": "No broker fee — the lender pays our commission on settlement."},
        }]
        schema = ('<script type="application/ld+json">'
                  + json.dumps({"@context": "https://schema.org", "@graph": graph},
                               ensure_ascii=False, indent=2) + "</script>")
        new, did = insert_before(html, "</head>", "LOCALSCHEMA", schema)
        if did:
            html = new
            stats["schema"] += 1

        meta_block = (f'<meta content="Mortgage Broker" name="finch:service"/>\n'
                      f'<meta content="{place}" name="finch:city"/>')
        new, did = insert_before(html, "</head>", "GEO", meta_block)
        if did:
            html = new

        form = lead_form_block(
            f"Talk to a mortgage broker in {place}",
            "Tell us where you're at — buying, refinancing or just working out what you can borrow — "
            "and we'll come back with the lenders most likely to approve you.",
            "Mortgage Broker", place, f"broker-{fn[:-5]}")
        anchor = "</main>" if "</main>" in html else '<footer class="site-footer">'
        new, did = insert_before(html, anchor, "LEADFORM", form)
        if did:
            html = new
            stats["form"] += 1

        open(fp, "w", encoding="utf-8").write(html)
    return stats


def pass_locations_hub():
    """The city hub had no structured data; give Google the full city list."""
    fp = os.path.join(ROOT, "locations", "index.html")
    if not os.path.exists(fp):
        return 0
    html = open(fp, encoding="utf-8").read()
    url = f"{SITE}/locations/index.html"
    tm = re.search(r"<title>(.*?)</title>", html, re.S)
    dm = re.search(r'<meta content="([^"]*)" name="description"', html)

    items = []
    pos = 0
    for city, (city_name, region, _rc, lat, lng) in CITIES.items():
        for svc, (service_label, _st) in SERVICES.items():
            fn = f"{svc}-{city}.html"
            if not os.path.exists(os.path.join(ROOT, "locations", fn)):
                continue
            pos += 1
            items.append({
                "@type": "ListItem",
                "position": pos,
                "name": f"{service_label} in {city_name}",
                "url": f"{SITE}/locations/{fn}",
            })

    graph = [org_node(), {
        "@type": "CollectionPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": tm.group(1).strip() if tm else "Mortgage Broker Service Locations NZ",
        "description": dm.group(1).strip() if dm else
            "Finch Mortgages serves home buyers, investors and refinancers across New Zealand.",
        "inLanguage": "en-NZ",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "breadcrumb": {"@id": f"{url}#breadcrumb"},
        "about": {"@id": f"{SITE}/#organization"},
        "mainEntity": {"@id": f"{url}#list"},
    }, {
        "@type": "ItemList",
        "@id": f"{url}#list",
        "name": "Mortgage services by New Zealand location",
        "numberOfItems": len(items),
        "itemListElement": items,
    }, {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Service Locations", "item": url},
        ],
    }]
    schema = ('<script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@graph": graph},
                           ensure_ascii=False, indent=2) + "</script>")
    new, did = insert_before(html, "</head>", "SCHEMA", schema)
    if did:
        open(fp, "w", encoding="utf-8").write(new)
        return len(items)
    return 0


def main():
    print("Finch Mortgages — local SEO + lead capture injection\n")
    if not rating_available():
        print("  NOTE: GBP_RATING / GBP_REVIEW_COUNT are blank, so no rating badge")
        print("        and no aggregateRating were emitted. Fill them in at the top")
        print("        of this script with the real Google figures and re-run.\n")

    print(f"  footer NAP + click-to-call ... {pass_footer_nap():>3} pages")
    print(f"  leadtrack.js tag ............. {pass_leadtrack():>3} pages")
    loc = pass_locations()
    print(f"  location JSON-LD ............. {loc['schema']:>3} pages")
    print(f"  location per-city geo meta ... {loc['geo']:>3} pages")
    print(f"  location lead forms .......... {loc['form']:>3} pages")
    if loc["skipped"]:
        print(f"  ! unparsed location slugs: {loc['skipped']}")
    print(f"  service lead forms ........... {pass_services():>3} pages")
    print(f"  lender hub JSON-LD ........... {pass_lender_schema():>3} pages")
    print(f"  city hub ItemList ............ {pass_locations_hub():>3} locations listed")
    lc, lc_missing = pass_location_local_content()
    print(f"  location city-specific content {lc:>3} pages")
    if lc_missing:
        print(f"  ! no city_data row for: {lc_missing}")
    brk = pass_broker_city_pages()
    print(f"  broker-city local schema ..... {brk['schema']:>3} pages")
    print(f"  broker-city lead forms ....... {brk['form']:>3} pages")
    print("\nDone.")


if __name__ == "__main__":
    main()
