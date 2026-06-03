"""Generate location-based 'NZ mortgage broker [city]' pages for SEO.

Each page targets a high-search-volume NZ city/region phrase like
'mortgage broker Wellington', 'mortgage broker Christchurch' etc.

Reuses the head + footer wrappers from an existing blog page so the new
pages match the rest of the site's nav, styles, and breadcrumb structure.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "blog/mortgage-broker-north-shore.html"
OUT_DIR = ROOT / "blog"
BASE_URL = "https://www.finchmortgages.co.nz"

# ISO 8601 dates for Article schema (required for Article rich results)
ARTICLE_PUBLISHED = "2026-01-15"
ARTICLE_MODIFIED = "2026-06-03"


CITIES = [
    {
        "slug": "mortgage-broker-te-atatu",
        "city": "Te Atatu",
        "region": "Te Atatu &amp; West Auckland",
        "intro_one_liner": "Finch is based right here in Te Atatu South — a genuinely local independent NZ mortgage broker arranging home loans across Te Atatu Peninsula, Te Atatu South, Henderson, Massey, and the wider West Auckland area.",
        "suburbs": "Te Atatu South, Te Atatu Peninsula, Henderson, Massey, Glendene, Kelston, New Lynn, Green Bay, Titirangi, Ranui, Swanson, Sunnyvale, Glen Eden, Royal Heights, West Harbour, Hobsonville, Westgate, and the wider West Auckland area",
        "market_note": "West Auckland blends established post-war suburbs with fast-growing new-build corridors through Massey, Hobsonville Point, and Westgate. New builds across these areas typically qualify for the main-bank LVR exemption (10-15% deposit) and frequently for the Kāinga Ora First Home Grant, while older weatherboard and cross-lease properties in Te Atatu and Glen Eden can attract additional lender scrutiny around insulation, Healthy Homes compliance, and title type. Knowing which lender treats each property type favourably is exactly what a local broker is for.",
        "common_buyers": "first home buyers across Henderson, Massey, and Te Atatu combining KiwiSaver and the Kāinga Ora First Home Loan; growing families upgrading within West Auckland; self-employed tradespeople and small business owners; investors targeting West Auckland rental yield; refinancers rolling off higher 2022-2023 fixed terms",
        "price_band": "Te Atatu standalone homes typically $900k-$1.4m, Henderson and Massey $800k-$1.2m, West Auckland townhouses and new builds $650k-$900k, Titirangi and bush-fringe homes $1m-$1.6m+",
    },
    {
        "slug": "mortgage-broker-nz",
        "city": "New Zealand",
        "region": "Nationwide",
        "intro_one_liner": "Finch is an independent New Zealand mortgage broker arranging home loans across every NZ city, town, and rural area.",
        "suburbs": "Auckland, Wellington, Christchurch, Hamilton, Tauranga, Dunedin, Palmerston North, Napier, Nelson, Queenstown, Whangārei, Invercargill, and every region in between",
        "market_note": "Across New Zealand, mortgage policy varies sharply by region — main-bank lending depth in Auckland, seismic considerations in Wellington, EQC zoning in Canterbury, and lifestyle-block specialisation in Waikato all influence which lender wins for your scenario. As a nationwide NZ broker, Finch matches your specific city or region to the lender most likely to deliver the sharpest pre-approval.",
        "common_buyers": "first home buyers using KiwiSaver and the Kāinga Ora First Home Loan; investors building a NZ residential portfolio; self-employed business owners; refinancers rolling off higher 2022-2023 fixed terms; commercial property buyers and developers",
        "price_band": "varying widely by region — Auckland and Queenstown command the highest median sale prices, while regional NZ markets remain materially more affordable",
    },
    {
        "slug": "mortgage-broker-wellington",
        "city": "Wellington",
        "region": "Wellington & Wairarapa",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across the Wellington region — from Te Aro and Kelburn to Lower Hutt, Upper Hutt, Porirua, and the Kāpiti Coast.",
        "suburbs": "Wellington CBD, Te Aro, Mount Victoria, Kelburn, Brooklyn, Karori, Newtown, Island Bay, Miramar, Khandallah, Johnsonville, Tawa, Lower Hutt, Upper Hutt, Petone, Wainuiomata, Porirua, Whitby, Paraparaumu, Waikanae, and the wider Wellington region",
        "market_note": "Wellington's property market is shaped by seismic considerations, EPB (Earthquake-Prone Building) register exposure, and a public-sector-heavy income profile. Some NZ lenders apply additional caution to apartments above certain heights or to properties in higher-seismic zones; others lend confidently with the right documentation. Knowing which lender treats your property favourably is the difference between a clean pre-approval and a frustrating decline.",
        "common_buyers": "public-sector and Crown agency employees, contractors on Wellington-rate income, first home buyers using KiwiSaver and Kāinga Ora First Home Loan in Lower Hutt and Porirua, investors targeting solid-yield suburbs in the Hutt Valley",
        "price_band": "Wellington CBD apartments typically $500-$900k, Wellington City standalone homes $900k-$1.5m+, Lower Hutt and Porirua $700k-$1.1m, Kāpiti Coast $750k-$1.2m",
    },
    {
        "slug": "mortgage-broker-christchurch",
        "city": "Christchurch",
        "region": "Christchurch & Canterbury",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across the greater Christchurch region — from Riccarton and Merivale to Rolleston, Rangiora, and the wider Canterbury district.",
        "suburbs": "Christchurch CBD, Merivale, Fendalton, Riccarton, Ilam, Burnside, Avonhead, Hornby, Halswell, Cashmere, Sumner, New Brighton, Linwood, Aranui, Belfast, Marshland, Rolleston, Lincoln, Prebbleton, Rangiora, Kaiapoi, and the wider Canterbury region",
        "market_note": "Christchurch property assessment requires careful attention to TC (Technical Category) zoning, EQC settlement history, and post-quake repair quality. Some lenders require additional engineering reports for TC2/TC3 properties; others are comfortable with standard registered valuations. Finch knows which Canterbury suburbs and property types attract main-bank or specialist non-bank pricing.",
        "common_buyers": "first home buyers across Rolleston, Lincoln, and Halswell where new builds qualify for LVR exemption and First Home Grant; investors targeting Selwyn district yield; trades and rebuild-era owner-occupiers refinancing",
        "price_band": "Christchurch standalone homes typically $600k-$1.1m, Selwyn district new builds $700k-$950k, Rolleston townhouses $550k-$750k, central Christchurch apartments $400k-$700k",
    },
    {
        "slug": "mortgage-broker-hamilton",
        "city": "Hamilton",
        "region": "Hamilton & Waikato",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across the Hamilton and wider Waikato region — from Hamilton East and Chartwell to Cambridge, Te Awamutu, and the rural Waikato.",
        "suburbs": "Hamilton CBD, Hamilton East, Hamilton West, Hillcrest, Chartwell, Rototuna, Flagstaff, Nawton, Frankton, Dinsdale, Glenview, Te Rapa, Cambridge, Te Awamutu, Ngāruawāhia, Huntly, Morrinsville, and the rural Waikato",
        "market_note": "The Waikato market spans tight Hamilton residential, fast-growing Cambridge and Te Awamutu commuter zones, and lifestyle/rural-residential blocks. Lenders treat lifestyle blocks over 1 hectare differently from standard residential, and some prefer specific sub-regions over others. Knowing which Waikato suburb gets sharp treatment versus which needs a non-bank lender is critical.",
        "common_buyers": "first home buyers across Hamilton's growth areas and Cambridge; investors targeting student rental yield near Waikato University; dairy contractors and rural-residential lifestyle-block buyers across the Waikato",
        "price_band": "Hamilton standalone homes typically $700k-$1.1m, Cambridge $900k-$1.4m, Te Awamutu $650k-$900k, Waikato lifestyle blocks $900k-$2m+",
    },
    {
        "slug": "mortgage-broker-tauranga",
        "city": "Tauranga",
        "region": "Tauranga & Bay of Plenty",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across the Tauranga and Bay of Plenty region — from Mount Maunganui and Pāpāmoa to Bethlehem, Welcome Bay, and Te Puke.",
        "suburbs": "Tauranga CBD, Mount Maunganui, Pāpāmoa, Pāpāmoa Beach, Bethlehem, Brookfield, Welcome Bay, Greerton, Pyes Pa, Tauriko, Ōmokoroa, Katikati, Te Puke, Whakatāne, Rotorua, and the wider Bay of Plenty",
        "market_note": "Tauranga and the wider Bay of Plenty have been among NZ's fastest-growing markets, with strong new-build supply across Pāpāmoa, Bethlehem, and Tauriko. New builds qualify for the main-bank LVR exemption (10-15% deposit) and frequently for the Kāinga Ora First Home Grant. Coastal properties may face insurance complexity that influences lender appetite.",
        "common_buyers": "first home buyers across Pāpāmoa, Welcome Bay, and Bethlehem where new builds match grant caps; retirees relocating from Auckland; lifestyle-block buyers in the rural Western Bay; investors targeting kiwifruit-belt rental demand",
        "price_band": "Tauranga standalone homes typically $850k-$1.4m, Pāpāmoa $850k-$1.3m, Mount Maunganui beachside $1.2m-$2m+, Bethlehem new builds $850k-$1.1m, Rotorua $600k-$900k",
    },
    {
        "slug": "mortgage-broker-dunedin",
        "city": "Dunedin",
        "region": "Dunedin & Otago",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Dunedin and the wider Otago region — from St Clair and Roslyn to Mosgiel and the Taieri.",
        "suburbs": "Dunedin CBD, North Dunedin, Roslyn, Maori Hill, St Clair, St Kilda, Andersons Bay, Musselburgh, Caversham, South Dunedin, Mornington, Pine Hill, Mosgiel, Brighton, Outram, and the wider Otago region",
        "market_note": "Dunedin's market is shaped by the University of Otago's student rental demand, the central retail and tourism sectors, and a stock of older character properties. Some lenders apply additional scrutiny to pre-1970 weatherboard homes; others lend confidently with the right insulation and heating documentation under Healthy Homes standards.",
        "common_buyers": "first home buyers across Mosgiel and South Dunedin where price points still meet First Home Grant caps; student-rental investors near the University; refinancers across central Dunedin's heritage suburbs",
        "price_band": "Dunedin standalone homes typically $550k-$900k, North Dunedin (university zone) $600k-$850k, Mosgiel $550k-$800k, central Dunedin heritage homes $700k-$1.2m",
    },
    {
        "slug": "mortgage-broker-queenstown",
        "city": "Queenstown",
        "region": "Queenstown & Central Otago",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across the Queenstown Lakes and Central Otago region — from Queenstown and Frankton to Arrowtown, Wānaka, and Cromwell.",
        "suburbs": "Queenstown CBD, Frankton, Arthurs Point, Fernhill, Goldfield Heights, Kelvin Heights, Lake Hayes Estate, Jacks Point, Arrowtown, Wānaka, Albert Town, Lake Hāwea, Cromwell, Alexandra, Clyde, and the wider Central Otago",
        "market_note": "Queenstown Lakes property assessment is shaped by district plan controls, sloped-site engineering, and a higher proportion of holiday-home and short-term-rental buyers. Some NZ lenders apply additional caution to short-term-let dependent income or to specific Queenstown Lakes zones; others lend confidently with the right documentation. Median sale prices here are amongst the highest in NZ.",
        "common_buyers": "owner-occupiers relocating for lifestyle and remote work; holiday-home buyers; tourism and hospitality operators; investors targeting short-term rental yield; commercial property buyers across Queenstown's retail and hospitality sectors",
        "price_band": "Queenstown standalone homes typically $1.5m-$3m+, Frankton townhouses $850k-$1.4m, Wānaka standalone $1.2m-$2.5m, Cromwell $750k-$1.2m",
    },
    {
        "slug": "mortgage-broker-napier-hawkes-bay",
        "city": "Napier &amp; Hawke's Bay",
        "region": "Hawke's Bay",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across the Hawke's Bay region — from Napier and Hastings to Havelock North, Taradale, and the wider region.",
        "suburbs": "Napier, Taradale, Bay View, Greenmeadows, Marewa, Ahuriri, Westshore, Hastings, Flaxmere, Havelock North, Clive, Te Awanga, Waipawa, Waipukurau, and the wider Hawke's Bay region",
        "market_note": "Hawke's Bay property is shaped by the region's strong horticulture, viticulture, and primary-industry employment base, plus a growing population of Auckland and Wellington relocators seeking lifestyle. Some Napier waterfront and coastal properties face insurance complexity that influences lender appetite.",
        "common_buyers": "first home buyers across Hastings and Flaxmere where prices still meet First Home Grant caps; lifestyle-block buyers; relocators from Auckland and Wellington; orcharding and viticulture employees and operators",
        "price_band": "Napier standalone homes typically $700k-$1.1m, Havelock North $1m-$1.6m, Hastings $600k-$900k, Hawke's Bay lifestyle blocks $1m-$2.5m+",
    },
    {
        "slug": "mortgage-broker-palmerston-north",
        "city": "Palmerston North",
        "region": "Palmerston North &amp; Manawatū",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Palmerston North and the wider Manawatū region — from Hokowhitu and Awapuni to Feilding and the rural Manawatū.",
        "suburbs": "Palmerston North CBD, Hokowhitu, Awapuni, Cloverlea, Roslyn, Highbury, Milson, Kelvin Grove, Aokautere, Summerhill, West End, Whakarongo, Feilding, Ashhurst, Bunnythorpe, and the wider Manawatū",
        "market_note": "Palmerston North benefits from Massey University, the NZ Defence Force, and a strong primary industry base — supporting stable lending demand. Most NZ lenders treat the city as a standard residential market with sharp main-bank pricing. Lifestyle blocks in the wider Manawatū may attract different lender treatment.",
        "common_buyers": "first home buyers across Palmerston North suburbs where prices meet First Home Grant caps; NZDF and university employees; investors targeting student-rental yield near Massey; lifestyle-block buyers across the Manawatū",
        "price_band": "Palmerston North standalone homes typically $550k-$850k, Hokowhitu and Aokautere $700k-$1m, Feilding $550k-$800k, Manawatū lifestyle blocks $850k-$1.5m",
    },
    {
        "slug": "mortgage-broker-nelson",
        "city": "Nelson",
        "region": "Nelson, Tasman &amp; Marlborough",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Nelson, Tasman, and Marlborough — from central Nelson and Stoke to Richmond, Motueka, and Blenheim.",
        "suburbs": "Nelson CBD, Tāhunanui, Wakapuaka, The Wood, Atawhai, Stoke, Annesbrook, Bishopdale, Marsden Valley, Enner Glynn, Richmond, Hope, Brightwater, Wakefield, Motueka, Mapua, Tasman, Blenheim, Picton, and the wider Marlborough",
        "market_note": "Nelson and Tasman are characterised by viticulture, marine industries, and tourism, with a strong owner-occupier and lifestyle-block lending market. Most NZ lenders price Nelson sharply as a standard residential market. Marlborough lifestyle and vineyard blocks may require specialist commercial-residential hybrid lending where main banks decline.",
        "common_buyers": "first home buyers across Nelson, Stoke, and Richmond; lifestyle-block buyers across Tasman and Marlborough; viticulture and marine industry operators; relocators from Wellington and Christchurch seeking lifestyle",
        "price_band": "Nelson standalone homes typically $700k-$1.1m, Stoke and Richmond $650k-$950k, Motueka $650k-$900k, Marlborough vineyard blocks $1.2m-$3m+",
    },
    {
        "slug": "mortgage-broker-whangarei-northland",
        "city": "Whangārei &amp; Northland",
        "region": "Whangārei &amp; Northland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Whangārei and the wider Northland region — from Whangārei Heads and Onerahi to Kerikeri, Paihia, and Kaitāia.",
        "suburbs": "Whangārei CBD, Onerahi, Tikipunga, Kamo, Maunu, Otaika, Riverside, Avenues, Whangārei Heads, Tutukaka, Ngunguru, Kerikeri, Paihia, Kawakawa, Kaikohe, Kaitāia, and the wider Northland region",
        "market_note": "Whangārei and Northland benefit from a steady stream of Auckland relocators and lifestyle buyers. Most NZ lenders treat Whangārei as a standard residential market with sharp pricing. Remote rural-residential properties further north may attract additional valuation scrutiny — knowing which lender comfortable on which property type matters.",
        "common_buyers": "first home buyers across Whangārei and Kerikeri; Auckland relocators seeking lifestyle and value; investors targeting Whangārei rental yield; lifestyle-block buyers across the Bay of Islands and mid-Northland",
        "price_band": "Whangārei standalone homes typically $650k-$950k, Onerahi and Tikipunga $600k-$850k, Kerikeri $750k-$1.2m, Bay of Islands lifestyle blocks $900k-$2m+",
    },
]


def title_for(c: dict) -> str:
    # Kept under 60 characters so titles don't truncate in SERPs.
    if c["slug"] == "mortgage-broker-nz":
        return "Mortgage Broker NZ | Independent NZ-Wide Broker | Finch"
    return f"Mortgage Broker {c['city']} | Finch Mortgages NZ"


def description_for(c: dict) -> str:
    # Trimmed to land near the 150-160 character SERP sweet spot.
    if c["slug"] == "mortgage-broker-nz":
        return (
            "Independent NZ mortgage broker — Finch arranges home loans across 20+ NZ lenders for "
            "buyers anywhere in New Zealand. Free advice, $0 broker fee, fast pre-approvals."
        )
    return (
        f"Independent {c['city']} mortgage broker — Finch compares 20+ NZ lenders to find local "
        f"buyers the sharpest rate and structure. Free advice, $0 broker fee."
    )


def keywords_for(c: dict) -> str:
    city = c["city"].replace("&amp;", "&")
    base = [
        f"mortgage broker {city}",
        f"{city} mortgage broker",
        f"{city} home loan",
        f"home loan broker {city}",
        f"best mortgage broker {city}",
        f"{city} mortgage advice",
        f"{city} mortgage rates",
        "NZ mortgage broker",
        "independent mortgage broker NZ",
        "free mortgage broker NZ",
        "NZ home loan broker",
    ]
    return ", ".join(base)


def schema_for(c: dict) -> str:
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog.html"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"Mortgage Broker {c['city'].replace('&amp;', '&')}",
                "item": f"{BASE_URL}/blog/{c['slug']}.html",
            },
        ],
    }
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"Mortgage Broker {c['city'].replace('&amp;', '&')} — Independent NZ Advice",
        "description": description_for(c),
        "url": f"{BASE_URL}/blog/{c['slug']}.html",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}/blog/{c['slug']}.html"},
        "inLanguage": "en-NZ",
        "image": f"{BASE_URL}/images/finch-logo.png",
        "datePublished": ARTICLE_PUBLISHED,
        "dateModified": ARTICLE_MODIFIED,
        "author": {
            "@type": "Person",
            "@id": f"{BASE_URL}/#mukhtar-kiyani",
            "name": "Mukhtar Kiyani",
            "jobTitle": "Founder & Mortgage Adviser",
            "url": f"{BASE_URL}/about.html",
        },
        "publisher": {
            "@type": "MortgageBroker",
            "@id": f"{BASE_URL}/#organization",
            "name": "Finch Mortgages",
            "url": f"{BASE_URL}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/finch-logo.png"},
        },
        "about": {
            "@type": "Service",
            "name": f"Mortgage broker in {c['city'].replace('&amp;', '&')}",
            "areaServed": {"@type": "Place", "name": c["region"]},
        },
    }
    return (
        "<script type=\"application/ld+json\">"
        + json.dumps(breadcrumb, indent=2)
        + "</script>\n<script type=\"application/ld+json\">"
        + json.dumps(article, indent=2)
        + "</script>"
    )


def main_body(c: dict) -> str:
    city = c["city"]
    region = c["region"]
    return textwrap.dedent(f"""
    <main style="padding-top:80px;">
    <!-- Hero -->
    <section class="container page-hero" style="padding-top:4rem;padding-bottom:4rem;">
      <div class="reveal" style="max-width:800px;">
        <nav class="breadcrumb"><a href="../index.html">Home</a><span class="breadcrumb-sep">/</span><a href="../blog.html">Blog</a><span class="breadcrumb-sep">/</span><span>Mortgage Broker {city}</span></nav>
        <div class="page-hero-tag">Local NZ Coverage · {region}</div>
        <h1>Mortgage Broker<br/><em style="font-style:italic;color:var(--finch-forest);">{city}.</em></h1>
        <p>{c['intro_one_liner']}</p>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
          <a class="btn-primary" href="../contact.html">Book a Free 15-Minute Call</a>
          <a class="btn-secondary" href="../mortgage-rates.html">View Live NZ Rates</a>
        </div>
      </div>
    </section>

    <!-- Body -->
    <section style="padding:4rem 0;background:var(--finch-mist);">
      <div class="container" style="max-width:800px;">
        <div class="prose" style="color:var(--neutral-medGray);line-height:1.8;font-size:1.05rem;">
          <h2 style="font-size:2rem;font-weight:700;color:var(--neutral-black);margin-bottom:1.5rem;font-family:var(--font-display);letter-spacing:-0.02em;">Why You Need an Independent Mortgage Broker in {city}</h2>
          <p style="margin-bottom:2rem;">Walking directly into your own bank limits your options to that single lender's pricing, scorecard, and product range. As an independent NZ mortgage broker covering {region}, Finch compares your scenario across the full panel of <strong>ANZ, ASB, BNZ, Westpac, Kiwibank, TSB, SBS, The Co-operative Bank, Heartland</strong>, plus specialist non-bank lenders including <strong>Resimac, Pepper Money, Avanti Finance, Liberty Financial, Basecorp, and Bluestone</strong>. Because each NZ lender's policy, test rate, and credit appetite differs week-to-week, knowing which one wins for your specific situation can be the difference between a clean approval at a sharp rate and a frustrating decline.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">{city} &amp; {region} — Local Market Notes</h3>
          <p style="margin-bottom:2rem;">{c['market_note']}</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Suburbs &amp; Areas We Cover Across {region}</h3>
          <p style="margin-bottom:2rem;">We arrange mortgages for clients across {c['suburbs']}.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Who Finch Helps in {city}</h3>
          <p style="margin-bottom:2rem;">Our typical {city} clients include {c['common_buyers']}. We work with PAYE professionals and complex self-employed scenarios alike, including LTCs, trusts, and partnership entities — and we know which NZ lender's scorecard treats each scenario most favourably.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Typical {city} Property Price Bands (2026)</h3>
          <p style="margin-bottom:2rem;">{c['price_band']}. Knowing which deposit pathway works best for each band — Kāinga Ora First Home Loan, family guarantee, new-build LVR exemption, or standard 20% deposit — is part of how we match you to the right lender.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">How the Finch Process Works for {city} Buyers</h3>
          <ol style="margin-bottom:2rem;padding-left:1.5rem;list-style:decimal;">
            <li style="margin-bottom:0.5rem;"><strong>Free 15-minute discovery call</strong> — by phone or Zoom, no obligation.</li>
            <li style="margin-bottom:0.5rem;"><strong>Document gathering</strong> — we send you a tailored checklist for {city}.</li>
            <li style="margin-bottom:0.5rem;"><strong>Lender match</strong> — we model your scenario across every NZ lender and recommend the strongest 1-2 options.</li>
            <li style="margin-bottom:0.5rem;"><strong>Pre-approval</strong> — typically issued within 5-10 working days for clean scenarios.</li>
            <li style="margin-bottom:0.5rem;"><strong>House hunting in {city}</strong> — bid at auction or negotiate by private treaty with certainty.</li>
            <li style="margin-bottom:0.5rem;"><strong>Full approval &amp; settlement</strong> — typically 4-6 weeks from accepted offer.</li>
            <li style="margin-bottom:0.5rem;"><strong>Ongoing reviews</strong> — at every fixed-term roll-off and annually.</li>
          </ol>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">What Finch Costs (Spoiler: $0 to You)</h3>
          <p style="margin-bottom:2rem;">For residential home loans, Finch charges you nothing. We are paid by the lender on settlement — not by you. That fee comes from the bank's distribution budget and would otherwise stay with the bank if you walked in direct. Our independent broker obligations under the Financial Markets Conduct Act mean we are legally required to act in your best interest, not the lender's. We hold FSP1011206 (FSPR FSP1011125) and are subject to NZ regulatory oversight.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">First Home Buyer Support in {city}</h3>
          <p style="margin-bottom:2rem;">We specialise in helping {city} first home buyers combine every available NZ deposit pathway — KiwiSaver withdrawal (after 3 years of contributions), the <a href="https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Kāinga Ora First Home Loan</a> (5% deposit through Westpac, Kiwibank, SBS, The Co-operative Bank), family guarantees, and new-build LVR exemption set by the <a href="https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions" target="_blank" rel="noopener" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">Reserve Bank's LVR rules</a>. Most first home buyers find their effective deposit goes much further than they expected once we layer these properly. Read the full <a href="../guides/first-home-guide.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">NZ first home buyer guide</a>.</p>

          <h3 style="font-size:1.35rem;font-weight:700;color:var(--finch-forest);margin-bottom:1rem;margin-top:2.5rem;">Refinance &amp; Restructure for {city} Homeowners</h3>
          <p style="margin-bottom:1rem;">If your fixed term is rolling off in the next 60 days, you're paying the loyalty tax. Refinancing through Finch typically captures a sharper rate plus 0.50-0.90% cashback (up to $20,000 depending on lender and loan size). We model your full economics — break fees, cashback clawback on existing loan, new cashback, legal costs — before recommending any move. Use our <a href="../calculators/refinance-savings.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:600;">refinance savings calculator</a> to ballpark the benefit.</p>
        </div>
      </div>
    </section>

    <!-- Related NZ Resources -->
    <section style="padding:4rem 0;background:white;">
      <div class="container" style="max-width:1000px;">
        <div class="section-label"><span>Keep Reading</span></div>
        <h2 class="section-heading" style="margin-bottom:2.5rem;">Related NZ mortgage resources</h2>
        <div class="cols-3" style="gap:1.5rem;">
          <a href="../services/home-loan.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Home Loan Service</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Independent advice across 20+ NZ lenders.</span></a>
          <a href="../calculators/borrowing-power.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Borrowing Power</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">See how much NZ banks will lend you.</span></a>
          <a href="../calculators/mortgage-calculator.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Mortgage Calculator</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Estimate repayments at NZ rates.</span></a>
          <a href="../guides/first-home-guide.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ First Home Buyer Guide</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Complete NZ FHB playbook.</span></a>
          <a href="../mortgage-rates.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">Live NZ Mortgage Rates</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">Current carded and broker rates.</span></a>
          <a href="../lenders.html" style="display:block;padding:1.5rem;background:var(--finch-mist);border-radius:1rem;text-decoration:none;color:var(--neutral-black);"><strong style="display:block;color:var(--finch-forest);margin-bottom:0.5rem;">NZ Lender Directory</strong><span style="font-size:0.9rem;color:var(--neutral-medGray);">All 20+ NZ lenders reviewed.</span></a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section style="padding:5rem 0;">
      <div class="container">
        <div class="cta-section reveal">
          <h2>Ready to talk to a<br/>{city} mortgage broker?</h2>
          <p>Book a free 15-minute consultation. No obligation, no cost — just honest NZ-specific advice.</p>
          <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
            <a class="btn-cta-white" href="../contact.html">Book a Free Call →</a>
            <a class="btn-cta-outline" href="../mortgage-rates.html">View Live NZ Rates</a>
          </div>
        </div>
      </div>
    </section>
    </main>
    """)


def build_page(c: dict, template_text: str) -> str:
    head_close = template_text.find("</head>")
    head = template_text[:head_close]

    title = title_for(c)
    description = description_for(c)
    canonical = f"{BASE_URL}/blog/{c['slug']}.html"
    keywords = keywords_for(c)
    schema = schema_for(c)

    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"description\"/?>',
        f'<meta content="{description}" name="description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<link href=\"https://www\.finchmortgages\.co\.nz/blog/[^\"]+\" rel=\"canonical\"/?>',
        f'<link href="{canonical}" rel="canonical"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"keywords\"/?>',
        f'<meta content="{keywords}" name="keywords"/>',
        head,
    )
    head = re.sub(
        r"<script type=\"application/ld\+json\">.*?</script>",
        lambda _m: schema,
        head,
        count=1,
        flags=re.S,
    )
    head += "</head>"

    main_close = template_text.find("</main>")
    footer = template_text[main_close + len("</main>"):]

    template_body_start = template_text.find("<body>")
    template_main_start = template_text.find("<main")
    body_open = template_text[template_body_start: template_main_start]

    return head + "\n" + body_open + main_body(c) + footer


def main() -> None:
    template_text = TEMPLATE.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for c in CITIES:
        out_path = OUT_DIR / f"{c['slug']}.html"
        out_path.write_text(build_page(c, template_text), encoding="utf-8")
        print(f"  + {out_path.relative_to(ROOT)}")

    print()
    print(f"Generated {len(CITIES)} city broker pages.")


if __name__ == "__main__":
    main()
