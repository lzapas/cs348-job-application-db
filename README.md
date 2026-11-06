# Job Application Tracker

A Flask web application for tracking job applications, built for CS348 (Information Systems) at Purdue University, Fall 2026.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3 / Flask |
| Database | SQLite, accessed with Python's built-in `sqlite3` module (plain SQL, no ORM) |
| Frontend | Jinja2 templates, HTML/CSS |

## Project Structure

```
cs348-job-application-db/
├── schema.sql             # Tables, constraints, and sample data
├── init_db.py             # Creates job_tracker.db from schema.sql
├── app.py                 # Routes: add/edit/delete (Req 1) and the report (Req 2)
├── templates/             # HTML pages (Jinja2)
├── static/style.css
├── docs/schema.md         # Database design
└── requirements.txt
```

## Setup

Requires Python 3.9+.

```powershell
git clone https://github.com/lzapas/cs348-job-application-db.git
cd cs348-job-application-db

python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
python init_db.py              # creates job_tracker.db with sample data
```

Rerun `python init_db.py` at any time to reset the database to the sample data.

## Running

```powershell
python app.py
```

Then open http://localhost:5000. Run it from the project folder so it finds `job_tracker.db`.

## Features

- **Applications** (`/applications`): add, edit, and delete applications. The company, status, and job type dropdowns are read from the database.
- **Report** (`/report`): filter by date range, salary range, company, status, and job type. Shows the matching applications plus a count, average/min/max salary, and the share that heard back.
- **SQL injection protection**: every value from the user is passed to `sqlite3` as a parameter (`?` or `:name`), never inserted into the SQL text.

## Project Stages

| Stage | Scope | Status |
|-------|-------|--------|
| 1 | Stack installed, Hello World page, demo video | Complete |
| 2 | Add/edit/delete interface and filtered report | Complete |
| 3 | SQL injection, indexes, transactions, AI usage | Not started |

## Troubleshooting

- **`ModuleNotFoundError: No module named 'flask'`**: activate the virtual environment first (`venv\Scripts\activate`), or run `venv\Scripts\python app.py`.
- **`no such table: applications`**: run `python init_db.py`, and run the app from the project folder.

## Author

Lukas Zapasnikas, Purdue University Computer Science
