-- Job Application Tracker: tables and sample data.
-- Run with: python init_db.py   (WARNING: deletes all existing data)

PRAGMA foreign_keys = ON;

-- Drop the table that references the others first
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS job_types;

-- Lookup tables: they fill the dropdowns in the form and the report
CREATE TABLE companies (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE statuses (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE job_types (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Main table: the add/edit/delete pages and the report work on this one
CREATE TABLE applications (
    id           INTEGER PRIMARY KEY,
    job_title    TEXT    NOT NULL,
    company_id   INTEGER NOT NULL REFERENCES companies(id),
    status_id    INTEGER NOT NULL REFERENCES statuses(id),
    job_type_id  INTEGER NOT NULL REFERENCES job_types(id),
    salary       INTEGER CHECK (salary >= 0),   -- NULL when the posting lists no pay
    date_applied TEXT    NOT NULL,              -- 'YYYY-MM-DD'
    notes        TEXT
);

-- Sample data. Lookup rows go first, because applications reference them.
-- Statuses are inserted in pipeline order, so ORDER BY id gives that order.
INSERT INTO statuses (name) VALUES
    ('Applied'), ('Phone Screen'), ('Interview'), ('Offer'), ('Rejected'), ('Withdrawn');

INSERT INTO job_types (name) VALUES
    ('Internship'), ('Full-time'), ('Part-time'), ('Co-op');

INSERT INTO companies (name) VALUES
    ('Google'), ('Microsoft'), ('Eli Lilly'), ('Salesforce'), ('Epic Systems'), ('Cummins');

INSERT INTO applications (job_title, company_id, status_id, job_type_id, salary, date_applied, notes) VALUES
    ('Software Engineering Intern', 1, 2, 1,  95000, '2026-08-20', 'Referral from a friend'),
    ('Software Engineer I',         2, 1, 2, 150000, '2026-09-03', NULL),
    ('Data Science Intern',         3, 3, 1,  72000, '2026-08-28', NULL),
    ('Backend Developer',           4, 5, 2, 130000, '2026-09-10', 'Rejected after the technical round'),
    ('Software Co-op',              6, 1, 4,  55000, '2026-09-15', NULL),
    ('Associate Developer',         5, 4, 2, 110000, '2026-08-12', 'Offer deadline Nov 20'),
    ('Student Web Developer',       3, 1, 3,   NULL, '2026-10-01', 'Pay not listed'),
    ('Software Engineer',           1, 6, 2,   NULL, '2026-10-05', NULL);
