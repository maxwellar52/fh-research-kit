# Genealogy folder: working rules

The researcher's name and this folder's location are in `genealogy_config.json`. Wherever the skills say `<Researcher Name>`, use `researcher_name` from that file.

## Folder structure

```
Genealogy/
├── CLAUDE.md                    ← these rules
├── genealogy_config.json        ← your name and this folder's path
├── _AAResearch_Tracker.xlsx     ← the only tracker file; always in this top folder
├── _tools/                      ← scripts: refill.py, makemd.py, tracker.py, story.py
│   ├── base/                    ← blank template the scripts start from
│   └── examples/                ← a fictional data file showing the format
├── Claude outputs/              ← files produced by Claude
├── <Surname> Family/            ← one folder per surname
│   └── <Full Name> <PID>/       ← one folder per person, e.g. John Smith ABCD-123
│       ├── json_data/data_<Full Name>.json
│       ├── Log_<Full Name>, <birth year>–<death year>.docx / .pdf
│       ├── Story_<Full Name>, <birth year>–<death year>.docx / .pdf
│       └── Superseded/          ← older versions, dated
└── XXNot in my line/            ← people FamilySearch shows as not related
```

- Save each person's files in a "<Full Name> <PID>" folder inside the matching "<Surname> Family" folder. Folder names leave out the married name in parentheses.
- If a surname folder already exists, reuse it. Do not create a second one.
- A spouse who is related by marriage goes in a "<Their Surname> Family" folder under their own surname, not in "XXNot in my line".
- Keep only one tracker file, `_AAResearch_Tracker.xlsx`, in the top Genealogy folder, never in a subfolder. Update it whenever a log or story is created or replaced.

## Naming

- Log files: `Log_<Full Name>, <birth year>–<death year>`
- Story files: `Story_<Full Name>, <birth year>–<death year>`
- Story heading: `Life of <Full Name>, <birth year>–<death year>` (no "The" at the start)
- Example: `Story_Mary Ann Smith (Jones), 1859–1925`

## Scripts

Logs are built with `_tools/refill.py` from `_tools/base/Ancestor_Research_Log_TEMPLATE.docx`. Run `makemd.py`, `tracker.py` and `story.py` from `_tools` as needed. Make PDFs from the .docx files with LibreOffice (`soffice --headless --convert-to pdf`) or Microsoft Word.

Older versions of files are kept in each person's `Superseded/` folder. Do not delete anything there. `cleanup_superseded.py` and `rename_all.py` also exist in `_tools`. Ask the user before running either one.

## Research logs

- Every log follows the seven-section layout, including a "Searches performed" section.
- Cite every source, with clickable URLs.
- Show conflicting evidence where it exists.
- Recommend FamilySearch tree actions, but do not make them.
- Rate evidence as Proven, Probable or Possible.
- Flag unresolved questions. Do not present them as fact.

## Rules for the user

- The user makes all FamilySearch edits personally. Suggest changes only.
- Check whether a person is related with FamilySearch's View My Relationship. If it shows a relationship, never say the people are not related.
- Add your own tree-specific rules here (for example, "Do not merge <PID> with <PID> without sufficient evidence").

## Output style

- Show each story revision as "(rev. N)" in story headers and page footers, not "(revised N times)". Log footers count re-runs as "(re-run N)".
- Every URL in the Notes of a story or log must be a clickable hyperlink in both the Word and PDF files.
