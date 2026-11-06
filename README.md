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

## Database Design

The tables are created by [`schema.sql`](schema.sql), which `init_db.py` runs.

```
companies (id PK, name UNIQUE)
statuses  (id PK, name UNIQUE)
job_types (id PK, name UNIQUE)

applications (id PK, job_title, company_id FK→companies.id, status_id FK→statuses.id,
              job_type_id FK→job_types.id, salary, date_applied, notes)
```

### `applications` (main table)
One row per job application. The add/edit/delete pages (Requirement 1) work on this table, and the report (Requirement 2) filters it.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Assigned automatically |
| job_title | TEXT | NOT NULL | |
| company_id | INTEGER | NOT NULL, FK → companies.id | |
| status_id | INTEGER | NOT NULL, FK → statuses.id | |
| job_type_id | INTEGER | NOT NULL, FK → job_types.id | |
| salary | INTEGER | CHECK (salary >= 0), nullable | Annual USD; NULL when the posting lists no pay |
| date_applied | TEXT | NOT NULL | `YYYY-MM-DD`, which sorts and compares correctly as text |
| notes | TEXT | nullable | |

### Lookup tables: `companies`, `statuses`, `job_types`
Each has `id INTEGER PRIMARY KEY` and `name TEXT NOT NULL UNIQUE`.

- **companies**: one row per employer, so a company's name is stored once instead of being repeated on every application.
- **statuses**: Applied, Phone Screen, Interview, Offer, Rejected, Withdrawn. They're inserted in pipeline order, so `ORDER BY id` gives pipeline order.
- **job_types**: Internship, Full-time, Part-time, Co-op.

Why separate tables instead of a text column on `applications`:
- No typos or inconsistent values (e.g. "Rejected" vs "Rejectd").
- A name is changed in one row, not on every application.
- The form dropdowns and report filters are built from these tables.

### Relationships

| Relationship | Cardinality | On delete |
|---|---|---|
| companies → applications | 1 : many | Restricted (a company with applications can't be deleted) |
| statuses → applications | 1 : many | Restricted |
| job_types → applications | 1 : many | Restricted |

SQLite only enforces foreign keys when `PRAGMA foreign_keys = ON` is run on each connection. `schema.sql` runs it for the setup script, and `get_db()` in `app.py` runs it for every web request.

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
