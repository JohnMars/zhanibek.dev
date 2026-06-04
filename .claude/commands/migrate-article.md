Migrate a Markdown file to a standalone HTML article page on zhanibek.dev.

## Input

The argument is a path to a Markdown file (`.md` or `.markdown`). It may be absolute or relative to the project root.

## Steps

### 1. Read the file
Read the full file content.

### 2. Parse frontmatter
Strip the YAML block between the opening and closing `---` markers. Extract:
- `title` — strip surrounding quotes
- `date` — take only the `YYYY-MM-DD` portion (ignore time and timezone)

### 3. Derive metadata automatically

**slug** — from the filename: strip any leading `YYYY-MM-DD-` date prefix, drop the extension, lowercase. Example: `2019-05-31-farewell-kolesa.md` → `farewell-kolesa`.

**lang** — scan the body text. If Cyrillic characters make up more than 5% of letter characters, set `ru`; otherwise `en`.

**readTime** — run:
```
python3 scripts/convert_posts.py --read-time <absolute_path>
```
Use the integer printed to stdout.

**tag** — choose the single best-fit from: `android`, `career`, `life`, `process`, `testing`. Base the choice on article content and categories from the frontmatter.

**excerpt** — write a 1–2 sentence summary that captures the concrete takeaway or story. Be specific; avoid generic phrases like "in this article I discuss…".

### 4. Confirm with the user
Show a summary table of the inferred metadata before writing anything:

```
slug:     farewell-kolesa
title:    Farewell Kolesa Group
date:     2019-05-31
lang:     en
tag:      career
readTime: 2
excerpt:  After 4 years leading Android at Kolesa Group, ...
```

Ask: "Proceed with these values, or adjust anything?"

Wait for confirmation before continuing.

### 5. Convert to HTML
Run the conversion script in single-post mode. Use the absolute path for `src`. Build the JSON argument as a single-line string with no newlines:

```bash
python3 scripts/convert_posts.py --single '<json>'
```

Where `<json>` is:
```json
{"slug":"...","title":"...","date":"YYYY-MM-DD","tag":"...","read_time":N,"lang":"ru|en","src":"/absolute/path/to/file.md","excerpt":"..."}
```

### 6. Add to site-data.js
Insert a new entry into the `articles` array in `site-data.js`, sorted by date descending (newest first). Format:

```js
{
  slug: "...",
  title: "...",
  date: "YYYY-MM-DD",
  readTime: N,
  tag: "...",
  excerpt: "...",
  url: "slug.html"
},
```

Do **not** add a `url` field if this is replacing an article that should use `article.html?slug=X` instead — but for migrated stand-alone pages, always include `url: "slug.html"`.

### 7. Regenerate feed and run preflight
```bash
python3 scripts/gen-feed.py && python3 scripts/preflight.py
```

If preflight fails, fix the reported issues before finishing.

### 8. Report
Tell the user:
- Output HTML file path
- Whether a table of contents was generated (articles with 3+ top-level headings get one automatically)
- Final readTime used
- Any images that were referenced but not found in `assets/` (they will need to be copied manually)
