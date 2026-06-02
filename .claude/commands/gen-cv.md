Generate a polished 2-page PDF CV from resume.html, optionally tailored to a specific job posting.
Output: resume.pdf (linked from the resume page download button).

---

## Step 1 — Job posting (optional but recommended)

Ask the user:
> "Do you have a job posting URL or description to tailor this CV for?
> If yes, paste the URL or the text. If no, I'll generate a general-purpose CV."

**If a URL is provided:** fetch the page and extract:
- Role title and seniority
- Required skills / tech stack
- Key responsibilities
- Company name and domain (fintech, media, etc.)

**If no URL:** proceed with a general CV that leads with the strongest, most transferable bullets.

---

## Step 2 — Read current resume

Read `resume.html` and extract all content:
- Name, tagline, contact links
- All experience entries with bullets (all roles, all sub-sections)
- Skills, speaking highlights, education, certifications

---

## Step 3 — Gap analysis (only if job posting was provided)

Compare the job requirements against the resume content. Be honest — do not invent or exaggerate:

1. **Strong matches** — skills/experience clearly present in resume.html. List them.
2. **Partial matches** — relevant experience that isn't worded to match the JD. Flag these for rewording.
3. **Gaps** — requirements not covered at all. For each gap, ask the user:
   > "The JD asks for [X]. Do you have relevant experience with this that isn't on your current resume?"
   If yes, incorporate their answer. If no, note the gap but don't fabricate.

---

## Step 4 — STAR coaching for key bullets

For the **most relevant 3–4 bullets** (either by JD match or by recency), suggest STAR-enhanced rewrites.

For each bullet, ask:
- **Result**: Can you quantify this? (users, %, ms, money, team size, time saved)
- **Action**: Was your contribution individual or team-led? How much did *you* own?

Propose the rewrite. Wait for confirmation before using it.

STAR bullet formula:
> "[Strong verb] [specific thing you did] — [quantified result or scale]"

Examples:
- Before: "Launched Bizum end-to-end on Android from a blank slate"
- After: "Shipped Bizum (Spain instant payments) from zero to production — P2P, Request-to-Pay, e-commerce — serving [X]K users within [Y] months"

---

## Step 5 — 2-page plan

With the JD in mind, decide what leads and what gets trimmed. Target layout:

| Page | Content |
|------|---------|
| 1 | Header · Trade Republic (all 3 sub-sections, prioritised bullets) |
| 2 | Zattoo · Alfa-Bank · Kolesa (top 3–4 bullets) · Skills · Speaking (top 4) · Education |

Trim rules:
- Springfruit (2013–2014): company + role line only, no bullets
- iBEC Systems (2014–2015): 1 bullet max
- Speaking: keep top 4 most relevant to the JD (or most prestigious if no JD)
- Publications: omit (they're on the website)

**If a JD was provided:** re-order or emphasise bullets that match it. For example, if the role is infra-heavy, lead the Trade Republic section with observability/OpenTelemetry work rather than payments.

Show the proposed trim/reorder list to the user and ask for confirmation.

---

## Step 6 — Update resume.html (ask first)

> "Should I update resume.html with the STAR-enhanced bullets so the website and PDF stay in sync? Or keep the changes PDF-only?"

If the user says yes: edit the relevant `<li>` items in resume.html.
If no: proceed with changes only in memory for the PDF run.

---

## Step 7 — Generate PDF

Run the generation script:
```
python3 scripts/gen-cv.py
```

This reads resume.html, lays out the content, and writes resume.pdf.
The resume page already has `<a href="resume.pdf" download>↓ download pdf</a>` — no HTML change needed.

---

## Step 8 — Verify

```
ls -lh resume.pdf
```

Report:
- File size
- Page count (should be 2; if more, propose specific cuts)
- Which JD keywords are now present in the PDF (if a posting was provided)
