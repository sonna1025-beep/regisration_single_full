# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup & Running

```bash
pip install flask pandas openpyxl
python app.py
```

App runs at http://127.0.0.1:5000

## Architecture

Single-file Flask app (`app.py`) with an SQLite database (`register.db`).

- `/` — registration form (Mongolian-language UI)
- `/register` — POST handler: validates email via regex, inserts into DB, flashes success/duplicate error
- `/admin` — lists all registered users in a table (no auth)
- `/export` — exports all users to `Register.xlsx` via pandas

**DB schema** (`users` table): `id`, `ovog` (last name), `ner` (first name), `utas` (phone), `email` (unique).

HTML templates are inline strings (`HTML`, `ADMIN_HTML`) rendered with `render_template_string`. There are no separate template files.

The `/admin` route has no authentication — anyone can access it.
