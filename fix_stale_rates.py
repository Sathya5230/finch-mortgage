"""Replace the hand-typed bank rate figures labelled "Live" / "Updated weekly".

mortgage-rates.html and the homepage benchmark card showed ANZ, BNZ and Heartland
floating at 7.95-7.99% under a "Live Rates · Updated weekly" badge. After the
2 September 2026 OCR rise, the banks' published floating rates were roughly 6.1-6.35%
(ANZ 6.29% per its 2 Sep 2026 release; Heartland showed 6.35% on 11 Oct 2026), and
nothing updates these figures automatically. Showing stale rates as live is
misleading on a YMYL page, so the tables now point to each lender's own rates page
(URLs checked 11 Oct 2026) and Finch's review instead of quoting numbers. If rates
are reinstated, add an "as at" date and source beside them.

Idempotent. Run with --apply to write; default is a dry run.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

LENDERS = [
    ("ANZ", "#00A4D6", "https://www.anz.co.nz/content/anzconz/nz/en/rates-fees-agreements/home-loans.html", "lenders/anz-home-loan-review.html"),
    ("BNZ", "#003478", "https://www.bnz.co.nz/personal-banking/home-loans/compare-bnz-home-loan-rates", "lenders/bnz-home-loan-review.html"),
    ("Heartland Bank", "#005A9C", "https://www.heartland.co.nz/home-loans", "lenders/heartland-bank-mortgage-review.html"),
]
TD = 'style="padding:1.25rem 1rem;"'
A = 'style="color:var(--finch-forest);font-weight:700;text-decoration:underline;"'


def rates_section():
    rows = "".join(
        f'<tr style="border-bottom:1px solid rgba(181,206,176,0.5);">'
        f'<td style="padding:1.25rem 1rem;font-weight:800;color:var(--neutral-black);"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{dot};margin-right:0.6rem;vertical-align:middle;"></span>{name}</td>'
        f'<td {TD}><a href="{url}" target="_blank" rel="nofollow noopener" {A}>{name} home loan rates ↗</a></td>'
        f'<td {TD}><a href="{review}" {A}>Our {name} review</a></td></tr>'
        for name, dot, url, review in LENDERS
    )
    return f"""<!-- ── WHERE TO CHECK RATES ── -->
<section style="padding:6rem 0;background:white;">
<div class="container">
<div class="section-label"><span>Today's Rates</span></div>
<h2 class="section-heading" style="margin-bottom:1.5rem;">Where to Check<br/><em>Today's Rates.</em></h2>
<p style="color:var(--neutral-medGray);line-height:1.8;max-width:760px;margin-bottom:2.5rem;">Banks change their advertised rates often, sometimes several times a month. Rather than show figures that may be out of date, here is where each bank publishes its current home loan rates. For the rate you would actually be offered, ask us: we compare pricing across the 23 lenders on our panel.</p>
<div style="overflow-x:auto;">
<table style="width:100%;min-width:560px;border-collapse:collapse;margin-bottom:2rem;">
<thead><tr>
<th style="text-align:left;padding:1.25rem 1rem;border-bottom:2px solid var(--finch-forest);color:var(--finch-forest);font-family:var(--font-display);font-size:1.15rem;">Lender</th>
<th style="text-align:left;padding:1.25rem 1rem;border-bottom:2px solid var(--finch-forest);color:var(--neutral-black);font-weight:700;">Current advertised rates</th>
<th style="text-align:left;padding:1.25rem 1rem;border-bottom:2px solid var(--finch-forest);color:var(--neutral-black);font-weight:700;">Finch review</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<div style="background:var(--finch-mist);padding:2rem;border-radius:1rem;border-left:4px solid var(--finch-forest);">
<h2 style="font-size:1.1rem;font-weight:700;color:var(--neutral-black);margin-bottom:0.5rem;">Advertised rates are a starting point</h2>
<p style="color:var(--neutral-medGray);font-size:0.95rem;line-height:1.7;">Banks publish "carded" rates, and most also advertise lower "special" rates for borrowers with at least 20% equity. Depending on your deposit, income and the lender, you may be offered a sharper rate or a cashback. We'll tell you what is realistic for your situation before you apply.</p>
<div style="margin-top:1.5rem;">
<a class="btn-primary" href="contact.html">Get a Custom Rate Quote →</a>
</div>
</div>
</div>
</section>"""


def homepage_card_rows():
    return "\n".join(
        f'<div style="display:flex;justify-content:space-between;align-items:center;{"padding-bottom:1rem;border-bottom:1px solid rgba(181,206,176,0.3);" if i < len(LENDERS) - 1 else ""}">\n'
        f'<div style="display:flex;align-items:center;gap:0.75rem;font-weight:700;color:var(--neutral-black);"><div style="width:10px;height:10px;border-radius:50%;background:{dot};"></div>{name}</div>'
        f'<a href="{url}" target="_blank" rel="nofollow noopener" style="font-weight:700;color:var(--finch-forest);text-decoration:underline;">Today\'s rates ↗</a>\n</div>'
        for i, (name, dot, url, _) in enumerate(LENDERS)
    )


def fix_rates_page(s):
    start = s.find("<!-- ── RATES TABLE ── -->")
    if start != -1 and "7.99%" in s[start:start + 9000]:
        end = s.find("</section>", start) + len("</section>")
        s = s[:start] + rates_section() + s[end:]
    pairs = {
        " Live Rates Updated weekly": " Rates change often · Check before you fix",
        'Compare the latest advertised ("carded") fixed and floating interest rates across New Zealand\'s top tier-one banks. Note: Finch can frequently secure unadvertised discounts below these numbers.':
            'Understand how advertised ("carded") fixed and floating rates work, see where each bank publishes its current rates, and find out what you could actually be offered.',
        "Compare today's NZ mortgage rates across ANZ, BNZ, Heartland Bank, SBS Bank and more. Live updates, OCR commentary, and expert analysis from Finch Mortgages.":
            "How NZ mortgage rates work, where ANZ, BNZ and Heartland publish today's rates, and how a broker can get you a better offer. Free advice from Finch.",
        '<div class="section-label"><span>Reading The Table</span></div>': '<div class="section-label"><span>Understanding Rates</span></div>',
        'The table above shows "carded" rates — the standard advertised rate each bank publishes':
            'Banks publish "carded" rates — the standard advertised rate each bank sets',
    }
    for old, new in pairs.items():
        s = s.replace(old, new)
    return s


def fix_homepage(s):
    old_badge = '<h3 style="font-size:1.25rem;color:var(--neutral-black);">1-Year Fixed Benchmark</h3>\n<span style="font-size:0.75rem;font-weight:800;color:var(--finch-forest);background:var(--finch-mist);padding:0.25rem 0.75rem;border-radius:999px;">Updated weekly</span>'
    new_badge = '<h3 style="font-size:1.25rem;color:var(--neutral-black);">Check Today\'s Rates</h3>\n<span style="font-size:0.75rem;font-weight:800;color:var(--finch-forest);background:var(--finch-mist);padding:0.25rem 0.75rem;border-radius:999px;">Rates change often</span>'
    if old_badge not in s:
        return s
    s = s.replace(old_badge, new_badge)
    a = s.find(new_badge)
    rows_start = s.find('<div style="display:flex;flex-direction:column;gap:1rem;">', a)
    rows_open = len('<div style="display:flex;flex-direction:column;gap:1rem;">')
    rows_end = s.find("5.89%</div>\n</div>\n</div>", rows_start)
    if rows_start == -1 or rows_end == -1:
        raise SystemExit("homepage card layout changed; update fix_stale_rates.py")
    rows_end += len("5.89%</div>\n</div>\n")
    return s[:rows_start + rows_open] + "\n" + homepage_card_rows() + "\n" + s[rows_end:]


def main():
    changed = 0
    for rel, fn in (("mortgage-rates.html", fix_rates_page), ("index.html", fix_homepage)):
        p = ROOT / rel
        src = p.read_text(encoding="utf-8")
        out = fn(src)
        if out != src:
            changed += 1
            print(f"  would change: {rel}" if not APPLY else f"  changed: {rel}")
            if APPLY:
                p.write_text(out, encoding="utf-8")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
