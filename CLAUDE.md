# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a personal Python/web bootcamp practice repository (Korean-language coursework), not a
single application. Work is organized chronologically into day-numbered folders, each containing
a Jupyter notebook plus whatever sample data/scripts that day's exercises needed. There is no
shared build system, package manifest, test suite, or app entrypoint spanning the whole repo —
each folder is largely self-contained.

## Structure and topics per folder

- `1,2day.ipynb`, `3day/3day.ipynb`, `4day/4day.ipynb` — core Python fundamentals (data types,
  functions, file I/O), plus `requests`/`matplotlib` exercises. `3day/` has sample text/CSV/image
  files used by those exercises; `4day/practice/` has a small file-I/O playground.
- `2week_1day/2week_1day.ipynb` — HTTP/`requests` basics; `shop.txt` is sample scraped/text data.
- `2week_2day/2week_2day.ipynb` — HTTP methods, `sqlite3`, `matplotlib`; `calculator.py` is a
  standalone module (`plus`/`minus`/`multiply`/`divide`) imported by the notebook; `geoje.db` is
  a SQLite practice DB; `test.html` is a scratch HTML file.
- `2week_3day/2week_3day.ipynb` — HTML/CSS scraping practice with `requests` + `BeautifulSoup` and
  `pymysql` (remote MySQL). `*.webp` images and `2week_3day.html` are exported/rendered notebook
  output. `css_practice.html` is a standalone CSS-selector practice page (open directly in a
  browser to preview).
- `2week_4day/` — currently empty.
- `2week_5day/2week_5day.ipynb` — intro to Flask backend concepts (routes, request/response);
  conceptually the lead-in to the `dddd/` Flask app.
- `dddd/` — small Flask apps demonstrating routing, JSON responses, dynamic URL params, and MySQL
  access via `pymysql`, run progressively across three files:
  - `app.py` — broadest example set (basic routes, `jsonify`, dynamic segments, MySQL query,
    `render_template`).
  - `app2.py` — trimmed down to just the `/customers` MySQL + template example.
  - `app3.py` — login (`/login`, GET query params) and signup (`/join`, GET renders form / POST
    inserts into MySQL) with `hashlib.sha256` password hashing.
  - `templates/*.html` — Jinja templates rendered by the routes above (`customers.html`,
    `join.html`, `template.html`, `test1.html`).

## Running things

There is no `requirements.txt`/`pyproject.toml`/lockfile in this repo — dependencies (`flask`,
`pymysql`, `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, etc.) are assumed to already be
installed in the active Python environment. Install ad hoc as needed (`pip install <package>`).

- **Notebooks**: open and run cells in Jupyter/VS Code; there is no notebook execution CLI wired
  up in this repo.
- **Flask apps in `dddd/`**: run directly, e.g. `python dddd/app.py`. Each hardcodes
  `app.run(host='0.0.0.0', port=80, debug=True)`, so binding to port 80 may require elevated
  privileges — change the `port=` argument if that fails locally. Only one of `app.py` /
  `app2.py` / `app3.py` should be run at a time (they all define overlapping routes on the same
  port).
- **`calculator.py`**: plain module, import and call its functions directly; no CLI.

## Working in this repo

- Match the existing style: notebooks and scripts use Korean comments/markdown and mixed
  English/Korean identifiers — keep new comments consistent with that rather than switching to
  English-only.
- The `dddd/*.py` files connect to a shared remote MySQL instance
  (`svc.sel3.cloudtype.app:31776`) with credentials hardcoded in the source. Treat these as
  throwaway practice credentials tied to a shared course database, not secrets to protect — but
  also don't assume they're safe to reuse for anything beyond this exercise, and don't add new
  hardcoded credentials elsewhere without calling it out.
- `app3.py`'s signup flow computes a SHA-256 hash but doesn't actually store it (it inserts the
  raw `user_pw` instead) — this is pre-existing exercise code, not something to silently "fix"
  unless asked, since it may be intentional for a later lesson step.
- No tests, linter, or CI are configured. Don't add tooling/config scaffolding unless asked.
