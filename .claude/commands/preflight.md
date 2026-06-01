Run the pre-publish sanity check script for the personal website.

## Steps

1. Regenerate the RSS feed from current site data:
   ```
   python3 scripts/gen-feed.py
   ```

2. Run the sanity check script:
   ```
   python3 scripts/preflight.py
   ```

3. Report the output to the user.
   - If it exits cleanly with "All checks passed" — site is ready to publish.
   - If it reports issues — list them and offer to fix each one.

## What the script checks

1. **SITE data file** — `site-data.js` exists and all 8 HTML files reference it
2. **Placeholder content** — `href="#"` links or lorem ipsum in body HTML
3. **Thumbnail assets** — every `thumbnail:` path in SITE.talks exists on disk
4. **Internal link targets** — `talk.html?slug=X` and `article.html?slug=X` links resolve to real slugs; external articles don't link to article.html
5. **Title tags** — present, non-empty, unique per page
6. **Books page links** — all book title links have real hrefs (not `#`)
7. **Home page logic** — date-sorted, articles capped at 3, talks at 2, no stale featured-flag filter
8. **Sitemap** — `sitemap.xml` exists and contains all 6 static page URLs
