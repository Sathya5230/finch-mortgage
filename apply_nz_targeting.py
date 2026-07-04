"""Apply New Zealand geo-targeting signals across the site.

Idempotent — safe to run after any page generator. Ensures every page (except
the protected high-conversion pages, which are managed by hand) carries the
NZ-specific signals search engines use for geo-targeting:

  * <html lang="en-NZ">            (NZ English, not generic en)
  * geo.region / geo.placename / geo.position / ICBM meta tags
  * <meta name="language" content="en-NZ">
  * <meta property="og:locale" content="en_NZ">
  * self-referencing hreflang="en-NZ" + hreflang="x-default" (from canonical)

Run this as the final step of the build pipeline, e.g. after
generate_*_pages.py and build_internal_links.py.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent

# index / first-home-buyers / contact are managed by hand — never touched here.
PROTECTED = {"index.html", "first-home-buyers.html", "contact.html"}
SKIP_DIRS = ("scratch", "node_modules", ".claude", ".git", ".vscode", "docs")

GEO_META = (
    '<meta name="geo.region" content="NZ"/>'
    '<meta name="geo.placename" content="Auckland, New Zealand"/>'
    '<meta name="geo.position" content="-36.8745;174.6483"/>'
    '<meta name="ICBM" content="-36.8745, 174.6483"/>'
    '<meta name="language" content="en-NZ"/>'
)
OG_LOCALE = '<meta property="og:locale" content="en_NZ"/>'


def process(path: Path) -> bool:
    text = original = path.read_text(encoding="utf-8")

    text = re.sub(
        r'<html(\s[^>]*?)?\slang="en"',
        lambda m: f'<html{m.group(1) or ""} lang="en-NZ"',
        text,
        count=1,
    )

    add = ""
    if 'name="geo.region"' not in text:
        add += GEO_META
    if 'property="og:locale"' not in text:
        add += OG_LOCALE
    if "hreflang=" not in text:
        canonical = re.search(
            r'<link href="(https://www\.finchmortgages\.co\.nz/[^"]*)" rel="canonical"/?>',
            text,
        )
        if canonical:
            url = canonical.group(1)
            add += (
                f'<link href="{url}" hreflang="en-NZ" rel="alternate"/>'
                f'<link href="{url}" hreflang="x-default" rel="alternate"/>'
            )

    if add:
        text = text.replace("</head>", add + "</head>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or rel.name in PROTECTED:
            continue
        if process(path):
            changed += 1
            print(f"  ~ {rel}")
    print(f"\nApplied NZ targeting to {changed} page(s).")


if __name__ == "__main__":
    main()
