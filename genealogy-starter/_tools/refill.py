"""refill.py — rebuild an Ancestor Research Log by refilling an existing log .docx
(7 sections, 6-column Sources table) from data_<Name>.json.
Usage: python3 refill.py base.docx data.json out.docx
"""
import sys, json, re, copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

# A URL ends before spaces and before a final . , ; : ) or ] so that punctuation stays outside the link.
URL_RE = re.compile(r'(https?://[^\s<>]+[^\s<>.,;:)\]])')
base, data_path, out = sys.argv[1:4]
D = json.load(open(data_path, encoding='utf-8'))
doc = Document(base)
body = doc.element.body
LINK_RPR = None


def run_xml(text, rpr):
    r = OxmlElement('w:r')
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def link_xml(part, url):
    rid = part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
    h.append(run_xml(url, LINK_RPR))
    return h


def fill_p(p_el, text, part, rpr):
    """Clear paragraph content (keep pPr) and write text with clickable URLs."""
    for ch in list(p_el):
        if ch.tag != qn('w:pPr'):
            p_el.remove(ch)
    pos = 0
    for m in URL_RE.finditer(text):
        if m.start() > pos:
            p_el.append(run_xml(text[pos:m.start()], rpr))
        p_el.append(link_xml(part, m.group(1)))
        pos = m.end()
    if pos < len(text):
        p_el.append(run_xml(text[pos:], rpr))


def first_rpr(p_el, idx=0):
    rs = [r for r in p_el.findall(qn('w:r')) if r.find(qn('w:t')) is not None]
    if not rs:
        return None
    rp = rs[min(idx, len(rs) - 1)].find(qn('w:rPr'))
    return copy.deepcopy(rp) if rp is not None else None


# capture hyperlink run format
for h in body.iter(qn('w:hyperlink')):
    LINK_RPR = copy.deepcopy(h.find(qn('w:r')).find(qn('w:rPr')))
    break

# Show links blue and underlined so they read as clickable in Word and PDF.
if LINK_RPR is None or len(LINK_RPR) == 0:
    LINK_RPR = OxmlElement('w:rPr')
    for tag, val in (('w:color', '0563C1'), ('w:u', 'single')):
        el = OxmlElement(tag); el.set(qn('w:val'), val); LINK_RPR.append(el)

part = doc.part
paras = doc.paragraphs
# Header block: paragraphs 2 and 3
fill_p(paras[2]._p, D['header_line'], part, first_rpr(paras[2]._p))
fill_p(paras[3]._p, D['summary'], part, first_rpr(paras[3]._p))

# Footer
for sec in doc.sections:
    for fp in sec.footer.paragraphs:
        if fp.text.strip():
            fill_p(fp._p, D['footer'], sec.footer.part, first_rpr(fp._p))


def fill_table(tbl, rows, link_cols=()):
    trs = tbl._tbl.findall(qn('w:tr'))
    tmpl = copy.deepcopy(trs[1])
    for tr in trs[1:]:
        tbl._tbl.remove(tr)
    for row in rows:
        tr = copy.deepcopy(tmpl)
        for ci, tc in enumerate(tr.findall(qn('w:tc'))):
            ps = tc.findall(qn('w:p'))
            for extra in ps[1:]:
                tc.remove(extra)
            p = ps[0]
            rpr = first_rpr(p) if ci not in link_cols else first_rpr(trs[1].findall(qn('w:tc'))[0].find(qn('w:p')))
            val = str(row[ci]) if ci < len(row) else ''
            fill_p(p, val, part, rpr)
        tbl._tbl.append(tr)


t = doc.tables
fill_table(t[0], D['identification'])
fill_table(t[1], D['vital_events'])
fill_table(t[2], D['spouses'])
fill_table(t[3], D['children'])
fill_table(t[4], D['sources'], link_cols=(2,))

# Sources note (paragraph just before Sources table)
prev = t[4]._tbl.getprevious()
fill_p(prev, D['sources_note'], part, first_rpr(prev))

# Rebuild everything after the Sources table
els = list(body.iterchildren())
start = els.index(t[4]._tbl) + 1
tail = [e for e in els[start:] if e.tag == qn('w:p')]
sectPr = body.find(qn('w:sectPr'))
from docx.text.paragraph import Paragraph
P = [Paragraph(e, doc) for e in tail]
def find(pred):
    return next(p._p for p in P if pred(p))
H1 = find(lambda p: p.style.name == 'Heading 1')
H2 = find(lambda p: p.style.name == 'Heading 2')
NORMAL = find(lambda p: p.style.name == 'Normal' and p.text.startswith('Proven ='))
SITE = find(lambda p: p.style.name == 'Normal' and p.runs and p.runs[0].bold and not p.text.startswith('Search terms'))
TERMS = find(lambda p: p.text.startswith('Search terms:'))
STEP = find(lambda p: p.text.startswith('Step 1.'))
INTRO = find(lambda p: p.text.startswith('Suggestions for you'))
protos = {k: copy.deepcopy(v) for k, v in dict(H1=H1, H2=H2, N=NORMAL, SITE=SITE, TERMS=TERMS, STEP=STEP, INTRO=INTRO).items()}
for e in tail:
    body.remove(e)


def add(kind, text, rpr_idx=0):
    p = copy.deepcopy(protos[kind])
    fill_p(p, text, part, first_rpr(protos[kind], rpr_idx))
    sectPr.addprevious(p)
    return p


add('H1', 'Research Notes')
for head, paras_ in D['notes']:
    add('H2', head)
    for tx in paras_:
        add('N', tx)
add('H2', 'Searches performed')
for site, terms, result in D['searches']:
    add('SITE', site)
    p = copy.deepcopy(protos['TERMS'])
    for ch in list(p):
        if ch.tag != qn('w:pPr'):
            p.remove(ch)
    p.append(run_xml('Search terms: ', first_rpr(protos['TERMS'], 0)))
    rest = f'{terms}. {result}' if terms != '—' else f'—. {result}'
    tmp = OxmlElement('w:p'); fill_p(tmp, rest, part, first_rpr(protos['TERMS'], 1))
    for ch in list(tmp):
        p.append(ch)
    sectPr.addprevious(p)
add('H1', 'Tree Actions Suggested')
add('INTRO', D['tree_intro'])
for i, (title, steps) in enumerate(D['tree_actions'], 1):
    add('H2', f'{i} {title}')
    for s in steps:
        add('STEP', s)

def prune_links(p):
    """Drop link records the text no longer uses (left over from the base file)."""
    used = set(re.findall(r'r:id="(rId\d+)"', p._element.xml))
    for rid in [k for k, r in p.rels.items() if r.reltype == RT.HYPERLINK and k not in used]:
        p.rels.pop(rid)


prune_links(doc.part)
for sec in doc.sections:
    prune_links(sec.footer.part)
doc.save(out)
print('saved', out)
