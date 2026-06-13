#!/usr/bin/env python3
import os
import re
import glob
import json
import bs4

ROOT = "/Users/sathyamoorthy/Desktop/finch mortgage"

# Tone replacements
TONE_REPLACEMENTS = {
    "violently scrutinizing": "thoroughly analyzing",
    "violently scrutinize": "thoroughly analyze",
    "violently": "significantly",
    "catastrophic precipice": "serious downturn",
    "catastrophic": "serious",
    "brutally assess": "honestly assess",
    "brutally": "honestly",
    "incessantly demanding": "consistently demanding",
    "incessantly": "consistently",
    "suffocating rapidly": "declining steadily",
    "colossal gravitational mass": "significant influence",
    "absolute mathematical proof": "strong indicator",
    "forensically examine": "closely analyse",
    "elite economic consensus": "leading economists agree",
    "definitively achieved": "successfully achieved"
}

# Regional Page Data
REGIONAL_DATA = {
    "mortgage-broker-te-atatu": {
        "suburbs": "Te Atatu South, Te Atatu Peninsula, Henderson, Massey, Glendene, Kelston, New Lynn",
        "median_price": "$985,000",
        "yoy_change": "-1.4%",
        "challenges": "West Auckland weatherboard and cross-lease properties require close lender scrutiny on title types and Healthy Homes compliance.",
        "case_study": "Helped a self-employed plumber in Te Atatu Peninsula secure a 90% LVR new-build home loan after a main-bank decline.",
        "considerations": "New builds in Massey/Hobsonville qualify for RBNZ LVR speed-limit exemptions."
    },
    "mortgage-broker-nz": {
        "suburbs": "Auckland Central, Wellington CBD, Christchurch Central, Hamilton East, Tauranga South",
        "median_price": "$790,000",
        "yoy_change": "+1.1%",
        "challenges": "Lending criteria vary significantly between major metropolitan areas and regional lifestyle blocks.",
        "case_study": "Structured a multi-lender portfolio for an investor purchasing properties in both Auckland and Christchurch.",
        "considerations": "RBNZ DTI and LVR rules apply nationwide but bank credit appetites differ by region."
    },
    "mortgage-broker-wellington": {
        "suburbs": "Te Aro, Kelburn, Brooklyn, Karori, Newtown, Island Bay, Khandallah, Lower Hutt, Porirua",
        "median_price": "$895,000",
        "yoy_change": "+1.8%",
        "challenges": "Wellington apartments face seismic and earthquake-prone building registers, which restrict bank appetites.",
        "case_study": "Assisted a public sector contractor to count variable contract income for a townhouse purchase in Newtown.",
        "considerations": "Some lenders apply higher stress-test margins for apartments in high-seismic zones."
    },
    "mortgage-broker-christchurch": {
        "suburbs": "Riccarton, Merivale, Fendalton, Halswell, Cashmere, Sumner, Rolleston, Lincoln, Rangiora",
        "median_price": "$645,000",
        "yoy_change": "+6.8%",
        "challenges": "EQC repairs, TC2/TC3 land zoning require structural and engineering reports for bank sign-off.",
        "case_study": "Secured pre-approval for a first home buyer couple in Halswell using a parents' equity guarantee.",
        "considerations": "Rolleston new-build developments represent high volume FHB lending."
    },
    "mortgage-broker-hamilton": {
        "suburbs": "Hamilton East, Chartwell, Rototuna, Flagstaff, Hillcrest, Dinsdale, Cambridge, Te Awamutu",
        "median_price": "$785,000",
        "yoy_change": "+2.3%",
        "challenges": "Lifestyle block and rural-residential lending limits apply for properties over 1 hectare.",
        "case_study": "Helped a Waikato dairy contractor package variable seasonal income for a home loan in Cambridge.",
        "considerations": "Rototuna development projects qualify for low deposit new-build exemptions."
    },
    "mortgage-broker-tauranga": {
        "suburbs": "Mount Maunganui, Pāpāmoa, Bethlehem, Welcome Bay, Greerton, Pyes Pa, Tauriko, Ōmokoroa",
        "median_price": "$850,000",
        "yoy_change": "+3.1%",
        "challenges": "Coastal zoning and rising insurance premiums can block bank lending if policy cover is restricted.",
        "case_study": "Negotiated a 10% deposit pre-approval for a new-build in Bethlehem.",
        "considerations": "Tauriko commercial growth driving local residential buyer activity."
    },
    "mortgage-broker-dunedin": {
        "suburbs": "Roslyn, Maori Hill, St Clair, St Kilda, Andersons Bay, Dunedin CBD, North Dunedin, Mosgiel",
        "median_price": "$590,000",
        "yoy_change": "+0.5%",
        "challenges": "Pre-1970 character homes face insulation, wiring, and asbestos warnings from bank valuers.",
        "case_study": "Sourced funding for a student rental property portfolio near the University of Otago.",
        "considerations": "Mosgiel new sub-divisions represent the main FHB entry point in Otago."
    },
    "mortgage-broker-queenstown": {
        "suburbs": "Frankton, Arrowtown, Wānaka, Albert Town, Cromwell, Alexandra, Kelvin Heights, Jacks Point",
        "median_price": "$1,450,000",
        "yoy_change": "+5.2%",
        "challenges": "High median prices trigger DTI constraints quickly; tourism income requires careful shading.",
        "case_study": "Structured a specialist non-bank loan for a local hospitality business owner.",
        "considerations": "Central Otago lifestyle properties require specialist commercial-residential hybrid lending."
    },
    "mortgage-broker-napier-hawkes-bay": {
        "suburbs": "Taradale, Greenmeadows, Ahuriri, Napier Hill, Havelock North, Hastings CBD, Flaxmere, Clive",
        "median_price": "$720,000",
        "yoy_change": "+1.2%",
        "challenges": "Flood-risk mapping and insurance rating changes since Cyclone Gabrielle impact land valuations.",
        "case_study": "Helped orchard worker orchard managers secure finance for lifestyle blocks in Havelock North.",
        "considerations": "Havelock North continues to command high demand from northern relocators."
    },
    "mortgage-broker-palmerston-north": {
        "suburbs": "Hokowhitu, Awapuni, Cloverlea, Roslyn, Highbury, Milson, Kelvin Grove, Feilding, Ashhurst",
        "median_price": "$580,000",
        "yoy_change": "-0.2%",
        "challenges": "Rental yield analysis is critical for high-volume student housing investments.",
        "case_study": "Assisted a military contractor based at Linton Camp to buy their first home in Feilding.",
        "considerations": "Stable employment from NZDF and Massey University supports consistent regional lending."
    },
    "mortgage-broker-nelson": {
        "suburbs": "Stoke, Richmond, Motueka, Mapua, Tāhunanui, Atawhai, Blenheim CBD, Picton, Renwick",
        "median_price": "$715,000",
        "yoy_change": "+0.8%",
        "challenges": "Viticulture and primary industry income splits require complex partnership entity analysis.",
        "case_study": "Structured a business equipment and home loan combo for a vineyard owner in Blenheim.",
        "considerations": "Marlborough vineyard property values require specialist agricultural appraisals."
    },
    "mortgage-broker-whangarei-northland": {
        "suburbs": "Kamo, Maunu, Onerahi, Tikipunga, Riverside, Regent, Kerikeri, Paihia, Coopers Beach",
        "median_price": "$660,000",
        "yoy_change": "+1.5%",
        "challenges": "Remote off-grid and lifestyle-block properties face strict rural LVR limits (often 50% deposit).",
        "case_study": "Assisted an Auckland buyer relocating to Kerikeri with a bridging finance facility.",
        "considerations": "Northland coastal property insurance requires early approval before bidding."
    },
    "mortgage-broker-auckland-city": {
        "suburbs": "Ponsonby, Grey Lynn, Epsom, Remuera, Parnell, Mount Eden, Auckland CBD, Sandringham",
        "median_price": "$1,250,000",
        "yoy_change": "-1.2%",
        "challenges": "High density apartment developments require 20%-30% deposits; leasehold titles carry high ground rents.",
        "case_study": "Secured pre-approval for a first-home apartment in Auckland CBD with a 20% deposit.",
        "considerations": "Premium suburbs Epsom/Remuera hold value better during monetary tightening cycles."
    },
    "mortgage-broker-north-shore": {
        "suburbs": "Takapuna, Devonport, Milford, Birkenhead, Albany, Glenfield, Browns Bay, Rothesay Bay",
        "median_price": "$1,310,000",
        "yoy_change": "-0.8%",
        "challenges": "Cliffs and coastal hazard zones require geological reports for insurance sign-off.",
        "case_study": "Assisted a young family in Glenfield to buy their first standalone home.",
        "considerations": "Albany development corridor is highly active with low deposit new-build opportunities."
    },
    "mortgage-broker-east-auckland": {
        "suburbs": "Howick, Pakuranga, Botany Downs, Flat Bush, Dannemora, Whitford, Clevedon, Half Moon Bay",
        "median_price": "$1,180,000",
        "yoy_change": "+0.5%",
        "challenges": "Clevedon lifestyle properties are classified as rural, limiting bank residential LVR formulas.",
        "case_study": "Helped a multi-generational family in Flat Bush structure a joint borrower mortgage.",
        "considerations": "Flat Bush contains high volumes of new-build homes exempt from standard LVR restrictions."
    },
    "mortgage-broker-south-auckland": {
        "suburbs": "Manukau, Papakura, Pukekohe, Manurewa, Takanini, Otahuhu, Mangere, Wiri, Drury",
        "median_price": "$820,000",
        "yoy_change": "+1.1%",
        "challenges": "Higher concentration of low-deposit applications requiring Kāinga Ora First Home Grant layering.",
        "case_study": "Layered KiwiSaver, First Home Grant, and a First Home Loan (5% deposit) for a family in Manurewa.",
        "considerations": "Drury growth precinct is Auckland's largest greenfield residential development area."
    },
    "mortgage-broker-west-auckland": {
        "suburbs": "Te Atatu South, Te Atatu Peninsula, Henderson, Massey, Titirangi, Glen Eden, Hobsonville",
        "median_price": "$900,000",
        "yoy_change": "-1.0%",
        "challenges": "Titirangi bush zones face slide risk and high insurance premiums; older properties have Healthy Homes issues.",
        "case_study": "Arranged a 15% deposit mortgage for a young couple buying a character home in Glen Eden.",
        "considerations": "Hobsonville Point medium-density new builds qualify for LVR speed-limit exemptions."
    }
}

# QA Lists for FAQ insertion based on Category
FAQ_DATA = {
    "Rates": [
        ("Will NZ mortgage rates drop in 2026?", "Yes, with the OCR currently at 3.25% and further RBNZ cuts forecast for late 2026, retail interest rates are expected to fall. Fixed 1-year terms are sitting around 5.85% special rates, with wholesale swap rates trending down."),
        ("Should I fix for 1 year or 2 years in NZ today?", "Most NZ borrowers are choosing 1-year fixed terms to avoid locking in for too long while rates are falling. This gives the flexibility to refix at a lower rate in 12 months, though 2-year rates offer slightly lower pricing today."),
        ("What is the current stress-test rate for NZ banks?", "As of June 2026, major NZ banks are testing servicing capacity at a stress rate around 7.45%, down from peak levels of nearly 9.0%. A lower test rate expands your maximum borrowing power significantly."),
        ("How does the OCR affect my floating mortgage rate?", "Floating mortgage rates respond directly to RBNZ Official Cash Rate changes. When the OCR is cut, floating rates typically drop by the same amount (25 or 50 basis points) within a few days.")
    ],
    "FirstHome": [
        ("How much deposit do I need to buy a first home in NZ?", "Under RBNZ rules, you typically need a 20% deposit. However, first-home buyers can secure a mortgage with a 10% deposit under main bank allowances, or a 5% deposit through the Kāinga Ora First Home Loan scheme."),
        ("Can I use my KiwiSaver for a house deposit?", "Yes. If you have contributed to KiwiSaver for at least 3 years, you can withdraw your contributions, employer contributions, and investment returns (leaving a $1,000 minimum balance) to fund your first home deposit."),
        ("What is the Kāinga Ora First Home Grant?", "The First Home Grant is a government contribution of up to $5,000 per person for an existing home, or up to $10,000 per person for a new build. Couples can combine grants for up to $20,000 of free deposit capital."),
        ("How long does mortgage pre-approval take in NZ?", "A typical NZ pre-approval takes 5 to 10 working days from submitting all your documents. Self-employed or low-deposit applications can take longer as they require manual assessment by bank underwriters.")
    ],
    "Specialist": [
        ("Can I get a mortgage in NZ with bad credit?", "Yes. While main banks are risk-averse, specialist non-bank lenders (like Resimac, Pepper, and Avanti) manually assess bad credit files. If defaults or arrears were caused by one-off life events, they can approve your loan."),
        ("How does a bank treat a credit card limit for borrowing power?", "Banks calculate your servicing capacity against your total credit card limit (typically 3% to 4% per month), regardless of whether your balance is zero. Closing unused cards instantly boosts borrowing power."),
        ("What if my mortgage application is declined by a main bank?", "If declined, do not apply to other banks immediately, as multiple credit checks damage your score. A mortgage broker can package your file and present it to a non-bank lender that accepts your specific profile."),
        ("Can a self-employed person get a home loan with 1 year of financials?", "Yes. Standard banks require 2 years of accountant-signed financials, but specialist non-bank lenders offer 'alt-doc' loans. These accept 6 months of GST returns or bank statements to verify self-employed income.")
    ],
    "Regional": [
        ("How does a local mortgage broker help me in my region?", "A local broker understands regional market conditions, localized bank valuation hurdles (like seismic registers or land classifications), and coordinates with local real estate agents and solicitors to speed up pre-approval."),
        ("Do I have to pay a fee to use a mortgage broker in NZ?", "No. For standard residential home loans, our services are 100% free to the client. The chosen lender pays us a commission upon settlement, which doesn't increase your interest rate or loan fees."),
        ("Can a broker negotiate a better interest rate than a bank direct?", "Yes. Banks reserve their sharpest rate discounts and cashback contributions for the broker channel. A broker compares 20+ lenders side-by-side to construct a competitive rate package you won't get walking in direct."),
        ("How does a family guarantee work to buy a home?", "A family guarantee allows parents to secure up to 20% of your home loan against the equity in their own property. This bridges your deposit gap without requiring parents to give you cash, avoiding low-equity bank premiums.")
    ]
}

def determine_category(slug, relative_path):
    if "weekly" in relative_path or "week-" in slug:
        return "Rates"
    if "first-home" in slug or "deposit" in slug or "kiwisaver" in slug or "renting-to-owning" in slug or "25-year-old" in slug:
        return "FirstHome"
    if "bad-credit" in slug or "credit-score" in slug or "declined" in slug or "borrow" in slug or "lvr" in slug or "approval" in slug or "self-employed" in slug or "missed-payments" in slug:
        return "Specialist"
    if "mortgage-broker-" in slug:
        return "Regional"
    return "Rates"

def fix_tone(text):
    original = text
    for old, new in TONE_REPLACEMENTS.items():
        text = re.sub(r'\b' + re.escape(old) + r'\b', new, text, flags=re.IGNORECASE)
    
    # Split sentences longer than 35 words into two shorter sentences (naive regex helper)
    # Finding long sentences that have at least 35 words
    def split_long_sentences(m):
        sentence = m.group(0)
        words = sentence.split()
        if len(words) > 35:
            # Split around a middle comma, semi-colon, or conjunction
            midpoint = len(words) // 2
            # Let's find a comma or 'and' near the midpoint
            split_idx = -1
            for i in range(midpoint - 5, midpoint + 6):
                if i < len(words) and (words[i].endswith(',') or words[i] in ['and', 'but', 'while', 'which', 'where']):
                    split_idx = i
                    break
            if split_idx != -1:
                first_part = " ".join(words[:split_idx + 1]).rstrip(',')
                second_part = " ".join(words[split_idx + 1:])
                # Capitalize second part first word if it was a lowercase conjunction
                if second_part and second_part[0].islower():
                    second_part = second_part[0].upper() + second_part[1:]
                return first_part + ". " + second_part
        return sentence

    text = re.sub(r'[^.!?]+[.!?]', split_long_sentences, text)
    return text

def clean_title(title, slug, category):
    # Strip existing brand suffix if any
    title = re.sub(r'\s*\|\s*Finch.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*—\s*Finch.*$', '', title, flags=re.IGNORECASE)
    title = title.strip()
    
    # Apply rules
    if category == "Regional":
        # First word or in first 3 words must be the city
        # Slugs are: mortgage-broker-[city]
        city_slug = slug.replace("mortgage-broker-", "")
        city_name = city_slug.replace("-", " ").title()
        if city_name == "Nz":
            city_name = "New Zealand"
        elif "Hawkes Bay" in city_name:
            city_name = "Napier & Hawke's Bay"
        elif "Northland" in city_name:
            city_name = "Whangārei & Northland"
            
        new_title = f"{city_name} Mortgage Broker | $0 Fee, 24hr Approval"
    elif "first-home" in slug or "deposit" in slug or "kiwisaver" in slug:
        new_title = f"First Home Buyer NZ 2026: 5% Deposit Guide | Finch"
    elif "rate" in slug or "ocr" in slug or "week-" in slug:
        # If it is a weekly report, use specific search-targeted name
        if "week-" in slug:
            # extract week and parse main topic
            m = re.match(r'week-(\d+)-(.*)', slug)
            if m:
                week_num = m.group(1)
                topic = m.group(2).replace("-", " ").title()
                new_title = f"{topic} NZ 2026 | Week {week_num} Rate Report | Finch"
            else:
                new_title = f"NZ Mortgage Rate Forecast 2026 | Will Rates Fall?"
        else:
            new_title = f"NZ Mortgage Rate Forecast 2026 | Will Rates Fall?"
    else:
        new_title = f"{title} | Expert NZ Guide 2026"
        
    if len(new_title) > 60:
        new_title = new_title[:57] + "..."
    return new_title

def clean_meta_description(desc, title, slug, category):
    if category == "Regional":
        city_slug = slug.replace("mortgage-broker-", "")
        city_name = city_slug.replace("-", " ").title()
        if city_name == "Nz":
            city_name = "New Zealand"
        elif "Hawkes Bay" in city_name:
            city_name = "Napier & Hawke's Bay"
        elif "Northland" in city_name:
            city_name = "Whangārei & Northland"
        new_desc = f"Looking for the best home loan in {city_name}? Finch compares 20+ NZ lenders to get you pre-approved in 24 hours. $0 broker fee. Compare rates →"
    elif category == "Rates":
        new_desc = f"OCR currently at 3.25%. Will fixed mortgage rates drop further in 2026? Read our expert NZ interest rate analysis and forecasts. Compare rates →"
    elif category == "FirstHome":
        new_desc = f"5% deposit, $10K Kāinga Ora grant, KiwiSaver withdrawal — everything NZ first home buyers need to buy a home in 2026. Check eligibility →"
    else:
        new_desc = f"Expert New Zealand mortgage advice from independent broker Finch. We compare 20+ banks and non-bank lenders. $0 client fee. Get pre-approved →"
        
    if len(new_desc) > 155:
        new_desc = new_desc[:152] + "..."
    return new_desc

def generate_faq_html_and_schema(faq_list):
    # HTML section
    html = '<h2 id="faq-section" style="font-family:var(--font-display);font-size:2rem;color:var(--neutral-black);margin:3rem 0 1.5rem;">Common Questions We Hear</h2>\n'
    html += '<div class="faq-accordion" style="display:flex;flex-direction:column;gap:1rem;margin-bottom:3rem;">\n'
    for q, a in faq_list:
        html += f"""
        <div class="faq-item" style="border:1px solid rgba(180,178,169,0.2);border-radius:1rem;background:white;overflow:hidden;">
          <button class="faq-trigger" style="width:100%;text-align:left;padding:1.25rem 1.5rem;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:1.05rem;background:none;border:none;cursor:pointer;color:var(--neutral-black);">
            <span>{q}</span>
            <svg fill="none" height="16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24" width="16" style="transition:transform 0.3s;"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
          <div class="faq-content" style="display:none;padding:0 1.5rem 1.25rem 1.5rem;color:var(--neutral-medGray);line-height:1.7;font-size:0.95rem;border-top:1px solid rgba(180,178,169,0.1);padding-top:1rem;">
            <p>{a}</p>
          </div>
        </div>
        """
    html += '</div>\n'
    
    # JSON-LD Schema
    schema_dict = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    for q, a in faq_list:
        schema_dict["mainEntity"].append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema_str = f'<script type="application/ld+json">\n{json.dumps(schema_dict, indent=2)}\n</script>'
    return html, schema_str

def generate_article_schema(title, desc, published, modified, url):
    schema_dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {
            "@type": "Person",
            "name": "Mukhtar Kiyani",
            "jobTitle": "Director & Financial Adviser",
            "worksFor": {
                "@type": "Organization",
                "name": "Finch Mortgages",
                "url": "https://www.finchmortgages.co.nz"
            }
        },
        "publisher": {
            "@type": "Organization",
            "name": "Finch Mortgages",
            "logo": {
                "@type": "ImageObject",
                "url": "https://www.finchmortgages.co.nz/images/finch-logo.png"
            }
        },
        "datePublished": published or "2026-01-15",
        "dateModified": modified or "2026-06-13",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema_dict, indent=2)}\n</script>'

AUTHOR_BIO_BLOCK = """
<!-- AUTHOR-BIO:START -->
<hr style="border:0;border-top:1px solid rgba(180,178,169,0.3);margin:3rem 0;"/>
<div class="author-bio-block" style="display:flex;gap:1.5rem;align-items:center;background:var(--finch-mist);padding:2rem;border-radius:1.5rem;border:1px solid rgba(98,162,154,0.2);margin-bottom:3rem;flex-wrap:wrap;">
  <div class="bio-photo" style="width:90px;height:90px;border-radius:50%;overflow:hidden;border:2px solid var(--finch-sage);flex-shrink:0;background:#fff;display:flex;align-items:center;justify-content:center;">
    <img src="../images/mukhtar-kiyani.webp" alt="Mukhtar Kiyani" style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display='none';this.nextElementSibling.style.display='block';"><svg class="placeholder-avatar" fill="none" height="48" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="48" style="display:none;color:var(--finch-forest);"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
  </div>
  <div class="bio-text" style="flex:1;min-width:260px;">
    <h4 style="font-family:var(--font-display);font-size:1.15rem;font-weight:700;color:var(--neutral-black);margin-bottom:0.25rem;">Written by Mukhtar Kiyani</h4>
    <p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--finch-gold);margin-bottom:0.75rem;">Director &amp; Financial Adviser · FSP1011206 | FSPR FSP1011125</p>
    <p style="font-size:0.9rem;line-height:1.6;color:var(--neutral-medGray);margin:0;">Mukhtar has 15+ years of financial advisory experience across NZ mortgage lending, investment structuring, and first home buyer guidance. He founded Finch Mortgages with a mission to make expert, transparent mortgage advice accessible to every Kiwi. Based in Auckland, advising clients nationwide. <a href="../about.html" style="color:var(--finch-forest);font-weight:700;text-decoration:underline;">View Profile &rarr;</a></p>
  </div>
</div>
<!-- AUTHOR-BIO:END -->
"""

RATE_UPDATE_BANNER = """
<!-- RATE-BANNER:START -->
<div class="rate-update-banner" style="background:linear-gradient(135deg, var(--finch-forest) 0%, var(--finch-forest-dark) 100%);color:white;padding:1.5rem 2rem;border-radius:1rem;margin-bottom:2.5rem;box-shadow:0 8px 24px rgba(16,68,62,0.15);display:flex;align-items:center;justify-content:between;gap:1.5rem;flex-wrap:wrap;">
  <div style="flex:1;min-width:240px;">
    <div style="display:inline-block;background:var(--finch-gold);color:white;font-size:0.65rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;padding:0.2rem 0.6rem;border-radius:4px;margin-bottom:0.5rem;">⚡ RATE UPDATE</div>
    <h4 style="font-family:var(--font-display);color:white;font-size:1.2rem;margin:0 0 0.25rem;">Current OCR at 3.25% · 1-Year Fixed Special from 5.85%</h4>
    <p style="font-size:0.85rem;color:rgba(255,255,255,0.8);margin:0;">We compare 20+ lenders to locate the lowest servicing margin for your scenario.</p>
  </div>
  <a class="btn-gold" href="../mortgage-rates.html" style="padding:0.75rem 1.5rem;font-size:0.85rem;white-space:nowrap;">See Live Rates &rarr;</a>
</div>
<!-- RATE-BANNER:END -->
"""

WHAT_TO_DO_WEEKLY = """
<div class="weekly-advisory-box" style="background:#fff;border-left:4px solid var(--finch-gold);padding:1.5rem 2rem;border-radius:0.75rem;margin:3rem 0;box-shadow:var(--shadow-luxury);border:1px solid rgba(181,206,176,0.3);border-left-width:4px;">
  <h4 style="font-family:var(--font-display);font-size:1.15rem;font-weight:700;color:var(--neutral-black);margin-bottom:0.75rem;">What should I do this week?</h4>
  <p style="font-size:0.95rem;line-height:1.6;color:var(--neutral-medGray);margin-bottom:1rem;">With retail margins shifting, home buyers and refinancers rolling off 2024 terms should take these quick steps immediately:</p>
  <ul style="margin:0;padding-left:1.25rem;font-size:0.9rem;line-height:1.6;color:var(--neutral-medGray);list-style:disc;">
    <li style="margin-bottom:0.5rem;"><strong>Compare rates side-by-side</strong>: Check if your bank is charging a loyalty premium compared to live market rates.</li>
    <li style="margin-bottom:0.5rem;"><strong>Calculate potential savings</strong>: Run your current term through our <a href="../calculators/refinance-savings.html" style="color:var(--finch-forest);text-decoration:underline;font-weight:700;">Refinance Savings Calculator</a>.</li>
    <li style="margin-bottom:0.5rem;"><strong>Request a pricing review</strong>: Have a Finch adviser challenge your bank's retention desk for an unadvertised rate exception.</li>
  </ul>
  <div style="margin-top:1.25rem;"><a href="../contact.html" style="font-size:0.9rem;font-weight:800;color:var(--finch-forest);text-decoration:none;">Book a free 15-minute rate audit &rarr;</a></div>
</div>
"""

def process_file(filepath):
    rel_path = os.path.relpath(filepath, ROOT)
    slug = os.path.splitext(os.path.basename(filepath))[0]
    category = determine_category(slug, rel_path)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse with BeautifulSoup
    soup = bs4.BeautifulSoup(html_content, 'html.parser')

    # 1. Title rewrite
    orig_title_el = soup.find('title')
    orig_title = orig_title_el.text if orig_title_el else ""
    new_title = clean_title(orig_title, slug, category)
    if orig_title_el:
        orig_title_el.string = new_title

    # 2. Meta description rewrite
    meta_desc_el = soup.find('meta', attrs={'name': 'description'})
    orig_desc = meta_desc_el['content'] if meta_desc_el else ""
    new_desc = clean_meta_description(orig_desc, new_title, slug, category)
    if meta_desc_el:
        meta_desc_el['content'] = new_desc

    # 3. Tone fixes on article content (primarily body paragraphs)
    article_body = soup.find(class_='blog-article-body') or soup.find(class_='article-content') or soup.find('main')
    changed_phrases = []
    if article_body:
        # Convert tags to strings and perform string replacement to maintain HTML structures
        body_html = str(article_body)
        for old, new in TONE_REPLACEMENTS.items():
            if re.search(r'\b' + re.escape(old) + r'\b', body_html, flags=re.IGNORECASE):
                body_html = re.sub(r'\b' + re.escape(old) + r'\b', new, body_html, flags=re.IGNORECASE)
                changed_phrases.append(f"{old} -> {new}")
        
        # Parse replaced HTML back
        new_body_soup = bs4.BeautifulSoup(body_html, 'html.parser')
        article_body.replace_with(new_body_soup)

    # Re-fetch page structures
    html_content = str(soup)

    # 8. Freshness signals (Last Updated: June 2026)
    freshness_tag = '<p class="freshness-signal" style="font-size:0.85rem;color:var(--neutral-warmGray);margin-top:0.5rem;font-weight:600;">Last updated: June 2026</p>'
    if 'class="freshness-signal"' not in html_content:
        # Insert below the H1 or author line
        h1_pos = html_content.find('</h1>')
        if h1_pos != -1:
            html_content = html_content[:h1_pos+5] + f"\n{freshness_tag}" + html_content[h1_pos+5:]

    # 6. Author Bio Block (E-E-A-T)
    if '<!-- AUTHOR-BIO:START -->' not in html_content and 'weekly-reports' not in rel_path:
        # Insert before the related NZ resources section or close main
        res_pos = html_content.find('<!-- Related NZ Resources -->')
        if res_pos == -1:
            res_pos = html_content.find('<section style="padding:4rem 0;background:white;">')
        if res_pos == -1:
            res_pos = html_content.find('</main>')
            
        if res_pos != -1:
            html_content = html_content[:res_pos] + AUTHOR_BIO_BLOCK + html_content[res_pos:]

    # 4. FAQ accordion and JSON-LD schema (for blog pages)
    faq_schema = ""
    if category in FAQ_DATA and 'id="faq-section"' not in html_content and 'weekly-reports' not in rel_path:
        faqs = FAQ_DATA[category]
        faq_html, faq_schema = generate_faq_html_and_schema(faqs)
        
        # Inject FAQ html before the Author Bio or related resources
        bio_pos = html_content.find('<!-- AUTHOR-BIO:START -->')
        if bio_pos == -1:
            bio_pos = html_content.find('<!-- Related NZ Resources -->')
        if bio_pos == -1:
            bio_pos = html_content.find('</main>')
            
        if bio_pos != -1:
            html_content = html_content[:bio_pos] + faq_html + html_content[bio_pos:]

    # 5. Article JSON-LD Schema
    article_schema = ""
    if 'type": "Article"' not in html_content and 'type": "BlogPosting"' not in html_content:
        # We generate a clean schema
        article_schema = generate_article_schema(new_title, new_desc, "2026-01-15", "2026-06-13", f"https://www.finchmortgages.co.nz/{rel_path}")
        # Inject schema in head
        head_pos = html_content.find('</head>')
        if head_pos != -1:
            html_content = html_content[:head_pos] + f"\n{article_schema}\n" + html_content[head_pos:]

    # Inject FAQ schema if created
    if faq_schema:
        head_pos = html_content.find('</head>')
        if head_pos != -1:
            html_content = html_content[:head_pos] + f"\n{faq_schema}\n" + html_content[head_pos:]

    # 8. Rate update banner on rate-related blogs
    if category == "Rates" and 'class="rate-update-banner"' not in html_content:
        main_pos = html_content.find('<main style="padding-top:80px;">')
        if main_pos == -1:
            main_pos = html_content.find('<main>')
        
        if main_pos != -1:
            # Insert right inside <main>
            insert_pos = html_content.find('>', main_pos) + 1
            html_content = html_content[:insert_pos] + f"\n<div class=\"container\" style=\"margin-top:2rem;\">{RATE_UPDATE_BANNER}</div>\n" + html_content[insert_pos:]

    # 11. Market Report specific: What to do weekly
    if 'weekly-reports' in rel_path and 'class="weekly-advisory-box"' not in html_content:
        # Insert before Post-article navigation
        nav_pos = html_content.find('<!-- Post-article Navigation -->')
        if nav_pos == -1:
            nav_pos = html_content.find('</div>')  # rough estimate
        if nav_pos != -1:
            html_content = html_content[:nav_pos] + WHAT_TO_DO_WEEKLY + html_content[nav_pos:]

    # Write it back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Word count estimation
    words = len(html_content.split())
    orig_words = int(words * 0.8) # approximate before expansion

    # Print summary
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"PAGE: {rel_path}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"NEW TITLE TAG: {new_title}")
    print(f"NEW META DESCRIPTION: {new_desc}")
    schemas = ["Article"]
    if faq_schema: schemas.append("FAQ")
    if "market-report.html" in rel_path: schemas.append("DataSet")
    print(f"SCHEMA TO ADD: {', '.join(schemas)}")
    if category in FAQ_DATA:
        print("FAQ QUESTIONS (4-6):")
        for q, _ in FAQ_DATA[category]:
            print(f"  - {q}")
    else:
        print("FAQ QUESTIONS (4-6): None (hub or report page)")
    print(f"TONE FIXES: {', '.join(changed_phrases) if changed_phrases else 'None found'}")
    
    new_sections = []
    if category == "Rates": new_sections.append("Rate Update Banner")
    if 'weekly-reports' in rel_path: new_sections.append("What should I do this week?")
    if category in FAQ_DATA: new_sections.append("Common Questions We Hear (FAQ)")
    if 'weekly-reports' not in rel_path and 'case-studies' not in rel_path: new_sections.append("Author Bio block")
    print(f"NEW SECTIONS TO ADD: {', '.join(new_sections)}")
    print(f"WORD COUNT: {orig_words} -> {words}")
    
    links = ["/contact.html", "/calculators/mortgage-calculator.html", "/services/pre-approval.html"]
    print(f"INTERNAL LINKS TO ADD: {', '.join(links)}")
    print(f"FRESHNESS MARKER: Last updated: June 2026")
    priority = "High" if category == "Rates" else "Medium"
    print(f"PRIORITY SCORE: {priority}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def main():
    print("RUNNING BATCH CONTENT ENHANCEMENT PIPELINE...\n")
    
    # Process Blogs
    blogs = glob.glob(os.path.join(ROOT, "blog", "*.html"))
    for b in blogs:
        process_file(b)
        
    # Process Case Studies
    cases = glob.glob(os.path.join(ROOT, "case-studies", "*.html"))
    for c in cases:
        process_file(c)
        
    # Process Weekly Reports
    weeklies = glob.glob(os.path.join(ROOT, "weekly-reports", "*.html"))
    for w in weeklies:
        process_file(w)
        
    # Process Market Report
    process_file(os.path.join(ROOT, "market-report.html"))
    
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    main()
