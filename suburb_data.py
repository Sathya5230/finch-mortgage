"""Auckland suburb data for locations/mortgage-broker-{suburb}.html (added November 2026).

Same shape and rules as town_data.TOWNS: verifiable local facts and general
lending practice only. No prices, populations, rates or claims about Finch's
client history. Finch's office is in Te Atatu South, so these are the pages
where "local" is literally true.

Suburbs that already have a blog/mortgage-broker-{suburb} page (Henderson,
Te Atatu, Massey, New Lynn, Hobsonville, Albany, Glenfield, Takapuna, Howick,
Botany, Flat Bush, Mt Roskill, Manukau, Papakura) are deliberately left out so
the two sets don't compete.

Coordinates: OpenStreetMap Nominatim, November 2026.
"""


def S(slug, name, hub, district, near, tags, note, faqs, prose=None):
    return {"slug": slug, "name": name, "region": "auckland", "council": "auckland",
            "hub": hub, "near": near, "tags": tags, "note": note, "faqs": faqs,
            "district": district, "prose": prose or name, "kind": "suburb"}


W, C, E, SA, N, HC = ("west-auckland", "auckland-city", "east-auckland",
                      "south-auckland", "north-shore", "orewa-hibiscus-coast")

SUBURBS = [
    # ---------------------------------------------------------------- West
    S("avondale", "Avondale", W, "Whau", "Rosebank, Waterview, New Windsor and Kelston", {
        "apartments": "Apartment blocks have gone up around the Avondale town centre and along Great North Road.",
        "crosslease": "Cross-leased units and half-shares are common on Avondale's older streets.",
        "townhouses": "Terraced housing has replaced many single houses on larger Avondale sites.",
        "commuter": "the city centre on the Western Line or the Northwestern Motorway",
    }, [
        "Avondale sits on the Western Line between New Lynn and Mt Albert, with the Whau River on one side and the racecourse, home of the Sunday market, in the middle. It has changed quickly. Older bungalows on full sections now sit beside terraces and apartment blocks, and more are planned around the town centre.",
        "For lending, that mix matters more than the postcode. A 1950s house on a full section, a cross-leased unit and a new 45-square-metre apartment can be on the same street, and a lender treats each one differently. Our office is close by in Te Atatu South, and telling them apart early saves a declined application.",
    ], [
        ["Will a bank lend on a small apartment in Avondale?",
         "It depends on the size and the building. Lenders set their own minimum floor areas and look at the body corporate's finances. Send us the listing before you offer and we'll tell you which lenders will consider it and what deposit they'd want.", "apartments"],
        ["Can I buy a cross-leased unit in Avondale with a low deposit?",
         "Often, yes. Lenders treat a tidy cross-lease much like a freehold house. The thing to check is that the building matches the flats plan on the title, because an unconsented deck or extension can hold up the loan.", "crosslease"],
    ]),
    S("glen-eden", "Glen Eden", W, "Waitākere Ranges", "Kaurilands, Konini, Sunnyvale and Oratia", {
        "older_homes": "Much of Glen Eden was built between the 1950s and 1970s, on sections big enough to have since been divided.",
        "crosslease": "Infill over the decades has left Glen Eden with plenty of cross-leased and rear-lot homes.",
        "commuter": "the city on the Western Line, or Henderson and New Lynn by road",
        "subdivide": "Glen Eden's larger sections still attract owners looking to add a second dwelling.",
    }, [
        "Glen Eden runs from its Western Line station up into the Waitākere foothills. Near the shops the land is flat and the houses are mostly mid-century weatherboard and brick. Head towards Kaurilands and Konini and the sections get steeper and bushier.",
        "Glen Eden suits first home buyers, who often arrive with a 10% deposit made up partly of KiwiSaver. Older houses mean building reports matter. A lender will want to know about the roof, the piles and any moisture before it commits.",
    ], [
        ["Do lenders treat the bush sections above Glen Eden differently?",
         "Sometimes. Steep sites, pole foundations and properties inside the Waitākere Ranges Heritage Area can need a registered valuation and a closer look at insurance. Most are financed without trouble, but check before you go unconditional."],
    ]),
    S("titirangi", "Titirangi", W, "Waitākere Ranges", "Woodlands Park, Laingholm, Green Bay and French Bay", {
        "flood": "The storms of early 2023 caused slips on a number of properties around Titirangi and the Waitākere foothills.",
        "heritage": "Titirangi lies within the Waitākere Ranges Heritage Area, which limits subdivision and protects the bush.",
        "older_homes": "Many Titirangi homes are 1960s to 1980s builds on pole foundations, with decks and timber cladding that need upkeep.",
        "coastal": "Properties above the Manukau Harbour at French Bay and Laingholm can carry coastal erosion or instability notations.",
    }, [
        "Titirangi is bush, steep driveways and harbour views. The village sits on the ridge and the houses step down through the trees towards the Manukau. Out towards Laingholm and Woodlands Park some properties rely on tank water or on-site wastewater.",
        "Lenders like Titirangi well enough, but they read the paperwork carefully. Land stability is the big one since the 2023 storms. A LIM that mentions a slip, or an insurer that has changed its terms, changes the conversation. We check both before recommending a lender, so you don't find out at the valuation.",
    ], [
        ["Can I get a mortgage on a Titirangi house that had a slip in 2023?",
         "Usually, if the damage has been repaired and signed off, and an insurer will give full replacement cover. Lenders will want the engineering reports and any Natural Hazards Commission claim closed. Where land is still unstable, lender choice narrows a lot.", "flood"],
        ["Does tank water or a septic system affect lending in Laingholm?",
         "Not with most lenders, as long as the systems are consented and working. A valuer will note them, and some lenders ask for evidence of recent servicing."],
    ]),
    S("kumeu", "Kumeū", W, "Rodney", "Huapai, Riverhead, Waimauku and Taupaki", {
        "flood": "The Kumeū River flooded the town centre in August 2021 and again in early 2023.",
        "newbuild": "in the subdivisions around Huapai",
        "lifestyle": "around Taupaki, Waimauku and Riverhead",
        "commuter": "Westgate and the city along State Highway 16",
    }, [
        "Kumeū and Huapai have grown into one town along State Highway 16, with new subdivisions on the Huapai side and vineyards, orchards and lifestyle blocks all around. It's straight up the highway from our office in Te Atatu South.",
        "Two things come up in nearly every Kumeū loan. One is flooding. Parts of the town have been under water twice in recent years, and lenders and insurers now look hard at where exactly a property sits. The other is land size. A house in a Huapai subdivision is standard lending. A four-hectare block at Taupaki isn't, and the list of willing lenders is shorter.",
    ], [
        ["Will a lender finance a house in Kumeū that's in a flood area?",
         "It depends on the property and the insurer. Lenders need full replacement insurance before they'll settle, so get an insurance quote for the exact address first. Homes outside the flood plain are financed normally.", "flood"],
        ["How much deposit do I need for a lifestyle block near Kumeū?",
         "More than for a house in town with most lenders, and it rises with land size. Lenders treat a block as residential only up to a set area. Tell us the size and what's on it and we'll check which lenders fit.", "lifestyle"],
    ], prose="Kumeū and Huapai"),
    S("westgate", "Westgate", W, "Henderson-Massey", "Whenuapai, Red Hills, West Harbour and Royal Heights", {
        "newbuild": "at Red Hills, Whenuapai and around the Westgate town centre",
        "townhouses": "Most new housing around Westgate and Red Hills is terraced or duplex.",
        "defence": "RNZAF Base Auckland at Whenuapai is a major local employer.",
        "commuter": "the city on the Northwestern Motorway, or the North Shore on the Upper Harbour Motorway",
    }, [
        "Westgate was farmland not long ago. Now it has the NorthWest shopping centre, Costco and thousands of new homes spreading through Red Hills and Whenuapai, with the Northwestern and Upper Harbour motorways meeting beside it.",
        "Nearly everything for sale is new or close to it, which shapes the lending. New builds are exempt from the Reserve Bank's loan-to-value restrictions, so a 10% deposit goes further here than in older suburbs. The catch is timing: if you buy off the plans, your finance is confirmed when the house is finished, not when you sign.",
    ], [
        ["Can I buy a new townhouse at Westgate or Red Hills with a 10% deposit?",
         "Often, yes. Many lenders accept a 10% deposit on a new build. You still need to pass the income tests, and the bank values the home at completion, so keep a buffer in case the valuation comes in under the contract price.", "newbuild"],
        ["I'm posted to Whenuapai. Should I buy or rent?",
         "That's your call, but we can show you the numbers. If a later posting would turn the home into a rental, we set the loan up with that in mind from the start, so the change is simple when it comes.", "defence"],
    ], prose="Westgate and Whenuapai"),

    # ------------------------------------------------------------- Central
    S("mt-albert", "Mt Albert", C, "Albert-Eden", "Ōwairaka, Sandringham, St Lukes and Morningside", {
        "heritage": "Parts of Mt Albert are covered by special character rules that protect its villas and bungalows.",
        "crosslease": "Cross-leased units, often two or three to a section, are scattered through Mt Albert.",
        "apartments": "Large apartment and terrace developments are under way on the former Unitec land at Carrington.",
        "commuter": "the city centre on the Western Line",
    }, [
        "Mt Albert wraps around its volcanic cone, Ōwairaka, with two Western Line stations and St Lukes at its edge. The streets are a mix of 1920s bungalows, older villas and units from the 1960s and 70s, and the old Unitec campus is being turned into a new neighbourhood.",
        "If you're trading up from a first home, the timing of the two sales is the hard part. The choices are bridging finance, a long settlement, or selling first. The character homes are lovely and they cost money to maintain. A lender won't mind the age. It will mind rot, old wiring or a roof at the end of its life.",
    ], [
        ["Can I buy my next home in Mt Albert before I sell my current one?",
         "Yes. Bridging finance covers the gap, and some lenders will lend against an unconditional sale. It costs more than a standard loan, so we keep the bridge short and have the long-term loan approved alongside it."],
    ]),
    S("mt-eden", "Mt Eden", C, "Albert-Eden", "Balmoral, Three Kings, Eden Terrace and Kingsland", {
        "heritage": "Much of Mt Eden sits under special character rules, and villas and bungalows dominate its streets.",
        "apartments": "Apartments cluster along Dominion Road, Mt Eden Road and down at Eden Terrace.",
        "investor": "Units and apartments close to the city draw investors as well as owner-occupiers.",
        "older_homes": "Mt Eden's villas are mostly more than a century old, and renovating them is a local pastime.",
    }, [
        "Mt Eden takes its name from Maungawhau, the cone at its centre. Around the village the streets are lined with villas and bungalows. Towards Eden Terrace and along Dominion Road there are apartments, some new and some from the 1990s and 2000s.",
        "That split matters. Lenders are relaxed about a villa on its own title. With apartments they want the floor area, the title type and the body corporate records, and for buildings of a certain age, evidence that any weathertightness work has been done and paid for. We ask for the disclosure statement before anything else.",
    ], [
        ["Do banks lend on older Mt Eden apartments?",
         "Yes, on most. What they check is the building: its size, whether the title is freehold or leasehold, the body corporate's maintenance fund and any remediation history. An apartment with unresolved building issues is hard to finance until the work is complete.", "apartments"],
        ["Can I borrow to renovate a Mt Eden villa?",
         "Usually. Cosmetic work can be funded with a top-up. Structural work is more like a construction loan, lent against the finished value and paid out in stages, and character rules can affect what the council will consent."],
    ]),
    S("epsom", "Epsom", C, "Albert-Eden", "Greenlane, Newmarket, One Tree Hill and Royal Oak", {
        "crosslease": "Epsom has many cross-leased units and townhouses, built when large sections were divided.",
        "subdivide": "Epsom's big sections have been steadily subdivided, and plenty of owners still look at adding a dwelling.",
        "older_homes": "Large early-twentieth-century homes are typical of Epsom's older streets.",
        "investor": "Units close to Newmarket and Greenlane are popular as rentals.",
    }, [
        "Epsom sits between Maungawhau and Maungakiekie, and much of it falls inside the zones for Auckland Grammar and Epsom Girls Grammar. That keeps demand steady, and it means families often stretch to buy here.",
        "Stretching is where we come in. Larger loans run into the Reserve Bank's debt-to-income limits sooner, and lenders differ on how they count bonuses, commission and business income. A well-chosen lender can add a meaningful amount to what you can borrow. For units, check the cross-lease plan matches what's built.",
    ], [
        ["How do debt-to-income limits affect buying in Epsom?",
         "Banks are restricted in how much they can lend above six times your gross income for a home you'll live in. On higher-priced homes that limit bites earlier. Each bank has some room for exceptions and counts income differently, so comparing lenders is worth it."],
    ]),
    S("remuera", "Remuera", C, "Ōrākei", "Meadowbank, Newmarket, Ōrākei and Upland Road", {
        "subdivide": "Remuera's large sections have long been subdivided, and rear-lot development is common.",
        "crosslease": "Many Remuera units and townhouses are on cross-lease titles.",
        "older_homes": "Remuera has some of Auckland's largest older homes, and they're expensive to maintain and insure.",
        "retirement": True,
    }, [
        "Remuera runs along the ridge above Hobson Bay and the Ōrākei Basin. The houses on the northern slopes are large and old. Tucked behind and between them are units, townhouses and newer homes on subdivided sites.",
        "Loans here tend to be big, and big loans are assessed differently. Lenders may want a registered valuation where they'd accept an estimate elsewhere, they look closely at how income is earned, and some send larger applications to a senior credit team. If a trust or company owns the property, add documents and time.",
    ], [
        ["Is it harder to get a large home loan?",
         "Not harder, but more detailed. Lenders often require a full registered valuation, apply debt-to-income limits and look closely at self-employed or investment income. Presenting the application well at the start saves weeks."],
        ["We want to downsize within Remuera. How does the lending work?",
         "If you're buying before selling, bridging finance covers the overlap. If the new home costs less, you may end up with little or no loan, and lenders will want to see how any remaining debt is repaid.", "retirement"],
    ]),
    S("ponsonby", "Ponsonby", C, "Waitematā", "Grey Lynn, Freemans Bay, Herne Bay and Westmere", {
        "heritage": "Ponsonby and Grey Lynn hold much of Auckland's oldest housing, and special character rules protect large parts of both.",
        "older_homes": "Villas and workers' cottages here are often more than 110 years old, on small sites.",
        "apartments": "Apartments line the Ponsonby Road ridge and Great North Road.",
        "investor": "Proximity to the city makes the area popular with investors.",
    }, [
        "Ponsonby and Grey Lynn are the villa suburbs: narrow streets, small sections and houses built before the First World War. Most have been renovated at least once. Along the ridges, apartment buildings have filled in the gaps.",
        "A renovated villa is easy to finance. An unrenovated one needs a careful building report, because lenders and insurers ask about piles, wiring and scrim linings. Many buyers here plan to renovate soon after buying, so we often set up the loan with the renovation in mind and check what the council's character rules allow.",
    ], [
        ["Will a bank lend on an unrenovated Ponsonby villa?",
         "Generally, yes, if it's liveable and insurable. The lender needs full replacement insurance, and insurers ask about wiring, plumbing and roof condition in very old homes. Get the building report and an insurance quote before you bid.", "older_homes"],
    ], prose="Ponsonby and Grey Lynn"),
    S("onehunga", "Onehunga", C, "Maungakiekie-Tāmaki", "Royal Oak, Te Papapa, Penrose and Hillsborough", {
        "townhouses": "Terraced housing has been built across Onehunga's former industrial and larger residential sites.",
        "older_homes": "Onehunga has streets of villas and bungalows dating from its days as a separate port borough.",
        "commuter": "the city on the Onehunga Line, or the airport and Manukau across the Māngere Bridge",
        "coastal": "Low-lying land near the Manukau Harbour foreshore can carry coastal inundation notations.",
    }, [
        "Onehunga was a port town before it was a suburb, and it still has its own main street, a train line and the Manukau Harbour at the bottom of the hill. Villas sit beside new terraces, with light industry towards Penrose.",
        "First home buyers like it for the mix of prices. The terraces are usually straightforward new-build lending. With them, check the title: some are freehold, some are unit titles with a body corporate, and some have a residents' society with annual levies. Lenders count those levies as a cost, so they affect what you can borrow.",
    ], [
        ["Do body corporate or residents' society fees affect my home loan?",
         "Yes. Lenders include them in your regular outgoings, so higher fees reduce your borrowing power slightly. They also check the body corporate is solvent and the building is properly insured.", "townhouses"],
    ]),
    S("ellerslie", "Ellerslie", C, "Ōrākei", "Greenlane, Penrose, Mt Wellington and St Johns", {
        "newbuild": "on the former racecourse hill land and on infill sites around the village",
        "townhouses": "New terraces and apartments are replacing single houses on larger Ellerslie sites.",
        "commuter": "the city on the Southern Line or the Southern Motorway",
        "crosslease": "Cross-leased units from the 1970s and 80s are common around Ellerslie village.",
    }, [
        "Ellerslie is a village suburb beside the Southern Motorway, with a station on the Southern Line and the racecourse next door. Part of the racecourse land is being developed for housing, adding new homes to an area of bungalows and units.",
        "People buy here for the commute, and many are couples on two professional incomes. That makes the lending simple on paper. The usual sticking point is other debt. A car loan and a couple of credit card limits can take a large slice off borrowing power, so we look at clearing them before applying.",
    ], [
        ["Should I pay off my car loan before applying for a mortgage?",
         "Often it's worth it. Lenders count the repayment against your income, and a few hundred dollars a month can reduce your borrowing by far more than the balance of the loan. We run the numbers both ways first."],
    ]),
    S("panmure", "Panmure", C, "Maungakiekie-Tāmaki", "Mt Wellington, Stonefields, Glen Innes and Point England", {
        "newbuild": "through the Tāmaki regeneration area in Glen Innes, Point England and Panmure",
        "townhouses": "Stonefields, built in the former Mt Wellington quarry, is almost entirely terraces and apartments.",
        "commuter": "the city on the Eastern Line, or Pakuranga and Botany on the Eastern Busway",
        "investor": "New-build terraces around Tāmaki attract investors, who face a lower deposit requirement on new homes.",
    }, [
        "Panmure sits beside its tidal basin with a rail and busway interchange at the centre. To the north, state housing in Glen Innes and Point England is being rebuilt at higher density through the Tāmaki regeneration programme. To the west, Stonefields fills the old quarry.",
        "Much of what's for sale is new, and some of it comes with schemes attached, such as shared ownership offered through the regeneration programme. Those arrangements involve specific lenders and extra documents. If you're looking at one, talk to us before signing so we can check who will lend on it.",
    ], [
        ["Can I get a mortgage for a shared ownership home in Tāmaki?",
         "Yes, but only some lenders take part in shared ownership schemes, and the provider usually has a list. We'll tell you whether a lender on our panel can do it or point you to one that can."],
    ], prose="Panmure and Mt Wellington"),
    S("st-heliers", "St Heliers", C, "Ōrākei", "Kohimarama, Mission Bay, Glendowie and Ōrākei", {
        "coastal": "Tāmaki Drive and the lowest parts of the bays are exposed to coastal flooding in storms and king tides.",
        "apartments": "Apartment buildings and units front the beaches at Mission Bay, Kohimarama and St Heliers.",
        "retirement": True,
        "crosslease": "Cross-leased units are common on the slopes behind the bays.",
    }, [
        "St Heliers, Kohimarama and Mission Bay follow Tāmaki Drive along the Waitematā. Apartments and units face the water, with houses on the hills behind. Many owners have been here for decades, and plenty of buyers are downsizing from larger homes nearby.",
        "Downsizers often buy with little or no mortgage. When they do borrow, lenders ask how the loan will be repaid after retirement, and a clear answer gets it approved. For waterfront apartments, the building's age and insurance come first. Some of the older blocks have had significant remediation.",
    ], [
        ["Can I get a home loan in my late 60s to buy an apartment in the bays?",
         "Yes, with many lenders. They'll want to see how repayments are met from retirement income or how the loan is cleared, for instance from the sale of your current home. A smaller loan with a defined end date is the easiest to approve.", "retirement"],
    ], prose="St Heliers and the eastern bays"),
    S("point-chevalier", "Point Chevalier", C, "Albert-Eden", "Western Springs, Waterview, Westmere and Carrington", {
        "older_homes": "Point Chevalier is known for its 1920s and 30s bungalows.",
        "crosslease": "Cross-leases are common where bungalow sections were split from the 1960s on.",
        "coastal": "Clifftop and low-lying properties around the peninsula can carry coastal erosion or inundation notations.",
        "commuter": "the city on the Northwestern Motorway and cycleway",
    }, [
        "Point Chevalier is a peninsula of Californian bungalows pointing into the Waitematā, with Coyle Park at the tip and the Northwestern Motorway at its base. It's just across the causeway from our office in Te Atatu South.",
        "Families tend to buy here and stay, so sales are often to people upgrading from a smaller place. That means two transactions to line up. If you'd like to buy first, we arrange bridging finance. If you'd rather sell first, we get a pre-approval ready so you can move quickly when the house you want appears.",
    ], [
        ["Do lenders mind a cross-lease in Point Chevalier?",
         "No, cross-leases are routine. The lender's lawyer checks that the house matches the flats plan on the title. If a previous owner added a room or a garage without updating the plan, it should be fixed before or as part of the purchase.", "crosslease"],
    ]),
    S("blockhouse-bay", "Blockhouse Bay", C, "Whau", "Lynfield, New Windsor, Green Bay and Avondale South", {
        "older_homes": "Blockhouse Bay is largely 1950s and 60s weatherboard and brick-and-tile housing.",
        "crosslease": "Many of its sections were divided for a second unit, leaving a lot of cross-lease titles.",
        "subdivide": "Sloping sections with room at the back still draw owners interested in building a second home.",
        "commuter": "the city via New North Road, or New Lynn's train station",
    }, [
        "Blockhouse Bay slopes down to the Manukau Harbour, with a village of shops at the top and a beach reserve at the bottom. Most of the housing is solid mid-century stock on decent sections.",
        "If you bought here years ago, you've probably built up equity, and you may be thinking about renovating or helping your children buy. Equity can do both. A top-up funds the renovation, and a limited guarantee over part of your equity can stand in for a child's deposit.",
    ], [
        ["Can I use the equity in my Blockhouse Bay home to help my child buy?",
         "Yes. You can gift money raised by a top-up, or give a limited guarantee secured against your home. A guarantee puts your property at risk if they can't pay, so lenders require you to get independent legal advice."],
    ]),
    S("waiheke-island", "Waiheke Island", C, "Waiheke", "Oneroa, Ostend, Onetangi, Surfdale and Palm Beach", {
        "holiday": "across the island, from Oneroa to Onetangi",
        "remote": True,
        "coastal": "Clifftop and beachfront sites around Waiheke can carry coastal erosion and instability notations.",
        "older_homes": "Many Waiheke houses began as baches and have been extended over the years, not always with consent.",
    }, [
        "Waiheke is part of Auckland and a 40-minute ferry from downtown, but it lends like somewhere further away. Homes run on tank water and on-site wastewater, building costs are higher, and a good share of the housing is holiday homes or short-stay rentals.",
        "Lenders vary on the island. Some treat it as standard Auckland. Others cap the loan-to-value ratio lower or decline certain properties. Short-stay income is counted by some and ignored by others. And old baches with unconsented additions are common enough that a careful LIM check is essential.",
    ], [
        ["Do banks lend on Waiheke Island the same as the rest of Auckland?",
         "Not all of them. Some apply standard terms, and others want a bigger deposit or restrict the property types they'll accept. We check each lender's policy for the island before you apply.", "remote"],
        ["Will a lender count Airbnb income from a Waiheke property?",
         "Some will count part of it if there's a track record, some assess it at a long-term rental figure, and some won't count it. If the income is needed to make the loan work, lender choice is everything."],
    ]),

    # ---------------------------------------------------------------- East
    S("pakuranga", "Pakuranga", E, "Howick", "Pakuranga Heights, Sunnyhills, Farm Cove and Highland Park", {
        "crosslease": "Pakuranga has a great many cross-leased brick-and-tile units from the 1970s.",
        "older_homes": "Most of Pakuranga was built in the 1960s and 70s.",
        "commuter": "Panmure station and the city on the Eastern Busway",
        "townhouses": "Terraced housing is replacing single houses on sites near the busway.",
    }, [
        "Pakuranga lies between the Tāmaki River and Howick. It was built in a hurry in the 1960s and 70s, mostly as brick-and-tile family homes and units. The Eastern Busway now links it to the train at Panmure and is being extended towards Botany.",
        "Brick-and-tile units on cross-lease titles make good first homes, and lenders are comfortable with them. The busway has also brought developers, so some buyers are choosing between an older unit and a new terrace. The deposit rules differ: new builds can be bought with less.",
    ], [
        ["Is it easier to get a loan for a new terrace or an older unit in Pakuranga?",
         "They're assessed the same way on income. On deposit, a new build can be easier, because new builds are exempt from the Reserve Bank's loan-to-value restrictions and more lenders accept 10%. An older unit usually needs 20% unless you qualify for a low-deposit allocation."],
    ]),
    S("beachlands", "Beachlands", E, "Franklin", "Maraetai, Whitford, Pine Harbour and Clevedon", {
        "newbuild": "in the subdivisions on the edges of Beachlands",
        "commuter": "the city by ferry from Pine Harbour",
        "lifestyle": "around Whitford and Clevedon",
        "coastal": "Clifftop and beachfront sites at Beachlands and Maraetai can carry coastal erosion notations.",
    }, [
        "Beachlands and Maraetai were bach settlements on the Pōhutukawa Coast. They're now commuter towns, with a ferry to the city from Pine Harbour and new subdivisions pushing out from the old streets. Inland, Whitford and Clevedon are lifestyle-block country.",
        "People often move here from closer-in suburbs for more house and a beach. That usually means selling one home and buying another, sometimes building. The lending needs to match the plan: a standard loan for an existing house, a construction loan for a build, and a different set of lenders if the land is more than a hectare or two.",
    ], [
        ["Can I build in Beachlands with a 10% deposit?",
         "Possibly. New builds are exempt from the Reserve Bank's loan-to-value restrictions, so some lenders accept 10% on a fixed-price build contract. Lenders pay out in stages as the build progresses and want a contingency in the budget.", "newbuild"],
    ], prose="Beachlands and Maraetai"),

    # --------------------------------------------------------------- South
    S("mangere", "Māngere", SA, "Māngere-Ōtāhuhu", "Māngere Bridge, Māngere East, Favona and Ihumātao", {
        "flood": "Parts of Māngere were badly flooded in January 2023, and flood-reduction work on its streams has followed.",
        "newbuild": "across the Māngere Development, where older state houses are being replaced",
        "townhouses": "New terraced homes are now a large part of what's for sale in Māngere.",
        "commuter": "the airport precinct, Manukau and the city",
    }, [
        "Māngere stretches from the village at Māngere Bridge to the airport. A large redevelopment is replacing old state houses with new homes, a share of them sold to first home buyers.",
        "Buying together is common here: parents and adult children, or siblings pooling incomes and KiwiSaver. Lenders are fine with several borrowers on one loan. Everyone's income counts, and so do everyone's debts. It's worth agreeing in writing who owns what share before you buy. After January 2023, check the flood maps for the exact address and get an insurance quote early.",
    ], [
        ["Can three or four family members buy a house together in Māngere?",
         "Yes. Lenders assess all borrowers together and each is liable for the whole loan. More incomes can mean more borrowing power, though every person's debts and credit history count too. A lawyer can record each person's share.", "townhouses"],
        ["Does the 2023 flooding affect getting a mortgage in Māngere?",
         "Only for affected properties. Lenders need full replacement insurance, so the insurer's view of the address decides it. Most Māngere homes are financed without any issue.", "flood"],
    ]),
    S("otahuhu", "Ōtāhuhu", SA, "Māngere-Ōtāhuhu", "Middlemore, Māngere East, Favona and Mt Richmond", {
        "older_homes": "Ōtāhuhu has streets of villas and bungalows, older than most of South Auckland's housing.",
        "townhouses": "Terraces are being built on larger sites near the station and town centre.",
        "commuter": "the city or Manukau by train from the Ōtāhuhu interchange",
        "investor": "Older houses on big sections draw investors and small developers.",
    }, [
        "Ōtāhuhu sits on the narrowest part of the Auckland isthmus, between the Tāmaki River and the Manukau Harbour. It has one of the city's busiest bus and train interchanges, a long main street, and industry on three sides.",
        "The housing is older than in neighbouring suburbs, and the sections are larger. That appeals to buyers planning to add a dwelling. Building at the back is construction lending, with consented plans and a fixed-price contract, not a simple top-up. For buyers who just want a home, older houses mean a building report is money well spent.",
    ], [
        ["Can I buy in Ōtāhuhu and build a second house on the section?",
         "It can be done in two steps: a standard home loan to buy, then a construction loan once you have consent and a fixed-price contract. Lenders will want to see you can afford both loans, counting some of the expected rent."],
    ]),
    S("papatoetoe", "Papatoetoe", SA, "Ōtara-Papatoetoe", "Hunters Corner, Puhinui, Middlemore and Old Papatoetoe", {
        "crosslease": "Papatoetoe's large sections were widely split, so cross-lease and rear-lot titles are everywhere.",
        "subdivide": "Big flat sections make Papatoetoe a favourite for adding a second dwelling.",
        "commuter": "the city or Manukau by train, with Puhinui station linking to the airport",
        "older_homes": "Much of the housing dates from the 1950s to the 1970s.",
    }, [
        "Papatoetoe has two centres, Old Papatoetoe by the station and Hunters Corner on Great South Road, and flat streets of mid-century houses between them. Two train lines run through it, and Puhinui station connects to the airport.",
        "A point for self-employed buyers, whether you're a tradesperson, a driver or run a shop. Lenders will lend on self-employed income, but they want it shown properly, usually with two years of accounts. If your tax returns understate what the business really earns, that limits what you can borrow. It's better to know that a year before you buy than the week you find a house.",
    ], [
        ["I'm self-employed in Papatoetoe. What do I need for a home loan?",
         "Usually two years of financial statements and tax returns, plus recent bank statements. Some lenders accept one year if you were in the same trade before. Non-bank lenders can use other evidence, at a higher rate."],
    ]),
    S("manurewa", "Manurewa", SA, "Manurewa", "Clendon Park, Weymouth, Wattle Downs and The Gardens", {
        "investor": "Investors are active buyers in Manurewa, alongside first home buyers.",
        "older_homes": "Most Manurewa houses were built from the 1960s to the 1980s.",
        "commuter": "Manukau and the city on the Southern Line or Southern Motorway",
        "crosslease": "Cross-leased units are common in the older parts of Manurewa.",
    }, [
        "Manurewa covers a lot of ground, from the Botanic Gardens and The Gardens in the east to Weymouth and Wattle Downs on the Manukau Harbour. It has two stations on the Southern Line and quick access to the motorway.",
        "First home buyers and investors often go after the same houses here. If you're a first home buyer, a solid pre-approval lets you make a clean offer. If you're an investor, remember rentals need a bigger deposit and must meet the Healthy Homes standards, which lenders may ask about.",
    ], [
        ["How much deposit does an investor need to buy in Manurewa?",
         "More than an owner-occupier. The Reserve Bank's rules mean most lenders want around 30% for an existing rental property, though new builds are exempt and can need less. Lenders also count only part of the rent as income.", "investor"],
    ]),
    S("takanini", "Takanini", SA, "Papakura", "Conifer Grove, Longford Park, Ardmore and Alfriston", {
        "newbuild": "across the subdivisions east of the motorway",
        "townhouses": "Newer Takanini streets are a mix of standalone houses, duplexes and terraces.",
        "commuter": "Manukau and the city on the Southern Line or Southern Motorway",
        "lifestyle": "around Ardmore and Alfriston",
    }, [
        "Takanini has gone from horse-training paddocks to one of South Auckland's biggest areas of new housing. It has a station on the Southern Line and a motorway interchange, with rural land still running out to Ardmore.",
        "One local detail is the ground. Parts of Takanini are built on peat, which needs specially designed foundations. For a new house with code compliance, lenders don't treat that as a problem. For anything older or altered, the engineering and consent records matter, and a valuer will look for them.",
    ], [
        ["Does peat soil in Takanini affect getting a mortgage?",
         "Not for a consented new build with the right foundations and a code compliance certificate. Lenders and insurers rely on those documents. If you're buying an older house or one with additions, check the consents cover all the work."],
    ]),
    S("drury", "Drury", SA, "Papakura", "Auranga, Karaka, Rāmarama and Paerātā", {
        "newbuild": "at Auranga and the other new neighbourhoods around Drury",
        "lifestyle": "around Karaka, Rāmarama and Ararimu",
        "commuter": "Manukau and the city on the Southern Motorway",
        "townhouses": "New Drury neighbourhoods include a large share of terraces and duplexes.",
    }, [
        "Drury was a village at a motorway off-ramp. It's now one of Auckland's main growth areas, with thousands of homes planned or under way, new stations on the rail line to Pukekohe in the plans, and the motorway being widened. Karaka's lifestyle blocks and horse studs are next door.",
        "Most Drury purchases are house-and-land packages or turnkey builds. The contract is signed a long time before the house is finished, and the loan is confirmed at the end. A lot can change in a year. We set up the approval with the build timeline in mind, and tell you what to avoid doing with your finances until you've settled.",
    ], [
        ["I've signed a turnkey contract in Drury. When do I arrange the mortgage?",
         "Get a pre-approval before you sign, then renew it a few months before completion. The lender reassesses you at that point and values the finished house, so keep your job and debts stable while it's being built.", "newbuild"],
    ]),

    # --------------------------------------------------------------- North
    S("devonport", "Devonport", N, "Devonport-Takapuna", "Stanley Point, Cheltenham, Narrow Neck and Bayswater", {
        "heritage": "Devonport is one of Auckland's most intact Victorian and Edwardian suburbs, and special character rules cover most of it.",
        "defence": "The Royal New Zealand Navy's base at Devonport is the area's largest employer.",
        "coastal": "Low-lying streets and the waterfront are exposed to coastal flooding, and some cliff-edge sites to erosion.",
        "older_homes": "Most Devonport houses are villas well over a century old.",
    }, [
        "Devonport sits at the end of a peninsula, twelve minutes by ferry from the city, with two volcanic cones and street after street of villas. The naval base takes up the western shore.",
        "Old timber houses by the sea need insurance that's priced accordingly, and lenders won't settle without it. Get a quote before you bid. Navy families tend to go one of two ways: buy to live in and rent the house out when posted, or buy a rental elsewhere while living in service housing. Each needs a different loan set-up.",
    ], [
        ["I'm in the Navy at Devonport. Will lenders count my allowances?",
         "Most count regular, ongoing allowances along with base pay, though they differ on which ones and how much. We check that before choosing a lender, since it can change your borrowing power noticeably.", "defence"],
    ]),
    S("birkenhead", "Birkenhead", N, "Kaipātiki", "Northcote, Northcote Point, Chatswood and Birkdale", {
        "older_homes": "Birkenhead and Northcote Point have many early villas and bungalows, with 1960s and 70s homes further back.",
        "newbuild": "in the Northcote redevelopment, where old state houses are being replaced with new homes",
        "commuter": "the city across the Harbour Bridge, or by ferry from Birkenhead",
        "townhouses": "New terraces and apartments are concentrated around the Northcote town centre.",
    }, [
        "Birkenhead and Northcote are the first suburbs over the Harbour Bridge. Much of Birkenhead is steep and bush-clad, with houses on poles looking over the upper harbour. Northcote is flatter and is being substantially rebuilt.",
        "Steep bush sections are lovely and they attract questions. A valuer will look at access, retaining walls and drainage, and a lender may ask for a report if the LIM mentions instability. In Northcote the questions are about new builds: completion dates, titles and whether a development has a residents' society.",
    ], [
        ["Do lenders treat steep sections in Birkenhead differently?",
         "Only if there's a known problem. Lenders rely on the valuation and the LIM. If either mentions land instability or failing retaining walls, expect to be asked for an engineer's report and confirmation of insurance."],
    ], prose="Birkenhead and Northcote"),
    S("browns-bay", "Browns Bay", N, "Hibiscus and Bays", "Rothesay Bay, Torbay, Mairangi Bay and Murrays Bay", {
        "coastal": "Clifftop properties along the East Coast Bays can carry erosion and instability notations, and some were affected by slips in the 2023 storms.",
        "apartments": "Apartments and units are concentrated around the Browns Bay town centre and beachfront.",
        "retirement": True,
        "crosslease": "Cross-leased units and townhouses are common throughout the bays.",
    }, [
        "Browns Bay is the main centre of the East Coast Bays, with a beach, a full set of shops and a string of smaller bays either side. The housing ranges from 1960s family homes to beachfront apartments and a good number of units.",
        "Two groups do most of the buying. Families come for the schools and the beach and borrow a lot to do it. Downsizers sell a larger home nearby and buy a unit or apartment, often mortgage-free. For clifftop homes, the LIM and insurance come first. Since 2023, insurers have looked much more closely at land stability.",
    ], [
        ["Can I get a mortgage on a clifftop home in the East Coast Bays?",
         "Usually. Lenders need full replacement insurance and a satisfactory valuation. If the LIM records instability or past slips, they may ask for a geotechnical report, and some lenders will want a larger deposit.", "coastal"],
    ]),
    S("silverdale", "Silverdale", HC, "Hibiscus and Bays", "Millwater, Milldale, Dairy Flat and Red Beach", {
        "newbuild": "at Milldale and Millwater",
        "commuter": "Albany and the city on the Northern Motorway, or by bus from the Hibiscus Coast Station",
        "lifestyle": "around Dairy Flat, Wainui and Stillwater",
        "townhouses": "Milldale includes a growing share of terraced and duplex homes alongside standalone houses.",
    }, [
        "Silverdale has grown from a small service town into the centre of two very large subdivisions, Millwater and Milldale, either side of the Northern Motorway. Dairy Flat and Wainui, just inland, are lifestyle blocks.",
        "Most buyers here are building or buying new. If you're building on your own section, you'll have a construction loan paid out in stages, and you'll pay interest only on what's been drawn. If you're buying turnkey, you pay a deposit and settle at the end. The second is simpler. The first can cost less. We'll go through both with your figures.",
    ], [
        ["What's the difference between a turnkey loan and a construction loan?",
         "With turnkey you pay a deposit and borrow the balance when the home is complete. With a construction loan you borrow in stages as the build progresses and pay interest along the way. Turnkey is simpler, and a staged build gives you more control.", "newbuild"],
    ], prose="Silverdale and Millwater"),
    S("whangaparaoa", "Whangaparāoa", HC, "Hibiscus and Bays", "Gulf Harbour, Stanmore Bay, Manly, Army Bay and Arkles Bay", {
        "coastal": "With cliffs and beaches on both sides, many peninsula properties carry coastal erosion or instability notations.",
        "retirement": True,
        "commuter": "Albany and the city by road, or by ferry from Gulf Harbour",
        "holiday": "around Manly, Army Bay and Tindalls Beach",
    }, [
        "The Whangaparāoa Peninsula runs out into the Hauraki Gulf with a single main road along its spine, beaches on both coasts and Gulf Harbour marina near the end. O Mahurangi Penlink, a new road and bridge to the motorway, is being built to shorten the trip.",
        "The peninsula suits retirees and commuters alike, and both borrow here. For retirees it's usually a modest loan with a clear plan to repay it. For commuting families it's a larger loan on two incomes. For anything near a cliff edge, the LIM and insurer decide how easy the lending will be.",
    ], [
        ["Does living at the end of the peninsula affect lending?",
         "No. Lenders treat Whangaparāoa as standard Auckland residential. What can matter is a specific property's coastal hazard notation or insurance position, so check those early."],
    ], prose="the Whangaparāoa Peninsula"),
]

SUBURB_COORDS = {
    "avondale": ("-36.8967", "174.6970"), "glen-eden": ("-36.9146", "174.6537"),
    "titirangi": ("-36.9378", "174.6572"), "kumeu": ("-36.7753", "174.5547"),
    "westgate": ("-36.8216", "174.6073"), "mt-albert": ("-36.8842", "174.7156"),
    "mt-eden": ("-36.8816", "174.7620"), "epsom": ("-36.8858", "174.7735"),
    "remuera": ("-36.8759", "174.8014"), "ponsonby": ("-36.8502", "174.7421"),
    "onehunga": ("-36.9229", "174.7854"), "ellerslie": ("-36.8976", "174.8150"),
    "panmure": ("-36.8988", "174.8551"), "st-heliers": ("-36.8514", "174.8579"),
    "point-chevalier": ("-36.8665", "174.7081"), "blockhouse-bay": ("-36.9198", "174.7015"),
    "waiheke-island": ("-36.7851", "175.0191"), "pakuranga": ("-36.9152", "174.8745"),
    "beachlands": ("-36.8824", "174.9971"), "mangere": ("-36.9708", "174.7995"),
    "otahuhu": ("-36.9468", "174.8458"), "papatoetoe": ("-36.9797", "174.8526"),
    "manurewa": ("-37.0213", "174.8971"), "takanini": ("-37.0403", "174.9195"),
    "drury": ("-37.1021", "174.9518"), "devonport": ("-36.8297", "174.7975"),
    "birkenhead": ("-36.8099", "174.7251"), "browns-bay": ("-36.7156", "174.7482"),
    "silverdale": ("-36.6177", "174.6769"), "whangaparaoa": ("-36.6203", "174.7214"),
}
