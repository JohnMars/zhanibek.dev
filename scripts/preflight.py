#!/usr/bin/env python3
"""Pre-publish sanity check for zhanibek.dev personal website."""

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["index.html", "articles.html", "article.html", "talks.html",
         "talk.html", "books.html", "now.html", "resume.html"]

issues = []

def flag(filename, description, snippet=""):
    snippet_str = f"\n    {snippet}" if snippet else ""
    issues.append(f"[{filename}] {description}{snippet_str}")

def read(filename):
    with open(os.path.join(BASE, filename)) as f:
        return f.read()

def extract_site_data(content):
    """Extract the window.SITE = {...}; block."""
    m = re.search(r'(window\.SITE\s*=\s*\{.*?\n\}\s*;)', content, re.DOTALL)
    return m.group(1) if m else None

def extract_array(content, array_name):
    """Extract slugs and fields from a named array in SITE data."""
    # Find the array block
    pattern = rf'{array_name}:\s*\[(.*?)\](?=\s*[,}}])'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    # Extract individual object blocks
    entries = re.findall(r'\{([^{}]+)\}', block, re.DOTALL)
    result = []
    for entry in entries:
        obj = {}
        for field_m in re.finditer(r'(\w+):\s*"([^"]*)"', entry):
            obj[field_m.group(1)] = field_m.group(2)
        for field_m in re.finditer(r'(\w+):\s*(true|false|\d+)', entry):
            val = field_m.group(2)
            obj[field_m.group(1)] = val == 'true' if val in ('true', 'false') else int(val)
        if obj:
            result.append(obj)
    return result

# ── Check 1: SITE data consistency ────────────────────────────────────────────
print("1. Checking SITE data consistency...")
if not os.path.exists(os.path.join(BASE, "site-data.js")):
    flag("site-data.js", "Missing site-data.js")
for fname in FILES:
    content = read(fname)
    if '<script src="site-data.js"></script>' not in content:
        flag(fname, "Missing <script src=\"site-data.js\"></script>")

# ── Check 2: Placeholder / dummy content ──────────────────────────────────────
print("2. Checking for placeholder/dummy content...")
# Only look in the <body> HTML, not in <style> or <script> blocks
BODY_RE = re.compile(r'</style>(.*?)<script', re.DOTALL)

for fname in FILES:
    content = read(fname)
    # Find href="#" on actual <a> tags in body HTML (not in JS/CSS)
    # Strip script and style blocks first
    no_scripts = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    no_style = re.sub(r'<style[^>]*>.*?</style>', '', no_scripts, flags=re.DOTALL)
    for m in re.finditer(r'<a\s[^>]*href="#"', no_style):
        snippet = content[max(0, m.start()-20):m.end()+40].replace('\n', ' ')
        flag(fname, 'href="#" placeholder link', snippet.strip())

    # Check for lorem ipsum in body
    if 'lorem ipsum' in content.lower():
        flag(fname, 'Lorem ipsum text found')

# ── Check 3: Thumbnail assets ─────────────────────────────────────────────────
print("3. Checking thumbnail assets...")
ref_content = read("site-data.js")
thumbnails = re.findall(r'thumbnail:\s*"([^"]+)"', ref_content)
for thumb in thumbnails:
    path = os.path.join(BASE, thumb)
    if not os.path.exists(path):
        flag("index.html", f"Missing thumbnail: {thumb}")

# ── Check 4: Internal link targets ────────────────────────────────────────────
print("4. Checking internal link targets...")
talks    = extract_array(ref_content, "talks")
articles = extract_array(ref_content, "articles")
talk_slugs = {t["slug"] for t in talks if "slug" in t}
article_slugs = {a["slug"] for a in articles if "slug" in a}
external_article_slugs = {a["slug"] for a in articles if "slug" in a and "url" in a}

for fname in FILES:
    content = read(fname)
    # Only check literal slug values (not JS template literals)
    for slug in re.findall(r'talk\.html\?slug=([a-z0-9][a-z0-9-]+)', content):
        if slug not in talk_slugs:
            flag(fname, f"Broken talk link: slug '{slug}' not in SITE.talks")
    for slug in re.findall(r'article\.html\?slug=([a-z0-9][a-z0-9-]+)', content):
        if slug not in article_slugs:
            flag(fname, f"Broken article link: slug '{slug}' not in SITE.articles")
        elif slug in external_article_slugs:
            flag(fname, f"Wrong article link: '{slug}' is external (has url field) but links to article.html")

# ── Check 5: Title tags ───────────────────────────────────────────────────────
print("5. Checking title tags...")
seen_titles = {}
for fname in FILES:
    content = read(fname)
    m = re.search(r'<title>(.*?)</title>', content)
    if not m:
        flag(fname, "Missing <title> tag")
        continue
    title = m.group(1).strip()
    if not title:
        flag(fname, "Empty <title> tag")
    elif title in seen_titles:
        flag(fname, f"Duplicate title tag (same as {seen_titles[title]}): '{title}'")
    else:
        seen_titles[title] = fname

# ── Check 6: Books page links ─────────────────────────────────────────────────
print("6. Checking books page links...")
books_content = read("books.html")
book_links = re.findall(r'class="title-line"[^>]*>.*?href="([^"]*)"', books_content, re.DOTALL)
for href in book_links:
    if not href or href == "#":
        flag("books.html", f"Book link missing or href='#': {href!r}")

# ── Check 7: Home page logic ──────────────────────────────────────────────────
print("7. Checking home page rendering logic...")
index_content = read("index.html")
if 'sort((a, b) => b.date.localeCompare(a.date)).slice(0, 3)' not in index_content:
    flag("index.html", "Articles not rendered with date-sort + slice(0,3)")
if 'sort((a, b) => b.date.localeCompare(a.date)).slice(0, 2)' not in index_content:
    flag("index.html", "Talks not rendered with date-sort + slice(0,2)")
if re.search(r'filter\([at] => [at]\.featured\)', index_content):
    flag("index.html", "Stale featured-flag filter still present in home page rendering")

# ── Check 8: Sitemap ─────────────────────────────────────────────────────────
print("8. Checking sitemap.xml...")
SITEMAP_PAGES = [
    "https://zhanibek.dev/",
    "https://zhanibek.dev/articles.html",
    "https://zhanibek.dev/talks.html",
    "https://zhanibek.dev/books.html",
    "https://zhanibek.dev/now.html",
    "https://zhanibek.dev/resume.html",
]
sitemap_path = os.path.join(BASE, "sitemap.xml")
if not os.path.exists(sitemap_path):
    flag("sitemap.xml", "Missing sitemap.xml")
else:
    with open(sitemap_path) as f:
        sitemap = f.read()
    for url in SITEMAP_PAGES:
        if url not in sitemap:
            flag("sitemap.xml", f"Missing URL in sitemap: {url}")

# ── Report ────────────────────────────────────────────────────────────────────
print()
if issues:
    print(f"Found {len(issues)} issue(s):\n")
    for issue in issues:
        print(f"  ✗ {issue}")
    sys.exit(1)
else:
    print("All checks passed. Site is clean.")
    sys.exit(0)
