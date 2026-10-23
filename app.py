import os
from datetime import date

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from models import Application, Company, JobType, Status, db

load_dotenv()

app = Flask(__name__)

# Secrets come from .env (see .env.example); the fallback is for local dev only
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')
# Relative SQLite paths resolve to the instance/ folder in Flask-SQLAlchemy 3
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# Every POST form must include csrf_token(), so other sites can't submit forms as the user
csrf = CSRFProtect(app)

NEW_COMPANY = 'new'  # value of the "+ Add new company" option in the company dropdown


def lookup_options():
    """Rows that populate the form dropdowns. Queried on every request, never hardcoded."""
    return {
        'companies': Company.query.order_by(Company.name).all(),
        'statuses': Status.query.order_by(Status.sort_order).all(),
        'job_types': JobType.query.order_by(JobType.name).all(),
    }


def parse_application_form(form):
    """Validate the submitted form. Returns (values, errors)."""
    errors = {}
    values = {
        'job_title': form.get('job_title', '').strip(),
        'company_id': form.get('company_id', ''),
        'new_company_name': form.get('new_company_name', '').strip(),
        'status_id': form.get('status_id', ''),
        'job_type_id': form.get('job_type_id', ''),
        'salary': form.get('salary', '').strip(),
        'date_applied': form.get('date_applied', '').strip(),
        'notes': form.get('notes', '').strip(),
    }

    if not values['job_title']:
        errors['job_title'] = 'Job title is required.'
    elif len(values['job_title']) > 200:
        errors['job_title'] = 'Job title must be 200 characters or fewer.'

    if values['company_id'] == NEW_COMPANY:
        if not values['new_company_name']:
            errors['company_id'] = 'Enter a name for the new company.'
    elif not values['company_id'].isdigit() or not db.session.get(Company, int(values['company_id'])):
        errors['company_id'] = 'Choose a company.'

    # The dropdowns only offer valid ids, but the request could be forged, so check the DB
    if not values['status_id'].isdigit() or not db.session.get(Status, int(values['status_id'])):
        errors['status_id'] = 'Choose a status.'
    if not values['job_type_id'].isdigit() or not db.session.get(JobType, int(values['job_type_id'])):
        errors['job_type_id'] = 'Choose a job type.'

    if values['salary'] and (not values['salary'].isdigit() or int(values['salary']) > 10_000_000):
        errors['salary'] = 'Salary must be a whole number between 0 and 10,000,000.'

    try:
        date.fromisoformat(values['date_applied'])
    except ValueError:
        errors['date_applied'] = 'Enter a valid date.'

    return values, errors


def apply_form_to(application, values):
    """Copy validated form values onto an Application (new or existing)."""
    if values['company_id'] == NEW_COMPANY:
        name = values['new_company_name']
        # Reuse an existing company if the name matches, instead of failing on UNIQUE(name)
        company = Company.query.filter(db.func.lower(Company.name) == name.lower()).first()
        if company is None:
            company = Company(name=name)
            db.session.add(company)  # inserted in the same transaction as the application
        application.company = company
    else:
        application.company_id = int(values['company_id'])

    application.job_title = values['job_title']
    application.status_id = int(values['status_id'])
    application.job_type_id = int(values['job_type_id'])
    application.salary = int(values['salary']) if values['salary'] else None
    application.date_applied = date.fromisoformat(values['date_applied'])
    application.notes = values['notes'] or None


def save_application(application, values, success_message):
    """Insert/update in one transaction. Returns True on success."""
    try:
        apply_form_to(application, values)
        db.session.add(application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('Could not save the application: it conflicts with existing data.', 'error')
        return False
    flash(success_message, 'success')
    return True


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/applications')
def list_applications():
    # joinedload fetches company/status/job type in the same query instead of one query per row
    applications = (Application.query
                    .options(joinedload(Application.company),
                             joinedload(Application.status),
                             joinedload(Application.job_type))
                    .order_by(Application.date_applied.desc(), Application.id.desc())
                    .all())
    return render_template('applications.html', applications=applications)


@app.route('/applications/new', methods=['GET', 'POST'])
def new_application():
    if request.method == 'POST':
        values, errors = parse_application_form(request.form)
        if not errors and save_application(Application(), values, 'Application added.'):
            return redirect(url_for('list_applications'))
    else:
        values, errors = {'date_applied': date.today().isoformat()}, {}

    return render_template('application_form.html', mode='new', values=values,
                           errors=errors, **lookup_options())


@app.route('/applications/<int:app_id>/edit', methods=['GET', 'POST'])
def edit_application(app_id):
    application = db.session.get(Application, app_id) or abort(404)

    if request.method == 'POST':
        values, errors = parse_application_form(request.form)
        if not errors and save_application(application, values, 'Application updated.'):
            return redirect(url_for('list_applications'))
    else:
        values = {
            'job_title': application.job_title,
            'company_id': str(application.company_id),
            'status_id': str(application.status_id),
            'job_type_id': str(application.job_type_id),
            'salary': '' if application.salary is None else str(application.salary),
            'date_applied': application.date_applied.isoformat(),
            'notes': application.notes or '',
        }
        errors = {}

    return render_template('application_form.html', mode='edit', application=application,
                           values=values, errors=errors, **lookup_options())


@app.route('/applications/<int:app_id>/delete', methods=['POST'])
def delete_application(app_id):
    application = db.session.get(Application, app_id) or abort(404)
    label = f'{application.job_title} at {application.company.name}'
    db.session.delete(application)  # interviews go too, via ON DELETE CASCADE
    db.session.commit()
    flash(f'Deleted "{label}".', 'success')
    return redirect(url_for('list_applications'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)
