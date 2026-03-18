## 🔴 HARD PROHIBITIONS — READ FIRST

The following are **banned in all generated code** for the current phase. Violations must include a `# Future Refactor:` comment and must not be submitted without explicit user approval:

| Prohibited Pattern | Why Banned | If Suggested, Must Say |
|---|---|---|
| `async def` view functions | Not used — all views are synchronous `def` | `# Future Refactor: async views not yet adopted in this project` |
| `{% partialdef %}` / `{% partial %}` tags | Template partials not yet adopted | `# Future Refactor: template partials not yet adopted in this project` |
| `django.tasks` / `@task` decorator | Background tasks not yet adopted | `# Future Refactor: background tasks not yet adopted in this project` |
| `python -m pip install` / bare `pip install` | Always use `uv add` | N/A — never suggest pip directly |
| python 3.13-only features (T-strings, etc.) | Project targets Python 3.13 | N/A — not compatible |

---

# Copilot Instructions: Skincare Allergy Filter

Purpose: Make AI coding agents productive immediately in this Django repo by documenting the real architecture, workflows, and project-specific conventions.

## Big Picture
- Framework: Django 6.0 + Templates (SQLite in dev).
- Language: Python 3.13 (Leverage modern type hints with `type` aliases)
- Environment & PDM: Standardize on `uv`. Always use `uv run` for executing management commands or scripts.
- Project: `skincare_project/` with apps: `allergies/`, `users/`.
- Auth: Custom user `users.CustomUser` (configured via `AUTH_USER_MODEL`).
- Domain: Predefined `Allergen` catalog; `UserAllergy` links a user to an `Allergen` with extra fields (severity_level, is_confirmed, source_info, JSON reaction details).
- Planned: AllergenAlias (or equivalent) — a many-to-one table mapping alternate ingredient names (INCI names, common names, abbreviations) to a canonical Allergen.allergen_key. All matching logic should be designed to accommodate this lookup stage between tokenization and comparison.

## 🚀 Quick Start for AI Agents

### Current Project Status

**✅ Completed Development Gates:**
- **Gate 1 (Dependencies):** `django-environ` installed and configured

**🚧 In Progress:**
- **Gate 2 (Logging):** Partial — logger exists in `allergies/admin.py`;
  `allergies/views.py` and `skincare_project/views.py` logging incomplete
- **Gate 3 (Error Handling):** Partial — try-except and `@transaction.atomic`
  patterns documented; not fully implemented across all views;
  `allergies/exceptions.py` existence unverified

**❌ Not Started (Blocked Until Gates 2–3 Complete):**
- **Gate 4 (Forms):** No `forms.py` files exist yet
- **Gate 5 (Tests):** `allergies/tests/test_models.py` has TODO at L59;
  view and form tests do not exist

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
- ✅ `source_info` (CharField with choices: `self_reported`, `medical_professional`,`allergy_test`, `family_history`) — NOT "source"
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
- **Expected JSONField Schemas (use only these keys — do not invent new ones):**
  - `user_reaction_details` → `{"symptom": str, "severity": str, "date": str}` (type alias: `ReactionDetails` in [allergies/models.py](allergies/models.py))
  - `admin_notes` → `{"verified_by": str, "verification_date": str}` (type alias: `AdminNotes` in [allergies/models.py](allergies/models.py))
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
- **Lockfile Commits:** After `uv add`, always commit both `pyproject.toml` and `uv.lock` together. The CI enforces `uv lock --check` — a stale lockfile will fail the build.
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

### Completed Foundations
- ✅ **django-environ Dependency:** Installed and configured in [skincare_project/settings.py](skincare_project/settings.py).

### Current Implementation Gaps (Prioritized)

- 🚧 **choices.py Incomplete:** Allergen lists have placeholder stubs
  (`# ... and so on`). Must be completed with full INCI-grounded ingredient
  catalog before forms or seeding migration can be implemented.
- 🚧 **Models Incomplete:** `allergies/models.py` — verify JSONField key
  validation in `clean()` is present. `users/models.py` — full field set
  and validation status unknown.
- 🚧 **Logging Incomplete:** `logger = logging.getLogger(__name__)` needed
  in `allergies/views.py`, `skincare_project/views.py`, and any new views.
  Status of `allergies/admin.py` logging unverified from source.
- 🚧 **Error Handling Incomplete:** `@transaction.atomic` and try-except
  blocks needed in all view functions. `allergies/exceptions.py` — existence
  and contents unverified.
- 🚧 **Test Coverage Incomplete:** `users/tests.py` (382 lines) — coverage
  scope unknown. `allergies/tests/test_models.py` has confirmed TODO at L59
  for `UserAllergy` fields. View tests and admin error handling tests —
  existence unverified.
- ❌ **Forms:** No `forms.py` files exist. Blocked until Gates 2–3 complete.
```

Remove the now-redundant separate "Completed Foundations" subsection above it, since it only listed `django-environ` which is already in Gate 1.

---

### 3. Fix the "Development Gates" status block (lines 391–413)

This is the most critical fix — it's what an AI agent reads to decide where to start. Replace:
```
**Current Status:** Gates 1-3 ✅ COMPLETE. Focus on Gates 4-5.

### Gate 1: Dependency Fix — ✅ COMPLETE
...

### Gate 2: Logging Infrastructure — ✅ COMPLETE
1. ✅ logger added to allergies/admin.py
2. ✅ logger added to allergies/views.py
   - Admin custom actions with INFO/ERROR logging
3. ✅ Security events logged
4. ✅ Production logging configured in settings.py

### Gate 3: Error Handling — ✅ COMPLETE
1. ✅ Try-except blocks in view functions
2. ✅ @transaction.atomic implemented
3. ✅ Custom exception classes in allergies/exceptions.py
4. ✅ Validation errors properly surfaced

### Gate 4: Forms & Validation — ⏳ NOT STARTED (UNBLOCKED)
```

With:
```
**Current Status:** Gate 1 ✅ COMPLETE. Gates 2–3 🚧 IN PROGRESS.
Gates 4–5 ❌ BLOCKED until Gates 2–3 complete.

### Gate 1: Dependency Fix — ✅ COMPLETE
1. ✅ `django-environ` installed and configured in `pyproject.toml`
2. ✅ Verified working in `skincare_project/settings.py`
3. ✅ Lockfile synced

### Gate 2: Logging Infrastructure — 🚧 IN PROGRESS
1. 🚧 `logger = logging.getLogger(__name__)` — status per file:
   - `allergies/admin.py` — believed present, verify from source
   - `allergies/views.py` — INCOMPLETE
   - `skincare_project/views.py` — INCOMPLETE
   - Any new view files — NOT STARTED
2. ❌ Security events (INFO level) not consistently logged across views
3. ❌ Production logging config in `settings.py` — status unverified

**Gate 2 is complete when:** every view function and admin action file
has a module-level logger and logs CREATE/UPDATE/DELETE events at INFO,
errors at ERROR with exc_info=True.

### Gate 3: Error Handling — 🚧 IN PROGRESS
1. ❌ Try-except blocks missing from view functions in
   `allergies/views.py` and `skincare_project/views.py`
2. ❌ `@transaction.atomic` not confirmed on multi-model operations
3. ❌ `allergies/exceptions.py` — existence and contents unverified;
   `AllergenNotFoundError` and `InvalidIngredientError` may not exist
4. ❌ Validation errors surfaced without 500s — not verified

**Gate 3 is complete when:** all view functions have try-except with
user-friendly error rendering, `@transaction.atomic` on writes, and
`allergies/exceptions.py` exists with domain exception classes.

### Gate 4: Forms & Validation — ❌ BLOCKED (Gates 2–3 incomplete)

### Blocked Features (Cannot Implement Until Foundations Complete)

- 🚫 **Product Safety Check POST Handler:** Cannot implement until logging + error handling exist in [skincare_project/views.py](skincare_project/views.py).
- 🚫 **User Forms & Validation:** Cannot implement until `UserAllergyForm` created with proper error surfacing.
- 🚫 **Users App Routing:** Cannot include [users/urls.py](users/urls.py) until views have logging and error handling.

### Planned Future Features (Post-Gates)

- Synonym Mapper / AllergenAlias: Many-to-one alias table mapping all known surface forms of an ingredient to a canonical allergen_key. Required before the product safety check can be considered production-accurate. Not yet designed — no model, migration, or service layer exists.

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
5. Ensure coverage meets 75% minimum (current threshold)

**After Gates 1-3 Complete:** Can implement product safety check POST handler and user management features.

## ⚠️ Gate Verification Protocol

Before marking any gate ✅ COMPLETE in this document, an AI agent or
contributor must:

1. Open the actual source file (not rely on this document's claims)
2. Confirm the specific lines exist — e.g., `grep -n "getLogger" allergies/views.py`
3. Run `uv run pytest` and confirm no related tests fail
4. Only then update the checkbox in this document

**Do not mark a gate complete based on documentation alone.**

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

### Coverage Requirements by Gate

**Gates 1–3 (Dependency, Logging, Error Handling):** 75% overall minimum — Focus on model and admin tests; 75% minimum for all new code
**Gate 4 (Forms & Validation):** 75% overall minimum — Add comprehensive view and form tests
**Gate 5 (Complete Tests):** 80% overall minimum — Full integration test suite

**AI Agent Guideline:** Write tests targeting the **next gate's threshold** when implementing new features.

### Coverage Targets by Module Type

- **Models:** 75% minimum (test all custom methods, properties, validation logic)
- **Views:** 75% minimum (test GET, POST, error cases, authentication)
- **Forms:** 75% minimum (test validation, clean methods, error messages)
- **Integration Tests:** Mark with `@pytest.mark.integration` for any test spanning multiple apps (e.g., `users` + `allergies`) or testing end-to-end workflows. `--strict-markers` is enforced in [pyproject.toml](pyproject.toml) — only use registered markers (`integration`, `slow`, `unit`).

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
- **Gate 3 (Coverage):** Codecov enforces a minimum threshold based on the project phase (currently 75%).
- **Instruction:** If CI fails on 'Static Analysis', prioritize fixing Ruff/Mypy errors before modifying logic.



## Extension Points
- Product safety check: implement POST handling in [skincare_project/views.py](skincare_project/views.py) `product` view.
  - Parse and tokenize the ingredient list.
  - Normalize tokens (lowercase, strip whitespace).
  - Resolve aliases via AllergenAlias lookup (planned — design the view's service layer to accept this as an injectable step).
  - Compare resolved keys against active UserAllergy for request.user.
  - Return matches with severity_level, source_info, user_reaction_details.
- Users app routing: include [users/urls.py](users/urls.py) in project URLs; link from layout using `{% url 'user:list' %}`.

## Practical Snippets
- Active allergens ordered:
  - `from allergies.models import Allergen`
  - `Allergen.objects.filter(is_active=True).order_by('category', 'allergen_key')`
- Current user allergies with labels:
  - `from allergies.models import UserAllergy`
  - `qs = UserAllergy.objects.select_related('allergen').filter(user=request.user, is_active=True)`
<!--
Phase 1: exact allergen_key match only.
Phase 2 (Synonym Mapper): resolve ingredient tokens to canonical allergen_keys
via AllergenAlias before this filter — do not extend this snippet until that
model exists.
 -->
  - `for ua in qs: label = ua.allergen.allergen_label`

## Gotchas
- `allergen_key` choices are category-dependent; leave `choices=[]` in the model and filter in forms.
- Ensure `UserAllergy.clean()` runs: save path uses `full_clean()` override; do not bypass `save()`.
- Static files are served from [static/](static) with `STATICFILES_DIRS` configured in settings.
- **Migration naming:** Always pass `--name` to `makemigrations` — e.g., `uv run python manage.py makemigrations allergies --name add_severity_to_userallergy`. Auto-generated names matching `0004_auto_<timestamp>` are **rejected at commit time** by the `enforce-migration-naming` pre-commit hook in [.pre-commit-config.yaml](.pre-commit-config.yaml).
- **JSONField key discipline:** Only use the canonical keys defined in the model `help_text` and type aliases (`ReactionDetails`, `AdminNotes` in [allergies/models.py](allergies/models.py)). Inventing new keys (e.g., `"reaction_type"`, `"onset"`) will silently corrupt existing data.

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
   - Changes should not introduce regre## 🔴 HARD PROHIBITIONS — READ FIRST

   The following are **banned in all generated code** for the current phase. Violations must include a `# Future Refactor:` comment and must not be submitted without explicit user approval:

   | Prohibited Pattern | Why Banned | If Suggested, Must Say |
   |---|---|---|
   | `async def` view functions | Not used — all views are synchronous `def` | `# Future Refactor: async views not yet adopted in this project` |
   | `{% partialdef %}` / `{% partial %}` tags | Template partials not yet adopted | `# Future Refactor: template partials not yet adopted in this project` |
   | `django.tasks` / `@task` decorator | Background tasks not yet adopted | `# Future Refactor: background tasks not yet adopted in this project` |
   | `python -m pip install` / bare `pip install` | Always use `uv add` | N/A — never suggest pip directly |
   | Python 3.14-only features (T-strings, etc.) | Project targets Python 3.13 | N/A — not compatible |

   ---

   # Copilot Instructions: Skincare Allergy Filter

   Purpose: Make AI coding agents productive immediately in this Django repo by
   documenting the real architecture, workflows, and project-specific conventions.

   ## 🚀 Quick Start for AI Agents

   **Before writing any code, read [`STATUS.md`](STATUS.md) at the project root.**

   `STATUS.md` is the authoritative source for:
   - Which development gates are complete, in progress, or blocked
   - The specific tasks currently active
   - Known gaps in existing files

   `copilot-instructions.md` (this file) documents stable conventions and
   architecture. It does not change unless the architecture changes.
   `STATUS.md` changes after every work session.

   ### Key Files Reference

   | File | Purpose | Key Contents |
   |------|---------|-------------|
   | [`STATUS.md`](STATUS.md) | Current gate status & active work | Updated after every session |
   | [`allergies/models.py`](allergies/models.py) | Core data models | `Allergen`, `UserAllergy` with `clean()` validation |
   | [`conftest.py`](conftest.py) | Test fixtures | `test_user`, `authenticated_client`, `contact_allergen`, `user_allergy` |
   | [`pyproject.toml`](pyproject.toml) | Project config | Dependencies, Ruff (py313), Mypy, coverage settings |
   | [`allergies/constants/choices.py`](allergies/constants/choices.py) | Allergen catalog | `CATEGORY_CHOICES`, `FORM_ALLERGIES_CHOICES`, `FLAT_ALLERGEN_LABEL_MAP` |
   | [`allergies/admin.py`](allergies/admin.py) | Admin interface | Custom actions, fieldsets |

   ### Critical Field Names (Use These Exactly)

   **UserAllergy Model Fields:**
   - ✅ `severity_level` (CharField: `mild`, `moderate`, `severe`, `life_threatening`) — NOT "severity"
   - ✅ `is_confirmed` (BooleanField) — NOT "confirmation" or "confirmation_status"
   - ✅ `source_info` (CharField: `self_reported`, `medical_professional`, `allergy_test`, `family_history`) — NOT "source"
   - ✅ `user_reaction_details` (JSONField — allowed keys: `symptom`, `severity`, `date` only)
   - ✅ `admin_notes` (JSONField — allowed keys: `verified_by`, `verification_date` only)
   - ✅ `symptom_onset_date` (DateField, nullable)

   **Allergen Model Fields:**
   - `category`, `allergen_key`, `is_active`, `created_at`, `updated_at`
   - Unique constraint: `(category, allergen_key)`

   **Related names (use these in queries):**
   - `user.user_allergies` — reverse of `UserAllergy.user` FK
   - `allergen.user_allergy_entries` — reverse of `UserAllergy.allergen` FK

   ### Python Version & Dependencies

   - **Python:** 3.13 (NOT 3.14 — no T-strings or other 3.14-only features)
   - **Django:** 6.0
   - **Package Manager:** `uv` (always use `uv run` commands)
   - **Ruff Target:** py313

   ---

   ## Big Picture

   - Framework: Django 6.0 + Templates (SQLite in dev).
   - Language: Python 3.13 (leverage modern type hints with `type` aliases)
   - Environment & PDM: Standardize on `uv`. Always use `uv run` for management
     commands or scripts.
   - Project: `skincare_project/` with apps: `allergies/`, `users/`.
   - Auth: Custom user `users.CustomUser` (configured via `AUTH_USER_MODEL`).
   - Domain: Predefined `Allergen` catalog; `UserAllergy` links a user to an
     `Allergen` with extra fields (`severity_level`, `is_confirmed`, `source_info`,
     JSON reaction details).
   - Planned: `AllergenAlias` — a many-to-one table mapping alternate ingredient
     names (INCI names, common names, abbreviations) to a canonical
     `Allergen.allergen_key`. All matching logic should be designed to accommodate
     this lookup stage between tokenization and comparison.

   ---

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
   uv run pytest --cov --cov-report=term-missing   # All tests with coverage
   uv run pytest allergies/tests/test_models.py -v  # Specific file
   uv run pytest -k test_allergen                   # Pattern match
   uv run pytest -m "not integration"               # Skip integration tests
   uv run pytest --cov --cov-report=html            # HTML report (open htmlcov/index.html)
   uv run pytest -ra                                # Test summary
   ```

   ### Linting & Formatting

   ```bash
   uv run ruff check .           # Check
   uv run ruff check --fix .     # Check and auto-fix
   uv run ruff format .          # Format
   uv run pre-commit run --all-files
   uv run pre-commit install
   ```

   ### Type Checking

   ```bash
   uv run mypy allergies users skincare_project
   uv run mypy .
   ```

   ### Django Management

   ```bash
   uv run python manage.py makemigrations
   uv run python manage.py migrate
   uv run python manage.py runserver
   uv run python manage.py createsuperuser
   uv run python manage.py shell
   uv run python manage.py showmigrations
   uv run python manage.py migrate allergies zero   # Rollback example
   ```

   ### Security & Code Quality

   ```bash
   uv run bandit -r allergies users skincare_project
   uv run safety scan --non-interactive
   uv run python manage.py check --deploy
   ```

   ---

   ## Architecture & Routing

   - Project URLs: `skincare_project/urls.py`
     - `''` → `views.home` → `templates/home.html`
     - `'product/'` → `views.product` → `templates/product.html`
     - `'allergies/'` → includes `allergies/urls.py` → `allergies_list`
     - Users app exists but is **not yet included** — add `path('users/', include('users.urls'))` once views have logging and error handling
   - Templates: Base layout at `templates/layout.html`; all pages `{% extends 'layout.html' %}` and load static

   ---

   ## Data Model Essentials

   - `Allergen` fields: `category` (from `CATEGORY_CHOICES`), `allergen_key`
     (category-dependent, `choices=[]` in model — filtered in forms), `is_active`.
     Unique constraint: `(category, allergen_key)`.
   - `UserAllergy`: `user` → `users.CustomUser`, `allergen` → `Allergen`
     (+ `severity_level`, `is_confirmed`, `source_info`, JSON fields).
     Unique constraint: `(user, allergen)`.
   - **JSONField schemas — use only these keys, never invent new ones:**
     - `user_reaction_details` → `{"symptom": str, "severity": str, "date": str}`
       (type alias: `ReactionDetails` in `allergies/models.py`)
     - `admin_notes` → `{"verified_by": str, "verification_date": str}`
       (type alias: `AdminNotes` in `allergies/models.py`)
     - `UserAllergy.clean()` enforces these key sets and will raise `ValidationError`
       on unknown keys — do not bypass `save()`.
   - Convenience: `Allergen.allergen_label` maps key → human label via
     `FLAT_ALLERGEN_LABEL_MAP`.

   ---

   ## Conventions

   - **Lint/Format:** Ruff, target py313. Run `ruff check . --fix` and `ruff format .`.
   - **Typing:** Python 3.13 `type` statement for aliases; `list[T]`, `dict[K,V]`
     syntax throughout. All function signatures must have explicit type hints.
     Use `QuerySet[Allergen]` (not bare `QuerySet`) for ORM annotations.
   - **Paths:** `pathlib.Path` over `os.path`.
   - **URLs:** Named routes everywhere (`name='allergies_list'`); `{% url '...' %}`
     in templates.
   - **Queries:** Always `.select_related('allergen')` for `UserAllergy` access;
     filter `is_active=True`.
   - **Mypy:** If a `ManyToManyField` assignment throws "Incompatible types" on
     `AbstractUser` overrides, use `# type: ignore[assignment]`.

   ---

   ## Dependency & Environment Management (`uv`)

   - **Execution:** Never ask the user to "activate venv." Use `uv run <command>`.
   - **Add Packages:** `uv add <package>` for base deps; `uv add --group <name> <package>` for groups (test, lint, type-check, security).
   - **Syncing:** `uv sync` to ensure the environment matches `uv.lock`.
   - **Lockfile Commits:** After `uv add`, always commit both `pyproject.toml` and
     `uv.lock` together. The CI enforces `uv lock --check` — a stale lockfile
     fails the build.
   - **Version Pinning:** Respect `.python-version` and `requires-python = ">=3.13"`.

   ---

   ## Logging Standards

   Add `logger = logging.getLogger(__name__)` at module level in **all views,
   models with business logic, and admin files**.

   ```python
   import logging
   logger = logging.getLogger(__name__)

   # Security events — INFO level
   logger.info(f"User {user.id} created allergy {allergy.id} for allergen {allergen.allergen_key}")

   # Errors — ERROR level with traceback
   logger.error(f"Failed to process ingredient list: {e}", exc_info=True)

   # Performance — DEBUG level (development only)
   logger.debug(f"Query took {elapsed}s: {query}")
   ```

   **GDPR Compliance:** Never log personal data (emails, passwords). Log user IDs only.

   See `LOGGING` in `skincare_project/settings.py` for handler configuration.

   **Gate 2 is complete when:** every view function and admin action file has a
   module-level logger and logs all CREATE/UPDATE/DELETE events at INFO; exceptions
   at ERROR with `exc_info=True`.

   ---

   ## Error Handling & Resilience

   ```python
   from django.db import transaction
   from django.core.exceptions import ValidationError
   import logging

   logger = logging.getLogger(__name__)

   @transaction.atomic
   def create_user_allergy(request):
       try:
           user_allergy.full_clean()  # Validates model constraints
           user_allergy.save()
           logger.info(f"User {request.user.id} created allergy {user_allergy.id}")
           return redirect('allergies:list')
       except ValidationError as e:
           logger.warning(f"Validation failed for user {request.user.id}: {e}")
           transaction.set_rollback(True)
           return render(request, 'form.html', {'error': str(e)})
       except Exception as e:
           logger.error(f"Unexpected error: {e}", exc_info=True)
           transaction.set_rollback(True)
           return render(request, 'error.html', {'message': 'Something went wrong'})
   ```

   ⚠️ When catching exceptions inside `@transaction.atomic`, you **must** either
   re-raise or call `transaction.set_rollback(True)`. Otherwise Django commits
   even after an exception.

   - **Custom Exceptions:** `allergies/exceptions.py` — `AllergenNotFoundError`,
     `InvalidIngredientError`. Verify this file exists before implementing views.
   - **Validation:** Never let `ValidationError` become a 500. Use `full_clean()`
     before `save()`.

   **Gate 3 is complete when:** all view functions have `try/except` with
   user-friendly error rendering, `@transaction.atomic` on all writes, and
   `allergies/exceptions.py` exists with domain exception classes.

   ---

   ## Forms & User Input Validation

   **Do not implement forms until Gates 2 and 3 are complete.** Check
   [`STATUS.md`](STATUS.md) for current gate state before starting.

   ### ModelForm Pattern

   ```python
   # allergies/forms.py (to be created at Gate 4)
   from django import forms
   from django.core.exceptions import ValidationError
   from allergies.models import UserAllergy, Allergen
   import logging

   logger = logging.getLogger(__name__)

   class UserAllergyForm(forms.ModelForm):
       class Meta:
           model = UserAllergy
           fields = ['allergen', 'severity_level', 'is_confirmed', 'source_info',
                     'user_reaction_details']
           widgets = {
               'user_reaction_details': forms.Textarea(attrs={'rows': 3}),
           }

       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['allergen'].queryset = Allergen.objects.filter(is_active=True)

       def clean(self):
           cleaned_data = super().clean()
           severity_level = cleaned_data.get('severity_level')
           if severity_level == 'severe' and not cleaned_data.get('is_confirmed'):
               logger.warning("Severe allergy submitted without confirmation")
               raise ValidationError("Severe allergies require confirmation")
           return cleaned_data
   ```

   ### Dynamic Category → Allergen Filtering

   The `allergen_key` choices depend on `category`. The recommended approach is a
   small JSON view (`get_allergen_keys`) that returns choices for a given category,
   called via plain JavaScript `fetch`. This avoids new dependencies and fits the
   current no-HTMX, no-partials constraint.

   ### Validation Order

   1. `Form.clean()` — cross-field validation
   2. `Model.clean()` — model-level constraints (`UserAllergy.clean()` enforces
      JSONField key discipline and future date rejection)
   3. `Model.save()` — database constraints (unique together, foreign keys)

   Always call `form.is_valid()` before accessing `form.cleaned_data`.

   ### CSRF Protection

   - Always include `{% csrf_token %}` in POST forms.
   - For JavaScript POST requests, include `X-CSRFToken` header from `getCookie('csrftoken')`.

   ### Form Error Display

   ```html
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

   ---

   ## Security Hardening (Production)

   See [`docs/SECURITY.md`](docs/SECURITY.md) for comprehensive guidance.

   ```python
   # settings.py pattern — conditional on DEBUG=False
   if not DEBUG:
       SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
       SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
       CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
       SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
   ```

   Never commit `.env`. Use `.env.example` as template.

   ---

   ## Migration Workflow

   ### Schema Migrations

   ```bash
   # Always pass --name — auto-generated names are rejected by pre-commit hook
   uv run python manage.py makemigrations allergies --name describe_the_change
   uv run python manage.py migrate
   ```

   Commit the model changes and the migration file together.

   ### Data Migrations (Allergen Catalog Seeding)

   ```bash
   uv run python manage.py makemigrations --empty allergies --name seed_allergens
   # Edit the generated file, then:
   uv run python manage.py migrate
   ```

   ```python
   # Pattern for seeding Allergen catalog from choices.py
   def seed_allergens(apps, schema_editor):
       Allergen = apps.get_model('allergies', 'Allergen')
       from allergies.constants.choices import FORM_ALLERGIES_CHOICES

       for category_key, _, choice_list in FORM_ALLERGIES_CHOICES:
           for key, label in choice_list:
               Allergen.objects.get_or_create(
                   category=category_key,
                   allergen_key=key,
                   defaults={'is_active': True}
               )

   def reverse_seed(apps, schema_editor):
       apps.get_model('allergies', 'Allergen').objects.all().delete()

   class Migration(migrations.Migration):
       dependencies = [('allergies', '0002_initial')]  # adjust to latest
       operations = [migrations.RunPython(seed_allergens, reverse_seed)]
   ```

   ⚠️ `choices.py` must be complete (no stub comments) before this migration is
   written. Check [`STATUS.md`](STATUS.md) → Known Gaps.

   ### Migration Conflicts

   ```bash
   git pull origin main
   uv run python manage.py showmigrations
   uv run python manage.py makemigrations --merge
   uv run python manage.py migrate
   ```

   ---

   ## Admin Customization Patterns

   ```python
   class UserAllergyAdmin(admin.ModelAdmin):
       list_display = ['user', 'allergen', 'severity_level', 'is_active']
       list_select_related = ['user', 'allergen']  # Avoid N+1

   @admin.action(description="Deactivate selected allergens")
   def deactivate_allergens(modeladmin, request, queryset):
       logger.info(f"Admin {request.user.id} deactivating {queryset.count()} allergens")
       queryset.update(is_active=False)
   ```

   - Mark `created_at`, `updated_at` as `readonly_fields`.
   - All admin actions must have logging (Gate 2 requirement).

   ---

   ## 🧪 Testing & Fixture Reference

   ### Coverage Thresholds by Gate

   | Gate | Overall Minimum | New Code Minimum |
   |------|----------------|------------------|
   | Gates 1–3 | 75% | 75% |
   | Gate 4 | 75% | 80% |
   | Gate 5 | 80% | 80% |

   ### Fixture Reference (`conftest.py`)

   **✅ Use these fixtures:**

   | Fixture | Creates | Use Case |
   |---------|---------|----------|
   | `test_user` | CustomUser | Standard authenticated user |
   | `user_email` | String | Email for test users |
   | `user_password` | String | Auto-dependency of `test_user` |
   | `authenticated_client` | Client (logged in) | Auth-required views |
   | `contact_allergen` | Allergen (SLS) | Contact/topical allergen |
   | `food_allergen` | Allergen (Peanut) | Food allergen |
   | `user_allergy` | UserAllergy | Linked user→allergen |

   **⚠️ Deprecated (backward compat only — do not use in new tests):**
   `custom_user` → use `test_user` | `allergen_contact` → use `contact_allergen` | `allergen_food` → use `food_allergen`

   ### Test File Organization

   ```
   allergies/tests/
   ├── __init__.py
   ├── test_models.py               # Allergen + UserAllergy model tests
   ├── test_views.py                # View tests (GET, POST, auth redirect)
   ├── test_admin_error_handling.py # Admin action error scenarios
   └── test_exceptions.py           # Custom exception tests

   users/
   └── tests.py                     # CustomUser model tests
   ```

   ### Example: Model Test

   ```python
   @pytest.mark.django_db
   class TestAllergenModel:
       def test_allergen_str_representation(self, contact_allergen, food_allergen):
           assert str(contact_allergen) == "Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
           assert str(food_allergen) == "Food Allergens: Peanut"
   ```

   ### Example: View Test

   ```python
   @pytest.mark.django_db
   class TestAllergiesListView:
       def test_authenticated_access_succeeds(self, authenticated_client):
           response = authenticated_client.get(reverse("allergies:list"))
           assert response.status_code == 200

       def test_unauthenticated_access_redirects(self, client):
           response = client.get(reverse("allergies:list"))
           assert response.status_code == 302
           assert "/accounts/login/" in response.url
   ```

   ### Test Markers

   Only registered markers may be used (`--strict-markers` enforced in `pyproject.toml`):
   `unit` | `integration` | `slow`

   ---

   ## 🗄️ Database State & Migration Strategy

   - **Development:** SQLite (`db.sqlite3`)
   - **CI/CD:** Fresh SQLite per test run
   - **Schema tracking:** `allergies/migrations/`, `users/migrations/`

   ### Fresh Database Setup

   ```bash
   cp db.sqlite3 db.sqlite3.backup  # Back up first
   rm db.sqlite3
   uv run python manage.py migrate
   uv run python manage.py createsuperuser
   ```

   ### Rollback

   ```bash
   uv run python manage.py migrate allergies zero           # Full rollback
   uv run python manage.py migrate allergies 0001_initial   # Specific migration
   uv run python manage.py showmigrations
   uv run python manage.py migrate --plan
   ```

   ---

   ## Current Patterns vs. Future Features

   ### ✅ Use These Now

   - **Synchronous Views:** All views are `def` — never `async def`
   - **Traditional Templates:** `{% extends 'layout.html' %}` and `{% include %}` — never `{% partialdef %}`
   - **SQLite in dev, PostgreSQL in prod**
   - **`uv` for all package management**
   - **Ruff + Mypy enforced in pre-commit**

   ### 🚧 Future Only — Do Not Use

   | Feature | Status | When to Consider |
   |---------|--------|-----------------|
   | `async def` views | ⚠️ NOT USED | External API integration (product scanning) |
   | `{% partialdef %}` / `{% partial %}` | ⚠️ NOT USED | If HTMX is adopted |
   | `django.tasks` / `@task` | ⚠️ NOT USED | Email notifications, data cleanup |
   | Django 6.0 Form Field Groups | ⚠️ NOT USED | Complex multi-section forms |

   When suggesting these to users: acknowledge the capability exists, clarify it
   is not used here, recommend the current synchronous/traditional pattern.

   ---

   ## Coding Standards (Ruff & Mypy)

   - Ruff target: py313. Use `_` for unused variables in tuple unpacking.
   - Run `uv run mypy .` before committing logic changes to models or views.
   - All new functions must have explicit type hints — no bare `QuerySet`, use `QuerySet[Allergen]`.
   - `# type: ignore[assignment]` is acceptable for `ManyToManyField` on `AbstractUser` overrides.

   ---

   ## CI/CD

   - CI enforces `.python-version` and `uv lock --check`. Sync lockfile before committing.
   - Gate 1 (Lint): Ruff + Mypy pre-commit must pass.
   - Gate 2 (Test): Pytest suite must pass.
   - Gate 3 (Coverage): 75% minimum (current phase). See coverage thresholds table above.
   - If CI fails on "Static Analysis", fix Ruff/Mypy errors before touching logic.

   ---

   ## Extension Points

   - **Product safety check POST handler** (`skincare_project/views.py` `product` view):
     1. Parse and tokenize the raw ingredient string (comma-split, strip whitespace, lowercase)
     2. Resolve aliases via `AllergenAlias` lookup (planned — design the service layer to accept this as an injectable step so Phase 1 exact matching works without it)
     3. Compare resolved keys against active `UserAllergy` for `request.user`
     4. Return matches with `severity_level`, `source_info`, `user_reaction_details`
     - **Blocked** until logging and error handling exist in this file. See [`STATUS.md`](STATUS.md).
   - **Users app routing:** add `path('users/', include('users.urls'))` once views have logging and error handling

   ---

   ## Practical Snippets

   ```python
   # Active allergens ordered
   from allergies.models import Allergen
   Allergen.objects.filter(is_active=True).order_by('category', 'allergen_key')

   # Current user allergies with labels
   # Phase 1: exact allergen_key match only.
   # Phase 2 (Synonym Mapper): resolve ingredient tokens to canonical allergen_keys
   # via AllergenAlias before this filter — do not extend this snippet until that model exists.
   from allergies.models import UserAllergy
   qs = UserAllergy.objects.select_related('allergen').filter(user=request.user, is_active=True)
   for ua in qs:
       label = ua.allergen.allergen_label
   ```

   ---

   ## Gotchas

   - `allergen_key` choices are category-dependent; `choices=[]` in the model is
     intentional — filtering happens in forms.
   - `UserAllergy.clean()` runs automatically via `save()` override — never call
     `save()` directly without going through `full_clean()`. The JSON key guard in
     `clean()` will reject unknown keys.
   - **Migration naming:** Always pass `--name`. Auto-generated names like
     `0004_auto_<timestamp>` are rejected by the `enforce-migration-naming`
     pre-commit hook.
   - **JSONField key discipline:** Only use canonical keys from model `help_text`
     and type aliases (`ReactionDetails`, `AdminNotes`). Inventing new keys
     silently corrupts existing data.
   - Static files served from `static/` with `STATICFILES_DIRS` in settings.

   ---

   ## AI Agent Behavior & Quality Standards

   ### Gate Enforcement

   Read [`STATUS.md`](STATUS.md) first. Do not implement Gate N work if Gate N-1
   is incomplete. Violations:
   - ❌ New view without logging → reject, complete Gate 2 first
   - ❌ Feature without error handling → reject, complete Gate 3 first
   - ❌ Form without tests → reject, add tests before marking done

   ### Verification Before Marking Complete

   Never mark a task done without:
   1. Opening the actual source file and confirming the code is there
   2. Running `uv run pytest` for affected modules
   3. Running `ruff check . --fix` and `ruff format .`
   4. Running `mypy .`
   5. Running `bandit -r . -ll` if models or views changed
   6. Updating [`STATUS.md`](STATUS.md) — not this file

   ### Core Principles

   1. **Simplicity First** — minimal changes for maximum impact; don't refactor
      unrelated code in the same commit
   2. **Root Cause** — no temporary fixes; trace to source
   3. **Minimal Blast Radius** — use `.select_related()`, test adjacent
      functionality if uncertain
   4. **Senior Engineer Standards** — docstrings for non-obvious logic; no debug
      statements or print() calls committed

   ### Autonomous Bug Fixing

   1. Parse error logs / stack traces without asking for clarification
   2. Trace to root cause
   3. Implement fix respecting gate order
   4. Run tests to verify
   5. Document non-obvious fixes with inline comments
   6. Stop and request guidance if the same CI job fails 3+ times

   ### Error Context

   | Error Type | Where to Look |
   |-----------|--------------|
   | Dependency | `pyproject.toml` dependency groups |
   | Import | Verify `uv sync` ran; check `.python-version` |
   | Model | `allergies/models.py`, `users/models.py` |
   | Validation | `allergies/constants/choices.py` `CATEGORY_CHOICES` |
   | Test | `pytest.ini` markers; `conftest.py` fixtures |
   | Type | `[tool.mypy]` and `[tool.django-stubs]` in `pyproject.toml` |

   ---

   ## Type Checking (Mypy)

   - Config: `[tool.mypy]` and `[tool.django-stubs]` in `pyproject.toml` are the source of truth.
   - Use `QuerySet[Allergen]` / `Manager[Allergen]` for ORM type hints.
   - Run `mypy .` before committing logic changes to `allergies/models.py`.
   - If pre-commit fails on type errors, run `mypy .` locally to debug.

   ---

   *This file documents stable architecture and conventions.*
   *For current gate status and active work items, see [`STATUS.md`](STATUS.md).*
   ssions
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
