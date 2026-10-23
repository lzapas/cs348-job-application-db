# Job Application Tracker

A Flask web application for tracking job applications, built for CS348 (Information Systems) at Purdue University, Fall 2026.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3 / Flask |
| ORM | Flask-SQLAlchemy (SQLAlchemy 2) |
| Database | SQLite (development) |
| Frontend | Jinja2 templates, HTML/CSS |

## Project Structure

```
cs348-job-application-db/
├── app.py              # Flask app, config, models, and routes
├── templates/
│   └── index.html      # Landing page
├── requirements.txt    # Python dependencies
├── .env.example        # Template for local environment variables
└── README.md
```

`venv/`, `.env`, and `instance/` (where the SQLite file lives) are local-only and ignored by git.

## Setup

Requires Python 3.9+.

```powershell
git clone https://github.com/lzapas/cs348-job-application-db.git
cd cs348-job-application-db

python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env
```

Set `SECRET_KEY` in `.env` to a random value, e.g. the output of `python -c "import secrets; print(secrets.token_hex(32))"`.

## Running

```powershell
python app.py
```

Then open http://localhost:5000. On first run, `db.create_all()` creates `instance/job_tracker.db`.

## Project Stages

| Stage | Scope | Status |
|-------|-------|--------|
| 1 | Stack installed, Hello World page, demo video | Complete |
| 2 | Add/edit/delete interface and filtered report | Not started |
| 3 | TBD | Not started |

## Troubleshooting

- **`python` is not recognized**: use `py` instead, or add Python to your PATH.
- **Port 5000 is in use**: change the port in the `app.run(...)` call in `app.py`.
- **`ModuleNotFoundError: No module named 'flask'`**: activate the virtual environment first (`venv\Scripts\activate`).

## Author

Lukas Zapasnikas, Purdue University Computer Science
