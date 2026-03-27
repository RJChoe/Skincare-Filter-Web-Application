# Contributing to Skincare Allergy Filter

Thank you for your interest in contributing to the Skincare Allergy Filter project! This guide outlines the development workflow, coding standards, and best practices for both human and AI contributors.

---

## Table of Contents

1. [Development Workflow](#development-workflow)
2. [Development Gates](#development-gates)
3. [Getting Started](#getting-started)
4. [Pull Request Requirements](#pull-request-requirements)
5. [Code Style](#code-style)
6. [Core Logic Patterns](#core-logic-patterns)
7. [Commit Messages](#commit-messages)
8. [Testing](#testing)
9. [For AI Agents](#for-ai-agents)
10. [Questions & Support](#questions--support)

---

## Development Workflow

### 1. Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Skincare-Filter-Web-Application.git
cd Skincare-Filter-Web-Application
```

### 2. Set Up Environment

```bash
# Install uv (if not already installed)
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and sync environment
uv sync

# Apply database migrations
uv run python manage.py migrate

# Install pre-commit hooks
uv run pre-commit install
```

### 3. Create Feature Branch

```bash
# Create a new branch from main
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 4. Make Changes

Follow the [Development Gates](#development-gates) (strict order: dependency → logging → error handling → forms → tests).

### 5. Test & Lint

```bash
# Run tests with coverage
uv run pytest --cov --cov-report=term-missing

# Run pre-commit hooks
pre-commit run --all-files

# Or let pre-commit run automatically on git commit
git commit -m "feat: add user allergy validation"
```
### 6. Push & Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Use the PR template and fill in all required sections
```

### Pre-commit Hooks

#### Setup
Install and configure pre-commit hooks:

```bash
# Install pre-commit (included in dev/lint groups)
uv sync --group lint

# Set up git hooks
uv run pre-commit install

# Run manually on all files
uv run pre-commit run --all-files
```

#### Configuration
Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.1
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: local
    hooks:
      - id: pytest-fast
        name: pytest-fast
        entry: uv run pytest -m "not slow" --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

This configuration runs:
- **Ruff Linter:** Checks code quality (500+ rules, including Django-specific checks)
- **Ruff Formatter:** Auto-formats Python code (Black-compatible)
- **File hygiene:** Removes trailing whitespace, ensures newlines at end of files
- **Fast tests:** Runs non-slow tests (typically ~5-10 seconds)

**Note:** Pre-commit hooks run automatically before each commit. If checks fail, the commit is blocked until issues are resolved.

### Fail Fast Checklist
Catch issues in ~10-15 seconds before committing. Run these manual checks during active development to verify code quality before pre-commit hooks execute.

#### Quick Verification Commands

- **Run fast tests** — Verify core logic without slow integration tests:
    ```bash
    uv run pytest -m "not slow"
    ```

- **Lint with Ruff** — Check code quality and formatting:
    ```bash
    uv run ruff check . --fix
    uv run ruff format . --check
    ```

- **Confirm migrations applied** — Check database migration status:
    ```bash
    uv run python manage.py showmigrations
    ```

#### Power User Tip
Run all checks sequentially with a single command:

```bash
uv run pytest -m "not slow" && uv run ruff check . --fix && uv run ruff format . --check && uv run python manage.py showmigrations
```

**Note:** While pre-commit hooks automate these checks, running them manually helps catch issues faster during development. See [Troubleshooting](#troubleshooting) for resolving common failures.

---

## Development Gates

**⚠️ CRITICAL: Follow these gates in strict priority order. Do NOT implement new features until foundations are complete.**

### Gate 1: Dependency Management

**Before any code changes:**

1. Install required dependencies:
   ```bash
   uv add <package>                    # Add to base dependencies
   uv add --group test <package>       # Add to test group
   uv add --group dev <package>        # Add to dev group
   ```

2. Verify dependency installation:
   ```bash
   uv run python -c "import <package>; print('OK')"
   ```

3. Update lockfile:
   ```bash
   uv sync
   ```

**Required Dependencies:**
- `django-environ` - Environment variable management (see [docs/SECURITY.md](docs/SECURITY.md))

### Gate 2: Logging Infrastructure

**Before implementing ANY new features:**

1. Add logging to all modules with business logic:
   ```python
   import logging

   logger = logging.getLogger(__name__)
   ```

2. Log security events at INFO level:
   ```python
   logger.info(f"User {user.id} created allergy {allergy.id} for allergen {allergen.allergen_key}")
   ```

3. Log errors at ERROR level with traceback:
   ```python
   logger.error(f"Failed to process ingredient list: {e}", exc_info=True)
   ```

4. Log performance issues at DEBUG level:
   ```python
   logger.debug(f"Query took {elapsed}s: {query}")
   ```

**Required Files:**
- `skincare_project/views.py`
- `allergies/views.py`
- `allergies/models.py` (for validation failures)
- `allergies/admin.py`
- `users/admin.py`

**⚠️ GDPR Compliance:** Do NOT log personal data (emails, passwords). Log user IDs only.

### Gate 3: Error Handling

**Before implementing forms or POST handlers:**

1. Add try-except blocks to all view functions:
   ```python
   from django.db import transaction
   from django.core.exceptions import ValidationError
   import logging

   logger = logging.getLogger(__name__)
    # ✅ Pattern 1: For Django views (direct HTTP handlers)
    @transaction.atomic
   def create_user_allergy(request):
       try:
           user_allergy = UserAllergy(user=request.user, allergen_id=request.POST['allergen'])
           user_allergy.full_clean()  # Validates model constraints
           user_allergy.save()
           logger.info(f"User {request.user.id} created allergy {user_allergy.id}")
           return redirect('allergies_list')
       except ValidationError as e:
           logger.warning(f"Validation failed for user {request.user.id}: {e}")
           transaction.set_rollback(True)  # Ensure transaction rollback
           return render(request, 'form.html', {'error': str(e)})
       except Exception as e:
           logger.error(f"Unexpected error creating allergy: {e}", exc_info=True)
           transaction.set_rollback(True)  # Ensure transaction rollback
           return render(request, 'error.html', {'message': 'Something went wrong'})

    # ✅ Pattern 2: For service layer (business logic)
    # services.py
    @transaction.atomic
    def create_user_allergy(user: User, allergen: Allergen, severity_level: str) -> UserAllergy:
        """Business logic for creating user allergy. Raises exceptions on failure."""
        user_allergy = UserAllergy(user=user, allergen=allergen, severity_level=severity_level)
        user_allergy.full_clean()  # Raises ValidationError
        user_allergy.save()
        return user_allergy

    # views.py - Caller handles exceptions and HTTP responses
    def create_allergy_view(request):
        try:
            allergy = create_user_allergy(
                user=request.user,
                allergen=Allergen.objects.get(id=request.POST['allergen']),
                severity=request.POST['severity']
            )
            logger.info(f"User {request.user.id} created allergy {allergy.id}")
            return redirect('allergies_list')
        except ValidationError as e:
            logger.warning(f"Validation failed for user {request.user.id}: {e}")
            return render(request, 'form.html', {'error': str(e)})
   ```

2. Implement @transaction.atomic for multi-model operations

⚠️ CRITICAL: When catching exceptions inside @transaction.atomic, you MUST either:

    +  Re-raise the exception (raise) to trigger automatic rollback, OR
    + Explicitly mark for rollback with transaction.set_rollback(True)

Otherwise, Django will COMMIT the transaction even if an exception occurred.

3. Create custom exception classes in `app/exceptions.py`:
   ```python
   class AllergenNotFoundError(Exception):
       """Raised when allergen lookup fails."""
       pass
   ```

4. Surface validation errors properly (no 500 errors on user input)

### Gate 4: Forms & Validation

**After logging + error handling are complete:**

1. Create `app/forms.py` with ModelForm classes
2. Implement dynamic field filtering (e.g., category-dependent allergen choices)
3. Add CSRF protection in templates: `{% csrf_token %}`
4. Add form validation with `clean()` methods
5. Test form validation with comprehensive test coverage
6. **⚠️ CRITICAL:** Ensure all validation and matching logic adheres to the [Core Logic Patterns](#core-logic-patterns) below.

### Gate 5: Complete Tests

**In parallel with Gate 4:**

1. Write tests for all new features (minimum 75% coverage for new code)
2. Test happy path, edge cases, and error scenarios
3. Add integration tests with `@pytest.mark.integration`
4. Ensure overall coverage meets 75% minimum (raises to 80% at Gate 5 completion)
5. Run tests before committing: `uv run pytest`

**See [docs/TESTING.md](docs/TESTING.md) for comprehensive testing guide.**

---

## Getting Started

### First-Time Contributors

1. Read [.github/instructions/copilot-instructions.md](.github/instructions/copilot-instructions.md) for architecture and conventions
2. Review [docs/TESTING.md](docs/TESTING.md) for testing patterns
3. Check [docs/SECURITY.md](docs/SECURITY.md) for security best practices
4. Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment workflows

### Finding Issues to Work On

- Browse [Issues](https://github.com/RJChoe/Skincare-Filter-Web-Application/issues)
- Look for `good-first-issue` label for beginner-friendly tasks
- Look for `help-wanted` label for issues needing contributors

### Claiming an Issue

Comment on the issue with:
```
I'd like to work on this issue. Expected completion: [date]
```

Wait for maintainer approval before starting work.

---

## Pull Request Requirements

> **Note:** Codecov coverage reports only appear on PRs from within the repository. Forked PRs will not receive a Codecov comment — this is expected security behaviour, not a failure.

All PRs must meet these criteria before merging:

### ✅ Code Quality

- [ ] **Tests added/updated** - Minimum 75% coverage for new code
- [ ] **Tests pass locally** - `uv run pytest` succeeds
- [ ] **Pre-commit hooks pass** - `pre-commit run --all-files` succeeds
- [ ] **No linting errors** - Ruff passes with `--fix` applied
- [ ] **Type checking passes** - Mypy passes (if applicable)

### ✅ Security

- [ ] **Security scan passes** - Bandit and Safety checks pass
- [ ] **No secrets committed** - Gitleaks passes
- [ ] **Environment variables used** - No hardcoded credentials
- [ ] **GDPR compliant** - No personal data in logs

### ✅ Documentation

- [ ] **Code comments added** - Non-obvious logic explained
- [ ] **Docstrings added** - All public functions/classes documented
- [ ] **Copilot instructions updated** - New patterns documented in [.github/instructions/copilot-instructions.md](.github/instructions/copilot-instructions.md)
- [ ] **README updated** - If user-facing features changed

### ✅ Database

- [ ] **Migration files included** - If models changed
- [ ] **Migration tested** - `uv run python manage.py migrate` succeeds
- [ ] **No data loss** - Migration is reversible if possible

### ✅ Development Gates

- [ ] **Gate 1: Dependencies** - All dependencies installed and in `pyproject.toml`
- [ ] **Gate 2: Logging** - All views/models have logging
- [ ] **Gate 3: Error handling** - Try-except blocks added, `@transaction.atomic` used
- [ ] **Gate 4: Forms validated** - If forms added, validation tested
- [ ] **Gate 5: Tests complete** - Coverage meets 75% for new code

### ✅ Architecture Updates

Any change to the folder structure or core logic requires an update to [ARCHITECTURE.md](./ARCHITECTURE.md).
---

## Code Style

### Python Standards

**Formatter:** Ruff (Black-compatible)
```bash
# Format code automatically
ruff format .
```
### Dependency Migration Notes

## Technical Decisions

### Migrating from [project.optional-dependencies]

If you have an existing development environment from before the PEP 735 migration:

1. Remove your existing virtual environment:
   ```bash
   # On Windows
   Remove-Item -Recurse -Force .venv

   # On macOS/Linux
   rm -rf .venv
   ```

2. Recreate the virtual environment:
   ```bash
   uv venv
   ```

3. Activate the virtual environment (see installation steps above)

4. Install dependencies with the new group system:
   ```bash
   uv sync --group dev
   ```

The new structure allows faster CI builds by installing only required dependencies per job (e.g., only `--group test` for test jobs).

## Core Logic Patterns

All backend contributions must adhere to the foundational logic patterns defined in [ARCHITECTURE.md](./ARCHITECTURE.md).

1. "Search & Destroy" Matching

    The primary objective of the filtering engine is the rapid identification of risk.

    - Fail Fast: The algorithm should flag a product as "Unsafe" immediately upon detecting the first blacklisted ingredient.
    - Identify Offender: The result must explicitly return the name of the detected allergen to the user.

2. Mandatory Normalization

    To prevent false negatives due to formatting or casing, all ingredient tokens must be processed before comparison:
    - Lowercasing: Convert all input strings and database lookups to lowercase.
    - Stripping: Remove all leading and trailing whitespace from tokens.
    - Example: " Almond Oil " must be processed as "almond oil".

**Linter:** Ruff with Django-specific rules
```bash
# Check and auto-fix issues
ruff check . --fix
```

**Type Hints:** Required for all functions
```python
# ✅ Good: Type hints for parameters and return value
def create_user_allergy(user: User, allergen: Allergen) -> UserAllergy:
    return UserAllergy.objects.create(user=user, allergen=allergen)

# ❌ Bad: No type hints
def create_user_allergy(user, allergen):
    return UserAllergy.objects.create(user=user, allergen=allergen)
```

**Imports:** Organized via Ruff (isort)
```python
# Order: future → standard library → third-party → first-party → local
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models

from allergies.constants.compounds import CATEGORY_CHOICES
from allergies.models import Allergen
```

**Paths:** Use `pathlib.Path`, not `os.path`
```python
# ✅ Good
from pathlib import Path

config_path = Path(__file__).parent / "config.json"

# ❌ Bad
import os

config_path = os.path.join(os.path.dirname(__file__), "config.json")
```

### Django Conventions

**URLs:** Use named routes
```python
# urls.py
path('allergies/', views.allergies_list, name='allergies_list'),

# views.py
from django.urls import reverse
redirect(reverse('allergies_list'))

# templates
{% url 'allergies_list' %}
```

**Queries:** Use `select_related()` and `prefetch_related()`
```python
# ✅ Good: Avoid N+1 queries
user_allergies = UserAllergy.objects.select_related('allergen').filter(user=request.user)

# ❌ Bad: N+1 query problem
user_allergies = UserAllergy.objects.filter(user=request.user)
for ua in user_allergies:
    print(ua.allergen.allergen_label)  # N additional queries
```

**Templates:** Extend `layout.html` and load static files
```django
{% extends 'layout.html' %}
{% load static %}

{% block content %}
  <img src="{% static 'images/logo.png' %}" alt="Logo">
{% endblock %}
```

### Configuration Files

- **Dependencies:** `pyproject.toml` (managed by uv)
- **Tool Config:** `pyproject.toml` ([tool.ruff], [tool.pytest.ini_options], [tool.coverage.*])
- **Pre-commit:** `.pre-commit-config.yaml`
- **Python Version:** `.python-version` (pinned to 3.13)


---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation only
- **style:** Code style changes (formatting, missing semicolons, etc.)
- **refactor:** Code refactoring (no functional changes)
- **test:** Adding or updating tests
- **chore:** Maintenance tasks (dependency updates, build config, etc.)
- **perf:** Performance improvements
- **ci:** CI/CD configuration changes

### Examples

```bash
# Feature
git commit -m "feat(allergies): add UserAllergy severity filtering"

# Bug fix
git commit -m "fix(users): prevent duplicate email registration"

# Documentation
git commit -m "docs(readme): update installation instructions for uv"

# Test
git commit -m "test(allergies): add integration tests for allergy CRUD"

# Chore
git commit -m "chore(deps): update django to 6.0.1"
```

### Scope Guidelines

- **allergies** - Allergies app changes
- **users** - Users app changes
- **templates** - Template changes
- **static** - Static file changes
- **ci** - CI/CD workflow changes
- **deps** - Dependency updates
- **config** - Configuration changes

---

## Testing

### Running Tests

```bash
# All tests
uv run pytest

# Specific app
uv run pytest allergies/tests/

# With coverage
uv run pytest --cov --cov-report=term-missing

# Verbose output
uv run pytest -v

# Run by marker
uv run pytest -m unit          # Only unit tests
uv run pytest -m integration   # Only integration tests
uv run pytest -m "not slow"    # Exclude slow tests
```

### Test Requirements

- **Minimum Coverage:** 75% for new code, 75% overall (raises to 80% at Gate 5 completion)
- **Test Categories:** Unit tests (fast), integration tests (`@pytest.mark.integration`), slow tests (`@pytest.mark.slow`)
- **Fixtures:** Use shared fixtures from [conftest.py](conftest.py) at project root
- **Naming:** Descriptive test names: `test_<action>_<expected_result>`

**See [docs/TESTING.md](docs/TESTING.md) for comprehensive testing guide.**

---

## For AI Agents

### Critical Instructions

1. **Read [.github/instructions/copilot-instructions.md](.github/instructions/copilot-instructions.md) FIRST** before making any changes
2. **Respect Development Gates** - Follow strict priority order (dependency → logging → error handling → forms → tests)
3. **Never skip tests** - All new features require tests with minimum 75% coverage
4. **Update copilot-instructions.md** - Document any new patterns or architectural decisions
5. **Use `uv run` prefix** - Never ask users to "activate venv"; always use `uv run <command>`

### Autonomous Bug Fixing Workflow

When assigned a bug report:

1. **Read error logs/traceback** - Identify root cause without asking for guidance
2. **Diagnose the issue** - Check relevant code, tests, and configuration
3. **Implement fix** - Make minimal changes to resolve the issue
4. **Add regression test** - Ensure bug doesn't reoccur
5. **Verify locally** - Run tests and confirm fix works
6. **Document changes** - Add code comments for non-obvious fixes

**Zero context switching required from the user.** Handle CI failures autonomously by reading logs and fixing issues.

### Feature Implementation Workflow

1. **Verify Development Gates** - Ensure Gates 1-3 are complete before implementing features
2. **Add logging first** - Add `logger = logging.getLogger(__name__)` to all new modules
3. **Implement error handling** - Add try-except blocks with proper validation
4. **Write tests in parallel** - Don't wait until the end; test as you code
5. **Update documentation** - Update copilot-instructions.md if introducing new patterns

### Code Quality Standards

- **Simplicity First** - Make every change as simple as possible
- **Minimal Impact** - Only touch necessary code; avoid scope creep
- **No Laziness** - Find root causes, no temporary fixes
- **Senior Developer Standards** - Code should be production-ready

### Common Pitfalls to Avoid

❌ **Don't:**
- Skip Development Gates
- Implement features without logging/error handling
- Commit code without tests
- Hardcode credentials or secrets
- Log personal data (GDPR violation)
- Use `os.path` instead of `pathlib.Path`
- Create N+1 query problems
- Skip pre-commit hooks

✅ **Do:**
- Follow Development Gates in order
- Add logging and error handling first
- Write tests with ≥75% coverage for new code
- Use environment variables for secrets
- Log user IDs only (not emails/passwords)
- Use `pathlib.Path` for file operations
- Use `select_related()`/`prefetch_related()` for queries
- Run pre-commit hooks before committing

---

## Questions & Support

### Resources

- **Architecture & Conventions:** [.github/instructions/copilot-instructions.md](.github/instructions/copilot-instructions.md)
- **Testing Guide:** [docs/TESTING.md](docs/TESTING.md)
- **Security Best Practices:** [docs/SECURITY.md](docs/SECURITY.md)
- **Deployment Guide:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Tool Configuration:** [pyproject.toml](pyproject.toml)

### Getting Help

- **Issues:** [GitHub Issues](https://github.com/RJChoe/Skincare-Filter-Web-Application/issues)
- **Discussions:** [GitHub Discussions](https://github.com/RJChoe/Skincare-Filter-Web-Application/discussions)
- **Maintainer:** @RJChoe

### Reporting Bugs

Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) and include:
- Clear description of the bug
- Reproduction steps
- Expected vs actual behavior
- Error messages/traceback
- Environment details (Python version, OS, browser)

### Requesting Features

Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md) and include:
- User story (As a... I want... So that...)
- Affected apps (allergies/users)
- Acceptance criteria
- Technical approach (optional)

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

Thank you for contributing to the Skincare Allergy Filter! 🎉
