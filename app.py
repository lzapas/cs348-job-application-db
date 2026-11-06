import sqlite3
from datetime import date

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = 'job_tracker.db'  # created by init_db.py


def get_db():
    """One database connection per request, reused if a page runs several queries."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row             # lets templates use row['job_title']
        g.db.execute('PRAGMA foreign_keys = ON')   # SQLite needs this on every connection
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Flask calls this at the end of every request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return redirect(url_for('list_applications'))


@app.route('/applications')
def list_applications():
    applications = get_db().execute("""
        SELECT a.id, a.date_applied, a.job_title, a.salary,
               c.name AS company, s.name AS status, jt.name AS job_type
        FROM applications a
        JOIN companies c  ON c.id  = a.company_id
        JOIN statuses s   ON s.id  = a.status_id
        JOIN job_types jt ON jt.id = a.job_type_id
        ORDER BY a.date_applied DESC
    """).fetchall()
    return render_template('applications.html', applications=applications)


def dropdown_options():
    """Options for the form's dropdowns, read from the lookup tables (never hardcoded)."""
    db = get_db()
    return {
        'companies': db.execute('SELECT id, name FROM companies ORDER BY name').fetchall(),
        'statuses':  db.execute('SELECT id, name FROM statuses ORDER BY id').fetchall(),
        'job_types': db.execute('SELECT id, name FROM job_types ORDER BY name').fetchall(),
    }


def read_form(form):
    """Turn the submitted form into column values, in the same order as the SQL below.
    Raises ValueError if a field is missing or invalid."""
    job_title = form['job_title'].strip()
    if not job_title:
        raise ValueError('Job title is required')
    salary = form['salary'].strip()
    return (
        job_title,
        int(form['company_id']),
        int(form['status_id']),
        int(form['job_type_id']),
        int(salary) if salary else None,                         # empty box -> NULL
        date.fromisoformat(form['date_applied']).isoformat(),    # rejects invalid dates
        form['notes'].strip() or None,                           # empty box -> NULL
    )


@app.route('/applications/new', methods=['GET', 'POST'])
def new_application():
    db = get_db()
    error = None
    if request.method == 'POST':
        try:
            # Each ? is filled in by sqlite3 with a value from read_form(), in order.
            # The values never become part of the SQL text (prepared statement).
            db.execute("""
                INSERT INTO applications
                    (job_title, company_id, status_id, job_type_id, salary, date_applied, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, read_form(request.form))
            db.commit()
            return redirect(url_for('list_applications'))
        except (ValueError, sqlite3.IntegrityError):
            # ValueError: bad form input. IntegrityError: the database rejected it
            # (e.g. a company id that doesn't exist, or a negative salary).
            db.rollback()  # undo anything from the failed attempt
            error = 'Please fill in every required field with a valid value.'

    # GET: empty form (date defaults to today). Failed POST: show what the user typed.
    values = request.form if request.method == 'POST' else {'date_applied': date.today().isoformat()}
    return render_template('application_form.html', values=values, error=error,
                           editing=False, **dropdown_options())


@app.route('/applications/<int:app_id>/edit', methods=['GET', 'POST'])
def edit_application(app_id):
    db = get_db()
    application = db.execute('SELECT * FROM applications WHERE id = ?', (app_id,)).fetchone()
    if application is None:
        abort(404)  # no application with that id

    error = None
    if request.method == 'POST':
        try:
            # Same values as the INSERT, plus the id at the end for WHERE id = ?
            db.execute("""
                UPDATE applications
                SET job_title = ?, company_id = ?, status_id = ?, job_type_id = ?,
                    salary = ?, date_applied = ?, notes = ?
                WHERE id = ?
            """, read_form(request.form) + (app_id,))
            db.commit()
            return redirect(url_for('list_applications'))
        except (ValueError, sqlite3.IntegrityError):
            db.rollback()
            error = 'Please fill in every required field with a valid value.'

    if request.method == 'POST':
        values = request.form  # failed save: show what the user typed
    else:
        # Fill the form with the saved row. NULL (None) becomes an empty box.
        values = {key: '' if value is None else value for key, value in dict(application).items()}
    return render_template('application_form.html', values=values, error=error,
                           editing=True, **dropdown_options())


@app.route('/applications/<int:app_id>/delete', methods=['POST'])
def delete_application(app_id):
    db = get_db()
    db.execute('DELETE FROM applications WHERE id = ?', (app_id,))
    db.commit()
    return redirect(url_for('list_applications'))


# Each report filter: form field name -> SQL condition.
# The SQL text is fixed here. The user's value is only ever passed as a parameter (:name),
# never pasted into the SQL string, so it can't change the query (prepared statement).
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
    # Keep only the filters the user filled in
    conditions, params = [], {}
    for name, condition in REPORT_FILTERS.items():
        value = request.args.get(name, '').strip()
        if value:
            conditions.append(condition)
            params[name] = value
    where = 'WHERE ' + ' AND '.join(conditions) if conditions else ''

    db = get_db()
    rows = db.execute(f"""
        SELECT a.date_applied, a.job_title, a.salary,
               c.name AS company, s.name AS status, jt.name AS job_type
        FROM applications a
        JOIN companies c  ON c.id  = a.company_id
        JOIN statuses s   ON s.id  = a.status_id
        JOIN job_types jt ON jt.id = a.job_type_id
        {where}
        ORDER BY a.date_applied DESC
    """, params).fetchall()

    # Statistics over the same filtered rows
    stats = db.execute(f"""
        SELECT COUNT(*)      AS total,
               AVG(a.salary) AS avg_salary,
               MIN(a.salary) AS min_salary,
               MAX(a.salary) AS max_salary,
               -- "heard back" = the company moved it past Applied (Withdrawn was my choice)
               SUM(CASE WHEN s.name NOT IN ('Applied', 'Withdrawn') THEN 1 ELSE 0 END) AS heard_back
        FROM applications a
        JOIN statuses s ON s.id = a.status_id
        {where}
    """, params).fetchone()

    return render_template('report.html', rows=rows, stats=stats, args=request.args,
                           **dropdown_options())


if __name__ == '__main__':
    app.run(debug=True)
