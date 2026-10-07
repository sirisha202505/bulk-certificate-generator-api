# Bulk Certificate Generator API

Bulk certificate generator API - AEREO SDE Intern Assignment.

## Features

- Create bulk certificate generation jobs
- Generate PDF certificates
- Track certificate generation status
- Retrieve generated certificates
- Download certificate PDFs

## API Endpoints

- POST `/jobs`
- GET `/jobs/{job_id}`
- GET `/jobs/{job_id}/certificates`
- GET `/certificates/{certificate_id}`

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- ReportLab
- SQLite
