from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


# SQLite ignores foreign keys (including ON DELETE CASCADE) unless enabled per connection
@event.listens_for(Engine, 'connect')
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__.startswith('sqlite3'):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(150))
    website = db.Column(db.String(255))

    applications = db.relationship('Application', back_populates='company')


class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    # Controls display order (Applied -> Offer) instead of alphabetical
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    applications = db.relationship('Application', back_populates='status')


class JobType(db.Model):
    __tablename__ = 'job_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    applications = db.relationship('Application', back_populates='job_type')


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    job_type_id = db.Column(db.Integer, db.ForeignKey('job_types.id'), nullable=False)
    # Annual USD; nullable because many postings don't list pay
    salary = db.Column(db.Integer, db.CheckConstraint('salary >= 0'))
    date_applied = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    company = db.relationship('Company', back_populates='applications')
    status = db.relationship('Status', back_populates='applications')
    job_type = db.relationship('JobType', back_populates='applications')
    # passive_deletes lets the database's ON DELETE CASCADE remove interviews
    interviews = db.relationship('Interview', back_populates='application',
                                 cascade='all, delete-orphan', passive_deletes=True)


class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer,
                               db.ForeignKey('applications.id', ondelete='CASCADE'),
                               nullable=False)
    round_name = db.Column(db.String(100), nullable=False)
    scheduled_at = db.Column(db.DateTime)
    outcome = db.Column(db.String(50))

    application = db.relationship('Application', back_populates='interviews')
