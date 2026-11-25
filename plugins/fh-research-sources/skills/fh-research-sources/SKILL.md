---
name: "fh-research-sources"
description: "Use in the Claude desktop app with Claude in Chrome connected and the Genealogy folder linked. For family history research on one ancestor: the FamilySearch relationship check and gathering sources across sites through Claude in Chrome, saving findings to the person's data JSON file."
---

# Family history research: sources and relationship

> **Setup:** `<Researcher Name>` means the `researcher_name` in `genealogy_config.json` in the root of your Genealogy folder. Never tag, name or list that person in stories or People lists.

Use Claude in Chrome for this step. Do not build logs, stories or tracker entries here. Those belong to the fh-build-log and fh-write-story skills.

## Step 0: check the setup first

Before anything else, confirm all of these:

1. Claude in Chrome tools are available: tools named `mcp__claude-in-chrome__*`, or an `enable__mcp__claude-in-chrome` tool that turns them on. If a different Chrome is connected, switch to it and say so in one line.
2. The Genealogy folder can be reached on the user's computer (the `genealogy_root` folder named in `genealogy_config.json`), with `_tools` and `_AAResearch_Tracker.xlsx` in its root.
3. The person's folder or json_data/ folder can be written to, so the findings can be saved.

If anything is missing, stop before doing any work. Do not run part of the skill, and do not save files anywhere else. Tell the user in two or three lines what is missing and that this skill needs the Claude desktop app with Claude in Chrome connected and the Genealogy folder linked. A cloud session or a claude.ai web chat can't reach the browser or the folder.

## Inputs

- The ancestor's name and FamilySearch PID, plus birth date and place if known.
- **FamilySearch is always searched.** It is the base site for all this work, so it is never offered as a choice. Every run does the relationship check, the attached sources (steps 1 and 2) and the FamilySearch records and tree searches in step 3, whatever else is ticked. Do not ask about it.
- **Other sites to search (tick boxes, by country).** Before any searching, unless the user has already named the sites, ask with the AskUserQuestion tool in two rounds. Before round 1, say in one line that FamilySearch is searched automatically.

  **Site lists by country** (each list is one question; put the site's web address in each option's description):

  | Country question | Sites |
  |---|---|
  | United States: records | Ancestry (ancestry.com), American Ancestors (americanancestors.org), Fold3 (fold3.com, military) |
  | United States: graves and newspapers | Find a Grave (findagrave.com), Newspapers.com (newspapers.com), Newspaper Archive (newspaperarchive.com), Chronicling America (loc.gov, free) |
  | England and Wales | Ancestry (ancestry.com), Findmypast (findmypast.co.uk), GRO (gro.gov.uk, birth and death indexes), Newspapers.com (newspapers.com, UK papers) |
  | Scotland | ScotlandsPeople (scotlandspeople.gov.uk), Findmypast (findmypast.co.uk), Ancestry (ancestry.com) |
  | Ireland | IrishGenealogy.ie (irishgenealogy.ie, civil and church), Census of Ireland 1901/1911 (nationalarchives.ie), Findmypast (findmypast.ie), Ancestry (ancestry.com) |
  | France | Geneanet (geneanet.org), Filae (filae.com) |
  | Denmark | Danish Family Search (danishfamilysearch.com), Arkivalieronline (sa.dk, church books), Geneanet (geneanet.org) |
  | Germany | Archion (archion.de, Protestant church books), Matricula (matricula-online.eu, Catholic church books, free), CompGen (compgen.de, local family books and GEDBAS), Ancestry (ancestry.com, German collections) |

  **Round 1 (one call, three questions):**
  1. "Which countries did <name> live in? (1 of 2)", `multiSelect: true`: United States, England and Wales, Scotland, Ireland.
  2. "Which countries did <name> live in? (2 of 2)", `multiSelect: true`: France, Denmark, Germany.
  3. "Search every site for the ticked countries, or pick them?", single choice: "All sites for these countries" (the same as clicking the country name) or "Let me pick sites".

  Pre-fill nothing, but in the question text name the countries the known places point to (for example "Places found: Staffordshire, Ohio, Pennsylvania").

  **Round 2 (only if "Let me pick sites"):** ask one question per country list above, for the ticked countries only, each with `multiSelect: true`. The United States has two lists. Ask at most four questions per call; if more are needed, make a second call straight after.

  If the user picks "All sites for these countries", search every site on the ticked countries' lists. A site that appears under more than one ticked country (Ancestry, Findmypast, Newspapers.com, Geneanet) is searched once, covering all those countries. The "Other" box on each question lets the user type in a site that isn't listed; search it too, using its own search form. If the AskUserQuestion tool isn't available, show the country lists as one numbered list in chat (countries numbered 1–6, sites as 1.1, 1.2 …) and ask the user to reply with country numbers, site numbers or both. Don't search until the user has chosen.

  Record the choices in the data JSON file as `countries_selected` and `sites_selected` (FamilySearch is not listed, since it is always searched). On a re-run, show the tick boxes again and say which countries and sites were chosen last time. If the user says "same as last time", use the recorded lists.
- **Places.** Note where the person lived across their whole life (county, state or country), including anywhere they moved to. Use these places to narrow searches in step 3.
- Use the spellings given. If the user corrects a name, use the corrected spelling everywhere.

## Steps

1. **Relationship check.** Open the person's FamilySearch page and click View My Relationship. Report the relationship exactly as FamilySearch shows it, for example "3rd great-grandfather" or "husband of 2nd great-aunt", and record it under Identification.
   - If any relationship is shown, never say we are not related. Say "direct ancestor" only when the path runs straight up the line.
   - If no relationship is shown, write "Not Related (FamilySearch, View My Relationship, accessed <date>)".
   - If the view can't be opened, write "Relationship not checked" and give the reason. Never write "Not Related" unless FamilySearch was checked.
   - The result decides the folder, so pass it on to fh-build-log.

2. **Attached sources.** Open the person's Details and Sources tabs. List each attached source. For sources attached with RecordSeek, open each one and read its record URL. Do this on every run and never reuse an earlier check.

3. **Searches.** Search FamilySearch (records and tree) and every site the user ticked, and record each search in the Searches performed list, including searches that found nothing:
   - Search only FamilySearch and the ticked sites. Do not search any other site, and do not list other sites in Searches performed.
   - Search each site once. If the person lived in more than one country, cover every place they lived in that one search session.
   - Narrow every search: exact name (plus known spelling variants), birth year ±5 years, and the county, state or country where the person lived.
   - Report every relevant record, including ones behind paywalls.
   - If a site can't be searched, mark it "not searched" with the reason.
   - One try per blocked site. If a site shows a CAPTCHA, a sign-in page, an error or a blank results page, try once only, mark it "not searched" with the reason, and move on.
   - If a site shows the user is signed out, search it anyway, note "appears signed out", and tell the user at the end.
   - Read search results as text, not screenshots, and read only what is needed: just the result rows (at most the first 20), not the whole page. Take a small screenshot only when the text can't be read another way.

   **Search links.** Open these links directly instead of filling in search forms.
   Replace {first}, {last}, {birth}, {death} with the person's details (spaces as +).
   If a link doesn't give results, use the site's form once and tell the user the link needs fixing.

   | Site | Link |
   |---|---|
   | FamilySearch records | https://www.familysearch.org/search/record/results?q.givenName={first}&q.surname={last}&q.birthLikeDate.from={birth-1}&q.birthLikeDate.to={birth+1}&q.deathLikeDate.from={death}&q.deathLikeDate.to={death} |
   | FamilySearch tree | https://www.familysearch.org/search/tree/results?q.givenName={first}&q.surname={last}&q.birthLikeDate.from={birth-1}&q.birthLikeDate.to={birth+1} |
   | Ancestry | https://www.ancestry.com/search/?name={first}_{last}&birth={birth}&death={death} |
   | Find a Grave | https://www.findagrave.com/memorial/search?firstname={first}&lastname={last}&birthyear={birth}&birthyearfilter=1&deathyear={death}&deathyearfilter=exact |
   | Findmypast | https://www.findmypast.co.uk/search/results?firstname={first}&lastname={last}&yearofbirth={birth}&yearofbirth_offset=1 |
   | Geneanet | https://en.geneanet.org/fonds/individus/?nom={last}&prenom={first} |
   | Newspapers.com | https://www.newspapers.com/search/?query=%22{first}%20{last}%22&dr_year={death-1}-{death+1} |
   | Fold3 | https://www.fold3.com/search?keywords={first}+{last} |
   | American Ancestors | https://www.americanancestors.org/search/database-search?firstname={first}&lastname={last}&fromyear={birth-5}&toyear={death}&location={state or country} |
   | Chronicling America | https://www.loc.gov/collections/chronicling-america/?q={first}+{last}&fa=location_state:{state, lower case} (searches can time out; one try) |
   | Newspaper Archive, Filae, ScotlandsPeople, IrishGenealogy.ie, Census of Ireland, Danish Family Search, Arkivalieronline, Archion, CompGen | use the form (no tested link yet) |
   | Matricula | no name index: browse the parish's church books once the parish is known; otherwise mark "not searched – parish unknown" |
   | Archion | paid pass needed to view images; if blocked, note "appears signed out" |
   | GRO | use the form (sign-in needed; no search links) |

   **Re-runs.** If json_data/data_<Full Name>.json already exists, this is a re-run. Still do steps 1 and 2 in full. For step 3, search any newly ticked sites, any site (FamilySearch included) that was "not searched" or failed last time, and any search a new fact calls for (a new name, date or place). Carry the other earlier searches forward unchanged, with their original access dates, and say in the Searches performed list that they were carried forward from the earlier run.

4. **Confidence and conflicts.** Give each fact one of three ratings: Proven, Probable or Possible. Note any conflicting evidence.

5. **Citations.** Use FamilySearch-style citations with the access date, for example: "Ohio, County Births, 1841-2003," database, FamilySearch (URL : accessed 1 Nov 2026).

6. **Scope.** Research the target ancestor only. Offer to create logs for spouses or children found along the way. Never edit FamilySearch. Suggest changes only; the user makes them.

7. **Save.** Write the findings to json_data/data_<Full Name>.json in the person's folder, with the date on the header line.

When finished, tell the user the research is saved and that the next step is the fh-build-log skill in Claude Code.
