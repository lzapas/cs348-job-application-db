"""Reset the database and fill it with demo data.

Usage: python seed.py   (WARNING: drops all existing tables)
"""
import random
from datetime import date, datetime, time, timedelta

from app import app
from models import Application, Company, Interview, JobType, Status, db

STATUSES = ['Applied', 'Phone Screen', 'Interview', 'Offer', 'Rejected', 'Withdrawn']
JOB_TYPES = ['Internship', 'Full-time', 'Part-time', 'Co-op']

COMPANIES = [
    ('Google', 'Technology', 'Mountain View, CA', 'https://careers.google.com'),
    ('Microsoft', 'Technology', 'Redmond, WA', 'https://careers.microsoft.com'),
    ('Amazon', 'E-commerce', 'Seattle, WA', 'https://amazon.jobs'),
    ('Eli Lilly', 'Pharmaceuticals', 'Indianapolis, IN', 'https://careers.lilly.com'),
    ('Salesforce', 'Software', 'Indianapolis, IN', 'https://careers.salesforce.com'),
    ('Capital One', 'Finance', 'McLean, VA', 'https://capitalonecareers.com'),
    ('Epic Systems', 'Healthcare IT', 'Verona, WI', 'https://careers.epic.com'),
    ('Cummins', 'Manufacturing', 'Columbus, IN', 'https://cummins.jobs'),
    ('Stripe', 'Fintech', 'San Francisco, CA', 'https://stripe.com/jobs'),
    ('Rivian', 'Automotive', 'Irvine, CA', 'https://rivian.com/careers'),
]

TITLES = {
    'Internship': ['Software Engineering Intern', 'Data Science Intern', 'Backend Intern'],
    'Co-op': ['Software Co-op', 'IT Co-op'],
    'Full-time': ['Software Engineer I', 'Data Engineer', 'Backend Engineer', 'Associate Developer'],
    'Part-time': ['Student Web Developer', 'Part-time QA Tester'],
}

# Rough annual-equivalent pay ranges per job type
SALARY_RANGES = {
    'Internship': (40_000, 95_000),
    'Co-op': (35_000, 70_000),
    'Full-time': (85_000, 185_000),
    'Part-time': (15_000, 35_000),
}

# How many interview rounds an application at each status has had
ROUNDS_BY_STATUS = {
    'Applied': 0, 'Phone Screen': 1, 'Interview': 2, 'Offer': 3, 'Rejected': 1, 'Withdrawn': 1,
}


def seed(num_applications=25):
    rng = random.Random(348)  # fixed seed so the demo data is the same every run

    db.drop_all()
    db.create_all()

    statuses = {name: Status(name=name, sort_order=i) for i, name in enumerate(STATUSES)}
    job_types = {name: JobType(name=name) for name in JOB_TYPES}
    companies = [Company(name=n, industry=i, location=l, website=w) for n, i, l, w in COMPANIES]
    db.session.add_all([*statuses.values(), *job_types.values(), *companies])

    start = date(2026, 8, 1)
    for _ in range(num_applications):
        jt = rng.choices(JOB_TYPES, weights=[5, 4, 1, 2])[0]
        st = rng.choices(STATUSES, weights=[6, 3, 3, 1, 5, 1])[0]
        low, high = SALARY_RANGES[jt]
        applied = start + timedelta(days=rng.randint(0, 80))

        application = Application(
            job_title=rng.choice(TITLES[jt]),
            company=rng.choice(companies),
            status=statuses[st],
            job_type=job_types[jt],
            # ~20% of postings don't list pay
            salary=None if rng.random() < 0.2 else rng.randrange(low, high, 1000),
            date_applied=applied,
        )
        for r in range(ROUNDS_BY_STATUS[st]):
            application.interviews.append(Interview(
                round_name=['Phone Screen', 'Technical', 'Final Round'][r],
                scheduled_at=datetime.combine(applied + timedelta(days=7 * (r + 1)), time(14, 0)),
                outcome='Passed' if r < ROUNDS_BY_STATUS[st] - 1 or st == 'Offer' else
                        ('Failed' if st == 'Rejected' else 'Pending'),
            ))
        db.session.add(application)

    db.session.commit()
    print(f'Seeded {len(companies)} companies, {num_applications} applications, '
          f'{Interview.query.count()} interviews.')


if __name__ == '__main__':
    with app.app_context():
        seed()
