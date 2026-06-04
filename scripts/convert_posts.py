#!/usr/bin/env python3
"""Convert Markdown articles to standalone HTML pages for zhanibek.dev.

Usage:
  # Rebuild all pre-configured posts:
  python3 scripts/convert_posts.py

  # Migrate a single file (slug and metadata required):
  python3 scripts/convert_posts.py --single '{"slug":"my-post","title":"My Post","date":"2024-01-15","tag":"android","read_time":5,"lang":"en","src":"/abs/path.md","excerpt":"..."}'

  # Estimate reading time for a file:
  python3 scripts/convert_posts.py --read-time /path/to/file.md
"""
import markdown
import re
import os
import sys
import json

SITE_DIR = "/Users/zhanibekmarshal/personal-website"
OLD_DIR  = "/Users/zhanibekmarshal/janibekmarshal.com/_posts"

POSTS = [
    {
        "slug":      "modular-android-libraries-ru",
        "title":     "Модульная разработка Android приложений",
        "date":      "2018-04-20",
        "tag":       "android",
        "read_time": 2,
        "lang":      "ru",
        "src":       f"{OLD_DIR}/2018-04-20-android-module-libraries.markdown",
        "excerpt":   "Как «Колёса Крыша Маркет» вынесла бизнес-логику и слой данных в общую библиотеку для трёх продуктов.",
    },
    {
        "slug":      "mvvm-from-theories-to-test-ru",
        "title":     "От теории до тестирования MVVM",
        "date":      "2018-07-19",
        "tag":       "android",
        "read_time": 1,
        "lang":      "ru",
        "src":       f"{OLD_DIR}/2018-07-19-mvvm-from-theories-to-test.md",
        "excerpt":   "Классический MVVM через Android Architecture Components - от теории к unit-тестированию.",
    },
    {
        "slug":      "why-android-kotlin-ru",
        "title":     "Почему Android разработчики переходят на Kotlin",
        "date":      "2018-09-28",
        "tag":       "android",
        "read_time": 1,
        "lang":      "ru",
        "src":       f"{OLD_DIR}/2018-09-28-why-android-developers-are-moving-to-kotlin.md",
        "excerpt":   "Заметки с митапа DrinkUp Almaty о прелестях Kotlin и почему разработчики уходят с Java.",
    },
    {
        "slug":      "android-architecture-components-codelab",
        "title":     "Code Labs: Android Architecture Components",
        "date":      "2018-10-12",
        "tag":       "android",
        "read_time": 25,
        "lang":      "ru",
        "src":       f"{OLD_DIR}/2018-10-12-google-devfest-almaty.md",
        "excerpt":   "Пошаговый codelab с DevFest Almaty 2018: ViewModel, LiveData, Room и Repository - строим приложение-клон Колёс.",
    },
    {
        "slug":      "kolesa-academy-android",
        "title":     "Колёса Академия - что нужно знать Android разработчику",
        "date":      "2018-12-08",
        "tag":       "android",
        "read_time": 12,
        "lang":      "ru",
        "src":       f"{OLD_DIR}/2018-12-08-kolesa-academy-how-to-prepare.md",
        "excerpt":   "OOP, паттерны, алгоритмы и Android SDK - что нужно знать, чтобы пройти отбор в Колёса Академию.",
    },
    {
        "slug":      "farewell-kolesa",
        "title":     "Farewell Kolesa Group",
        "date":      "2019-05-31",
        "tag":       "career",
        "read_time": 2,
        "lang":      "en",
        "src":       f"{OLD_DIR}/2019-05-31-farewell-kolesa.md",
        "excerpt":   "After 4 years and 3 months at the best IT company in Kazakhstan, moving on - and what leading an Android team taught me about staying kind.",
    },
    {
        "slug":      "why-berlin-over-tokyo",
        "title":     "Почему выбрал Берлин вместо Токио",
        "date":      "2020-10-11",
        "tag":       "life",
        "read_time": 18,
        "lang":      "ru",
        "src":       f"{OLD_DIR}/2020-10-11-why-berlin-over-tokyo.md",
        "excerpt":   "Год планировал переехать в Токио, но выбрал Берлин - о трудоголизме, жилье, work-life balance и жизни в немецкой столице.",
    },
]

MONTHS = {1:"jan",2:"feb",3:"mar",4:"apr",5:"may",6:"jun",
          7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}

def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text

def shift_headings(md_text):
    """Bump all headings down one level so body never uses h1."""
    lines = []
    for line in md_text.split("\n"):
        m = re.match(r"^(#{1,5})(\s)", line)
        if m:
            line = "#" + line
        lines.append(line)
    return "\n".join(lines)

def remove_local_images(html):
    """No-op: images are now copied to assets/."""
    return html

def build_toc(html_body):
    """Add IDs to headings and return (modified_html, toc_html).
    Detects the minimum heading level present, then builds a ToC from
    that level (primary) and one deeper (indented). Requires 3+ primary headings."""
    counter = [0]
    headings = []

    def add_id(m):
        tag     = m.group(1)          # e.g. "h3"
        attrs   = m.group(2)
        content = m.group(3)
        level   = int(tag[1])
        counter[0] += 1
        slug = f"s{counter[0]}"
        plain = re.sub(r'<[^>]+>', '', content).strip()
        headings.append((level, slug, plain))
        return f'<{tag} id="{slug}"{attrs}>{content}</{tag}>'

    modified = re.sub(r'<(h[2-4])([^>]*)>(.*?)</\1>', add_id, html_body, flags=re.DOTALL)

    if not headings:
        return modified, ""

    min_level = min(lvl for lvl, _, _ in headings)
    primary_count = sum(1 for lvl, _, _ in headings if lvl == min_level)
    if primary_count < 3:
        return modified, ""

    items = []
    for level, slug, text in headings:
        if level == min_level:
            items.append(f'    <li><a href="#{slug}">{text}</a></li>')
        elif level == min_level + 1:
            items.append(f'    <li class="toc-h3"><a href="#{slug}">{text}</a></li>')
        # skip deeper levels

    toc = (
        '    <nav class="toc">\n'
        '      <p class="toc-label">contents</p>\n'
        '      <ul>\n'
        + '\n'.join(items) + '\n'
        + '      </ul>\n'
        + '    </nav>'
    )
    return modified, toc

def fmt_date(iso):
    y, mo, d = map(int, iso.split("-"))
    return f"{d:02d} {MONTHS[mo]} {y}"

CHROME_JS = r"""(function() {
  const THEME_KEY = "zm.theme";
  function applyTheme(t) {
    if (t === "system" || !t) document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", t);
  }
  function currentTheme() { return localStorage.getItem(THEME_KEY) || "system"; }
  function nextTheme(t)   { return t === "light" ? "dark" : t === "dark" ? "system" : "light"; }
  function setLabel(btn) {
    const t = currentTheme();
    btn.textContent = t === "light" ? "☀" : t === "dark" ? "☾" : "◐";
    btn.setAttribute("title", `theme: ${t} (click to cycle)`);
  }
  applyTheme(currentTheme());

  document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector("[data-theme-toggle]");
    if (btn) { setLabel(btn); btn.addEventListener("click", () => { const t = nextTheme(currentTheme()); localStorage.setItem(THEME_KEY, t); applyTheme(t); setLabel(btn); }); }

    // active nav
    const raw = location.pathname.split("/").pop() || "index";
    const path = raw.replace(/\.html$/, "") || "index";
    document.querySelectorAll("nav.primary a").forEach(a => {
      const href = a.getAttribute("href").replace(/\.html$/, "");
      if (href === path) a.setAttribute("aria-current", "page");
    });

    // density
    const d = localStorage.getItem("zm.density") || "comfy";
    document.documentElement.setAttribute("data-density", d);

    // read-time hide
    const showRT = localStorage.getItem("zm.readtime") !== "false";
    document.documentElement.setAttribute("data-hide-readtime", String(!showRT));

    // search
    const overlay = document.querySelector("[data-search-overlay]");
    const input   = document.querySelector("[data-search-input]");
    const results = document.querySelector("[data-search-results]");
    const openBtn = document.querySelector("[data-search-open]");
    function buildIndex() {
      const items = [];
      (window.SITE?.articles || []).forEach(a => items.push({ kind:"article", title:a.title, excerpt:a.excerpt, href: a.url && /^https?:\/\//.test(a.url) ? a.url : (a.url || `article.html?slug=${a.slug}`) }));
      (window.SITE?.talks   || []).forEach(t => items.push({ kind:"talk",    title:t.title, excerpt:`${t.venue}, ${t.city}`, href:`talk.html?slug=${t.slug}` }));
      [{ kind:"page",title:"Resume",excerpt:"Experience",href:"resume.html"},
       { kind:"page",title:"Now",   excerpt:"What I'm working on",href:"now.html"},
       { kind:"page",title:"Articles",excerpt:"All writing",href:"articles.html"},
       { kind:"page",title:"Talks",  excerpt:"Public speaking",href:"talks.html"},
       { kind:"page",title:"Books",  excerpt:"Reading list",href:"books.html"}].forEach(p=>items.push(p));
      return items;
    }
    const idx = buildIndex(); let activeIdx = 0;
    function render(q) {
      if (!results) return;
      q = q.trim().toLowerCase();
      let list = q ? idx.filter(i => i.title.toLowerCase().includes(q) || (i.excerpt||"").toLowerCase().includes(q)) : idx;
      if (!list.length) { results.innerHTML = `<div class="search-empty">no results for "${q}"</div>`; return; }
      results.innerHTML = list.slice(0,12).map((r,i)=>`<a class="search-result ${i===activeIdx?'active':''}" href="${r.href}" data-idx="${i}"><span class="kind">${r.kind}</span><span class="title">${r.title}</span></a>`).join("");
    }
    function openSearch()  { if (!overlay) return; overlay.setAttribute("data-open","true"); activeIdx=0; render(""); setTimeout(()=>input?.focus(),30); }
    function closeSearch() { if (!overlay) return; overlay.setAttribute("data-open","false"); if (input) input.value=""; }
    openBtn?.addEventListener("click", openSearch);
    overlay?.addEventListener("click", e => { if (e.target===overlay) closeSearch(); });
    input?.addEventListener("input", e => { activeIdx=0; render(e.target.value); });
    input?.addEventListener("keydown", e => {
      const links = results.querySelectorAll(".search-result");
      if (e.key==="ArrowDown") { e.preventDefault(); activeIdx=Math.min(activeIdx+1,links.length-1); render(input.value); }
      else if (e.key==="ArrowUp") { e.preventDefault(); activeIdx=Math.max(activeIdx-1,0); render(input.value); }
      else if (e.key==="Enter") { const a=results.querySelector(`.search-result[data-idx="${activeIdx}"]`); if(a) location.href=a.getAttribute("href"); }
      else if (e.key==="Escape") closeSearch();
    });
    document.addEventListener("keydown", e => {
      if ((e.key==="k"||e.key==="K")&&(e.metaKey||e.ctrlKey)) { e.preventDefault(); openSearch(); }
      else if (e.key==="/"&&document.activeElement?.tagName!=="INPUT") { e.preventDefault(); openSearch(); }
      else if (e.key==="Escape"&&overlay?.getAttribute("data-open")==="true") closeSearch();
    });

    // reading progress
    const bar = document.querySelector(".progress");
    if (bar) {
      const onScroll = () => {
        const article = document.querySelector("article.prose");
        if (!article) { bar.style.width="0%"; return; }
        const rect = article.getBoundingClientRect();
        const pct  = Math.max(0, Math.min(1, -rect.top / (rect.height - window.innerHeight)));
        bar.style.width = (pct * 100) + "%";
      };
      window.addEventListener("scroll", onScroll, { passive:true });
      onScroll();
    }
  });

  window.ZM = {
    setDensity(d)   { localStorage.setItem("zm.density",d); document.documentElement.setAttribute("data-density",d); },
    setReadtime(v)  { localStorage.setItem("zm.readtime",String(!!v)); document.documentElement.setAttribute("data-hide-readtime",String(!v)); },
    setTheme(t)     { localStorage.setItem(THEME_KEY,t); applyTheme(t); const b=document.querySelector("[data-theme-toggle]"); if(b){ const t2=t==="light"?"☀":t==="dark"?"☾":"◐"; b.textContent=t2; } },
    getDensity()    { return localStorage.getItem("zm.density")||"comfy"; },
    getReadtime()   { return localStorage.getItem("zm.readtime")!=="false"; },
    getTheme()      { return currentTheme(); }
  };
})();"""

TEMPLATE = """\
<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="favicon.svg">
<title>{title} - Zhanibek Marshal</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://zhanibek.dev/{slug}.html">
<meta name="description" content="{excerpt}">
<meta property="og:title" content="{title} - Zhanibek Marshal">
<meta property="og:description" content="{excerpt}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://zhanibek.dev/{slug}.html">
<meta property="og:image" content="https://zhanibek.dev/assets/og-image.jpg">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="Zhanibek Marshal - RSS" href="feed.xml">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="styles.css">
<script>(function(){{const t=localStorage.getItem("zm.theme");if(t&&t!=="system")document.documentElement.setAttribute("data-theme",t);const d=localStorage.getItem("zm.density");if(d)document.documentElement.setAttribute("data-density",d);}})();</script>
</head>
<body>

<div class="progress"></div>

<header class="site-header shell" style="padding-bottom:0; margin-bottom:0; border:0;">
  <a href="index.html" class="brand"><span class="dot"></span>Zhanibek Marshal</a>
  <nav class="primary">
    <a href="index.html">home</a>
    <a href="articles.html">articles</a>
    <a href="talks.html">talks</a>
    <a href="resume.html">resume</a>
    <a href="now.html">now</a>
    <a href="books.html">books</a>
    <span class="utilities">
      <button class="icon-btn" data-search-open><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14 14"/></svg></button>
      <a class="icon-btn" href="feed.xml"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 3a10 10 0 0 1 10 10"/><path d="M3 8a5 5 0 0 1 5 5"/><circle cx="3.5" cy="12.5" r="1" fill="currentColor"/></svg></a>
      <button class="icon-btn" data-theme-toggle>◐</button>
    </span>
  </nav>
</header>

<main class="shell">
  <article class="prose">
    <h1>{title}</h1>
    <div class="article-meta">
      <span>{date_display}</span>
      <span>{tag}</span>
      <span class="read-time">{read_time} min read</span>
    </div>

{toc}
{body}

    <div class="divider"></div>
    <p style="font-family:var(--mono); font-size:var(--type-meta); color:var(--ink-3); text-transform:lowercase;">filed under <a href="articles.html">{tag}</a> · <a href="feed.xml">subscribe via rss</a></p>
  </article>

  <footer class="site-footer">
    <span>© 2026 Zhanibek Marshal</span>
    <span><a href="feed.xml">rss</a> · <a href="https://androiddev.social/@zhanibek">mastodon</a> · <a href="https://www.linkedin.com/in/johnmarshal/">linkedin</a></span>
  </footer>
</main>

<div class="search-overlay" data-search-overlay data-open="false">
  <div class="search-box">
    <input class="search-input" data-search-input placeholder="search articles, talks, pages..." type="text" autocomplete="off">
    <div class="search-results" data-search-results></div>
  </div>
</div>

<script src="site-data.js"></script>
<script>
{chrome_js}
</script>
<script src="tweaks.js"></script>
</body>
</html>
"""

def convert_post(post):
    with open(post["src"], encoding="utf-8") as f:
        text = f.read()

    text = strip_frontmatter(text)
    text = shift_headings(text)

    md = markdown.Markdown(extensions=["fenced_code", "tables", "nl2br"])
    html_body = md.convert(text)
    html_body = remove_local_images(html_body)

    # Build ToC and inject heading IDs before indenting
    html_body, toc = build_toc(html_body)

    # Indent body, but skip lines inside <pre> blocks to preserve code whitespace
    body_lines = []
    in_pre = False
    for line in html_body.split("\n"):
        if "<pre" in line:
            in_pre = True
        if in_pre:
            body_lines.append(line)
        else:
            body_lines.append("    " + line)
        if "</pre>" in line:
            in_pre = False
    body = "\n".join(body_lines)

    page = TEMPLATE.format(
        lang        = post["lang"],
        slug        = post["slug"],
        title       = post["title"],
        excerpt     = post["excerpt"],
        date_display= fmt_date(post["date"]),
        tag         = post["tag"],
        read_time   = post["read_time"],
        toc         = toc,
        body        = body,
        chrome_js   = CHROME_JS,
    )

    out = os.path.join(SITE_DIR, post["slug"] + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  written: {out}")

def estimate_read_time(src_path):
    """Return estimated reading time in minutes for a markdown file.
    Strips code blocks before counting; uses 200 WPM for technical prose."""
    with open(src_path, encoding="utf-8") as f:
        text = f.read()
    text = strip_frontmatter(text)
    text = re.sub(r'```[\s\S]*?```', '', text)   # fenced code blocks
    text = re.sub(r'`[^`\n]+`', '', text)         # inline code
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)    # images
    text = re.sub(r'\[([^\]]*?)\]\([^)]*?\)', r'\1', text)  # link labels
    text = re.sub(r'[#*_>-]', ' ', text)
    words = len(text.split())
    return max(1, round(words / 200))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--single":
        post = json.loads(sys.argv[2])
        convert_post(post)
        print("Done.")
    elif len(sys.argv) == 3 and sys.argv[1] == "--read-time":
        mins = estimate_read_time(sys.argv[2])
        print(mins)
    else:
        for post in POSTS:
            convert_post(post)
        print("Done.")
