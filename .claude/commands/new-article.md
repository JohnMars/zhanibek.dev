Add a new article entry to the personal website's `window.SITE.articles` array.

## Steps

1. Ask the user for:
   - **title** — article title
   - **date** — publication date (YYYY-MM-DD)
   - **readTime** — estimated read time in minutes (integer)
   - **tag** — one of: android, process, design, testing, team
   - **excerpt** — one or two sentence summary
   - **url** (optional) — if it's an external article (Habr, Medium, company blog, etc.), provide the full URL; leave blank for an internal article

2. Generate a `slug` from the title: lowercase, spaces → hyphens, remove special chars.

3. Insert the new entry at the **top** of the `articles: [` array (after the opening `[`) in **`site-data.js` only**. Do not edit any HTML file.

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
},
```

5. If the article is external, also regenerate `feed.xml`:
   ```
   python3 scripts/gen-feed.py
   ```

6. Confirm the entry was added and show it.
