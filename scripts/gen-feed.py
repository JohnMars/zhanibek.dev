#!/usr/bin/env python3
"""Generate feed.xml from site-data.js articles."""

import os, re, sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://zhanibek.dev"

def read(fname):
    with open(os.path.join(BASE, fname)) as f:
        return f.read()

def extract_array(content, array_name):
    m = re.search(rf'{array_name}:\s*\[(.*?)\](?=\s*[,}}])', content, re.DOTALL)
    if not m:
        return []
    entries = re.findall(r'\{([^{}]+)\}', m.group(1), re.DOTALL)
    result = []
    for entry in entries:
        obj = {}
        for fm in re.finditer(r'(\w+):\s*"([^"]*)"', entry):
            obj[fm.group(1)] = fm.group(2)
        for fm in re.finditer(r'(\w+):\s*(true|false|\d+)', entry):
            val = fm.group(2)
            obj[fm.group(1)] = val == 'true' if val in ('true', 'false') else int(val)
        if obj:
            result.append(obj)
    return result

def rfc2822(iso_date):
    d = datetime.fromisoformat(iso_date).replace(tzinfo=timezone.utc)
    return d.strftime("%a, %d %b %Y 09:00:00 +0000")

def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

site_data = read("site-data.js")
articles = extract_array(site_data, "articles")

# Sort descending by date, skip articles with no excerpt (external without one)
articles = sorted(articles, key=lambda a: a.get("date", ""), reverse=True)

now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

items = []
for a in articles:
    slug  = a.get("slug", "")
    title = escape(a.get("title", ""))
    date  = a.get("date", "")
    excerpt = escape(a.get("excerpt", ""))
    url   = a.get("url") or f"{BASE_URL}/article.html?slug={slug}"
    pub   = rfc2822(date) if date else ""

    items.append(f"""
    <item>
      <title>{title}</title>
      <link>{url}</link>
      <guid isPermaLink="false">zhanibek.dev/{slug}</guid>
      <pubDate>{pub}</pubDate>
      <description>{excerpt}</description>
    </item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Zhanibek Marshal</title>
    <link>{BASE_URL}/</link>
    <description>Notes on Android, team practice, and the small process choices that compound.</description>
    <language>en-gb</language>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml" />
    <lastBuildDate>{now}</lastBuildDate>
{"".join(items)}
  </channel>
</rss>
"""

out = os.path.join(BASE, "feed.xml")
with open(out, "w") as f:
    f.write(feed)

print(f"feed.xml written ({len(articles)} articles).")
