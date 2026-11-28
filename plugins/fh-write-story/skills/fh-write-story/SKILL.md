---
name: "fh-write-story"
description: "Write an ancestor's life story from their data JSON, build it with story.py and make the People in this story list. Use only after the user says yes to the story."
---

# Family history: write the Ancestor Story

> **Setup:** `<Researcher Name>` means the `researcher_name` in `genealogy_config.json` in the root of your Genealogy folder. Never tag, name or list that person in stories or People lists.

Run this only after the research log is built and the user has answered the Yes/No question. Work from the data JSON file. Do not do new genealogical research.

## If the user says no

- Set "Story (Y/N)" to N in _AAResearch_Tracker.xlsx.
- Add "Story declined <date>" to the `notes` in the data JSON, then rebuild the log with refill.py and topdf.py (commands in fh-build-log) so the note shows. A log built minutes ago in this session needs no Superseded copy.
- If no answer is given (for example in an unattended run), enter "N – awaiting answer" in the tracker, do not add the declined note, and say it is waiting.

## If the user says yes

1. Write the story from json_data/data_<Full Name>.json. Add a "story" section to the JSON. Brief web searches are allowed only for general historical context, such as what an occupation involved. Each one must be cited in a footnote.
2. Use chronological order: origins and parents; birth and childhood; marriage(s); children; occupations and residences; migrations; military service; later life; death and burial.
3. Write like a skilled biographer: a warm, readable life story for relatives, not a report. Never invent dialogue, feelings or motives.
4. Style:
   - Short, clear sentences. Split any sentence that carries more than one main idea.
   - Vary transitions. Don't start sentences with "And" repeatedly. Use link words such as "by then", "that year", "meanwhile", "later".
   - Don't end a sentence with a preposition or with a vague word such as "it" or "that". Name the thing instead.
   - Vary sentence openings so paragraphs don't all start with "He".
   - Section headings in title case. Leave short words (a, an, the, and, of, in, at, to, for) lower case unless they come first.
5. The first time any job title appears (the ancestor's, a spouse's, a parent's or a sibling's), explain what the work involved in that place and period, with a cited historical source: tasks, skills, hours, conditions or pay. Later mentions need no repeat.
6. Occupations: describe every occupation the sources record for the ancestor and each spouse, with the year and place. Show how the work changed. Name the employer when a source gives it. If a wife has no recorded occupation, mention any work the sources hint at. Otherwise say plainly that none is recorded.
7. Cite with numbered footnotes using the short collection title. Full citations stay in the log.
8. Top of the story, in order: title "Life of <Full Name>, <birth year>–<death year>" (no "Ancestor Story" heading); a bold line with name, dates, PID and date written; then the relationship line exactly as FamilySearch shows it, with <Researcher Name> in place of "you". Example: "Mary Smith is <Researcher Name>'s 1st cousin 2x removed (FamilySearch, View My Relationship, accessed 13 Nov 2026)." If no relationship: "<Name> is Not Related to <Researcher Name> (FamilySearch, View My Relationship, accessed <date>)." If the view wasn't opened: "Relationship to <Researcher Name> not checked" with the reason. Do not describe the family path.
9. If the person is living, put "LIVING – do not upload to Memories" at the top.
10. End with a short "Open questions" paragraph covering what is still unknown.
11. Dates: use the same forms as the log file name (see fh-build-log): "<birth year>–present" for a living person, "<birth year>–unknown" when the death year is unknown, "<birth year>–abt <year>" when estimated, "abt <year>" for an unknown birth year. Never use "?".
12. Re-read once for the style points above and fix any that slip through.

## Build and save

- The `story` section of the data JSON holds: `file` ("Story_<Full Name>, <years>"), `title_line`, `header_line`, `relationship`, `living` (true/false), `written` (date), `footer` ("… (rev. N)" after the first version), `sections` [[heading, [paragraph, …]], …], `open_questions` [text, …], `context_sources` {"C1": [short title, URL, note], …} and, for sources from another person's log, `related_sources` {"KEY": [short title, URL, note]}.
- Cite inside the text with markers: `{S12}` is source 12 in this person's log, `{C1}` a context source, `{KEY}` a related source. story.py numbers the notes in order of first use and reuses a number when a source is cited again.
- Build from Genealogy/_tools (don't open the scripts to learn their options; these commands are complete):
  - `python3 story.py "../<person folder>/<log>.docx" "<json>" "../<person folder>/<story>"` (no extension on the last name: it writes the .docx and the .md)
  - `python3 topdf.py "../<person folder>/<story>.docx"`
- File name: Story_<Full Name>, <birth year>–<death year>. The .docx and .pdf stay in the person folder. Move the .md to the Project's claude/ folder if a Project tool is available, otherwise to Claude outputs/ (tell the user to add it to the Project). Never leave it in the person folder.
- Move any replaced story into Superseded/ with the date in its name, as the fh-build-log skill describes.
- Set "Story (Y/N)" to Y in the tracker.
- Also save "People in <Full Name> <birth year> story.xlsx" in the same folder, e.g. "People in Mary Ann Smith (Jones) 1859 story.xlsx". Make it with openpyxl: one sheet, header row "Name", "Relationship to <Full Name>", "PID", "FamilySearch URL", then one row per person named in the story, the ancestor first. PID is "not in tree" when there is none. Make each URL (https://www.familysearch.org/tree/person/details/<PID>) a clickable hyperlink. Leave out <Researcher Name>.