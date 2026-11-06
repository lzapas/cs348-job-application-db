from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


# SQLite ignores foreign keys unless this is turned on for each connection
@event.listens_for(Engine, 'connect')
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)


class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class JobType(db.Model):
    __tablename__ = 'job_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Application(db.Model):
    """Main table: the add/edit/delete pages (Requirement 1) work on this table."""
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    job_type_id = db.Column(db.Integer, db.ForeignKey('job_types.id'), nullable=False)
    salary = db.Column(db.Integer, db.CheckConstraint('salary >= 0'))  # NULL if not listed
    date_applied = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text)

    company = db.relationship('Company')
    status = db.relationship('Status')
    job_type = db.relationship('JobType')
