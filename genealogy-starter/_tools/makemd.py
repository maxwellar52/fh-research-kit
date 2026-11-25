"""makemd.py — write the Markdown copy of a research log from data_<Name>.json.
Usage: python3 makemd.py data.json out.md"""
import sys, json, re
D = json.load(open(sys.argv[1], encoding='utf-8'))
L = []
cell = lambda s: str(s).replace('|', '\\|').replace('\n', ' ')
link = lambda s: re.sub(r'(https?://\S+)', r'<\1>', s)
L += ['# Ancestor Research Log', '', '*Genealogical Research and Source Tracking Worksheet*', '',
      f"**{D['header_line']}**", '', D['summary'], '']
def table(head, rows):
    L.append('| ' + ' | '.join(head) + ' |'); L.append('|' + '---|' * len(head))
    for r in rows: L.append('| ' + ' | '.join(link(cell(c)) for c in r) + ' |')
    L.append('')
L += ['## 1. Identification', '']; table(['Field', 'Details'], D['identification'])
L += ['## 2. Vital Events', '']; table(['Event', 'Date', 'Location and evidence'], D['vital_events'])
L += ['## 3. Spouse(s)', '']; table(['Spouse Name', 'Marriage Date and Location / Notes'], D['spouses'])
L += ['## 4. Child(ren)', '']; table(['Child Name', 'Identification and Notes'], D['children'])
L += ['## 5. Sources', '', D['sources_note'], '']
table(['#', 'Source Citation', 'Repository / URL', 'Attached in FS? (Y/N)', 'Date Accessed', 'Findings / Notes'], D['sources'])
L += ['## 6. Research Notes', '']
for h, ps in D['notes']:
    L += [f'### {h}', ''] + [link(p) + '\n' for p in ps]
L += ['### Searches performed', '']
table(['Site / collection', 'Search terms', 'Result'], D['searches'])
L += ['## 7. Tree Actions Suggested', '', D['tree_intro'], '']
for i, (t, steps) in enumerate(D['tree_actions'], 1):
    L += [f'### {i}. {t}', ''] + [f'- {link(s)}' for s in steps] + ['']
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(L))
print('saved', sys.argv[2])
