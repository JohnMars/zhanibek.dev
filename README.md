# zhanibek.dev

Personal website of Zhanibek Marshal — Senior Android Engineer based in Berlin.

Built with vanilla HTML, CSS, and JavaScript. No build step, no frameworks.

## Structure

```
index.html          Home
articles.html       Writing list
article.html        Article reader (query param: ?slug=)
talks.html          Talks list
talk.html           Talk detail (query param: ?slug=)
books.html          Reading list
now.html            Now page
resume.html         Resume (links to resume.pdf)
site-data.js        Single source of truth for all content (articles, talks, author)
styles.css          Global styles
tweaks.js           Edit mode panel (vanilla JS, injected by parent frame)
```

## Scripts

```bash
python3 scripts/gen-feed.py   # Regenerate feed.xml from site-data.js
python3 scripts/gen-cv.py     # Regenerate resume.pdf from resume.html
python3 scripts/preflight.py  # Pre-publish sanity checks
```

## Deployment

Hosted on Cloudflare Pages. Pushes to `main` deploy automatically.

## Claude skills

- `/new-article` - Add a new article or external link
- `/new-talk` - Add a new talk
- `/gen-cv` - Generate a tailored PDF CV from resume.html
- `/preflight` - Run pre-publish checks before deploying
