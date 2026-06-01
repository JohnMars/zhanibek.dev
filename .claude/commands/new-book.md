Add a new book recommendation to the personal website's `books.html` page.

## Steps

1. Ask the user for:
   - **title** — book title
   - **author** — author name(s)
   - **note** — one or two sentence personal take on why the book matters
   - **tags** — one to three topic tags (e.g. android, architecture, leadership, productivity, career, testing, design)

2. Insert the new book at the **top** of the `<ul class="book-list">` in `books.html`, using this HTML format:

```html
        <li>
          <div class="title-line"><em>Book Title</em> — Author Name</div>
          <div class="book-tags">
            <span class="book-tag">tag1</span>
            <span class="book-tag">tag2</span>
          </div>
          <div class="note">Personal note about the book.</div>
        </li>
```

3. Confirm the book was added and show the new entry.
