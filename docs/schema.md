# Database Design

Relational schema for the Job Application Tracker (SQLite, defined with SQLAlchemy models in `models.py`).

```
companies (id PK, name UNIQUE, industry, location, website)
statuses  (id PK, name UNIQUE, sort_order)
job_types (id PK, name UNIQUE)

applications (id PK, job_title, company_id FK→companies.id, status_id FK→statuses.id,
              job_type_id FK→job_types.id, salary, date_applied, notes, created_at)

interviews (id PK, application_id FK→applications.id ON DELETE CASCADE,
            round_name, scheduled_at, outcome)
```

## Tables

### `applications` (main table)
One row per job application. This is the table the add/edit/delete interface (Requirement 1) operates on.

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
| created_at | DATETIME | NOT NULL | When the row was entered |

### `companies`
One row per employer. Several applications can reference the same company, so company details are stored once instead of being repeated on every application.

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| name | VARCHAR(200) | NOT NULL, UNIQUE |
| industry | VARCHAR(100) | |
| location | VARCHAR(150) | |
| website | VARCHAR(255) | |

### `statuses`
Lookup table of pipeline stages (Applied, Phone Screen, Interview, Offer, Rejected, Withdrawn). `sort_order` keeps them in pipeline order in the UI. Storing statuses as rows instead of free text prevents typos like "Rejectd" and lets the status dropdown and report checkboxes be built from the database.

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| name | VARCHAR(50) | NOT NULL, UNIQUE |
| sort_order | INTEGER | NOT NULL |

### `job_types`
Lookup table (Internship, Full-time, Part-time, Co-op). Populates the job-type dropdowns for the same reasons as `statuses`.

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| name | VARCHAR(50) | NOT NULL, UNIQUE |

### `interviews`
Interview rounds for an application (one application → many interviews). Used by the report to compute interviews per application.

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| application_id | INTEGER | NOT NULL, FK → applications.id ON DELETE CASCADE |
| round_name | VARCHAR(100) | NOT NULL |
| scheduled_at | DATETIME | |
| outcome | VARCHAR(50) | |

## Relationships

| Relationship | Cardinality | On delete |
|---|---|---|
| companies → applications | 1 : many | Restricted (a company with applications can't be deleted) |
| statuses → applications | 1 : many | Restricted |
| job_types → applications | 1 : many | Restricted |
| applications → interviews | 1 : many | CASCADE: deleting an application deletes its interviews |

SQLite only enforces foreign keys when `PRAGMA foreign_keys=ON` is set on each connection. `models.py` sets it with a SQLAlchemy connect event.
