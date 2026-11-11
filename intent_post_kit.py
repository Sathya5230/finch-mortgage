"""Shared helpers for the November 2026 high-intent post batches
(refinance_intent_posts.py and home_loan_intent_posts.py).

Content rules are the same as the other post modules: explain how lending
works, never quote interest rates, never attribute a policy to a named lender,
never promise an approval. Dollar figures appear only as worked examples or
with an "as at" date and a source.
"""

from generate_local_intent_blogs import callout, link, ol, p, table, ul  # noqa: F401

PUBLISHED = "2026-11-11"

IRD = "https://www.ird.govt.nz/"
RBNZ_LVR = "https://www.rbnz.govt.nz/regulation-and-supervision/banks/macro-prudential-policy/loan-to-value-ratio-restrictions"
KO_FHL = "https://kaingaora.govt.nz/en_NZ/home-ownership/first-home-loan/"
SORTED = "https://sorted.org.nz/guides/home-buying/"
FSCL = "https://www.fscl.org.nz/"

REL_REFI = [
    ("../services/refinance.html", "Refinance Your Mortgage",
     "Refinance advice across the 23 lenders on our panel."),
    ("../calculators/refinance-savings.html", "Refinance Savings Calculator",
     "Estimate what switching could save."),
    ("../guides/refinance-guide.html", "NZ Refinance Guide",
     "When to refinance, and how the switch works."),
]

REL_HOME = [
    ("../services/home-loan.html", "Home Loans",
     "Home loan advice across the 23 lenders on our panel."),
    ("../calculators/borrowing-power.html", "Borrowing Power Calculator",
     "A rough idea of what lenders may lend you."),
    ("../services/pre-approval.html", "Pre-Approval",
     "Know your budget before you make an offer."),
]


def body(*blocks):
    """Plain strings become paragraphs, lists become bullet lists, HTML passes through."""
    out = ""
    for b in blocks:
        if isinstance(b, list):
            out += ul(b)
        elif b.lstrip().startswith("<"):
            out += b
        else:
            out += p(b)
    return out


def post(slug, title, h1, intro, description, keywords, sections, faqs, *,
         service, label, about, cta, cta_sub, related, faq_heading="Common questions",
         refi_form=False):
    assert len(title) <= 60, (slug, "title", len(title))
    assert 110 <= len(description) <= 158, (slug, "description", len(description))
    return {
        "slug": slug, "published": PUBLISHED, "title": title, "h1": h1,
        "section_label": label, "region": "", "lead_service": service,
        "about": about, "intro_pull": intro, "description": description,
        "keywords": keywords, "cta_heading": cta, "cta_sub": cta_sub,
        "sections": [(h, body(*b)) for h, *b in sections],
        "faqs": faqs, "faq_heading": faq_heading, "related": related,
        "refi_form": refi_form,
    }
