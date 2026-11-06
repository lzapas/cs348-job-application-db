# Database Design

SQLite database for the Job Application Tracker. The tables are created by [`schema.sql`](../schema.sql), which `init_db.py` runs.

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
| id | INTEGER | PRIMARY KEY | Assigned automatically |
| job_title | TEXT | NOT NULL | |
| company_id | INTEGER | NOT NULL, FK → companies.id | |
| status_id | INTEGER | NOT NULL, FK → statuses.id | |
| job_type_id | INTEGER | NOT NULL, FK → job_types.id | |
| salary | INTEGER | CHECK (salary >= 0), nullable | Annual USD; NULL when the posting lists no pay |
| date_applied | TEXT | NOT NULL | `YYYY-MM-DD`, which sorts and compares correctly as text |
| notes | TEXT | nullable | |

## Lookup tables: `companies`, `statuses`, `job_types`
Each has `id INTEGER PRIMARY KEY` and `name TEXT NOT NULL UNIQUE`.

- **companies**: one row per employer, so a company's name is stored once instead of being repeated on every application.
- **statuses**: Applied, Phone Screen, Interview, Offer, Rejected, Withdrawn. They're inserted in pipeline order, so `ORDER BY id` gives pipeline order.
- **job_types**: Internship, Full-time, Part-time, Co-op.

Why separate tables instead of a text column on `applications`:
- No typos or inconsistent values (e.g. "Rejected" vs "Rejectd").
- A name is changed in one row, not on every application.
- The form dropdowns and report filters are built from these tables.

## Relationships

| Relationship | Cardinality | On delete |
|---|---|---|
| companies → applications | 1 : many | Restricted (a company with applications can't be deleted) |
| statuses → applications | 1 : many | Restricted |
| job_types → applications | 1 : many | Restricted |

SQLite only enforces foreign keys when `PRAGMA foreign_keys = ON` is run on each connection. `schema.sql` runs it for the setup script, and `get_db()` in `app.py` runs it for every web request.
