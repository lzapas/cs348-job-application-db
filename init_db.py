"""Create job_tracker.db from schema.sql, then print the applications to check it worked."""
import sqlite3

conn = sqlite3.connect('job_tracker.db')

with open('schema.sql') as f:
    conn.executescript(f.read())  # runs every statement in the file
conn.commit()

# Check: list each application with its company/status/type names instead of ids
rows = conn.execute("""
    SELECT a.date_applied, c.name, a.job_title, s.name, jt.name, a.salary
    FROM applications a
    JOIN companies c  ON c.id  = a.company_id
    JOIN statuses s   ON s.id  = a.status_id
    JOIN job_types jt ON jt.id = a.job_type_id
    ORDER BY a.date_applied DESC
""").fetchall()

for row in rows:
    print(row)

conn.close()
