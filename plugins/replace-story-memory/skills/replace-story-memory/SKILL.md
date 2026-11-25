---
name: "replace-story-memory"
description: "Replace a story that is already a FamilySearch Memory with its new PDF, keeping the same tags plus anyone new in the People list. Use for \"replace the story\", \"update the story memory\", \"upload the new story\"."
---

# Replace an Ancestor Story Memory on FamilySearch

> **Setup:** `<Researcher Name>` means the `researcher_name` in `genealogy_config.json` in the root of your Genealogy folder. Never tag, name or list that person in stories or People lists.

Use this when a person's story is already a Memory on FamilySearch and the story has since been rebuilt. If the person has no story Memory yet, stop and use the upload-story-memory skill instead.

FamilySearch does not let you swap the file inside an existing Memory. So this skill uploads the new PDF as a new Memory, gives it the same tags as the old one (plus anyone new in the People list), and then removes the old Memory once the user confirms.

The user's request to replace the story is their approval to upload the new Memory and tag it. Deleting the old Memory is permanent, so always ask before deleting it (step 6).

## 1. Find the files

1. Work in the Genealogy folder on the computer this chat is linked to (the `genealogy_root` folder named in `genealogy_config.json`). Ignore "._" files.
2. In <Surname> Family/<Full Name> <PID>/ find:
   - the current story PDF: "Story_<Full Name>, <birth year>–<death year>.pdf" (maiden name with married names in parentheses, e.g. "Story_Mary Ann Smith (Jones), 1859–1925.pdf"). Older stories may still be named "Ancestor_Story_<Full Name> <birth year>.pdf"; use whichever is in the folder (not the Superseded/ copies).
   - People in <Full Name> <birth year> story.xlsx
3. If the story PDF is missing, stop and tell the user. If the PDF is older than the story .docx or the Project's claude/ .md copy, say so and ask before going on.
4. If the story starts with "LIVING – do not upload to Memories", stop. Never upload it.

## 2. Read the People list

1. Stage the .xlsx and read every row: Name, Relationship, PID, FamilySearch URL.
2. Keep the rows with a FamilySearch PID (e.g. ABCD-123). Skip "not in tree" and blank PIDs, but list them in the report.
3. Remove duplicate PIDs. Put the target ancestor first.

## 3. Find the old Memory and record its tags

Use Claude in Chrome (load the chrome-browser skill first). Open a new tab.

1. Open https://www.familysearch.org/tree/person/memories/<target PID>.
2. Find the old story Memory. It is titled "Story_…", "Ancestor_Story_…" or "Life of …" for this person. If there is none, stop and use upload-story-memory. If there is more than one, list them and ask the user which to replace.
3. Open it and note its title, date range, description and its Tagged People (name and PID of each).
4. Build the tag list for the new Memory: every PID tagged on the old Memory, plus every PID from the People list that is not already there. If someone tagged on the old Memory is not in the People list, keep them, and mention them in the report.
5. Check each PID that is new since the old Memory: the person page must open and show a deceased person. Don't tag anyone living, private, merged or not found.

## 4. Upload the new PDF

1. On the target's Memories tab, click Add Memories, then Upload.
2. Try the browser's file upload tool with the PDF. If it can't reach the file (common on some computers), ask the user to drag the PDF into the open FamilySearch upload window, then carry on once it shows as uploaded.
3. Open the new Memory (Info panel, Edit Details):
   - Title: the PDF's file name without .pdf, e.g. "Story_Mary Ann Smith (Jones), 1859–1925". FamilySearch usually fills this from the file name; check it.
   - Date: birth year to death year, as on the old Memory.
   - Description: the story's title line, e.g. "Life of Mary Ann Smith (Jones), 1859–1925".
4. Save. Don't accept new terms or change account settings; if FamilySearch asks, stop and ask the user.

## 5. Tag the new Memory

1. Open the Tagged tab and click Tag People. The person whose Memories tab you uploaded from is usually tagged already.
2. For each PID in the tag list, type the PID in the search box, check that the name and dates match, and click the person.
3. Re-read the Tagged People list and compare it with the tag list. Fix any missing or wrong tag before going on.

## 6. Remove the old Memory (ask first)

1. Only after the new Memory has every tag, ask the user: "The new story Memory is up with all N tags. Delete the old Memory '<old title>' (uploaded <date>)? This can't be undone." Wait for a clear yes.
2. If yes: open the old Memory and delete it (it is your own upload). Confirm it no longer appears on the Memories tab.
3. If no, or no answer: leave the old Memory in place and say so in the report.

## 7. Report

Tell the user briefly:
- the new Memory's title and where to find it (the person's Memories tab URL)
- how many people were tagged, and anyone added since the old Memory
- anyone skipped, and why (not in tree, living, private, merged, not found)
- whether the old Memory was deleted or kept

Don't change the log, the story or the tracker. Close the tabs you opened.

## Rules

- Never edit any person's FamilySearch tree data. This skill only adds the new Memory, tags it, and (with a yes) deletes the old one.
- Never delete the old Memory before the new one is uploaded and fully tagged, and never without the user's yes.
- Never upload a story marked LIVING.
- Never tag <Researcher Name> or any living person.
- If the browser tool fails two or three times on the same step, stop and tell the user what happened.