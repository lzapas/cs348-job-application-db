# Job Application Tracker

A Flask web application for tracking job applications, built for CS348 (Information Systems) at Purdue University, Fall 2026.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3 / Flask |
| ORM | Flask-SQLAlchemy (SQLAlchemy 2) |
| Database | SQLite |
| Frontend | Jinja2 templates, HTML/CSS |

## Project Structure

```
cs348-job-application-db/
├── app.py                 # Routes: add/edit/delete (Req 1) and the report (Req 2)
├── models.py              # Database tables
├── seed.py                # Resets the database and loads demo data
├── docs/schema.md         # Database design
├── templates/             # HTML pages (Jinja2)
├── static/style.css
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
python seed.py                 # creates instance/job_tracker.db with demo data
```

## Running

```powershell
python app.py
```

Then open http://localhost:5000.

Optional environment variables: `SECRET_KEY` (signs flash messages) and `DATABASE_URL` (defaults to `sqlite:///job_tracker.db`).

## Features

- **Applications** (`/applications`): add, edit and delete applications. The company, status and job type dropdowns are filled from the database.
- **Report** (`/report`): filter by date range, salary range, company, status and job type. It shows the matching applications plus a count, average/min/max salary, and the share that heard back. The SQL uses bound parameters for every user-supplied value.

## Project Stages

| Stage | Scope | Status |
|-------|-------|--------|
| 1 | Stack installed, Hello World page, demo video | Complete |
| 2 | Add/edit/delete interface and filtered report | Complete |
| 3 | SQL injection, indexes, transactions, AI usage | Not started |

## Author

Lukas Zapasnikas, Purdue University Computer Science
