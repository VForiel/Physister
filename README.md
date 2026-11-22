# Physister

Started as a repo to explain physics to my little sister 🥰, now it's her whole study companion for
physiotherapy school: every course of the first two years of the UCLouvain bachelor in physiotherapy
(KINE1BA, bloc 1 and 2), in French.

Mostly vibe-coded, copy what you want and credit me if you want, I don't really care ^^

## What's inside

- **32 courses**, one module each in `courses/`, following the official 2026-2027 programme
- explanations split in chapters, with interactive zones (Hodgkin-Huxley simulation, spirometer,
  centre of mass, Ottawa rules, Fagan nomogram, etc.)
- **randomised quizzes** with three levels (easy, medium, hard); numeric questions draw new values each time
- flashcards with "I knew it / review again"
- glossary terms with a tooltip, a page glossary and a Wikipedia link
- progress saved server-side in a JSON file (single user, no account), with a reset per course or global
- the old physics pages are kept in `archive/`

## Run it

```bash
pip install -r requirements.txt
streamlit run Accueil.py
```

Tests (every chapter renders, every question builds, every glossary term exists):

```bash
pip install -r requirements-dev.txt
python -m pytest tests -q
```

## Add or edit a course

A course module defines `COURSE`, `TERMS`, `CHAPTERS` (title + function), `QUESTIONS`, `CARDS`, `VIDEOS`, `LINKS`,
then gets listed in `courses/__init__.py`. In text, `[[key]]` or `[[key|shown text]]` links to a glossary term
(`[[key\|text]]` inside a Markdown table). Question helpers are in `app/quiz.py` (`qcm`, `multi`, `vf`, `num`,
`gen_qcm`, `table_qcm`).

## Hosting

Docker image + systemd socket activation (`deploy/`): the container only starts on the first request and stops
after 10 minutes without connection, so it costs nothing when nobody uses it.
