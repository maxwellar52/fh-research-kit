---
name: "rerun-ancestor-log"
description: "Re-check one ancestor's FamilySearch record after the user fixes the tree, then update their log, story, People list and tracker. Use for \"fixed, run again\", \"rerun\", \"check and update\"."
---

# Re-run an ancestor log after FamilySearch corrections

> **Setup:** `<Researcher Name>` means the `researcher_name` in `genealogy_config.json` in the root of your Genealogy folder. Never tag, name or list that person in stories or People lists.

Use when the user has made changes in FamilySearch for an ancestor who already has a log and says something like "fixed", "run again", "rerun", "check and update". The target is the ancestor of the current conversation unless the user names another (name + PID).

No new genealogical research unless the user asks. This is a compare-and-update pass. Claude never edits FamilySearch.

## 1. Read the current tree (Claude in Chrome)

Read the page, not FamilySearch's API: API calls with the session token are blocked. Never read the session cookie. Load the Chrome tools you need in one ToolSearch call (`navigate`, `javascript_tool`, `get_page_text`, `browser_batch`, `find`).

1. If `localStorage.__x` isn't set yet this session, run the whole of `Genealogy/_tools/fs_sources_helper.js` once in `javascript_tool` on any familysearch.org page.
2. In one `browser_batch`: `navigate` to `https://www.familysearch.org/en/tree/person/details/<PID>`; `javascript_tool` with `await (new (Object.getPrototypeOf(async function(){}).constructor)(localStorage.__x))()`; `get_page_text`. This returns the vitals plus one compact line per attached source (the first 22), with the source count. For more than 22 sources, click the rest in a page script that writes into `<main>` the same way, and read it back with `get_page_text` (`javascript_tool` output is cut off at about 1,000 characters).
3. Match each source to the log by title, date and place. The helper leaves out URLs, so open a source to read its record ID only when the match is unclear or the source is new. Note any source still marked "Unfinished Attachments".
4. If the Memories count changed, open the Memories tab and read any new memory, since it may hold new evidence.
5. For any source that is new, or that reappeared after being detached, check when it was attached (shown in the source panel) and its tags. Flag an accidental re-attachment of a known-wrong source.
6. Re-check View My Relationship only if the parents or spouse changed; otherwise reuse the relationship already in the log.
7. Close the tab when done.

## 2. Compare with the log

Load `<person folder>/json_data/data_<Full Name>.json` directly from the Genealogy folder (the `genealogy_root` folder named in `genealogy_config.json`). Ignore "._" files. For each item, decide: done, still open, or newly wrong.
- Each tree action in `tree_actions`: done → remove it; partly done → reword it; still open → keep it.
- `sources`: update the Attached in FS? column (Y/N) and the notes ("Attached/Detached by you <date>"). Add new evidence as new numbered sources with full citations.
- `vital_events`, `spouses`, `children`, `notes`: say what the tree now shows. Move resolved conflicts to "(resolved)".
- Add a "Changes since the first log" note (or extend it) listing what the user changed in this pass.
- Add a row at the top of `searches`: "FamilySearch — Target Details and Sources (Nth re-run)" with the source count and findings.
- Update `summary`, `header_line` and the log `footer`, and the Research Date in `identification`. Log footers count re-runs as "(re-run N)", e.g. "Research Log 18 Nov 2026 (re-run 2)"; story footers use "(rev. N)" (see Story below).
- If no actions remain, set `tree_actions` to one entry, "No tree actions outstanding", which links the person's profile and names the records that would advance the research.
- `tracker_entry`: update Status and Superseded copy; keep Story (Y/N).
- People list: if a story exists, update `People in <Full Name> <birth year> story.xlsx` whenever the tree now has a PID for someone listed as "not in tree" (or a PID changed): fill in the PID and the clickable FamilySearch link, and supersede the old file. Check this even when the story text itself doesn't change.
- Story: change only what the new evidence changes (keep the facts and the citation markers as fh-write-story describes). New context lookups must be cited as `C<n>` context sources. Update `written`, `header_line` and `footer` ("rev. N", e.g. "18 Nov 2026 (rev. 8)"; never "revised N times") and the open questions.

## 3. Supersede, rebuild, save

1. List `<person folder>/Superseded/` and pick the next free suffix for today: `(YYYY-MM-DD)`, then `b`, `c`… Never overwrite.
2. Move the current log and story .docx/.pdf (and the People list .xlsx, if it changes) into `<person folder>/Superseded/` with the suffixed names. Work on the files in place in the Genealogy folder; do not copy them anywhere else first.
3. Save the updated JSON to `<person folder>/json_data/data_<Full Name>.json`.
4. Rebuild with the project scripts, run from `Genealogy/_tools` (`<person folder>` here is `../<Surname> Family/<Full Name> <PID>`; these commands are complete, so don't open the scripts):
   - `python3 refill.py base/Ancestor_Research_Log_TEMPLATE.docx "<json>" "<person folder>/<log>.docx"`
   - `python3 makemd.py "<json>" "../Claude outputs/<log>.md"`
   - `python3 story.py "<person folder>/<log>.docx" "<json>" "<person folder>/<story>"` (only if a story exists)
   - `python3 topdf.py "<person folder>/<log>.docx" "<person folder>/<story>.docx"` (leave out the story if there is none)
   - `python3 tracker.py ../_AAResearch_Tracker.xlsx "<json>"`
5. The .md copies go only to the Project's claude/ folder (story.py writes `<story>.md` next to the story .docx; move it, don't leave it in the person folder). If a Project tool is available, write them there (they were just generated, so no need to re-read them first). Otherwise keep them in `Genealogy/Claude outputs/` and tell the user to add them to the Project.
6. Send the log PDF (and the story PDF, if it changed) with SendUserFile.

## 4. Report (short)

- What the user fixed (one line per item).
- Anything new or newly wrong, such as a re-attached wrong source or new evidence in a Memory. Give its ID and when it was attached.
- What's still outstanding (it's in the log's Tree Actions), or "no tree actions outstanding" plus the records that would advance the research.
- Whether the story's content changed or only its date line, and whether the People list was updated with new PIDs.
- The Superseded suffix used.