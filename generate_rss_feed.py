#!/usr/bin/env python3
"""Generates rss.xml from every blog/*.html and weekly-reports/*.html page.

Reads title, meta description, and JSON-LD datePublished directly from each
generated page, so it stays in sync with whatever the various blog/report
generator scripts produced -- no separate content to maintain by hand.

Run after adding new blog posts or weekly reports: python3 generate_rss_feed.py
"""
import glob
import os
import re
from datetime import datetime, timezone
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.finchmortgages.co.nz"
OUT_PATH = os.path.join(ROOT, "rss.xml")
MAX_ITEMS = 200


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def extract(path, url_prefix):
    text = read(path)

    title_m = re.search(r"<title>(.*?)</title>", text, re.S)
    if not title_m:
        return None
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()

    desc_m = re.search(r'name="description" content="([^"]*)"', text) or re.search(
        r'content="([^"]*)" name="description"', text
    )
    description = desc_m.group(1).strip() if desc_m else ""

    date_m = re.search(r'"datePublished":\s*"([^"]*)"', text)
    if not date_m:
        return None
    date_published = date_m.group(1)

    slug = os.path.basename(path)
    link = f"{BASE_URL}/{url_prefix}/{slug}"

    return {
        "title": title,
        "description": description,
        "link": link,
        "date": date_published,
    }


def rfc822(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=9, minute=0, tzinfo=timezone.utc
    )
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def main():
    items = []
    for path in glob.glob(os.path.join(ROOT, "blog", "*.html")):
        item = extract(path, "blog")
        if item:
            items.append(item)
    for path in glob.glob(os.path.join(ROOT, "weekly-reports", "*.html")):
        item = extract(path, "weekly-reports")
        if item:
            items.append(item)
    for path in glob.glob(os.path.join(ROOT, "case-studies", "*.html")):
        item = extract(path, "case-studies")
        if item:
            items.append(item)

    items.sort(key=lambda i: i["date"], reverse=True)
    items = items[:MAX_ITEMS]

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")

    item_xml = "\n".join(
        f"""    <item>
      <title>{escape(i['title'])}</title>
      <link>{escape(i['link'])}</link>
      <guid isPermaLink="true">{escape(i['link'])}</guid>
      <description>{escape(i['description'])}</description>
      <pubDate>{rfc822(i['date'])}</pubDate>
    </item>"""
        for i in items
    )

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Finch Mortgages — NZ Mortgage Blog &amp; Weekly Rate Reports</title>
    <link>{BASE_URL}/blog.html</link>
    <atom:link href="{BASE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>Independent NZ mortgage broker Finch Mortgages — first home buyer guides, lender comparisons, rate forecasts, and weekly NZ mortgage market reports.</description>
    <language>en-nz</language>
    <lastBuildDate>{now}</lastBuildDate>
    <generator>generate_rss_feed.py</generator>
{item_xml}
  </channel>
</rss>
"""

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(feed)

    print(f"Wrote {OUT_PATH} with {len(items)} items.")


if __name__ == "__main__":
    main()
