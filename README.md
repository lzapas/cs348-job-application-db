# Job Application Tracker

A full-stack web application for tracking job applications, managing recruiter contacts, and generating analytics reports. Built for CS348 - Database Systems at Purdue University.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage](#usage)
- [Project Phases](#project-phases)
- [Screenshots](#screenshots)
- [Author](#author)
- [License](#license)

---

## Overview

The Job Application Tracker helps job seekers organize their applications, track communication with recruiters, and analyze their job search performance. This project demonstrates core database concepts including schema design, CRUD operations, complex queries, and analytics reporting.

## Features

### Phase 2 (Coming Soon)
- **Application Management** (CRUD)
  - Add, edit, and delete job applications
  - Track company, job title, salary, status, and application date
  - Manage multiple recruiter contacts per application
  
- **Analytics Dashboard**
  - Filter applications by status, date range, and company
  - View statistics including:
    - Average time to interview
    - Application success rate by company
    - Distribution of application statuses
    - Salary trends

### Phase 3 (Coming Soon)
- GCP Cloud SQL migration
- Advanced reporting with time-series analysis
- Export reports to CSV

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.9+ / Flask |
| **ORM** | SQLAlchemy |
| **Database** | SQLite (dev) → PostgreSQL on GCP Cloud SQL (prod) |
| **Frontend** | Jinja2 / HTML5 / CSS3 |
| **Deployment** | Google Cloud Platform (planned) |

## Database Schema

### Applications Table
```sql
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    job_title VARCHAR(200) NOT NULL,
    job_posting_url TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    status VARCHAR(50) NOT NULL,
    date_applied DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);