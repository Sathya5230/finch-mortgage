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
ARTICLE_MODIFIED = "2026-07-03"

# Slugs to (re)generate when run directly. Keep this scoped to newly added
# entries -- existing pages accumulate hand edits (FAQ schema tweaks, freshness
# copy) after generation, and a full re-run would blow those away.
NEW_SLUGS = {
    "mortgage-broker-rotorua",
    "mortgage-broker-new-plymouth-taranaki",
    "mortgage-broker-invercargill-southland",
    "mortgage-broker-whanganui",
    "mortgage-broker-gisborne",
    "mortgage-broker-masterton-wairarapa",
    "mortgage-broker-pukekohe-franklin",
    "mortgage-broker-orewa-hibiscus-coast",
}

FAQ_SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How does a local mortgage broker help me in my region?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A local broker understands regional market conditions, localized bank valuation hurdles (like seismic registers or land classifications), and coordinates with local real estate agents and solicitors to speed up pre-approval."
      }
    },
    {
      "@type": "Question",
      "name": "Do I have to pay a fee to use a mortgage broker in NZ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. For standard residential home loans, our services are 100% free to the client. The chosen lender pays us a commission upon settlement, which doesn't increase your interest rate or loan fees."
      }
    },
    {
      "@type": "Question",
      "name": "Can a broker negotiate a better interest rate than a bank direct?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Banks reserve their sharpest rate discounts and cashback contributions for the broker channel. A broker compares 20+ lenders side-by-side to construct a competitive rate package you won't get walking in direct."
      }
    },
    {
      "@type": "Question",
      "name": "How does a family guarantee work to buy a home?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A family guarantee allows parents to secure up to 20% of your home loan against the equity in their own property. This bridges your deposit gap without requiring parents to give you cash, avoiding low-equity bank premiums."
      }
    }
  ]
}
</script>"""


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
    {
        "slug": "mortgage-broker-henderson",
        "city": "Henderson",
        "region": "Henderson &amp; West Auckland",
        "intro_one_liner": "Finch is based right next door in Te Atatu South — a genuinely local independent NZ mortgage broker arranging home loans for buyers across Henderson, Henderson Valley, and the wider West Auckland corridor.",
        "suburbs": "Henderson, Henderson Valley, Oratia, Sturges Road, Falls Park, Corban Estate, Sunnyvale, Glen Eden, Glendene, Te Atatu South, Massey, and the wider West Auckland area",
        "market_note": "Henderson is West Auckland's commercial and transport hub, with a mix of established 1960s-90s standalone homes, newer townhouse developments near the town centre, and lifestyle-leaning properties in Henderson Valley. New-build townhouses close to the train station typically qualify for the main-bank LVR exemption (10-15% deposit) and often the Kāinga Ora First Home Grant, while older cross-lease and character homes further out can attract closer lender scrutiny on title type and condition.",
        "common_buyers": "first home buyers combining KiwiSaver and the Kāinga Ora First Home Loan on Henderson townhouses; growing families upgrading from apartments into Henderson Valley; self-employed tradespeople based in the West Auckland industrial zone; investors targeting Henderson's rental yield relative to central Auckland",
        "price_band": "Henderson standalone homes typically $850k-$1.2m, Henderson Valley lifestyle properties $1.1m-$1.8m, new-build townhouses near the town centre $650k-$900k",
    },
    {
        "slug": "mortgage-broker-glenfield",
        "city": "Glenfield",
        "region": "Glenfield &amp; the North Shore",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Glenfield and the wider North Shore — from Wairau Valley and Sunnynook to Marlborough and Bayview.",
        "suburbs": "Glenfield, Wairau Valley, Sunnynook, Marlborough, Bayview, Hillcrest, Northcote, Beach Haven, Birkdale, Birkenhead, Albany, and the wider North Shore",
        "market_note": "Glenfield offers some of the North Shore's more accessible standalone-home price points, with a mix of 1970s-90s brick-and-tile homes and newer infill townhouses near Glenfield Mall and the Wairau industrial precinct. Some lenders price standalone Glenfield homes on par with wider Shore suburbs, while cross-lease and older unit-title properties can see more conservative valuations.",
        "common_buyers": "first home buyers priced out of Takapuna and Albany looking to Glenfield's relative affordability; families upgrading from apartments; North Shore tradespeople and Wairau Valley business owners; refinancers rolling off higher 2022-2023 fixed terms",
        "price_band": "Glenfield standalone homes typically $950k-$1.35m, Glenfield/Sunnynook townhouses $700k-$950k, Bayview and Beach Haven $900k-$1.3m",
    },
    {
        "slug": "mortgage-broker-flat-bush",
        "city": "Flat Bush",
        "region": "Flat Bush &amp; South-East Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Flat Bush and the fast-growing South-East Auckland corridor — from Ormiston and Flat Bush Stonefields to Botany and Dannemora.",
        "suburbs": "Flat Bush, Ormiston, Flat Bush Stonefields, Barry Curtis, Dannemora, Botany Downs, East Tāmaki, Chapel Downs, and the wider South-East Auckland area",
        "market_note": "Flat Bush is one of Auckland's largest master-planned new-build communities, with most housing stock built in the last 15 years across a mix of standalone homes, terraces, and apartments. The high proportion of genuine new builds means many Flat Bush purchases qualify for the main-bank LVR exemption (10-15% deposit) and the Kāinga Ora First Home Grant, but body-corporate terrace developments can carry additional lender due diligence on the body-corp financials.",
        "common_buyers": "first home buyers and young families targeting Flat Bush's new-build LVR exemption; investors drawn to strong rental demand near the Ormiston town centre and schools; multicultural extended families using pooled deposits and family guarantees; professionals commuting via the Southern or South-Eastern motorways",
        "price_band": "Flat Bush standalone new builds typically $1m-$1.5m, terraces and townhouses $750k-$1.05m, apartments $550k-$800k",
    },
    {
        "slug": "mortgage-broker-albany",
        "city": "Albany",
        "region": "Albany &amp; the Upper North Shore",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Albany and the upper North Shore — from the Albany business district and North Harbour to Rosedale, Fairview Heights, and Schnapper Rock.",
        "suburbs": "Albany, North Harbour, Rosedale, Fairview Heights, Schnapper Rock, Unsworth Heights, Greenhithe, Pinehill, Oteha, and the wider upper North Shore",
        "market_note": "Albany combines a major commercial and retail hub with newer master-planned residential pockets, so lender treatment varies significantly by property type — established 1990s-2000s standalone homes are priced conventionally, while newer terraces and apartments near the town centre are often assessed as new-build stock eligible for the LVR exemption.",
        "common_buyers": "young professionals working in the Albany business district buying their first apartment or terrace; families targeting Albany's school zones; investors drawn to Albany's rental demand from Massey University Albany students and North Harbour employees",
        "price_band": "Albany standalone homes typically $1.1m-$1.6m, terraces and townhouses $800k-$1.1m, apartments $550k-$800k",
    },
    {
        "slug": "mortgage-broker-massey",
        "city": "Massey",
        "region": "Massey &amp; West Auckland",
        "intro_one_liner": "Finch is based right nearby in Te Atatu South — a genuinely local independent NZ mortgage broker arranging home loans for buyers across Massey, Royal Heights, and the wider West Auckland growth corridor.",
        "suburbs": "Massey, Royal Heights, West Harbour, Ranui, Swanson, Red Hills, Fred Taylor Drive corridor, Westgate, and the wider West Auckland area",
        "market_note": "Massey spans established 1970s-90s family suburbs alongside significant new-build development around Westgate and the Fred Taylor Drive corridor. Genuine new builds in these growth pockets typically qualify for the main-bank LVR exemption and Kāinga Ora First Home Grant, while older Massey housing stock is treated as standard existing-property lending.",
        "common_buyers": "first home buyers combining KiwiSaver and the First Home Loan on Massey and Westgate new builds; families upgrading within West Auckland; tradespeople and small business owners based near the Westgate commercial precinct",
        "price_band": "Massey standalone homes typically $850k-$1.2m, new-build terraces near Westgate $700k-$950k, Royal Heights and West Harbour $900k-$1.3m",
    },
    {
        "slug": "mortgage-broker-hobsonville",
        "city": "Hobsonville",
        "region": "Hobsonville &amp; West Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Hobsonville Point and the wider Hobsonville area — one of Auckland's premier master-planned waterfront new-build communities.",
        "suburbs": "Hobsonville Point, Hobsonville, Scott Point, Catalina Bay, Buckley Park, Whenuapai, Westgate, and the wider West Auckland coastal corridor",
        "market_note": "Hobsonville Point is almost entirely new-build stock developed over the past decade, so the large majority of purchases qualify for the main-bank LVR exemption (10-15% deposit) and frequently the Kāinga Ora First Home Grant. Because many homes sit within managed covenant developments, some lenders also want sight of the design covenant and body-corporate documents before issuing unconditional approval.",
        "common_buyers": "first home buyers and young families targeting Hobsonville's new-build LVR exemption and walkable master-planned amenities; professionals working in the Westgate/Hobsonville commercial precinct; downsizers moving from larger sections into low-maintenance terraces",
        "price_band": "Hobsonville Point terraces and townhouses typically $850k-$1.2m, standalone homes $1.2m-$1.8m, apartments $650k-$900k",
    },
    {
        "slug": "mortgage-broker-new-lynn",
        "city": "New Lynn",
        "region": "New Lynn &amp; West Auckland",
        "intro_one_liner": "Finch is based nearby in Te Atatu South — a genuinely local independent NZ mortgage broker arranging home loans for buyers across New Lynn, Avondale, and the wider West Auckland transport corridor.",
        "suburbs": "New Lynn, Avondale, Blockhouse Bay, Kelston, Green Bay, Titirangi, Glen Eden, and the wider West Auckland area",
        "market_note": "New Lynn's transformation into a transit-oriented town centre has brought a wave of apartment and terrace development around the train station, alongside its traditional stock of standalone bungalows and 1960s-80s family homes. Lenders generally treat New Lynn's new-build apartments as standard urban intensification stock, with LVR exemption eligibility depending on build date and title type.",
        "common_buyers": "first home buyers targeting New Lynn's apartments and terraces for train-line convenience; families in Blockhouse Bay and Kelston upgrading within budget; investors drawn to New Lynn's rental demand near the town centre and transport hub",
        "price_band": "New Lynn standalone homes typically $950k-$1.3m, terraces and townhouses $700k-$950k, apartments $500k-$750k",
    },
    {
        "slug": "mortgage-broker-mt-roskill",
        "city": "Mt Roskill",
        "region": "Mt Roskill &amp; Central Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Mt Roskill and the wider Central Auckland isthmus — from Wesley and Three Kings to Hillsborough and Waikowhai.",
        "suburbs": "Mt Roskill, Wesley, Three Kings, Hillsborough, Waikowhai, Lynfield, May Road, and the wider central-west Auckland isthmus",
        "market_note": "Mt Roskill sits on the central isthmus and blends its long-standing stock of 1940s-70s bungalows and state houses with newer medium-density housing developed through recent urban regeneration. Character and pre-1960s homes can require additional documentation around Healthy Homes compliance, while newer terrace developments are typically assessed as standard urban infill.",
        "common_buyers": "first home buyers targeting Mt Roskill's relative central-Auckland affordability; families in multicultural, multi-generational households using pooled deposits; investors drawn to strong rental demand given the isthmus location and transport links",
        "price_band": "Mt Roskill standalone homes typically $1.05m-$1.5m, new-build terraces $800k-$1.1m, older units $600k-$850k",
    },
    {
        "slug": "mortgage-broker-manukau",
        "city": "Manukau",
        "region": "Manukau &amp; South Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Manukau and the wider South Auckland metro area — from the Manukau city centre to Wiri, Māngere East, and Homai.",
        "suburbs": "Manukau, Manukau Heights, Wiri, Māngere East, Homai, Clendon Park, Papatoetoe, Otara, and the wider South Auckland metro area",
        "market_note": "Manukau is South Auckland's commercial and civic hub, surrounded by established family suburbs with generally more accessible price points than central Auckland. Lenders serving Manukau range from all four main banks through to non-bank specialists who focus on lower-deposit and non-standard-income scenarios, which is where local broker knowledge of scorecard fit matters most.",
        "common_buyers": "first home buyers using KiwiSaver and the Kāinga Ora First Home Loan across Manukau's more affordable suburbs; multicultural and multi-generational families using pooled deposits and family guarantees; self-employed small business owners; investors targeting South Auckland rental yield",
        "price_band": "Manukau-area standalone homes typically $750k-$1.05m, Papatoetoe and Homai $700k-$950k, new-build terraces $600k-$850k",
    },
    {
        "slug": "mortgage-broker-papakura",
        "city": "Papakura",
        "region": "Papakura &amp; Southern Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Papakura and the southern Auckland rail corridor — from Papakura town centre to Takanini, Drury, and Karaka.",
        "suburbs": "Papakura, Takanini, Drury, Opaheke, Red Hill, Karaka, Ardmore, Rosehill, and the wider southern Auckland growth corridor",
        "market_note": "Papakura and the Takanini-Drury corridor form one of Auckland's fastest-growing new-build areas, driven by the southern motorway and rail upgrades. A high proportion of new-build terraces and standalone homes here qualify for the main-bank LVR exemption and Kāinga Ora First Home Grant, while Karaka's larger lifestyle sections attract a different lending assessment around land use and zoning.",
        "common_buyers": "first home buyers targeting Papakura and Takanini's new-build LVR exemption pricing; families relocating south for larger sections at accessible prices; lifestyle-block buyers in Karaka and Ardmore; investors targeting the southern growth corridor's rental demand",
        "price_band": "Papakura standalone homes typically $750k-$1.05m, Takanini and Drury new builds $750k-$1m, Karaka lifestyle properties $1.3m-$2.2m+",
    },
    {
        "slug": "mortgage-broker-botany",
        "city": "Botany",
        "region": "Botany &amp; East Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Botany and the wider East Auckland retail and residential corridor — from Botany Downs and Golflands to Somerville and Pakuranga.",
        "suburbs": "Botany, Botany Downs, Golflands, Somerville, Pakuranga, Pakuranga Heights, Highland Park, Bucklands Beach, and the wider East Auckland area",
        "market_note": "Botany is East Auckland's main retail and commercial hub, surrounded by well-established family suburbs built mainly from the 1980s-2000s, plus newer infill development. Most Botany-area properties are assessed as standard existing-dwelling lending, with lenders generally comfortable across the area given consistent, stable demand.",
        "common_buyers": "families targeting Botany's school zones and retail amenity; first home buyers in Golflands and Somerville's more accessible price points; East Auckland professionals commuting via the Pakuranga and Ti Rakau corridors; investors drawn to consistent East Auckland rental demand",
        "price_band": "Botany-area standalone homes typically $1.1m-$1.5m, Golflands and Somerville townhouses $800k-$1.1m, Pakuranga units $600k-$850k",
    },
    {
        "slug": "mortgage-broker-howick",
        "city": "Howick",
        "region": "Howick &amp; East Auckland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Howick and the wider East Auckland coastal suburbs — from Howick village and Cockle Bay to Half Moon Bay and Beachlands.",
        "suburbs": "Howick, Cockle Bay, Half Moon Bay, Bucklands Beach, Shelly Park, Mellons Bay, Beachlands, Maraetai, and the wider East Auckland coastal corridor",
        "market_note": "Howick and its surrounding coastal suburbs feature a strong stock of established character and 1970s-2000s standalone homes with harbour proximity, which typically carry premium pricing relative to inland East Auckland. Lenders assess these areas as stable, well-established residential markets, though waterfront and cliff-edge properties can require additional valuation and insurance documentation.",
        "common_buyers": "families and professionals targeting Howick's school zones and coastal lifestyle; downsizers moving from larger sections into townhouses near the village; investors targeting long-term capital growth in established East Auckland suburbs",
        "price_band": "Howick standalone homes typically $1.2m-$1.8m, Cockle Bay and Shelly Park waterfront-adjacent $1.4m-$2.2m+, Beachlands and Maraetai $950k-$1.5m",
    },
    {
        "slug": "mortgage-broker-takapuna",
        "city": "Takapuna",
        "region": "Takapuna &amp; the North Shore",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans for buyers across Takapuna and the central North Shore — from Takapuna Beach and Hauraki to Milford, Forrest Hill, and Northcote Point.",
        "suburbs": "Takapuna, Hauraki, Milford, Forrest Hill, Sunnynook, Northcote Point, Bayswater, Belmont, Devonport, and the wider central North Shore",
        "market_note": "Takapuna is one of the North Shore's premium beachside markets, combining high-value standalone homes with a growing stock of apartments and terraces near the town centre and beachfront. Given the higher price points, main-bank test-rate serviceability and the size of the required deposit are usually the binding constraint rather than property type — a scenario where comparing lender policy on high-value lending pays off.",
        "common_buyers": "professionals and business owners targeting Takapuna's beachside lifestyle and school zones; downsizers moving from larger Devonport or Belmont villas into low-maintenance apartments; investors targeting premium North Shore rental demand; high-net-worth refinancers restructuring larger loans",
        "price_band": "Takapuna standalone homes typically $1.8m-$3m+, Milford and Hauraki $1.4m-$2.2m, Takapuna apartments and terraces $700k-$1.4m",
    },
    {
        "slug": "mortgage-broker-rotorua",
        "city": "Rotorua",
        "region": "Rotorua &amp; the Central North Island",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Rotorua and the wider central North Island — from Rotorua's lakeside suburbs to Tokoroa, Taupō, and the surrounding districts.",
        "suburbs": "Rotorua CBD, Glenholme, Fenton Park, Springfield, Ngongotahā, Western Heights, Lynmore, Owhata, Hillcrest, Tokoroa, Taupō, and the wider central North Island",
        "market_note": "Rotorua's economy centres on geothermal tourism, forestry, and a significant Māori tourism and cultural sector, giving it a different buyer profile from the coastal Bay of Plenty. Housing is generally more affordable than Tauranga, with a mix of established lakeside suburbs and newer subdivisions on the city's edges. Some lenders apply extra caution to properties on geothermal-affected land or with ground-stability history — knowing which lender is comfortable with which pocket of Rotorua matters here more than in most NZ cities.",
        "common_buyers": "first home buyers taking advantage of Rotorua's relative affordability versus coastal BOP; tourism and hospitality sector workers; forestry contractors and Tokoroa-based buyers; investors targeting Rotorua's steady rental demand from tourism-sector and seasonal workers",
        "price_band": "Rotorua standalone homes typically $550k-$850k, lakeside and Lynmore properties $700k-$1.1m, Tokoroa $350k-$550k, Taupō lakeside $800k-$1.4m",
    },
    {
        "slug": "mortgage-broker-new-plymouth-taranaki",
        "city": "New Plymouth &amp; Taranaki",
        "region": "Taranaki",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across New Plymouth and the wider Taranaki region — from the city centre and coastal suburbs to Waitara, Inglewood, Stratford, and Hāwera.",
        "suburbs": "New Plymouth CBD, Fitzroy, Merrilands, Vogeltown, Westown, Bell Block, Waitara, Inglewood, Oakura, Ōkato, Stratford, Hāwera, and the wider Taranaki region",
        "market_note": "Taranaki's economy has long been anchored by the oil and gas sector alongside a strong dairy farming base, with New Plymouth increasingly diversifying into renewable energy and tech. This mixed economic base means lenders often see a wide income spread — from high-earning energy-sector contractors to dairy farm owners and lifestyle-block buyers — each assessed quite differently depending on the lender's rural and contractor-income policies.",
        "common_buyers": "energy-sector contractors and engineers on strong but sometimes project-based income; dairy farmers and rural-sector buyers across the wider Taranaki plains; first home buyers in New Plymouth's more accessible eastern suburbs; lifestyle-block buyers around Ōkato and Inglewood",
        "price_band": "New Plymouth standalone homes typically $650k-$950k, coastal Fitzroy and Oakura $800k-$1.3m, Waitara and Inglewood $500k-$750k, Taranaki dairy and lifestyle blocks $1.2m-$3m+",
    },
    {
        "slug": "mortgage-broker-invercargill-southland",
        "city": "Invercargill &amp; Southland",
        "region": "Southland",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Invercargill and the wider Southland region — from the city centre to Bluff, Gore, Winton, and the Southland plains.",
        "suburbs": "Invercargill CBD, Georgetown, Waikiwi, Otatara, Rosedale, Windsor, Bluff, Gore, Winton, Riverton, and the wider Southland region",
        "market_note": "Southland's economy is built on dairy and sheep/beef farming, aluminium smelting at Bluff, and a growing education and healthcare base — and it remains one of New Zealand's most affordable regions to buy in. That affordability means many Southland buyers reach full home ownership faster and with smaller deposits relative to income than almost anywhere else in NZ, though rural and farm-adjacent properties still need lender-specific handling for zoning and land use.",
        "common_buyers": "first home buyers benefiting from Southland's comparatively low entry prices; dairy and sheep/beef farm owners and rural contractors; healthcare and education-sector professionals relocating from higher-cost centres; investors drawn to strong rental yield relative to purchase price",
        "price_band": "Invercargill standalone homes typically $400k-$600k, Georgetown and Otatara $500k-$750k, Gore and Winton $350k-$500k, Southland lifestyle and farm blocks vary widely by land area",
    },
    {
        "slug": "mortgage-broker-whanganui",
        "city": "Whanganui",
        "region": "Whanganui &amp; the Lower North Island",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Whanganui and the surrounding lower North Island — from the riverside city centre to Castlecliff, Aramoho, and the wider Whanganui district.",
        "suburbs": "Whanganui CBD, Gonville, Castlecliff, Aramoho, Springvale, Durie Hill, St John's Hill, Marybank, and the wider Whanganui district",
        "market_note": "Whanganui's economy combines a strong arts and heritage identity with agricultural service industries and a growing base of remote workers and relocators drawn by its river setting and affordability relative to Wellington and Palmerston North. Housing stock is a mix of character villas and bungalows in the older river-side suburbs and more modern homes further out — lenders generally treat Whanganui as a stable, standard residential market.",
        "common_buyers": "first home buyers and young families drawn by Whanganui's affordability versus the wider lower North Island; remote workers and relocators from Wellington and Palmerston North; agricultural-sector employees; renovators taking on character villas in Durie Hill and St John's Hill",
        "price_band": "Whanganui standalone homes typically $450k-$700k, Durie Hill and St John's Hill character homes $550k-$850k, Castlecliff and Gonville $350k-$500k",
    },
    {
        "slug": "mortgage-broker-gisborne",
        "city": "Gisborne",
        "region": "Gisborne &amp; Tairāwhiti",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Gisborne and the wider Tairāwhiti region — from the city centre to Kaiti, Whataupoko, Wainui Beach, and the surrounding East Coast.",
        "suburbs": "Gisborne CBD, Kaiti, Whataupoko, Mangapapa, Elgin, Wainui Beach, Okitu, Te Karaka, and the wider Tairāwhiti / East Coast region",
        "market_note": "Gisborne's economy is anchored by horticulture and viticulture, forestry, and fishing, with Wainui Beach adding a lifestyle-property dimension not found in most comparably sized NZ towns. As one of the more remote regional centres, Gisborne sees less main-bank branch presence than larger cities, which is exactly where a broker who knows current lender appetite for the region adds the most value — some lenders price Gisborne sharply, others are more conservative given the East Coast's exposure to weather events.",
        "common_buyers": "first home buyers across Gisborne's more accessible inland suburbs; horticulture, viticulture, and forestry-sector employees and business owners; lifestyle and beachfront buyers around Wainui Beach and Okitu; relocators seeking East Coast lifestyle and lower entry prices",
        "price_band": "Gisborne standalone homes typically $500k-$750k, Wainui Beach and Okitu $700k-$1.2m+, Kaiti and Elgin $400k-$600k",
    },
    {
        "slug": "mortgage-broker-masterton-wairarapa",
        "city": "Masterton &amp; the Wairarapa",
        "region": "Wairarapa",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Masterton and the wider Wairarapa — from Masterton itself to Carterton, Greytown, Featherston, and Martinborough.",
        "suburbs": "Masterton CBD, Lansdowne, Solway, Te Ore Ore, Carterton, Greytown, Featherston, Martinborough, and the wider Wairarapa district",
        "market_note": "The Wairarapa has become one of the North Island's strongest relocator markets, driven by Wellington commuters using the Wairarapa rail line and buyers priced out of the capital seeking lifestyle blocks, vineyards, and character homes in towns like Greytown and Martinborough. This has pushed pricing in the boutique southern Wairarapa towns notably higher than Masterton itself, which remains the region's more affordable, practical base.",
        "common_buyers": "Wellington commuters relocating for lifestyle and using the Wairarapa rail line; lifestyle-block and small-vineyard buyers around Martinborough and Greytown; first home buyers targeting Masterton and Carterton's relative affordability; farming and rural-service sector buyers across the wider Wairarapa",
        "price_band": "Masterton standalone homes typically $600k-$850k, Carterton $600k-$900k, Greytown and Martinborough $850k-$1.4m+, Wairarapa lifestyle blocks $1m-$2.5m+",
    },
    {
        "slug": "mortgage-broker-pukekohe-franklin",
        "city": "Pukekohe &amp; Franklin",
        "region": "Pukekohe &amp; South Auckland / Franklin",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Pukekohe and the wider Franklin district — one of Auckland's fastest-growing southern growth corridors, from Pukekohe township to Paerata, Patumāhoe, Tuakau, and Waiuku.",
        "suburbs": "Pukekohe CBD, Pukekohe East, Paerata, Buckland, Patumāhoe, Tuakau, Pōkeno, Waiuku, and the wider Franklin district",
        "market_note": "Pukekohe and the Franklin district sit at the southern edge of the Auckland Council boundary, long known for market-garden and vegetable-growing land, now rapidly urbanising through large master-planned developments like Paerata Rise. New-build purchases across this growth corridor commonly qualify for the main-bank LVR exemption and Kāinga Ora First Home Grant, while established rural and lifestyle land further out is assessed under different rural-lending criteria — a distinction that matters a great deal for buyers moving between the two.",
        "common_buyers": "first home buyers and young families targeting new-build LVR exemption pricing in Paerata and Pukekohe East; commuters using the Auckland rail line extension; market-gardening and rural-sector business owners; lifestyle-block buyers around Patumāhoe and Waiuku",
        "price_band": "Pukekohe standalone homes typically $850k-$1.15m, new-build terraces in Paerata $700k-$950k, Tuakau and Pōkeno $700k-$950k, Franklin lifestyle blocks $1.2m-$2.5m+",
    },
    {
        "slug": "mortgage-broker-orewa-hibiscus-coast",
        "city": "Orewa &amp; the Hibiscus Coast",
        "region": "Hibiscus Coast &amp; Rodney",
        "intro_one_liner": "Finch is an independent NZ mortgage broker arranging home loans across Orewa and the wider Hibiscus Coast — Auckland's northern beachside growth corridor, from Orewa and Silverdale to Whangaparāoa, Millwater, and Warkworth.",
        "suburbs": "Orewa, Silverdale, Millwater, Red Beach, Whangaparāoa, Stanmore Bay, Army Bay, Gulf Harbour, Warkworth, Snells Beach, and the wider Rodney district",
        "market_note": "The Hibiscus Coast has been one of greater Auckland's fastest-growing areas, driven by the Northern Motorway extension through Ōrewa and Pūhoi and large master-planned developments around Millwater and Silverdale. New builds across these growth areas typically qualify for the main-bank LVR exemption and Kāinga Ora First Home Grant, while established beachside suburbs like Whangaparāoa and Gulf Harbour carry more of a lifestyle price premium tied to coastal and marina proximity.",
        "common_buyers": "families and first home buyers targeting new-build LVR exemption pricing in Millwater and Silverdale; retirees and downsizers moving to Orewa and Whangaparāoa for beachside lifestyle; Auckland CBD commuters using the Northern Busway extension; boating and marina-lifestyle buyers around Gulf Harbour",
        "price_band": "Orewa and Silverdale standalone homes typically $1m-$1.5m, Millwater new-build terraces $800k-$1.1m, Whangaparāoa Peninsula $950k-$1.4m, Warkworth and Snells Beach $850k-$1.3m",
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
        + "</script>\n"
        + FAQ_SCHEMA
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
        <p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: July 2026</p>
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
        r'<meta content=\"[^\"]*\" property=\"og:title\"/?>',
        f'<meta content="{title}" property="og:title"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:description\"/?>',
        f'<meta content="{description}" property="og:description"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" property=\"og:url\"/?>',
        f'<meta content="{canonical}" property="og:url"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"twitter:title\"/?>',
        f'<meta content="{title}" name="twitter:title"/>',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta content=\"[^\"]*\" name=\"twitter:description\"/?>',
        f'<meta content="{description}" name="twitter:description"/>',
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

    targets = [c for c in CITIES if c["slug"] in NEW_SLUGS]
    for c in targets:
        out_path = OUT_DIR / f"{c['slug']}.html"
        out_path.write_text(build_page(c, template_text), encoding="utf-8")
        print(f"  + {out_path.relative_to(ROOT)}")

    print()
    print(f"Generated {len(targets)} city broker pages.")


if __name__ == "__main__":
    main()
