# Star Social 🌟

A Django-based social media platform where users can create groups, write posts, and connect with others.

## Features

- 👥 **Groups** — Create and join interest-based groups
- 📝 **Posts** — Write posts globally or within groups (Markdown supported)
- 👤 **User Profiles** — View posts by specific users
- 🔐 **Authentication** — Secure signup, login, and logout

## Tech Stack

- **Backend**: Django 5.2 LTS, Python 3.12+
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: Bootstrap 5, Crispy Forms
- **Testing**: pytest, pytest-django
- **Static Files**: WhiteNoise

## Quick Start

### 1. Clone and setup

```bash
git clone https://github.com/mushkett/Social_media_site.git
cd Social_media_site

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY and ADMIN_URL to random values:
# python -c "import secrets; print(secrets.token_urlsafe(50))"  # for SECRET_KEY
# python -c "import secrets; print(secrets.token_urlsafe(16))"  # for ADMIN_URL
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 5. Start development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=html
```

## Project Structure

```
Social_media_site/
├── Social_media/       # Project configuration
│   └── settings/       # Settings (base, dev, prod)
├── accounts/           # User authentication
├── groups/             # Groups management
├── posts/              # Posts management
├── templates/          # Base templates
├── static/             # Static files (CSS)
└── tests/              # Test suite
```

## Using PostgreSQL (Optional)

For PostgreSQL, start the database with Docker:

```bash
docker compose up -d db
```

Then update `.env`:

```
DATABASE_URL=postgres://postgres:postgres@localhost:5432/social_media
```

## License

MIT
