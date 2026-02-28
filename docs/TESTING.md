# Testing Guide

## Overview

This guide documents the testing strategy, fixture patterns, coverage expectations, and best practices for writing tests in the Skincare Allergy Filter project. All contributors (human and AI agents) must follow these guidelines to maintain code quality and reliability.

**Current Coverage Target:** 50% (Phase 1 minimum) → 80% (Phase 2 goal)

---

## Test Organization

### Directory Structure

```
allergies/tests/
    __init__.py
    test_models.py           # Allergen, UserAllergy model tests
    test_views_error_handling.py
    test_admin_error_handling.py
    test_exceptions.py

users/
    tests.py                 # CustomUser model tests, signals, validators

conftest.py                  # Shared fixtures (project root)
```

### Test Categories

Tests are organized using pytest markers defined in [pyproject.toml](../pyproject.toml#L287-L291):

- **`@pytest.mark.unit`** - Fast unit tests (< 100ms), no database or external dependencies preferred
- **`@pytest.mark.integration`** - Integration tests involving multiple models, database transactions, or external APIs
- **`@pytest.mark.slow`** - Tests taking > 1 second (use sparingly)

**Default:** Tests without markers are treated as standard unit tests with database access.

---

## Fixtures

### Shared Fixtures (Project Root)

Located in [conftest.py](../conftest.py) at the project root for reuse across all apps:

```python
@pytest.fixture
def media_root(settings, tmp_path_factory):
    """Redirect MEDIA_ROOT to a temp directory; prevents writes to real media/ during tests."""
    temp_media = tmp_path_factory.mktemp("media")
    settings.MEDIA_ROOT = str(temp_media)
    yield temp_media

@pytest.fixture
def user_email():
    """Standard test email address."""
    return "test@example.com"

@pytest.fixture
def user_password():
    """Standard test password for all users."""
    return "SecurePassword123!"

@pytest.fixture
def test_user(db, user_email, user_password):
    """Create standard test user with predictable credentials."""
    return User.objects.create_user(
        email=user_email,
        username="testuser",
        password=user_password
    )

@pytest.fixture
def authenticated_client(client, test_user, user_password):
    """Django test client with authenticated session."""
    client.login(email=test_user.email, password=user_password)
    return client

@pytest.fixture
def contact_allergen(db):
    """Contact allergen: Sodium Lauryl Sulfate (SLS)."""
    return Allergen.objects.create(
        category=CATEGORY_CONTACT,
        allergen_key="sls",
        is_active=True
    )

@pytest.fixture
def food_allergen(db):
    """Food allergen: Peanut."""
    return Allergen.objects.create(
        category=CATEGORY_FOOD,
        allergen_key="peanut",
        is_active=True
    )

@pytest.fixture
def user_allergy(db, test_user, contact_allergen):
    """Confirmed UserAllergy linking test_user to contact_allergen."""
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
        severity_level="moderate",
        is_confirmed=True,
    )

@pytest.fixture
def unconfirmed_user_allergy(db, test_user, contact_allergen):
    """Unconfirmed UserAllergy; uses model defaults (severity_level='', is_confirmed=False)."""
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
    )
```

### App-Specific Fixtures

For fixtures used only within a single app, define them in the app's test file or a `conftest.py` within that app's test directory. The shared fixtures above cover the most common cross-app scenarios — only create app-specific fixtures for truly isolated concerns.

### Deprecated Aliases

The following fixture aliases exist in [conftest.py](../conftest.py) for backward compatibility. **New tests must use the canonical name.** Aliases will be removed in `v1.0.0`.

| Alias | Canonical Replacement | Removed in |
|---|---|---|
| `custom_user` | `test_user` | `v1.0.0` |
| `allergen_contact` | `contact_allergen` | `v1.0.0` |
| `allergen_food` | `food_allergen` | `v1.0.0` |

> [!NOTE]
> When you encounter `custom_user`, `allergen_contact`, or `allergen_food` in older test files, replace them with their canonical counterparts above. Do not introduce these aliases in new tests.

---

## Test Patterns

### Model Tests

**Location:** `app/tests/test_models.py`

**Pattern:** Test model creation, validation, constraints, methods, and string representations.

**Example from [allergies/tests/test_models.py](../allergies/tests/test_models.py#L29-L42):**

```python
class TestAllergenModel:
    def test_allergen_str_representation(self, allergen_contact, allergen_food):
        """Verify __str__ returns 'Category: Allergen Name' format."""
        assert (
            str(allergen_contact)
            == "Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
        )
        assert str(allergen_food) == "Food Allergens: Peanut"

    def test_category_to_allergens_map(self):
        """Verify CATEGORY_TO_ALLERGENS_MAP contains all allergen choices."""
        contact_allergens = CATEGORY_TO_ALLERGENS_MAP.get(CATEGORY_CONTACT, [])
        food_allergens = CATEGORY_TO_ALLERGENS_MAP.get(CATEGORY_FOOD, [])

        assert ("sls", "Sodium Lauryl Sulfate (SLS)") in contact_allergens
        assert ("peanut", "Peanut") in food_allergens
        assert len(contact_allergens) > 1
        assert len(food_allergens) > 1
```

**Common Model Test Scenarios:**

1. **Field Validation** - Test max_length, choices, blank/null constraints
2. **Unique Constraints** - Verify `unique_together` enforcement
3. **Custom Validation** - Test `clean()` method raises `ValidationError`
4. **String Representation** - Test `__str__()` and `__repr__()`
5. **Properties & Methods** - Test custom model methods and computed properties
6. **Signals** - Test post_save, pre_save, pre_delete signal handlers

### View Tests

**Location:** `app/tests/test_views.py`

**Pattern:** Test HTTP responses, authentication requirements, template rendering, form validation, and error handling.

**Key Areas to Cover:**

1. **HTTP Method Support** - GET, POST, PUT, DELETE
2. **Authentication** - Unauthenticated vs authenticated access
3. **Authorization** - User permissions and ownership checks
4. **Status Codes** - 200 OK, 201 Created, 400 Bad Request, 403 Forbidden, 404 Not Found
5. **Template Rendering** - Correct template used, context variables present
6. **Redirects** - POST-redirect-GET pattern for form submissions
7. **Error Handling** - Graceful handling of invalid input, database errors

**Example Pattern:**

```python
@pytest.mark.django_db
class TestAllergyListView:
    def test_unauthenticated_user_redirected(self, client):
        """Verify anonymous users are redirected to login."""
        response = client.get(reverse('allergies_list'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_authenticated_user_sees_own_allergies(self, authenticated_client, test_user, contact_allergen):
        """Verify user sees only their own allergies."""
        UserAllergy.objects.create(user=test_user, allergen=contact_allergen)

        response = authenticated_client.get(reverse('allergies_list'))

        assert response.status_code == 200
        assert 'allergies/allergies_list.html' in [t.name for t in response.templates]
        assert contact_allergen.allergen_label in response.content.decode()

    def test_post_creates_allergy(self, authenticated_client, test_user, contact_allergen):
        """Verify POST creates UserAllergy and redirects."""
        data = {
            'allergen': contact_allergen.id,
            'severity_level': 'moderate',
            'is_confirmed': True,
        }

        response = authenticated_client.post(reverse('allergy_create'), data=data)

        assert response.status_code == 302
        assert UserAllergy.objects.filter(user=test_user, allergen=contact_allergen).exists()
```

### Error Handling Tests

**Location:** `app/tests/test_views_error_handling.py`, `app/tests/test_admin_error_handling.py`

**Purpose:** Verify graceful error handling for validation errors, database errors, and edge cases.

**Pattern:** Test exception handling, transaction rollbacks, user-friendly error messages, and logging.

```python
class TestErrorHandling:
    def test_duplicate_allergy_raises_validation_error(self, authenticated_client, test_user, contact_allergen):
        """Verify duplicate UserAllergy raises ValidationError, not IntegrityError."""
        UserAllergy.objects.create(user=test_user, allergen=contact_allergen)

        data = {'allergen': contact_allergen.id, 'severity_level': 'mild', 'is_confirmed': False}
        response = authenticated_client.post(reverse('allergy_create'), data=data)

        assert response.status_code == 400
        assert 'already exists' in response.content.decode().lower()
```

### Integration Tests

**Marker:** `@pytest.mark.integration`

**Purpose:** Test interactions between multiple models, apps, or external systems.

**Example:**

```python
@pytest.mark.integration
def test_user_allergy_cascade_delete(test_user, contact_allergen):
    """Verify UserAllergy is deleted when user is deleted."""
    UserAllergy.objects.create(user=test_user, allergen=contact_allergen)

    user_id = test_user.id
    test_user.delete()

    assert not UserAllergy.objects.filter(user_id=user_id).exists()
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
uv run pytest

# Run tests for specific app
uv run pytest allergies/tests/

# Run specific test file
uv run pytest allergies/tests/test_models.py

# Run specific test class or function
uv run pytest allergies/tests/test_models.py::TestAllergenModel
uv run pytest allergies/tests/test_models.py::TestAllergenModel::test_allergen_str_representation

# Run tests by marker
uv run pytest -m unit          # Only unit tests
uv run pytest -m integration   # Only integration tests
uv run pytest -m "not slow"    # Exclude slow tests
```

### With Coverage

```bash
# Run tests with coverage report
uv run pytest --cov --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov --cov-report=html

# Open coverage report (Windows)
start htmlcov/index.html

# Fail if coverage is below threshold (50%)
uv run pytest --cov --cov-fail-under=50
```

### Verbose Output

```bash
# Show test names and outcomes
uv run pytest -v

# Show print statements and logs
uv run pytest -s

# Show detailed traceback
uv run pytest --tb=long

# Show summary of all test outcomes
uv run pytest -ra
```

### Parallel Execution (Future)

```bash
# Install pytest-xdist
uv add --group test pytest-xdist

# Run tests in parallel (4 workers)
uv run pytest -n 4
```

---

## Coverage Configuration

Coverage settings are defined in [pyproject.toml](../pyproject.toml#L302-L336).

### Current Settings

- **Minimum Coverage:** 50% (`fail_under = 50`)
- **Branch Coverage:** Enabled (`branch = true`)
- **HTML Reports:** Output to `htmlcov/`
- **Omitted Files:** Migrations, tests, `__pycache__`, venv, `manage.py`, ASGI/WSGI

### Phase 1 vs Phase 2

| Metric               | Phase 1 (Current) | Phase 2 (Goal)  |
|----------------------|-------------------|-----------------|
| Overall Coverage     | 50%               | 80%             |
| New Code Coverage    | 70%               | 90%             |
| Branch Coverage      | ✅ Enabled         | ✅ Enabled       |

**Coverage Rules for New Code:**

- **New features:** Minimum 70% coverage required
- **Bug fixes:** Must include regression test
- **Refactoring:** Must not decrease coverage

---

## AI Testing Guidelines

### For AI Agents Implementing Features

**Rule 1: All new features require tests BEFORE merging**

- Write tests in parallel with feature implementation (Development Gate 5)
- Tests must cover happy path, edge cases, and error scenarios
- Minimum 70% coverage for new code

**Rule 2: Use descriptive test names**

Format: `test_<action>_<expected_result>`

✅ Good:
```python
def test_create_user_allergy_with_duplicate_allergen_raises_validation_error(...)
def test_authenticated_user_sees_only_own_allergies(...)
def test_allergen_str_representation_includes_category_and_name(...)
```

❌ Bad:
```python
def test_allergy(...)
def test_view(...)
def test_model_1(...)
```

**Rule 3: Use fixtures from conftest.py**

Reuse shared fixtures instead of duplicating setup code:

```python
# ❌ Don't duplicate fixture logic
def test_something():
    user = User.objects.create_user(email="test@example.com", username="testuser", password="pass")
    allergen = Allergen.objects.create(category=CATEGORY_CONTACT, allergen_key="sls")
    # ...

# ✅ Use shared fixtures
def test_something(test_user, contact_allergen):
    # Fixtures automatically provide user and allergen
    # ...
```

**Rule 4: Test error handling, not just happy paths**

Every feature must test:
- ✅ Valid input (happy path)
- ✅ Invalid input (validation errors)
- ✅ Edge cases (empty strings, None values, boundary conditions)
- ✅ Authentication/authorization (unauthenticated, unauthorized users)

**Rule 5: Follow Development Gates**

Do NOT write tests before implementing:
1. ✅ Gate 1: Dependencies installed
2. ✅ Gate 2: Logging infrastructure in place
3. ✅ Gate 3: Error handling implemented
4. ✅ Gate 4: Forms created (if applicable)
5. 🎯 Gate 5: **NOW write tests** (parallel with Gate 4 for forms)

See [.github/instructions/copilot-instructions.md](../.github/instructions/copilot-instructions.md#L108-L150) for full gate requirements.

**Rule 6: Run tests before committing**

```bash
# Run tests and pre-commit hooks
uv run pytest
pre-commit run --all-files

# Verify coverage meets minimum
uv run pytest --cov --cov-fail-under=50
```

---

## Test Data Strategies

### Realistic vs Minimal Data

**Use realistic data for:**
- Integration tests
- End-to-end scenarios
- User acceptance testing
- Example data in fixtures

**Use minimal data for:**
- Unit tests
- Validation tests
- Performance tests

### Test Database

- **Development:** SQLite (`db.sqlite3`)
- **CI/CD:** Fresh SQLite instance per test run
- **Tests:** In-memory SQLite (fast, isolated)

Django pytest automatically creates a test database for each test session and rolls back transactions after each test.

---

## Common Pitfalls

### ❌ Testing Implementation Details

Don't test private methods or internal state. Test **behavior** from the user's perspective.

```python
# ❌ Bad: Testing internal attribute
def test_allergen_internal_cache():
    allergen = Allergen(category=CATEGORY_CONTACT, allergen_key="sls")
    assert allergen._cached_label is None

# ✅ Good: Testing public behavior
def test_allergen_label_property_returns_correct_label():
    allergen = Allergen(category=CATEGORY_CONTACT, allergen_key="sls")
    assert allergen.allergen_label == "Sodium Lauryl Sulfate (SLS)"
```

### ❌ Overly Broad Assertions

Be specific about what you're testing.

```python
# ❌ Bad: Too vague
def test_create_allergy(test_user, contact_allergen):
    allergy = UserAllergy.objects.create(user=test_user, allergen=contact_allergen)
    assert allergy

# ✅ Good: Specific assertions
def test_create_allergy_sets_correct_attributes(test_user, contact_allergen):
    allergy = UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
        severity_level="moderate",
        is_confirmed=True
    )
    assert allergy.user == test_user
    assert allergy.allergen == contact_allergen
    assert allergy.severity_level == "moderate"
    assert allergy.is_confirmed is True
```

### ❌ Ignoring Pre-commit Hooks

Tests must pass **and** pre-commit hooks must pass before committing.

```bash
# ✅ Always run before committing
uv run pytest && pre-commit run --all-files
```

---

## Future Enhancements

### Planned Testing Infrastructure

- [ ] **Factory Boy** - Generate test data with realistic relationships
- [ ] **pytest-xdist** - Parallel test execution for faster CI
- [ ] **pytest-django fixtures** - Database reuse for faster tests
- [ ] **Hypothesis** - Property-based testing for edge case discovery
- [ ] **Selenium/Playwright** - End-to-end UI testing
- [ ] **VCR.py** - Record/replay HTTP interactions for external API tests

### Coverage Milestones

| Milestone        | Target | ETA     | Requirements                          |
|------------------|--------|---------|---------------------------------------|
| Phase 1 Complete | 50%    | Current | All apps have basic model/view tests  |
| Phase 2 Start    | 60%    | Q2 2026 | Admin tests, error handling complete  |
| Phase 2 Complete | 80%    | Q3 2026 | Integration tests, signal tests added |
| Production Ready | 90%+   | Q4 2026 | E2E tests, performance tests added    |

---

## Resources

- **Pytest Documentation:** https://docs.pytest.org/
- **pytest-django Documentation:** https://pytest-django.readthedocs.io/
- **Django Testing:** https://docs.djangoproject.com/en/6.0/topics/testing/
- **Coverage.py:** https://coverage.readthedocs.io/

---

## Questions?

For questions about testing strategy or patterns, refer to:
- [.github/instructions/copilot-instructions.md](../.github/instructions/copilot-instructions.md) - Development gates and conventions
- [pyproject.toml](../pyproject.toml) - Tool configurations (pytest, coverage, mypy)
- Existing test files in `allergies/tests/` and `users/tests.py`
