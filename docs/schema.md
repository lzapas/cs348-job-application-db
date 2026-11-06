# Database Design

Relational schema for the Job Application Tracker (SQLite, defined with SQLAlchemy models in `models.py`).

```
companies (id PK, name UNIQUE)
statuses  (id PK, name UNIQUE)
job_types (id PK, name UNIQUE)

applications (id PK, job_title, company_id FK→companies.id, status_id FK→statuses.id,
              job_type_id FK→job_types.id, salary, date_applied, notes)
```

## `applications` (main table)
One row per job application. The add/edit/delete pages (Requirement 1) work on this table, and the report (Requirement 2) filters it.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| id | INTEGER | PK | |
| job_title | VARCHAR(200) | NOT NULL | |
| company_id | INTEGER | NOT NULL, FK → companies.id | |
| status_id | INTEGER | NOT NULL, FK → statuses.id | |
| job_type_id | INTEGER | NOT NULL, FK → job_types.id | |
| salary | INTEGER | CHECK (salary >= 0), nullable | Annual USD; NULL when the posting lists no pay |
| date_applied | DATE | NOT NULL | |
| notes | TEXT | nullable | |

## Lookup tables: `companies`, `statuses`, `job_types`
Each has `id INTEGER PK` and `name VARCHAR NOT NULL UNIQUE`.

- **companies**: one row per employer, so a company's name is stored once instead of being repeated on every application.
- **statuses**: Applied, Phone Screen, Interview, Offer, Rejected, Withdrawn. They're inserted in pipeline order, so ordering by `id` gives pipeline order.
- **job_types**: Internship, Full-time, Part-time, Co-op.

Keeping these values in tables instead of free text prevents typos (e.g. "Rejectd") and lets the form dropdowns and report filters be built from the database.

## Relationships

| Relationship | Cardinality | On delete |
|---|---|---|
| companies → applications | 1 : many | Restricted (a company with applications can't be deleted) |
| statuses → applications | 1 : many | Restricted |
| job_types → applications | 1 : many | Restricted |

SQLite only enforces foreign keys when `PRAGMA foreign_keys=ON` is set on each connection. `models.py` turns it on with a SQLAlchemy connect event.
