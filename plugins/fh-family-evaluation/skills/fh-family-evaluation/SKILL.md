---
name: "fh-family-evaluation"
description: "Check a FamilySearch couple and all their children for wrong children, duplicates, grandchildren or mixed families, using sources, census and the GRO index, and build a Family Evaluation. Use for \"evaluate this family\"."
---

# Fh Family Evaluation: check a couple and their children

> **Setup:** `<Researcher Name>` means the `researcher_name` in `genealogy_config.json` in the root of your Genealogy folder. Never tag, name or list that person in stories or People lists.

Use Claude in Chrome for the FamilySearch and GRO work, and Bash for the build. Never edit FamilySearch: suggest changes only, and the user makes them. Rate every conclusion **Proven**, **Probable** or **Possible**. Flag open questions instead of stating them as fact.

## Step 0: check the setup first

1. Claude in Chrome tools (`mcp__claude-in-chrome__*`) are available. Load them in one ToolSearch call, including `javascript_tool`, `get_page_text`, `find`, `form_input` and `browser_batch`.
2. The Genealogy folder is reachable, with `_tools/evaluate.py`, `_tools/base/Ancestor_Research_Log_TEMPLATE.docx` and `_AAResearch_Tracker.xlsx` in its root (the `genealogy_root` folder named in `genealogy_config.json`).

If either is missing, stop and tell the user in two lines what is missing.

## Inputs

- The father's (or mother's) FamilySearch PID. The user may paste a tree link or the person card.
- What the user suspects, if they say (for example "one or two families mixed").

## Steps

### 1. Read the family

Open `https://www.familysearch.org/en/tree/person/details/<PID>` and read it with `get_page_text`. Record:

- the couple: names, PIDs, dates, places and the marriage;
- every child: name, years and PID, in tree order;
- the couple's parents, and any second set of parents shown on a child;
- "Foster", "Guardianship" or "Preferred" labels, which show non-biological links already set.

### 2. Read every attached source

Do this for the father, the mother and **every** child. The source panel's details are not in `<main>`, and calling FamilySearch's API with a session token is blocked. So click each source and read the panel from the page. Once per session, run the whole of `Genealogy/_tools/fs_sources_helper.js` in `javascript_tool` on any familysearch.org page. It saves the helper in the site's localStorage, where it stays across pages.

Then, for each person, run one `browser_batch`:

1. `navigate` to `https://www.familysearch.org/en/tree/person/details/<PID>`;
2. `javascript_tool` with `await (new (Object.getPrototypeOf(async function(){}).constructor)(localStorage.__x))()`;
3. `get_page_text`, which returns the vitals plus one compact line per source.

You can do two or three people per batch. The helper reads the first 22 sources. For a person with more (often the father), run it, then for the rest click the remaining source buttons in a page script that writes into `<main>` the same way. Keep each script under 40 seconds, or it times out. `javascript_tool` output is cut off at about 1,000 characters, so always write long text into `<main>` and read it back with `get_page_text`.

### 3. Test each child

For every child, ask these questions:

- **Census fit.** Is the child in the couple's household, with the right relationship ("son"/"daughter", not "granddaughter", "nephew" or "visitor") and an age that fits? Census indexes put grandchildren and others under "Other People on This Record". Read the relationship.
- **Parents named.** Do baptism, marriage and death records name this father and mother? Remember a late baptism: several older children baptised on one day.
- **Mother's age.** Was the mother between about 15 and 50 at the birth? A child born to a mother of 47 or more, living with an unmarried older daughter, is often a grandchild.
- **Duplicates.** Two children with the same name: is one a duplicate (same baptism, no other records), or a namesake born after an earlier child died (check the burial)?
- **Mixed families.** Does any child have two sets of parents, or sources from another place, another spouse or another family (different birthplaces, different parents' names)? Check the merge history ("Latest Changes") for recent merges.
- **Wrong attachments.** Index lines with a different surname or spouse (for example a marriage index naming another spouse) are often attached by mistake.
- **Places.** Does the birth place match the census birthplace and the GRO district?

Give each child one verdict: **Proven child**, **Probable child**, **Possible child**, **Duplicate of #n**, **Grandchild**, **Belongs to another family**, or **Unsourced**.

### 4. Count the children (very important)

The 1911 census of England and Wales asks a married woman how many children were born alive, how many were still living and how many had died. The index does not show this, so ask the user to read it from the image: "What does the 1911 census say for children born alive, living and died?" Then check the tree against it:

- documented children + unsourced children = **born alive**?
- children with a death before April 1911 = **died**?
- If the tree has more children than the census, the extras are duplicates, grandchildren or another family's children.

For the United States, the 1900 and 1910 censuses ask the same question ("mother of how many children / number living").

### 5. Check the GRO index (England and Wales)

For any child without a birth or death record, search the GRO online index at https://www.gro.gov.uk/gro/content/certificates/indexes_search.asp. The user must already be signed in. Never enter a password.

- Births give the **mother's maiden name**. This proves the mother, and it often shows the real spelling of her surname.
- Deaths give the **age at death**, which links a death to a birth.
- Search surname + forename + sex + year ±1 or ±2, then filter the result rows to the family's district. For deaths, also search the surname alone with the district (no forename) to catch infants listed under another name.
- Form quirks: changing the year, the range or Birth/Death reloads the page and may clear text boxes. Set those dropdowns first, then type the surname and forename, then pick the sex, then click Search. Read the results with `javascript_tool` over `tr` rows: the name row plus the next row (the GRO reference).
- Write each reference as "1872 Dec qtr, Stoke upon Trent 6B/255". GRO entries have no permanent link, so record the search page URL.

### 6. Write the data file

Save `json_data/evaldata_<Father Full Name>.json` in the father's folder: `<Surname> Family/<Full Name> <PID>/`. Create the folder if needed, reusing the surname folder. Use the fields listed at the top of `_tools/evaluate.py`:

- `header_line`: "<Father> <years> (<PID>) and <Mother> <years> (<PID>)   •   m. <date>, <place>   •   evaluated <date>"
- `summary`: what is right, the counts (well supported / duplicate / grandchild / other family / unsourced), and the main problem in one paragraph. End with "No tree changes were made."
- `footer`: "<Father> & <Mother> • <PID> • Family Evaluation <date>" (re-runs: add "(re-run N)")
- `couple`, `children`: the verdict tables (bold with `**…**`)
- `mixed`: one paragraph per mixed-in family or unrelated person, plus how to tell the families apart
- `checks`: the census count, the GRO results (with a table) and what would prove it
- `searches`: every search, including ones that found nothing
- `tree_intro`, `tree_actions`: step-by-step FamilySearch fixes. Give each a reason the user can paste, and cite tree profiles as "FamilySearch Family Tree, Name (PID), URL"
- `unresolved`: the open questions

Every URL must be a full https link; `evaluate.py` makes them clickable.

### 7. Build

1. If an earlier evaluation of this family is in the folder, first move its .docx, .pdf and .md into the folder's `Superseded/` with the date added, for example "Family Evaluation_<Father> and <Mother>, m. <year> (2026-11-26).docx". The build overwrites files of the same name.
2. From the father's folder, run (the command is complete, so don't open the script):

```
python3 ../../_tools/evaluate.py "json_data/evaldata_<Father Full Name>.json" "Family Evaluation_<Father Full Name> and <Mother Full Name>, m. <marriage year>" --pdf
```

This writes the .docx, .md and .pdf. The PDF is made by Microsoft Word on a Mac, otherwise by LibreOffice. If it reports "PDF NOT MADE", run `python3 ../../_tools/topdf.py "<file>.docx"`, and if that fails too, tell the user to open the .docx in Word and save it as PDF.

### 8. Finish

- Send the PDF with SendUserFile.
- In chat, give a short outline: what is right, what is wrong (each problem with its PID), the 1911 count result and the top tree actions.
- Offer research logs (fh-research-sources, then fh-build-log) for any child whose identity is still in doubt.
