"""evaluate.py — build a Family Evaluation (.docx, .md and, on a Mac with Word, .pdf)
from evaldata_<Father>.json, using the Ancestor Research Log template's styles.

Usage:  python3 evaluate.py evaldata.json "<out folder>/<file base name>" [--pdf]

The JSON holds:
  header_line, summary, footer                       strings
  couple:    [[Person, PID, Verdict, Evidence / problems], ...]
  children:  [[#, Child, PID, Verdict, Evidence / problems], ...]
  mixed:     [paragraph, ...]                        (other families / wrong attachments)
  checks:    [{"heading": str, "paras": [str], "table": {"head": [..], "rows": [[..]]}}, ...]
  searches:  [[Site / collection, Search terms, Result], ...]
  tree_intro: str
  tree_actions: [[title, [step, ...]], ...]
  unresolved: [str, ...]
Text may use **bold**. Every http(s) URL becomes a clickable link in Word and PDF.
"""
import sys, json, re, copy, subprocess
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Pt, Inches

TOOLS = Path(__file__).resolve().parent
TEMPLATE = TOOLS / 'base' / 'Ancestor_Research_Log_TEMPLATE.docx'
TOKEN_RE = re.compile(r'(https?://[^\s<>|]+[^\s<>|.,;:)\]])|\*\*(.+?)\*\*')
HEAD_FILL = 'D9E2F3'
CELL_SZ = '19'  # half-points, as in the log tables

data_path, out_base = sys.argv[1], sys.argv[2]
want_pdf = '--pdf' in sys.argv
D = json.load(open(data_path, encoding='utf-8'))
doc = Document(str(TEMPLATE))
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
for el in list(body):
    if el is not sectPr:
        body.remove(el)
part = doc.part


def _run(text, bold=False, size=None, link=False):
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    if bold:
        rpr.append(OxmlElement('w:b'))
    if link:
        c = OxmlElement('w:color'); c.set(qn('w:val'), '0563C1'); rpr.append(c)
        u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rpr.append(u)
    if size:
        s = OxmlElement('w:sz'); s.set(qn('w:val'), size); rpr.append(s)
    r.append(rpr)
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def write(p_el, text, bold=False, size=None, the_part=None):
    """Append text to a w:p, turning URLs into hyperlinks and **x** into bold."""
    the_part = the_part or part
    pos = 0
    for m in TOKEN_RE.finditer(text):
        if m.start() > pos:
            p_el.append(_run(text[pos:m.start()], bold, size))
        if m.group(1):
            rid = the_part.relate_to(m.group(1), RT.HYPERLINK, is_external=True)
            h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
            h.append(_run(m.group(1), bold, size, link=True))
            p_el.append(h)
        else:
            p_el.append(_run(m.group(2), True, size))
        pos = m.end()
    if pos < len(text):
        p_el.append(_run(text[pos:], bold, size))


def para(text, style='Normal', bold=False):
    p = doc.add_paragraph(style=style)
    write(p._p, text, bold)
    return p


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), fill)
    tcPr.append(sh)


def table(head, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(head))
    t.style = doc.styles['Table Grid']
    t.autofit = False
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]; shade(c, HEAD_FILL)
        write(c.paragraphs[0]._p, h, bold=True, size=CELL_SZ)
    for r in rows:
        cells = t.add_row().cells
        for i in range(len(head)):
            write(cells[i].paragraphs[0]._p, str(r[i]) if i < len(r) else '', size=CELL_SZ)
    if not widths:  # share the page width, giving the last column the rest
        n = len(head); widths = [1.3] * (n - 1) + [7.3 - 1.3 * (n - 1)]
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = Inches(widths[i])
    doc.add_paragraph()
    return t


# Header block (same look as the research log)
para('Family Evaluation', 'Title')
para('Parents and Children Check — FamilySearch Family Tree')
para(D['header_line'], bold=True)
para(D['summary'])
para('Proven = direct record evidence; Probable = strong indirect evidence; Possible = some evidence, not yet tested.')

para('The Couple', 'Heading 1')
table(['Person', 'PID', 'Verdict', 'Evidence / problems'], D['couple'], [1.3, 0.9, 1.1, 4.0])

para('Children', 'Heading 1')
table(['#', 'Child', 'PID', 'Verdict', 'Evidence / problems'], D['children'], [0.35, 1.3, 0.9, 1.05, 3.7])

para('Mixed-in Families and Wrong Attachments', 'Heading 1')
for tx in D['mixed']:
    para(tx)

para('Extra Checks', 'Heading 1')
for ch in D['checks']:
    para(ch['heading'], 'Heading 2')
    for tx in ch.get('paras', []):
        para(tx)
    if ch.get('table'):
        table(ch['table']['head'], ch['table']['rows'])

para('Searches Performed', 'Heading 1')
table(['Site / collection', 'Search terms', 'Result'], D['searches'], [1.8, 2.5, 3.0])

para('Tree Actions Suggested', 'Heading 1')
para(D['tree_intro'])
for i, (title, steps) in enumerate(D['tree_actions'], 1):
    para(f'{i} {title}', 'Heading 2')
    for s in steps:
        para(s)

para('Unresolved Questions', 'Heading 1')
for tx in D['unresolved']:
    para('• ' + tx)

# Footer
for sec in doc.sections:
    for fp in sec.footer.paragraphs:
        if fp.text.strip():
            for ch in list(fp._p):
                if ch.tag != qn('w:pPr'):
                    fp._p.remove(ch)
            write(fp._p, D['footer'], the_part=sec.footer.part)

out_docx = Path(out_base + '.docx')
doc.save(str(out_docx))
print('saved', out_docx)

# Markdown copy
cell = lambda s: str(s).replace('|', '\\|').replace('\n', ' ')
link = lambda s: re.sub(r'(?<!<)(https?://[^\s<>|]+[^\s<>|.,;:)\]])', r'<\1>', s)
L = ['# Family Evaluation', '', '*Parents and Children Check — FamilySearch Family Tree*', '',
     f"**{D['header_line']}**", '', link(D['summary']), '']
def mdt(head, rows):
    L.append('| ' + ' | '.join(head) + ' |'); L.append('|' + '---|' * len(head))
    for r in rows:
        L.append('| ' + ' | '.join(link(cell(c)) for c in r) + ' |')
    L.append('')
L += ['## 1. The Couple', '']; mdt(['Person', 'PID', 'Verdict', 'Evidence / problems'], D['couple'])
L += ['## 2. Children', '']; mdt(['#', 'Child', 'PID', 'Verdict', 'Evidence / problems'], D['children'])
L += ['## 3. Mixed-in Families and Wrong Attachments', ''] + [link(t) + '\n' for t in D['mixed']]
L += ['## 4. Extra Checks', '']
for ch in D['checks']:
    L += [f"### {ch['heading']}", ''] + [link(t) + '\n' for t in ch.get('paras', [])]
    if ch.get('table'):
        mdt(ch['table']['head'], ch['table']['rows'])
L += ['## 5. Searches Performed', '']; mdt(['Site / collection', 'Search terms', 'Result'], D['searches'])
L += ['## 6. Tree Actions Suggested', '', link(D['tree_intro']), '']
for i, (t, steps) in enumerate(D['tree_actions'], 1):
    L += [f'### {i}. {t}', ''] + [f'- {link(s)}' for s in steps] + ['']
L += ['## 7. Unresolved Questions', ''] + [f'- {link(t)}' for t in D['unresolved']]
out_md = Path(out_base + '.md')
out_md.write_text('\n'.join(L) + '\n', encoding='utf-8')
print('saved', out_md)

if want_pdf:
    out_pdf = out_docx.with_suffix('.pdf')
    script = f'''
tell application "Microsoft Word"
    set d to open file name (POSIX file "{out_docx.resolve()}" as text)
    save as d file name (POSIX file "{out_pdf.resolve()}" as text) file format format PDF
    close d saving no
end tell'''
    try:
        subprocess.run(['osascript', '-e', script], check=True, capture_output=True, text=True, timeout=180)
        print('saved', out_pdf)
    except Exception as e:  # Windows or no Word: fall back to LibreOffice
        try:
            subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(out_docx.parent), str(out_docx)],
                           check=True, timeout=180)
            print('saved', out_pdf)
        except Exception as e2:
            print('PDF NOT MADE — open the .docx in Word and Save as PDF.', e, e2)
