# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django web application project named `testWebsite`. It's a standard Django project setup with a main application for building web functionality.

## Project Structure

```
testWebsite/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── venv/                 # Virtual environment
├── testWebsite/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
└── main/                 # Main Django app
    ├── __init__.py
    ├── admin.py         # Django admin configuration
    ├── apps.py          # App configuration
    ├── models.py        # Database models
    ├── views.py         # View functions
    ├── tests.py         # Unit tests
    └── migrations/      # Database migrations
```

## Common Development Commands

### Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

### Django Management
```bash
# Run development server
python manage.py runserver

# Run development server on specific port
python manage.py runserver 8001

# Make migrations after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

### Database Management
```bash
# Create and apply initial migrations
python manage.py makemigrations
python manage.py migrate

# Reset database (careful - this deletes data)
rm db.sqlite3
python manage.py migrate
```

### Dependency Management
```bash
# Install dependencies
pip install -r requirements.txt

# Add new dependency and update requirements
pip install <package_name>
pip freeze > requirements.txt
```

## Development Setup

1. **Activate virtual environment**: `source venv/bin/activate`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run migrations**: `python manage.py migrate`
4. **Start development server**: `python manage.py runserver`
5. **Access application**: http://127.0.0.1:8000/

## Key Django Concepts

### Apps
- `main/` - Primary application containing core functionality
- To create new apps: `python manage.py startapp <app_name>`

### URL Routing
- Main URL configuration in `testWebsite/urls.py`
- App-specific URLs should be created in `main/urls.py` and included in main config

### Models (Database)
- Define data models in `main/models.py`
- After model changes, always run: `python manage.py makemigrations` then `python manage.py migrate`

### Views
- Request handling logic in `main/views.py`
- Can be function-based or class-based views

### Templates
- Create `main/templates/` directory for HTML templates
- Configure template settings in `testWebsite/settings.py`

### Static Files
- Create `main/static/` directory for CSS, JavaScript, images
- Configure static files settings in `testWebsite/settings.py`

## Configuration Notes

- **Database**: Default SQLite database (`db.sqlite3`)
- **Django Version**: 4.2.23
- **Python Version**: 3.9
- **Debug Mode**: Enabled by default in development

## Next Steps for Development

1. Configure the `main` app in `testWebsite/settings.py` INSTALLED_APPS
2. Create URL patterns in `main/urls.py`
3. Create views in `main/views.py`
4. Create templates directory and HTML files
5. Define models if database functionality is needed
6. Set up static files directory for CSS/JS

## Security Notes

- Never commit `settings.py` with SECRET_KEY to public repositories
- Use environment variables for sensitive configuration in production
- Disable DEBUG mode in production
- Configure allowed hosts properly for production deployment