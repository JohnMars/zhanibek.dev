Update the home page to show the most recent articles and talks after new content has been added.

The home page (`index.html`) automatically renders:
- The **3 most recent articles** by date
- The **2 most recent talks** by date

No manual featuring or flag management is needed — the rendering is date-sorted. This skill verifies everything looks correct after adding new content.

## Steps

1. Read `window.SITE.articles` and `window.SITE.talks` from `index.html`.

2. **Verify home page rendering logic** in `index.html` contains:
   ```javascript
   const allArticles = [...SITE.articles].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 3);
   ```
   and:
   ```javascript
   const talksToShow = [...SITE.talks].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 2);
   ```
   If either is missing or different, restore it.

3. **Confirm what will show on the home page** — print the 3 most recent articles and 2 most recent talks (title + date) so the user can verify the right content is surfaced.

4. **Check SITE data is consistent** across all 8 files (`index.html`, `articles.html`, `article.html`, `talks.html`, `talk.html`, `books.html`, `now.html`, `resume.html`). If any file has a stale or different array, flag it — the new content may not have been written to all files.

5. Report a summary: what's showing on the home page, and whether all 8 files are in sync.
