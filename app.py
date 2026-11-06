import os
from datetime import date

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from models import Application, Company, JobType, Status, db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')  # needed for flash()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_tracker.db')
db.init_app(app)


def dropdown_options():
    """Rows for the dropdowns, queried from the database on every request (never hardcoded)."""
    return {
        'companies': Company.query.order_by(Company.name).all(),
        'statuses': Status.query.order_by(Status.id).all(),
        'job_types': JobType.query.order_by(JobType.name).all(),
    }


def save_from_form(application):
    """Copy the submitted form onto `application` and commit. Returns True on success."""
    form = request.form
    try:
        application.job_title = form['job_title'].strip()
        application.company_id = int(form['company_id'])
        application.status_id = int(form['status_id'])
        application.job_type_id = int(form['job_type_id'])
        application.salary = int(form['salary']) if form['salary'] else None
        application.date_applied = date.fromisoformat(form['date_applied'])
        application.notes = form['notes'].strip() or None
        if not application.job_title:
            raise ValueError
        db.session.add(application)
        db.session.commit()
        return True
    except (ValueError, IntegrityError):
        # ValueError: a field is missing or malformed.
        # IntegrityError: the database rejected it (bad foreign key, negative salary, ...).
        db.session.rollback()
        flash('Please fill in every required field with a valid value.', 'error')
        return False


@app.route('/')
def index():
    return redirect(url_for('list_applications'))


# ---------- Requirement 1: insert / update / delete applications ----------

@app.route('/applications')
def list_applications():
    applications = Application.query.order_by(Application.date_applied.desc()).all()
    return render_template('applications.html', applications=applications)


@app.route('/applications/new', methods=['GET', 'POST'])
def new_application():
    if request.method == 'POST' and save_from_form(Application()):
        flash('Application added.', 'success')
        return redirect(url_for('list_applications'))
    values = request.form or {'date_applied': date.today().isoformat()}
    return render_template('application_form.html', values=values, **dropdown_options())


@app.route('/applications/<int:app_id>/edit', methods=['GET', 'POST'])
def edit_application(app_id):
    application = db.session.get(Application, app_id) or abort(404)
    if request.method == 'POST' and save_from_form(application):
        flash('Application updated.', 'success')
        return redirect(url_for('list_applications'))
    values = request.form or {
        'job_title': application.job_title,
        'company_id': application.company_id,
        'status_id': application.status_id,
        'job_type_id': application.job_type_id,
        'salary': application.salary or '',
        'date_applied': application.date_applied.isoformat(),
        'notes': application.notes or '',
    }
    return render_template('application_form.html', values=values, application=application,
                           **dropdown_options())


@app.route('/applications/<int:app_id>/delete', methods=['POST'])
def delete_application(app_id):
    application = db.session.get(Application, app_id) or abort(404)
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted.', 'success')
    return redirect(url_for('list_applications'))


# ---------- Requirement 2: filtered report ----------

# Each report filter: query-string name -> SQL condition. The SQL text is fixed here;
# the user's value is only ever sent as a bound parameter (:name), never pasted into the SQL.
REPORT_FILTERS = {
    'date_from':   'a.date_applied >= :date_from',
    'date_to':     'a.date_applied <= :date_to',
    'salary_min':  'a.salary >= :salary_min',
    'salary_max':  'a.salary <= :salary_max',
    'company_id':  'a.company_id = :company_id',
    'status_id':   'a.status_id = :status_id',
    'job_type_id': 'a.job_type_id = :job_type_id',
}


@app.route('/report')
def report():
    conditions, params = [], {}
    for name, condition in REPORT_FILTERS.items():
        value = request.args.get(name, '').strip()
        if value:
            conditions.append(condition)
            params[name] = value
    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    rows = db.session.execute(text(f"""
        SELECT a.date_applied, a.job_title, a.salary,
               c.name AS company, s.name AS status, jt.name AS job_type
        FROM applications a
        JOIN companies c  ON c.id  = a.company_id
        JOIN statuses s   ON s.id  = a.status_id
        JOIN job_types jt ON jt.id = a.job_type_id
        {where}
        ORDER BY a.date_applied DESC
    """), params).mappings().all()

    stats = db.session.execute(text(f"""
        SELECT COUNT(*)      AS total,
               AVG(a.salary) AS avg_salary,
               MIN(a.salary) AS min_salary,
               MAX(a.salary) AS max_salary,
               -- "heard back" = the company moved it past Applied (Withdrawn was my choice)
               SUM(CASE WHEN s.name NOT IN ('Applied', 'Withdrawn') THEN 1 ELSE 0 END) AS heard_back
        FROM applications a
        JOIN statuses s ON s.id = a.status_id
        {where}
    """), params).mappings().one()

    return render_template('report.html', rows=rows, stats=stats, args=request.args,
                           **dropdown_options())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
