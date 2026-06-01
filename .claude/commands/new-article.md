Add a new article entry to the personal website's `window.SITE.articles` array across all 8 HTML files.

## Steps

1. Ask the user for:
   - **title** — article title
   - **date** — publication date (YYYY-MM-DD)
   - **readTime** — estimated read time in minutes (integer)
   - **tag** — one of: android, process, design, testing, team
   - **excerpt** — one or two sentence summary
   - **url** (optional) — if it's an external article (Habr, Medium, company blog, etc.), provide the full URL; leave blank for an internal article
   - **featured** (optional) — true to pin it on the homepage

2. Generate a `slug` from the title: lowercase, spaces → hyphens, remove special chars.

3. Insert the new entry at the **top** of the `articles: [` array (after the opening `[`) in all 8 HTML files:
   - `index.html`, `articles.html`, `article.html`, `talks.html`, `talk.html`, `resume.html`, `now.html`, `books.html`

4. Entry format (include only non-empty optional fields):
```javascript
{
  slug: "the-slug",
  title: "The Title",
  date: "YYYY-MM-DD",
  readTime: N,
  tag: "android",
  excerpt: "One or two sentence summary.",
  url: "https://...",      // only if external
  featured: true           // only if featured
},
```

5. Confirm how many files were updated and show the new entry.
