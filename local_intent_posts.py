#!/usr/bin/env python3
"""Post definitions for generate_local_intent_blogs.py.

Content rules (context/brand-voice.md, context/seo-guidelines.md):
  - Explain mechanisms, never invent rates, lender names + policies, or odds.
  - Hedge lender-specific variation explicitly — that variation is the reason
    a broker adds value, so say so rather than inventing a number.
  - NZ terminology only. 1,500-2,000 words per post.
"""

from generate_local_intent_blogs import callout, link, ol, p, table, ul

# Shared "related reading" sets. Paths are relative to /blog/.
REL_CORE = [
    ("../services/home-loan.html", "NZ Home Loan Service",
     "Independent advice across 20+ NZ lenders."),
    ("../calculators/borrowing-power.html", "Borrowing Power Calculator",
     "See what NZ banks will actually lend you."),
    ("../mortgage-rates.html", "Live NZ Mortgage Rates",
     "Current carded and broker rates."),
]

REL_FHB = [
    ("../guides/first-home-guide.html", "First Home Buyer Guide",
     "The complete NZ first home playbook."),
    ("kiwisaver-first-home-withdrawal.html", "KiwiSaver First Home Withdrawal",
     "How to get your deposit out."),
    ("deposit-needed-home-loan-nz.html", "How Much Deposit You Need",
     "NZ deposit rules explained."),
]

REL_INVEST = [
    ("../services/investment-property.html", "Investment Property Loans",
     "Structure and lender matching for investors."),
    ("../calculators/rental-yield-calculator.html", "Rental Yield Calculator",
     "Model the numbers before you buy."),
    ("using-home-equity-investment-property-nz.html", "Using Home Equity",
     "Turn equity into your next purchase."),
]

REL_SELFEMP = [
    ("../services/self-employed.html", "Self-Employed Mortgages",
     "For business owners and contractors."),
    ("../case-studies/self-employed-approval.html", "Self-Employed Case Study",
     "How one client got approved."),
    ("../lenders/non-bank-lenders.html", "NZ Non-Bank Lenders",
     "When the main banks say no."),
]


POSTS = [

    # =====================================================================
    # GROUP A — Region-specific lending obstacles
    # =====================================================================

    {
        "slug": "leasehold-apartment-mortgage-auckland",
        "title": "Leasehold Apartment Mortgages in Auckland | Finch",
        "h1": "Leasehold Apartment Mortgages in Auckland",
        "section_label": "Auckland Property",
        "region": "Auckland",
        "lead_service": "Home Loan",
        "about": ["Leasehold property", "Auckland apartments", "Unit titles"],
        "intro_pull": "Leasehold apartments look like bargains until you try to finance one. Here is how Auckland lenders actually treat leasehold, and what makes the difference between an approval and a flat decline.",
        "description": "Can you get a mortgage on a leasehold apartment in Auckland? How NZ lenders assess ground rent, lease term and unit title — and which deals get approved.",
        "keywords": [
            "leasehold apartment mortgage Auckland",
            "leasehold property NZ home loan",
            "can you get a mortgage on leasehold NZ",
            "unit title mortgage NZ",
            "Auckland apartment finance",
            "leasehold vs freehold NZ",
        ],
        "cta_heading": "Thinking about a leasehold or apartment purchase in Auckland?",
        "cta_sub": "Send us the address and the title type. We will tell you which lenders will look at it before you spend money on legal review.",
        "sections": [
            ("The short answer", (
                p("Yes, you can get a mortgage on an Auckland leasehold apartment — but your lender choice narrows sharply, and several main banks will not lend on leasehold at all. The ones that do usually want a bigger deposit, and some will only lend over a shorter term than the 30 years you might expect.")
                + p("The reason is simple. With leasehold you do not own the land. You own the building or the right to occupy, and you pay ground rent to the landowner under a lease with a fixed end date. A bank taking that as security is taking a wasting asset, and it prices and structures accordingly.")
                + callout("Why the price looks low", "Leasehold apartments often advertise well below comparable freehold stock. That discount is not a deal — it is the market pricing in ground rent, rent review risk and a finite lease. Judge the total cost of ownership, not the purchase price.")
            )),
            ("Leasehold, freehold and unit title are three different things", (
                p("These terms get used loosely in Auckland listings, and the difference changes both your finance and your long-term costs.")
                + table(
                    ["Title type", "What you own", "Typical lender view"],
                    [
                        ["Freehold (fee simple)", "The land and everything on it, indefinitely.", "Most straightforward. Standard lending applies."],
                        ["Unit title", "Your unit, plus a share of common property, governed by a body corporate.", "Widely accepted. Lenders scrutinise body corporate health and levies."],
                        ["Cross-lease", "An undivided share of the land with other owners, plus a lease of your dwelling.", "Generally accepted, but defects in the flats plan can stall an approval."],
                        ["Leasehold", "The right to occupy for a fixed term. The land stays with the landowner.", "Most restrictive. Several lenders decline outright."],
                    ],
                )
                + p("Note that leasehold and unit title are not mutually exclusive. Plenty of Auckland apartments are unit titles sitting on leasehold land, which means you get both the body corporate obligations and the ground rent.")
            )),
            ("What lenders actually look at on a leasehold file", (
                p("When we take a leasehold apartment to a lender, these are the points that decide the outcome:")
                + ul([
                    "<strong>Years left on the lease.</strong> This is the big one. A long unexpired term is far more financeable than a short one, and as the remaining term shrinks, lender appetite drops and loan terms get cut to match.",
                    "<strong>Ground rent and the review mechanism.</strong> How much is payable now, how often it is reviewed, and on what basis. A lease with periodic market reviews carries real risk of a step change in your outgoings.",
                    "<strong>Who the landowner is.</strong> Leases held by councils, trusts or iwi entities are assessed differently from private landowners, and the lease terms vary accordingly.",
                    "<strong>Floor area.</strong> Many lenders apply a minimum apartment size and require a larger deposit below it. The threshold and the treatment vary by lender, which is exactly why shopping the file matters.",
                    "<strong>Body corporate health.</strong> Levy levels, the long-term maintenance plan, the state of the reserve fund, and any special levies on the horizon.",
                ])
            )),
            ("The documents to get before you commit", (
                p("For a unit title purchase the Unit Titles Act requires the seller to give you a pre-contract disclosure statement, and you can request an additional disclosure statement. Use that right. For leasehold you also want the lease itself, in full.")
                + ol([
                    "The full lease document, including the rent review clause and the expiry date.",
                    "Pre-contract and additional disclosure statements for a unit title.",
                    "The body corporate's long-term maintenance plan and most recent financial statements.",
                    "Minutes of recent body corporate meetings — this is where looming special levies surface first.",
                    "A registered valuation, which your lender will usually require anyway.",
                ])
                + p("Have your solicitor read the lease before you go unconditional, not after. " + link("../blog/hidden-costs-buying-house-nz.html", "The hidden costs of buying in NZ") + " covers the other outgoings people miss.")
            )),
            ("Resale and the long view", (
                p("The question that catches buyers out is not whether they can finance it today. It is whether the next buyer can finance it in ten years, when the lease is a decade shorter. If lender appetite has tightened by then, your pool of buyers shrinks and so does your price.")
                + p("That does not make leasehold a mistake. For some buyers — particularly those wanting a central Auckland base and not treating the property as a long-term capital asset — the maths works. But it should be a decision made with the lease term and review schedule in front of you.")
            )),
            ("How we approach these", (
                p("Leasehold is one of the clearest cases where lender choice decides the outcome. The same apartment, same buyer, same deposit can be a decline at one bank and a straightforward approval at another. Because we are not tied to one lender, we check appetite before the application goes anywhere — so you are not collecting declines on your credit file while you work out who lends on what.")
                + p("Send us the listing and the title type. We will tell you where it can be placed, and what deposit each option is likely to want.")
            )),
        ],
        "faqs": [
            ("Will a bank lend on a leasehold apartment in Auckland?",
             "Some will and some will not. Several main banks decline leasehold outright, while others will lend with a larger deposit and sometimes a shorter loan term. The unexpired lease term, the ground rent review mechanism and the apartment's floor area are the main factors. Because policy differs so much between lenders, it is worth checking appetite before you make an offer."),
            ("How many years left on a lease do lenders want to see?",
             "There is no single industry figure, and each lender sets its own policy. The general principle is that the longer the unexpired term, the more comfortable lenders are, and that some will shorten your maximum loan term so the loan is repaid well inside the remaining lease. A lease with only a short period left is very difficult to finance."),
            ("Is a unit title apartment harder to finance than a standalone house?",
             "Not usually, but there is more to check. Lenders look at the body corporate's financial position, levy levels and the long-term maintenance plan, and many apply a minimum floor area below which a larger deposit is required. A well-run body corporate and a reasonable floor area generally present no problem."),
            ("What is the difference between leasehold and cross-lease?",
             "With leasehold you do not own the land at all — you hold a lease over it for a fixed term and pay ground rent. With cross-lease you do own the land, as an undivided share held jointly with the other owners, plus a lease of your own dwelling. Cross-lease is generally financeable; leasehold is far more restricted."),
        ],
        "faq_heading": "Leasehold apartment finance: common questions",
        "related": REL_CORE + [
            ("cross-lease-unit-title-freehold-nz.html", "Cross-Lease vs Freehold",
             "How title type changes your loan."),
            ("../case-studies/apartment-investor-scaling.html", "Apartment Investor Case Study",
             "Scaling a portfolio of apartments."),
            ("../locations/home-loan-auckland-city.html", "Home Loans in Auckland",
             "Local lending advice for Auckland."),
        ],
    },

    {
        "slug": "cross-lease-unit-title-freehold-nz",
        "title": "Cross-Lease vs Freehold vs Unit Title NZ | Finch",
        "h1": "Cross-Lease vs Freehold vs Unit Title in NZ",
        "section_label": "NZ Property Titles",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Property titles", "Cross-lease", "Unit titles"],
        "intro_pull": "Your title type decides more than you think — how much you can borrow, how fast you can settle, and whether a renovation needs your neighbour's signature.",
        "description": "Cross-lease, freehold and unit title explained for NZ buyers: what each means for your mortgage, your renovation plans and your resale value.",
        "keywords": [
            "cross lease vs freehold NZ",
            "unit title vs cross lease",
            "what is cross lease NZ",
            "defective cross lease NZ",
            "NZ property title types mortgage",
            "cross lease mortgage approval NZ",
        ],
        "cta_heading": "Not sure what your title type means for your loan?",
        "cta_sub": "Send us the address. We will tell you how lenders are likely to treat the title and what it means for your deposit.",
        "sections": [
            ("Why title type matters to a lender", (
                p("A mortgage is a loan secured against a property. So the bank's first question is not really about you — it is about what exactly it would be able to sell if things went wrong. Title type answers that question, and it is why two identical-looking houses on the same street can get different lending treatment.")
                + p("Around three-quarters of New Zealand residential property is freehold, which is why most buyers never think about this. The other quarter is where the complications live.")
            )),
            ("Freehold (fee simple)", (
                p("You own the land and the buildings on it, indefinitely, with no shared ownership and no ground rent. You can renovate, subdivide or demolish subject only to council rules and your district plan.")
                + p("From a lending point of view this is the baseline. Standard loan terms, standard deposit requirements, no additional title scrutiny. If you have a choice and the numbers are comparable, freehold is the simplest thing to own and the simplest thing to sell.")
            )),
            ("Cross-lease: the one that causes surprises", (
                p("Cross-lease is a legacy of decades of NZ subdivision. You and the other owners jointly own the whole piece of land as an undivided share, and each of you holds a long lease over your own dwelling and its defined exclusive-use area. Typically there is a 'flats plan' showing where each building and area sits.")
                + p("Lenders generally lend on cross-lease without much fuss. The problem is not the structure, it is when the structure stops matching reality.")
                + callout("The defective cross-lease trap", "If someone has added a deck, carport, conservatory or extension that is not shown on the flats plan, the cross-lease becomes 'defective'. The title no longer describes the building. That can delay a settlement, require the other owners to sign a new flats plan, and in some cases hold up finance until it is resolved.")
                + p("Fixing a defective cross-lease means a surveyor, a new flats plan, and the co-operation and signatures of every other owner on the title. If a neighbour is unwilling or unreachable, it can take a long time. Your solicitor should check the flats plan against what is physically there before you go unconditional.")
            )),
            ("Unit title: body corporate territory", (
                p("Unit titles are governed by the Unit Titles Act 2010. You own your unit, plus an undivided share of the common property, and you are automatically a member of the body corporate that manages it. Apartments, townhouse developments and many modern terraces are unit titles.")
                + p("What lenders care about here is the body corporate's financial health:")
                + ul([
                    "<strong>Levy levels</strong> — these are a committed ongoing expense and count against your serviceability, the same way a car loan repayment does.",
                    "<strong>The long-term maintenance plan</strong> — is the building's future maintenance actually funded?",
                    "<strong>Special levies</strong> — a looming one-off levy for reclad or structural work can be very large, and it surfaces in meeting minutes before it surfaces anywhere else.",
                    "<strong>Floor area</strong> — many lenders apply a minimum size for apartments and want a bigger deposit below it.",
                ])
                + p("Use your disclosure rights. The seller must provide a pre-contract disclosure statement, and you can request an additional disclosure statement with more detail. Read both.")
            )),
            ("Leasehold: you do not own the land", (
                p("With leasehold you hold the right to occupy for a fixed term and pay ground rent to the landowner. Several lenders decline leasehold outright and those that do lend typically want a larger deposit. If you are looking at leasehold, read " + link("leasehold-apartment-mortgage-auckland.html", "our guide to leasehold apartment mortgages") + " before going any further.")
            )),
            ("What to check before you make an offer", (
                ol([
                    "Get the record of title and read what type it is — do not rely on the listing.",
                    "For cross-lease, compare the flats plan against the actual building, including decks and outbuildings.",
                    "For unit title, get the disclosure statements, the long-term maintenance plan and recent meeting minutes.",
                    "For leasehold, get the full lease, the expiry date and the rent review clause.",
                    "Tell your broker the title type up front, so lender appetite is checked before you are committed.",
                ])
                + p("None of these title types is automatically a bad buy. But each changes who will lend, how much, and how quickly — and the cost of finding that out late is measured in lost deposits and failed finance conditions.")
            )),
        ],
        "faqs": [
            ("Is a cross-lease property harder to get a mortgage on?",
             "Usually no. Lenders generally treat cross-lease much like freehold. The complication arises when the flats plan does not match what has actually been built — an unconsented deck or extension, for example — which makes the cross-lease 'defective' and can delay both finance and settlement until it is corrected."),
            ("What makes a cross-lease defective, and who fixes it?",
             "A cross-lease is defective when the physical buildings and exclusive-use areas no longer match the registered flats plan. Fixing it requires a surveyor to prepare an updated flats plan and the agreement and signatures of all the other owners on the title. That co-operation requirement is what makes it slow."),
            ("Do body corporate levies affect how much I can borrow?",
             "Yes. Lenders treat levies as a committed ongoing expense in your serviceability assessment, in much the same way as a loan repayment or insurance premium. Higher levies reduce the amount you can borrow, so factor them in early rather than at application."),
            ("Is freehold always the best title to buy?",
             "Freehold is the simplest to own, finance and sell, so where the price is comparable it is usually the easier choice. But plenty of good properties are cross-lease or unit title, and those titles are entirely financeable. The point is to understand what you are buying and check the specific risks for that title type."),
        ],
        "faq_heading": "NZ property titles: common questions",
        "related": REL_CORE + [
            ("leasehold-apartment-mortgage-auckland.html", "Leasehold Apartments Auckland",
             "Financing leasehold property."),
            ("lim-builders-report-finance-nz.html", "LIM & Builder's Reports",
             "When a report kills your finance."),
            ("hidden-costs-buying-house-nz.html", "Hidden Costs of Buying",
             "The outgoings buyers forget."),
        ],
    },

    {
        "slug": "earthquake-prone-building-mortgage-wellington",
        "title": "Earthquake-Prone Buildings & Wellington Mortgages",
        "h1": "Earthquake-Prone Buildings and Wellington Mortgages",
        "section_label": "Wellington Property",
        "region": "Wellington",
        "lead_service": "Home Loan",
        "about": ["Earthquake-prone buildings", "Seismic strengthening", "Wellington property"],
        "intro_pull": "In Wellington, the seismic rating on a building can matter more to your finance than your income does. Usually it is not the bank that stops the deal — it is the insurer.",
        "description": "How seismic ratings and earthquake-prone building notices affect Wellington mortgages, why insurance is the real blocker, and what to check before you offer.",
        "keywords": [
            "earthquake prone building mortgage NZ",
            "seismic rating mortgage Wellington",
            "NBS rating home loan NZ",
            "Wellington apartment earthquake mortgage",
            "earthquake prone building insurance NZ",
            "Wellington mortgage broker seismic",
        ],
        "cta_heading": "Looking at a Wellington property with a seismic question mark?",
        "cta_sub": "Send us the address and any engineering report you have. We will tell you whether it is financeable before you pay for legal review.",
        "sections": [
            ("The thing most buyers get wrong", (
                p("People assume the bank is the obstacle. In Wellington it usually is not. The bank's condition is that the property must be insurable — and it is the insurer who decides that. A building that cannot get full replacement insurance generally cannot get a standard mortgage, no matter how strong your application is.")
                + p("So the order of questions matters. Before you ask whether a lender will approve the loan, find out whether an insurer will cover the building, and on what terms.")
            )),
            ("What %NBS actually means", (
                p("Seismic performance is expressed as a percentage of New Building Standard, written %NBS. It is an engineer's assessment of how the building would perform in a design-level earthquake compared with an equivalent new build.")
                + p("Under the Building Act, a building assessed below 34%NBS is classed as earthquake-prone. The territorial authority issues an earthquake-prone building notice, the building goes on the national EPB register, and a deadline is set for strengthening work. Wellington has a high concentration of these because of its seismicity and its older building stock.")
                + table(
                    ["Assessment", "Status", "What it usually means for finance"],
                    [
                        ["Below 34%NBS", "Earthquake-prone. Notice issued, on the EPB register.", "Hardest case. Insurance is often the binding constraint; specialist lending may be the only route."],
                        ["34-66%NBS", "Not earthquake-prone, but below new-build standard.", "Varies widely. Insurer appetite and the engineering detail drive the outcome."],
                        ["67%NBS and above", "Generally regarded as acceptable.", "Usually treated as standard residential lending."],
                    ],
                )
                + callout("Ratings are opinions, not facts", "A %NBS figure comes from a specific engineer using a specific assessment method at a specific time. A later, more detailed assessment can land on a different number. If a deal hinges on the rating, find out what kind of assessment produced it and how old it is.")
            )),
            ("Where this bites hardest: apartments and body corporates", (
                p("For a standalone timber-framed house, seismic rating is rarely the issue — light timber construction generally performs well and these properties are not usually assessed at all. The problem concentrates in multi-unit buildings, particularly older concrete and masonry apartment blocks in and around the central city.")
                + p("In a unit title building, strengthening is a body corporate matter, and the cost is shared across owners by unit entitlement. That has two consequences for you:")
                + ul([
                    "A special levy for strengthening work can be very large, and it is your liability as an owner even if the work was agreed before you bought.",
                    "A building partway through the strengthening process can be in limbo — not yet compliant, with costs agreed but not yet spent.",
                ])
                + p("Meeting minutes and the long-term maintenance plan are where you find this. Read them before you go unconditional, not after.")
            )),
            ("What to get before you make an offer", (
                ol([
                    "Check the council's earthquake-prone building register for the address.",
                    "Ask for any seismic assessment on the building, and note whether it is an initial or detailed engineering evaluation, and its date.",
                    "For a unit title, get the disclosure statements, long-term maintenance plan and recent minutes, and look specifically for strengthening resolutions and levies.",
                    "Get an indicative insurance quote early. This is the step buyers skip and it is the one that most often ends the deal.",
                    "Talk to your broker before the offer, with the rating and the insurance position in hand.",
                ])
            )),
            ("Strengthened buildings can be a genuine opportunity", (
                p("The flip side is worth saying. A building that has completed its strengthening work, has the documentation to prove it and a rating comfortably above the threshold can be good buying — because the market often discounts the whole category rather than the individual building, and because the big capital cost has already been incurred by previous owners.")
                + p("The key is documentary evidence: the engineering sign-off, the scope of what was done, and confirmation from the council. With that in hand, these properties generally finance normally.")
            )),
            ("How we work these files", (
                p("Seismic files need sequencing rather than optimism. We start with insurability, then match the property to lenders whose policy fits that specific situation, and only then put an application together. That avoids the common pattern of a buyer collecting two declines before anyone checks whether the building could be insured at all.")
                + p("If you are looking in Wellington and the building has any seismic history, send it to us early. See also our " + link("../locations/home-loan-wellington.html", "Wellington home loan page") + " for how we work in the region.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage on an earthquake-prone building in NZ?",
             "It is difficult but not always impossible. The usual blocker is insurance rather than the lender — most mortgages require the property to be insured, so if an insurer will not provide cover, standard lending generally will not proceed. Where cover is available, some specialist lenders may consider the file, typically with a larger deposit."),
            ("What seismic rating do banks want to see?",
             "There is no single published figure and each lender and insurer sets its own approach. In practice, buildings assessed at 67%NBS or above are generally treated as standard, those below 34%NBS are classed as earthquake-prone and are the hardest to finance, and the middle band is assessed case by case on the engineering detail and insurer appetite."),
            ("Does a seismic rating affect standalone houses in Wellington?",
             "Rarely. Light timber-framed houses generally perform well in earthquakes and are not usually subject to seismic assessment or earthquake-prone notices. The issue concentrates in older multi-unit concrete and masonry buildings, particularly apartments in and near the central city."),
            ("Who pays for strengthening work in an apartment building?",
             "In a unit title building the strengthening is a body corporate project and the cost is shared among owners according to unit entitlement, usually through a special levy. That liability attaches to you as owner, including where the work was resolved before you purchased, which is why reading the body corporate minutes before you commit matters."),
        ],
        "faq_heading": "Seismic ratings and Wellington finance: common questions",
        "related": REL_CORE + [
            ("../locations/home-loan-wellington.html", "Home Loans in Wellington",
             "Local lending advice for the capital."),
            ("lim-builders-report-finance-nz.html", "LIM & Builder's Reports",
             "What reports reveal before you buy."),
            ("flood-zone-insurance-mortgage-decline-nz.html", "Flood Zones & Insurance",
             "When insurance stops a mortgage."),
        ],
    },

    {
        "slug": "tc2-tc3-land-christchurch-mortgage",
        "title": "TC2 & TC3 Land in Christchurch: Lending Explained",
        "h1": "TC2 and TC3 Land in Christchurch: How Lending Works",
        "section_label": "Canterbury Property",
        "region": "Christchurch",
        "lead_service": "Home Loan",
        "about": ["Technical categories", "Canterbury land", "Christchurch property"],
        "intro_pull": "Technical category zoning still shapes Christchurch lending more than a decade on. TC3 does not mean unfinanceable — it means the file needs different evidence.",
        "description": "How TC1, TC2 and TC3 land classifications affect Christchurch mortgages, what lenders ask for on TC3, and how past claim history changes a file.",
        "keywords": [
            "TC3 land mortgage Christchurch",
            "TC2 TC3 technical category lending",
            "Christchurch mortgage land zoning",
            "Canterbury home loan TC3",
            "EQC claim history mortgage NZ",
            "Christchurch mortgage broker",
        ],
        "cta_heading": "Buying on TC2 or TC3 land in Canterbury?",
        "cta_sub": "Send us the address and any geotech or claim documentation. We will tell you which lenders will take it and what they will want to see.",
        "sections": [
            ("What the technical categories mean", (
                p("After the 2010 and 2011 Canterbury earthquakes, residential land across greater Christchurch was mapped into technical categories describing how the ground is expected to perform in future earthquakes, principally its vulnerability to liquefaction. The categories drive what foundation design is required for new building work.")
                + table(
                    ["Category", "Land performance expectation", "Foundation implication"],
                    [
                        ["TC1", "Liquefaction damage unlikely.", "Standard foundations generally suitable."],
                        ["TC2", "Minor to moderate liquefaction damage possible.", "More robust foundation design required for new build."],
                        ["TC3", "Moderate to significant liquefaction damage possible.", "Site-specific geotechnical investigation required to design foundations."],
                    ],
                )
                + p("The categories describe the land, not the house sitting on it. A well-built, undamaged, fully repaired home on TC3 land can be a perfectly sound purchase. The category tells you what engineering scrutiny applies, not whether the property is a problem.")
            )),
            ("How lenders actually treat each category", (
                p("TC1 and TC2 are generally unremarkable for lending purposes — these are the majority of greater Christchurch properties and they are financed every day without special conditions.")
                + p("TC3 is where files need more care. Lenders are not primarily worried about the zoning label; they are worried about two things it implies:")
                + ul([
                    "<strong>Insurability.</strong> As everywhere in New Zealand, the lender needs the property insured. Insurer appetite and the terms offered are the first thing to establish.",
                    "<strong>Valuation certainty.</strong> Lenders want confidence in what the property is worth and what condition it is genuinely in, which on TC3 can mean wanting more than a desktop assessment.",
                ])
                + callout("The usual reality", "Most TC3 purchases of already-repaired, insured homes finance normally. The hard cases are unrepaired damage, incomplete or undocumented repairs, and vacant TC3 land where someone intends to build.")
            )),
            ("Claim history is the part people under-prepare", (
                p("Canterbury properties often carry a history: earthquake claims, repairs done under various programmes, cash settlements, and sometimes repairs that were scoped but never completed. For a lender and an insurer, the question is what was damaged, what was actually fixed, and whether it was signed off.")
                + p("What you want in hand:")
                + ol([
                    "The claim history for the property, including any settlements, through the Natural Hazards Commission (formerly EQC) and the private insurer.",
                    "Documentation of repair scope and completion — what was done, by whom, and with what sign-off.",
                    "Consent records and code compliance certificates for any structural repair work, available from the council and on the LIM.",
                    "Confirmation that the property is currently insurable, ideally an indicative quote.",
                ])
                + p("A cash-settled claim where the owner kept the money and never did the repair is a specific trap. The damage is still there, the money has gone, and both insurer and lender will want to know how it will be remediated.")
            )),
            ("Building new on TC3", (
                p("If you are buying TC3 land to build, the geotechnical investigation is not optional — it drives the foundation design, and the foundation design drives the build cost. That matters for finance because a construction loan is assessed on a fixed-price build contract.")
                + p("Get the geotech work done before you lock in a budget. A TC3 foundation can cost materially more than a TC1 equivalent, and discovering that after you have signed a build contract is an expensive way to learn it. Our " + link("../services/construction-loan.html", "construction loan page") + " explains how progressive drawdowns work.")
            )),
            ("What to do before you offer", (
                ol([
                    "Find the technical category for the address — Canterbury Maps and the LIM will tell you.",
                    "Order the LIM early and read the hazard and consent sections.",
                    "Request the full claim and repair history from the vendor.",
                    "Get an indicative insurance quote for the specific address.",
                    "Send the package to your broker before the finance condition clock starts.",
                ])
                + p("Canterbury is a market where local knowledge genuinely changes outcomes, because the documentation trail is unusually long and lender comfort depends on how well it is presented. See our " + link("../locations/home-loan-christchurch.html", "Christchurch home loan page") + " for how we work in the region.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage on TC3 land in Christchurch?",
             "Yes, in most cases. TC3 land is financed regularly, particularly where the home has been repaired, the repairs are documented and the property is insurable. The harder cases are unrepaired or undocumented earthquake damage, cash-settled claims where the repair was never completed, and vacant TC3 land where foundation costs are not yet established."),
            ("Does TC3 zoning reduce what a property is worth?",
             "The technical category can affect buyer sentiment and the cost of future building work, but it is only one input into value. A registered valuation reflects the specific property, its condition, repair history and location. Two TC3 properties can value very differently depending on whether the repair trail is clean and complete."),
            ("What does a lender want to see for a Canterbury property with claim history?",
             "Broadly: what was damaged, what was repaired, who did it and whether it was signed off. That usually means claim and settlement records, repair scope and completion documentation, consent and code compliance records for structural work, and confirmation that the property can currently be insured."),
            ("Is the technical category about the land or the house?",
             "The land. Technical categories describe expected ground performance in future earthquakes, mainly liquefaction vulnerability, and they determine what foundation design is needed for new building work. The condition of the existing house is assessed separately, through the valuation, any builder's report and the repair history."),
        ],
        "faq_heading": "TC zoning and Canterbury lending: common questions",
        "related": REL_CORE + [
            ("../locations/home-loan-christchurch.html", "Home Loans in Christchurch",
             "Local lending advice for Canterbury."),
            ("../services/construction-loan.html", "Construction Loans",
             "How progressive drawdowns work."),
            ("lim-builders-report-finance-nz.html", "LIM & Builder's Reports",
             "Reading the reports that matter."),
        ],
    },

    {
        "slug": "flood-zone-insurance-mortgage-decline-nz",
        "title": "Flood Zones & Insurance: Why NZ Loans Get Declined",
        "h1": "Flood Zones and Insurance-Driven Mortgage Declines",
        "section_label": "NZ Property Risk",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Flood risk", "Property insurance", "Natural hazards"],
        "intro_pull": "The fastest-growing reason NZ home loans fall over has nothing to do with the borrower. If an insurer will not cover the address, the mortgage usually cannot proceed.",
        "description": "Why flood risk and insurance refusals are stopping NZ mortgages, how risk-based pricing works by address, and what to check before you make an offer.",
        "keywords": [
            "flood zone mortgage NZ",
            "insurance declined mortgage NZ",
            "can't get insurance can't get mortgage NZ",
            "NZ flood risk property finance",
            "risk based insurance pricing NZ",
            "natural hazard LIM report NZ",
        ],
        "cta_heading": "Worried an address might not be insurable?",
        "cta_sub": "Send us the property details. We will help you sequence the insurance and finance checks in the right order, before you are committed.",
        "sections": [
            ("No insurance, no mortgage", (
                p("Almost every New Zealand mortgage contains a condition requiring the property to be insured for full replacement, with the lender noted on the policy. That condition is not negotiable, because the lender's security is the building. If the building burns down or washes away uninsured, the security is gone.")
                + p("This creates a chain that catches buyers out. The lender will approve your loan subject to insurance. You then discover the insurer will not cover that address, or will only cover it with a flood exclusion, or at a premium several times what you budgeted. The finance condition fails — and it fails for reasons that have nothing to do with your income or deposit.")
                + callout("Sequence matters", "Check insurability before you check borrowing capacity on a property you are worried about. An indicative insurance quote for the specific address costs you nothing and takes a phone call. A failed finance condition can cost you your deposit.")
            )),
            ("What changed in the NZ insurance market", (
                p("New Zealand insurers have moved steadily from broad community pricing toward risk-based pricing by individual address. Where premiums were once set largely by region and sum insured, insurers now model hazard exposure much more precisely — flood, coastal inundation, erosion, landslip and seismicity.")
                + p("The practical consequences for buyers:")
                + ul([
                    "Two houses on the same street can attract very different premiums if one sits lower or closer to a watercourse.",
                    "Some addresses attract flood exclusions rather than outright declines — cover for everything except the risk you most need covered.",
                    "Premiums and excesses on higher-risk addresses can change materially at renewal, which affects your ongoing serviceability, not just your purchase.",
                    "A property that was insurable five years ago is not guaranteed to be insurable today.",
                ])
            )),
            ("How lenders factor hazard risk in", (
                p("Lenders approach this from two directions. First, the hard requirement that the property be insured. Second, and more quietly, through valuation — a valuer assessing a property with known flood history will reflect that in the figure, and a lower valuation means a lower loan against the same purchase price.")
                + p("Insurance premiums also count as a committed expense in serviceability. An annual premium several times the norm reduces what you can borrow, in the same way body corporate levies or a car loan repayment do.")
            )),
            ("Where to find the risk information", (
                ol([
                    "<strong>The LIM report.</strong> Councils must disclose known natural hazard information they hold. Flood history, overland flow paths and inundation risk generally appear here. Order it early.",
                    "<strong>Council hazard maps.</strong> Most territorial authorities publish flood hazard and coastal inundation mapping online, free to search by address.",
                    "<strong>An indicative insurance quote.</strong> The single most useful check. Insurers price the actual address, so this reveals what no map will tell you.",
                    "<strong>The vendor and neighbours.</strong> Ask directly whether the property has flooded and whether a claim was made. Claim history follows the property.",
                    "<strong>The record of title and any drainage diagrams.</strong> These can reveal overland flow paths across the site.",
                ])
            )),
            ("If you still want the property", (
                p("A flagged hazard is not automatically a reason to walk away. Plenty of good homes sit in areas with some mapped flood risk and insure normally. What matters is getting specific:")
                + ul([
                    "Get a written insurance position for the address, including any exclusions and the excess, before you go unconditional.",
                    "Make your finance condition realistic in length so there is time to resolve insurance. See " + link("finance-condition-sale-purchase-nz.html", "how long a finance condition really needs") + ".",
                    "Budget the actual premium into your serviceability, not an average figure.",
                    "Think about resale. If insurability is tightening in that area, your future buyer faces the same chain you just worked through.",
                ])
            )),
            ("How we handle hazard-flagged properties", (
                p("We treat insurance as a gate, not a formality. If a property has flood history or sits in a mapped hazard area, we want the insurance position established before the lender application goes in — because an approval subject to a condition that cannot be met is not an approval.")
                + p("Send us the address and the LIM if you have it. We will tell you what to establish, in what order, and which lenders are most comfortable with the situation.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage if I can't insure the house?",
             "Generally no. Standard New Zealand mortgages require the property to be insured for full replacement with the lender noted on the policy, because the building is the lender's security. If no insurer will provide cover, the finance condition will usually fail regardless of how strong the rest of your application is."),
            ("Does a flood zone always mean a mortgage decline?",
             "No. Many properties in mapped flood-risk areas are insured and financed normally. What matters is the specific address: whether an insurer will cover it, on what terms, what the premium and excess are, and whether there is a claim history. Get a written insurance position before you go unconditional."),
            ("Where do I find out if a NZ property has flooded before?",
             "Start with the LIM report, which discloses natural hazard information the council holds, and the council's online flood hazard maps. Then ask the vendor directly about flooding and claims, and get an indicative insurance quote for the address — insurers price individual addresses and will often reveal risk the maps do not show."),
            ("Do high insurance premiums reduce how much I can borrow?",
             "Yes. Lenders count insurance premiums as a committed ongoing expense when assessing serviceability. An unusually high premium on a hazard-exposed property reduces your borrowing capacity, so use the actual quoted figure in your budgeting rather than a regional average."),
        ],
        "faq_heading": "Flood risk, insurance and finance: common questions",
        "related": REL_CORE + [
            ("lim-builders-report-finance-nz.html", "LIM & Builder's Reports",
             "What the reports disclose."),
            ("finance-condition-sale-purchase-nz.html", "Finance Conditions Explained",
             "How long you really need."),
            ("hidden-costs-buying-house-nz.html", "Hidden Costs of Buying",
             "Insurance and the rest."),
        ],
    },

    {
        "slug": "lifestyle-block-rural-lending-waikato",
        "title": "Lifestyle Block & Rural Lending in NZ | Finch",
        "h1": "Lifestyle Block and Rural-Residential Lending in NZ",
        "section_label": "Rural & Lifestyle",
        "region": "Waikato",
        "lead_service": "Home Loan",
        "about": ["Lifestyle blocks", "Rural lending", "Waikato property"],
        "intro_pull": "The moment a property crosses from residential into lifestyle, the lending rules change — deposit, land area limits, and whether the land's income counts at all.",
        "description": "How NZ lenders assess lifestyle blocks and rural-residential property: land area thresholds, deposit requirements, and why farm income rarely counts.",
        "keywords": [
            "lifestyle block mortgage NZ",
            "rural residential home loan NZ",
            "lifestyle block deposit NZ",
            "Waikato lifestyle block finance",
            "rural lending NZ bank",
            "hectare limit mortgage NZ",
        ],
        "cta_heading": "Looking at a lifestyle block in the Waikato or beyond?",
        "cta_sub": "Tell us the land area, the title and what is on it. We will tell you which lenders treat it as residential and what deposit each will want.",
        "sections": [
            ("Where residential stops and lifestyle begins", (
                p("Lenders divide property into categories, and the category determines the policy applied. A standard suburban section is residential. A 20-hectare dairy unit is rural commercial. Lifestyle blocks sit in the awkward middle, and each lender draws the line in a different place.")
                + p("The main trigger is land area. Beyond a certain size, a lender stops treating the property as a house with a big garden and starts treating it as rural land with a house on it. That shift changes your maximum lending, your deposit, and sometimes your interest rate.")
                + callout("The thresholds vary — deliberately check", "Lenders set their own land area limits for residential policy, and the common thresholds sit at a few hectares, with further tiers above that. Because the cut-offs differ between lenders, the same 6-hectare block can be residential lending at one bank and rural at another. This is one of the clearest cases where lender choice changes your deposit.")
            )),
            ("What changes once a property is classed rural or lifestyle", (
                table(
                    ["Factor", "Standard residential", "Lifestyle / rural-residential"],
                    [
                        ["Maximum loan-to-value", "Standard residential LVR settings apply.", "Typically more conservative — a larger deposit is usually required."],
                        ["Land income", "Not applicable.", "Income from grazing, cropping or leasing is usually discounted heavily or excluded."],
                        ["Valuation", "Often a desktop or short-form valuation.", "Usually a full registered valuation, sometimes with a rural specialist."],
                        ["Water and services", "Reticulated supply assumed.", "Tank water, bore, septic and shared access are all assessed."],
                        ["Loan type", "Standard home loan.", "May be a rural or lifestyle product, with different pricing."],
                    ],
                )
            )),
            ("Why the land's income usually does not help you", (
                p("Buyers are often surprised that a block running stock, or with a grazing lease in place, does not improve their borrowing capacity. The lender's reasoning is that the income is variable, seasonal, dependent on commodity prices and weather, and frequently not well documented.")
                + p("In practice most lenders assessing a lifestyle purchase will either exclude land-derived income or shade it very heavily, and will assess your serviceability on your employment or business income instead. If the land income is genuinely substantial and well documented over multiple years, it is worth presenting — but plan your budget on the assumption it will not move the needle.")
            )),
            ("The practical things that stall rural files", (
                ul([
                    "<strong>Water supply.</strong> Tank or bore rather than reticulated. Lenders and insurers want to know the supply is adequate and potable, and valuers factor it in.",
                    "<strong>Wastewater.</strong> Septic systems need to be consented and functioning. An unconsented or failing system is a valuation and insurance issue.",
                    "<strong>Access.</strong> Right-of-way easements, shared driveways and unformed legal road access all need checking on the title.",
                    "<strong>Outbuildings.</strong> Sheds, barns and implement sheds built without consent are common on older blocks, and unconsented structures affect both value and insurance.",
                    "<strong>Contamination history.</strong> Former horticultural or spray sheds can trigger HAIL considerations on the LIM, which affects both lending and future development.",
                ])
                + p("Order the LIM early on a rural purchase. There is usually more on it than on a suburban equivalent, and it takes longer to work through. Our guide to " + link("lim-builders-report-finance-nz.html", "LIM and builder's reports") + " covers what to look for.")
            )),
            ("Building or adding a dwelling", (
                p("Many lifestyle purchases come with a plan — a second dwelling, a minor unit for family, or a shed conversion. Two things to know before you budget on that:")
                + ol([
                    "Whether the district plan and the title allow an additional dwelling at all. Rural zoning is often restrictive and a second dwelling may need resource consent.",
                    "That construction lending on rural land is assessed differently from a suburban build, with a fixed-price contract and progressive drawdowns. See our " + link("../services/construction-loan.html", "construction loan page") + " and our guide to " + link("granny-flats-minor-dwellings-finance-nz.html", "minor dwelling finance") + ".",
                ])
            )),
            ("How to approach a lifestyle purchase", (
                p("The single most useful thing you can do is establish the lender position before you fall in love with a block. Land area, title type, water, wastewater and access determine which lenders can look at it, and the deposit requirement can differ by a meaningful margin between them.")
                + p("Send us the listing and the title. We will tell you where it sits in each lender's policy and what deposit to plan for — before you are committed to a finance condition you cannot meet.")
            )),
        ],
        "faqs": [
            ("How much deposit do I need for a lifestyle block in NZ?",
             "More than for a standard residential purchase, in most cases. Once a property falls outside a lender's residential land area threshold, loan-to-value limits typically tighten. The exact requirement varies significantly between lenders, and because each sets its own land area cut-off, the same block can attract different deposit requirements at different banks."),
            ("Will income from grazing or leasing the land help my application?",
             "Usually very little. Most lenders assessing a lifestyle purchase exclude land-derived income or discount it heavily, because it is variable, seasonal and often poorly documented. Serviceability is generally assessed on your employment or business income, so budget on the basis that land income will not increase your borrowing capacity."),
            ("At what size does a property stop being residential for lending?",
             "There is no single national threshold — each lender sets its own, and the common cut-offs sit at a few hectares with further tiers above. That variation is why the same property can be residential lending at one bank and rural at another, and why it is worth checking policy before making an offer."),
            ("What do lenders check on a rural property that they skip in town?",
             "Water supply (tank or bore rather than reticulated), wastewater and septic consent, legal access and rights of way, whether outbuildings were consented, and any contamination history from former horticultural use. These usually require a full registered valuation rather than a desktop assessment."),
        ],
        "faq_heading": "Lifestyle block lending: common questions",
        "related": REL_CORE + [
            ("../case-studies/lifestyle-block-rural-purchase.html", "Lifestyle Block Case Study",
             "A rural purchase, start to finish."),
            ("granny-flats-minor-dwellings-finance-nz.html", "Minor Dwelling Finance",
             "Funding a second dwelling."),
            ("../locations/home-loan-hamilton.html", "Home Loans in Hamilton",
             "Lending across the Waikato."),
        ],
    },

    {
        "slug": "queenstown-holiday-home-short-stay-income-mortgage",
        "title": "Queenstown Holiday Homes & Short-Stay Income Loans",
        "h1": "Queenstown Holiday Homes and Short-Stay Income",
        "section_label": "Queenstown Property",
        "region": "Queenstown",
        "lead_service": "Investment Property Loan",
        "about": ["Holiday homes", "Short-stay accommodation", "Queenstown property"],
        "intro_pull": "The Airbnb projection in the listing is not the number your bank will use. Here is how lenders actually treat short-stay income on a Queenstown purchase.",
        "description": "How NZ lenders assess short-stay and Airbnb income on Queenstown holiday homes, why projections are discounted, and what deposit second homes need.",
        "keywords": [
            "Queenstown holiday home mortgage",
            "Airbnb income mortgage NZ",
            "short stay income home loan NZ",
            "second home deposit NZ",
            "holiday home finance Queenstown",
            "short term rental mortgage NZ",
        ],
        "cta_heading": "Buying a holiday home or short-stay property in Queenstown?",
        "cta_sub": "Tell us the property and how you plan to use it. We will show you which lenders count short-stay income and what they will actually credit.",
        "sections": [
            ("The projection problem", (
                p("Queenstown listings routinely include short-stay income projections, and they can look compelling. The difficulty is that a projection is a forecast prepared by someone with an interest in the sale, and lenders assess security and serviceability on evidence.")
                + p("As a general rule, the less established and the more variable an income stream is, the more heavily a lender discounts it. Short-stay accommodation income is seasonal, highly sensitive to tourism conditions, dependent on platform dynamics and exposed to regulatory change. That puts it at the cautious end of the spectrum.")
                + callout("Plan for zero, be pleased by more", "The safest way to budget a short-stay purchase is to assume the lender credits none of the projected income and assess whether you can service the loan on your other income. If a lender does give partial credit, that is upside — not the foundation of the plan.")
            )),
            ("How lenders treat short-stay income", (
                p("Lender policy on short-stay income ranges from excluding it entirely to accepting a shaded portion where there is an established trading history. The factors that move a lender toward giving it some credit:")
                + ul([
                    "<strong>Documented history.</strong> Actual platform statements and tax returns showing income across multiple years, ideally including a weak season, carry far more weight than a projection.",
                    "<strong>Whether it is declared.</strong> Income that appears in filed tax returns is assessable. Income that does not, is not.",
                    "<strong>Managed or self-managed.</strong> A professional management agreement with a track record is easier to evidence than informal self-management.",
                    "<strong>Consent position.</strong> Whether the property is lawfully permitted to be used for short-stay accommodation under the district plan and any body corporate rules.",
                ])
                + p("Where a lender does count it, expect a meaningful discount to reflect vacancy, seasonality and costs. Long-term residential rental income is generally treated more generously than short-stay income, for the same reasons.")
            )),
            ("The consent and body corporate question", (
                p("This is the issue that surprises buyers most. Short-stay accommodation is a particular use of land, and whether it is permitted depends on the district plan, the zone, and in apartments the body corporate rules.")
                + p("Before you buy on the basis of short-stay income, establish:")
                + ol([
                    "Whether the district plan permits short-stay accommodation at that property, for the number of nights you intend, and whether resource consent is required.",
                    "Whether any existing resource consent is in place and transfers with the property.",
                    "For a unit title, whether the body corporate operating rules permit short-stay letting at all — many restrict or prohibit it.",
                    "What rates category the property sits in, since commercial or mixed-use rating can materially change your outgoings.",
                ])
                + p("A property you cannot lawfully let short-stay is simply a holiday home, and should be budgeted as one.")
            )),
            ("Second homes and deposits", (
                p("A holiday home you do not live in is not your owner-occupied home, and it is generally not a standard investment property either. Lenders categorise it as a second home or a holiday home, and the deposit expectation usually sits above owner-occupied levels.")
                + p("Two structural points worth understanding:")
                + ul([
                    "If you are using equity in your existing home to fund the purchase, the structure matters — how the loans are split affects flexibility, and potentially the deductibility of interest. See " + link("using-home-equity-investment-property-nz.html", "using home equity to buy another property") + ".",
                    "Investment and second-home lending has its own loan-to-value settings, and residential investment property is treated differently again from a purely personal holiday home.",
                ])
                + p("Get the intended use clear with your adviser at the outset, because changing the stated purpose later can require restructuring.")
            )),
            ("Tax is a separate question — get advice", (
                p("Short-stay income is taxable, and there are specific rules about mixed-use assets where a property is used privately for part of the year and income-earningly for the rest. There can also be GST implications once short-stay turnover passes the registration threshold, and selling a GST-registered property has its own consequences.")
                + p("These are accountant questions, not broker questions, and they can change the economics of the purchase significantly. Get tax advice before you commit, not at the end of your first financial year. Also read our guide to the " + link("bright-line-test-nz-2026.html", "bright-line test") + " if you might sell within a few years.")
            )),
            ("How we structure these purchases", (
                p("Queenstown files work best when the income assumption is conservative and the consent position is nailed down first. We establish what each lender will actually credit from short-stay income, confirm the property can lawfully be used that way, and then structure the lending around the income you can genuinely evidence.")
                + p("Send us the property and your plan for it. See also our " + link("../locations/investment-property-queenstown.html", "Queenstown investment property page") + ".")
            )),
        ],
        "faqs": [
            ("Will a NZ bank count Airbnb income towards my mortgage?",
             "Some will count a portion, some will not count it at all. Where it is counted, lenders generally want a documented trading history across multiple years, evidenced in platform statements and filed tax returns, and they apply a significant discount for seasonality and vacancy. Projections supplied with a listing carry little weight."),
            ("How much deposit do I need for a holiday home in NZ?",
             "Typically more than for the home you live in. Lenders classify a property you do not occupy as a second home or an investment, and loan-to-value requirements are more conservative than owner-occupied lending. The exact figure depends on the lender, the property type and how the lending is structured."),
            ("Do I need resource consent to run a property as short-stay accommodation?",
             "It depends on the district plan, the zone and how many nights a year you intend to let it. Some councils permit limited short-stay letting as of right and require consent beyond a threshold. In apartments the body corporate operating rules may restrict or prohibit short-stay letting entirely, regardless of the council position."),
            ("Is short-stay income treated the same as long-term rental income?",
             "No. Long-term residential rental income is generally assessed more generously because it is more stable and easier to evidence through a tenancy agreement. Short-stay income is seasonal, variable and exposed to regulatory change, so lenders discount it more heavily or exclude it."),
        ],
        "faq_heading": "Queenstown holiday home finance: common questions",
        "related": REL_INVEST + [
            ("../locations/investment-property-queenstown.html", "Queenstown Investment Property",
             "Local investor lending."),
            ("bright-line-test-nz-2026.html", "Bright-Line Test 2026",
             "Tax on selling within the window."),
            ("../case-studies/second-home-holiday-home-purchase.html", "Holiday Home Case Study",
             "How one purchase was structured."),
        ],
    },

    {
        "slug": "healthy-homes-standards-lending-nz",
        "title": "Healthy Homes Standards & NZ Investor Lending",
        "h1": "Healthy Homes Standards and Investor Lending",
        "section_label": "NZ Property Investment",
        "region": None,
        "lead_service": "Investment Property Loan",
        "about": ["Healthy Homes Standards", "Rental property compliance", "Property investment"],
        "intro_pull": "Compliance is not optional and it is not cheap. For investors, the question is whether the remediation cost is in your purchase budget or a surprise after settlement.",
        "description": "What the Healthy Homes Standards require of NZ rentals, how compliance costs affect investment lending, and how to budget remediation into a purchase.",
        "keywords": [
            "Healthy Homes Standards NZ compliance",
            "healthy homes investment property loan",
            "rental property compliance cost NZ",
            "NZ investor mortgage healthy homes",
            "insulation requirements rental NZ",
            "buying non compliant rental NZ",
        ],
        "cta_heading": "Buying a rental that needs compliance work?",
        "cta_sub": "Tell us the property and what it needs. We will structure the lending so remediation is funded from day one, not scraped together later.",
        "sections": [
            ("What the standards actually require", (
                p("The Healthy Homes Standards sit under the Residential Tenancies Act and set minimum requirements for private rental properties across five areas. They are compulsory, and they are enforced through the Tenancy Tribunal.")
                + table(
                    ["Standard", "What it covers"],
                    [
                        ["Heating", "A fixed heating device in the main living room capable of meeting a required heating capacity, calculated for that room."],
                        ["Insulation", "Ceiling and underfloor insulation meeting the required standard, where it is reasonably practicable to install."],
                        ["Ventilation", "Openable windows in habitable rooms, plus extraction in kitchens and bathrooms."],
                        ["Moisture and drainage", "Efficient drainage, guttering and downpipes, and a ground moisture barrier where there is an enclosed subfloor."],
                        ["Draught stopping", "Unreasonable gaps and holes blocked, and unused open fireplaces closed off or removed."],
                    ],
                )
                + p("Landlords must also provide a compliance statement with new or renewed tenancy agreements. Tenancy Services publishes the detailed technical requirements, including the heating capacity calculator, and that is the authoritative source rather than any summary.")
            )),
            ("Why this is a lending conversation, not just a compliance one", (
                p("For an investor, compliance work is capital expenditure that has to happen, often soon after settlement, and frequently before the property can be lawfully tenanted on a new agreement. That creates a cash flow problem at exactly the moment your reserves are lowest.")
                + p("The mistake we see is buyers budgeting the deposit and the legal fees, then discovering the property needs a heat pump sized for the living room, underfloor insulation, a ground moisture barrier and new guttering. That can be a substantial sum, and if it is not in the lending structure it comes out of savings you may not have.")
                + callout("Fund it at purchase, not after", "It is generally easier to build remediation into the lending at the time of purchase — through the loan structure or an arranged facility — than to go back to a lender for a small top-up six months later. Price the work before you make the offer.")
            )),
            ("How lenders see a non-compliant rental", (
                p("Lenders do not usually refuse to lend because a property is not yet Healthy Homes compliant. What they do care about is the knock-on effects:")
                + ul([
                    "<strong>Valuation.</strong> A valuer assessing a property needing significant work will reflect that in the figure, which reduces your maximum loan against the same purchase price.",
                    "<strong>Rental assessment.</strong> If the property cannot be lawfully tenanted until work is done, the rental income supporting your serviceability is delayed.",
                    "<strong>Condition issues that overlap.</strong> Moisture, drainage and subfloor problems that trigger Healthy Homes requirements often sit alongside issues that matter more to a lender — rot, inadequate drainage, or weathertightness concerns.",
                ])
                + p("So the standards rarely block an approval directly, but they frequently reduce the loan amount and delay the income.")
            )),
            ("Budgeting the work properly", (
                ol([
                    "Get a Healthy Homes assessment before you go unconditional. Specialist assessors will inspect against all five standards and give you a scoped list.",
                    "Price the heating requirement specifically. It is calculated for the actual living room dimensions, and an undersized unit does not comply even if it heats the room adequately in practice.",
                    "Check whether insulation can practicably be installed. Some older properties have access limitations that change the scope and cost.",
                    "Add the moisture barrier and drainage work, which are commonly missed and can involve more labour than expected.",
                    "Take the total to your broker and build it into the lending structure before settlement.",
                ])
            )),
            ("The upside of buying a non-compliant property", (
                p("There is a genuine opportunity here for investors willing to do the work. Properties needing compliance remediation often transact at a discount to comparable compliant stock, because many buyers do not want the project. If you have priced the work accurately and funded it properly, you are buying the discount and capturing the uplift.")
                + p("The condition for that working is accurate pricing. Buying at a discount and then discovering the scope was double your estimate turns the opportunity into a problem. See our " + link("../calculators/rental-yield-calculator.html", "rental yield calculator") + " to model the numbers with remediation included.")
            )),
            ("How we structure investor purchases", (
                p("We ask what the property needs before we ask what you can borrow, because the remediation budget belongs in the lending structure rather than in your back pocket. That usually means establishing the scope, getting it priced, then structuring the purchase and the work together.")
                + p("Send us the property and the assessment if you have one. Our " + link("../services/investment-property.html", "investment property service page") + " explains how we approach investor lending.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage on a rental that is not Healthy Homes compliant?",
             "Generally yes. Non-compliance does not usually stop a lender approving a loan. The practical effects are indirect: the valuation may be lower because of the work required, and if the property cannot be lawfully tenanted on a new agreement until the work is done, the rental income supporting your serviceability is delayed."),
            ("Do Healthy Homes Standards apply to the home I live in?",
             "No. The standards apply to private residential rental properties under the Residential Tenancies Act. If you are buying a home to live in, they do not apply to you — though the underlying issues they address, such as insulation, drainage and moisture, are still worth assessing before you buy."),
            ("Can I borrow the money to do the compliance work?",
             "Often yes, and it is usually easier to arrange at the time of purchase than afterwards. Depending on your equity position and the lender, remediation can be built into the purchase lending or arranged as a separate facility. Price the work before you make an offer so it can be included in the structure."),
            ("What is the most commonly underestimated Healthy Homes cost?",
             "The heating requirement and the ground moisture barrier. Heating capacity is calculated for the specific living room dimensions, so an undersized unit does not comply even if it feels warm enough, and correctly sized units in larger rooms can be expensive. Moisture barriers and associated drainage work involve more labour than most buyers expect."),
        ],
        "faq_heading": "Healthy Homes and investor lending: common questions",
        "related": REL_INVEST + [
            ("../case-studies/leaky-home-remediation-finance.html", "Remediation Finance Case Study",
             "Funding a major repair."),
            ("../calculators/rental-yield-calculator.html", "Rental Yield Calculator",
             "Model yield after remediation."),
            ("mortgage-top-up-nz.html", "Mortgage Top-Up",
             "Borrowing for property work."),
        ],
    },

    # =====================================================================
    # GROUP B — Debt and income blockers
    # =====================================================================

    {
        "slug": "student-loan-mortgage-borrowing-power-nz",
        "title": "How Your Student Loan Affects Your NZ Mortgage",
        "h1": "How Your Student Loan Affects What You Can Borrow",
        "section_label": "Borrowing Power",
        "region": None,
        "lead_service": "First Home Buyer Mortgage",
        "about": ["Student loans", "Borrowing power", "Serviceability"],
        "intro_pull": "It is not the balance that hurts your application — it is the compulsory repayment. Which means paying a chunk off your loan may do less for your borrowing power than you think.",
        "description": "How NZ lenders treat student loan repayments in a mortgage application, why the balance matters less than the repayment, and whether paying it down helps.",
        "keywords": [
            "student loan mortgage NZ",
            "does student loan affect mortgage NZ",
            "student loan borrowing power NZ",
            "pay off student loan before mortgage NZ",
            "student loan home loan application NZ",
            "NZ mortgage serviceability student loan",
        ],
        "cta_heading": "Want to know what your student loan is actually costing you?",
        "cta_sub": "Send us your income and loan balance. We will show you the borrowing difference across lenders — and whether paying it down is worth it.",
        "sections": [
            ("The mechanism, in one paragraph", (
                p("If you live in New Zealand, your student loan repayment is a compulsory deduction taken at a set rate on income above the annual repayment threshold, collected through PAYE. It is not a debt you choose to service — it is taken automatically. Lenders therefore treat it as a fixed, committed expense that reduces the income available to pay a mortgage.")
                + p("The important consequence: the thing driving the impact on your application is the <em>repayment</em>, not the <em>balance</em>. Two applicants on the same income with wildly different loan balances will often have close to the same borrowing capacity, because they are making the same compulsory repayment.")
                + callout("Why paying a lump sum off may not help much", "Reducing your balance from, say, $30,000 to $20,000 does not change your compulsory repayment at all — it is calculated on your income, not your balance. Your borrowing power is largely unchanged. Clearing the loan entirely is what removes the repayment, and that is a very different sum.")
            )),
            ("What that means in practice", (
                p("Work through the logic before you make a decision about your savings:")
                + ol([
                    "A partial lump sum shortens how long you will be repaying, which saves you money over time. Genuinely worthwhile for your long-term finances.",
                    "But it does not increase what a lender will advance today, because the compulsory repayment is unchanged.",
                    "And it reduces your deposit, which <em>does</em> directly reduce what you can buy — and can push you into a higher loan-to-value band with worse pricing.",
                ])
                + p("For most first home buyers, that maths points one way: keep the savings in your deposit. See " + link("deposit-needed-home-loan-nz.html", "how much deposit you actually need") + " for why the deposit lever is usually the stronger one.")
            )),
            ("When clearing the loan does make sense", (
                p("There are situations where paying the loan off in full is the right call:")
                + ul([
                    "<strong>The balance is small.</strong> If you can clear it outright without meaningfully denting your deposit, you remove a committed expense permanently and free up serviceability.",
                    "<strong>You are close to a serviceability ceiling.</strong> If a lender's assessment lands just short of the loan you need, removing the repayment entirely can bridge the gap.",
                    "<strong>You already have a strong deposit.</strong> If you are comfortably above the LVR band you want and have surplus savings, clearing the loan is a reasonable use of the excess.",
                    "<strong>You are heading overseas.</strong> Non-resident borrowers face different, generally stricter student loan repayment obligations and interest applies. That is a separate planning question.",
                ])
            )),
            ("How it interacts with DTI", (
                p("New Zealand lenders operate under debt-to-income restrictions as well as loan-to-value limits. DTI compares your total borrowing to your gross income, and it is a separate constraint from serviceability.")
                + p("Student loans sit slightly awkwardly here. Treatment can differ between lenders, and whether the loan affects your DTI calculation or only your serviceability assessment is a policy question rather than a universal rule. The practical effect is that the same situation can produce different maximum lending at different banks — which is the recurring theme of this article and the reason comparing matters. Our " + link("dti-calculator-debt-to-income-nz.html", "guide to NZ DTI rules") + " explains the framework.")
            )),
            ("What to do before you apply", (
                ol([
                    "Get your actual loan balance and current repayment figures from your myIR account.",
                    "Do not make a lump sum repayment decision until you have modelled both scenarios with a broker.",
                    "Deal with your other consumer debt first. A credit card limit or a car loan usually costs you far more borrowing capacity per dollar than a student loan does — see " + link("car-loan-personal-debt-borrowing-power-nz.html", "what personal debt really costs you") + ".",
                    "Keep your deposit intact unless there is a specific reason to use it elsewhere.",
                ])
            )),
            ("The reassuring part", (
                p("A student loan is one of the least damaging debts you can carry into a mortgage application. It carries no interest while you are New Zealand-based, the repayment is proportional to your income, and it is not a sign of credit stress — lenders see it constantly and it is entirely normal.")
                + p("Plenty of our first home buyer clients buy with a student loan still outstanding. It reduces your capacity somewhat, but it very rarely decides the outcome. Send us your numbers and we will show you the actual difference rather than the one you are imagining.")
            )),
        ],
        "faqs": [
            ("Does a student loan stop you getting a mortgage in NZ?",
             "No. A student loan reduces your borrowing capacity somewhat because the compulsory repayment is treated as a committed expense, but it very rarely prevents approval. It is a normal feature of New Zealand applications and lenders assess it routinely. Many first home buyers purchase with a student loan still outstanding."),
            ("Should I pay off my student loan before applying for a mortgage?",
             "Usually not with money you were going to use as deposit. Your compulsory repayment is calculated on your income, not your balance, so a partial lump sum does not increase what a lender will advance — while reducing your deposit directly reduces what you can buy. Clearing the loan in full does remove the repayment, so it can be worthwhile if the balance is small or you have surplus savings."),
            ("Is it the student loan balance or the repayment that affects my application?",
             "Primarily the repayment. Lenders treat the compulsory deduction as a fixed committed expense reducing the income available to service a mortgage. Because the repayment is based on your income rather than your balance, two people on the same income with very different balances often have similar borrowing capacity."),
            ("Does a student loan affect my DTI calculation?",
             "Treatment varies between lenders, and whether a student loan is captured in the debt-to-income calculation or only in the serviceability assessment is a matter of individual lender policy rather than a single national rule. That variation means the same situation can produce different maximum lending at different banks."),
        ],
        "faq_heading": "Student loans and mortgages: common questions",
        "related": REL_FHB + [
            ("car-loan-personal-debt-borrowing-power-nz.html", "Car Loans & Personal Debt",
             "What consumer debt really costs."),
            ("dti-calculator-debt-to-income-nz.html", "NZ DTI Rules",
             "How income caps limit borrowing."),
            ("../calculators/borrowing-power.html", "Borrowing Power Calculator",
             "Model your own numbers."),
        ],
    },

    {
        "slug": "afterpay-bnpl-mortgage-application-nz",
        "title": "Afterpay, Laybuy & BNPL: The Drag on Your Mortgage",
        "h1": "Afterpay, Laybuy and BNPL on a Mortgage Application",
        "section_label": "Borrowing Power",
        "region": None,
        "lead_service": "First Home Buyer Mortgage",
        "about": ["Buy now pay later", "Credit assessment", "Bank statements"],
        "intro_pull": "Buy now pay later rarely shows up on a credit report. It shows up on your bank statements — and that is exactly where the assessor is looking.",
        "description": "How NZ lenders view Afterpay, Laybuy and other BNPL use on a mortgage application, what your bank statements reveal, and how long before applying to stop.",
        "keywords": [
            "Afterpay mortgage application NZ",
            "does buy now pay later affect mortgage NZ",
            "Laybuy mortgage NZ",
            "BNPL home loan application NZ",
            "bank statements mortgage assessment NZ",
            "mortgage application spending habits NZ",
        ],
        "cta_heading": "Not sure how your bank statements will read?",
        "cta_sub": "We review statements before any lender does. Send us three months and we will tell you what an assessor would flag — and how to fix it.",
        "sections": [
            ("Where BNPL actually shows up", (
                p("Buy now pay later sits in an unusual position. Many BNPL providers have historically not reported to the main New Zealand credit bureaux in the way a bank loan does, so a clean credit report does not mean your BNPL use is invisible.")
                + p("What lenders ask for is three to six months of bank statements. Every Afterpay, Laybuy, Zip or Klarna instalment appears there, by name, dated, with an amount. An assessor reading your statements sees your BNPL use in full detail regardless of what your credit report says.")
                + callout("The two separate problems", "BNPL creates two distinct issues. First, the instalments are an outgoing that counts against your serviceability. Second, and more consequential, frequent BNPL use is read as a signal about how you manage money — reliance on short-term credit for everyday purchases.")
            )),
            ("How an assessor reads your statements", (
                p("A credit assessor is building a picture of your actual spending behaviour, not just totting up declared expenses. On your statements they are looking for:")
                + ul([
                    "<strong>Frequency.</strong> Occasional BNPL use for a large purchase reads very differently from a dozen concurrent instalment streams.",
                    "<strong>Concurrency.</strong> Several active BNPL arrangements running at once suggests the facility is funding routine spending.",
                    "<strong>Dishonours and late fees.</strong> A failed BNPL direct debit is a significant red flag — it indicates you ran out of money on a scheduled payment date.",
                    "<strong>Timing relative to payday.</strong> Spending that consistently runs out before the next pay cycle is a serviceability signal in itself.",
                    "<strong>Overdraft use alongside it.</strong> BNPL instalments pushing an account into overdraft compounds the picture considerably.",
                ])
                + p("None of these is an automatic decline. Together, a pattern of heavy reliance can reduce your assessed surplus, prompt a lender to question your declared living expenses, or in some cases tip a marginal application the wrong way.")
            )),
            ("The clean-up timeline", (
                p("Because lenders look at three to six months of statements, the fix needs lead time. If you intend to apply for a mortgage, work backwards:")
                + table(
                    ["Timing", "What to do"],
                    [
                        ["6 months out", "Stop opening new BNPL arrangements. Begin paying down existing ones."],
                        ["3-4 months out", "Clear and close BNPL accounts entirely. Closed is better than zero-balance — an open facility is an available liability."],
                        ["3 months out", "Start the statement period you want an assessor to read. From here, your statements are the evidence."],
                        ["Application", "Statements show no BNPL activity, no dishonours, and a consistent surplus each pay cycle."],
                    ],
                )
                + p("If you cannot wait three months, that is not fatal — it just means the application needs to be placed with a lender whose policy fits, and the rest of the file needs to be strong. That is a conversation to have before applying rather than after a decline.")
            )),
            ("Why closing the account matters, not just clearing it", (
                p("This mirrors how lenders treat credit cards. An available credit facility is assessed as a potential liability, because you could draw on it tomorrow. A credit card with a $10,000 limit and a zero balance still reduces your borrowing capacity, because the lender assesses a notional repayment against the limit rather than the balance.")
                + p("BNPL facilities work similarly in the assessor's mind. Clearing the balance helps; closing the account and removing the available limit helps more. The same logic applies to overdrafts and unused store cards — see " + link("car-loan-personal-debt-borrowing-power-nz.html", "what personal debt really costs your borrowing power") + ".")
            )),
            ("What not to do", (
                ul([
                    "<strong>Do not hide it.</strong> You will be providing statements. Undeclared outgoings that appear on statements damage your credibility, and credibility is doing real work in a marginal file.",
                    "<strong>Do not shuffle money between accounts to obscure the pattern.</strong> Assessors read transfers and it reads worse than the original spending.",
                    "<strong>Do not open a personal loan to consolidate BNPL just before applying.</strong> You have converted a short-term facility into a documented term debt, which may serve you worse.",
                    "<strong>Do not assume a good credit score covers it.</strong> The statements are a separate and more detailed source of evidence.",
                ])
            )),
            ("The honest perspective", (
                p("BNPL use is extremely common and lenders know it. A few instalments for a washing machine will not derail your application. What causes problems is a statement that reads as consistently stretched — multiple concurrent arrangements, dishonours, and spending running out before payday.")
                + p("If that describes your last three months, the answer is usually time rather than a different lender. Three to four clean months changes the picture substantially. Send us your statements and we will tell you honestly where you stand and how long you need.")
            )),
        ],
        "faqs": [
            ("Does Afterpay affect a mortgage application in New Zealand?",
             "It can. Many BNPL providers do not report to the credit bureaux the way a bank loan does, so it may not appear on your credit report — but lenders request three to six months of bank statements, where every instalment is visible. Assessors treat the instalments as an outgoing and read frequent use as a signal about how you manage money."),
            ("How long before applying should I stop using BNPL?",
             "Aim for three to four months of clean statements, since that is the period lenders typically review. Ideally stop opening new arrangements around six months out, clear and close existing accounts by three to four months out, and let the statements the assessor reads show no BNPL activity and a consistent surplus."),
            ("Is it enough to pay off my BNPL balance, or should I close the account?",
             "Closing is better. An open facility with available credit is assessed as a potential liability because you could draw on it at any time, in the same way a zero-balance credit card with a high limit still reduces borrowing capacity. Clearing the balance helps; removing the facility helps more."),
            ("Will one or two BNPL purchases ruin my application?",
             "No. Occasional use for a larger purchase is unremarkable and lenders see it constantly. The problems arise with a pattern of heavy reliance — several concurrent arrangements, dishonoured direct debits, or spending that consistently runs out before the next pay cycle."),
        ],
        "faq_heading": "BNPL and mortgage applications: common questions",
        "related": REL_FHB + [
            ("car-loan-personal-debt-borrowing-power-nz.html", "Car Loans & Personal Debt",
             "The real cost to your borrowing."),
            ("improve-credit-score-mortgage-nz.html", "Improve Your Credit Score",
             "Before you apply."),
            ("mortgage-document-checklist-nz.html", "Document Checklist",
             "Everything banks ask for."),
        ],
    },

    {
        "slug": "car-loan-personal-debt-borrowing-power-nz",
        "title": "What Car Loans & Credit Cards Cost Your Mortgage",
        "h1": "What Car Loans and Credit Cards Really Cost You",
        "section_label": "Borrowing Power",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Consumer debt", "Credit cards", "Borrowing power"],
        "intro_pull": "A credit card you never use can cost you tens of thousands in borrowing power. Lenders assess your limit, not your balance — and that changes what you should do before applying.",
        "description": "How NZ lenders assess car loans, credit cards and overdrafts in a mortgage application, why limits matter more than balances, and what to clear first.",
        "keywords": [
            "car loan affect mortgage NZ",
            "credit card limit mortgage borrowing power NZ",
            "personal debt home loan NZ",
            "does credit card affect mortgage NZ",
            "overdraft mortgage application NZ",
            "reduce debt before mortgage NZ",
        ],
        "cta_heading": "Want to know which debt to clear first?",
        "cta_sub": "Send us your debts and limits. We will show you which one is costing you the most borrowing power — and what clearing it actually buys you.",
        "sections": [
            ("The rule that surprises everyone", (
                p("For revolving credit — credit cards and overdrafts — most New Zealand lenders assess a notional monthly repayment calculated against your <em>credit limit</em>, not your current balance. The logic is that you could max the card tomorrow, so the lender must assume you might.")
                + p("That produces a counterintuitive result. A credit card with a $15,000 limit and a zero balance still reduces your borrowing capacity, often substantially. You are being assessed as though you owe the full limit and are repaying it.")
                + callout("The highest-leverage thing you can do", "Reducing or cancelling unused credit card limits is frequently the single most effective way to increase your borrowing capacity — and it costs you nothing. Many buyers spend months saving a bigger deposit when cancelling a dormant card would have moved them further.")
            )),
            ("How each debt type is treated", (
                table(
                    ["Debt type", "How lenders generally assess it", "Best action before applying"],
                    [
                        ["Credit card", "A notional monthly repayment against the full limit, regardless of balance.", "Reduce the limit or close the card entirely."],
                        ["Overdraft", "Similarly assessed against the facility limit.", "Reduce or remove the facility."],
                        ["Car loan / personal loan", "The actual contracted repayment, for the remaining term.", "Pay out if close to the end; otherwise weigh against deposit."],
                        ["Hire purchase / store finance", "The actual repayment. Interest-free terms still count.", "Clear where practical — these are often small but add up."],
                        ["Student loan", "The compulsory income-based repayment.", "Usually leave alone — see our student loan guide."],
                        ["BNPL", "Instalments as an outgoing, plus a behavioural signal.", "Clear and close three to four months out."],
                    ],
                )
                + p("The pattern: for revolving facilities the limit is what matters, and for term debt the contracted repayment is what matters.")
            )),
            ("Why a car loan hits harder than its size suggests", (
                p("Car loans are usually assessed on the actual repayment, which sounds fair. The problem is the scale of the repayment relative to the balance — consumer car finance is typically repaid over a short term, so the monthly commitment is large for the amount owed.")
                + p("A car loan with a modest remaining balance but a substantial monthly repayment consumes serviceability out of proportion to the debt. And every dollar of monthly commitment removed translates into a multiple of that in additional mortgage capacity, because a mortgage is assessed over a much longer term.")
                + p("This is why the question is rarely 'should I pay off debt or save deposit' in the abstract. It depends which debt. Clearing a car loan with high repayments relative to its balance often does more for your borrowing power than the equivalent added to your deposit. Clearing a student loan generally does not.")
            )),
            ("The order to deal with things", (
                ol([
                    "<strong>Cancel or reduce unused credit card and overdraft limits.</strong> Free, immediate, and often the biggest single gain.",
                    "<strong>Clear small consumer debts</strong> — store cards, hire purchase, interest-free arrangements. Individually minor, collectively meaningful, and they clutter your statements.",
                    "<strong>Close BNPL facilities</strong> three to four months before applying. See " + link("afterpay-bnpl-mortgage-application-nz.html", "our guide to BNPL on applications") + ".",
                    "<strong>Then assess the car loan.</strong> If it can be cleared without gutting your deposit, usually worth doing. If clearing it would push you into a worse loan-to-value band, model both scenarios first.",
                    "<strong>Leave the student loan</strong> unless the balance is small enough to clear outright. See " + link("student-loan-mortgage-borrowing-power-nz.html", "why paying it down may not help") + ".",
                ])
            )),
            ("Debt consolidation: useful or counterproductive?", (
                p("Consolidating several debts into one loan can simplify your position and reduce total repayments, which helps serviceability. But timing matters. Taking out a new personal loan weeks before a mortgage application creates a fresh credit enquiry, a newly documented term debt, and a statement history showing recent borrowing — none of which helps.")
                + p("Where consolidation genuinely helps is when it is done well in advance and demonstrably reduces your total monthly commitments. If your debt position is complex, it is worth modelling with a broker before restructuring anything. Our " + link("../case-studies/debt-consolidation.html", "debt consolidation case study") + " shows how one client approached it.")
            )),
            ("Model it before you act", (
                p("The frustrating part of all this is that the arithmetic differs by lender. Notional credit card repayment rates vary, as do treatment of interest-free arrangements and how surplus is calculated. The same set of debts can produce materially different maximum lending at different banks.")
                + p("That is worth using rather than worrying about. Send us a list of your debts, limits and repayments. We will model your capacity across lenders and tell you specifically which actions buy you the most — so you are not paying down the wrong thing for six months.")
            )),
        ],
        "faqs": [
            ("Does a credit card with no balance affect my mortgage?",
             "Yes, usually significantly. Most New Zealand lenders assess a notional monthly repayment against your full credit limit rather than your current balance, on the basis that you could draw the full limit at any time. A high-limit card with a zero balance still reduces your borrowing capacity, which is why reducing or cancelling unused limits is so effective."),
            ("Should I pay off my car loan or save a bigger deposit?",
             "It depends on the repayment size relative to the balance. Car finance is typically repaid over a short term, so the monthly commitment is large for the amount owed, and removing it frees up serviceability out of proportion to the debt. Clearing it is often the better move — but if doing so would push you into a worse loan-to-value band, model both options first."),
            ("Which debt should I clear first before applying for a mortgage?",
             "Start with what is free: reduce or cancel unused credit card and overdraft limits, since these are assessed against the limit. Then clear small consumer debts and close BNPL facilities. Assess a car loan next, weighing it against your deposit. A student loan is usually best left alone unless you can clear it entirely."),
            ("Is debt consolidation a good idea before a mortgage application?",
             "It can help if done well in advance and it genuinely reduces your total monthly commitments. Done shortly before applying it tends to hurt — a new personal loan creates a fresh credit enquiry, a newly documented term debt and recent borrowing activity on your statements. Model it with an adviser before restructuring."),
        ],
        "faq_heading": "Consumer debt and borrowing power: common questions",
        "related": REL_CORE + [
            ("student-loan-mortgage-borrowing-power-nz.html", "Student Loans & Mortgages",
             "Why paying it down may not help."),
            ("afterpay-bnpl-mortgage-application-nz.html", "Afterpay & BNPL",
             "What your statements reveal."),
            ("../case-studies/debt-consolidation.html", "Debt Consolidation Case Study",
             "How one client restructured."),
        ],
    },

    {
        "slug": "mortgage-on-parental-leave-nz",
        "title": "Getting a Mortgage While on Parental Leave in NZ",
        "h1": "Getting a Mortgage While on Parental Leave",
        "section_label": "Income Assessment",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Parental leave", "Income assessment", "Serviceability"],
        "intro_pull": "Lender policy on parental leave varies more than on almost any other income question. One bank's decline is another's straightforward approval — with the same letter from your employer.",
        "description": "How NZ lenders assess income during parental leave, what a return-to-work letter needs to say, and why lender choice matters more here than almost anywhere.",
        "keywords": [
            "mortgage on parental leave NZ",
            "maternity leave home loan NZ",
            "return to work letter mortgage NZ",
            "paid parental leave mortgage application NZ",
            "mortgage while on maternity leave",
            "NZ lender parental leave policy",
        ],
        "cta_heading": "On parental leave and want to buy?",
        "cta_sub": "Tell us your return-to-work plan and pre-leave income. We will find the lenders whose policy fits — before you risk a decline.",
        "sections": [
            ("Why this is a lender-choice problem", (
                p("Most lending obstacles come down to the numbers. This one comes down to policy, and policy on parental leave differs sharply between New Zealand lenders. Broadly, lenders fall into three camps:")
                + ul([
                    "<strong>Assess on pre-leave income</strong> where you can evidence a confirmed return to work, usually within a defined period, on stated hours and pay.",
                    "<strong>Assess on current income only</strong>, which during parental leave means the government entitlement plus any employer top-up — a much lower figure.",
                    "<strong>Assess on a blend or a stepped basis</strong>, sometimes requiring that the loan be serviceable on reduced income for the leave period.",
                ])
                + p("Because the same application can be comfortably approved under the first approach and declined under the second, the lender you approach first effectively determines your outcome. This is not a situation to find out by applying.")
                + callout("Apply once, to the right lender", "Each application generates a credit enquiry, and a cluster of enquiries and declines makes every subsequent application harder. On a parental leave file, establishing policy fit before applying is the whole game.")
            )),
            ("The return-to-work letter does the heavy lifting", (
                p("Where a lender will assess on pre-leave income, the evidence it wants is a letter from your employer. A vague letter gets queried; a specific one gets through. Ask your employer to confirm, in writing on letterhead:")
                + ol([
                    "Your position and that your role is being held for you.",
                    "Your confirmed return date.",
                    "The hours you will return to — full-time, or specified part-time hours.",
                    "The salary or hourly rate on return, stated as a figure.",
                    "That there is no expectation of redundancy or restructure affecting the role.",
                ])
                + p("If you are returning part-time rather than to your previous hours, say so clearly and state the figure. A letter that implies a full-time return when you intend to return three days a week creates a problem later, and lenders do sometimes verify directly with employers.")
            )),
            ("Paid parental leave and what counts", (
                p("Government paid parental leave is an entitlement paid at a capped rate for a set period, and it is genuine income that lenders will recognise — but it is temporary and capped, so on its own it supports far less borrowing than your working salary.")
                + p("Some employers top up parental leave to full or partial salary. Where that happens, get it documented, because it materially improves the picture during the leave period. Also worth noting for the file:")
                + ul([
                    "<strong>Your partner's income.</strong> On a joint application, a partner in stable full-time employment does a great deal of work on serviceability.",
                    "<strong>Accrued leave.</strong> Some applicants plan a return partly funded by annual leave. Document it if relevant.",
                    "<strong>Childcare costs on return.</strong> Lenders will factor these into your post-return expenses, and they can be substantial. Be realistic rather than optimistic here, because an unrealistic figure undermines the whole application.",
                ])
            )),
            ("The expenses side matters more than people expect", (
                p("A new child changes your assessed living expenses permanently, and lenders apply household expense benchmarks that scale with dependants. So even on a file assessed at pre-leave income, your borrowing capacity will usually be lower than it was before the baby.")
                + p("Childcare is the big one. Depending on hours and provider, it can rival a mortgage repayment, and lenders will include it. Twenty hours ECE subsidies and Working for Families support may offset part of it — document what you will actually receive rather than leaving the assessor to assume.")
            )),
            ("Timing strategy", (
                p("You have three broad options, and the right one depends on how urgently you need to buy:")
                + table(
                    ["Approach", "When it works"],
                    [
                        ["Apply during leave with a return-to-work letter", "You have a confirmed return date and a strong joint income. Needs the right lender."],
                        ["Get pre-approved before going on leave", "You are planning ahead. Pre-approvals have a limited validity, so timing matters — see our guide on expired pre-approvals."],
                        ["Wait until back at work", "The simplest path. Usually a payslip or two back at work resolves the issue entirely."],
                    ],
                )
                + p("If you are not under time pressure, waiting until you have one or two payslips from your return is by far the easiest route. If you are buying now, the file needs to be placed deliberately.")
            )),
            ("How we handle these", (
                p("We check policy before we submit. That means asking lenders how they will treat your specific situation — leave period, return date, return hours, partner income — and placing the application where the answer is favourable. It is unglamorous work and it is the difference between an approval and a decline on an identical file.")
                + p("Send us your return-to-work details and your pre-leave income. We will tell you which lenders fit and what evidence to gather. Our " + link("../case-studies/new-job-probation-period-approval.html", "probation period case study") + " shows a similar employment-evidence problem solved.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage while on maternity or parental leave in NZ?",
             "Yes, though it depends heavily on which lender you approach. Some will assess your application on your pre-leave income where you can evidence a confirmed return to work, while others will only consider your current income during leave, which is much lower. Because policy differs so much, establishing lender fit before applying is essential."),
            ("What does a return-to-work letter need to say?",
             "It should be on employer letterhead and confirm your position and that the role is being held, your confirmed return date, the hours you are returning to, the salary or hourly rate on return as a specific figure, and that no redundancy or restructure affects the role. Vague letters get queried; specific ones get through."),
            ("Will childcare costs reduce how much I can borrow?",
             "Yes. Lenders include childcare in your assessed living expenses once you return to work, and the cost can be substantial. Household expense benchmarks also scale with the number of dependants, so your borrowing capacity will usually be lower than before the child regardless of how your income is assessed. Document any subsidies or support you will actually receive."),
            ("Is it better to wait until I am back at work?",
             "If you are not under time pressure, usually yes — one or two payslips after returning generally resolves the income question entirely and widens your lender options considerably. If you need to buy during leave, it is workable, but the application needs to be placed with a lender whose parental leave policy fits your circumstances."),
        ],
        "faq_heading": "Parental leave and mortgages: common questions",
        "related": REL_CORE + [
            ("casual-part-time-seasonal-income-mortgage-nz.html", "Casual & Part-Time Income",
             "Which lenders count it."),
            ("../case-studies/new-job-probation-period-approval.html", "Probation Period Case Study",
             "Approval on a new job."),
            ("pre-approval-expired-nz.html", "Pre-Approval Expired?",
             "What happens next."),
        ],
    },

    {
        "slug": "casual-part-time-seasonal-income-mortgage-nz",
        "title": "Casual, Part-Time & Seasonal Income Mortgages NZ",
        "h1": "Casual, Part-Time and Seasonal Income Mortgages",
        "section_label": "Income Assessment",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Casual income", "Seasonal work", "Income assessment"],
        "intro_pull": "Irregular income is not disqualifying — it just has to be evidenced differently. The applicants who struggle are usually the ones who present a good year instead of a full picture.",
        "description": "How NZ lenders assess casual, part-time, seasonal and variable income for a mortgage, how long a history you need, and how averaging and shading work.",
        "keywords": [
            "casual income mortgage NZ",
            "part time income home loan NZ",
            "seasonal worker mortgage NZ",
            "variable income mortgage application NZ",
            "overtime bonus income mortgage NZ",
            "NZ lender income shading",
        ],
        "cta_heading": "Income that does not fit a simple payslip?",
        "cta_sub": "Send us two years of income history. We will tell you how lenders will average and shade it — and which ones treat it most favourably.",
        "sections": [
            ("The two things lenders are testing", (
                p("With any non-standard income, a lender is answering two questions: is this income <em>consistent enough</em> to rely on, and is it <em>likely to continue</em>? Everything about how irregular income is assessed flows from those two tests.")
                + p("Consistency is demonstrated by history. Continuity is demonstrated by the nature of the work and the relationship with the employer. If you can show both, most lenders will work with you — though they will usually be conservative about the figure they use.")
            )),
            ("How much history you need", (
                p("As a general guide, the less regular the income, the longer the history a lender wants:")
                + table(
                    ["Income type", "Typical history sought", "How it is usually assessed"],
                    [
                        ["Permanent part-time", "Shortest — often a few months in the role.", "Usually taken at face value from payslips and a contract."],
                        ["Regular overtime / shift allowances", "Commonly 6-12 months.", "Averaged, and often shaded to allow for variability."],
                        ["Bonus / commission", "Commonly 1-2 years.", "Averaged over the period, usually shaded."],
                        ["Casual employment", "Commonly 6-12 months with the same employer.", "Averaged, shaded, and continuity of engagement matters."],
                        ["Seasonal work", "Usually 2 years, to capture a full cycle.", "Averaged across the full cycle, including the off-season."],
                    ],
                )
                + p("These are general patterns rather than fixed rules — each lender sets its own requirements and the variation between them is wide. The figures above are a planning guide, not a policy statement.")
                + callout("Averaging and shading explained", "Averaging means a lender takes your income over a period and uses the average rather than your best month. Shading means it then applies a discount to allow for the risk that the income does not continue at that level. Both reduce the figure used — which is why presenting a long, honest history beats presenting a strong recent run.")
            )),
            ("Seasonal income: present the whole cycle", (
                p("Seasonal workers — horticulture, viticulture, tourism, shearing, fishing, and plenty of contracting — have a specific challenge. Income arrives in concentrated periods and the off-season is lean. A lender looking at three months of peak-season payslips sees a figure that is not sustainable across the year.")
                + p("The way through is to present two full years so the lender can see the complete cycle, including the quiet months, and work out a reliable annual figure. Counterintuitively, including your worst months strengthens the application, because it demonstrates you understand your own income pattern and the averaged figure is credible.")
                + p("Also worth showing: that you manage the off-season. Bank statements demonstrating you save through the peak and draw down sensibly through the lean period directly address the lender's core worry.")
            )),
            ("Multiple income sources", (
                p("Many applicants in this category have more than one stream — a part-time permanent role plus casual shifts, or employment plus a side business. Lenders will often consider all of it, but each stream is assessed on its own terms and the weakest-evidenced stream may be excluded entirely.")
                + p("Keep the sources clearly separated in your documentation. Income paid into the same account as everything else, with no clear trail, is much harder for an assessor to credit. If you have self-employed income alongside employment, read " + link("one-year-self-employed-mortgage-nz.html", "our guide to self-employed income") + " as well.")
            )),
            ("Documents to gather", (
                ol([
                    "Two years of IRD income summaries, available through myIR. These are the most useful single document because they are authoritative and show the full picture.",
                    "Payslips covering the longest period you can — ideally spanning a full seasonal cycle.",
                    "Your employment agreement or contract, even for casual work, showing the basis of engagement.",
                    "A letter from your employer confirming the ongoing nature of the engagement and typical hours, where you can get one.",
                    "Bank statements for three to six months, showing the income arriving and how you manage between peaks.",
                ])
                + p("Our " + link("mortgage-document-checklist-nz.html", "full NZ mortgage document checklist") + " covers the rest of the file.")
            )),
            ("The strategic point", (
                p("Lender appetite for irregular income varies enormously, and it is not a simple bank-versus-non-bank split — some main banks are comfortable with well-evidenced casual income while others are not, and the same is true across the non-bank market.")
                + p("What that means practically is that a decline from one lender tells you very little about your actual prospects. If your income is irregular, the file needs to be matched to policy before it is submitted. Send us two years of income history and we will tell you where it fits best and what figure lenders are likely to use.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage on casual income in New Zealand?",
             "Yes. Lenders generally want to see a consistent history with the same employer — commonly six to twelve months — and evidence that the engagement is ongoing. They will typically average your income over the period and apply a discount for variability, so the assessed figure will be lower than your best months suggest."),
            ("How do lenders assess seasonal income?",
             "Usually by averaging across a full cycle, which is why most want around two years of history. Presenting only your peak season produces an unsustainable figure that lenders will not rely on. Including the lean months strengthens the application, as does showing bank statements that demonstrate you save through the peak and manage the off-season."),
            ("What does income shading mean?",
             "Shading is the discount a lender applies to variable income to allow for the risk it does not continue at the same level. Combined with averaging — using your average rather than your best period — it means the income figure used in your assessment is lower than your recent earnings. The size of the discount varies by lender and income type."),
            ("Does overtime count towards a mortgage application?",
             "Often yes, if it is regular and documented. Lenders commonly want six to twelve months of consistent overtime, then average it and apply a discount. Occasional or one-off overtime is less likely to be counted. The same general approach applies to shift allowances, bonuses and commission, usually with a longer history required."),
        ],
        "faq_heading": "Irregular income and mortgages: common questions",
        "related": REL_SELFEMP + [
            ("one-year-self-employed-mortgage-nz.html", "One Year Self-Employed",
             "Can you get a mortgage yet?"),
            ("../case-studies/contractor-fixed-term-income.html", "Contractor Case Study",
             "Fixed-term income approved."),
            ("mortgage-document-checklist-nz.html", "Document Checklist",
             "What to gather first."),
        ],
    },

    {
        "slug": "non-resident-offshore-income-mortgage-nz",
        "title": "Non-Resident & Offshore Income Mortgages in NZ",
        "h1": "Non-Resident and Offshore Income Mortgages in NZ",
        "section_label": "Overseas Buyers",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Non-resident lending", "Offshore income", "Overseas investment rules"],
        "intro_pull": "There are two separate hurdles here, and people routinely conflate them: whether you are legally allowed to buy, and whether a lender will fund it.",
        "description": "Buying NZ property as a non-resident or on offshore income: the Overseas Investment Act rules, which lenders consider it, and how foreign income is assessed.",
        "keywords": [
            "non resident mortgage NZ",
            "offshore income home loan NZ",
            "can foreigners buy property NZ",
            "overseas investment act residential NZ",
            "expat mortgage New Zealand",
            "foreign income mortgage application NZ",
        ],
        "cta_heading": "Buying from overseas or on offshore income?",
        "cta_sub": "Tell us your residency status and where your income is earned. We will tell you the eligibility position and which lenders will look at it.",
        "sections": [
            ("Two separate questions", (
                p("Before anything else, separate these:")
                + ol([
                    "<strong>Are you legally permitted to buy New Zealand residential land?</strong> This is governed by the Overseas Investment Act and administered by Land Information New Zealand. It has nothing to do with lending.",
                    "<strong>Will a lender finance you?</strong> A separate commercial question answered by individual lender policy.",
                ])
                + p("You can be perfectly eligible to buy and still find no lender willing to fund you. You can also have strong income and be legally unable to purchase. Establish both before you spend money.")
                + callout("Get specialist advice on eligibility", "Overseas investment rules are detailed, they turn on your specific status and the type of land, and they have been subject to policy change. Confirm your position with a New Zealand property lawyer and the current LINZ guidance — not with a summary article, including this one.")
            )),
            ("The eligibility side, in outline", (
                p("Since the Overseas Investment Act was amended to cover residential land, most overseas persons require consent to buy residential property in New Zealand, and consent is not routinely granted for ordinary home purchases.")
                + p("The broad position, which you must verify for your own circumstances:")
                + ul([
                    "<strong>New Zealand citizens</strong> can buy freely, whether or not they currently live here.",
                    "<strong>Holders of a residence class visa</strong> who meet residency requirements around actually living in New Zealand are generally treated as not being overseas persons.",
                    "<strong>Australian and Singaporean citizens and permanent residents</strong> have exemptions arising from trade agreements.",
                    "<strong>Other overseas persons</strong> generally require consent, which is limited in scope — certain categories of development and some apartment arrangements are treated differently from standard residential purchases.",
                ])
                + p("The distinction between holding a residence class visa and actually meeting the residency test matters, and it is a common point of confusion. This is lawyer territory.")
            )),
            ("How lenders assess offshore income", (
                p("Separately from eligibility, lenders assessing foreign-earned income are managing several risks at once:")
                + ul([
                    "<strong>Currency risk.</strong> Your income is in one currency and the mortgage is in NZD. Lenders that accept offshore income typically apply a discount to allow for exchange rate movement, often a substantial one.",
                    "<strong>Verification difficulty.</strong> Confirming foreign payslips, tax filings and employer legitimacy is harder, and documents may need translation and certification.",
                    "<strong>Enforcement.</strong> Recovering from a borrower and assets located offshore is more complex.",
                    "<strong>Which currencies.</strong> Lenders that do accept foreign income often restrict it to a defined list of major currencies.",
                ])
                + p("The practical result is that non-resident lending is a narrow market in New Zealand, deposit requirements are typically well above domestic levels, and the income figure used will be materially less than you earn.")
            )),
            ("Returning New Zealanders are a different case", (
                p("If you are a New Zealand citizen coming home, your position is much stronger on both counts. Eligibility is not an issue, and lenders are considerably more comfortable — particularly where you have a confirmed New Zealand job to return to.")
                + p("What strengthens a returning Kiwi file:")
                + ol([
                    "A signed New Zealand employment agreement with a start date, position and salary.",
                    "A clear return date and evidence of the move — flights, shipping, a tenancy ended.",
                    "Two years of overseas income documentation and tax filings.",
                    "Evidence of the deposit, including its source, and of funds transferred or ready to transfer.",
                    "A New Zealand credit file where you have one, or overseas credit reports where you do not.",
                ])
                + p("Our " + link("../case-studies/returning-kiwi-overseas-income.html", "returning Kiwi case study") + " walks through how one of these files was structured. If you are on a work visa rather than returning, read " + link("work-visa-home-loan-nz.html", "our work visa home loan guide") + ".")
            )),
            ("Anti-money-laundering requirements", (
                p("Every New Zealand lender and lawyer operates under the AML/CFT regime, and cross-border transactions attract thorough source-of-funds verification. Expect to document not just that you have the deposit but where it came from — and expect that to take longer than you think.")
                + p("Start gathering this early: sale proceeds from an overseas property, a documented savings history, a gift with a signed gifting certificate, or an inheritance with probate documentation. Funds that cannot be traced to a verified source will hold up a settlement regardless of how strong everything else is.")
            )),
            ("How to approach it", (
                p("Sequence it: confirm eligibility with a New Zealand property lawyer, then establish lender appetite for your specific income and residency combination, then look at property. Doing it in the other order wastes money and time.")
                + p("Send us your residency status, where your income is earned and in what currency, and your deposit position. We will tell you honestly whether there is a lending path — and if there is not yet, what would need to change.")
            )),
        ],
        "faqs": [
            ("Can a non-resident buy residential property in New Zealand?",
             "In most cases an overseas person requires consent under the Overseas Investment Act to buy residential land, and consent is not routinely granted for ordinary home purchases. New Zealand citizens can buy freely, holders of a residence class visa who meet residency requirements are generally not treated as overseas persons, and Australian and Singaporean citizens and permanent residents have exemptions. Confirm your own position with a New Zealand property lawyer."),
            ("Will a NZ bank lend against income earned overseas?",
             "Some lenders will, but it is a narrow market. Those that do typically apply a significant discount to foreign income to allow for exchange rate risk, often restrict acceptable currencies to a list of major ones, and require a larger deposit than for domestic borrowers. Verification requirements are also more demanding."),
            ("Is it easier for a returning New Zealander to get a mortgage?",
             "Considerably. Citizenship removes the eligibility question entirely, and lenders are far more comfortable where there is a confirmed New Zealand job to return to. A signed employment agreement with a start date and salary, a clear return date, and two years of documented overseas income make for a strong file."),
            ("What source-of-funds evidence is needed for an overseas deposit?",
             "Lenders and lawyers operate under New Zealand's anti-money-laundering regime and will verify where your deposit came from, not just that you have it. That typically means sale and settlement documents for an overseas property, a documented savings history, a signed gifting certificate for a gift, or probate documentation for an inheritance. Start gathering this early, as it often takes longer than expected."),
        ],
        "faq_heading": "Non-resident and offshore income: common questions",
        "related": REL_CORE + [
            ("work-visa-home-loan-nz.html", "Work Visa Home Loans",
             "Which banks lend to migrants."),
            ("../case-studies/returning-kiwi-overseas-income.html", "Returning Kiwi Case Study",
             "Coming home and buying."),
            ("../case-studies/new-migrant-first-mortgage.html", "New Migrant Case Study",
             "A first NZ mortgage."),
        ],
    },

    {
        "slug": "one-year-self-employed-mortgage-nz",
        "title": "One Year Self-Employed: Can You Get a NZ Mortgage?",
        "h1": "One Year Self-Employed: Can You Get a Mortgage Yet?",
        "section_label": "Self-Employed",
        "region": None,
        "lead_service": "Self-Employed Mortgage",
        "about": ["Self-employed lending", "Business financials", "Income assessment"],
        "intro_pull": "The standard answer is two years of financials. The real answer is that some lenders will work with one — if the file is built to answer the questions two years would have answered.",
        "description": "Can you get a NZ mortgage with only one year of self-employed financials? Which lenders consider it, what evidence strengthens the file, and the alternatives.",
        "keywords": [
            "one year self employed mortgage NZ",
            "self employed mortgage 1 year accounts NZ",
            "new business home loan NZ",
            "self employed mortgage requirements NZ",
            "NZ mortgage without two years financials",
            "contractor mortgage one year NZ",
        ],
        "cta_heading": "One year of trading and ready to buy?",
        "cta_sub": "Send us your financials and your background in the industry. We will tell you honestly whether it is placeable now or worth waiting.",
        "sections": [
            ("The standard position and the exceptions", (
                p("Most New Zealand main banks want two years of completed financial statements and tax returns before they will assess self-employed income. Two years lets them see a trend rather than a snapshot, and smooth out a one-off good or bad year.")
                + p("But 'most banks want two years' is not the same as 'nobody will lend on one'. There is a segment of the market — including some main bank policies in specific circumstances and a broader group of non-bank lenders — that will consider a single year where the surrounding evidence is strong. The question is not whether it is possible but whether <em>your</em> file answers the questions a second year would have answered.")
            )),
            ("What makes a one-year file work", (
                p("The lenders who consider these are looking for continuity and credibility. The strongest cases usually have several of the following:")
                + ul([
                    "<strong>Same industry, same work.</strong> You were a PAYE employee doing this job, and now you do it for yourself. Your income did not appear from nowhere — the structure around it changed. This is the single most persuasive factor.",
                    "<strong>A full year of completed financials</strong> prepared by a chartered accountant, not management accounts or a spreadsheet.",
                    "<strong>Year-to-date figures</strong> for the current year showing the trend has continued or improved.",
                    "<strong>Contracts or a client base</strong> demonstrating forward work — signed agreements, retainers, or a concentrated long-term client relationship.",
                    "<strong>GST returns</strong> corroborating turnover independently of the financial statements.",
                    "<strong>A clean credit file and clean business banking</strong> with no dishonours and consistent drawings.",
                    "<strong>A larger deposit.</strong> This does more work here than almost anywhere else, because it reduces the lender's exposure while the income history is short.",
                ])
                + callout("The industry-continuity point is doing most of the work", "An electrician with eight years at a firm who went out on their own twelve months ago is a very different proposition from someone who started an unrelated business a year ago. If that describes you, say so prominently and document the employment history that preceded it.")
            )),
            ("How self-employed income is actually calculated", (
                p("A common misunderstanding is that lenders look at your business turnover. They do not. They look at the income available to you, which generally means net profit, plus certain add-backs that represent non-cash or discretionary items.")
                + p("Add-backs commonly considered include depreciation, interest on business debt being refinanced, and one-off non-recurring expenses. Treatment varies between lenders and some are more generous than others. Where there are two years of figures, most lenders will either average them or use the lower year, depending on the trend.")
                + p("This is why your accountant matters to your mortgage. Financials prepared to minimise tax can understate the income available for lending purposes. If you plan to buy, talk to your accountant about it before the financials are finalised — not after.")
            )),
            ("The alternatives if one year is not enough", (
                table(
                    ["Option", "How it works", "Trade-off"],
                    [
                        ["Wait for year two", "Apply once the second year's financials are complete.", "Simplest and cheapest, but costs you time in the market."],
                        ["Non-bank lender now, refinance later", "Borrow on one year's figures, then move to a main bank once you have two.", "Higher rate and possible fees in the interim; needs an exit plan."],
                        ["Larger deposit", "Reduce the loan-to-value to bring more lenders into range.", "Requires available funds."],
                        ["Family guarantee or gifted equity", "A family member supports the application with security or a gift.", "Real obligations for the guarantor — needs independent legal advice."],
                        ["Joint application", "Apply with a partner in stable PAYE employment.", "Only works if their income carries enough of the serviceability."],
                    ],
                )
                + p("The non-bank-then-refinance path is a legitimate strategy, but only with a clear exit. Go in knowing what you will need to qualify for the refinance and roughly when. Our " + link("../case-studies/non-bank-to-bank-refinance-credit-repair.html", "non-bank to bank refinance case study") + " shows how that sequencing works in practice.")
            )),
            ("What to prepare", (
                ol([
                    "Completed financial statements and tax return for your first full year, prepared by a chartered accountant.",
                    "Year-to-date management figures for the current year.",
                    "GST returns covering the trading period.",
                    "Your employment history before going self-employed — CV, prior payslips, or a reference confirming the same industry.",
                    "Contracts, retainers or client agreements showing forward work.",
                    "Twelve months of business and personal bank statements.",
                    "Evidence of your deposit and its source.",
                ])
                + p("See our " + link("../services/self-employed.html", "self-employed mortgage service page") + " for how we build these files.")
            )),
            ("An honest assessment", (
                p("Some one-year files are genuinely placeable now. Others are much better served by waiting a few months for the second year's accounts, because the lending available on one year may come with pricing and conditions that cost more than the delay.")
                + p("We will tell you which situation you are in. Send us your financials and your background — including what you did before — and we will give you a straight answer on whether to go now or wait, and what the difference is likely to cost either way.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage with only one year of self-employed accounts in NZ?",
             "Sometimes. Most main banks prefer two years of completed financials, but some lenders — including certain main bank policies in specific circumstances and a number of non-bank lenders — will consider one year where the supporting evidence is strong. Industry continuity, a larger deposit and documented forward work make the biggest difference."),
            ("What is the single most helpful factor on a one-year file?",
             "Industry continuity. If you were a PAYE employee doing the same work and have simply changed the structure you do it under, lenders can see the income did not appear from nowhere. Document the employment history that preceded the business prominently, as it addresses the lender's main concern directly."),
            ("Do lenders look at my business turnover or my profit?",
             "Profit, broadly. Lenders assess the income available to you, generally net profit plus certain add-backs such as depreciation and some one-off expenses. Turnover is not the figure used. Because financials prepared to minimise tax can understate assessable income, it is worth discussing your plans with your accountant before the accounts are finalised."),
            ("Should I use a non-bank lender now or wait for my second year?",
             "It depends on the cost of each. Borrowing through a non-bank now and refinancing to a main bank once you have two years of figures is a legitimate strategy, but it carries a higher rate in the interim and needs a clear exit plan. Sometimes waiting a few months for the second year's accounts is cheaper overall."),
        ],
        "faq_heading": "One year self-employed: common questions",
        "related": REL_SELFEMP + [
            ("casual-part-time-seasonal-income-mortgage-nz.html", "Casual & Variable Income",
             "How lenders average and shade."),
            ("../case-studies/non-bank-to-bank-refinance-credit-repair.html", "Non-Bank to Bank Refinance",
             "The refinance exit path."),
            ("self-employed-low-deposit-approval.html", "Self-Employed Low Deposit",
             "A low deposit approval."),
        ],
    },

    # =====================================================================
    # GROUP C — Transaction-moment topics
    # =====================================================================

    {
        "slug": "finance-condition-sale-purchase-nz",
        "title": "Finance Conditions in a NZ Sale & Purchase Agreement",
        "h1": "The Finance Condition: How Long You Really Need",
        "section_label": "Buying Process",
        "region": None,
        "lead_service": "Mortgage Pre-Approval",
        "about": ["Finance conditions", "Sale and purchase agreements", "Conditional offers"],
        "intro_pull": "Ten working days sounds generous until a valuation takes a week to book. The finance condition is the most commonly underestimated clause in a New Zealand offer.",
        "description": "How the finance condition in a NZ sale and purchase agreement works, how many working days you actually need, and what happens if you cannot confirm in time.",
        "keywords": [
            "finance condition sale and purchase NZ",
            "how long finance condition NZ",
            "finance clause working days NZ",
            "conditional offer finance NZ",
            "extend finance condition NZ",
            "unconditional offer NZ mortgage",
        ],
        "cta_heading": "Making an offer soon?",
        "cta_sub": "Talk to us before you sign. We will tell you how many working days your situation realistically needs — and get the pre-work done first.",
        "sections": [
            ("What the condition actually commits you to", (
                p("A finance condition in the standard New Zealand sale and purchase agreement gives you a defined period to arrange finance that is satisfactory to you. If you cannot, you can cancel the agreement by giving notice in the manner the agreement requires, within the time it requires.")
                + p("Two things about that are easy to get wrong. First, the period is usually expressed in <strong>working days</strong>, which excludes weekends and public holidays — so ten working days is two calendar weeks, and more over a holiday period. Second, you must actively confirm or cancel. Letting the date pass without doing either puts you in a difficult position, and the vendor may be able to press you to settle or treat you as in default.")
                + callout("Always use your own lawyer's wording", "Do not rely on a standard clause or an agent's suggestion for your finance condition. Your lawyer should draft or review it, because the wording determines what counts as satisfactory finance and how you give notice. This article explains the mechanics; it is not legal advice.")
            )),
            ("Why ten working days is often not enough", (
                p("Agents frequently suggest ten working days because it is conventional and it is attractive to vendors. Whether it works for you depends on what has to happen inside it:")
                + table(
                    ["Step", "Typical time", "Notes"],
                    [
                        ["Submit the file to the lender", "1-2 days", "Fast if your documents are already gathered. Slow if not."],
                        ["Lender assessment", "Several days", "Varies by lender, by queue, and by how complex your income is."],
                        ["Valuation instructed and completed", "Up to a week or more", "Often the bottleneck. Depends on valuer availability in the area."],
                        ["Conditions cleared and approval issued", "1-3 days", "Insurance confirmation, title review, any outstanding items."],
                        ["Your solicitor confirms the condition", "1 day", "Must be done within the period and in the required form."],
                    ],
                )
                + p("Add those up and ten working days is tight for a straightforward PAYE purchase with documents ready — and genuinely risky if your income is self-employed, the property is unusual, or a valuation is required in a region with few valuers.")
            )),
            ("What lengthens the timeline", (
                ul([
                    "<strong>A registered valuation is required.</strong> Much more likely on lower deposits, unusual properties, rural land, apartments and anything with condition issues.",
                    "<strong>Self-employed or variable income.</strong> More documents, more assessment time.",
                    "<strong>Insurance questions.</strong> Hazard-exposed properties can take time to get a written insurance position — see " + link("flood-zone-insurance-mortgage-decline-nz.html", "flood risk and insurance declines") + ".",
                    "<strong>Unusual title.</strong> Leasehold, cross-lease defects or unit title disclosure review all add legal time.",
                    "<strong>Holiday periods.</strong> Working days exclude public holidays, but lender and valuer capacity also drops around Christmas and Easter.",
                ])
            )),
            ("Pre-approval does not remove the need for the condition", (
                p("This is the most consequential misunderstanding in the process. A pre-approval is an indication of what a lender will lend <em>you</em>, usually subject to conditions, and it is not approval to buy a <em>specific property</em>.")
                + p("Once you have an accepted offer, the lender still has to assess the property — valuation, title, insurability, and whether it fits the lender's security policy. A pre-approved buyer can still have finance fall over because of the property. So even with a pre-approval in hand, you need a finance condition unless you are genuinely prepared to carry the risk.")
                + p("Where a pre-approval helps enormously is speed: the income and credit side is already assessed, so the remaining work is about the property. That can turn a risky ten working days into a comfortable one. Our " + link("mortgage-pre-approval-timeline.html", "pre-approval timeline guide") + " explains the sequence.")
            )),
            ("Auctions are a different situation entirely", (
                p("At auction there is no finance condition. A successful bid is an unconditional purchase, and the deposit is payable immediately. You need your finance arranged for that specific property beforehand — including the valuation and the lender's agreement on that security.")
                + p("If you are bidding, read " + link("buying-at-auction-nz-finance-ready.html", "how to be finance-ready to bid") + " first. The preparation is substantially more involved than for a conditional offer, and the consequence of getting it wrong is losing your deposit.")
            )),
            ("If you need more time", (
                p("You can ask for an extension. Your solicitor requests it from the vendor's solicitor before the condition date, and the vendor may agree or decline — in a competitive market, or where there is a backup offer, they may well decline.")
                + p("Practical rules:")
                + ol([
                    "Ask early. Requesting an extension on the morning of the deadline is much weaker than flagging it three days out.",
                    "Have a reason and a realistic new date. 'The valuation is booked for Thursday' is persuasive. 'We need more time' is not.",
                    "Never confirm the condition on the assumption approval is coming. Confirming makes you unconditional, and if finance then fails you are liable.",
                    "Keep your broker and solicitor talking to each other directly. Most late scrambles are communication failures, not lending failures.",
                ])
                + p("The better answer is to negotiate a realistic period at the outset. A vendor who wants a clean sale would usually rather give you fifteen working days than have the deal collapse at day ten.")
            )),
            ("How we work alongside your offer", (
                p("We would always rather hear from you before you sign than after. Given a day's notice we can tell you what your situation realistically needs, get the income side pre-assessed, and have the file ready to submit the moment the offer is accepted — which is what turns the condition period into a formality instead of a race.")
                + p("Send us the property and your situation before you make an offer.")
            )),
        ],
        "faqs": [
            ("How many working days should I allow for a finance condition in NZ?",
             "Ten working days is conventional but often tight. A straightforward PAYE purchase with documents already gathered can work within it, but allow longer — commonly fifteen working days or more — if you are self-employed, a registered valuation is likely, the property is unusual or rural, or there are insurance questions. Remember working days exclude weekends and public holidays."),
            ("Do I still need a finance condition if I have pre-approval?",
             "Generally yes. A pre-approval assesses you, not a specific property, and is usually subject to conditions. Once you have an accepted offer the lender still assesses the property itself — valuation, title and insurability — so finance can still fall over for property reasons. Pre-approval makes the condition period much faster, but it does not remove the need for it."),
            ("What happens if I cannot confirm finance in time?",
             "You should ask your solicitor to request an extension from the vendor's solicitor before the condition date, giving a reason and a realistic new date. The vendor may decline. What you must not do is confirm the condition in the hope approval arrives — confirming makes you unconditional and you become liable to complete the purchase."),
            ("Can I put a finance condition in an auction purchase?",
             "No. A successful auction bid is an unconditional purchase with the deposit payable immediately, so there is no finance condition to rely on. You need your finance arranged for that specific property before bidding, including the valuation and the lender's agreement to accept it as security."),
        ],
        "faq_heading": "Finance conditions: common questions",
        "related": REL_CORE + [
            ("mortgage-pre-approval-timeline.html", "Pre-Approval Timeline",
             "What happens and when."),
            ("buying-at-auction-nz-finance-ready.html", "Finance-Ready for Auction",
             "Bidding without a condition."),
            ("pre-approval-expired-nz.html", "Pre-Approval Expired?",
             "Getting back in the market."),
        ],
    },

    {
        "slug": "pre-approval-expired-nz",
        "title": "Your NZ Mortgage Pre-Approval Expired: What Now?",
        "h1": "Your Pre-Approval Expired: What Happens Now",
        "section_label": "Buying Process",
        "region": None,
        "lead_service": "Mortgage Pre-Approval",
        "about": ["Mortgage pre-approval", "Pre-approval renewal", "Lending policy"],
        "intro_pull": "Renewing is usually straightforward, but it is not automatic — and the amount you are re-approved for can be different, because the rules may have moved while you were house hunting.",
        "description": "What to do when your NZ mortgage pre-approval expires: how renewal works, what documents you need again, and why the amount can change second time around.",
        "keywords": [
            "mortgage pre approval expired NZ",
            "how long does pre approval last NZ",
            "renew mortgage pre approval NZ",
            "pre approval extension NZ",
            "pre approval expiry home loan NZ",
            "reapply pre approval NZ",
        ],
        "cta_heading": "Pre-approval lapsed or about to?",
        "cta_sub": "Send us your updated details. We will get you re-approved — and check whether a different lender now gives you more.",
        "sections": [
            ("How long pre-approvals last", (
                p("New Zealand pre-approvals are time-limited, and the period differs by lender. Commonly they run for around three months, with some shorter and some longer, and some lenders offer a single extension on request without a full reassessment.")
                + p("The reason for the limit is simple: a pre-approval is based on a snapshot of your income, your debts, the lender's policy and the regulatory settings at a point in time. All four can change, so lenders refuse to be bound by a stale assessment.")
                + callout("Diarise the expiry date", "Most people discover their pre-approval has expired at exactly the wrong moment — when they have found a house. Put the expiry date in your calendar with a three-week warning, and talk to your broker before it lapses rather than after.")
            )),
            ("Renewal is usually simple", (
                p("If nothing material has changed, renewal is generally a light-touch process. Expect to provide refreshed versions of the same documents:")
                + ol([
                    "Recent payslips, usually the most recent two or three.",
                    "Updated bank statements, typically the last three months.",
                    "Confirmation that your employment, income and debts are unchanged.",
                    "An updated statement of your deposit, including any growth since last time.",
                    "A fresh credit check in most cases.",
                ])
                + p("Where your circumstances are genuinely unchanged, this is often turned around quickly. Our " + link("mortgage-document-checklist-nz.html", "document checklist") + " covers what to have ready.")
            )),
            ("Why the number can change", (
                p("This is the part that catches people. Being re-approved is usually easy; being re-approved for the same amount is not guaranteed. Several things may have moved while you were looking:")
                + ul([
                    "<strong>Test rates.</strong> Lenders assess your ability to repay at a stress-test rate above the advertised rate. If test rates have moved, your assessed capacity moves with them — in either direction.",
                    "<strong>Living expense benchmarks.</strong> Lenders periodically update the household expense figures they apply. Higher benchmarks reduce capacity.",
                    "<strong>Regulatory settings.</strong> Loan-to-value and debt-to-income restrictions are set by the Reserve Bank and have been adjusted over time. A change affects what any lender can offer you.",
                    "<strong>Your own position.</strong> A new car loan, a higher credit card limit, a change of job or a new dependant all feed in.",
                    "<strong>Your deposit.</strong> Often the good news — if you have kept saving, you may qualify for more, or move into a better loan-to-value band with better pricing.",
                ])
                + p("So the renewal conversation is worth treating as a fresh assessment rather than a formality, because the answer may genuinely be different.")
            )),
            ("Treat it as an opportunity to shop", (
                p("An expired pre-approval is a natural moment to ask whether your original lender is still the right one. Lender policies diverge over time, appetite shifts, and the bank that gave you the best number six months ago may not now.")
                + p("Because you are being reassessed anyway, comparing costs you nothing extra. We regularly find that a client's renewal is stronger at a different lender — sometimes materially so, particularly where their income has become more complex or where a specific lender has sharpened its appetite in their category.")
                + p("One caution: do not make speculative applications to multiple lenders yourself. Each generates a credit enquiry and a cluster of enquiries looks like distress. Policy comparison should happen before any application goes in.")
            )),
            ("If something has changed for the worse", (
                p("Renewals get harder when circumstances have moved against you — a job change, reduced hours, a new debt, or a missed payment on your record. None of these is necessarily fatal, but they change which lender is the right target.")
                + table(
                    ["Change", "What usually helps"],
                    [
                        ["New job", "Evidence of continuity — same industry, signed agreement, and where possible a payslip or two in the new role."],
                        ["Reduced hours or income", "A reassessment at the lower figure, and possibly a longer loan term or a larger deposit to bridge the gap."],
                        ["New consumer debt", "Clearing or reducing it before reapplying — see our guide to what debt costs your borrowing power."],
                        ["Missed payments", "Time, plus documented evidence the cause was resolved. See our guide on missed payments and applications."],
                    ],
                )
                + p("The worst approach is to reapply blind and collect a decline. Work out the target first.")
            )),
            ("Practical timing", (
                p("Start the renewal three to four weeks before expiry. That gives time to gather documents, deal with anything unexpected, and compare lenders without pressure. It also means you are never in the position of finding a house with no live approval.")
                + p("And remember that even a current pre-approval is not approval for a specific property — you will still need a finance condition in your offer. See " + link("finance-condition-sale-purchase-nz.html", "how the finance condition works") + ".")
                + p("Send us your updated position and we will handle the renewal, and tell you whether staying with your current lender is still your best option.")
            )),
        ],
        "faqs": [
            ("How long does a mortgage pre-approval last in New Zealand?",
             "It varies by lender. Around three months is common, with some shorter and some longer, and some lenders will grant a single extension on request without a full reassessment. The limit exists because a pre-approval reflects your circumstances, the lender's policy and the regulatory settings at one point in time."),
            ("Can I be re-approved for less than last time?",
             "Yes, and it happens. Lender stress-test rates, household expense benchmarks and Reserve Bank loan-to-value and debt-to-income settings all change over time, and so may your own debts and income. Conversely, if you have kept saving, a larger deposit may mean you qualify for more or move into a better pricing band."),
            ("Should I renew with the same lender or shop around?",
             "It is worth comparing, since you are being reassessed anyway. Lender policies and appetite diverge over time, so the bank that offered the best number originally may not now. Avoid making speculative applications to several lenders yourself though — each creates a credit enquiry, and a cluster of them makes approval harder."),
            ("When should I start the renewal process?",
             "Three to four weeks before expiry. That leaves time to gather updated documents, deal with anything unexpected and compare lenders without pressure, and it means you are never in the position of finding a property with no live pre-approval in place."),
        ],
        "faq_heading": "Expired pre-approvals: common questions",
        "related": REL_CORE + [
            ("mortgage-pre-approval-timeline.html", "Pre-Approval Timeline",
             "The full NZ sequence."),
            ("finance-condition-sale-purchase-nz.html", "Finance Conditions",
             "Why you still need one."),
            ("missed-payments-mortgage-rejection.html", "Missed Payments",
             "Repairing your record."),
        ],
    },

    {
        "slug": "buying-off-the-plans-finance-nz",
        "title": "Buying Off the Plans in NZ: The Finance Risks",
        "h1": "Buying Off the Plans: Sunset Clauses and Finance Risk",
        "section_label": "New Builds",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["Off the plans", "New builds", "Sunset clauses"],
        "intro_pull": "You sign today and settle in two years. Everything that matters about your finance — your income, the rules, and the property's value — can change in between.",
        "description": "The finance risks of buying off the plans in NZ: sunset clauses, valuation shortfalls at completion, and why you cannot get a binding approval years ahead.",
        "keywords": [
            "buying off the plans NZ finance",
            "off the plans mortgage NZ",
            "sunset clause NZ property",
            "valuation shortfall off the plans NZ",
            "new build LVR exemption NZ",
            "off plan apartment finance NZ",
        ],
        "cta_heading": "Considering an off-the-plans purchase?",
        "cta_sub": "Send us the contract and the completion timeline. We will walk you through the finance risk before you pay a deposit.",
        "sections": [
            ("The structural problem with off-the-plans finance", (
                p("When you buy an existing house, you arrange finance and settle within weeks. When you buy off the plans, you sign a contract now and settle when the building is finished — which might be eighteen months or three years away.")
                + p("No lender will give you a binding, unconditional approval that far ahead, because it cannot know what your income, the lending rules or the property's value will be at completion. You can usually get an indication, and some lenders will look at it closer to completion, but the gap between signing and settling is a risk you carry.")
                + callout("The key question to ask yourself", "If my income dropped, lending rules tightened, and the valuation came in below the price I agreed — could I still settle? If the honest answer is no, the purchase is riskier than it looks, however good the development is.")
            )),
            ("Valuation shortfall: the main financial risk", (
                p("Lenders lend against the <em>lower</em> of the purchase price or the valuation at the time of settlement. If the market has softened between signing and completion, the valuation can come in below the price you contracted to pay.")
                + p("You are still contractually obliged to pay the agreed price. The lender will only lend against the lower figure. The difference is a shortfall you must cover in cash, on top of your planned deposit.")
                + p("A worked illustration of the mechanism — using round numbers, not a prediction:")
                + ul([
                    "You contract to buy at $800,000 with a planned 20% deposit of $160,000, expecting a $640,000 loan.",
                    "At completion the property values at $750,000.",
                    "The lender will lend 80% of $750,000, which is $600,000.",
                    "You still owe $800,000 under the contract, so you now need $200,000 rather than $160,000 — an extra $40,000 in cash.",
                ])
                + p("This is the single most common way off-the-plans purchases go wrong, and it has nothing to do with the buyer's conduct.")
            )),
            ("Sunset clauses work in two directions", (
                p("A sunset clause sets a date by which the development must be completed. If it is not, the contract can be cancelled. Buyers often assume this protects them — and it does, partly, by giving an exit if the project stalls indefinitely.")
                + p("But the clause may also allow the <em>developer</em> to cancel. In a rising market, a developer who can cancel and resell at today's higher prices has an incentive to do so. Your deposit comes back, but the gain you expected goes to someone else, and you are back in a more expensive market.")
                + p("What to have your lawyer check:")
                + ol([
                    "Who can cancel under the sunset clause — you, the developer, or both.",
                    "The sunset date, and how it can be extended, and by whom.",
                    "What happens to your deposit and whether any interest accrues.",
                    "Whether the developer can vary the plans, specifications or unit size, and within what tolerance.",
                    "Whether your deposit is held in a solicitor's trust account, and what security you have for it.",
                ])
            )),
            ("The new build advantages are real", (
                p("None of this means off the plans is a bad idea. There are genuine benefits worth weighing:")
                + ul([
                    "<strong>Loan-to-value treatment.</strong> New builds have historically been treated more favourably under Reserve Bank LVR restrictions than existing properties, which can mean a smaller deposit. The settings change over time, so confirm the current position rather than relying on what applied last year.",
                    "<strong>A long run to save.</strong> The period between signing and settlement is time to build your deposit, which can offset some of the valuation risk.",
                    "<strong>A new home.</strong> Builder's warranties, current building standards, Healthy Homes compliance from the outset, and generally lower maintenance.",
                    "<strong>Price certainty on the build.</strong> You have locked a price, which in a rising market works in your favour.",
                ])
            )),
            ("How to reduce the risk", (
                ol([
                    "<strong>Keep saving the whole way through.</strong> A larger deposit at settlement is the most direct protection against a valuation shortfall.",
                    "<strong>Have your lawyer review the contract before you pay anything.</strong> Off-the-plans contracts are developer-drafted and vary enormously.",
                    "<strong>Check the developer's track record.</strong> Completed projects, time taken, and whether buyers settled without issue.",
                    "<strong>Get an indicative lending position now and reconfirm as completion approaches.</strong> Not binding, but it tells you whether you are in range.",
                    "<strong>Understand the title.</strong> Many off-the-plans purchases are unit titles with body corporate obligations — see " + link("cross-lease-unit-title-freehold-nz.html", "our guide to NZ title types") + ".",
                    "<strong>Confirm the CCC position.</strong> Settlement normally requires code compliance certification, and delays there delay your settlement.",
                ])
            )),
            ("How we approach these", (
                p("We set expectations honestly at the start and stay with the file through to completion. That means giving you a realistic view of where you would stand at settlement under a weaker market, flagging what in the contract creates finance risk, and reconnecting as completion approaches to get the actual approval in place.")
                + p("Send us the contract and the expected completion date. We will tell you what the finance path looks like and what to keep saving.")
            )),
        ],
        "faqs": [
            ("Can I get a mortgage approved before an off-the-plans build is finished?",
             "Not a binding unconditional approval, generally. Lenders cannot commit years ahead because your income, the lending rules and the property's value at completion are all unknown. You can usually obtain an indicative position, and the formal application is made as completion approaches, which means you carry risk in the interim."),
            ("What happens if the valuation comes in below the price I agreed?",
             "You are still contractually obliged to pay the agreed price, but the lender will only lend against the lower of the price and the valuation. The difference becomes a cash shortfall you must cover on top of your planned deposit. This is the most common way off-the-plans purchases run into trouble, which is why continuing to save through the build period matters."),
            ("Can a developer cancel my contract under a sunset clause?",
             "Possibly — it depends on the wording. Some sunset clauses allow either party to cancel if the development is not completed by the sunset date, which means a developer in a rising market may have an incentive to cancel and resell. Have your lawyer check who can cancel, how the date can be extended and by whom, before you pay a deposit."),
            ("Do new builds still get better LVR treatment in NZ?",
             "New builds have historically been treated more favourably than existing properties under Reserve Bank loan-to-value restrictions, which can mean a smaller deposit is required. These settings are adjusted from time to time, so confirm the current position with your adviser rather than relying on what applied previously."),
        ],
        "faq_heading": "Buying off the plans: common questions",
        "related": REL_CORE + [
            ("../services/construction-loan.html", "Construction Loans",
             "Progressive drawdown lending."),
            ("cross-lease-unit-title-freehold-nz.html", "NZ Property Titles",
             "Unit titles and body corporates."),
            ("build-vs-buy-nz.html", "Build vs Buy",
             "Which is cheaper right now?"),
        ],
    },

    {
        "slug": "lim-builders-report-finance-nz",
        "title": "When a LIM or Builder's Report Kills Your Finance",
        "h1": "When a LIM or Builder's Report Kills Your Finance",
        "section_label": "Buying Process",
        "region": None,
        "lead_service": "Home Loan",
        "about": ["LIM reports", "Builder's reports", "Unconsented work"],
        "intro_pull": "Unconsented work is the quiet deal-killer. The bank is not lending on the house you are buying — it is lending on the house the council has a record of.",
        "description": "How LIM reports and builder's reports affect NZ mortgage approvals: unconsented work, weathertightness, hazards, and what lenders do about each.",
        "keywords": [
            "LIM report mortgage NZ",
            "unconsented work mortgage NZ",
            "builders report finance declined NZ",
            "no code compliance certificate mortgage NZ",
            "LIM report what to look for NZ",
            "weathertightness mortgage NZ",
        ],
        "cta_heading": "Something concerning in a LIM or builder's report?",
        "cta_sub": "Send us the report. We will tell you whether it is a lender problem, a price negotiation, or a reason to walk away.",
        "sections": [
            ("The two reports and what each does", (
                p("A <strong>LIM</strong> — Land Information Memorandum — is issued by the territorial authority and sets out what the council knows about the property: building consents and code compliance certificates, hazards, drainage, zoning, rates, and any notices or requisitions. It is a record of the official position.")
                + p("A <strong>builder's report</strong> is a private inspection of the physical condition of the building by a qualified inspector. It tells you what is actually there and what state it is in.")
                + p("You want both, and you want them before your finance condition expires, because each can surface issues that affect lending. Order the LIM as soon as your offer is accepted — councils have statutory timeframes but they are not instant.")
            )),
            ("Unconsented work: the most common finance killer", (
                p("This is the issue we see stop more deals than any other. Building work that required consent but never got one, or got a consent that was never signed off with a code compliance certificate, creates a gap between the house and its official record.")
                + p("Why lenders care:")
                + ul([
                    "<strong>Valuation.</strong> A valuer may exclude unconsented floor area from the valuation, or discount it. A house marketed as four bedrooms may be valued as three.",
                    "<strong>Insurance.</strong> Insurers may exclude unconsented structures from cover, and a lender needs the security insured.",
                    "<strong>Council enforcement risk.</strong> A council can require unconsented work to be consented retrospectively, altered, or removed. That liability transfers to you as the new owner.",
                    "<strong>Resale.</strong> The lender is thinking about selling the property if it has to, and unconsented work narrows the future buyer pool for the same reasons it is narrowing yours.",
                ])
                + callout("The usual culprits", "Decks and pergolas, carports and garages, internal walls moved or added, bathrooms and kitchens relocated, garage conversions into living space, sleepouts and sheds with power or plumbing, and woodburners installed without consent. Older properties very commonly have at least one.")
            )),
            ("What can be done about unconsented work", (
                table(
                    ["Route", "What it involves", "Practical note"],
                    [
                        ["Certificate of Acceptance", "Apply to the council to accept work done without consent.", "Not available in all cases, costs money, and the council may require remedial work or inspection openings."],
                        ["Retrospective consent", "Consent the work properly where it is still possible.", "Can be slow and may require the work to be brought up to current code."],
                        ["Vendor fixes before settlement", "Negotiate that the vendor resolves it as a condition.", "Cleanest for you, but adds time and the vendor must agree."],
                        ["Price adjustment", "Buy with the issue, at a reduced price reflecting the cost and risk.", "Works only if your lender will still lend — check first, not after."],
                        ["Remove the work", "Take out the unconsented structure.", "Sometimes the cheapest route for a minor structure."],
                        ["Walk away", "Cancel under the LIM or builder's report condition.", "Why you include those conditions in the first place."],
                    ],
                )
                + p("Which routes are open depends on what the work is and how significant it is. A small unconsented deck is a different conversation from a converted garage being used as a bedroom.")
            )),
            ("Weathertightness and monolithic cladding", (
                p("A builder's report flagging weathertightness concerns, particularly on monolithic-clad homes from the mid-1990s to mid-2000s, is a significant lending issue. Lenders and insurers are both cautious, and some lenders will decline these outright.")
                + p("If a report raises weathertightness, the usual next step is a specialist weathertightness assessment with invasive moisture testing rather than a visual inspection. That costs more and takes longer, but a visual report alone will rarely satisfy a cautious lender. Remediation costs on these properties can be very large — see our " + link("../case-studies/leaky-home-remediation-finance.html", "remediation finance case study") + ".")
            )),
            ("What else on a LIM affects lending", (
                ul([
                    "<strong>Natural hazards.</strong> Flood, erosion, landslip and inundation. These feed into insurability, which is usually the binding constraint — see " + link("flood-zone-insurance-mortgage-decline-nz.html", "flood risk and insurance") + ".",
                    "<strong>Contaminated land (HAIL).</strong> Former horticultural, industrial or spray shed use. Affects lending, insurance and future development.",
                    "<strong>Drainage.</strong> Private drains crossing other properties, shared drains, or stormwater overland flow paths across the site.",
                    "<strong>Notices and requisitions.</strong> Outstanding council requirements attach to the property, not the previous owner.",
                    "<strong>Zoning and designations.</strong> A designation for a future road or public work materially affects value.",
                    "<strong>Rates arrears.</strong> Usually resolved at settlement, but worth knowing about.",
                ])
            )),
            ("How to handle it without losing the deal", (
                ol([
                    "Make your offer conditional on a satisfactory LIM and builder's report, with enough working days to get both — see " + link("finance-condition-sale-purchase-nz.html", "how long conditions really need") + ".",
                    "Order the LIM the day your offer is accepted.",
                    "Send anything concerning to your broker immediately, not at the end of the condition period. Lender appetite on these issues varies, and knowing early gives you options.",
                    "Get the remediation priced before you negotiate. A specific figure is a much stronger negotiating position than a general worry.",
                    "Use your lawyer. Consent and enforcement questions are legal questions.",
                ])
                + p("Most LIM and builder's report issues are negotiable rather than fatal. The deals that fail are usually the ones where the problem surfaced too late to do anything about it. Send us the report as soon as you have it.")
            )),
        ],
        "faqs": [
            ("Will a bank lend on a house with unconsented work?",
             "Sometimes, depending on what the work is and how significant it is. Lender appetite varies considerably. The complications are that a valuer may exclude unconsented floor area from the valuation, insurers may exclude the structure from cover, and the council can require the work to be consented, altered or removed — with that liability passing to you as the new owner."),
            ("What is a Certificate of Acceptance?",
             "It is a council mechanism for accepting building work that was done without the required consent. It is not available in every situation, it costs money, and the council may require remedial work or the opening up of completed areas for inspection. It is one of several routes for resolving unconsented work, alongside retrospective consent, removal or a price adjustment."),
            ("Why do lenders worry about monolithic cladding?",
             "Monolithic-clad homes built from roughly the mid-1990s to the mid-2000s are associated with weathertightness failures, and remediation costs can be very large. Both lenders and insurers are cautious, and some lenders decline these properties. Where a builder's report raises weathertightness, a specialist assessment with invasive moisture testing is usually needed rather than a visual inspection."),
            ("When should I order a LIM report?",
             "As soon as your offer is accepted. Councils have statutory timeframes for issuing a LIM but it is not immediate, and you need time to read it, get any concerning items priced or assessed, and discuss them with your broker and lawyer before your conditions expire. Make sure your offer allows enough working days for this."),
        ],
        "faq_heading": "LIM and builder's reports: common questions",
        "related": REL_CORE + [
            ("finance-condition-sale-purchase-nz.html", "Finance Conditions",
             "Allowing enough time."),
            ("flood-zone-insurance-mortgage-decline-nz.html", "Flood Zones & Insurance",
             "When hazards stop a loan."),
            ("../case-studies/leaky-home-remediation-finance.html", "Remediation Finance",
             "Funding weathertightness repair."),
        ],
    },

    {
        "slug": "buying-house-from-family-below-market-value-nz",
        "title": "Buying a House From Family Below Market Value NZ",
        "h1": "Buying a Home From Family Below Market Value",
        "section_label": "Buying Process",
        "region": None,
        "lead_service": "First Home Buyer Mortgage",
        "about": ["Favourable purchase", "Gifted equity", "Family property transfer"],
        "intro_pull": "If your parents sell you the family home below its value, that discount can work as your deposit. The structure has to be right — and everyone needs their own lawyer.",
        "description": "How a favourable purchase works in NZ: buying from family below market value, using the discount as deposit, and the legal and tax issues to settle first.",
        "keywords": [
            "buying house from family below market value NZ",
            "favourable purchase mortgage NZ",
            "gifted equity NZ mortgage",
            "buying parents house NZ",
            "family property transfer mortgage NZ",
            "gifting certificate NZ mortgage",
        ],
        "cta_heading": "Buying from a family member?",
        "cta_sub": "Tell us the valuation and the agreed price. We will show you how lenders treat the gap — and what documentation they will want.",
        "sections": [
            ("How a favourable purchase works", (
                p("A favourable purchase — sometimes called gifted equity — is where a family member sells you a property for less than its market value, and the discount is treated as your contribution to the deal.")
                + p("The mechanism rests on a distinction that catches people out. Lenders normally lend against the <em>lower</em> of purchase price or valuation. But in a genuine favourable purchase between related parties, many lenders will assess the loan-to-value ratio against the <strong>registered valuation</strong> rather than the discounted price — which means the discount functions as equity you did not have to save.")
                + p("A worked illustration, using round numbers:")
                + ul([
                    "Your parents' home is valued at $700,000 by a registered valuer.",
                    "They agree to sell it to you for $560,000.",
                    "The $140,000 difference is 20% of the valuation.",
                    "Where a lender accepts this, you may be able to borrow the full $560,000 purchase price while still sitting at 80% of the property's value.",
                ])
                + callout("Not every lender does this", "Treatment of favourable purchases varies, and some lenders will still use the lower purchase price, or cap how much of the deposit can come from gifted equity. Establish lender policy before you agree a price with your family, because the answer changes what structure works.")
            )),
            ("What lenders will require", (
                ol([
                    "<strong>A registered valuation.</strong> Not a rates valuation, not an appraisal from an agent — a valuation from a registered valuer, usually instructed by the lender.",
                    "<strong>A gifting certificate or deed of gift.</strong> A signed document from the vendor confirming the discount is a genuine gift, with no expectation of repayment and no security taken over the property.",
                    "<strong>Independent legal advice for both sides.</strong> You and your family members need separate lawyers. This is not a formality — lenders require it and it protects everyone.",
                    "<strong>A proper sale and purchase agreement.</strong> The transaction must be documented as a real sale at the agreed price, not an informal arrangement.",
                    "<strong>Confirmation the vendor is not retaining an interest.</strong> If your parents want to keep a stake, or want the money back later, that is a different transaction entirely and changes the lending.",
                ])
                + p("The word 'genuine' is doing a lot of work here. A gift that is really a loan — with an expectation of repayment — is a liability, and lenders will treat it as one if they discover it.")
            )),
            ("The questions families need to answer first", (
                p("The lending is usually the easy part. The difficult conversations are about fairness and consequences, and they are much better had before anything is signed:")
                + ul([
                    "<strong>Other siblings.</strong> Is the discount an advance on inheritance, and will it be accounted for in the estate? Write down what has been agreed.",
                    "<strong>The vendor's own position.</strong> Do your parents need the full value to fund retirement or care? Selling below value reduces the capital available to them, permanently.",
                    "<strong>Residential care subsidy.</strong> Gifting can affect eligibility for residential care subsidies, where asset testing applies and historic gifting is examined. Specialist advice is essential here.",
                    "<strong>Relationship property.</strong> A gift to you may become relationship property depending on how it is handled. If you have a partner, consider a contracting out agreement.",
                    "<strong>What if things go wrong.</strong> If you later cannot pay the mortgage, the house your family gifted equity in is the security. Everyone should understand that.",
                ])
                + p("These are lawyer and accountant questions, and they are worth paying for properly.")
            )),
            ("Tax and the bright-line test", (
                p("New Zealand has no general gift duty, so the gift itself is not usually taxed. But there are other tax considerations:")
                + ul([
                    "<strong>Bright-line test.</strong> If the property is not the vendor's main home — a rental, a holiday home, or a property held in a trust or company — selling it may trigger bright-line obligations even in a family transfer at a discount. See our " + link("bright-line-test-nz-2026.html", "bright-line test guide") + ".",
                    "<strong>Deemed market value.</strong> For tax purposes, transactions between associated persons can be treated as occurring at market value regardless of the price actually paid.",
                    "<strong>Trusts and companies.</strong> If the property is held in a structure, the rules are more complex and trustee duties apply.",
                ])
                + p("Get accounting advice before agreeing a price. A transfer that looks straightforward can have a tax consequence that outweighs the benefit of the discount.")
            )),
            ("Alternatives worth considering", (
                table(
                    ["Structure", "How it works", "Main consideration"],
                    [
                        ["Favourable purchase", "Sell below value; the discount acts as deposit.", "Vendor permanently gives up that capital."],
                        ["Cash gift for deposit", "Family gifts cash; you buy at market value.", "Needs a gifting certificate; vendor must have liquid funds."],
                        ["Family guarantee", "Family offers security over their property rather than cash.", "Real risk to the guarantor's home — independent advice essential."],
                        ["Family loan", "Family lends you the deposit.", "A liability, so it reduces your serviceability. Must be disclosed."],
                        ["Buy at market value with a private arrangement", "Full price paid, family helps separately.", "Must be transparent to the lender — undisclosed side arrangements are a serious problem."],
                    ],
                )
                + p("Our " + link("../case-studies/family-guarantee-first-home.html", "family guarantee case study") + " and " + link("../case-studies/gifted-deposit-no-savings.html", "gifted deposit case study") + " show two of these in practice.")
            )),
            ("How we approach family transactions", (
                p("We start with lender policy, because it determines what structure is worth pursuing. Then we make sure the documentation is right — valuation, gifting certificate, separate legal advice — so the file does not stall at the last minute over a missing signature.")
                + p("Most importantly, we are straight with everyone involved about what the arrangement means. These deals go wrong when expectations were never written down. Send us the valuation and what your family has in mind, and we will tell you what is achievable and what to formalise.")
            )),
        ],
        "faqs": [
            ("Can I use a family discount as my deposit in NZ?",
             "Often yes. Where a family member sells you a property below market value, many lenders will assess the loan-to-value ratio against the registered valuation rather than the discounted purchase price, which means the discount functions as equity. Lender treatment varies though, and some will use the lower price or cap how much deposit can come from gifted equity."),
            ("What documents does a lender need for a favourable purchase?",
             "Typically a registered valuation (not a rates valuation or agent appraisal), a signed gifting certificate or deed of gift confirming the discount is a genuine gift with no expectation of repayment, evidence of independent legal advice for both parties, and a properly documented sale and purchase agreement at the agreed price."),
            ("Is there gift duty on buying a family home below value in NZ?",
             "New Zealand does not have general gift duty, so the gift itself is not usually taxed. However other tax issues can arise — the bright-line test may apply if the property was not the vendor's main home, and transactions between associated persons can be treated as occurring at market value for tax purposes. Get accounting advice before agreeing a price."),
            ("Does gifting affect a residential care subsidy?",
             "It can. Eligibility for residential care subsidies involves asset testing, and historic gifting is examined as part of that assessment. If the family members selling to you may need residential care in future, this is an important consideration and warrants specialist advice before any transfer is made."),
        ],
        "faq_heading": "Buying from family: common questions",
        "related": REL_FHB + [
            ("../case-studies/gifted-deposit-no-savings.html", "Gifted Deposit Case Study",
             "Buying with family help."),
            ("../case-studies/family-guarantee-first-home.html", "Family Guarantee Case Study",
             "Using family security."),
            ("bright-line-test-nz-2026.html", "Bright-Line Test 2026",
             "Tax on property transfers."),
        ],
    },
]


# ---------------------------------------------------------------------------
# Supplementary sections, appended per slug. Split out so each post's core
# argument stays readable above while depth lives here. Targets the
# 1,500-2,000 word range in context/seo-guidelines.md.
# ---------------------------------------------------------------------------

EXTRA_SECTIONS = {

    "leasehold-apartment-mortgage-auckland": [
        ("What ground rent actually does to your budget", (
            p("Ground rent is the payment you make to the landowner for the right to occupy. It is not a mortgage payment, it does not reduce over time, and it does not build you any equity. For budgeting purposes it behaves like a rates bill that can be reset upward periodically.")
            + p("Two features of the lease determine how risky it is:")
            + ul([
                "<strong>The review period.</strong> How often the ground rent can be reset. Longer gaps between reviews mean more certainty for you, but also a larger adjustment when the review arrives.",
                "<strong>The review basis.</strong> Some leases reset to a percentage of current land value, which in a market where land has appreciated significantly can produce a very large increase. Others move by a fixed formula or an index, which is far more predictable.",
            ])
            + p("Lenders assess ground rent as a committed outgoing in your serviceability, the same way they treat body corporate levies. So a high ground rent reduces your borrowing capacity on top of narrowing your lender options. If a review is due within a few years of your purchase, ask your lawyer what the likely new figure is — and budget for it rather than hoping.")
        )),
        ("A realistic worked comparison", (
            p("Consider two central Auckland apartments, both asking around the same weekly cost to occupy, using round illustrative numbers rather than current market figures:")
            + table(
                ["", "Freehold unit title", "Leasehold unit title"],
                [
                    ["Purchase price", "$650,000", "$420,000"],
                    ["Deposit at 20%", "$130,000", "$84,000 (if the lender accepts 20%)"],
                    ["Body corporate levies", "Payable", "Payable"],
                    ["Ground rent", "None", "Payable, and subject to review"],
                    ["Equity position in 15 years", "Mortgage paid down, land value retained", "Mortgage paid down, lease 15 years shorter"],
                    ["Future buyer's finance options", "Broad", "Narrower, and narrowing further"],
                ],
            )
            + p("The leasehold option needs less cash up front, which is genuinely useful if deposit is your constraint. What you are trading is long-term optionality: a shorter lease at resale, a smaller buyer pool, and an outgoing that can be reset upward. Neither column is automatically right — but the decision should be made with both in front of you, not on the purchase price alone.")
        )),
        ("Questions to put to your lawyer in writing", (
            ol([
                "What is the lease expiry date, and is there any right of renewal?",
                "When is the next ground rent review, and on what basis is the new rent calculated?",
                "What has the ground rent done at the last two reviews?",
                "Are there any arrears of ground rent or levies attaching to the unit?",
                "What happens at the end of the lease term — who owns the improvements?",
                "Does the lease restrict subletting, renovation or short-stay use?",
                "For a unit title, what does the long-term maintenance plan say, and is the reserve fund adequate?",
            ])
            + p("Get the answers in writing before your finance condition expires. Our guide to " + link("finance-condition-sale-purchase-nz.html", "how long a finance condition really needs") + " explains why apartment and leasehold purchases usually need more working days than a standard house.")
        )),
    ],

    "cross-lease-unit-title-freehold-nz": [
        ("How to read a record of title", (
            p("You can order a record of title for any New Zealand property through LINZ or via your lawyer, and it is the authoritative statement of what you are buying. The key things to find:")
            + ul([
                "<strong>The estate.</strong> 'Fee simple' means freehold. 'Leasehold' means you hold a lease. A cross-lease will usually show a fee simple share held with others, plus leasehold interests.",
                "<strong>The legal description.</strong> Lot and DP numbers, which tie back to the survey plan.",
                "<strong>Registered interests.</strong> Easements, covenants, rights of way, building line restrictions and any mortgages or caveats.",
                "<strong>Ownership shares.</strong> On a cross-lease, the undivided share you hold — a one-half or one-third share, for example.",
            ])
            + p("Covenants matter more than buyers expect. A land covenant can restrict building materials, fence heights, how many dwellings can be built, or whether you can run a business from the property. They bind you as the new owner, and they are not always obvious from the listing.")
        )),
        ("The renovation question, by title type", (
            p("If you intend to alter the property, your title type determines who else has a say:")
            + table(
                ["Title", "Who you need agreement from", "Practical effect"],
                [
                    ["Freehold", "Council consent only.", "Simplest. Subject to the district plan and any covenants."],
                    ["Cross-lease", "Council, plus the other owners on the title for anything affecting the flats plan or common area.", "Any change to your building's footprint likely needs a new flats plan and every owner's signature."],
                    ["Unit title", "Council, plus the body corporate for work affecting common property or the building exterior.", "Internal non-structural work is usually straightforward; anything external needs body corporate approval."],
                    ["Leasehold", "Council, the body corporate if applicable, and usually the landowner under the lease.", "Most restricted. Check the lease for alteration clauses."],
                ],
            )
            + p("This is why cross-lease owners sometimes find they cannot add a deck without a neighbour's co-operation — and why an existing unconsented deck creates the defect described earlier. If renovation is part of your plan, confirm the path before you buy.")
        )),
        ("Converting a cross-lease to freehold", (
            p("It is sometimes possible to convert a cross-lease into separate fee simple titles, which removes the shared-ownership complications permanently and generally improves value. The process involves surveying, a subdivision consent from the council, and the agreement of all owners on the title.")
            + p("It is not cheap and it is not quick, and the requirement for unanimous agreement is the usual obstacle — one unwilling or uncontactable owner stops it. But where owners are co-operative it can be worth investigating, particularly if several of you would benefit. Talk to a surveyor and your lawyer about feasibility for your specific title before budgeting for it.")
        )),
    ],

    "earthquake-prone-building-mortgage-wellington": [
        ("Initial versus detailed engineering assessments", (
            p("Not all seismic assessments are equivalent, and the difference matters when a deal hinges on the number.")
            + ul([
                "<strong>Initial Seismic Assessment (ISA).</strong> A relatively quick, largely desk-based review using available drawings and a visual inspection. Cheaper and faster, but indicative — it produces a broad estimate rather than a precise figure.",
                "<strong>Detailed Seismic Assessment (DSA).</strong> A thorough engineering analysis of the specific structure, often involving intrusive investigation to confirm construction details. More expensive and slower, but far more reliable.",
            ])
            + p("It is common for a DSA to produce a materially different rating from an earlier ISA, in either direction. If a building has only an ISA and the rating is what is standing between you and finance, commissioning a DSA may be worth the cost — though in a unit title building that is usually a body corporate decision rather than yours alone.")
            + p("Always ask which type of assessment produced the figure you have been given, who prepared it, and when. A ten-year-old ISA is weak evidence for a lender or an insurer.")
        )),
        ("What strengthening work actually involves", (
            p("If you are buying into a building with strengthening ahead of it, it helps to know what the project typically entails and why the cost varies so much. Common approaches include adding structural steel or concrete shear walls, tying floors and roofs more securely to walls, securing unreinforced masonry parapets and chimneys, and strengthening connections throughout the structure.")
            + p("The cost drivers are the building's existing structure, its height, how much of it must be vacated during works, and heritage constraints. A heritage-listed façade can add substantially, because the strengthening has to be achieved without altering protected features.")
            + p("For a purchaser the practical questions are: has the body corporate resolved to do the work, has it been priced, has the money been collected or borrowed, and what is the timeline. A building where all four have clear answers is a far safer purchase than one where the engineering report exists but nothing has been decided.")
        )),
        ("Insurance: what to ask and when", (
            p("Because insurance is usually the binding constraint, treat it as the first step rather than the last. What to do, in order:")
            + ol([
                "Ask the vendor or body corporate who currently insures the building and whether cover is full replacement or something less.",
                "Ask whether the premium or excess has changed materially in recent renewals, and whether any insurer has declined or imposed conditions.",
                "Approach a broker who deals with Wellington commercial and apartment risk — they will know which insurers are writing business in that building type.",
                "Get the position in writing before you confirm your finance condition.",
            ])
            + p("In a unit title building the insurance is generally arranged by the body corporate for the whole structure, so your individual position depends on a decision you do not control. That is worth understanding before you commit — if the body corporate loses cover, your mortgage is affected regardless of your own conduct.")
        )),
    ],

    "tc2-tc3-land-christchurch-mortgage": [
        ("What a cash-settled claim means for you as buyer", (
            p("A significant number of Canterbury properties were cash-settled rather than repaired under a managed programme. The owner received a sum of money assessed as the cost of repair, and then decided what to do with it. Some completed the work properly. Some did part of it. Some did none.")
            + p("If you are buying one of these, you need to establish which. The money has gone to the previous owner either way, and if the damage remains, the cost of remediation falls to you — and the entitlement to claim it again generally does not transfer.")
            + p("What to ask for:")
            + ul([
                "The settlement documentation showing what the payment covered and what scope of work it was assessed against.",
                "Evidence of what was actually done — invoices, builder details, consents and code compliance certificates for any structural work.",
                "A builder's report specifically briefed to check the areas covered by the claim.",
                "Confirmation from an insurer that they will provide full cover on the property in its current condition.",
            ])
            + p("A property with a clean, documented repair trail is a straightforward purchase. One with a cash settlement and no evidence of work is a renovation project with an unknown budget — price it accordingly, and read our guide to " + link("lim-builders-report-finance-nz.html", "LIM and builder's reports") + ".")
        )),
        ("Foundation types you will encounter", (
            p("Post-earthquake rebuilds and repairs in Canterbury used a range of foundation solutions, and valuers, insurers and lenders are all more comfortable with some than others. You will come across standard concrete slabs, timber pile floors, and various engineered options designed for TC2 and TC3 land including reinforced concrete rafts and waffle slabs.")
            + p("You do not need to be an engineer, but you should know what is under the house and whether it was designed and signed off for the land's technical category. The documentation trail — geotechnical report, engineering design, building consent and code compliance certificate — is what gives a lender comfort. Where that trail is complete, the foundation type itself is rarely the issue.")
            + p("Where it becomes an issue is work done without proper design or sign-off, which brings you back to the unconsented work problem and all the valuation and insurance consequences that come with it.")
        )),
        ("Buying bare TC3 land to build", (
            p("If you are buying a vacant TC3 section, the sequence matters enormously because your build cost is not knowable until the geotechnical investigation is done.")
            + ol([
                "Make your offer conditional on a satisfactory geotechnical investigation, with enough working days to get it done.",
                "Commission the geotech report and have it reviewed by your designer or engineer.",
                "Get the foundation design priced before you sign a build contract.",
                "Only then finalise your construction lending, which will be assessed against the fixed-price contract.",
            ])
            + p("Buyers who sign a build contract before the geotech work is complete sometimes find the foundation requirement adds a substantial sum they had not budgeted. Because construction lending is assessed on the contract price and your ability to service the completed loan, a large unplanned increase can leave you unable to proceed — having already committed to the land.")
        )),
    ],

    "flood-zone-insurance-mortgage-decline-nz": [
        ("What an insurance decline actually looks like", (
            p("Insurers rarely say 'no'. More often they offer terms that amount to the same thing from a lender's point of view:")
            + ul([
                "<strong>A flood exclusion.</strong> Cover for fire, theft and everything else, but not for the peril the property is actually exposed to. Lenders generally will not accept this where flood is the known risk.",
                "<strong>A very high excess.</strong> Cover exists, but with an excess so large that a realistic flood event is effectively uninsured.",
                "<strong>A sub-limit.</strong> Cover capped at a figure below full replacement, which does not satisfy a standard mortgage condition.",
                "<strong>Referral and delay.</strong> The risk is referred to an underwriter and no answer arrives before your finance condition expires.",
            ])
            + p("That last one is the quiet killer. A deal can fail not because insurance was refused but because the answer did not arrive in time. If a property has any hazard flag, build the insurance enquiry into your timeline from day one and allow extra working days.")
        )),
        ("The questions to ask an insurer", (
            ol([
                "Will you offer full replacement cover at this address?",
                "Is natural disaster and flood cover included, or excluded?",
                "What is the excess, specifically for flood and for natural disaster?",
                "What is the annual premium, and has it changed materially in recent years at this address?",
                "Is the quote subject to inspection, or to information you have not yet seen?",
                "Are you prepared to confirm this in writing for my lender?",
            ])
            + p("That last point matters. A verbal indication from a call centre is not evidence a lender can rely on. You want something written, naming the address, confirming the cover and terms.")
        )),
        ("Thinking about the long term", (
            p("Insurance affordability and availability at a given address is not static. New Zealand insurers continue to refine risk-based pricing, and councils continue to update hazard mapping as modelling improves. A property that insures comfortably today may be more expensive to insure in a decade.")
            + p("That has two implications for a buyer:")
            + ul([
                "<strong>Your own costs.</strong> Premium increases are an ongoing outgoing, and large ones affect your ability to service the loan over time.",
                "<strong>Resale.</strong> Your future buyer will face the same insurance-then-finance chain. If insurability has tightened, your buyer pool shrinks and that affects price.",
            ])
            + p("None of this is a reason to avoid every property with a hazard flag — a great many New Zealand homes have some mapped exposure. It is a reason to price the risk honestly, get the written insurance position before you commit, and factor the real premium rather than an average into your budget. See " + link("hidden-costs-buying-house-nz.html", "the hidden costs of buying a house in NZ") + " for the other outgoings that catch buyers out.")
        )),
    ],
    "lifestyle-block-rural-lending-waikato": [
        ("Water and wastewater: what lenders and valuers check", (
            p("On a reticulated suburban section nobody asks about water. On a lifestyle block it is one of the first questions, because supply and disposal affect whether the property is habitable, insurable and valuable.")
            + p("<strong>Water supply.</strong> Most lifestyle blocks rely on roof-collected rainwater into tanks, a bore, a stream take under a resource consent, or a shared rural scheme. A valuer will note the source and its adequacy. Things that cause problems: tank capacity too small for the household, a bore with no pump test or water quality analysis, or a take relying on a consent that is expiring or not transferable.")
            + p("<strong>Wastewater.</strong> Septic tanks and on-site treatment systems need to be consented and functioning. An unconsented system, or one discharging improperly, is a council compliance issue that transfers to you. Ask for the consent, any maintenance records, and whether the system has been inspected recently.")
            + p("Practical steps before you go unconditional: get the water tested, get the septic system inspected, and check the LIM for any consents or abatement notices relating to either. These are cheap checks relative to the cost of discovering a failed system after settlement.")
        )),
        ("Access and the title details that matter", (
            p("Rural titles carry interests that suburban ones usually do not, and each can affect lending:")
            + ul([
                "<strong>Rights of way.</strong> If your access crosses someone else's land, there should be a registered easement. Informal access by long-standing arrangement is a genuine problem — it may not be legally secure, and a lender taking the property as security will care.",
                "<strong>Shared driveway maintenance.</strong> Who pays, and is it documented? An undocumented arrangement among neighbours becomes your dispute.",
                "<strong>Unformed legal road.</strong> Access technically exists in law but no road has been built. This can be a significant issue for both value and insurability.",
                "<strong>Covenants and consent notices.</strong> Rural subdivisions often carry consent notices restricting further subdivision, requiring specific building platforms, or mandating effluent disposal arrangements.",
            ])
            + p("Have your lawyer report specifically on access and consent notices. On rural files this is where unpleasant surprises concentrate, and they are far cheaper to find before settlement than after.")
        )),
        ("Insurance on rural property", (
            p("Rural insurance differs from suburban cover in ways that affect your budget and sometimes your finance. Distance from a fire station and availability of a water supply for firefighting both feed into premiums. Outbuildings need to be specified and valued. If you are running stock or any commercial activity, a standard domestic policy may not cover it.")
            + p("Get a quote for the specific property early, including all the outbuildings you intend to insure, and confirm whether any rural activity you plan is covered. As with any property, a lender will require the security to be insured — and on rural land the premium is often materially higher than buyers expect, which reduces your assessed serviceability.")
        )),
    ],

    "queenstown-holiday-home-short-stay-income-mortgage": [
        ("Running the numbers honestly", (
            p("Short-stay projections usually quote gross nightly rate multiplied by an assumed occupancy. The gap between that figure and what reaches your bank account is wide. The costs that come out of it:")
            + ul([
                "Platform commission and payment processing fees.",
                "Management fees, if you are not managing it yourself — and self-managing from another city is harder than it sounds.",
                "Cleaning and linen between every guest, which on short stays is a frequent cost.",
                "Consumables, replacements and higher wear than a long-term tenancy.",
                "Rates, which may be assessed in a different category for commercial or mixed use.",
                "Insurance, which for short-stay letting is not a standard domestic policy.",
                "Body corporate levies, where applicable.",
                "Periods you block out for your own use, which remove income entirely.",
            ])
            + p("Model your purchase on a conservative occupancy and a realistic net figure. If the deal only works at high occupancy in a strong season, it is a fragile deal — and the lender's assessment will reflect that fragility even if yours does not.")
        )),
        ("Long-term rental as the fallback", (
            p("The most useful stress test for a short-stay purchase is to ask whether it works as a conventional long-term rental. Short-stay demand can be interrupted by regulation, platform changes, a downturn in tourism, or simply more competing listings. Long-term residential demand is far more stable.")
            + p("If the property would service the mortgage as a long-term rental, the short-stay upside is genuine upside and your downside is covered. If it only works as short-stay, you are exposed to a single volatile income stream with a mortgage attached.")
            + p("This is also how a cautious lender thinks. Where a lender will consider rental income at all, long-term residential rent is generally assessed more generously and more predictably than short-stay projections. Our " + link("../calculators/rental-yield-calculator.html", "rental yield calculator") + " lets you model both scenarios.")
        )),
        ("Structuring a holiday home purchase", (
            p("Most holiday home purchases in Queenstown and Wanaka are funded at least partly with equity released from a main home elsewhere. The structure of that matters:")
            + ol([
                "<strong>Keep the lending separate.</strong> A distinct loan or split for the holiday property makes the interest and the position on that asset clear, which matters if the property ever earns income and for any future tax treatment.",
                "<strong>Decide the use up front.</strong> Purely private, purely income-earning, or mixed. The answer changes the lending category, the insurance, and the tax position.",
                "<strong>Think about the exit.</strong> Holiday markets can be less liquid than main centres. Consider how long a sale might take in a weaker market.",
                "<strong>Get tax advice before settlement.</strong> Mixed-use asset rules and potential GST consequences are easier to plan for than to unwind.",
            ])
            + p("See " + link("using-home-equity-investment-property-nz.html", "using home equity to buy another property") + " for how equity release works in practice.")
        )),
    ],

    "healthy-homes-standards-lending-nz": [
        ("A realistic compliance budget", (
            p("Costs vary by property, region and contractor, so treat the following as a structure for your own quoting rather than a price list. What you need priced, item by item:")
            + ol([
                "<strong>Heating.</strong> A fixed heater sized for the living room, using the official heating capacity calculation. Larger or poorly insulated living rooms need larger units, and in some cases more than one appliance is required.",
                "<strong>Ceiling insulation.</strong> Top-up or full replacement to the required standard, depending on what is there.",
                "<strong>Underfloor insulation.</strong> Only where there is accessible suspended flooring. Access limitations change the cost significantly.",
                "<strong>Ground moisture barrier.</strong> Required where there is an enclosed subfloor. Often underestimated because it is labour-intensive in tight crawl spaces.",
                "<strong>Extraction.</strong> Kitchen and bathroom extraction venting externally, to the required capacity.",
                "<strong>Drainage and guttering.</strong> Gutters, downpipes and drains in working order, discharging appropriately.",
                "<strong>Draught stopping.</strong> Blocking gaps and closing off unused open fireplaces.",
            ])
            + p("Get a single quote covering all of it rather than pricing items piecemeal, and ask the assessor to confirm the scope in writing against each of the five standards. That document is what you take to your broker.")
        )),
        ("Where compliance issues overlap with lending issues", (
            p("The standards are a tenancy obligation, but the physical problems they address often signal things a lender cares about more directly. A property failing the moisture and drainage standard may have:")
            + ul([
                "Poor subfloor ventilation leading to rot in bearers and joists.",
                "Drainage discharging against foundations, causing ongoing moisture ingress.",
                "Gutters that have been overflowing long enough to damage cladding or framing.",
            ])
            + p("These are valuation and sometimes insurability matters, not just compliance ones. So when an assessment flags moisture or drainage, it is worth getting a builder to look at the underlying cause rather than just quoting the minimum compliance fix. A cheap remedy that leaves the cause in place will cost more later, and a valuer may well notice.")
            + p("This is also why we ask investors for the builder's report alongside the Healthy Homes assessment. Read together they give a much clearer picture of what the property actually needs. See " + link("lim-builders-report-finance-nz.html", "our guide to LIM and builder's reports") + ".")
        )),
        ("Timing the work around your tenancy", (
            p("The practical sequencing problem is that remediation is easiest in an empty property, but an empty property earns nothing and your lender has assessed your serviceability partly on rental income.")
            + p("Options worth discussing with your adviser before settlement:")
            + ul([
                "<strong>Settle and complete work before tenanting.</strong> Cleanest execution, but you carry the mortgage with no income for the period.",
                "<strong>Buy with a tenant in place and work around them.</strong> Income continues, but scheduling is harder and some work is impractical while occupied.",
                "<strong>Negotiate the work as a vendor condition.</strong> The vendor completes compliance before settlement. Best outcome for you where the vendor agrees, though it will usually be reflected in the price.",
            ])
            + p("Whichever route you take, build the vacancy period or the remediation cost into your serviceability assessment honestly. A plan that assumes rent from week one and no remediation cost is not a plan.")
        )),
    ],

    "student-loan-mortgage-borrowing-power-nz": [
        ("A worked comparison of the two choices", (
            p("Take an applicant with $20,000 saved and a $15,000 student loan, deciding whether to clear the loan or keep the savings as deposit. Using round illustrative numbers:")
            + table(
                ["", "Clear the loan", "Keep it as deposit"],
                [
                    ["Savings remaining", "$5,000", "$20,000"],
                    ["Student loan balance", "Nil", "$15,000"],
                    ["Compulsory repayment", "Removed — frees serviceability", "Continues — counts as an expense"],
                    ["Deposit available", "$5,000", "$20,000"],
                    ["Likely effect", "Slightly higher assessed capacity, but a very small deposit", "Lower assessed capacity, far stronger deposit position"],
                ],
            )
            + p("For most first home buyers the right-hand column wins, and often decisively, because deposit size drives both the loan-to-value band you land in and whether you qualify at all. Clearing a $15,000 loan to free up a modest amount of monthly serviceability rarely compensates for arriving with $5,000 deposit.")
            + p("The calculus flips when the loan balance is small relative to your savings. Clearing a $2,000 balance out of $60,000 in savings removes a committed expense permanently at negligible cost to your deposit — that is usually worth doing.")
        )),
        ("If you are heading overseas, or coming back", (
            p("Student loan obligations change when you stop being New Zealand-based. Overseas-based borrowers face a different repayment basis — obligations are generally set as fixed amounts based on the loan balance rather than calculated as a share of income — and interest applies to the loan, unlike the interest-free treatment for New Zealand-based borrowers.")
            + p("Two consequences that matter for a mortgage:")
            + ul([
                "<strong>If you are leaving.</strong> Your repayment obligation and the accrual of interest change, so a loan you were comfortably servicing can become more expensive. Factor that into any plan to buy here and rent the property out while away.",
                "<strong>If you are returning.</strong> Arrears accumulated while overseas can be substantial and can affect your credit position. Resolve the loan status with Inland Revenue before applying for a mortgage, and get a current statement for your file.",
            ])
            + p("Returning borrowers should also read " + link("non-resident-offshore-income-mortgage-nz.html", "our guide to offshore income mortgages") + ", which covers the broader documentation requirements.")
        )),
        ("The bigger levers, in order", (
            p("If increasing your borrowing capacity is the goal, the student loan is rarely where the biggest gain sits. In rough order of effect per dollar or hour of effort:")
            + ol([
                "<strong>Reduce or cancel unused credit card and overdraft limits.</strong> Free, immediate, and frequently the largest single gain because lenders assess against the limit.",
                "<strong>Clear short-term consumer debt</strong> with high repayments relative to balance — car finance, hire purchase, personal loans.",
                "<strong>Close BNPL facilities</strong> and give yourself three to four clean months of statements.",
                "<strong>Grow the deposit</strong>, which improves both the amount and the pricing.",
                "<strong>Consider a longer loan term</strong>, which reduces the assessed repayment, though it increases total interest paid.",
                "<strong>Then look at the student loan</strong>, and only clear it if you can do so without materially denting the deposit.",
            ])
            + p("Our guide to " + link("car-loan-personal-debt-borrowing-power-nz.html", "what car loans and credit cards really cost you") + " covers the first two in detail.")
        )),
    ],

    "afterpay-bnpl-mortgage-application-nz": [
        ("What else on your statements gets read", (
            p("BNPL is one line in a broader review. While an assessor has three to six months of your transactions open, they are forming a view of your overall financial conduct. Things that draw attention:")
            + ul([
                "<strong>Gambling transactions.</strong> Treated seriously by most lenders, particularly where frequent or escalating. This is one of the more common reasons an otherwise strong file is declined.",
                "<strong>Dishonoured payments and overdraft fees.</strong> Direct evidence of running out of money on a scheduled payment date.",
                "<strong>Payday or short-term high-cost lending.</strong> A significant negative signal, generally more damaging than BNPL.",
                "<strong>Undeclared debt repayments.</strong> Regular payments to a lender you did not disclose. This is a credibility problem as much as a serviceability one.",
                "<strong>Living expenses well below your declared figure.</strong> If you declare $800 a month of living costs and your statements show $2,000, the assessor will use the statements.",
                "<strong>Large unexplained deposits.</strong> These attract source-of-funds questions under anti-money-laundering obligations.",
            ])
            + p("The reassuring counterpoint: ordinary spending is ordinary. Nobody is judging your coffee habit. What matters is whether the account shows a consistent surplus and no signs of stress.")
        )),
        ("How to present living expenses credibly", (
            p("Lenders apply benchmark household expense figures and compare them against both your declared costs and your actual statements. They will generally use the higher of the benchmark and your declared figure, so understating costs achieves nothing except damaging your credibility.")
            + p("The better approach:")
            + ol([
                "Work out your actual monthly spending from three months of statements before you fill in any application.",
                "Declare that figure, not an optimistic one.",
                "Where a recent period was unusually high for an identifiable reason — a holiday, a medical cost, moving house — note it explicitly so the assessor does not treat it as your baseline.",
                "Where you have genuinely cut back, give it a few months so the statements support the new figure.",
            ])
            + p("An application where declared expenses match the statements reads as competent and honest, and that counts for a lot on a marginal file.")
        )),
        ("A three-month clean-up plan", (
            p("If you intend to apply in roughly three to four months, here is a concrete sequence:")
            + table(
                ["Period", "Actions"],
                [
                    ["Now", "List every BNPL account, credit card, overdraft and consumer debt with its limit and balance. Stop opening anything new."],
                    ["Weeks 1-2", "Clear and close BNPL accounts. Reduce or cancel unused credit card and overdraft limits."],
                    ["Weeks 2-4", "Set up a dedicated savings transfer on payday so the statements show deliberate saving."],
                    ["Months 2-3", "Keep the accounts clean. No dishonours, consistent surplus, no new credit enquiries."],
                    ["Month 3-4", "Pull your own credit report and check it. Then talk to your broker with three clean months behind you."],
                ],
            )
            + p("Checking your own credit report costs nothing and does not harm your score. Doing it before you apply means you find any errors or forgotten defaults while there is still time to deal with them — see " + link("improve-credit-score-mortgage-nz.html", "improving your credit score before a mortgage") + ".")
        )),
    ],
    "car-loan-personal-debt-borrowing-power-nz": [
        ("Why removing a repayment buys so much mortgage capacity", (
            p("The reason clearing short-term debt has an outsized effect is the difference in term. A car loan might be repaid over five years; a mortgage is assessed over thirty. So a dollar of monthly commitment removed from the short-term debt frees up a dollar of monthly capacity that can support a much larger amount of long-term borrowing.")
            + p("The precise multiple depends on the lender's stress-test rate and assessment term, and it is not something to calculate on the back of an envelope — but the direction is reliable and the magnitude is usually surprising. This is why we ask clients for a full list of commitments before talking about property prices.")
            + callout("The counterintuitive part", "A $6,000 car loan with a large monthly repayment can restrict your borrowing more than a $20,000 student loan with a modest income-based deduction. Size of debt is a poor guide to its impact. Monthly commitment is the thing to look at.")
        )),
        ("Credit limits: the free win most buyers miss", (
            p("Because revolving facilities are assessed against the limit rather than the balance, reducing limits costs you nothing and can move your capacity materially. What to do:")
            + ol([
                "List every credit card, store card and overdraft with its limit — including ones you never use.",
                "Decide the minimum limit you genuinely need for emergencies. Many buyers find the honest answer is zero or a small buffer.",
                "Ask your bank to reduce the limits in writing, or close the facilities entirely.",
                "Get written confirmation of the closure or reduction, because your broker will need to evidence it.",
                "Do this before the application, not during it. A limit reduction processed mid-assessment creates confusion.",
            ])
            + p("One caution: closing your oldest credit account can slightly affect your credit file, since length of credit history is one factor in a score. In practice the serviceability gain from removing a large limit almost always outweighs that, but if you have several cards, keep the oldest with a small limit and close the rest.")
        )),
        ("Interest-free and buy-now-pay-later finance still counts", (
            p("Store finance arranged as twelve or twenty-four months interest-free feels free, and in interest terms it is. But it is a contracted term debt with a monthly repayment, it appears on your credit file in most cases, and lenders assess the repayment like any other.")
            + p("The same applies to:")
            + ul([
                "Furniture and appliance finance on deferred-payment terms.",
                "Mobile phone plans with a handset repayment component.",
                "Gym and service contracts with a fixed term you cannot exit.",
                "Vehicle leases and novated arrangements, which are sometimes overlooked because they are not called loans.",
            ])
            + p("Declare all of it. These arrangements show on bank statements and often on credit files, and an undeclared commitment that the assessor finds is worse than a declared one — it calls the rest of your application into question. Our " + link("mortgage-document-checklist-nz.html", "document checklist") + " covers what to gather.")
        )),
    ],

    "mortgage-on-parental-leave-nz": [
        ("Building the strongest possible file", (
            p("Because policy varies, the quality of your evidence does more work here than almost anywhere. A file that answers every obvious question before it is asked gets a different reception from one that invites queries. What to assemble:")
            + ol([
                "<strong>The return-to-work letter</strong>, specific on date, hours and pay, on employer letterhead and signed by someone with authority.",
                "<strong>Pre-leave payslips</strong> covering at least three months before leave started, showing your normal income.",
                "<strong>Your most recent IRD income summary</strong>, which corroborates the pre-leave figure independently.",
                "<strong>Evidence of current parental leave payments</strong>, including any employer top-up.",
                "<strong>Your partner's full income documentation</strong>, if applying jointly.",
                "<strong>A written childcare plan with actual quoted costs</strong>, plus any subsidy entitlement you have confirmed.",
                "<strong>Bank statements</strong> showing you have managed the reduced-income period without stress.",
            ])
            + p("That last item is quietly persuasive. Statements showing you have lived within the lower parental leave income, without dishonours or overdraft reliance, directly demonstrate the resilience the lender is trying to assess.")
        )),
        ("Returning part-time: get the numbers right", (
            p("Many parents return to fewer hours than they left. That is entirely workable, but it has to be presented accurately from the outset, because the application is assessed on the income you will actually have.")
            + p("Common mistakes we see:")
            + ul([
                "A return-to-work letter stating full-time hours when the plan is three days a week. If the lender later verifies this, the application has a credibility problem.",
                "Budgeting on full-time income while planning part-time hours, which produces an approval you cannot comfortably service.",
                "Forgetting that part-time hours and childcare costs move in opposite directions — fewer work days means less income but also less childcare.",
            ])
            + p("The honest approach is usually also the better one: state the actual return hours and pay, include the real childcare cost for those days, and get an approval that fits the life you are going to be living.")
        )),
        ("What to do if the timing is tight", (
            p("If you have found a property and your pre-approval does not reflect your leave situation, move quickly and in the right order:")
            + ol([
                "Tell your broker immediately what has changed. Do not submit an application and hope.",
                "Get the return-to-work letter started — employers can take a week or more to produce one.",
                "Negotiate a longer finance condition in your offer, since this file needs more assessment time than a standard one. See " + link("finance-condition-sale-purchase-nz.html", "how long a finance condition really needs") + ".",
                "Be prepared for the possibility that the achievable loan is lower than your pre-leave approval, and know your fallback before you make the offer.",
            ])
            + p("The worst outcome is going unconditional on the assumption that a pre-leave pre-approval still stands. Confirm the position first.")
        )),
    ],

    "casual-part-time-seasonal-income-mortgage-nz": [
        ("A worked seasonal example", (
            p("Take a seasonal worker whose income arrives unevenly across the year. Using round illustrative figures:")
            + table(
                ["Period", "Gross income", "What a lender sees"],
                [
                    ["Peak season (4 months)", "$38,000", "Strong, but not sustainable at this rate"],
                    ["Shoulder (3 months)", "$12,000", "Reduced hours"],
                    ["Off-season (5 months)", "$6,000", "Minimal or no work"],
                    ["Full year", "$56,000", "The figure to build an application on"],
                ],
            )
            + p("If this applicant submits four months of peak payslips, the lender annualises something close to $114,000 — then discovers from tax records or bank statements that the real figure is $56,000, and the application loses credibility. If the same applicant submits two years of IRD income summaries showing roughly $56,000 each year, the lender has a reliable figure and a demonstrated pattern.")
            + p("The second approach yields a lower headline income and a much better outcome. Consistency across two years is worth more than a strong recent run.")
        )),
        ("Making your bank statements work for you", (
            p("With irregular income, your statements are doing more than verifying deposits — they are demonstrating that you can manage the pattern. Over three to six months a lender wants to see:")
            + ul([
                "<strong>Deliberate saving through the peak.</strong> Regular transfers into a savings account while income is high is the single most persuasive behaviour you can show.",
                "<strong>Controlled drawdown through the lean period.</strong> Living off savings rather than credit.",
                "<strong>No dishonours or overdraft reliance</strong> in the off-season.",
                "<strong>No short-term or payday lending</strong> bridging gaps between seasons.",
            ])
            + p("If your recent statements do not look like this, the fix is behavioural and it takes a few months. That is frustrating if you want to buy now, but it is far more effective than hoping a lender overlooks it — and it is the same pattern we describe in our guide to " + link("afterpay-bnpl-mortgage-application-nz.html", "BNPL on mortgage applications") + ".")
        )),
        ("Fixed-term contracts and labour-hire arrangements", (
            p("A particular sub-case worth separating out: workers on fixed-term contracts, or engaged through a labour-hire or recruitment agency. Here the income may be regular and substantial, but the engagement has an end date, which is what concerns a lender.")
            + p("What strengthens these applications:")
            + ol([
                "A history of successive contracts, ideally with the same client or agency, showing the work keeps being renewed.",
                "A current contract with as much remaining term as possible.",
                "Evidence of demand in your field, and of your own track record of continuous engagement.",
                "Where available, a letter from the client or agency indicating intention to renew or extend.",
            ])
            + p("Lender appetite for fixed-term income varies a great deal — some treat a well-established contractor as equivalent to a permanent employee, others apply significant caution. Our " + link("../case-studies/contractor-fixed-term-income.html", "contractor case study") + " shows how one of these files was put together.")
        )),
    ],

    "non-resident-offshore-income-mortgage-nz": [
        ("Documentation: expect more of everything", (
            p("Cross-border files require substantially more paperwork than domestic ones, and gathering it is usually the longest part of the process. Plan for:")
            + ol([
                "<strong>Identity verification</strong> to New Zealand AML standards, often requiring certified copies of passports and proof of address, sometimes certified by a notary or embassy.",
                "<strong>Two years of overseas tax returns and assessments</strong>, with certified translations where they are not in English.",
                "<strong>Overseas payslips and employment contracts</strong>, again translated where needed.",
                "<strong>Overseas bank statements</strong> for the accounts your income is paid into and your deposit is held in.",
                "<strong>Overseas credit reports</strong>, where you have no New Zealand credit history.",
                "<strong>Evidence of visa or residency status</strong>, and legal confirmation of your eligibility to purchase.",
                "<strong>Full source-of-funds trail</strong> for the deposit.",
            ])
            + p("Start this early. Obtaining certified translations and overseas tax documents can take weeks, and it is the most common cause of delay on these files — not the lending decision itself.")
        )),
        ("How currency shading works in practice", (
            p("Where a lender accepts foreign income, it will typically convert it to New Zealand dollars and then apply a discount to protect against exchange rate movement. The discount exists because if your home currency weakens against the NZD, your effective income to service a NZD mortgage falls.")
            + p("Two practical consequences:")
            + ul([
                "<strong>The income used will be well below what you earn.</strong> Budget on the shaded figure, not the gross.",
                "<strong>Currency choice matters.</strong> Lenders that accept foreign income generally maintain a list of acceptable currencies, usually major ones. Income in a currency outside that list may not be assessable at all, regardless of amount.",
            ])
            + p("There is also a real risk to you, not just the lender. If you are earning abroad and servicing a NZD mortgage, you carry genuine exchange rate exposure on your monthly payment. Build a buffer rather than budgeting at the current rate.")
        )),
        ("Tax and withholding considerations", (
            p("Owning New Zealand property while living overseas brings tax obligations that are easy to overlook and expensive to get wrong. Issues to take advice on before you buy:")
            + ul([
                "<strong>Rental income</strong> from a New Zealand property is taxable here, and there are withholding and filing obligations for non-resident owners.",
                "<strong>The bright-line test</strong> applies to residential property sales within the relevant period, and the main home exclusion generally will not help if you are not living in it — see " + link("bright-line-test-nz-2026.html", "our bright-line guide") + ".",
                "<strong>Residential land withholding tax</strong> can apply on sale by an offshore person.",
                "<strong>Double tax agreements</strong> may affect how income is taxed between New Zealand and your country of residence.",
            ])
            + p("These are accountant questions and they warrant specialist cross-border advice. Getting them right before purchase is far cheaper than restructuring afterwards.")
        )),
    ],

    "one-year-self-employed-mortgage-nz": [
        ("How to present your financials", (
            p("The presentation of a one-year file matters because the lender is being asked to extrapolate from limited data. You are trying to make that extrapolation feel safe. Practical steps:")
            + ol([
                "<strong>Use a chartered accountant.</strong> Financials prepared by a recognised professional carry weight that spreadsheets and software exports do not.",
                "<strong>Provide year-to-date figures.</strong> Nothing supports a single year of accounts better than current-year numbers showing the trend holding or improving.",
                "<strong>Reconcile to GST returns.</strong> Independent corroboration of turnover from a third-party source is persuasive.",
                "<strong>Include an accountant's letter.</strong> A short letter commenting on the business's position, the sustainability of drawings, and any one-off items in the accounts can resolve questions before they are asked.",
                "<strong>Explain any unusual items.</strong> Start-up costs, one-off equipment purchases or a bad debt in year one all depress profit. Flag them with evidence rather than letting the assessor assume they are recurring.",
            ])
            + p("See our " + link("../services/self-employed.html", "self-employed mortgage page") + " for how we assemble these files.")
        )),
        ("Add-backs: what they are and why they matter", (
            p("Lenders assess your income as net profit plus certain add-backs — expenses recorded in the accounts that do not represent cash leaving your pocket, or that will not recur. Commonly considered:")
            + table(
                ["Add-back", "Why it is added back"],
                [
                    ["Depreciation", "An accounting entry, not a cash outflow in the period."],
                    ["Interest on business debt being refinanced", "If the debt is being repaid or restructured, the expense changes."],
                    ["One-off non-recurring expenses", "Start-up costs, a single equipment purchase, a legal dispute — not part of ongoing trading."],
                    ["Certain home office and vehicle apportionments", "Treatment varies; some lenders add back a portion."],
                    ["Shareholder salary adjustments", "Where drawings and salary are structured for tax rather than reflecting the business's capacity."],
                ],
            )
            + p("Treatment varies between lenders, and some are noticeably more generous than others. This is a significant source of difference in the maximum loan available on identical accounts — and one reason a decline from a single lender tells you very little.")
        )),
        ("Planning ahead if you can wait", (
            p("If buying is twelve to eighteen months away, you can materially improve your position between now and then. What actually helps:")
            + ul([
                "<strong>Talk to your accountant about the tax-versus-lending trade-off</strong> before the next set of accounts is finalised. Minimising taxable profit reduces assessable income.",
                "<strong>Keep business and personal banking cleanly separated.</strong> Mixed accounts make assessment harder and slower.",
                "<strong>Take consistent, regular drawings</strong> rather than irregular lump sums. It reads as a sustainable income pattern.",
                "<strong>Build the deposit</strong>, which does more for a self-employed file than almost anything else.",
                "<strong>Keep your personal credit clean</strong> and reduce consumer debt and credit limits — see " + link("car-loan-personal-debt-borrowing-power-nz.html", "what consumer debt costs your borrowing power") + ".",
                "<strong>Secure longer-term contracts</strong> where your industry allows, as evidence of forward revenue.",
            ])
            + p("A client who does these things for a year arrives with a genuinely strong two-year file rather than a marginal one-year file, and the difference in both approval likelihood and pricing is usually significant.")
        )),
    ],
    "finance-condition-sale-purchase-nz": [
        ("Other conditions that interact with finance", (
            p("The finance condition rarely sits alone, and the others have their own dates that need to work together. Common conditions in a New Zealand offer:")
            + ul([
                "<strong>LIM report.</strong> Council-issued, and it takes time to arrive. What it contains can affect your finance, so ideally the LIM date sits before the finance date.",
                "<strong>Builder's report.</strong> Same logic — issues found here can change what a lender will do.",
                "<strong>Valuation.</strong> Sometimes a separate condition, though often it is the lender requiring one as part of finance.",
                "<strong>Title approval.</strong> Your lawyer reviewing the record of title, easements, covenants and any disclosure statements.",
                "<strong>Sale of your existing property.</strong> The most complex to coordinate, and it carries its own finance implications.",
            ])
            + p("Sequence these deliberately. A finance condition that expires before your builder's report is due means you are confirming finance without knowing what the inspector found — which defeats the purpose of both conditions.")
        )),
        ("Buying before you sell", (
            p("If you need to sell your current home to buy the next one, you have a sequencing problem that affects your finance condition directly. The options:")
            + table(
                ["Approach", "How it works", "Risk"],
                [
                    ["Sell first, then buy", "Go to market unconditional with cash in hand.", "You may need to rent between, and you buy in an unknown market."],
                    ["Buy conditional on sale", "Your offer is conditional on selling your existing property.", "Vendors dislike it; often uncompetitive, and may carry a cash-out clause."],
                    ["Bridging finance", "Borrow to hold both properties briefly.", "Costs more, and you carry two loans until the sale settles."],
                ],
            )
            + p("Bridging is the route that preserves the most flexibility, and it is more accessible than many people assume where there is decent equity. It does need to be arranged in advance, not discovered mid-negotiation. Our " + link("bridging-finance-guide-nz.html", "bridging finance guide") + " explains how it works and what it costs.")
        )),
        ("Getting the condition period right: a checklist", (
            ol([
                "Talk to your broker before you write the offer, not after it is accepted.",
                "Have your documents already gathered so day one is submission day, not collection day.",
                "Ask whether a registered valuation is likely for this property and deposit level, and how long valuations are taking in that area.",
                "Add working days for self-employed income, unusual title, hazard exposure or apartment purchases.",
                "Count the public holidays in the period.",
                "Have your lawyer draft or review the clause wording.",
                "Agree with your broker and lawyer who is confirming what, and by when.",
            ])
            + p("A realistic condition period costs you very little in negotiating position — most vendors prefer a credible fifteen working days to an optimistic ten that collapses. What costs you is being unable to confirm, and either losing the property or going unconditional on finance you do not yet have.")
        )),
    ],

    "pre-approval-expired-nz": [
        ("Conditional versus fully assessed pre-approvals", (
            p("Not all pre-approvals carry the same weight, and knowing which you hold matters when it lapses.")
            + ul([
                "<strong>An indicative or system-generated pre-approval</strong> is based on information you supplied, often online, with limited verification. It is useful for setting a budget but a lender can revise it substantially once documents are assessed.",
                "<strong>A fully assessed pre-approval</strong> has had your income, expenses and credit verified by a credit assessor. It is far more reliable and, when it expires, far easier to renew because the assessment work has been done.",
            ])
            + p("If your lapsed approval was the indicative kind, treat the renewal as a first proper application rather than a refresh — and allow more time. If it was fully assessed, renewal is usually quick where nothing has changed.")
            + callout("Worth asking", "When you get any pre-approval, ask explicitly: has this been assessed by a credit team, what conditions attach to it, and when does it expire? Those three answers tell you how much you can rely on it.")
        )),
        ("What a pre-approval never covers", (
            p("Even a current, fully assessed pre-approval has limits that catch buyers out. It generally does not confirm:")
            + ul([
                "<strong>That the lender will accept a particular property as security.</strong> Apartment size, title type, hazard exposure, unconsented work and rural land can all cause a property-specific decline.",
                "<strong>The valuation.</strong> The lender lends against the lower of price or valuation, and the valuation is only done once you have a property.",
                "<strong>Insurability.</strong> A property that cannot be insured generally cannot be mortgaged.",
                "<strong>The interest rate.</strong> Rates at drawdown are what you get, unless a specific rate lock applies.",
            ])
            + p("This is why a finance condition remains necessary even with pre-approval in hand — see " + link("finance-condition-sale-purchase-nz.html", "the finance condition explained") + ". A pre-approval tells you the lender is comfortable with <em>you</em>; the condition protects you while they get comfortable with the <em>property</em>.")
        )),
        ("Using the gap productively", (
            p("If your pre-approval has lapsed and you are not under immediate pressure, the interval is an opportunity rather than a setback. The things that will most improve your next approval:")
            + ol([
                "<strong>Reduce or cancel unused credit limits.</strong> Free, and often the largest single gain.",
                "<strong>Clear short-term consumer debt</strong> with high repayments relative to balance.",
                "<strong>Add to the deposit</strong>, which improves both the amount available and the pricing band.",
                "<strong>Get three to four clean months of bank statements</strong> with no dishonours and a visible surplus.",
                "<strong>Check your own credit report</strong> for errors or forgotten defaults while there is still time to resolve them.",
                "<strong>Resolve anything that changed</strong> — document a new job, a changed income, or a cleared default.",
            ])
            + p("Clients who come back after three focused months frequently get a better number than their original approval, not merely the same one. See " + link("car-loan-personal-debt-borrowing-power-nz.html", "what consumer debt costs your borrowing power") + " for where the biggest gains usually sit.")
        )),
    ],

    "buying-off-the-plans-finance-nz": [
        ("Progressive payment versus single settlement", (
            p("Off-the-plans contracts are structured in one of two broad ways, and which you are signing changes your finance requirement completely.")
            + ul([
                "<strong>Single settlement on completion.</strong> You pay a deposit on signing — commonly held in a trust account — and the balance in one payment when the build is complete and title issues. Your mortgage draws down once, at the end. This is the typical structure for apartments and completed townhouses.",
                "<strong>Progressive payments during construction.</strong> You pay in stages as the build progresses. This is more common where you own the land and are contracting a build, and it requires a construction loan with staged drawdowns rather than a standard mortgage.",
            ])
            + p("The distinction matters because a construction facility is assessed differently — against a fixed-price build contract, with the lender inspecting and releasing funds at each stage. Our " + link("../services/construction-loan.html", "construction loan page") + " sets out how that works. If you are not sure which structure your contract uses, ask your lawyer before signing.")
        )),
        ("Title, CCC and what has to exist before you can settle", (
            p("Settlement on an off-the-plans purchase depends on things that have nothing to do with your finance being ready. Typically all of the following must be in place:")
            + ol([
                "<strong>A separate title issued</strong> for your unit or lot. On a subdivision this requires survey, council sign-off and LINZ registration, and it can lag the physical completion of the building.",
                "<strong>Code compliance certificate</strong> confirming the building work complies with its consent.",
                "<strong>For a unit title, the body corporate established</strong> and the unit plan deposited.",
                "<strong>Your lender's final approval</strong>, based on a valuation of the completed property.",
            ])
            + p("Delays in any of these delay your settlement, and the contract will specify what happens then — including whether interest or penalties accrue. Have your lawyer explain the settlement mechanics and what happens if title is late, because it is common.")
        )),
        ("A pre-purchase due diligence list", (
            p("Before you pay a deposit on an off-the-plans purchase, work through the following with your lawyer and your broker:")
            + table(
                ["Area", "What to establish"],
                [
                    ["The developer", "Completed projects, whether they finished on time, whether buyers settled without issue."],
                    ["Deposit protection", "Where your deposit is held, whether in a solicitor's trust account, and what security you have."],
                    ["Sunset clause", "The date, who can cancel, how it can be extended and by whom."],
                    ["Variation rights", "Whether the developer can change plans, finishes or unit size, and within what tolerance."],
                    ["Title and CCC timing", "What must exist before settlement and what happens if it is late."],
                    ["Body corporate", "Projected levies, the proposed long-term maintenance plan, and your unit entitlement."],
                    ["Your finance position", "An indicative lending assessment now, and a plan to reconfirm as completion approaches."],
                    ["Your downside", "Whether you could still settle if the valuation came in below the contract price."],
                ],
            )
            + p("The last line is the one to be most honest with yourself about. Everything else is manageable; a valuation shortfall you cannot cover is the scenario that forces a distressed outcome.")
        )),
    ],

    "lim-builders-report-finance-nz": [
        ("Choosing and briefing a building inspector", (
            p("Building inspection is not a licensed occupation in New Zealand in the way some trades are, so the quality of reports varies considerably. What to look for and how to brief them:")
            + ul([
                "<strong>Relevant qualifications and membership</strong> of a recognised industry body, and professional indemnity insurance.",
                "<strong>A written report with photographs</strong>, not a verbal summary or a tick-box sheet.",
                "<strong>Willingness to use moisture meters</strong> and, where warranted, recommend invasive testing.",
                "<strong>A clear scope statement</strong> setting out what was and was not inspected — most reports exclude areas that could not be accessed.",
                "<strong>Independence from the agent.</strong> Commission your own inspector rather than using one recommended by the selling agent.",
            ])
            + p("Brief them on anything specific you are worried about: the cladding type, a suspected addition, moisture staining you noticed, or the subfloor. A general inspection may not look closely at something you have a particular concern about unless you raise it.")
        )),
        ("Reading the consent record on a LIM", (
            p("The building consent section of a LIM is where unconsented work reveals itself, but it takes some interpretation. What you are comparing is the consent history against what physically exists.")
            + ol([
                "List every consent on the LIM, with its description and date.",
                "Check whether each has a code compliance certificate. A consent issued but never signed off is a problem in itself, separate from entirely unconsented work.",
                "Walk the property against that list. Is there a deck, carport, sleepout, extension or woodburner with no corresponding consent?",
                "Check the floor area. If the LIM or rating record shows a smaller area than the house appears to have, something has been added.",
                "Note any notices, requisitions or outstanding council requirements.",
            ])
            + p("Where you find a gap, get it priced and get advice before your conditions expire. A deck without consent might be resolved cheaply; a converted garage being used as a bedroom is a bigger piece of work with valuation consequences.")
        )),
        ("Using a report to renegotiate", (
            p("A report that finds problems is not a failure — it is information, and information has negotiating value. How to use it well:")
            + ul([
                "<strong>Get the remediation priced by a tradesperson</strong> before you raise it. A quote is a negotiating position; a worry is not.",
                "<strong>Separate the serious from the cosmetic.</strong> Bundling minor maintenance with a genuine structural issue weakens your case on the thing that matters.",
                "<strong>Check with your broker first</strong> whether the lender will proceed at all. There is no point negotiating a discount on a property your lender will not accept as security.",
                "<strong>Decide your position before you open the conversation</strong> — a price reduction, vendor remediation before settlement, or cancellation.",
                "<strong>Keep it in writing through your lawyer</strong>, so any agreed variation is properly recorded.",
            ])
            + p("Vendors who have already had one buyer walk away over a report are often more receptive than you expect. Equally, in a competitive market you may have little leverage — which is why knowing your lender's position first matters so much.")
        )),
    ],

    "buying-house-from-family-below-market-value-nz": [
        ("Getting the valuation right", (
            p("The registered valuation is the foundation of a favourable purchase, because the gifted equity is measured against it. A few points that matter:")
            + ul([
                "<strong>It must be a registered valuation.</strong> A rating valuation is a mass-appraisal figure for rates purposes and is not acceptable. An agent's appraisal is a marketing estimate, not a valuation.",
                "<strong>The lender usually instructs it.</strong> Most lenders require the valuation to be commissioned through their own panel, so a valuation you obtained independently may need to be redone.",
                "<strong>It reflects market value, not family value.</strong> The valuer assesses what the property would sell for on the open market, which is the whole point.",
                "<strong>Valuations have a shelf life.</strong> If the transaction takes months to organise, the lender may require a fresh one.",
            ])
            + p("Do not agree a price with your family before you have a sense of the valuation and the lender's policy. A price agreed on assumption can need renegotiating, which is an awkward conversation inside a family.")
        )),
        ("The paperwork, in order", (
            ol([
                "<strong>Establish lender policy</strong> on favourable purchases and how much of the deposit may come from gifted equity.",
                "<strong>Each party engages their own lawyer.</strong> Separate representation is required and it protects everyone.",
                "<strong>Obtain the registered valuation</strong> through the lender's process.",
                "<strong>Agree the price</strong> in light of the valuation and the lender's requirements.",
                "<strong>Sign a proper sale and purchase agreement</strong> at the agreed price.",
                "<strong>Vendor signs a gifting certificate or deed of gift</strong> confirming the discount is a genuine gift, with no repayment expected and no security retained.",
                "<strong>Vendor obtains independent advice</strong> on the consequences for them — tax, estate, and any future residential care assessment.",
                "<strong>Submit the full package</strong> to the lender together, so the file is not held up by a missing document.",
            ])
            + p("The most common cause of delay on these files is a gifting certificate that is missing, unsigned, or worded in a way that implies repayment. Get the wording from your lawyer rather than using a template.")
        )),
        ("Writing down what the family has agreed", (
            p("The hardest part of these transactions is not legal or financial — it is the unspoken expectations. Years later, a sibling remembers it as an advance on inheritance and you remember it as a gift. Nobody wrote anything down.")
            + p("What we encourage families to document, separately from the lending paperwork:")
            + ul([
                "Whether the discount is intended as an advance on inheritance, to be accounted for in the estate, or as a gift that is not.",
                "What happens if the vendor later needs the capital — and the clear acknowledgement that it is gone.",
                "Whether other children are to receive equivalent help, and when.",
                "What happens if you separate from a partner, and whether a contracting out agreement is needed.",
                "What happens if you later want to sell.",
            ])
            + p("A short written record signed by everyone, prepared alongside the legal documents, costs very little and prevents the kind of dispute that outlives the mortgage. Your lawyer can incorporate this into the estate planning conversation at the same time.")
        )),
    ],
}

for _post in POSTS:
    _post["sections"] = _post["sections"] + EXTRA_SECTIONS.get(_post["slug"], [])


# Additional FAQs for posts that sat under the 1,500-word floor in
# context/seo-guidelines.md. More FAQ coverage also widens the FAQPage schema
# surface, which is what AI answer engines quote from.

EXTRA_FAQS = {
    "cross-lease-unit-title-freehold-nz": [
        ("Can I convert a cross-lease to freehold?",
         "Sometimes. It requires a surveyor, a subdivision consent from the council, and the agreement of every other owner on the title. That unanimous-agreement requirement is usually the obstacle, since one unwilling or uncontactable owner stops the process. Where owners co-operate it can improve value and remove the shared-ownership complications permanently, so it is worth asking a surveyor about feasibility for your specific title."),
        ("What is a land covenant and can it affect my plans?",
         "A covenant is a restriction registered on the title that binds you as the new owner. Covenants commonly control building materials, roof and fence heights, minimum floor areas, how many dwellings may be built, or whether a business can be run from the property. They are not always obvious from a listing, so ask your lawyer to report on any registered covenants before you go unconditional."),
    ],
    "earthquake-prone-building-mortgage-wellington": [
        ("What is the difference between an ISA and a DSA?",
         "An Initial Seismic Assessment is a relatively quick, largely desk-based review producing an indicative rating. A Detailed Seismic Assessment is a thorough engineering analysis of the specific structure, often involving intrusive investigation, and is far more reliable. A DSA can produce a materially different rating from an earlier ISA in either direction, so always ask which type produced the figure you have been given, and when."),
        ("Who arranges insurance in an apartment building?",
         "In a unit title building the body corporate generally arranges insurance for the whole structure, so your individual position depends on a decision you do not control. That matters for your mortgage, because if the body corporate loses or cannot renew cover, your lending is affected regardless of your own conduct. Check the current insurance position and recent renewal history before you commit."),
    ],
    "tc2-tc3-land-christchurch-mortgage": [
        ("What should I check if a Canterbury property was cash-settled?",
         "Establish whether the repair work was actually done. The settlement money went to the previous owner, and if damage remains the remediation cost falls to you, with the entitlement to claim again generally not transferring. Ask for the settlement documentation and the scope it was assessed against, evidence of what was done including consents and code compliance certificates, a builder's report briefed on those areas, and written confirmation that an insurer will cover the property as it stands."),
        ("What order should I do things in when buying bare TC3 land?",
         "Make your offer conditional on a satisfactory geotechnical investigation with enough working days to complete it, commission the geotech report and have it reviewed, get the foundation design priced, and only then finalise your construction lending. Signing a build contract before the geotech work is complete risks discovering a substantial unbudgeted foundation cost after you have already committed to the land."),
    ],
    "flood-zone-insurance-mortgage-decline-nz": [
        ("What does an insurance decline usually look like in practice?",
         "Insurers rarely say a flat no. More often they offer terms that have the same effect for a lender: cover with a flood exclusion, an excess so high that a realistic event is effectively uninsured, a sum insured capped below full replacement, or a referral to an underwriter that produces no answer before your finance condition expires. That last one is the most common way these deals quietly fail."),
        ("What should I ask an insurer before making an offer?",
         "Ask whether they will offer full replacement cover at that specific address, whether flood and natural disaster cover is included or excluded, what the excess is for flood specifically, what the annual premium is and whether it has changed materially at that address recently, and whether the quote is subject to inspection. Then ask them to confirm it in writing — a verbal indication from a call centre is not evidence a lender can rely on."),
    ],
    "lifestyle-block-rural-lending-waikato": [
        ("What do lenders check about water and wastewater on a rural property?",
         "For water they look at the source — tank, bore, stream take under consent, or a shared rural scheme — and whether supply is adequate and potable. For wastewater they want the septic or treatment system to be consented and functioning. Get the water tested and the system inspected before going unconditional, and check the LIM for any consents or abatement notices, since an unconsented or failing system becomes your compliance problem."),
        ("Why does access matter so much on a rural title?",
         "Because a lender taking the property as security needs the access to be legally secure. If your driveway crosses someone else's land there should be a registered easement; informal access by long-standing arrangement may not be enforceable. Unformed legal road, where access exists in law but no road was ever built, is a significant issue for both value and insurability. Have your lawyer report specifically on access and any consent notices."),
    ],
    "queenstown-holiday-home-short-stay-income-mortgage": [
        ("What costs come out of short-stay income before I see it?",
         "Platform commission and payment fees, management fees if you are not self-managing, cleaning and linen between every guest, consumables and higher wear than a long-term tenancy, rates which may sit in a different category for mixed use, specialist insurance rather than a standard domestic policy, body corporate levies where applicable, and the income you forgo during periods you block out for your own use."),
        ("How should I stress-test a short-stay purchase?",
         "Ask whether the property would service the mortgage as a conventional long-term rental. Short-stay demand can be interrupted by regulation, platform changes, a tourism downturn or simply more competing listings, whereas long-term residential demand is far more stable. If it works as a long-term rental, short-stay income is genuine upside. If it only works as short-stay, you are carrying a mortgage against a single volatile income stream."),
    ],
    "healthy-homes-standards-lending-nz": [
        ("Should I do compliance work before or after tenanting?",
         "Completing the work before tenanting gives the cleanest execution but means carrying the mortgage with no income for that period. Buying with a tenant in place keeps income flowing but makes scheduling harder and some work impractical. Negotiating the work as a vendor condition before settlement is usually the best outcome where the vendor agrees, though it will generally be reflected in the price. Whichever route you take, build the vacancy or the cost into your serviceability honestly."),
        ("Do Healthy Homes problems signal bigger issues?",
         "Often yes. A property failing the moisture and drainage standard may have poor subfloor ventilation causing rot in bearers and joists, drainage discharging against foundations, or gutters that have been overflowing long enough to damage cladding or framing. Those are valuation and sometimes insurability matters, not just compliance ones, so it is worth having a builder identify the underlying cause rather than quoting the minimum fix."),
    ],
    "student-loan-mortgage-borrowing-power-nz": [
        ("What changes if I go overseas with a student loan?",
         "Obligations change when you stop being New Zealand-based. Overseas-based borrowers face a different repayment basis, generally set as fixed amounts based on the loan balance rather than a share of income, and interest applies to the loan unlike the interest-free treatment for New Zealand-based borrowers. If you are returning, arrears accumulated while away can be substantial and affect your credit position, so resolve the loan status with Inland Revenue before applying."),
        ("What should I do before my student loan to increase borrowing power?",
         "Reduce or cancel unused credit card and overdraft limits first, since lenders assess these against the limit rather than the balance and it costs you nothing. Then clear short-term consumer debt with high repayments relative to balance, close BNPL facilities and build three to four clean months of statements, and grow the deposit. The student loan is usually the last lever to pull, not the first."),
    ],
    "afterpay-bnpl-mortgage-application-nz": [
        ("What else on my bank statements will a lender notice?",
         "Gambling transactions, which most lenders treat seriously, particularly where frequent or escalating. Also dishonoured payments and overdraft fees, payday or short-term high-cost lending, regular repayments to a lender you did not disclose, living expenses well above your declared figure, and large unexplained deposits which attract source-of-funds questions. Ordinary spending is unremarkable — what matters is whether the account shows a consistent surplus and no signs of stress."),
        ("How should I declare my living expenses?",
         "Work out your actual monthly spending from three months of statements before filling in any application, and declare that figure rather than an optimistic one. Lenders apply benchmark household expense figures and compare them against both your declared costs and your statements, generally using the higher. Understating achieves nothing except damaging your credibility, and an application where declared expenses match the statements reads as competent and honest."),
    ],
    "car-loan-personal-debt-borrowing-power-nz": [
        ("Does interest-free store finance still count against me?",
         "Yes. Interest-free terms mean you pay no interest, but it remains a contracted term debt with a monthly repayment, it appears on your credit file in most cases, and lenders assess the repayment like any other. The same applies to mobile plans with a handset component, furniture and appliance finance, fixed-term service contracts, and vehicle leases. Declare all of it, because undeclared commitments that appear on statements call the rest of your application into question."),
        ("Is there a downside to closing my credit cards?",
         "Closing your oldest credit account can slightly affect your credit file, because length of credit history is one factor in a score. In practice the serviceability gain from removing a large limit almost always outweighs that. If you hold several cards, a reasonable approach is to keep the oldest one with a small limit and close the rest, and get written confirmation of each closure for your broker."),
    ],
    "mortgage-on-parental-leave-nz": [
        ("What if I am returning part-time rather than full-time?",
         "State the actual return hours and pay from the outset. A return-to-work letter claiming full-time hours when you plan three days a week creates a credibility problem if the lender verifies it, and budgeting on full-time income produces an approval you cannot comfortably service. The offsetting point is that fewer work days also means less childcare cost, so the honest figures often work better than people expect."),
        ("What makes a parental leave application strongest?",
         "A specific return-to-work letter, pre-leave payslips covering at least three months, your most recent IRD income summary to corroborate the pre-leave figure, evidence of current parental leave payments and any employer top-up, your partner's full income documentation on a joint application, a written childcare plan with actual quoted costs and any confirmed subsidy, and bank statements showing you have managed the reduced-income period without dishonours or overdraft reliance."),
    ],
    "casual-part-time-seasonal-income-mortgage-nz": [
        ("What should my bank statements show if my income is irregular?",
         "Deliberate saving through the peak period, which is the single most persuasive behaviour you can demonstrate, controlled drawdown of those savings through the lean period rather than reliance on credit, no dishonours or overdraft dependence in the off-season, and no short-term or payday lending bridging the gaps between seasons. If your recent statements do not look like this, the fix is behavioural and takes a few months."),
        ("How are fixed-term contracts and labour-hire work assessed?",
         "The income may be regular and substantial, but the engagement has an end date, which is what concerns a lender. What helps is a history of successive contracts, ideally with the same client or agency, a current contract with as much remaining term as possible, evidence of demand in your field and your own record of continuous engagement, and where available a letter indicating intention to renew. Lender appetite varies considerably here."),
    ],
    "non-resident-offshore-income-mortgage-nz": [
        ("What documents should I start gathering early?",
         "Identity verification to New Zealand anti-money-laundering standards, often requiring certified copies, two years of overseas tax returns and assessments with certified translations where not in English, overseas payslips and employment contracts, overseas bank statements, overseas credit reports where you have no New Zealand credit history, evidence of your visa or residency status, and a full source-of-funds trail for the deposit. Obtaining translations and overseas tax documents commonly takes weeks."),
        ("What tax issues apply if I own NZ property from overseas?",
         "Rental income from a New Zealand property is taxable here with withholding and filing obligations for non-resident owners. The bright-line test applies to residential property sales within the relevant period, and the main home exclusion generally will not assist if you are not living in it. Residential land withholding tax can apply on sale by an offshore person, and double tax agreements may affect treatment. Take specialist cross-border advice before buying."),
    ],
    "pre-approval-expired-nz": [
        ("What is the difference between an indicative and a fully assessed pre-approval?",
         "An indicative or system-generated pre-approval rests on information you supplied, often online, with limited verification, and a lender can revise it substantially once documents are assessed. A fully assessed pre-approval has had your income, expenses and credit verified by a credit assessor, making it far more reliable and much quicker to renew. Ask explicitly which you hold, what conditions attach, and when it expires."),
        ("What does a pre-approval not cover?",
         "It generally does not confirm that the lender will accept a particular property as security — apartment size, title type, hazard exposure, unconsented work and rural land can all cause a property-specific decline. It also does not cover the valuation, insurability, or your interest rate at drawdown unless a specific rate lock applies. That is why a finance condition remains necessary even with a current pre-approval in hand."),
    ],
}

for _post in POSTS:
    _post["faqs"] = _post["faqs"] + EXTRA_FAQS.get(_post["slug"], [])
