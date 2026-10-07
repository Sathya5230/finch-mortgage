#!/usr/bin/env python3
"""Interest-rate posts for generate_local_intent_blogs.py.

Rewrites blog/will-mortgage-rates-drop-nz-2026.html at the same URL. The old page
said the OCR was 3.25% and that 2026 "definitively points towards" cuts; the Reserve
Bank actually held at 2.25% in April 2026, then raised to 2.50% (8 July) and 2.75%
(2 September). Update OCR_TIMELINE after each review — every rate claim in the post
comes from it.

Run:  python3 generate_local_intent_blogs.py rates_posts
"""

from generate_local_intent_blogs import callout, link, ol, p, table, ul

RBNZ_NEWS = "https://www.rbnz.govt.nz/news-and-events/news"
OCR_TIMELINE = [
    ("April 2026", "Held at 2.25%", RBNZ_NEWS + "/2026/04/ocr-on-hold-at-2-25"),
    ("8 July 2026", "Raised to 2.50%", RBNZ_NEWS + "/2026/07/ocr-increased-to-2-50-to-return-inflation-to-2-percent"),
    ("2 September 2026", "Raised to 2.75%", RBNZ_NEWS + "/2026/09/ocr-increased-by-25-basis-points-to-2-75"),
]
AS_AT = "early October 2026"
CURRENT_OCR = "2.75%"

POSTS = [
    {
        "slug": "will-mortgage-rates-drop-nz-2026",
        "published": "2026-10-07",
        "title": "Will NZ Mortgage Rates Go Up or Down in 2026? | Finch",
        "h1": "Will NZ Mortgage Rates Go Up or Down in 2026?",
        "section_label": "Interest Rates",
        "region": "",
        "lead_service": "Refinance",
        "about": ["Mortgage interest rates", "Official Cash Rate", "Fixed vs floating", "New Zealand home loans"],
        "intro_pull": f"After cutting rates through 2024 and 2025, the Reserve Bank started raising the OCR again in July 2026. As at {AS_AT} it sits at {CURRENT_OCR}. Here's what that means for your mortgage, and how to choose a fixed term without trying to predict the market.",
        "description": f"Will NZ mortgage rates rise or fall? The OCR is {CURRENT_OCR} after rises in July and September 2026. What it means for fixed rates, floating rates and your term.",
        "keywords": [
            "will mortgage rates drop NZ",
            "will interest rates go up NZ",
            "NZ mortgage rates forecast 2026",
            "OCR increase 2026",
            "should I fix my mortgage NZ",
            "mortgage rates rising NZ",
        ],
        "cta_heading": "Fixed term coming up?",
        "cta_sub": "Tell us when your fixed terms end and your loan balance. We'll compare current offers across lenders and suggest a fixed-term mix that suits you.",
        "sections": [
            ("Where the OCR is now", (
                p(f"The Official Cash Rate (OCR) is the Reserve Bank's main tool for controlling inflation. After a long run of cuts from August 2024, the Reserve Bank held the OCR at 2.25% in April 2026 and then began raising it as inflation picked up. As at {AS_AT}, it is <strong>{CURRENT_OCR}</strong>.")
                + table(["Decision", "OCR"], [[link(url, when), what] for when, what, url in OCR_TIMELINE])
                + p("The Reserve Bank has said it is gradually removing stimulus to bring inflation back towards the 2% midpoint of its 1–3% target range. Its decisions, statements and forecasts are published at " + link("https://www.rbnz.govt.nz/", "rbnz.govt.nz") + ".")
                + callout("The honest answer", "No one can say for certain where rates will go. Forecasts from banks and economists change with every inflation figure and OCR review. What you can control is how much rate risk your loan structure takes on.")
            )),
            ("How OCR changes reach your mortgage", (
                ul([
                    "<strong>Floating rates</strong> usually move soon after an OCR change, but each bank decides how much to pass on and when.",
                    "<strong>Fixed rates</strong> are mainly driven by wholesale swap rates, which move on <em>expectations</em> of future OCR decisions. So fixed rates often rise or fall before the OCR moves.",
                    "<strong>Your existing fixed rate</strong> doesn't change until your term ends. OCR changes affect you when you refix, or on any floating portion.",
                ])
            )),
            ("Choosing a fixed term when rates are rising", (
                table(
                    ["Approach", "Works well when", "Risk"],
                    [
                        ["Short fix (6–12 months)", "You expect your plans or income to change, or you think rates may ease soon.", "If rates keep rising, you refix sooner at a higher rate."],
                        ["Medium fix (18 months–2 years)", "You want certainty for a reasonable period without a long commitment.", "Less flexibility to sell or restructure without a break fee."],
                        ["Long fix (3–5 years)", "Your budget is tight and certainty matters more than possible savings.", "If rates fall, you're locked in, and breaking can be costly."],
                        ["Split across terms", "You want to spread your risk instead of predicting rates.", "Some of the loan will always be on a less favourable rate in hindsight."],
                    ],
                )
                + p("Many borrowers split their loan across two or three terms, so not all of it rolls over at once. Keeping a small floating or revolving portion lets you make extra repayments without break fees. See " + link("fixed-vs-floating-mortgage-nz.html", "fixed vs floating") + " and " + link("best-time-to-fix-mortgage-nz.html", "the best time to fix") + ".")
            )),
            ("If your fixed term ends soon", (
                ol([
                    "<strong>Start 60–90 days out.</strong> Most lenders let you lock a new rate in advance.",
                    "<strong>Compare your bank's offer with the market.</strong> Retention rates are often better than the advertised rate if you ask.",
                    "<strong>Check whether refinancing is worth it.</strong> Weigh any cashback against legal costs and clawback. Use the " + link("../calculators/refinance-savings.html", "refinance savings calculator") + ".",
                    "<strong>Stress-test your budget.</strong> Check your repayments at a higher rate with the " + link("../calculators/mortgage-calculator.html", "mortgage calculator") + ".",
                ])
                + p("Our " + link("fixed-rate-ending-refix-guide-nz.html", "refix playbook") + " covers the timeline step by step.")
            )),
            ("What to watch", (
                ul([
                    "<strong>OCR reviews</strong> — the Reserve Bank publishes its decision schedule and each statement on its website.",
                    "<strong>Inflation</strong> — Stats NZ publishes the Consumers Price Index quarterly. It's the figure the Reserve Bank targets.",
                    "<strong>Banks' fixed-rate changes</strong> — these often move ahead of the OCR. Our " + link("../mortgage-rates.html", "rates page") + " and your adviser can tell you what's on offer now.",
                ])
            )),
        ],
        "faqs": [
            ("Will mortgage rates go down in NZ in 2026?",
             f"Not on the current trend. The Reserve Bank raised the OCR in July and September 2026, to {CURRENT_OCR} as at {AS_AT}, to bring inflation back towards target. Rates could still change direction, but no one can predict that with certainty, so many borrowers split their loan across fixed terms."),
            ("Why is the OCR going up?",
             "The Reserve Bank raises the OCR when inflation is above its 1–3% target range and it wants to slow price rises. It has said it is gradually removing monetary stimulus to bring inflation back towards the 2% midpoint."),
            ("Does an OCR increase change my fixed mortgage rate?",
             "Not until your fixed term ends. Your rate is locked in for the term. OCR changes affect floating loans, and the rate you'll be offered when you refix."),
            ("Should I fix or float when rates are rising?",
             "Fixing gives you certainty while rates are rising, and floating means your repayments can increase. Many borrowers fix most of the loan and keep a small floating or revolving portion for extra repayments. The right mix depends on your budget and plans."),
        ],
        "faq_heading": "Mortgage rates: common questions",
        "related": [
            ("../mortgage-rates.html", "NZ Mortgage Rates", "Compare current fixed and floating rates."),
            ("how-ocr-affects-mortgages-nz.html", "How the OCR Affects Mortgages", "The mechanics, explained."),
            ("fixed-rate-ending-refix-guide-nz.html", "Fixed Rate Ending?", "Your refix playbook."),
        ],
    },
]
