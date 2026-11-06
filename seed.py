"""Reset the database and fill it with demo data.

Usage: python seed.py   (WARNING: deletes all existing data)
"""
import random
from datetime import date, timedelta

from app import app
from models import Application, Company, JobType, Status, db

STATUSES = ['Applied', 'Phone Screen', 'Interview', 'Offer', 'Rejected', 'Withdrawn']  # pipeline order
JOB_TYPES = ['Internship', 'Full-time', 'Part-time', 'Co-op']
COMPANIES = ['Google', 'Microsoft', 'Amazon', 'Eli Lilly', 'Salesforce',
             'Capital One', 'Epic Systems', 'Cummins', 'Stripe', 'Rivian']
TITLES = ['Software Engineer', 'Data Engineer', 'Backend Developer', 'Data Science Intern', 'QA Tester']


def seed(count=25):
    rng = random.Random(348)  # fixed seed: same demo data every run
    db.drop_all()
    db.create_all()

    statuses = [Status(name=n) for n in STATUSES]
    job_types = [JobType(name=n) for n in JOB_TYPES]
    companies = [Company(name=n) for n in COMPANIES]
    db.session.add_all(statuses + job_types + companies)

    for _ in range(count):
        db.session.add(Application(
            job_title=rng.choice(TITLES),
            company=rng.choice(companies),
            status=rng.choice(statuses),
            job_type=rng.choice(job_types),
            salary=None if rng.random() < 0.2 else rng.randrange(40_000, 180_000, 1000),
            date_applied=date(2026, 8, 1) + timedelta(days=rng.randint(0, 80)),
        ))

    db.session.commit()
    print(f'Seeded {count} applications.')


if __name__ == '__main__':
    with app.app_context():
        seed()
