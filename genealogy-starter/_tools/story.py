"""story.py — write the Ancestor Story (.docx and .md) from the "story" section of data_<Name>.json,
using the person's research log .docx as the style base (same fonts, colours, margins, footer).
Usage: python3 story.py log.docx data.json out_base      -> out_base.docx, out_base.md
Then make the PDF as for the logs:  soffice --headless --convert-to pdf out_base.docx

JSON "story" keys: header_line, title_line ("Life of <Full Name>, <years>", no "The"), relationship (FamilySearch
  View My Relationship wording with the researcher's name in place of you/my), living, footer, written,
  sections [[heading, [paragraphs]]], open_questions [..],
  related_sources {"KEY": [short, url, note]}, context_sources {"C1": [short, url, note]}.
Citation markers in paragraphs: {S12} = this log's source 12; {GWS:S8} or {C1} = related/context source.
Notes are numbered in order of first use; a source cited again reuses its number.
"""
import sys, json, re, copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

base, data_path, out = sys.argv[1:4]
D = json.load(open(data_path, encoding='utf-8'))
S = D['story']
MARK = re.compile(r'((?:\{[A-Za-z0-9:]+\})+)')
URL_RE = re.compile(r'(https?://\S+?)(?=\s|$)')

# ---- note numbering -------------------------------------------------------
src = {f"S{r[0]}": r for r in D['sources']}
other = {**S.get('related_sources', {}), **S.get('context_sources', {})}
order, notes = {}, []


def short_of(key):
    if key in src:
        r = src[key]
        m = re.search(r'[“"](.+?)[,]?[”"]', r[1])
        title = ((r[1][:m.start()].strip() + ' ' + m.group(1)).strip() if m else r[1].split(',')[0]).rstrip(',')
        return title, r[2], f'Research Log {key}'
    if key in other:
        return tuple(other[key])
    raise KeyError(f'unknown citation {{{key}}}')


def nums(group):
    out = []
    for key in re.findall(r'\{([A-Za-z0-9:]+)\}', group):
        if key not in order:
            order[key] = len(order) + 1
            notes.append((order[key], *short_of(key)))
        out.append(str(order[key]))
    return ','.join(out)


def split(text):
    """-> list of (text, is_superscript)"""
    parts = []
    for i, piece in enumerate(MARK.split(text)):
        if piece:
            parts.append((nums(piece), True) if i % 2 else (piece, False))
    return parts


# ---- docx helpers (same approach as refill.py) ----------------------------
doc = Document(base)
body = doc.element.body
part = doc.part
LINK_RPR = None
for h in body.iter(qn('w:hyperlink')):
    LINK_RPR = copy.deepcopy(h.find(qn('w:r')).find(qn('w:rPr')))
    break

# Links in the story are shown blue and underlined so they read as clickable
# (the base log's own hyperlinks carry no visible style).
if LINK_RPR is None or len(LINK_RPR) == 0:
    LINK_RPR = OxmlElement('w:rPr')
    for tag, val in (('w:color', '0563C1'), ('w:u', 'single')):
        el = OxmlElement(tag); el.set(qn('w:val'), val); LINK_RPR.append(el)


def run_xml(text, rpr, sup=False, italic=False):
    r = OxmlElement('w:r')
    rp = copy.deepcopy(rpr) if rpr is not None else OxmlElement('w:rPr')
    if sup:
        v = OxmlElement('w:vertAlign'); v.set(qn('w:val'), 'superscript'); rp.append(v)
    if italic:
        rp.append(OxmlElement('w:i'))
    r.append(rp)
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def add_text(p_el, text, rpr, italic=False):
    pos = 0
    for m in URL_RE.finditer(text):
        if m.start() > pos:
            p_el.append(run_xml(text[pos:m.start()], rpr, italic=italic))
        rid = part.relate_to(m.group(1), RT.HYPERLINK, is_external=True)
        h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
        h.append(run_xml(m.group(1), LINK_RPR)); p_el.append(h)
        pos = m.end()
    if pos < len(text):
        p_el.append(run_xml(text[pos:], rpr, italic=italic))


def first_rpr(p_el):
    for r in p_el.findall(qn('w:r')):
        if r.find(qn('w:t')) is not None:
            rp = r.find(qn('w:rPr'))
            return copy.deepcopy(rp) if rp is not None else None
    return None


from docx.text.paragraph import Paragraph
P = doc.paragraphs
protos = {'TITLE': P[0]._p, 'SUB': P[1]._p, 'BOLD': P[2]._p, 'N': P[3]._p,
          'H1': next(p._p for p in P if p.style.name == 'Heading 1'),
          'H2': next(p._p for p in P if p.style.name == 'Heading 2')}
protos = {k: copy.deepcopy(v) for k, v in protos.items()}
sectPr = body.find(qn('w:sectPr'))
for el in list(body):
    if el is not sectPr:
        body.remove(el)


def add(kind, parts, italic=False):
    p = copy.deepcopy(protos[kind])
    rpr = first_rpr(protos[kind])
    for ch in list(p):
        if ch.tag != qn('w:pPr'):
            p.remove(ch)
    if isinstance(parts, str):
        parts = [(parts, False)]
    for text, sup in parts:
        if sup:
            p.append(run_xml(text, rpr, sup=True))
        else:
            add_text(p, text, rpr, italic)
    sectPr.addprevious(p)


for sec in doc.sections:
    for fp in sec.footer.paragraphs:
        if fp.text.strip():
            rpr = first_rpr(fp._p)
            for ch in list(fp._p):
                if ch.tag != qn('w:pPr'):
                    fp._p.remove(ch)
            fp._p.append(run_xml(S['footer'], rpr))

# ---- build ----------------------------------------------------------------
GEN = (f"This story was generated on {S['written']} using Claude AI, which also generated the "
       "Notes section with the URL's to sources researched for this story.")
md = [f"# {S['title_line']}", '', f'*{GEN}*', '']
add('TITLE', S['title_line'])
add('SUB', GEN)
if S.get('living'):
    add('BOLD', 'LIVING – do not upload to Memories'); md += ['**LIVING – do not upload to Memories**', '']
add('BOLD', S['header_line']); md += [f"**{S['header_line']}**", '']
add('N', S['relationship'], italic=True); md += [f"*{S['relationship']}*", '']


def md_text(parts):
    return ''.join(f'<sup>{t}</sup>' if s else t for t, s in parts)


for head, paras in S['sections']:
    add('H1', head); md += [f'## {head}', '']
    for tx in paras:
        parts = split(tx)
        add('N', parts); md += [md_text(parts), '']

add('H1', 'Open Questions'); md += ['## Open Questions', '']
for q in S['open_questions']:
    parts = split(q)
    add('N', [('•  ', False)] + parts); md += [f'- {md_text(parts)}']
md.append('')

key_line = ('How to read this story: facts stated plainly are Proven; “likely” or “very likely” marks Probable facts; '
            '“may have” marks Possible ones. Full citations are in ' + D['file'] + '.')
add('H1', 'Notes'); md += ['## Notes', '']
for n, title, url, where in notes:
    line = f'{n}. {title}, {url} ({where}).'
    add('N', line); md += [f'{n}. {title}, <{url}> ({where}).']
md.append('')
add('N', key_line, italic=True); md += [f'*{key_line}*', '']

doc.save(out + '.docx')
open(out + '.md', 'w', encoding='utf-8').write('\n'.join(md))
print('saved', out + '.docx', out + '.md', f'({len(notes)} notes)')
