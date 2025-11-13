# Copilot Instructions: Skincare Allergy Filter

Purpose: Help AI coding agents work productively in this Django project by documenting architecture, workflows, and project-specific patterns.

## Big Picture
- Framework: Django 5.2 (full-stack: views + templates) with SQLite (`db.sqlite3`).
- Project: `skincare_project/` with two apps: `allergies/` and `user/`.
- Frontend: Django templates under `templates/` with a base layout `templates/layout.html`; static assets under `static/` (wired via `{% load static %}`).
- Core domain: Allergen taxonomy in `allergies/constants/allergens.py`; models in `allergies/models.py` define `Allergy` and `UserAllergy` (ties to `django.contrib.auth.models.User`).
- Current feature state: Page routing + scaffolding exist (`home`, `product`, `allergies list`, `user list`). Product safety comparison logic is not implemented yet.

## Architecture & Routing
- Project URLs: `skincare_project/urls.py`
  - `''` → `skincare_project.views.home` (renders `templates/home.html`).
  - `'product/'` → `skincare_project.views.product` (renders `templates/product.html`).
  - `'allergies/'` → includes `allergies/urls.py`.
  - Admin at `'admin/'`.
- App URLs:
  - `allergies/urls.py`: `''` → `allergies.views.allergies_list` (`templates/allergies/allergies_list.html`).
  - `user/urls.py`: namespaced via `app_name = 'user'`; root path `''` → `user.views.user_list` (`templates/user/user_list.html`). Not yet included in project URLs.
- Templates:
  - Base: `templates/layout.html` (includes `static/js/main.js` and `static/css/style.css`).
  - Child pages extend the base using `{% extends 'layout.html' %}` and fill `block content`.

## Developer Workflows (Windows PowerShell)
- Create venv and install deps:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate
  pip install -r requirements.txt
  ```
- Run DB migrations:
  ```powershell
  python manage.py makemigrations allergies user
  python manage.py migrate
  ```
- Start dev server:
  ```powershell
  python manage.py runserver
  ```
- Run tests (none meaningful yet):
  ```powershell
  python manage.py test
  ```

## Project Conventions
- Views: Function-based views returning `render(request, template)`; keep logic thin and move domain code to helpers/services as it grows.
- URLs: Prefer named URL patterns. The project root currently lacks names; when adding/updating, include `name='...'` and use `{% url 'name' %}` in templates instead of hard-coded paths.
- App namespace: `user/urls.py` defines `app_name = 'user'`. Use `{% url 'user:list' %}` once the app is included in project URLs.
- Templates: Extend `templates/layout.html`. Put app-specific pages under `app_name/templates/app_name/`.
- Static files: Served from `static/` during dev; referenced via `{% load static %}` and `{% static 'path' %}`.
- Allergen taxonomy: Update `allergies/constants/allergens.py` to add categories/choices. Models use `ALLERGIES_CHOICES` for the `Allergy.category` field.
- Database: Default SQLite checked in (`db.sqlite3`) for dev; avoid writing production secrets to settings.

## Key Files
- `skincare_project/settings.py`: Template dirs, static files, installed apps.
- `skincare_project/urls.py`: Top-level routing and includes.
- `skincare_project/views.py`: `home` and `product` views.
- `allergies/models.py`: `Allergy` and `UserAllergy` models (ordering, uniqueness).
- `allergies/constants/allergens.py`: Authoritative list of allergen categories and items.
- `templates/layout.html`: Base layout and navigation.

## Practical Examples
- Include the `user` app at `/user/`:
  ```python
  # skincare_project/urls.py
  from django.urls import path, include
  urlpatterns = [
      # ...existing
      path('user/', include('user.urls')),
  ]
  ```
  Then link from templates:
  ```django
  <a href="{% url 'user:list' %}">Users</a>
  ```
- Name root URLs for template usage:
  ```python
  # skincare_project/urls.py
  from . import views
  urlpatterns = [
      path('', views.home, name='home'),
      path('product/', views.product, name='product'),
  ]
  ```
  ```django
  <a href="{% url 'home' %}">Home</a>
  <a href="{% url 'product' %}">Product</a>
  ```
- Query active allergens ordered by category/name:
  ```python
  from allergies.models import Allergy
  active = Allergy.objects.filter(is_active=True).order_by('category', 'name')
  ```

## Extension Points
- Product safety check: `templates/product.html` posts ingredients to the same route; add POST handling in `skincare_project/views.product` and compare against `UserAllergy` and/or `Allergy.common_names`.
- Admin UX: Register `Allergy`/`UserAllergy` in `allergies/admin.py` for easy management.

Notes: The repository includes a dev `SECRET_KEY` and SQLite DB for convenience only. Treat them as development artifacts.
