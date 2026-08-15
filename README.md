# Stub Signature-Based Efficient Public Data Auditing System

A Django-based prototype for efficient public data auditing in cloud computing using stub signatures, file hashing, and Paillier homomorphic encryption.

## Features

- User registration and login
- File upload and encryption using Paillier cryptography
- SHA-256 hashing for file integrity
- Cloud-service-provider workflow
- Third-party public cloud auditing workflow
- Audit challenge/proof/verification flow
- REST API endpoints for user records
- Django-based web interface

## Technology Stack

- Python
- Django 5.1.1
- Django REST Framework
- Paillier cryptosystem (`phe`)
- SQLite for local development
- HTML, CSS, JavaScript, Bootstrap

## Project Structure

```text
.
├── app/                 # Django application
├── project/             # Django project configuration
├── templates/           # HTML templates
├── static/              # CSS, JavaScript, images and vendor assets
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

Uploaded, encrypted, and decrypted runtime files are intentionally excluded from Git.

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and set your own values.

Important: never commit `.env` or real passwords/API keys to GitHub.

The application reads the following environment variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `CLOUD_EMAIL`
- `CLOUD_PASSWORD`
- `PTPC_EMAIL`
- `PTPC_PASSWORD`

This project does not load `.env` automatically. Set these variables in your operating-system environment or use a local environment-variable tool before running Django.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the local address shown by Django in your browser.

## Security Notes

- Do not commit `db.sqlite3`.
- Do not commit `.env`.
- Do not commit uploaded, encrypted, or decrypted files.
- Use a Gmail App Password for SMTP instead of your normal Gmail password.
- The original project contained credentials in source code; these have been removed from the GitHub-ready version and replaced with environment variables.
- This is an academic prototype and should receive additional security hardening before production deployment.

## Academic Project

This repository contains the implementation of the B.Tech project:

**Stub Signature-Based Efficient Public Data Auditing System Using Dynamic Procedures in Cloud Computing**

