# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Registo de Notificações de Violência contra Profissionais de Saúde** — A Flask web application for registering and analyzing violence incidents (verbal, physical, psychological) reported by healthcare professionals in the ULS-NE region (Bragança, Portugal).

### Key Features
- **Public incident submission** — Anonymous or confidential form submission
- **Admin dashboard** — Track incidents by status (open, in analysis, closed), unit, violence type, time patterns
- **Follow-up system** — Comments and status tracking for each incident
- **Email notifications** — Configurable SMTP for alerts
- **User management** — Admin authentication with role-based access

---

## Tech Stack

- **Flask 2.3.3** — Web framework
- **SQLAlchemy 3.1.1** — ORM for SQLite database
- **Flask-Login 0.6.3** — User authentication
- **Flask-WTF 1.2.1** — Form handling with CSRF protection
- **Gunicorn** — Production WSGI server
- **SQLite** — Database (auto-created at `instance/notificacoes.db`)

---

## Development

### Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
source venv/bin/activate
python run.py
```

App runs at `http://localhost:5000`

**Default admin credentials:**
- Username: `admin`
- Password: `Admin1234!`
- Admin panel: `http://localhost:5000/admin/login`

### Database

- Database is created automatically on first run at `instance/notificacoes.db`
- To reset after model changes: delete the `.db` file and restart the app
- Schema is seeded with default admin user on creation

### Email Configuration

SMTP settings are configured via the admin panel at `/admin/settings` and stored in the `SMTPConfig` model. Used for incident notifications.

---

## Architecture

### Core Models (`app/models.py`)

- **Notification** — Incident reports with metadata (date, time, location, violence types, victim/perpetrator info, descriptions, impact assessment)
- **User** — Admin users with password hashing
- **Comment** — Follow-up analysis/notes on incidents
- **SMTPConfig** — Email server configuration

**Key data:** Notifications track 6 violence types (physical, verbal, psychological, sexual, patrimonial, other), victim category (health professional, patient, visitor, other), perpetrator type, and local units (15 health centers + hospitals across the region).

### Routes (`app/routes/`)

- **public.py** — Public incident submission form and success pages
- **auth.py** — Admin login/logout
- **backoffice.py** — Incident dashboard, filtering, detail view
- **users.py** — Admin user management
- **settings.py** — SMTP configuration

### Templates (`app/templates/`)

- `public/` — Public-facing forms and status pages
- `admin/` — Admin dashboard and management pages
- `base.html` — Layout templates with internationalization support (Portuguese)

---

## Common Workflows

### Adding a New Field to Incidents

1. Add column to `Notification` model in `app/models.py`
2. Update the form in the relevant route (`public.py` or `backoffice.py`)
3. Update templates to display/edit the field
4. Delete `instance/notificacoes.db` and restart to regenerate schema

### Changing SMTP Configuration

Admin users configure email settings via `/admin/settings`. Settings are persisted in `SMTPConfig` table and loaded by `app/email_utils.py`.

### Filtering/Searching Incidents

Implement filters in `backoffice.py` route and pass query results to the dashboard template. The model properties like `tipos_violencia_labels` handle label translation.

---

## Production Deployment

```bash
sudo bash deploy.sh
```

Uses Gunicorn as WSGI server. Ensure `SECRET_KEY` environment variable is set (currently defaults to insecure dev value in `app/config.py`).

---

## Notes

- All authentication is admin-only; public incident submission is anonymous/unauthenticated
- Portuguese language used in UI, data fields, and user-facing text
- CSRF protection enabled globally via Flask-WTF
- Database uses SQLite for simplicity; consider migration to PostgreSQL for production scale
