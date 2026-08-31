# Job Application Tracker

A Flask-based web application for tracking job applications. Built for CS348 - Database Systems at Purdue University.


## Overview

The Job Application Tracker helps users organize and track their job applications. This is Phase 1 of the project, which focuses on setting up the development environment and creating a Hello World page.


## Tech Stack (Phase 1)

| Component | Technology |
|-----------|------------|
| Backend | Python 3.x / Flask |
| ORM | SQLAlchemy |
| Database | SQLite (development) |
| Frontend | HTML5 / CSS3 |


## Current Features (Phase 1)

- Flask web server configured
- SQLAlchemy ORM integrated
- SQLite database connected
- Hello World landing page
- Development environment ready


## Project Structure

cs348-job-application-db/
├── app.py # Flask application entry point
├── templates/
│ └── index.html # Hello World landing page
├── requirements.txt # Python dependencies
├── venv/ # Virtual environment (ignored)
└── README.md # Project documentation



## Installation

### Prerequisites
- Python 3.9+
- Git
- Virtualenv (recommended)

### Setup Instructions


**2. Create and activate virtual environment**

Windows:

python -m venv venv
venv\Scripts\activate

**3. Install dependencies**

pip install -r requirements.txt


**4. Initialize database**

python app.py

(The database file `job_tracker.db` will be created automatically)

**5. Run the application**

http://localhost:5000



## Screenshots

### Hello World Page
![Hello World Page](screenshots/hello-world.png)


## Phase 1 Deliverables

| Requirement | Status |
|-------------|--------|
| Programming language/framework installed | Complete |
| Hello World page developed | Complete |
| Demo video recorded (1-2 minutes) | Complete |
| Submitted to Brightspace | Complete |


## Demo Video Notes

The Phase 1 demo video demonstrates:

1. Terminal: Shows Python, Flask, and dependencies installed
2. Browser: Shows Hello World page running at localhost:5000
3. Code: Shows app.py and templates/index.html structure
4. Environment: Shows virtual environment activated


## Troubleshooting

**Issue**: 'python' is not recognized
**Solution**: Use `py` instead of `python`, or add Python to your PATH

**Issue**: Port 5000 is already in use
**Solution**: Change the port in `app.py` from 5000 to 5001

**Issue**: ModuleNotFoundError: No module named 'flask'
**Solution**: Activate your virtual environment: `venv\Scripts\activate`

**Issue**: The view function for 'hello' did not return a valid response
**Solution**: Make sure your `hello()` function has `return render_template('index.html')`

**Issue**: (venv) not showing in terminal
**Solution**: Reactivate with `venv\Scripts\activate`


## Author

Your Name
- Purdue University, Computer Science
- CS348 - Database Systems
- Fall 2026


## License

This project is for educational purposes as part of CS348 at Purdue University.


Last Updated: August 30, 2026