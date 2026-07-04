#!/usr/bin/env python3
"""
Builds internal-link sections to de-orphan lender reviews, city pages, and
guides. Idempotent: each injected block sits between INTERNAL-LINKS markers and
is replaced on re-run. Inserted immediately before <footer class="site-footer">.

Run after adding new review/city/blog pages: python3 build_internal_links.py
"""
import os, re, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
START = "<!-- INTERNAL-LINKS:START -->"
END = "<!-- INTERNAL-LINKS:END -->"
FOOTER = '<footer class="site-footer">'

CAT_FROM_SUFFIX = {
    "Mortgage Rates & Policy": "Major Banks",
    "Non-Bank Mortgages": "Non-Bank Lenders",
    "Asset & Specialist Finance": "Specialist Lenders",
    "Credit Union Lending": "Credit Unions",
}
CAT_HUB = {
    "Major Banks": "lenders/major-banks.html",
    "Non-Bank Lenders": "lenders/non-bank-lenders.html",
    "Specialist Lenders": "lenders/specialist-lenders.html",
    "Credit Unions": "lenders/credit-unions.html",
}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def title_of(path):
    m = re.search(r"<title>(.*?)</title>", read(path), re.S)
    return html.unescape(m.group(1).strip()) if m else os.path.basename(path)


def clean(label):
    label = label.split(" | ")[0].split(" — ")[0]
    label = re.sub(r"\s*\(?20\d\d\)?$", "", label).strip()
    label = re.sub(r"\s+NZ$", "", label).strip()
    return label


# ---------------------------------------------------------------- gather data
reviews = []  # (slug, label, category)
for p in sorted(glob.glob(os.path.join(ROOT, "lenders", "*-review.html"))):
    t = title_of(p)
    suffix = t.split(" | ")
    cat = "Specialist Lenders"
    for part in suffix:
        if part.strip() in CAT_FROM_SUFFIX:
            cat = CAT_FROM_SUFFIX[part.strip()]
            break
    reviews.append((os.path.basename(p), clean(t), cat))

CAT_ORDER = ["Major Banks", "Non-Bank Lenders", "Specialist Lenders", "Credit Unions"]

# location pages = blog/mortgage-broker-* minus the two topic articles
TOPIC = {"mortgage-broker-fees-nz.html", "mortgage-broker-vs-bank-nz.html"}
locations = []  # (slug, label)
for p in sorted(glob.glob(os.path.join(ROOT, "blog", "mortgage-broker-*.html"))):
    b = os.path.basename(p)
    if b in TOPIC:
        continue
    locations.append((b, clean(title_of(p))))

# all blog posts for the index
blog_posts = []  # (slug, label)
for p in sorted(glob.glob(os.path.join(ROOT, "blog", "*.html"))):
    blog_posts.append((os.path.basename(p), clean(title_of(p))))


# ---------------------------------------------------------------- html builder
def section(heading, sub, groups, bg="var(--finch-mist)"):
    """groups: list of (group_title_or_None, [(href, text), ...])"""
    cols = ""
    for gtitle, links in groups:
        if gtitle:
            cols += (
                f'<div style="font-size:0.7rem;font-weight:800;text-transform:uppercase;'
                f'letter-spacing:0.08em;color:var(--finch-forest);margin:1.25rem 0 0.5rem;">{gtitle}</div>'
            )
        cols += '<div style="display:flex;flex-wrap:wrap;gap:0.6rem;">'
        for href, text in links:
            cols += (
                f'<a href="{href}" style="display:inline-block;background:white;'
                f'border:1px solid rgba(181,206,176,0.5);border-radius:999px;'
                f'padding:0.5rem 1rem;font-size:0.85rem;font-weight:600;'
                f'color:var(--finch-forest);text-decoration:none;">{text}</a>'
            )
        cols += "</div>"
    return f"""{START}
<section style="padding:4rem 0;background:{bg};">
  <div class="container">
    <h2 style="font-family:var(--font-display);font-size:clamp(1.5rem,3vw,2rem);font-weight:700;color:var(--neutral-black);margin-bottom:0.5rem;">{heading}</h2>
    <p style="color:var(--neutral-medGray);max-width:680px;line-height:1.7;margin-bottom:1.5rem;">{sub}</p>
    {cols}
  </div>
</section>
{END}
"""


def inject(path, block):
    s = read(path)
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
    if START in s:
        s = pat.sub("", s)
    if FOOTER not in s:
        print(f"  ! no footer anchor, skipped: {os.path.relpath(path, ROOT)}")
        return False
    s = s.replace(FOOTER, block + FOOTER, 1)
    write(path, s)
    return True


# ---------------------------------------------------------------- 1. lenders.html
groups = []
for cat in CAT_ORDER:
    links = [(f"lenders/{slug}", label) for slug, label, c in reviews if c == cat]
    if links:
        groups.append((cat, links))
block = section(
    "Browse All Lender Reviews",
    "In-depth, independent reviews of every major bank, non-bank, specialist and credit-union lender we work with across New Zealand.",
    groups,
)
inject(os.path.join(ROOT, "lenders.html"), block)
print(f"lenders.html: linked {len(reviews)} reviews")

# ---------------------------------------------------------------- 2. blog.html
block = section(
    "All Guides & Articles",
    "Every Finch Mortgages guide, market explainer and regional broker page in one place.",
    [(None, [(f"blog/{slug}", label) for slug, label in blog_posts])],
    bg="white",
)
inject(os.path.join(ROOT, "blog.html"), block)
print(f"blog.html: linked {len(blog_posts)} posts")

# ---------------------------------------------------------------- 3. city pages
for slug, label in locations:
    siblings = [(s2, l2) for s2, l2 in locations if s2 != slug]
    links = [(s2, l2) for s2, l2 in siblings]
    block = section(
        "Mortgage Brokers Across New Zealand",
        "Local mortgage broker support in other regions — same independent, $0-fee advice nationwide.",
        [(None, links)],
        bg="var(--finch-mist)",
    )
    inject(os.path.join(ROOT, "blog", slug), block)
print(f"city pages: cross-linked {len(locations)} locations")

# ---------------------------------------------------------------- 4. review pages
for slug, label, cat in reviews:
    sib = [(s2, l2) for s2, l2, c2 in reviews if c2 == cat and s2 != slug]
    links = [("../lenders.html", "All Lenders Hub")] + [(s2, l2) for s2, l2 in sib]
    block = section(
        f"Compare Other {cat}",
        "See how this lender stacks up against the alternatives before you choose.",
        [(None, links)],
        bg="var(--finch-mist)",
    )
    inject(os.path.join(ROOT, "lenders", slug), block)
print(f"review pages: cross-linked {len(reviews)} reviews")

# ---------------------------------------------------------------- 5. guides
guide_links = [
    ("../calculators/mortgage-calculator.html", "Mortgage Calculator"),
    ("../calculators/borrowing-power.html", "Borrowing Power"),
    ("../calculators/extra-repayment.html", "Extra Repayment"),
    ("../lenders.html", "Compare Lenders"),
    ("../lenders/asb-mortgage-review.html", "ASB Review"),
    ("../lenders/anz-home-loan-review.html", "ANZ Review"),
    ("../lenders/kiwibank-home-loan-review.html", "Kiwibank Review"),
]
for p in sorted(glob.glob(os.path.join(ROOT, "guides", "*.html"))):
    block = section(
        "Helpful Tools & Lender Reviews",
        "Put these guides into action with our free calculators and independent lender reviews.",
        [(None, guide_links)],
        bg="white",
    )
    inject(p, block)
print(f"guides: added tool/review links")

# ---------------------------------------------------------------- 6. case studies
cases = []
for p in sorted(glob.glob(os.path.join(ROOT, "case-studies", "*.html"))):
    cases.append((os.path.basename(p), clean(title_of(p))))
block = section(
    "More Client Case Studies",
    "Real New Zealand borrowers, real outcomes — see how Finch structured each approval.",
    [(None, [(f"case-studies/{slug}", label) for slug, label in cases])],
    bg="var(--finch-mist)",
)
inject(os.path.join(ROOT, "case-studies.html"), block)
print(f"case-studies.html: linked {len(cases)} case studies")

# ---------------------------------------------------------------- 7. service-city pages (locations/)
SERVICES_META = [
    {"slug": "home-loan", "name": "Home Loan", "title": "Home Loans & Buying a Home"},
    {"slug": "first-home-buyer", "name": "First Home Buyer", "title": "First Home Buyer Mortgages"},
    {"slug": "refinance", "name": "Refinance", "title": "Refinance & Restructure Mortgage"},
    {"slug": "investment-property", "name": "Investment Property", "title": "Investment Property Loans"},
    {"slug": "self-employed", "name": "Self Employed", "title": "Self-Employed Home Loans"},
    {"slug": "pre-approval", "name": "Pre-Approval", "title": "Mortgage Pre-Approvals"},
]
SERVICE_NAMES = {s["slug"]: s["title"] for s in SERVICES_META}
SERVICE_NAME_SHORT = {s["slug"]: s["name"] for s in SERVICES_META}

# Load CITIES from city_data to get friendly display names and slugs
from city_data import CITIES
CITY_NAMES = {}
for c in CITIES:
    clean_slug = c["slug"].replace("mortgage-broker-", "")
    CITY_NAMES[clean_slug] = c["city"].replace("&amp;", "&").replace("&amp; ", "& ")

# Target cities (12 requested ones)
TARGET_CITIES = {
    "auckland-city", "wellington", "christchurch", "hamilton", "tauranga", 
    "dunedin", "queenstown", "napier-hawkes-bay", "palmerston-north", 
    "nelson", "whangarei-northland", "manukau"
}

# Parse filenames in locations/ directory
service_cities = []  # (filename, label, service_slug, city_slug)
for p in sorted(glob.glob(os.path.join(ROOT, "locations", "*.html"))):
    b = os.path.basename(p)
    if b == "index.html":
        continue
    # Find matching service prefix
    for s in SERVICE_NAME_SHORT.keys():
        if b.startswith(s + "-"):
            city_slug = b[len(s) + 1 : -5]  # remove service prefix and ".html"
            service_cities.append((b, clean(title_of(p)), s, city_slug))
            break

# Inject cross links into each locations/*.html file
for filename, label, s_slug, c_slug in service_cities:
    # Sibling Services in the same city
    sib_services = [
        (f"{s_meta['slug']}-{c_slug}.html", f"{s_meta['name']} in {CITY_NAMES.get(c_slug, c_slug)}")
        for s_meta in SERVICES_META if s_meta['slug'] != s_slug
    ]
    
    # Sibling Cities for the same service
    sib_cities = [
        (f"{s_slug}-{city_item}.html", f"{SERVICE_NAME_SHORT[s_slug]} in {CITY_NAMES.get(city_item, city_item)}")
        for city_item in TARGET_CITIES if city_item != c_slug
    ]
    
    # Matching city broker page link (e.g. blog/mortgage-broker-wellington.html)
    city_page_filename = f"mortgage-broker-{c_slug}.html"
    
    groups = [
        ("Core Service & City Guides", [
            (f"../services/{s_slug}.html", f"{SERVICE_NAMES[s_slug]} Hub"),
            (f"../blog/{city_page_filename}", f"{CITY_NAMES.get(c_slug, c_slug)} Mortgage Broker Guide")
        ]),
        (f"Other Mortgage Services in {CITY_NAMES.get(c_slug, c_slug)}", sib_services),
        (f"{SERVICE_NAMES[s_slug]} in Other NZ Cities", sib_cities)
    ]
    
    block = section(
        f"Explore Local Mortgage Services",
        "Compare home loan options, restructure your existing mortgage, or connect with our local advisers.",
        groups,
        bg="var(--finch-mist)"
    )
    
    inject(os.path.join(ROOT, "locations", filename), block)

# ---------------------------------------------------------------- 8. individual blog post cross-links
# Windowed round-robin so every post picks up multiple inbound links, not just
# the one from blog.html's hub list. City pages already get their own
# cross-linking in step 3 (same START/END markers, would be clobbered here).
location_slugs = {slug for slug, _ in locations}
non_location_posts = [(slug, label) for slug, label in blog_posts if slug not in location_slugs]
n = len(non_location_posts)
for i, (slug, label) in enumerate(non_location_posts):
    sib = [non_location_posts[(i + j) % n] for j in range(1, 5) if n > 1]
    links = [("../blog.html", "All Guides & Articles")] + [(f"../blog/{s2}", l2) for s2, l2 in sib]
    block = section(
        "Related Guides",
        "More mortgage guidance from Finch to help you plan your next move.",
        [(None, links)],
        bg="white",
    )
    inject(os.path.join(ROOT, "blog", slug), block)
print(f"blog posts: cross-linked {n} posts")

# ---------------------------------------------------------------- 9. individual case study cross-links
n = len(cases)
for i, (slug, label) in enumerate(cases):
    sib = [cases[(i + j) % n] for j in range(1, 5) if n > 1]
    links = [("../case-studies.html", "All Case Studies")] + [(f"../case-studies/{s2}", l2) for s2, l2 in sib]
    block = section(
        "Related Case Studies",
        "More real New Zealand borrower outcomes structured by Finch.",
        [(None, links)],
        bg="var(--finch-mist)",
    )
    inject(os.path.join(ROOT, "case-studies", slug), block)
print(f"case studies: cross-linked {n} case studies")

print(f"service-city pages: cross-linked {len(service_cities)} locations")

print("\nDone.")
