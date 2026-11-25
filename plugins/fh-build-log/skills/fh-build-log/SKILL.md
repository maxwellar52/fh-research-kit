---
name: "fh-build-log"
description: "Use in Claude Code inside the Genealogy folder to build or rebuild an ancestor's research log, update the research tracker and move older versions to Superseded. Run after the research is saved."
---

# Family history: build the research log

Run this in Claude Code, opened in the Genealogy folder. Use the scripts in _tools. Do not write new scripts. Make minimal changes.

## Before building

1. Confirm the folder has _tools and _AAResearch_Tracker.xlsx in its root. If not, stop and ask the user.
2. Ignore the "._" files macOS leaves behind.
3. Check the copy is current. Compare the date on the header line of json_data/data_<Full Name>.json with the header line of the Project's claude/ .md copy. If the folder copy is older, tell the user and ask before continuing.

## Folder and file names

- Folder: Genealogy/<Surname> Family/<Full Name> <PID>/ (e.g. Genealogy/Smith Family/John Smith ABCD-123/).
- If the relationship check found no relationship, use Genealogy/XXNot in my line/<Full Name> <PID>/ instead.
- Log file: Log_<Full Name>, <birth year>–<death year>. Example: Log_Mary Ann Smith (Jones), 1859–1925.
- Women: maiden name with the married name in parentheses. More than one marriage: married names in order, e.g. (Street, Jones).
- Unknown birth year: "abt 1874". No death year: "–present" for a living person, "–unknown" when unknown, "–abt <year>" when estimated. Never use "?" in a file name.
- Folder and JSON names leave out the married name in parentheses (e.g. Ellen Brown).

## Build

1. Build with _tools/refill.py from _tools/base/Ancestor_Research_Log_TEMPLATE.docx. Keep formatting identical.
2. Produce .docx, .pdf and .md. The .md is a copy for your claude.ai Project, if you use one (otherwise save it in `Claude outputs/`); don't leave it in the person folder.
3. Use portrait layout and these seven sections, in this order: Identification; Vital Events; Spouse(s); Child(ren); Sources; Research Notes; Tree Actions Suggested.
4. Identification: if the person is living, add "LIVING – do not upload to Memories".
5. Sources table: six columns, including "Attached in FS? (Y/N)". Show the full clickable URL for every source, including ones already attached.
6. GRO entries have no permanent link. If FamilySearch already holds the GRO entry, put the GRO reference in the notes of the matching index source and write where it appears, e.g. "Y (also quoted in the Birth reason)". If FamilySearch has no reference, list the GRO search as its own source, mark it "N – search GRO" and add a Tree Action to record it.
7. Research Notes: include a Searches performed block.
8. Tree Actions: give step-by-step FamilySearch fixes. Each URL gets a short citation before it, e.g. "Utah, U.S., Select Marriage Records, 1860-1944, <URL>". Tree profiles: "FamilySearch Family Tree, Name (PID), URL". Find a Grave: "Find a Grave, memorial <no.>, Name, URL".

## Superseded and the tracker

- Before replacing a log, story or People list, move the old .docx, .pdf or .xlsx into the person's folder's Superseded/ subfolder and add the date to its name, e.g. "Log_Ellen Brown (Taylor), 1890–1987 (2026-11-16).docx". Use b, c, d for more versions on the same day.
- Update _AAResearch_Tracker.xlsx for every new or replaced log. There is only one tracker, in the root. If one is found in a subfolder, move it to that folder's Superseded/ and report it.
- Columns: Folder (full path from Genealogy, e.g. Genealogy/Brown Family/Thomas Brown WXYZ-456); In my line? (Direct ancestor / Relative (relationship) / By marriage (relationship) / Not Related / Not checked (reason)); Story (Y/N).

## Older files

- _tools/rename_all.py renames older Ancestor_Research_Log_ and Ancestor_Story_ files to the Log_ and Story_ style. Always run a dry run first, show the result, and run --apply only after the user agrees.

## Finish

Tell the user the log is built and the tracker is updated. Then ask: "Write the Ancestor Story for <Full Name> now? (Yes / No)" and wait for the answer. If the user says no, use the fh-write-story skill's No steps.