# Copilot Instructions: Skincare Allergy Filter

Purpose: Make AI coding agents productive immediately in this Django repo by documenting the real architecture, workflows, and project-specific conventions.

## Big Picture
- Framework: Django 6.0 + Templates (SQLite in dev).
- Project: `skincare_project/` with apps: `allergies/`, `users/`.
- Auth: Custom user `users.CustomUser` (configured via `AUTH_USER_MODEL`).
- Domain: Predefined `Allergen` catalog; `UserAllergy` links a user to an `Allergen` with extra fields (severity, confirmation, source, JSON notes).

## Architecture & Routing
- Project URLs: See [skincare_project/urls.py](skincare_project/urls.py)
  - `''` → `views.home` renders [templates/home.html](templates/home.html).
  - `'product/'` → `views.product` renders [templates/product.html](templates/product.html).
  - `'allergies/'` → includes [allergies/urls.py](allergies/urls.py) → `allergies_list`.
  - Users app exists but is NOT included yet; add:
    - path: `path('users/', include('users.urls'))`
- Templates: Base layout at [templates/layout.html](templates/layout.html); all pages `{% extends 'layout.html' %}` and load static.

## Data Model Essentials
- Models: See [allergies/models.py](allergies/models.py) and choices in [allergies/constants/choices.py](allergies/constants/choices.py).
- `Allergen` fields: `category` (from `CATEGORY_CHOICES`), `allergen_key` (category-dependent), `is_active` with unique `(category, allergen_key)`.
- `UserAllergy`: `user` → `users.CustomUser`, `allergen` → `Allergen` (+ severity, confirmation, JSON fields). Unique `(user, allergen)`.
- Convenience: `Allergen.allergen_label` maps key to human label via `FLAT_ALLERGEN_LABEL_MAP`.

## Database Management
- **Local Development:** Use SQLite (`db.sqlite3`) for zero-config startup.
- **CI/CD:** Tests run against a fresh SQLite instance in GitHub Actions unless a `DATABASE_URL` is provided.
- **Migrations:** Always run `python manage.py makemigrations` and include them in commits.
- **Instruction:** When suggesting model changes, remind the user to run migrations to keep the local SQLite file in sync.

## Conventions
- Lint/Format: Ruff configured in [pyproject.toml](pyproject.toml) (target Python 3.14). Run `ruff check . --fix` and `ruff format .`.
- Typing: Use Python 3.14 type hints consistently for all function signatures and class attributes. Leverage modern syntax (`list[T]`, `dict[K,V]`, `type` statement for aliases).
- Paths: Prefer `pathlib.Path` over `os.path`.
- URLs: Use named routes (`name='home'`, `name='product'`) and `{% url '...' %}` in templates. Current root `home` is missing a name.
- Queries: For `UserAllergy` access, use `.select_related('allergen')` and filter `is_active=True`.

## Developer Workflows (Windows-friendly)
- Create venv + install:
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate`
  - `pip install -r requirements.txt`
- DB setup:
  - `python manage.py makemigrations allergies users`
  - `python manage.py migrate`
- Run server: `python manage.py runserver`
- Lint/format: `ruff check . --fix` then `ruff format .`

## CI/CD Standards
- **Pipeline Structure:** We use a tiered CI. Static analysis (Ruff/Mypy) is the 'Gatekeeper' and must pass before Tests run.
- **Workflow Dependency:** The `test` job depends on the `static-analysis` job via the `needs` keyword.
- **AI Guidance:** If a PR fails the first tier (Lint), do not attempt to debug tests. Fix formatting and type hints first.

## CI/CD Workflow
- **Gate 1 (Lint):** Pre-commit (Ruff + Mypy) must pass.
- **Gate 2 (Test):** Pytest suite must pass.
- **Gate 3 (Coverage):** Codecov enforces a minimum threshold based on the project phase (currently 50%).
- **Instruction:** If CI fails on 'Static Analysis', prioritize fixing Ruff/Mypy errors before modifying logic.

## Testing & Coverage Gate
- **Threshold:** Enforced via `[tool.coverage.report]` in `pyproject.toml`.
- **Phase 1 Target:** 50% (Current). AI should prioritize writing model tests for `Allergen` and `UserAllergy` to meet this.
- **Verification:** Before pushing, verify with `pytest`. If the exit code is non-zero due to coverage, ask the AI to: *"@workspace /explain which branches are missing coverage and generate the missing tests."*

## Testing & Coverage
- Test runner: `pytest` (pytest-django).
- Coverage (Phase 1 target 50% enforced):
  - `pytest --cov=allergies --cov=users --cov-report=term-missing`
  - HTML report: `pytest --cov --cov-report=html` → open `htmlcov/index.html`.
- Priority: Model tests for `Allergen.__str__`, `allergen_label`, `UserAllergy.clean()` and uniqueness.

## Extension Points
- Product safety check: implement POST handling in [skincare_project/views.py](skincare_project/views.py) `product` view.
  - Parse user-provided ingredient list.
  - Compare against active `UserAllergy` for `request.user` (join via `select_related('allergen')`).
  - Return matches (include severity/source).
- Users app routing: include [users/urls.py](users/urls.py) in project URLs; link from layout using `{% url 'user:list' %}`.

## Practical Snippets
- Active allergens ordered:
  - `from allergies.models import Allergen`
  - `Allergen.objects.filter(is_active=True).order_by('category', 'allergen_key')`
- Current user allergies with labels:
  - `from allergies.models import UserAllergy`
  - `qs = UserAllergy.objects.select_related('allergen').filter(user=request.user, is_active=True)`
  - `for ua in qs: label = ua.allergen.allergen_label`

## Gotchas
- `allergen_key` choices are category-dependent; leave `choices=[]` in the model and filter in forms.
- Ensure `UserAllergy.clean()` runs: save path uses `full_clean()` override; do not bypass `save()`.
- Static files are served from [static/](static) with `STATICFILES_DIRS` configured in settings.

## Python 3.14 + Django 6.0 Notes
- **Type Aliases:** Use the `type` statement for complex type aliases (e.g., `type AllergenDict = dict[str, str | int]`).
- **Performance:** Django 6.0 includes ORM optimizations; benchmark queries with `.explain()` when needed.
- **Async Views:** Django 6.0 enhances async support. For future product scanning endpoints, consider `async def product_check(request: HttpRequest)`.
- **Compatibility:** All dependencies in `requirements.txt` are compatible with Python 3.14 and Django 6.0.

For anything unclear or missing, call out what you need clarified (e.g., product safety parsing rules, users routes naming), and I'll refine this doc.

## Type Checking (Mypy)
- **Configuration:** Always respect the `[tool.mypy]` and `[tool.django-stubs]` blocks in `pyproject.toml`.
- **Django Stubs:** Use `QuerySet[Allergen]` or `Manager[Allergen]` when type-hinting complex ORM queries to ensure compatibility with `django-stubs`.
- **Workflow:** Run `mypy .` to verify type safety before committing logic changes to `allergies/models.py`.

## Type Safety & Quality Gate
- **Source of Truth:** All type configurations live in `pyproject.toml`.
- **Pre-commit:** We use `mypy` with `django-stubs`. If a commit fails, run `mypy .` locally to debug.
- **AI Instructions:** When writing new logic for `allergies/views.py`, ensure all functions have explicit type hints. If the AI suggests a generic `QuerySet`, prompt it to use specific model typing (e.g., `QuerySet[Allergen]`).
