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

### Current Implementation Gaps (Must Address Before New Features)

- ❌ **Logging Infrastructure:** Zero logging statements exist in codebase. All views, models with business logic, and admin files need `logger = logging.getLogger(__name__)` at module level.
- ❌ **Error Handling:** No try-except blocks in views ([skincare_project/views.py](skincare_project/views.py), [allergies/views.py](allergies/views.py)). Only model-level validation exists in [allergies/models.py](allergies/models.py#L74-L82).
- ❌ **Forms Implementation:** No `forms.py` files exist. Need `UserAllergyForm` with dynamic `allergen_key` filtering based on category selection.
- ❌ **View Tests:** [users/tests.py](users/tests.py) is completely empty. No view tests exist for [allergies/views.py](allergies/views.py) or [skincare_project/views.py](skincare_project/views.py).
- 🚧 **Model Tests Incomplete:** [allergies/tests/test_models.py](allergies/tests/test_models.py#L59) has TODO comment for `UserAllergy` model tests (severity, confirmation, notes fields).
- 🚧 **django-environ Dependency:** Used in [skincare_project/settings.py](skincare_project/settings.py) but not in `pyproject.toml` dependencies. Run `uv add django-environ` to fix.
- 🚧 **Admin Logging:** [allergies/admin.py](allergies/admin.py) and [users/admin.py](users/admin.py) have no logging for CRUD operations (GDPR compliance gap).

### Blocked Features (Cannot Implement Until Foundations Complete)

- 🚫 **Product Safety Check POST Handler:** Cannot implement until logging + error handling exist in [skincare_project/views.py](skincare_project/views.py).
- 🚫 **User Forms & Validation:** Cannot implement until `UserAllergyForm` created with proper error surfacing.
- 🚫 **Users App Routing:** Cannot include [users/urls.py](users/urls.py) until views have logging and error handling.

## Development Gates (Strict Priority Order)

**⚠️ CRITICAL: Do NOT implement new features until these foundations are complete.**

### Gate 1: Dependency Fix (IMMEDIATE)
1. Install `django-environ`: `uv add django-environ`
2. Verify: `uv run python -c "import environ; print('OK')"`
3. Update lockfile: `uv sync`

### Gate 2: Logging Infrastructure (BEFORE ANY NEW FEATURES)
1. Add `logger = logging.getLogger(__name__)` to:
   - [skincare_project/views.py](skincare_project/views.py)
   - [allergies/views.py](allergies/views.py)
   - [allergies/models.py](allergies/models.py) (for validation failures)
   - [allergies/admin.py](allergies/admin.py)
   - [users/admin.py](users/admin.py)
2. Log security events (user actions at INFO level)
3. Configure production logging in [settings.py](skincare_project/settings.py)

### Gate 3: Error Handling (BEFORE IMPLEMENTING FORMS OR POST HANDLERS)
1. Add try-except to all view functions (except minimal template renders with `# minimal-view: no-logger-needed`)
2. Implement `@transaction.atomic` for multi-model operations
3. Create custom exception classes in `allergies/exceptions.py`
4. Surface validation errors properly (no 500 errors on user input)

### Gate 4: Forms & Validation (AFTER LOGGING + ERROR HANDLING)
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
        fields = ['allergen', 'severity', 'confirmation_status', 'source', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter allergen choices to active only
        self.fields['allergen'].queryset = Allergen.objects.filter(is_active=True)

    def clean(self):
        """Custom validation beyond model constraints."""
        cleaned_data = super().clean()
        allergen = cleaned_data.get('allergen')
        severity = cleaned_data.get('severity')

        if severity == 'severe' and not cleaned_data.get('confirmation_status'):
            logger.warning("Severe allergy without confirmation status")
            raise ValidationError("Severe allergies require confirmation status")

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
       list_display = ['user', 'allergen', 'severity', 'is_active']
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

## Testing Requirements

**Current Coverage:** 50% minimum (Phase 1). See [pyproject.toml](pyproject.toml) `[tool.coverage.report]` for configuration.

### Coverage Targets by Module Type

- **Models:** 80% minimum (test all custom methods, properties, validation logic)
- **Views:** 70% minimum (test GET, POST, error cases, authentication)
- **Forms:** 80% minimum (test validation, clean methods, error messages)
- **Integration Tests:** Mark with `@pytest.mark.integration` for end-to-end workflows

### Test Patterns

```python
# allergies/tests/test_views.py (to be created)
import pytest
from django.test import Client
from django.urls import reverse
from allergies.models import Allergen, UserAllergy
from users.models import CustomUser

@pytest.mark.django_db
class TestAllergiesListView:
    def test_allergies_list_authenticated(self):
        """Authenticated users can view allergies list."""
        client = Client()
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        client.login(username='testuser', password='testpass')

        response = client.get(reverse('allergies:list'))
        assert response.status_code == 200
        assert 'allergies/allergies_list.html' in [t.name for t in response.templates]

    def test_allergies_list_filters_active_only(self):
        """List view shows only active allergens."""
        # Test implementation
        pass
```

### Running Tests

```bash
# Run all tests with coverage
uv run pytest --cov=allergies --cov=users --cov-report=term-missing

# Run specific test file
uv run pytest allergies/tests/test_models.py -v

# Run with integration tests
uv run pytest -m integration

# Generate HTML coverage report
uv run pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

### Known Test Gaps

- ❌ [users/tests.py](users/tests.py) is completely empty
- 🚧 [allergies/tests/test_models.py](allergies/tests/test_models.py#L59) has incomplete `UserAllergy` tests (TODO comment)
- ❌ No view tests exist for any app
- ❌ No form tests (no forms implemented yet)
- ❌ No integration tests for product safety workflow

## 3. Current Patterns vs. Future Features

### ✅ Current Patterns (Implemented & Recommended)

Use these patterns in current development:

- **Synchronous Views:** All views are standard `def` functions (see [skincare_project/views.py](skincare_project/views.py), [allergies/views.py](allergies/views.py)).
- **Traditional Templates:** Use `{% extends 'layout.html' %}` and `{% include %}` for template composition (see [templates/layout.html](templates/layout.html)).
- **SQLite Development Database:** Default `db.sqlite3` for local development (see [Database Management](#database-management)).
- **Type Hints:** Use Python 3.14 `type` statement for aliases, modern syntax `list[T]`, `dict[K,V]` (see [allergies/models.py](allergies/models.py)).
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
