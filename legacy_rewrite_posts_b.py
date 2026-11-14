#!/usr/bin/env python3
"""Rewrites of the five Auckland area broker pages (see legacy_rewrite_posts.py).

Local detail is limited to things that are stable and checkable: which suburbs
an area covers, the housing types found there, and the lending questions those
raise. No prices, yields, growth claims or travel times. Titles are unchanged
from the versions Google has indexed.
"""

from intent_post_kit import link, post, table

MODIFIED = "2026-11-13"
B = "../blog/"
L = "../locations/"
C = "../calculators/"

REL_AREA = [
    ("../locations/index.html", "Areas We Cover", "Mortgage advice across Auckland and New Zealand."),
    ("../calculators/borrowing-power.html", "Borrowing Power Calculator", "A rough idea of what lenders may lend you."),
    ("../services/pre-approval.html", "Pre-Approval", "Know your budget before you make an offer."),
]

HOW = ("How we work",
       "Finch Mortgages is an independent mortgage adviser based in Te Atatu South. We compare your situation across the 23 lenders on our panel, which includes banks and non-bank lenders, and manage the application through to settlement. There's no fee for residential home loans, because the lender pays us a commission when the loan settles. Our " + link("../disclosure.html", "disclosure statement") + " sets out how that works.",
       "You can meet us in person, or do everything by phone, video and secure document upload.")


def suburbs(pairs):
    return ", ".join(link(h, t) for h, t in pairs)


def A(published, slug, title, h1, intro, description, keywords, sections, faqs, *, area, cta):
    d = post(slug, title, h1, intro, description, keywords, sections + [HOW], faqs,
             service="Mortgage Broker", label=f"{area} Mortgage Broker",
             about=f"Mortgage broking in {area}", cta=cta,
             cta_sub="Tell us what you're planning and we'll come back to you with your options.",
             related=REL_AREA)
    d["published"] = published
    d["modified"] = MODIFIED
    d["region"] = "Auckland"
    return d


AREA_POSTS = [
    A("2026-04-15",
      "mortgage-broker-west-auckland",
      "West Auckland Mortgage Broker | $0 Fee, 23 Lenders | Finch",
      "Mortgage Broker West Auckland",
      "Finch Mortgages is based in Te Atatu South, so West Auckland is home. We arrange home loans from Henderson and Massey out to Kumeū and Titirangi, for first home buyers, people refinancing and investors.",
      "West Auckland mortgage broker based in Te Atatu South. Home loans, refinancing and first home advice across 23 lenders, with no fee on residential home loans.",
      ["mortgage broker West Auckland", "West Auckland mortgage adviser", "home loan West Auckland", "mortgage broker Henderson", "mortgage broker Waitakere"],
      [
          ("Where we work in West Auckland",
           "Our office is at 17a Marlene Ave, Te Atatu South. We have local pages for " + suburbs([
               (B + "mortgage-broker-te-atatu.html", "Te Atatu"), (B + "mortgage-broker-henderson.html", "Henderson"),
               (B + "mortgage-broker-massey.html", "Massey"), (B + "mortgage-broker-new-lynn.html", "New Lynn"),
               (B + "mortgage-broker-hobsonville.html", "Hobsonville"), (L + "mortgage-broker-glen-eden.html", "Glen Eden"),
               (L + "mortgage-broker-titirangi.html", "Titirangi"), (L + "mortgage-broker-westgate.html", "Westgate"),
               (L + "mortgage-broker-kumeu.html", "Kumeū"), (L + "mortgage-broker-avondale.html", "Avondale")]) + ", and we cover the suburbs in between."),
          ("What West Auckland properties mean for a loan",
           "The west has a wider mix of housing than most of Auckland, and lenders treat the types differently.",
           table(["Property", "What lenders look at"], [
               ["New terraced houses and apartments, common around Hobsonville, Westgate, Henderson and New Lynn", "New builds can need a smaller deposit. Lenders check apartment size, the body corporate and the builder's completion documents"],
               ["Older houses on cross-leased sections", "Whether additions such as decks and garages match the flats plan on the title"],
               ["Plaster-clad homes from the 1990s and 2000s", "A building report covering weathertightness, and sometimes a larger deposit"],
               ["Bush sections and homes in the Waitākere foothills", "Access, tank water and septic systems, and slope stability"],
               ["Lifestyle blocks around Kumeū, Taupaki and Waitākere", "Land size. Above a certain area many lenders lend a lower percentage or treat it as rural"],
           ]),
           "More on each: " + link(B + "cross-lease-unit-title-freehold-nz.html", "cross-leases and unit titles") + ", " + link(B + "plaster-house-monolithic-cladding-mortgage-nz.html", "plaster cladding") + " and " + link(B + "apartment-home-loan-nz.html", "apartments") + "."),
          ("Flood history and insurance",
           "Parts of West Auckland were badly affected by the January 2023 floods. Lenders need house insurance in place before settlement, so for any property near a stream or in a mapped flood plain, read the LIM for flood information and get an insurance quote before you go unconditional. " + link(B + "flood-zone-insurance-mortgage-decline-nz.html", "Flood zones, insurance and mortgages") + " explains what to check."),
          ("What we help with",
           [
               "<strong>First homes.</strong> Deposits from savings, KiwiSaver and family, low-deposit options and the First Home Loan. See " + link("../services/first-home-buyer.html", "first home buyer loans") + ".",
               "<strong>Refinancing.</strong> Comparing your bank's refix offer, and working out break fees and cashback clawback before you move. See " + link("../services/refinance.html", "refinancing") + ".",
               "<strong>Self-employed borrowers.</strong> Tradespeople and business owners whose income doesn't fit a payslip. See " + link("../services/self-employed.html", "self-employed home loans") + ".",
               "<strong>Building and investing.</strong> " + link("../services/construction-loan.html", "Construction loans") + " and " + link("../services/investment-property.html", "investment property lending") + ".",
           ]),
      ],
      [
          ("Where is Finch Mortgages based?", "At 17a Marlene Ave, Te Atatu South, in West Auckland. We also work with clients by phone and video."),
          ("How much does a West Auckland mortgage broker cost?", "Finch doesn't charge a fee for residential home loans. The lender pays a commission when the loan settles, which is set out in our disclosure statement."),
          ("Can I get a home loan for a lifestyle block in West Auckland?", "Yes, though lenders treat larger blocks differently. Above a certain land size many lend a lower percentage of the value, so the deposit needed can be higher."),
          ("Do you help with new builds in Hobsonville and Westgate?", "Yes. We arrange lending for completed new builds, turnkey purchases and off-the-plans contracts, including checking how long a pre-approval needs to last."),
      ],
      area="West Auckland", cta="Talk to a mortgage broker in West Auckland"),

    A("2026-04-01",
      "mortgage-broker-east-auckland",
      "East Auckland Mortgage Broker | $0 Fee, 23 Lenders | Finch",
      "Mortgage Broker East Auckland",
      "We arrange home loans across East Auckland, from Howick and Pakuranga to Botany, Flat Bush and Beachlands, and compare 23 lenders to find one that fits your situation.",
      "East Auckland mortgage broker for Howick, Pakuranga, Botany and Flat Bush. Home loans, refinancing and first home advice across 23 lenders. No broker fee.",
      ["mortgage broker East Auckland", "East Auckland mortgage adviser", "home loan East Auckland", "mortgage broker Howick", "mortgage broker Botany"],
      [
          ("Where we work in East Auckland",
           "We have local pages for " + suburbs([
               (B + "mortgage-broker-howick.html", "Howick"), (B + "mortgage-broker-botany.html", "Botany"),
               (B + "mortgage-broker-flat-bush.html", "Flat Bush"), (L + "mortgage-broker-pakuranga.html", "Pakuranga"),
               (L + "mortgage-broker-beachlands.html", "Beachlands"), (L + "mortgage-broker-panmure.html", "Panmure")]) + ", and we cover Bucklands Beach, Half Moon Bay, Dannemora and East Tāmaki too. Appointments are by phone or video, or at our office in Te Atatu South."),
          ("What East Auckland properties mean for a loan",
           table(["Property", "What lenders look at"], [
               ["Cross-leased houses and units, common in Howick, Pakuranga and Bucklands Beach", "Whether the buildings match the flats plan. Unrecorded additions need sorting out before or as part of the purchase"],
               ["Large family homes in Flat Bush and Dannemora", "Affordability on a bigger loan, and for plaster-clad homes of the 2000s, a building report"],
               ["New terraced houses and apartments in Flat Bush and Ormiston", "New-build status, the completion documents, and apartment size"],
               ["Coastal and cliff-top properties", "Insurance, and any hazard notes on the LIM"],
           ]),
           "More on each: " + link(B + "cross-lease-unit-title-freehold-nz.html", "cross-leases and unit titles") + ", " + link(B + "plaster-house-monolithic-cladding-mortgage-nz.html", "plaster cladding") + " and " + link(B + "new-build-home-loan-deposit-nz.html", "new-build deposits") + "."),
          ("Households with more than one income",
           "Many East Auckland homes are bought by extended families, or by buyers who plan to rent out rooms. Lenders handle this in different ways.",
           [
               "Parents or adult children can be co-borrowers, which adds their income and their commitments to the application.",
               "Some lenders count boarder or flatmate income within limits. Others don't count it at all.",
               "A parent can help without being on the loan, through a gift or a guarantee.",
           ],
           "See " + link(B + "co-owning-home-friends-family-nz.html", "buying with family") + ", " + link(B + "boarder-flatmate-income-mortgage-nz.html", "boarder income") + " and " + link(B + "guarantor-home-loan-nz.html", "guarantees") + "."),
          ("Moving up within the area",
           "A lot of our East Auckland work is for owners selling one home and buying another. The main decision is whether to sell first or buy first, and whether you need bridging finance in between. " + link(B + "sell-or-buy-first-nz.html", "Sell or buy first?") + " and " + link(B + "bridging-finance-guide-nz.html", "bridging finance") + " explain the options."),
      ],
      [
          ("Do you have an office in East Auckland?", "No. Our office is in Te Atatu South. Most East Auckland clients work with us by phone and video, and you're welcome to visit."),
          ("Can I get a mortgage on a cross-lease property in Howick?", "Yes. Lenders accept cross-leases, but your lawyer needs to confirm the buildings match the flats plan on the title. Unrecorded additions can delay or complicate a purchase."),
          ("Can my parents be on the loan with me?", "Yes. Family members can be co-borrowers, and their income and debts are then assessed together with yours. A gift or guarantee are alternatives that keep them off the loan."),
          ("How much does it cost to use Finch?", "There's no fee for residential home loans. The lender pays a commission when the loan settles."),
      ],
      area="East Auckland", cta="Talk to a mortgage broker in East Auckland"),

    A("2026-03-15",
      "mortgage-broker-north-shore",
      "North Shore Mortgage Broker | $0 Fee, 23 Lenders | Finch",
      "Mortgage Broker North Shore",
      "We arrange home loans across the North Shore, from Devonport and Takapuna to Albany and the East Coast Bays, and compare 23 lenders to find one that fits your situation.",
      "North Shore mortgage broker for Takapuna, Albany, Glenfield and the East Coast Bays. Home loans and refinancing across 23 lenders, with no broker fee.",
      ["mortgage broker North Shore", "North Shore mortgage adviser", "home loan North Shore Auckland", "mortgage broker Takapuna", "mortgage broker Albany"],
      [
          ("Where we work on the North Shore",
           "We have local pages for " + suburbs([
               (B + "mortgage-broker-takapuna.html", "Takapuna"), (B + "mortgage-broker-albany.html", "Albany"),
               (B + "mortgage-broker-glenfield.html", "Glenfield"), (L + "mortgage-broker-birkenhead.html", "Birkenhead"),
               (L + "mortgage-broker-browns-bay.html", "Browns Bay"), (L + "mortgage-broker-devonport.html", "Devonport")]) + ", and we cover Milford, Northcote, Beach Haven and Long Bay too. Appointments are by phone or video, or at our office in Te Atatu South."),
          ("What North Shore properties mean for a loan",
           table(["Property", "What lenders look at"], [
               ["Apartments in Takapuna and Albany", "Floor size, whether the title is freehold or leasehold, the body corporate's finances and any remediation work"],
               ["Cliff-top and coastal homes in the East Coast Bays and Devonport", "Insurance, and land stability notes on the LIM"],
               ["Cross-leased houses and units in Glenfield, Birkenhead and Northcote", "Whether the buildings match the flats plan on the title"],
               ["Plaster-clad homes from the 1990s and 2000s, common around Albany", "A building report covering weathertightness"],
               ["New builds in Long Bay and Albany", "New-build status and the completion documents"],
           ]),
           "More on each: " + link(B + "apartment-home-loan-nz.html", "apartment home loans") + ", " + link(B + "leasehold-apartment-mortgage-auckland.html", "leasehold apartments") + " and " + link(B + "plaster-house-monolithic-cladding-mortgage-nz.html", "plaster cladding") + "."),
          ("Off-the-plans purchases",
           "If you're buying an apartment or townhouse before it's built, the loan is confirmed close to completion, not when you sign. A pre-approval won't last that long, and your income, the lender's rules or the valuation can change in between. Know what your contract says about delays and sunset dates, and keep your finances steady until settlement. " + link(B + "buying-off-the-plans-finance-nz.html", "Buying off the plans") + " covers the risks."),
          ("Moving up, or downsizing",
           "Many North Shore owners have a lot of equity and are either buying a larger home or moving to something smaller. Both can involve owning two properties for a time. See " + link(B + "sell-or-buy-first-nz.html", "sell or buy first") + " and " + link(B + "bridging-finance-guide-nz.html", "bridging finance") + ". If you're over 50, lenders will also ask how the loan gets repaid by retirement. " + link(B + "home-loan-over-50-nz.html", "Home loans over 50") + " explains what they need."),
      ],
      [
          ("Do you have an office on the North Shore?", "No. Our office is in Te Atatu South. Most North Shore clients work with us by phone and video, and you're welcome to visit."),
          ("Is it harder to get a mortgage for an apartment in Takapuna?", "It can be. Lenders set minimum floor sizes and often want a larger deposit for small or leasehold apartments. They also look at the body corporate and the building's condition."),
          ("Can I get pre-approval for an off-the-plans purchase in Albany?", "You can get an indication, but the loan is confirmed near completion, which may be a year or more away. Plan for your circumstances and the lender's rules changing in that time."),
          ("How much does it cost to use Finch?", "There's no fee for residential home loans. The lender pays a commission when the loan settles."),
      ],
      area="North Shore", cta="Talk to a mortgage broker on the North Shore"),

    A("2026-05-01",
      "mortgage-broker-south-auckland",
      "South Auckland Mortgage Broker | $0 Fee, 23 Lenders | Finch",
      "Mortgage Broker South Auckland",
      "We arrange home loans across South Auckland, from Māngere and Manukau to Papakura and Drury, for first home buyers, growing families and people refinancing.",
      "South Auckland mortgage broker for Manukau, Papatoetoe, Manurewa and Papakura. First home loans and refinancing across 23 lenders. No broker fee.",
      ["mortgage broker South Auckland", "South Auckland mortgage adviser", "home loan South Auckland", "mortgage broker Manukau", "mortgage broker Papakura"],
      [
          ("Where we work in South Auckland",
           "We have local pages for " + suburbs([
               (B + "mortgage-broker-manukau.html", "Manukau"), (B + "mortgage-broker-papakura.html", "Papakura"),
               (L + "mortgage-broker-mangere.html", "Māngere"), (L + "mortgage-broker-papatoetoe.html", "Papatoetoe"),
               (L + "mortgage-broker-manurewa.html", "Manurewa"), (L + "mortgage-broker-otahuhu.html", "Ōtāhuhu"),
               (L + "mortgage-broker-takanini.html", "Takanini"), (L + "mortgage-broker-drury.html", "Drury"),
               (B + "mortgage-broker-pukekohe-franklin.html", "Pukekohe")]) + ". Appointments are by phone or video, or at our office in Te Atatu South."),
          ("First home buyers",
           "South Auckland has a lot of new terraced housing, particularly around Takanini, Papakura and Drury, and many of our clients here are buying their first home.",
           [
               "<strong>New builds can need a smaller deposit</strong>, because they're exempt from the Reserve Bank's deposit limits.",
               "<strong>KiwiSaver</strong> can usually be withdrawn after three years. See " + link(B + "kiwisaver-first-home-withdrawal.html", "KiwiSaver first-home withdrawal") + ".",
               "<strong>The Kāinga Ora First Home Loan</strong> allows a 5% deposit for buyers under the income caps. See our " + link(B + "first-home-loan-kainga-ora-nz.html", "First Home Loan guide") + ".",
               "<strong>Turnkey contracts</strong> mean a small deposit now and the balance when the house is finished. See " + link(B + "turnkey-home-loan-nz.html", "turnkey home loans") + ".",
           ]),
          ("Buying as a family",
           "It's common here for several family members to buy and live together. Lenders can work with that, but each handles it differently.",
           [
               "Everyone on the loan has their income, debts and credit record assessed.",
               "Some lenders count boarder income within limits. Others don't.",
               "Income from a second job, overtime or shift allowances is often counted in part, usually with a track record.",
               "Family overseas can gift money towards the deposit, with a gift letter and evidence of where it came from.",
           ],
           "See " + link(B + "co-owning-home-friends-family-nz.html", "buying with family") + ", " + link(B + "boarder-flatmate-income-mortgage-nz.html", "boarder income") + " and " + link(B + "commission-bonus-overtime-income-mortgage-nz.html", "overtime and variable income") + "."),
          ("What South Auckland properties mean for a loan",
           table(["Property", "What lenders look at"], [
               ["New terraced houses", "New-build status, the completion documents, and any residents' association or body corporate fees"],
               ["Older homes on large sections", "The building report, and unconsented work such as garage conversions and sleepouts"],
               ["Properties with a minor dwelling", "Whether the second dwelling is consented, and how its rent is counted"],
               ["Homes in low-lying areas", "Flood information on the LIM, and insurance"],
           ]),
           "More on each: " + link(B + "unconsented-work-mortgage-nz.html", "unconsented work") + ", " + link(B + "granny-flats-minor-dwellings-finance-nz.html", "minor dwellings") + " and " + link(B + "flood-zone-insurance-mortgage-decline-nz.html", "flood zones and insurance") + "."),
      ],
      [
          ("Do you have an office in South Auckland?", "No. Our office is in Te Atatu South. Most South Auckland clients work with us by phone and video, and you're welcome to visit."),
          ("Can several family members buy a house together?", "Yes. Each person on the loan is assessed on their income, debts and credit record, and all are responsible for the whole loan. Get legal advice on how ownership is recorded."),
          ("Can I buy a new build in Takanini or Drury with less than 20% deposit?", "Possibly. New builds are exempt from the Reserve Bank's deposit limits, so some lenders accept less than 20%. You still need to pass the affordability test."),
          ("How much does it cost to use Finch?", "There's no fee for residential home loans. The lender pays a commission when the loan settles."),
      ],
      area="South Auckland", cta="Talk to a mortgage broker in South Auckland"),

    A("2026-03-01",
      "mortgage-broker-auckland-city",
      "Mortgage Broker Central Auckland | Mortgage Adviser | Finch",
      "Mortgage Broker Central Auckland",
      "We arrange home loans across central Auckland, from city apartments to the villas and bungalows of the inner suburbs, and compare 23 lenders to find one that fits.",
      "Central Auckland mortgage broker for the CBD, Ponsonby, Mt Eden, Epsom and Remuera. Apartment, home and investment loans across 23 lenders. No broker fee.",
      ["mortgage broker Auckland", "mortgage broker Central Auckland", "Auckland mortgage adviser", "home loan Auckland city", "apartment mortgage Auckland"],
      [
          ("Where we work in central Auckland",
           "We have local pages for " + suburbs([
               (L + "mortgage-broker-ponsonby.html", "Ponsonby"), (L + "mortgage-broker-mt-eden.html", "Mt Eden"),
               (L + "mortgage-broker-mt-albert.html", "Mt Albert"), (L + "mortgage-broker-epsom.html", "Epsom"),
               (L + "mortgage-broker-remuera.html", "Remuera"), (L + "mortgage-broker-ellerslie.html", "Ellerslie"),
               (L + "mortgage-broker-onehunga.html", "Onehunga"), (B + "mortgage-broker-mt-roskill.html", "Mt Roskill"),
               (L + "mortgage-broker-point-chevalier.html", "Point Chevalier")]) + ". For the rest of the city see " + suburbs([
               (B + "mortgage-broker-west-auckland.html", "West Auckland"), (B + "mortgage-broker-north-shore.html", "the North Shore"),
               (B + "mortgage-broker-east-auckland.html", "East Auckland"), (B + "mortgage-broker-south-auckland.html", "South Auckland")]) + ". Our office is in Te Atatu South, and we also work by phone and video."),
          ("City apartments",
           "Apartments are where central Auckland lending differs most from the suburbs. Before you make an offer, check:",
           [
               "<strong>Floor size.</strong> Lenders set a minimum, and below it they want a much larger deposit or won't lend. The minimum differs between lenders.",
               "<strong>Title.</strong> Leasehold apartments have ground rent that can rise at each review, and fewer lenders accept them. See " + link(B + "leasehold-apartment-mortgage-auckland.html", "leasehold apartments in Auckland") + ".",
               "<strong>The body corporate.</strong> Lenders read the minutes and accounts for planned remediation, special levies and the state of the long-term maintenance fund.",
               "<strong>Use.</strong> Serviced apartments, hotel-managed units and student accommodation are treated as specialist lending.",
           ],
           link(B + "apartment-home-loan-nz.html", "Apartment home loans") + " covers each of these."),
          ("Villas, bungalows and cross-leases",
           table(["Property", "What lenders look at"], [
               ["Character villas and bungalows in suburbs such as Ponsonby, Grey Lynn and Mt Eden", "The building report: piles, roof, wiring, and whether renovations were consented"],
               ["Cross-leased houses and units", "Whether the buildings match the flats plan on the title"],
               ["Units and townhouses on unit titles", "The body corporate's records, as for apartments"],
               ["Homes with a minor dwelling or home-and-income layout", "Consents for the second dwelling, and how the rent is counted"],
           ]),
           "See " + link(B + "cross-lease-unit-title-freehold-nz.html", "cross-lease, unit title and freehold") + " and " + link(B + "unconsented-work-mortgage-nz.html", "unconsented work") + "."),
          ("Borrowing in Auckland's price range",
           "Auckland prices mean larger loans, so the debt-to-income limit and the affordability test come into play sooner than elsewhere. Lenders differ in the test rate they use and the income they count, and on a large loan that difference can be significant. Check your own position with the " + link(C + "dti-calculator.html", "DTI calculator") + " and the " + link(C + "borrowing-power.html", "borrowing power calculator") + ", or read " + link(B + "how-much-can-i-borrow.html", "how much can I borrow") + "."),
          ("What we help with",
           [
               "<strong>First homes</strong>, including apartments and units. See " + link(L + "first-home-buyer-auckland-city.html", "first home buyers in Auckland") + ".",
               "<strong>Refinancing</strong> when a fixed term ends. See " + link(L + "refinance-auckland-city.html", "refinancing in Auckland") + ".",
               "<strong>Investment property.</strong> See " + link(L + "investment-property-auckland-city.html", "investment loans in Auckland") + ".",
               "<strong>Self-employed and contract income.</strong> See " + link(L + "self-employed-auckland-city.html", "self-employed home loans in Auckland") + ".",
           ]),
      ],
      [
          ("Where is Finch Mortgages located?", "At 17a Marlene Ave, Te Atatu South, Auckland. We work with clients across the city in person, by phone and by video."),
          ("How much deposit do I need for an Auckland apartment?", "It depends on the apartment. A standard freehold apartment above the lender's minimum size can be bought on normal deposit terms. Small, leasehold or serviced apartments usually need more."),
          ("Do Auckland mortgage brokers charge a fee?", "Finch doesn't charge a fee for residential home loans. The lender pays a commission when the loan settles, as set out in our disclosure statement."),
          ("Which banks do you work with?", "Our panel has 23 lenders, including banks such as ANZ, BNZ, SBS Bank and The Co-operative Bank, and non-bank and specialist lenders. The full list is on our lenders page."),
      ],
      area="Central Auckland", cta="Talk to a mortgage broker in Auckland"),
]
