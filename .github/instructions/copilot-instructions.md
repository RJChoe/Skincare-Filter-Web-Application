# Copilot Instructions: Skincare Allergy Filter

Purpose: Make AI coding agents productive immediately in this Django repo by documenting the real architecture, workflows, and project-specific conventions.

## Big Picture
- Framework: Django 6.0 + Templates (SQLite in dev).
- Language: Python 3.13 (Leverage modern type hints with `type` aliases)
- Environment & PDM: Standardize on `uv`. Always use `uv run` for executing management commands or scripts.
- Project: `skincare_project/` with apps: `allergies/`, `users/`.
- Auth: Custom user `users.CustomUser` (configured via `AUTH_USER_MODEL`).
- Domain: Predefined `Allergen` catalog; `UserAllergy` links a user to an `Allergen` with extra fields (severity_level, is_confirmed, source_info, JSON reaction details).

## 🚀 Quick Start for AI Agents

### Current Project Status

**✅ Completed Development Gates:**
- **Gate 1 (Dependencies):** `django-environ` installed and configured
- **Gate 2 (Logging):** Comprehensive logging in [allergies/admin.py](allergies/admin.py#L12), [allergies/views.py](allergies/views.py), [users/tests.py](users/tests.py)
- **Gate 3 (Error Handling):** Try-except blocks with transaction management in views and admin actions

**⏳ In Progress / Not Started:**
- **Gate 4 (Forms):** ❌ No `forms.py` files exist yet
- **Gate 5 (Tests):** 🚧 Comprehensive user tests (382 lines) exist, but [allergies/tests/test_models.py](allergies/tests/test_models.py#L59) has TODO for `UserAllergy` model tests

### Key Files Reference

| File | Purpose | Key Contents |
|------|---------|-------------|
| [allergies/models.py](allergies/models.py) | Core data models | `Allergen`, `UserAllergy` with validation at [L74-L82](allergies/models.py#L74-L82) |
| [conftest.py](conftest.py) | Test fixtures | `test_user`, `authenticated_client`, `contact_allergen`, `user_allergy` |
| [pyproject.toml](pyproject.toml) | Project config | Dependencies, Ruff (py313), Mypy, coverage settings |
| [allergies/constants/choices.py](allergies/constants/choices.py) | Allergen catalog | `CATEGORY_CHOICES`, `ALLERGEN_CHOICES`, `FLAT_ALLERGEN_LABEL_MAP` |
| [allergies/admin.py](allergies/admin.py) | Admin interface | Custom actions with logging, fieldsets |
| [users/tests.py](users/tests.py) | User model tests | 382 lines of comprehensive test coverage |

### Critical Field Names (Use These Exactly)

**UserAllergy Model Fields:**
- ✅ `severity_level` (CharField with choices: `mild`, `moderate`, `severe`, `unknown`) — NOT "severity"
- ✅ `is_confirmed` (BooleanField) — NOT "confirmation" or "confirmation_status"
- ✅ `source_info` (CharField with choices: `medical_professional`, `self_reported`, `testing`, `family_history`) — NOT "source"
- ✅ `user_reaction_details` (JSONField) — User-facing notes
- ✅ `admin_notes` (JSONField) — Admin-facing notes
- ✅ `symptom_onset_date` (DateField, nullable)

**Allergen Model Fields:**
- `category`, `allergen_key`, `is_active`, `created_at`, `updated_at`
- Unique constraint: `(category, allergen_key)`

### Python Version & Dependencies

- **Python:** 3.13 (NOT 3.14 — no T-strings or other 3.14-only features)
- **Django:** 6.0
- **Package Manager:** `uv` (always use `uv run` commands)
- **Ruff Target:** py313

## 📋 Common Commands

### Setup & Environment

```bash
# Install uv (if not already installed)
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.13 and pin version
uv python install 3.13
uv python pin 3.13

# Create virtual environment and sync dependencies
uv venv
uv sync                  # Install base dependencies
uv sync --group dev      # Install all dev dependencies (test, lint, type-check, security)

# Add new dependencies
uv add <package>                # Base dependencies
uv add --group test <package>   # Test group
uv add --group lint <package>   # Lint group
```

### Testing Workflow

```bash
# Run all tests with coverage
uv run pytest --cov --cov-report=term-missing

# Run specific test file
uv run pytest allergies/tests/test_models.py -v

# Run tests matching pattern
uv run pytest -k test_allergen

# Run only unit tests (skip integration)
uv run pytest -m "not integration"

# Generate HTML coverage report
uv run pytest --cov --cov-report=html
# Then open htmlcov/index.html in browser

# Show test summary
uv run pytest -ra
```

### Linting & Formatting

```bash
# Check code with Ruff
uv run ruff check .

# Auto-fix Ruff issues
uv run ruff check --fix .

# Format code with Ruff
uv run ruff format .

# Run all pre-commit checks
uv run pre-commit run --all-files

# Install pre-commit hooks
uv run pre-commit install
```

### Type Checking

```bash
# Type check specific modules
uv run mypy allergies users skincare_project

# Type check entire project
uv run mypy .
```

### Django Management

```bash
# Create and apply migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Start development server
uv run python manage.py runserver

# Create superuser for admin access
uv run python manage.py createsuperuser

# Django shell
uv run python manage.py shell

# Show current migration status
uv run python manage.py showmigrations

# Rollback migrations (example: rollback allergies app)
uv run python manage.py migrate allergies zero
```

### Security & Code Quality

```bash
# Security scanning with Bandit
uv run bandit -r allergies users skincare_project

# Check for vulnerable dependencies
uv run safety scan --non-interactive

# Production deployment check
uv run python manage.py check --deploy
```

### Deployment Workflow

```bash
# 1. Run full test suite
uv run pytest --cov

# 2. Check linting and formatting
uv run ruff check . --fix
uv run ruff format .

# 3. Type checking
uv run mypy .

# 4. Security checks
uv run bandit -r allergies users skincare_project
uv run safety scan --non-interactive

# 5. Production readiness check
uv run python manage.py check --deploy

# 6. Collect static files (production)
uv run python manage.py collectstatic --noinput
```

## Current Patterns vs. Future Features

**⚠️ IMPORTANT:** This section clarifies which Django 6.0 features are currently used vs. aspirational. Always use implemented patterns unless planning a major refactor.

### ✅ Current Patterns (Implemented & Recommended)

Use these patterns in current development:

- **Synchronous Views:** All views are standard `def` functions (see [skincare_project/views.py](skincare_project/views.py), [allergies/views.py](allergies/views.py)).
- **Traditional Templates:** Use `{% extends 'layout.html' %}` and `{% include %}` for template composition (see [templates/layout.html](templates/layout.html)).
- **SQLite Development Database:** Default `db.sqlite3` for local development (see [Database Management](#database-management)).
- **Type Hints:** Use Python 3.13 modern syntax `list[T]`, `dict[K,V]`, `type` statement for aliases (see [allergies/models.py](allergies/models.py)).
- **Ruff + Mypy:** Linting and type checking enforced in pre-commit (see [.pre-commit-config.yaml](.pre-commit-config.yaml)).
- **uv Package Manager:** All commands via `uv run` (see [Common Commands](#-common-commands)).

### 🚧 Future Django 6.0 Features (⚠️ NOT USED IN THIS PROJECT)

These Django 6.0 capabilities exist but are **not implemented** in this codebase. Mark as "Future Enhancement" when suggesting:

| Feature | Django 6.0 Capability | Current Status | When to Consider |
|---------|----------------------|----------------|------------------|
| **Async Views** | `async def` view functions | ⚠️ NOT USED | External API integration (product scanning) |
| **Template Partials** | `{% partialdef %}` / `{% partial %}` | ⚠️ NOT USED | HTMX dynamic UI updates |
| **Background Tasks** | `django.tasks` framework | ⚠️ NOT USED | Email notifications, data cleanup |
| **Form Field Groups** | New form rendering API | ⚠️ NOT USED | Complex multi-section forms |

**Example: Async Views (NOT CURRENTLY USED)**
```python
# ⚠️ Future pattern (not implemented in this project)
async def product_check(request: HttpRequest):
    ingredient_data = await fetch_product_api(barcode)  # External API call
    matches = await check_allergens_async(ingredient_data, request.user)
    return JsonResponse({'matches': matches})
```

**Example: Template Partials (NOT CURRENTLY USED)**
```html
<!-- ⚠️ Future pattern (not implemented in this project) -->
{% partialdef allergen-row allergen=allergen %}
    <tr id="allergen-{{ allergen.id }}">
        <td>{{ allergen.allergen_label }}</td>
        <td>{{ allergen.category }}</td>
    </tr>
{% endpartialdef %}
```

**Example: Background Tasks (NOT CURRENTLY USED)**
```python
# ⚠️ Future pattern (not implemented in this project)
from django.tasks import task

@task
def send_allergy_alert_email(user_id, allergen_id):
    # Async email sending
    pass

# Usage: send_allergy_alert_email.enqueue(user.id, allergen.id)
```

### Implementation Guidance

When users ask about these features:
1. **Acknowledge** the Django 6.0 capability exists.
2. **Clarify** it's not currently implemented in this project.
3. **Recommend** synchronous/traditional patterns for consistency.
4. **Document** as "Future Enhancement" if it aligns with project roadmap (e.g., async for external APIs).

Example response:
> "Django 6.0 supports `{% partialdef %}` for HTMX integration, but this project currently uses traditional `{% include %}` tags (see [templates/layout.html](templates/layout.html)). For consistency, continue using `{% include %}` unless we plan to refactor for HTMX support."

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
- `UserAllergy`: `user` → `users.CustomUser`, `allergen` → `Allergen` (+ severity_level, is_confirmed, source_info, JSON fields). Unique `(user, allergen)`.
- Convenience: `Allergen.allergen_label` maps key to human label via `FLAT_ALLERGEN_LABEL_MAP`.

## Database Management
- **Local Development:** Use SQLite (`db.sqlite3`) for zero-config startup.
- **CI/CD:** Tests run against a fresh SQLite instance in GitHub Actions unless a `DATABASE_URL` is provided.
- **Instruction:** When suggesting model changes, remind the user to run migrations to keep the local SQLite file in sync.

## Conventions
- Lint/Format: Ruff configured in [pyproject.toml](pyproject.toml) (target Python 3.13 / py313). Run `ruff check . --fix` and `ruff format .`.
- Typing: Use Python 3.13 type hints consistently for all function signatures and class attributes. Leverage modern syntax (`list[T]`, `dict[K,V]`, `type` statement for aliases).
- Paths: Prefer `pathlib.Path` over `os.path`.
- URLs: Use named routes (`name='home'`, `name='product'`) and `{% url '...' %}` in templates. Current root `home` is missing a name.
- Queries: For `UserAllergy` access, use `.select_related('allergen')` and filter `is_active=True`.

## Dependency & Environment Management (`uv`)
- **Execution:** Never ask the user to "activate venv." Use `uv run <command>` (e.g., `uv run python manage.py migrate`).
- **Add Packages:** Use `uv add <package>` for base deps and `uv add --group <name> <package>` for specific groups (test, lint, type-check, security).
- **Syncing:** Use `uv sync` to ensure the environment matches `uv.lock`.
- **Version Pinning:** Respect `.python-version` and `requires-python = ">=3.13"` in `pyproject.toml`.
- **Required Dependencies:** `django-environ` is **required** (not optional) - install with `uv add django-environ`. See [docs/SECURITY.md](docs/SECURITY.md) for environment variable management.

## Error Handling & Resilience
- **Custom Exceptions:** Define domain-specific exceptions in `app/exceptions.py` (e.g., `AllergenNotFoundError`, `InvalidIngredientError`) for clear error semantics.
- **Transaction Management:** Use `@transaction.atomic` decorator for operations modifying multiple models to ensure database consistency and automatic rollback on errors.
- **View Error Handling:** Wrap business logic in try-except blocks with user-friendly error messages:
  ```python
  from django.db import transaction
  from django.core.exceptions import ValidationError
  import logging

  logger = logging.getLogger(__name__)

  @transaction.atomic
  def create_user_allergy(request):
      try:
          # Business logic here
          user_allergy.full_clean()  # Validates model constraints
          user_allergy.save()
      except ValidationError as e:
          logger.warning(f"Validation failed for user {request.user.id}: {e}")
          # Surface error to user via form or message
      except Exception as e:
          logger.error(f"Unexpected error creating allergy: {e}", exc_info=True)
          # Show generic error message, don't expose internals
  ```
- **Validation Errors:** Surface `model.ValidationError` in forms, never let them become 500 errors. Use `full_clean()` before `save()` (see [allergies/models.py](allergies/models.py) for pattern).
- **Graceful Degradation:** For external API calls (future product scanning), implement timeout, retry logic, and fallback responses.

## Logging Standards
- **Setup:** Add `logger = logging.getLogger(__name__)` at module level in **all views, models with business logic, and admin files**.
- **Security Events (INFO level):** Log user authentication, `UserAllergy` CRUD operations (create/update/delete), admin actions:
  ```python
  logger.info(f"User {user.id} created allergy {allergy.id} for allergen {allergen.allergen_key}")
  ```
- **Errors (ERROR level):** Log validation failures, database errors, external API failures with traceback:
  ```python
  logger.error(f"Failed to process ingredient list: {e}", exc_info=True)
  ```
- **Performance (DEBUG level):** Log slow queries, ORM query counts (development only):
  ```python
  logger.debug(f"Query took {elapsed}s: {query}")
  ```
- **Configuration:** See `LOGGING` in [settings.py](skincare_project/settings.py) for structured logging. Production should log to external service (e.g., Sentry, CloudWatch).
- **GDPR Compliance:** Do **not** log personal data (emails, passwords). Log user IDs only.

## Known Gaps & Implementation Status

### ✅ Completed Foundations

- ✅ **Logging Infrastructure:** Comprehensive logging implemented in [allergies/admin.py](allergies/admin.py#L12), [allergies/views.py](allergies/views.py), and admin actions with INFO/ERROR levels.
- ✅ **Error Handling:** Try-except blocks with `@transaction.atomic` in views and admin actions. Model validation at [allergies/models.py](allergies/models.py#L74-L82).
- ✅ **django-environ Dependency:** Installed and configured in [skincare_project/settings.py](skincare_project/settings.py).
- ✅ **User Tests:** Comprehensive 382-line test suite in [users/tests.py](users/tests.py) with CustomUser model coverage.
- ✅ **View Tests:** Allergy view tests exist in [allergies/tests/test_views.py](allergies/tests/test_views.py) and admin error handling tests in [allergies/tests/test_admin_error_handling.py](allergies/tests/test_admin_error_handling.py).

### Current Implementation Gaps (Prioritized)

- ❌ **Forms Implementation:** No `forms.py` files exist. Need `UserAllergyForm` with dynamic `allergen_key` filtering based on category selection. **BLOCKED:** Until Gate 4 requirements met.
- 🚧 **Model Tests Incomplete:** [allergies/tests/test_models.py](allergies/tests/test_models.py#L59) has TODO comment for `UserAllergy` model tests (severity_level, is_confirmed, user_reaction_details fields).

### Blocked Features (Cannot Implement Until Foundations Complete)

- 🚫 **Product Safety Check POST Handler:** Cannot implement until logging + error handling exist in [skincare_project/views.py](skincare_project/views.py).
- 🚫 **User Forms & Validation:** Cannot implement until `UserAllergyForm` created with proper error surfacing.
- 🚫 **Users App Routing:** Cannot include [users/urls.py](users/urls.py) until views have logging and error handling.

## Development Gates (Strict Priority Order)

**Current Status:** Gates 1-3 ✅ COMPLETE. Focus on Gates 4-5.

### Gate 1: Dependency Fix — ✅ COMPLETE
1. ✅ `django-environ` installed and configured in [pyproject.toml](pyproject.toml)
2. ✅ Verified working in [skincare_project/settings.py](skincare_project/settings.py)
3. ✅ Lockfile synced

### Gate 2: Logging Infrastructure — ✅ COMPLETE
1. ✅ `logger = logging.getLogger(__name__)` added to:
   - [allergies/admin.py](allergies/admin.py#L12)
   - [allergies/views.py](allergies/views.py)
   - Admin custom actions with INFO/ERROR logging
2. ✅ Security events logged (user actions at INFO level)
3. ✅ Production logging configured in [settings.py](skincare_project/settings.py)

### Gate 3: Error Handling — ✅ COMPLETE
1. ✅ Try-except blocks in view functions with user-friendly error messages
2. ✅ `@transaction.atomic` implemented for multi-model operations
3. ✅ Custom exception classes in [allergies/exceptions.py](allergies/exceptions.py)
4. ✅ Validation errors properly surfaced (no 500 errors)

### Gate 4: Forms & Validation — ⏳ NOT STARTED (UNBLOCKED)
1. Create `allergies/forms.py` with `UserAllergyForm`
2. Implement dynamic `allergen_key` filtering (category-dependent)
3. Add CSRF protection in templates
4. Test form validation with comprehensive test coverage

### Gate 5: Complete Tests (PARALLEL WITH GATE 4)
1. Fill [users/tests.py](users/tests.py) with `CustomUser` model tests
2. Complete [allergies/tests/test_models.py](allergies/tests/test_models.py) TODO at line 59
3. Add view tests for [allergies/views.py](allergies/views.py)
4. Add integration tests with `@pytest.mark.integration`
5. Ensure coverage meets 50% minimum (current phase 1 threshold)

**After Gates 1-3 Complete:** Can implement product safety check POST handler and user management features.

## Forms & User Input Validation

**Current Status:** ❌ No forms implemented yet. Must complete Development Gates 1-3 before creating forms.

### ModelForm Pattern (Future Implementation)

When implementing forms (after Gates 1-3), follow this pattern:

```python
# allergies/forms.py (to be created)
from django import forms
from django.core.exceptions import ValidationError
from allergies.models import UserAllergy, Allergen
from allergies.constants.choices import FLAT_ALLERGEN_LABEL_MAP
import logging

logger = logging.getLogger(__name__)

class UserAllergyForm(forms.ModelForm):
    """Form for creating/editing user allergies with dynamic allergen_key filtering."""

    class Meta:
        model = UserAllergy
        fields = ['allergen', 'severity_level', 'is_confirmed', 'source_info', 'user_reaction_details']
        widgets = {
            'user_reaction_details': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter allergen choices to active only
        self.fields['allergen'].queryset = Allergen.objects.filter(is_active=True)

    def clean(self):
        """Custom validation beyond model constraints."""
        cleaned_data = super().clean()
        allergen = cleaned_data.get('allergen')
        severity_level = cleaned_data.get('severity_level')

        if severity_level == 'severe' and not cleaned_data.get('is_confirmed'):
            logger.warning("Severe allergy without confirmation")
            raise ValidationError("Severe allergies require confirmation")

        return cleaned_data
```

### Dynamic Choice Filtering (Category-Dependent allergen_key)

The `allergen_key` choices depend on `category` selection. Implement with JavaScript/HTMX:

```html
<!-- Template pattern for dynamic filtering -->
<form method="post" id="allergy-form">
    {% csrf_token %}

    <select name="category" id="id_category" hx-get="{% url 'allergies:get_allergen_keys' %}" hx-target="#allergen-key-select">
        <option value="">Select Category</option>
        {% for value, label in CATEGORY_CHOICES %}
            <option value="{{ value }}">{{ label }}</option>
        {% endfor %}
    </select>

    <select name="allergen_key" id="allergen-key-select">
        <option value="">Select allergen...</option>
    </select>

    {{ form.as_p }}
    <button type="submit">Save Allergy</button>
</form>
```

### CSRF Protection

- **Middleware:** Already configured in [settings.py](skincare_project/settings.py) (`CsrfViewMiddleware`).
- **Templates:** Always include `{% csrf_token %}` in POST forms.
- **AJAX:** Include CSRF token in headers for JavaScript requests:
  ```javascript
  fetch(url, {
      method: 'POST',
      headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  });
  ```

### Form Error Display

```html
<!-- Display form errors in templates -->
{% if form.errors %}
    <div class="error-messages">
        {{ form.non_field_errors }}
        {% for field in form %}
            {% if field.errors %}
                <p>{{ field.label }}: {{ field.errors }}</p>
            {% endif %}
        {% endfor %}
    </div>
{% endif %}
```

### Validation Order

1. **Form.clean():** Custom cross-field validation (e.g., severity + confirmation check).
2. **Model.clean():** Model-level constraints (see [allergies/models.py](allergies/models.py#L74-L82) for `UserAllergy.clean()`).
3. **Model.save():** Database constraints (unique together, foreign keys).

Always call `form.is_valid()` before accessing `form.cleaned_data` to ensure all validation runs.

## Security Hardening (Production)

**See [docs/SECURITY.md](docs/SECURITY.md) for comprehensive security guidance.**

### Quick Reference

- **Required Settings:** Run `uv run python manage.py check --deploy` before production deployment.
- **SSL/HTTPS:** Set all `SECURE_*` and `*_COOKIE_SECURE` settings to `True` in production (see [docs/SECURITY.md](docs/SECURITY.md#production-security-settings)).
- **Headers:** Configure `SECURE_HSTS_SECONDS`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF` (conditional on `DEBUG=False`).
- **Environment:** Never commit `.env` file; use [.env.example](.env.example) as template. Install `django-environ` (required): `uv add django-environ`.
- **Dependencies:** Run `uv run safety check` and `uv run bandit -r allergies users skincare_project` before commits.

### Conditional Security Settings Pattern

```python
# settings.py pattern
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
    SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
    # ... see docs/SECURITY.md for complete list
```

## Migration Workflow

### Schema Migrations (Model Changes)

1. **After modifying models** in [allergies/models.py](allergies/models.py) or [users/models.py](users/models.py):
   ```bash
   uv run python manage.py makemigrations
   ```
2. **Review generated migration** in `app/migrations/` before committing.
3. **Apply migration** to local SQLite:
   ```bash
   uv run python manage.py migrate
   ```
4. **Commit both** the model changes and migration file.

### Data Migrations (Seed Data)

For populating `Allergen` catalog from [allergies/constants/choices.py](allergies/constants/choices.py):

```bash
# Create empty migration
uv run python manage.py makemigrations --empty allergies --name seed_allergens

# Edit migration file to add RunPython operation
# See Django docs: https://docs.djangoproject.com/en/5.2/topics/migrations/#data-migrations
```

```python
# Example data migration for seeding Allergens
def seed_allergens(apps, schema_editor):
    Allergen = apps.get_model('allergies', 'Allergen')
    from allergies.constants.choices import ALLERGEN_CHOICES

    for category, allergen_list in ALLERGEN_CHOICES:
        for key, label in allergen_list:
            Allergen.objects.get_or_create(
                category=category,
                allergen_key=key,
                defaults={'is_active': True}
            )

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(seed_allergens),
    ]
```

### Migration Conflicts (Team Environments)

If `makemigrations` detects conflicts:
1. Pull latest from `main` branch
2. Resolve conflicts in migration files manually
3. Test with `uv run python manage.py migrate`
4. Commit resolved migration

### Reminder Pattern

When suggesting model changes, always remind:
> "After making these changes, run `uv run python manage.py makemigrations` and `uv run python manage.py migrate` to update your local database."

## Admin Customization Patterns

**Reference Implementations:** See [allergies/admin.py](allergies/admin.py) and [users/admin.py](users/admin.py) for established patterns.

### Best Practices

1. **list_display Optimization:** Use `select_related()` for foreign keys to avoid N+1 queries:
   ```python
   class UserAllergyAdmin(admin.ModelAdmin):
       list_display = ['user', 'allergen', 'severity_level', 'is_active']
       list_select_related = ['user', 'allergen']  # Optimize queries
   ```

2. **Fieldsets for Organization:** Group related fields (see [allergies/admin.py](allergies/admin.py#L10-L38) for example).

3. **Read-Only Audit Fields:** Mark `created_at`, `updated_at` as read-only for data integrity.

4. **Custom Admin Actions:** For bulk operations (e.g., bulk deactivate allergens):
   ```python
   @admin.action(description="Deactivate selected allergens")
   def deactivate_allergens(modeladmin, request, queryset):
       logger.info(f"Admin {request.user.id} deactivating {queryset.count()} allergens")
       queryset.update(is_active=False)
   ```

5. **Logging Admin Actions:** Add logging to track CRUD operations for GDPR compliance (see Development Gate 2).

## 🧪 Testing & Fixture Reference

### Coverage Requirements by Phase

**Phase 1 (Current):** 50% minimum — Focus on model and admin tests
**Phase 2 (Q2 2026):** 70% minimum — Add comprehensive view and form tests
**Phase 3 (Q3 2026):** 90% minimum — Full integration test suite

**AI Agent Guideline:** Write tests targeting the **next phase threshold** when implementing new features.

### Coverage Targets by Module Type

- **Models:** 80% minimum (test all custom methods, properties, validation logic)
- **Views:** 70% minimum (test GET, POST, error cases, authentication)
- **Forms:** 80% minimum (test validation, clean methods, error messages)
- **Integration Tests:** Mark with `@pytest.mark.integration` for end-to-end workflows

### Fixture Reference ([conftest.py](conftest.py))

**✅ Recommended Fixtures (Use These):**

| Fixture | Creates | Use Case | Example |
|---------|---------|----------|----------|
| `test_user` | CustomUser | Standard authenticated user | `def test_view(test_user): ...` |
| `user_email` | String | Email for test users | `def test_signup(user_email): ...` |
| `user_password` | String | Password for test users | Auto-dependency of `test_user` |
| `authenticated_client` | Client (logged in) | Testing auth-required views | `def test_list(authenticated_client): ...` |
| `contact_allergen` | Allergen (SLS) | Contact/topical allergen | `def test_allergy(contact_allergen): ...` |
| `food_allergen` | Allergen (Peanut) | Food allergen | `def test_food(food_allergen): ...` |
| `user_allergy` | UserAllergy | Linked user→allergen | `def test_relationship(user_allergy): ...` |

**⚠️ DEPRECATED Fixtures (Backward Compatibility Only — Do Not Use in New Tests):**

| Old Fixture | Replacement | Status |
|-------------|-------------|--------|
| `custom_user` | `test_user` | ⚠️ Use `test_user` in new tests |
| `allergen_contact` | `contact_allergen` | ⚠️ Use `contact_allergen` in new tests |
| `allergen_food` | `food_allergen` | ⚠️ Use `food_allergen` in new tests |

### Fixture Usage Examples

#### Example 1: Testing Model String Representation

```python
import pytest
from allergies.models import Allergen

@pytest.mark.django_db
class TestAllergenModel:
    def test_allergen_str_representation(self, contact_allergen, food_allergen):
        """Test __str__ method returns expected format."""
        assert (
            str(contact_allergen)
            == "Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
        )
        assert str(food_allergen) == "Food Allergens: Peanut"
```

#### Example 2: Testing Authenticated View Access

```python
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestAllergiesListView:
    def test_authenticated_access_succeeds(self, authenticated_client):
        """Authenticated users should access page successfully."""
        response = authenticated_client.get(reverse("allergies:list"))

        assert response.status_code == 200
        assert "allergies/allergies_list.html" in [
            t.name for t in response.templates
        ]

    def test_unauthenticated_access_redirects(self, client):
        """Unauthenticated users should redirect to login."""
        response = client.get(reverse("allergies:list"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url
```

#### Example 3: Testing Admin Actions with Logging

```python
import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from allergies.admin import AllergenAdmin
from allergies.models import Allergen
from users.models import CustomUser

@pytest.mark.django_db
class TestAllergenAdmin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.admin = AllergenAdmin(Allergen, self.site)
        self.superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="admin123"
        )

    def test_deactivate_allergens_success(self, caplog, contact_allergen, food_allergen):
        """Test successful bulk deactivation with logging."""
        # Create mock request
        request = self.factory.get("/")
        request.user = self.superuser

        # Add session support for messages
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        # Get queryset and run action
        queryset = Allergen.objects.filter(
            id__in=[contact_allergen.id, food_allergen.id]
        )

        with caplog.at_level("INFO", logger="allergies.admin"):
            self.admin.deactivate_allergens(request, queryset)

        # Verify allergens were deactivated
        contact_allergen.refresh_from_db()
        food_allergen.refresh_from_db()
        assert not contact_allergen.is_active
        assert not food_allergen.is_active

        # Verify logging
        assert "deactivating 2 allergens" in caplog.text.lower()
```

### Running Tests (See [Common Commands](#-common-commands))

```bash
# Run all tests with coverage
uv run pytest --cov --cov-report=term-missing

# Run specific test file
uv run pytest allergies/tests/test_models.py -v

# Run tests matching pattern
uv run pytest -k test_allergen

# Generate HTML coverage report
uv run pytest --cov --cov-report=html  # Open htmlcov/index.html
```

### Test File Organization

```
allergies/tests/
├── __init__.py
├── test_models.py              # Model tests (Allergen, UserAllergy)
├── test_views.py               # View tests (allergies_list)
├── test_admin_error_handling.py  # Admin action error scenarios
└── test_exceptions.py          # Custom exception tests

users/
└── tests.py                    # ✅ 382 lines of comprehensive user tests
```

### Known Test Gaps

- 🚧 [allergies/tests/test_models.py](allergies/tests/test_models.py#L59) has incomplete `UserAllergy` tests (TODO comment for severity_level, is_confirmed, user_reaction_details fields)
- ❌ No form tests (no forms implemented yet — blocked on Gate 4)
- ❌ No integration tests for product safety workflow (future enhancement)

## 🗄️ Database State & Migration Strategy

### Current Database State

- **Development Database:** [db.sqlite3](db.sqlite3) exists and contains development data
- **CI/CD Database:** Fresh SQLite instance created for each test run
- **Schema Tracking:** Migrations in `allergies/migrations/` and `users/migrations/`

### Fresh Database Setup

When starting fresh or after major schema changes:

```bash
# 1. Remove existing database (⚠️ DESTRUCTIVE - backs up first)
cp db.sqlite3 db.sqlite3.backup
rm db.sqlite3

# 2. Apply all migrations
uv run python manage.py migrate

# 3. Create superuser for admin access
uv run python manage.py createsuperuser

# 4. (Optional) Seed allergen catalog
uv run python manage.py makemigrations --empty allergies --name seed_allergens
# Edit migration file, then:
uv run python manage.py migrate
```

### Rollback Strategy

```bash
# Rollback specific app to zero (removes all migrations)
uv run python manage.py migrate allergies zero

# Rollback to specific migration
uv run python manage.py migrate allergies 0001_initial

# Show migration status
uv run python manage.py showmigrations

# Show migration plan (dry-run)
uv run python manage.py migrate --plan
```

### Data Migration Pattern for Allergen Catalog

When seeding the predefined `Allergen` catalog from [allergies/constants/choices.py](allergies/constants/choices.py):

```python
# Example data migration (allergies/migrations/000X_seed_allergens.py)
from django.db import migrations

def seed_allergens(apps, schema_editor):
    Allergen = apps.get_model('allergies', 'Allergen')
    from allergies.constants.choices import ALLERGEN_CHOICES

    for category, allergen_list in ALLERGEN_CHOICES:
        for key, label in allergen_list:
            Allergen.objects.get_or_create(
                category=category,
                allergen_key=key,
                defaults={'is_active': True}
            )

def reverse_seed(apps, schema_editor):
    """Rollback: remove seeded allergens."""
    Allergen = apps.get_model('allergies', 'Allergen')
    Allergen.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('allergies', '0002_initial'),  # Adjust to latest migration
    ]

    operations = [
        migrations.RunPython(seed_allergens, reverse_seed),
    ]
```

### Migration Reminder Pattern

When suggesting model changes, always remind:
> "After making these changes, run `uv run python manage.py makemigrations` and `uv run python manage.py migrate` to update your local database."

### Handling Migration Conflicts (Team Environments)

If `makemigrations` detects conflicts:
1. Pull latest from `main` branch: `git pull origin main`
2. Check for conflicting migrations: `uv run python manage.py showmigrations`
3. Resolve conflicts manually or use `--merge`: `uv run python manage.py makemigrations --merge`
4. Test migration: `uv run python manage.py migrate`
5. Commit resolved migration: `git add . && git commit -m "Merge migrations"`

## Current Patterns vs. Future Features (Moved Earlier)

### ✅ Current Patterns (Implemented & Recommended)

Use these patterns in current development:

- **Synchronous Views:** All views are standard `def` functions (see [skincare_project/views.py](skincare_project/views.py), [allergies/views.py](allergies/views.py)).
- **Traditional Templates:** Use `{% extends 'layout.html' %}` and `{% include %}` for template composition (see [templates/layout.html](templates/layout.html)).
- **SQLite Development Database:** Default `db.sqlite3` for local development (see [Database Management](#database-management)).
- **Type Hints:** Use Python 3.13 `type` statement for aliases, modern syntax `list[T]`, `dict[K,V]` (see [allergies/models.py](allergies/models.py)).
- **Ruff + Mypy:** Linting and type checking enforced in pre-commit (see [.pre-commit-config.yaml](.pre-commit-config.yaml)).
- **uv Package Manager:** All commands via `uv run` (see [Dependency & Environment Management](#dependency--environment-management-uv)).

### 🚧 Future Django 6.0 Features (Aspirational, Not Yet Implemented)

Mark these as "Future" when suggesting to users:

- **Async Views:** Django 6.0 supports `async def` views for I/O-bound operations. **Not currently used** in this project. Consider for future external API integration (product ingredient scanning):
  ```python
  # Future pattern (not implemented)
  async def product_check(request: HttpRequest):
      ingredient_data = await fetch_product_api(barcode)  # External API call
      matches = await check_allergens_async(ingredient_data, request.user)
      return JsonResponse({'matches': matches})
  ```

- **Template Partials (`{% partialdef %}`):** Django 6.0 adds `{% partialdef %}` and `{% partial %}` for HTMX-friendly components. **Not currently used**. Consider when implementing dynamic UI updates:
  ```html
  <!-- Future pattern (not implemented) -->
  {% partialdef allergen-row allergen=allergen %}
      <tr id="allergen-{{ allergen.id }}">
          <td>{{ allergen.allergen_label }}</td>
          <td>{{ allergen.category }}</td>
      </tr>
  {% endpartialdef %}
  ```

- **Background Tasks (`django.tasks`):** Django 6.0 includes native background task framework. **Not currently implemented**. Consider for future email notifications or data cleanup:
  ```python
  # Future pattern (not implemented)
  from django.tasks import task

  @task
  def send_allergy_alert_email(user_id, allergen_id):
      # Async email sending
      pass

  # Usage: send_allergy_alert_email.enqueue(user.id, allergen.id)
  ```

- **Django 6.0 Form Field Groups:** New form rendering API for grouped fields. **Not currently used** (no forms implemented yet).

### Implementation Guidance

When users ask about these features:
1. **Acknowledge** the Django 6.0 capability exists.
2. **Clarify** it's not currently implemented in this project.
3. **Recommend** synchronous/traditional patterns for consistency.
4. **Document** as "Future Enhancement" if it aligns with project roadmap (e.g., async for external APIs).

Example response:
> "Django 6.0 supports `{% partialdef %}` for HTMX integration, but this project currently uses traditional `{% include %}` tags (see [templates/layout.html](templates/layout.html)). For consistency, continue using `{% include %}` unless we plan to refactor for HTMX support."

## 3. Django 6.0 Conventions (Historical - See "Current Patterns vs. Future Features" Above)
- **Background Tasks:** Prefer the native `django.tasks` framework over Celery for lightweight operations like email or data cleanup.
- **Template Partials:** Use `{% partialdef %}` and `{% partial %}` tags within templates to handle modular components (HTMX-friendly) instead of excessive `{% include %}` calls.
- **Type Safety:** Use `TypeAlias` for complex types and explicitly hint all QuerySets as `QuerySet[ModelName]` or `Manager[ModelName]` to satisfy `django-stubs`.

## Coding Standards (Ruff & Mypy)
- **Linting:** Follow **Ruff** conventions (target: py313). Use `_` for intentionally unused variables in tuple unpacking (e.g., `for key, _, list in choices:`).
- **Validation:** Run `uv run mypy .` before proposing logic changes
- **Mypy:** If a ManyToManyField assignment throws an "Incompatible types" error (common in `AbstractUser` overrides), use `# type: ignore[assignment]`.
- **Async Views:** ⚠️ NOT CURRENTLY USED. Stick to synchronous `def` views for consistency.

## CI/CD Workflow
**CI Awareness:** The CI enforces `.python-version` and `uv lock --check`. Always ensure the lockfile is synced before suggesting a commit.
- **Testing:** Use `pytest` for all new features. Place tests in `app/tests/` and run via `uv run pytest`.
- **Gate 1 (Lint):** Pre-commit (Ruff + Mypy) must pass.
- **Gate 2 (Test):** Pytest suite must pass.
- **Gate 3 (Coverage):** Codecov enforces a minimum threshold based on the project phase (currently 50%).
- **Instruction:** If CI fails on 'Static Analysis', prioritize fixing Ruff/Mypy errors before modifying logic.



## Extension Points
- Product safety check: implement POST handling in [skincare_project/views.py](skincare_project/views.py) `product` view.
  - Parse user-provided ingredient list.
  - Compare against active `UserAllergy` for `request.user` (join via `select_related('allergen')`).
  - Return matches (include severity_level, source_info, user_reaction_details).
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

## Python 3.13 + Django 6.0 Technical Notes
- **Type Aliases:** Use the `type` statement for complex type aliases (e.g., `type AllergenDict = dict[str, str | int]`).
- **Performance:** Django 6.0 includes ORM optimizations; benchmark queries with `.explain()` when needed.
- **Async Views:** ⚠️ Django 6.0 supports async but NOT CURRENTLY USED in this project. Stick to synchronous views.
- **Compatibility:** All dependencies are compatible with Python 3.13 and Django 6.0.

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

## AI Agent Behavior & Quality Standards

### Autonomous Bug Fixing
When given bug reports, CI failures, or error logs:
1. **Read & Diagnose Independently:** Parse error logs, stack traces, and failing test output without requesting clarification
2. **Identify Root Cause:** Trace the error to its source (model validation, query issue, missing dependency, etc.)
3. **Follow Development Gates:** Implement fix respecting Gate 1 → 5 order (dependencies → logging → error handling → forms → tests)
4. **Verify Fix Works:** Run `uv run pytest` for affected modules, check coverage with `pytest --cov`
5. **Document Non-Obvious Fixes:** Add inline comments explaining why the fix was needed

**Examples of Autonomous Workflows:**
- CI test failure → Read pytest output → Identify missing fixture → Add to `conftest.py` → Verify tests pass
- Mypy type error → Check `pyproject.toml` type config → Add type hints → Run `mypy .` → Confirm passes
- Security scan failure (bandit) → Review flagged code → Apply secure alternative → Re-run `bandit -r .`

**When to Stop & Request Guidance:**
- Same CI job fails 3+ times after attempted fixes
- User requirements are ambiguous or contradictory
- Architectural assumptions prove fundamentally wrong (e.g., model relationships need redesign)

### Verification Before Marking Complete
Never mark a task complete without proving correctness:
- **Tests:** Run `uv run pytest` for affected apps (e.g., `pytest allergies/tests/ -v`)
- **Coverage:** Check impact with `pytest --cov --cov-report=term-missing`
- **Linting:** Confirm `ruff check . --fix` and `ruff format .` pass
- **Type Safety:** Run `mypy .` for type correctness
- **Security:** If models/views changed, run `bandit -r . -ll` (high/medium severity)
- **Staff Engineer Bar:** Ask "Would a senior engineer approve this PR?"

### Core Development Principles
These principles override convenience:

1. **Simplicity First**
   - Minimal code changes for maximum impact
   - Touch only files necessary to fix the issue
   - Avoid refactoring unrelated code in the same commit
   - Example: If fixing a view bug, don't rewrite the entire view unless necessary

2. **Root Cause Analysis (No Laziness)**
   - Never propose temporary fixes or workarounds
   - Trace issues to their source (don't mask symptoms)
   - Example: If `UserAllergy` validation fails, fix the model constraint, don't add view-level checks
   - Example: If imports fail, add to dependencies, don't suggest "try installing manually"

3. **Minimal Blast Radius**
   - Changes should not introduce regressions
   - Use `.select_related()` when adding queries to avoid N+1 issues
   - Test adjacent functionality if uncertain about impact
   - Example: Changing `Allergen.allergen_key` validation → test all `UserAllergy` creation flows

4. **Senior Engineer Standards**
   - Write code you'd accept in code review
   - Include docstrings for non-obvious functions
   - Follow Django best practices (CBVs where appropriate, proper form usage)
   - Don't check in debug statements, commented code, or print() calls

### Error Context for AI Agents
When encountering errors, AI agents should reference:
- **Dependency Issues:** Check `pyproject.toml` dependency groups (test, lint, type-check, security)
- **Import Errors:** Verify `uv sync` has been run and `.python-version` matches (Python 3.13)
- **Model Errors:** Review `allergies/models.py` and `users/models.py` for constraints
- **Validation Errors:** Check `CATEGORY_CHOICES` in `allergies/constants/choices.py`
- **Test Failures:** Check `pytest.ini` for markers (unit, integration, slow)
- **Type Errors:** Review `[tool.mypy]` and `[tool.django-stubs]` in `pyproject.toml`

### Development Gate Enforcement
AI agents must respect the strict gate order:

**Gate 1: Dependencies** → Install before writing code
```bash
uv add django-environ  # Required for environment variables
uv add --group test pytest-django  # Test dependencies
```

**Gate 2: Logging Infrastructure** → Add before business logic
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"User {user.id} created allergy")  # Security events
logger.error(f"Validation failed: {e}", exc_info=True)  # Errors
```

**Gate 3: Error Handling** → Implement before features
```python
from django.db import transaction

@transaction.atomic
def view_function(request):
    try:
        # Business logic
        obj.full_clean()  # Validate before save
        obj.save()
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        return render(request, 'form.html', {'error': e.message})
```

**Gate 4: Forms & Validation** → After error handling exists
```python
# allergies/forms.py
from django import forms
class UserAllergyForm(forms.ModelForm):
    class Meta:
        model = UserAllergy
        fields = ['allergen', 'severity_level', 'is_confirmed', 'source_info']
```

**Gate 5: Tests** → Complete before marking feature done
```python
# allergies/tests/test_views.py
def test_create_allergy_success(authenticated_client, contact_allergen):
    response = authenticated_client.post('/allergies/create/', {
        'allergen': contact_allergen.id,
        'severity_level': 'moderate'
    })
    assert response.status_code == 302
    assert UserAllergy.objects.filter(allergen=contact_allergen).exists()
```

**Violation Consequences:**
- ❌ Proposing a new view without logging → Reject, add Gate 2 first
- ❌ Suggesting a feature without error handling → Reject, add Gate 3 first
- ❌ Implementing a form without tests → Reject, add Gate 5 before marking done

---

**Note for AI Agents:** This section codifies expected behavior for autonomous operation. When in doubt, prioritize code quality over speed. A working, well-tested feature implemented tomorrow is better than a broken feature shipped today.
