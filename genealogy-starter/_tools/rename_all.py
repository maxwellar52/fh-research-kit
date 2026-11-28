"""rename_all.py — rename every person's research log and story to the new style:
    Log_<Full Name>, <birth year>–<death year>.docx/.pdf
    Story_<Full Name>, <birth year>–<death year>.docx/.pdf
e.g. Log_Mary Ann Smith (Jones), 1859–1925.pdf

The name and years come from each person's json_data/data_<Name>.json
(the story title, or the log header line). The JSON is updated to match, and the
story title changes from "The Life of ..." to "Life of ..." (the heading inside an
existing story document changes only when the story is next rebuilt).

Superseded/ folders, People lists, "-1" duplicates and Claude outputs/ are left alone.

Usage (from Terminal):
    python3 rename_all.py /path/to/Genealogy            # dry run: shows what would change
    python3 rename_all.py /path/to/Genealogy --apply    # does it, and writes _tools/rename_log.txt
"""
import sys, os, re, json, glob

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else
                       os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
apply = '--apply' in sys.argv
DASH = '–'
out, problems = [], []


def base_name(d):
    """'Mary Ann Smith (Jones), 1859–1925' from the JSON."""
    t = (d.get('story') or {}).get('title_line') or ''
    m = re.match(r'^(?:The )?Life of (.+?), ((?:abt )?\d{4}' + DASH + r'.+)$', t)
    if m:
        name, years = m.group(1), m.group(2)
    else:
        h = d.get('header_line', '').split('•')[0].strip()
        m = re.match(r'^(.+?) ((?:abt )?\d{4}' + DASH + r'\S+(?: \d{4})?)$', h)
        if not m:
            return None
        name, years = m.group(1), m.group(2)
    # '?' is not allowed in file names on Windows, so an unknown death year is 'unknown'
    years = years.replace(DASH + 'Deceased', DASH + 'unknown').replace(DASH + '?', DASH + 'unknown')
    return f'{name}, {years}'


for jp in sorted(glob.glob(os.path.join(root, '*', '*', 'json_data', 'data_*.json'))):
    if re.search(r'-\d+\.json$', jp) or '/._' in jp or '\\._' in jp:
        continue
    folder = os.path.dirname(os.path.dirname(jp))
    rel = os.path.relpath(folder, root)
    try:
        d = json.load(open(jp, encoding='utf-8'))
    except Exception as e:
        problems.append(f'{rel}: could not read JSON ({e})'); continue
    base = base_name(d)
    if not base:
        problems.append(f'{rel}: no name/years found in JSON; skipped'); continue
    for kind, pats in (('Log', ('Ancestor_Research_Log_', 'Log_')), ('Story', ('Ancestor_Story_', 'Story_'))):
        for ext in ('.docx', '.pdf'):
            new = f'{kind}_{base}{ext}'
            cands = [f for f in os.listdir(folder)
                     if f.endswith(ext) and not f.startswith('._') and f != new
                     and f.startswith(pats) and not re.search(r'-\d+' + re.escape(ext) + '$', f)]
            if not cands:
                continue
            if len(cands) > 1:
                problems.append(f'{rel}: more than one {kind} {ext} ({", ".join(cands)}); skipped'); continue
            if os.path.exists(os.path.join(folder, new)):
                problems.append(f'{rel}: {new} already exists; {cands[0]} left as is'); continue
            out.append(f'{rel}:  {cands[0]}  ->  {new}')
            if apply:
                os.rename(os.path.join(folder, cands[0]), os.path.join(folder, new))
    # JSON
    changed = False
    if d.get('file') != f'Log_{base}':
        d['file'] = f'Log_{base}'; changed = True
    s = d.get('story')
    if s:
        if s.get('file') != f'Story_{base}':
            s['file'] = f'Story_{base}'; changed = True
        if s.get('title_line') != f'Life of {base}':
            s['title_line'] = f'Life of {base}'; changed = True
    te = d.get('tracker_entry')
    if te and te.get('Log file') != f'Log_{base}.docx':
        te['Log file'] = f'Log_{base}.docx'; changed = True
    if changed:
        out.append(f'{rel}:  JSON updated ({os.path.basename(jp)})')
        if apply:
            with open(jp, 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False, indent=1)

print(('APPLIED' if apply else 'DRY RUN (nothing changed; add --apply to do it)') + f' — {root}\n')
print('\n'.join(out) or 'Nothing to rename.')
if problems:
    print('\nCheck these:\n' + '\n'.join(problems))
if any('JSON updated' in line for line in out):
    print('\nThe tracker spreadsheet is not changed by this script. ' +
          ('Run tracker.py for each person whose JSON was updated, ' if apply else 'After --apply, run tracker.py for each person whose JSON is updated, ') +
          'e.g.  python3 tracker.py ../_AAResearch_Tracker.xlsx "<person folder>/json_data/data_<Name>.json"')
if apply:
    with open(os.path.join(root, '_tools', 'rename_log.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out + [''] + problems))
