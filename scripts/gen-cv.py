#!/usr/bin/env python3
"""Generate resume.pdf from resume.html.
Run: python3 scripts/gen-cv.py
Output: resume.pdf (project root, already linked from resume.html)
"""
import os, re, sys
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "resume.html")
OUT  = os.path.join(BASE, "resume.pdf")

W, H      = A4                  # 595 x 842 pt
M_LR      = 1.8 * cm            # left/right margin
M_TB      = 1.5 * cm            # top/bottom margin
COL_DATE  = 2.3 * cm
COL_GAP   = 0.4 * cm
COL_BODY  = W - 2*M_LR - COL_DATE - COL_GAP

INK    = HexColor('#1a1815')
INK2   = HexColor('#4a463e')
INK3   = HexColor('#7a7468')
ACCENT = HexColor('#D97757')
RULE_C = HexColor('#d9d3c4')

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=8, leading=11,
                    textColor=INK, spaceAfter=0, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

STYLES = {
    'name':       S('name', fontName='Times-Roman', fontSize=22, leading=26,
                    textColor=INK, spaceAfter=3),
    'tagline':    S('tagline', fontSize=8.5, leading=12, textColor=INK2, spaceAfter=2),
    'contact':    S('contact', fontSize=7.5, leading=10, textColor=INK3),
    'sec_head':   S('sec_head', fontName='Helvetica-Bold', fontSize=7, leading=9,
                    textColor=ACCENT, spaceBefore=8, spaceAfter=4),
    'date':       S('date', fontSize=7.5, leading=10, textColor=INK3, alignment=TA_LEFT),
    'title':      S('title', fontName='Helvetica-Bold', fontSize=9, leading=12,
                    textColor=INK, spaceAfter=1),
    'company':    S('company', fontSize=8.5, leading=11, textColor=INK2, spaceAfter=2),
    'desc':       S('desc', fontName='Helvetica-Oblique', fontSize=8, leading=11,
                    textColor=INK3, spaceAfter=2),
    'subsec':     S('subsec', fontName='Helvetica-Bold', fontSize=7, leading=9,
                    textColor=INK3, spaceBefore=5, spaceAfter=2),
    'bullet':     S('bullet', fontSize=8, leading=11, textColor=INK,
                    leftIndent=7, firstLineIndent=-7, spaceAfter=1.5),
    'skill_lbl':  S('skill_lbl', fontName='Helvetica-Bold', fontSize=7.5, leading=10,
                    textColor=INK3),
    'skill_val':  S('skill_val', fontSize=8, leading=11, textColor=INK, spaceAfter=4),
}


# ── HTML helpers ──────────────────────────────────────────────────────────────
def strip(s):
    s = re.sub(r'<[^>]+>', '', s)
    for e, r in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&nbsp;', ' '),
                 ('&mdash;', '-'), ('&#8212;', '-')]:
        s = s.replace(e, r)
    return re.sub(r'\s+', ' ', s).strip()

def bullets_from(ul_html):
    return [strip(m.group(1))
            for m in re.finditer(r'<li[^>]*>(.*?)</li>', ul_html, re.DOTALL)]


# ── Parse resume.html ─────────────────────────────────────────────────────────
def parse():
    with open(HTML) as f:
        html = f.read()

    data = {'name': '', 'tagline': '', 'contact': [], 'sections': []}

    # Name
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    data['name'] = m.group(1).strip() if m else 'Zhanibek Marshal'

    # Tagline from hero <p>
    hero = re.search(r'class="hero"[^>]*>(.*?)</section>', html, re.DOTALL)
    if hero:
        p = re.search(r'<p[^>]*>(.*?)</p>', hero.group(1), re.DOTALL)
        if p:
            data['tagline'] = strip(p.group(1))

    # Contact links (skip the PDF link)
    dl = re.search(r'class="download-row">(.*?)</div>', html, re.DOTALL)
    if dl:
        for m in re.finditer(r'href="([^"]+)"[^>]*>([^<]+)<', dl.group(1)):
            href, txt = m.group(1), m.group(2).strip()
            if '.pdf' not in href:
                data['contact'].append(txt.lstrip('✉ ').lstrip('↓ ').strip())

    # Sections
    for sec_m in re.finditer(
            r'<div class="resume-section">(.*?)(?=<div class="resume-section">|</main>)',
            html, re.DOTALL):
        sec_html = sec_m.group(1)
        h2 = re.search(r'<h2>([^<]+)</h2>', sec_html)
        if not h2:
            continue
        sec_name = h2.group(1)
        entries  = []

        for grid_m in re.finditer(
                r'<div class="resume-grid">(.*?)(?=<div class="resume-grid">|</div>\s*</div>)',
                sec_html, re.DOTALL):
            g = grid_m.group(1)

            when_m = re.search(r'<div class="when">([^<]+)</div>', g)
            when   = when_m.group(1).strip() if when_m else ''

            what_m = re.search(r'<div class="what">(.*)', g, re.DOTALL)
            if not what_m:
                continue
            what = what_m.group(1)

            h3    = re.search(r'<h3[^>]*>([^<]+)</h3>', what)
            where = re.search(r'<div class="where">([^<]+)</div>', what)
            title   = h3.group(1).strip()    if h3    else ''
            company = where.group(1).strip() if where else ''

            # Check for sub-sections (Trade Republic style)
            # Sub-section headers are <p style="...mono...">sub · date</p>
            subsecs = []
            parts   = re.split(r'(<p[^>]*font-family[^>]*mono[^>]*>.*?</p>)', what, flags=re.DOTALL)
            desc    = ''
            if len(parts) == 1:
                # No sub-sections: optional plain <p> description + single <ul>
                dp = re.search(r'<p(?![^>]*mono)[^>]*>(.*?)</p>', what, re.DOTALL)
                if dp:
                    desc = strip(dp.group(1))
                ul = re.search(r'<ul>(.*?)</ul>', what, re.DOTALL)
                bullets = bullets_from(ul.group(1)) if ul else []
                entries.append({
                    'when': when, 'title': title, 'company': company,
                    'desc': desc, 'subsecs': [], 'bullets': bullets
                })
            else:
                # Has sub-sections
                for i in range(1, len(parts), 2):
                    sub_label = strip(parts[i])
                    block     = parts[i + 1] if i + 1 < len(parts) else ''
                    ul        = re.search(r'<ul>(.*?)</ul>', block, re.DOTALL)
                    sub_bullets = bullets_from(ul.group(1)) if ul else []
                    subsecs.append({'label': sub_label, 'bullets': sub_bullets})
                entries.append({
                    'when': when, 'title': title, 'company': company,
                    'desc': '', 'subsecs': subsecs, 'bullets': []
                })

        if entries:
            data['sections'].append({'name': sec_name, 'entries': entries})

    # Skills section - parse separately (different HTML structure)
    skills_block = re.search(r'<div class="resume-skills">(.*?)</div>\s*</div>', html, re.DOTALL)
    if skills_block:
        skills = []
        for sg in re.finditer(r'<div class="skill-group">(.*?)</div>', skills_block.group(1), re.DOTALL):
            lbl = re.search(r'<div class="label">([^<]+)</div>', sg.group(1))
            val = re.search(r'<p[^>]*>([^<]+)</p>', sg.group(1))
            if lbl and val:
                skills.append((lbl.group(1).strip(), val.group(1).strip()))
        # Replace parsed Skills section with correct data
        for sec in data['sections']:
            if sec['name'] == 'Skills':
                sec['skills'] = skills

    return data


# ── Layout builders ───────────────────────────────────────────────────────────
def hr():
    return HRFlowable(width='100%', thickness=0.5, color=RULE_C, spaceAfter=6)

def p(text, style):
    return Paragraph(text, STYLES[style])

def grid_row(when_text, content_items, top_pad=2):
    """Two-column row: narrow date | wide content."""
    date_cell = [p(when_text, 'date')]
    content_cell = content_items
    t = Table(
        [[date_cell, content_cell]],
        colWidths=[COL_DATE, COL_BODY],
        hAlign='LEFT'
    )
    t.setStyle(TableStyle([
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING',   (0, 0), (-1, -1), top_pad),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 2),
    ]))
    return t

def bullet_para(text):
    return p(f'• {text}', 'bullet')


# ── Build PDF flowables ───────────────────────────────────────────────────────
def build_story(data):
    story = []

    # Header
    story.append(p(data['name'], 'name'))
    if data['tagline']:
        story.append(p(data['tagline'], 'tagline'))
    if data['contact']:
        story.append(p('  ·  '.join(data['contact']), 'contact'))
    story.append(Spacer(1, 4))
    story.append(hr())

    for sec in data['sections']:
        sec_name = sec['name']

        if sec_name == 'Skills':
            story.append(p(sec_name.upper(), 'sec_head'))
            skills = sec.get('skills', [])
            for lbl, val in skills:
                story.append(p(lbl.upper(), 'skill_lbl'))
                story.append(p(val, 'skill_val'))
            continue

        if sec_name == 'Publications':
            continue  # Omit from PDF; linked on website

        story.append(p(sec_name.upper(), 'sec_head'))

        for entry in sec['entries']:
            content = []

            if entry['title']:
                content.append(p(entry['title'], 'title'))
            if entry['company']:
                content.append(p(entry['company'], 'company'))
            if entry.get('desc'):
                content.append(p(entry['desc'], 'desc'))

            for ss in entry.get('subsecs', []):
                content.append(p(ss['label'], 'subsec'))
                for b in ss['bullets']:
                    content.append(bullet_para(b))

            for b in entry.get('bullets', []):
                content.append(bullet_para(b))

            row = grid_row(entry['when'], content)
            story.append(KeepTogether(row) if len(content) <= 4 else row)
            story.append(Spacer(1, 5))

    return story


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    data  = parse()
    story = build_story(data)

    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=M_LR, rightMargin=M_LR,
        topMargin=M_TB,  bottomMargin=M_TB,
        title=f"{data['name']} - CV",
        author=data['name'],
    )
    doc.build(story)

    # Report
    try:
        from PyPDF2 import PdfReader
        pages = len(PdfReader(OUT).pages)
    except ImportError:
        pages = '?'

    size_kb = os.path.getsize(OUT) // 1024
    print(f"resume.pdf written — {size_kb} KB", end='')
    if pages != '?':
        marker = ' ✓' if pages <= 2 else f' ⚠ ({pages} pages — trim content to fit 2)'
        print(f', {pages} page{"s" if pages != 1 else ""}{marker}')
    else:
        print()

if __name__ == '__main__':
    main()
