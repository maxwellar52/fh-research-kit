---
name: "upload-story-memory"
description: "Upload a NEW Ancestor Story PDF to FamilySearch as a Memory and tag everyone with a PID from the matching People in ... story.xlsx list. Use for \"upload the story\", \"add the story to FamilySearch\", \"post the story as a memory\"."
---

# Upload a new Ancestor Story to FamilySearch Memories

> **Setup:** `<Researcher Name>` means the `researcher_name` in `genealogy_config.json` in the root of your Genealogy folder. Never tag, name or list that person in stories or People lists.

Use this when a person's story has never been uploaded to FamilySearch. If the story is already a Memory, stop and use the replace-story-memory skill instead.

The user's request to upload the story is their approval to add this Memory and its tags. Ask again only if something differs from what they asked for (a different file, a person not in the People list, an existing Memory with the same title).

## 1. Find the files

1. Work in the Genealogy folder on the computer this chat is linked to (the `genealogy_root` folder named in `genealogy_config.json`). Ignore "._" files.
2. In <Surname> Family/<Full Name> <PID>/ find:
   - the story PDF: "Story_<Full Name>, <birth year>–<death year>.pdf" (maiden name with married names in parentheses, e.g. "Story_Mary Ann Smith (Jones), 1859–1925.pdf"). Older stories may still be named "Ancestor_Story_<Full Name> <birth year>.pdf"; use whichever is in the folder (not the Superseded/ copies).
   - People in <Full Name> <birth year> story.xlsx
3. If either file is missing, stop and tell the user. If the story PDF is older than the .docx or the Project's claude/ .md copy, say so and ask before uploading.
4. If the story starts with "LIVING – do not upload to Memories", stop. Never upload it.

## 2. Read the People list

1. Stage the .xlsx and read every row: Name, Relationship, PID, FamilySearch URL.
2. Keep the rows whose PID looks like a FamilySearch PID (e.g. ABCD-123). Skip "not in tree" rows and blank PIDs, but list them in the report.
3. Remove duplicate PIDs. Put the target ancestor first.

## 3. Check FamilySearch first

Use Claude in Chrome (load the chrome-browser skill first). Open a new tab.

1. Open https://www.familysearch.org/tree/person/memories/<target PID>.
2. If a Memory with the same title (or another story for this person, titled "Story_…", "Life of …" or "Ancestor_Story_…") is already there, stop and tell the user to use replace-story-memory.
3. For each PID in the list, check that the person page opens and shows a deceased person. FamilySearch only lets you tag deceased people in the shared tree. Note any PID that is living, private, merged or not found, and don't tag it.

## 4. Upload the PDF

1. On the target's Memories tab, click Add Memories and choose to upload a file.
2. Upload the story PDF with the browser's file upload tool. If the tool can't reach the file on this computer, ask the user to drag the PDF into the open FamilySearch upload window, then carry on from step 3 once it appears.
3. Title: the PDF's file name without .pdf, e.g. "Story_Mary Ann Smith (Jones), 1859–1925". FamilySearch usually fills this in from the file name; check it and correct it if needed.
4. Add a date range of the person's birth year to death year (e.g. 1859 to 1925), as the earlier story Memories have.
5. Description (optional): the story's title line, e.g. "Life of Mary Ann Smith (Jones), 1859–1925" (no "The" at the start).
6. Save. Don't accept any new terms or change any account settings. If FamilySearch asks for either, stop and ask the user.

## 5. Tag the people

1. Open the new Memory. Click Tag People (or Tag a Person).
2. For a PDF, FamilySearch may ask for a tag area or ask you to name the person. Use one tag per person and don't draw face areas.
3. For each PID in order, add a tag with the name from the list, then attach it to the person by searching by PID (or pasting the PID) under "Attach to Family Tree". Check that the name and dates shown match the list before confirming.
4. Tag the target ancestor first, then everyone else in list order.
5. If a tag attaches to the wrong person, remove that tag at once and try again with the PID.

## 6. Check and report

1. Re-open the Memory and read its tagged people. Compare them with the PIDs from the list.
2. Open the target's Memories tab and confirm the story is listed.
3. Tell the user, briefly:
   - the Memory title and its URL
   - how many people were tagged, out of how many PIDs in the list
   - anyone skipped, and why (not in tree, living, private, merged, not found, tagging failed)
4. Don't change the log, the story or the tracker. If the user wants the upload recorded, they will ask.
5. Close the tabs you opened.

## Rules

- Never edit any person's FamilySearch tree data. This skill only adds the Memory and its tags.
- Never upload a story marked LIVING.
- Never tag <Researcher Name> or any living person.
- If the browser tool fails two or three times on the same step, stop and tell the user what happened.