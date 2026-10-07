#!/usr/bin/env python3
"""First home buyer posts for generate_local_intent_blogs.py.

Replaces weekly-reports/week-11-first-home-grant.html, which wrongly said the First
Home Grant had been extended to 2027. The grant closed on 22 May 2024; people still
search for it, so this post answers that search accurately.

Run:  python3 generate_local_intent_blogs.py first_home_posts
"""

from generate_local_intent_blogs import callout, link, ol, p, table, ul
from local_intent_posts import REL_FHB

KO_FHL = "https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/"
RBNZ_LVR = "https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions"

POSTS = [
    {
        "slug": "first-home-grant-nz-closed-alternatives",
        "published": "2026-10-07",
        "title": "First Home Grant NZ: Closed — What to Use Instead | Finch",
        "h1": "The First Home Grant Has Closed: What First Home Buyers Can Use Instead",
        "section_label": "First Home Buyers",
        "region": "",
        "lead_service": "First Home Buyer",
        "about": ["First Home Grant", "Kāinga Ora First Home Loan", "KiwiSaver first home withdrawal", "First home buyers"],
        "intro_pull": "The Kāinga Ora First Home Grant stopped taking applications on 22 May 2024 and hasn't been replaced. If you were counting on it, here's what's still available to help with your deposit — and how to put it together.",
        "description": "The NZ First Home Grant closed on 22 May 2024. What first home buyers can still use: KiwiSaver withdrawal, the Kāinga Ora First Home Loan and new-build options.",
        "keywords": [
            "first home grant NZ",
            "first home grant closed",
            "first home grant 2026",
            "Kāinga Ora First Home Grant",
            "first home buyer help NZ",
            "first home grant alternatives NZ",
        ],
        "cta_heading": "Working out your first home deposit?",
        "cta_sub": "Tell us your savings, KiwiSaver balance and income. We'll show you which deposit options you qualify for and what you could borrow.",
        "sections": [
            ("What happened to the First Home Grant", (
                p("The Kāinga Ora First Home Grant paid eligible first home buyers up to $5,000 per person for an existing home, or up to $10,000 per person for a new build. It <strong>closed to new applications on 22 May 2024</strong>, when the Government announced in Budget 2024 that the funding would be redirected to social housing.")
                + p("It has not been replaced with a new grant. If you see a website or social media post describing the First Home Grant as currently available, it's out of date.")
                + callout("Already approved before it closed?", "People who were pre-approved for the grant before 22 May 2024 were dealt with under the old rules. If that applies to you, check your position directly with Kāinga Ora.")
            )),
            ("What's still available", (
                table(
                    ["Option", "What it does", "Key points"],
                    [
                        ["KiwiSaver first home withdrawal", "Lets you use most of your KiwiSaver savings towards your first home.", "Generally available after three years of membership. You must leave at least $1,000 in the account. Withdrawn funds are paid to your solicitor for settlement."],
                        ["Kāinga Ora First Home Loan", "Lets eligible buyers purchase with a 5% deposit through participating lenders, with Kāinga Ora underwriting the loan.", "Income and other eligibility criteria apply. Check the current criteria on " + link(KO_FHL, "Kāinga Ora's website") + "."],
                        ["New-build exemption", "New builds are exempt from the Reserve Bank's low-deposit speed limits.", "Some lenders offer new-build lending with a smaller deposit than for an existing home. See the " + link(RBNZ_LVR, "Reserve Bank's LVR settings") + "."],
                        ["Family guarantee", "A family member uses equity in their own home as extra security for part of your loan.", "No cash changes hands. The guarantor takes on real risk, so they need independent legal advice."],
                        ["Gifted deposit", "Family gives you money towards the deposit.", "Most lenders accept a genuine gift with a signed gift letter confirming it doesn't need to be repaid."],
                        ["Low-deposit bank lending", "Banks can lend a limited share of their new lending to owner-occupiers with less than 20% deposit.", "Usually comes with a low-equity margin or fee, and stricter criteria."],
                    ],
                )
            )),
            ("How the numbers change without the grant", (
                p("For a couple buying a new build, losing the grant could mean up to $20,000 less towards the deposit. On an existing home, up to $10,000 less. That gap is usually closed in one of three ways:")
                + ul([
                    "<strong>Using the 5% deposit route.</strong> The Kāinga Ora First Home Loan, or low-deposit new-build lending, reduces the deposit you need in the first place.",
                    "<strong>Adding family support.</strong> A guarantee or gift can cover the shortfall without delaying your purchase.",
                    "<strong>Waiting and saving.</strong> Sometimes a few more months of KiwiSaver contributions and savings is the simplest answer — especially if it moves you over a deposit threshold that improves your rate.",
                ])
                + p("Work out what you can borrow with the " + link("../calculators/borrowing-power.html", "borrowing power calculator") + ", and see " + link("deposit-needed-home-loan-nz.html", "how much deposit you need") + ".")
            )),
            ("Putting your deposit together", (
                ol([
                    "<strong>Check your KiwiSaver eligibility and balance.</strong> Ask your provider for your withdrawable amount.",
                    "<strong>Add up savings and any family gift.</strong> Lenders want to see where every dollar came from.",
                    "<strong>Decide on new build or existing.</strong> It changes which low-deposit options are open to you.",
                    "<strong>Check First Home Loan eligibility</strong> if your deposit is under 20%.",
                    "<strong>Get pre-approved</strong> before you start making offers, so you know your real budget.",
                ])
                + p("Our " + link("../guides/first-home-guide.html", "first home buyer guide") + " covers the full process, and " + link("kiwisaver-first-home-withdrawal.html", "the KiwiSaver withdrawal guide") + " explains the withdrawal in detail.")
            )),
        ],
        "faqs": [
            ("Is the First Home Grant still available in NZ?",
             "No. The Kāinga Ora First Home Grant closed to new applications on 22 May 2024 and has not been replaced. The Kāinga Ora First Home Loan, which lets eligible buyers purchase with a 5% deposit, is still available."),
            ("Why was the First Home Grant stopped?",
             "The Government announced in Budget 2024 that the grant would close and the funding would be redirected to social housing."),
            ("Can I still use my KiwiSaver to buy my first home?",
             "Yes. The KiwiSaver first home withdrawal is separate from the grant and is still available. You generally need to have been a member for at least three years, and you must leave at least $1,000 in your account."),
            ("What is the Kāinga Ora First Home Loan?",
             "It's a scheme that lets eligible first home buyers purchase with a 5% deposit through participating lenders, with Kāinga Ora underwriting the loan. Income and other criteria apply, so check the current rules on the Kāinga Ora website."),
        ],
        "faq_heading": "First Home Grant: common questions",
        "related": REL_FHB,
    },
]
