Add a new talk entry to the personal website's `window.SITE.talks` array.

## Steps

1. Ask the user for:
   - **title** — talk title
   - **venue** — conference or meetup name (e.g. "Droidcon Berlin", "Android KZ Meetup")
   - **date** — talk date (YYYY-MM-DD)
   - **city** — city where the talk was given (or "Online")
   - **duration** — e.g. "30 min", "20 min"
   - **abstract** — one or two sentence description of the talk
   - **slides** (optional) — SpeakerDeck URL
   - **video** (optional) — YouTube URL of the recording
   - **featured** (optional) — true to show on homepage

2. Generate a `slug` and `year` from the title and date.

3. Download the thumbnail:
   - If `slides` is a SpeakerDeck URL: fetch the oEmbed endpoint `https://speakerdeck.com/oembed.json?url=<slides_url>`, extract the presentation ID from the iframe `src` attribute (pattern: `speakerdeck.com/player/{id}`), then download `https://files.speakerdeck.com/presentations/{id}/slide_0.jpg` to `assets/thumbnails/{slug}.jpg`.
   - If `video` is a YouTube URL (and no slides): download the YouTube hqdefault thumbnail `https://i.ytimg.com/vi/{video_id}/hqdefault.jpg` to `assets/thumbnails/{slug}.jpg`.
   - Set `thumbnail: "assets/thumbnails/{slug}.jpg"` in the entry.

4. Insert the new entry at the **top** of the `talks: [` array (after the opening `[`) in **`site-data.js` only**. Do not edit any HTML file.

5. Entry format (include only non-empty optional fields):
```javascript
{
  slug: "the-slug",
  title: "The Title",
  venue: "Conference Name",
  date: "YYYY-MM-DD",
  year: YYYY,
  city: "City",
  duration: "30 min",
  featured: true,           // only if featured
  slides: "https://...",    // only if provided
  video: "https://...",     // only if provided
  thumbnail: "assets/thumbnails/the-slug.jpg",
  abstract: "One or two sentence description."
},
```

6. Confirm the entry was added and show it.
