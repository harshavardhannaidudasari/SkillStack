# SkillStack

A personal skill and learning tracker — for any programming language,
framework, tool, or soft skill. Add what you're learning, track your
progress, and jot down notes and resources as you go.

## Features

- Add skills with a free-text category, so it covers literally anything —
  programming languages, frameworks, cloud tools, soft skills, whatever
  you're tracking.
- Track status (`Want to Learn` → `Learning` → `Proficient` → `Expert`) and
  a 0–100% progress bar for each skill.
- Notes and resource links per skill.
- Filter by category or status.
- Summary counts at a glance.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then open <http://localhost:5050>.

Data is stored locally in `data/skillstack.db` (SQLite — created
automatically on first run, gitignored).

## Tech

Flask + SQLite, server-rendered templates, no build step and no external
services required.
