# SkillStack

A self-guided learning platform covering 12 in-demand skill tracks —
AI/ML, Data Science, Cybersecurity, Cloud & DevOps, Full-Stack Web Dev,
Digital Marketing, UI/UX Design, Business Analytics, Renewable Energy,
Blockchain & FinTech, a multi-language Programming Languages track, and
Software Testing & QA Automation.

Every course is broken into small, focused topics. Each topic pairs a
curated video with a short practice quiz written for that exact topic, so
you watch, then immediately check what stuck — no jumping between tabs.

## Features

- 12 courses, 80+ topics, each with a video + a 2-question practice quiz.
- Progress is tracked per topic and saved locally (`localStorage`), with an
  overall completion ring in the header and a per-course progress bar.
- Animated 3D hero (Three.js) you can drag to spin, and tilting course
  cards.
- Light/dark theme toggle (also respects your OS preference by default).
- Course search/filter on the home screen.
- Hash-based routing (`#/course/<id>/topic/<n>`), so a specific topic is a
  shareable, bookmarkable, back-button-friendly URL.

## Running it

It's a single self-contained HTML file — no build step, no server, no
dependencies to install. Just open `index.html` in a browser, or serve the
folder with any static file server:

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>.

## Tech

Vanilla HTML/CSS/JS (no framework), Three.js loaded from a CDN for the
hero animation, YouTube embeds for video content, `localStorage` for
progress — everything else is inline in `index.html`.
