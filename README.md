# fh-research-kit

Family history research skills for Claude. They research one ancestor at a time on FamilySearch and other record sites, then produce:

- a research log (Word and PDF) with cited sources, evidence ratings and suggested FamilySearch tree fixes
- a readable life story of the ancestor, with numbered notes
- a "People in this story" list, used to upload the story to FamilySearch Memories and tag everyone in it

Claude never edits your FamilySearch tree. It only suggests changes, and you make them yourself. The two Memories skills are the exception: they upload a story and tag people, and only when you ask.

## What's in the kit

| Skill | What it does |
|---|---|
| `fh-research-sources` | Checks the FamilySearch relationship, reads attached sources and searches FamilySearch plus the sites you tick, by country. Saves the findings to the person's data file. |
| `fh-build-log` | Builds the research log (.docx, .pdf, .md) and updates the tracker spreadsheet. |
| `fh-write-story` | Writes the ancestor's life story and the People list. |
| `fh-family-evaluation` | Checks a couple and all their children in FamilySearch for wrong children, duplicates, grandchildren listed as children, mixed families and wrong sources, using the attached sources, the census child count and the GRO index. Builds a Family Evaluation (.docx, .pdf, .md). |
| `rerun-ancestor-log` | Re-checks FamilySearch after you've fixed the tree, then updates the log and story. |
| `upload-story-memory` | Uploads a new story PDF to FamilySearch Memories and tags the people in it. |
| `replace-story-memory` | Replaces a story that's already a Memory, keeping its tags. |

`genealogy-starter/` is the folder you copy to start your own Genealogy folder. It holds the scripts, the blank log template, an empty tracker, a starter `CLAUDE.md` with the working rules, and a fictional example data file.

Countries offered in `fh-research-sources`: United States, England and Wales, Scotland, Ireland, France, Denmark and Germany. You pick countries, then either all their sites or individual ones.

## What you need

- The **Claude desktop app**, with **Claude Code** and **Claude in Chrome** connected. The research and Memories skills drive your own Chrome, so you must be signed in to FamilySearch there, and to any paid sites you want searched.
- A free **FamilySearch** account.
- **Python 3** with two packages: `pip3 install python-docx openpyxl`
- **LibreOffice** or **Microsoft Word**, to turn the .docx files into PDFs.

## Getting the kit

The project is public, so you don't need a GitHub account. Choose one of these ways.

**Download a ZIP (easiest)**

1. Go to https://github.com/maxwellar52/fh-research-kit
2. Click the green **Code** button, then **Download ZIP**.
3. Unzip it wherever you like.

This is a snapshot. To get later updates, download the ZIP again.

**Clone with Git (best for updates)**

Git is usually already on a Mac. On Windows, install it from https://git-scm.com. In Terminal (Mac) or Git Bash / PowerShell (Windows):

```
git clone https://github.com/maxwellar52/fh-research-kit.git
```

This creates a `fh-research-kit` folder. To get updates later, run `git pull` inside that folder.

**GitHub Desktop (Git without commands)**

1. Install GitHub Desktop from https://desktop.github.com
2. Choose **File → Clone repository → URL**, paste `https://github.com/maxwellar52/fh-research-kit` and pick a folder.
3. To get updates later, click **Fetch origin**, then **Pull**.

Your copy is your own. You can't change this project directly. To suggest a change, click **Fork** on the GitHub page and send a pull request.

Updates never touch your own `Genealogy` folder, because you copy `genealogy-starter` out of the kit (see Setup). After an update, copy any new scripts from `genealogy-starter/_tools` into your `Genealogy/_tools` yourself.

## Setup

1. Copy the `genealogy-starter` folder to where you keep your research and rename it `Genealogy`.
2. Edit `Genealogy/genealogy_config.json`: put your full name (as FamilySearch knows you) in `researcher_name` and the folder's full path in `genealogy_root`.
3. Add any rules of your own to `Genealogy/CLAUDE.md`.
4. Install the skills in Claude Code:

   ```
   /plugin marketplace add maxwellar52/fh-research-kit
   /plugin install fh-research-sources@fh-research-kit
   /plugin install fh-build-log@fh-research-kit
   /plugin install fh-write-story@fh-research-kit
   /plugin install fh-family-evaluation@fh-research-kit
   /plugin install rerun-ancestor-log@fh-research-kit
   /plugin install upload-story-memory@fh-research-kit
   /plugin install replace-story-memory@fh-research-kit
   ```

   To use the skills on claude.ai instead, zip each `plugins/<name>/skills/<name>` folder and upload it as a skill.
5. Open a Claude Code session in your `Genealogy` folder.

## Using it

1. Copy the person's name and PID from FamilySearch and ask Claude to research them. It runs `fh-research-sources` and asks which countries and sites to search.
2. Say "Build the log". This runs `fh-build-log`.
3. Answer "Yes" when asked about the story. This runs `fh-write-story`.
4. Optional: say "Upload the story" to add it to FamilySearch Memories.
5. After you fix the tree in FamilySearch, say "Fixed, run again". This runs `rerun-ancestor-log`.

## Privacy

Your Genealogy folder holds details of real people, some of them living. Keep it out of this repository and out of any public place. Logs and stories for living people are marked "LIVING – do not upload to Memories", and the upload skills refuse them.

## Licence

See [LICENSE](LICENSE).
