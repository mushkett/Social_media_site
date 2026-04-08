# CLAUDE.md - AI Assistant Guide for Social Media Site

## Project Overview

Django-based social media platform with groups and posts functionality. Users can create/join groups and publish posts within groups or globally.

## Tech Stack

- **Python**: 3.12+
- **Django**: 5.2+ LTS
- **Database**: PostgreSQL (via Docker for local dev)
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Security**: django-csp, django-ratelimit, nh3 (HTML sanitization)
- **Testing**: pytest + pytest-django
- **Static Files**: WhiteNoise

## Quick Commands

```bash
# Development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Shell
python manage.py shell_plus  # django-extensions

# Docker PostgreSQL (local development)
docker compose up -d db
```

## Project Structure

```
Social_media_site/
├── Social_media/           # Main project configuration
│   ├── settings/
│   │   ├── base.py         # Common settings
│   │   ├── dev.py          # Development settings (DEBUG=True)
│   │   └── prod.py         # Production settings
│   ├── urls.py             # Root URL configuration
│   └── views.py            # Homepage view
├── accounts/               # User authentication app
│   ├── forms.py            # UserCreateForm
│   ├── urls.py             # login, logout, signup
│   └── views.py            # SignUp view
├── groups/                 # Groups management app
│   ├── models.py           # Group, GroupMember
│   ├── urls.py             # CRUD + join/leave
│   └── views.py            # CBV for groups
├── posts/                  # Posts management app
│   ├── models.py           # Post
│   ├── urls.py             # CRUD + user posts
│   └── views.py            # CBV for posts
├── templates/              # Project-level templates
│   └── base.html           # Main layout (Bootstrap 5)
├── static/css/             # Static CSS
├── docker-compose.yml      # PostgreSQL container
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Python dependencies
```

## Django Apps

### accounts

- Uses Django's built-in `User` model
- Custom `SignUp` view with `UserCreationForm`
- URLs: `/accounts/login/`, `/accounts/logout/`, `/accounts/signup/`

### groups

- **Models**: `Group`, `GroupMember` (M2M through table)
- **Features**: Create, list, detail, join/leave groups
- **URLs**: `/groups/`, `/groups/new/`, `/groups/<slug>/`, `/groups/join/<slug>/`, `/groups/leave/<slug>/`
- Join/leave operations use POST requests with CSRF protection

### posts

- **Models**: `Post` (with optional group FK)
- **Features**: CRUD for posts, user post list, group-filtered posts
- **URLs**: `/posts/`, `/posts/new/`, `/posts/<pk>/`, `/posts/by/<username>/`, `/posts/in/<slug>/`
- Markdown rendering with HTML sanitization (nh3)

## Code Conventions

### Views

- Use **Class-Based Views** (CBV) exclusively
- Inherit from Django generic views: `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`
- Use `LoginRequiredMixin` for authenticated views
- Use `UserPassesTestMixin` for permission checks

### Models

- Use `UniqueConstraint` instead of deprecated `unique_together`
- Use `models.TextChoices` for choice fields
- Always add `__str__` method
- Use `related_name` for ForeignKey/ManyToMany

### URLs

- Use path converters: `<int:pk>`, `<slug:slug>`, `<str:username>`
- Name all URL patterns for `reverse()` usage
- Use app namespaces: `app_name = 'groups'`

### Templates

- Namespace app templates: `app/templates/app/template.html`
- Use `{% block %}` inheritance from `base.html`
- Escape user content, use `|safe` only for sanitized HTML

### Forms

- Use `crispy_forms` with Bootstrap 5 pack
- Validate in `clean_*` methods
- Use POST for state-changing operations

### Testing

- Use pytest with pytest-django
- Test files: `tests/test_*.py` or `app/tests/test_*.py`
- Use fixtures for common test data
- Aim for >80% coverage

## Environment Variables

Required in `.env` file (copy from `.env.example`):

```env
# Django
SECRET_KEY=your-secret-key-here   # generate: python -c "import secrets; print(secrets.token_urlsafe(50))"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3  # or postgres://postgres:postgres@localhost:5432/social_media

# Django settings module
DJANGO_SETTINGS_MODULE=Social_media.settings.dev

# Admin panel URL — use a random secret string
ADMIN_URL=your-secret-admin-path   # generate: python -c "import secrets; print(secrets.token_urlsafe(16))"
```

## Database

### Local Development (Docker)

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: social_media
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Models Diagram

```
User (django.contrib.auth)
  │
  ├──< GroupMember >── Group (M2M through)
  │
  └──< Post >── Group (optional FK)
```

## Security Checklist

- [x] SECRET_KEY from environment variable (required, no default)
- [x] Admin URL randomised via `ADMIN_URL` env var
- [x] Admin login rate-limited (5 POST/hour per IP via django-ratelimit)
- [x] CSP configured (django-csp) — no `data:` in img-src
- [x] Markdown sanitized with nh3 (http/https only, no javascript: URIs)
- [x] SameSite + HttpOnly cookies in production
- [x] HSTS, SSL redirect, CSRF protection enabled in production
- [x] `DeleteGroup` scoped to creator via `get_queryset()`
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS properly configured for production domain
- [ ] No sensitive data in git (.env in .gitignore)

## Common Tasks

### Adding a new model field

1. Add field to model
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. Update forms/views/templates if needed
5. Add tests

### Adding a new view

1. Create view class in `views.py`
2. Add URL pattern in `urls.py`
3. Create template
4. Add tests

### Debugging

```python
# In shell_plus
from groups.models import Group
Group.objects.all()

# SQL logging in settings
LOGGING = {
    'loggers': {
        'django.db.backends': {'level': 'DEBUG'}
    }
}
```

## Known Issues / TODOs

- [ ] Add email verification for signup
- [ ] Add password reset functionality
- [ ] Add user profile page
- [ ] Add post comments
- [ ] Add post likes
- [ ] Add pagination to list views
- [ ] Add search functionality
- [ ] Add notifications
