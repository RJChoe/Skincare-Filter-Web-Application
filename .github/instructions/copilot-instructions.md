# Copilot Instructions: Skincare Allergy Filter

Purpose: Make AI coding agents productive immediately in this Django repo by documenting the real architecture, workflows, and project-specific conventions.

## Big Picture
- Framework: Django 6.0 + Templates (SQLite in dev).
- Language: Python 3.14 (Leverage `type` aliases and T-strings)
- Environment & PDM: Standardize on `uv`. Always use `uv run` for executing management commands or scripts.
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
- **Instruction:** When suggesting model changes, remind the user to run migrations to keep the local SQLite file in sync.

## Conventions
- Lint/Format: Ruff configured in [pyproject.toml](pyproject.toml) (target Python 3.14). Run `ruff check . --fix` and `ruff format .`.
- Typing: Use Python 3.14 type hints consistently for all function signatures and class attributes. Leverage modern syntax (`list[T]`, `dict[K,V]`, `type` statement for aliases).
- Paths: Prefer `pathlib.Path` over `os.path`.
- URLs: Use named routes (`name='home'`, `name='product'`) and `{% url '...' %}` in templates. Current root `home` is missing a name.
- Queries: For `UserAllergy` access, use `.select_related('allergen')` and filter `is_active=True`.

## Dependency & Environment Management (`uv`)
- **Execution:** Never ask the user to "activate venv." Use `uv run <command>` (e.g., `uv run python manage.py migrate`).
- **Add Packages:** Use `uv add <package>` for base deps and `uv add --group <name> <package>` for specific groups (test, lint, type-check, security).
- **Syncing:** Use `uv sync` to ensure the environment matches `uv.lock`.
- **Version Pinning:** Respect `.python-version` and `requires-python = ">=3.14"` in `pyproject.toml`.

## 3. Django 6.0 Conventions
- **Background Tasks:** Prefer the native `django.tasks` framework over Celery for lightweight operations like email or data cleanup.
- **Template Partials:** Use `{% partialdef %}` and `{% partial %}` tags within templates to handle modular components (HTMX-friendly) instead of excessive `{% include %}` calls.
- **Type Safety:** Use `TypeAlias` for complex types and explicitly hint all QuerySets as `QuerySet[ModelName]` or `Manager[ModelName]` to satisfy `django-stubs`.

## 4. Coding Standards (Ruff & Mypy)
- **Linting:** Follow **Ruff** conventions. Use `_` for intentionally unused variables in tuple unpacking (e.g., `for key, _, list in choices:`).
- **Validation:** Run `uv run mypy .` before proposing logic changes
- **Mypy:** If a ManyToManyField assignment throws an "Incompatible types" error (common in `AbstractUser` overrides), use `# type: ignore[assignment]`.
- **Async:** Use `async def` for I/O bound views (like external product scanning) where supported by Django 6.0.

## CI/CD Workflow
**CI Awareness:** The CI enforces `.python-version` and `uv lock --check`. Always ensure the lockfile is synced before suggesting a commit.
- **Testing:** Use `pytest` for all new features. Place tests in `app/tests/` and run via `uv run pytest`.
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
- **T-Strings:** Use Python 3.14 Template Strings (`t"..."`) for safer string processing where applicable
- **Compatibility:** All dependencies in `requirements.txt` are compatible with Python 3.14 and Django 6.0.

For anything unclear or missing, call out what you need clarified (e.g., product safety parsing rules, users routes naming), and I'll refine this doc.

## AI Interaction Rules
- **DRY Principle:** Avoid suggesting duplicate code; refactor shared logic into utility functions or model methods (e.g., allergen lookup, validation helpers).
- **Check Configuration First:** Before suggesting style, dependency, or tool changes, reference `pyproject.toml` (Ruff, Mypy, Pytest configs are the source of truth).
- **Tests Required:** All new features must include corresponding `pytest` tests in `app/tests/`. No feature proposal is complete without test coverage.

## Type Checking (Mypy)
- **Configuration:** Always respect the `[tool.mypy]` and `[tool.django-stubs]` blocks in `pyproject.toml`.
- **Django Stubs:** Use `QuerySet[Allergen]` or `Manager[Allergen]` when type-hinting complex ORM queries to ensure compatibility with `django-stubs`.
- **Workflow:** Run `mypy .` to verify type safety before committing logic changes to `allergies/models.py`.

## Type Safety & Quality Gate
- **Source of Truth:** All type configurations live in `pyproject.toml`.
- **Pre-commit:** We use `mypy` with `django-stubs`. If a commit fails, run `mypy .` locally to debug.
- **AI Instructions:** When writing new logic for `allergies/views.py`, ensure all functions have explicit type hints. If the AI suggests a generic `QuerySet`, prompt it to use specific model typing (e.g., `QuerySet[Allergen]`).
