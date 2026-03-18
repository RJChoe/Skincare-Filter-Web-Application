# Testing Guide

> Gate 5 reference. See [STATUS.md](../../STATUS.md) for current completion state.
> Source of truth for fixtures, patterns, coverage thresholds, and pitfalls.

---

## Running Tests

```bash
uv run pytest                                    # All tests (coverage auto-applied via pyproject.toml)
uv run pytest allergies/tests/test_models.py -v  # Specific file, verbose
uv run pytest allergies/tests/test_models.py::TestAllergenModel  # Specific class
uv run pytest -k test_allergen                   # Pattern match
uv run pytest -m "not slow"                      # Exclude slow tests
uv run pytest -m integration                     # Only integration tests
uv run pytest --cov --cov-report=html            # HTML report → open htmlcov/index.html
uv run pytest --no-cov                           # Skip coverage (faster during active development)
uv run pytest -ra                                # Summary of all non-passing tests
uv run pytest -s                                 # Show log/print output inline
```

Coverage settings (`branch = true`, `fail_under`, omit patterns) are configured in
`pyproject.toml` — do not pass `--cov` flags manually unless overriding.

---

## Coverage Thresholds

| Gate | Overall | New Code | Notes |
|------|---------|----------|-------|
| Gates 1–3 | 75% | 75% | Models, admin |
| Gate 4 | 75% | 80% | Views + forms added |
| Gate 5 | 80% | 80% | Full feature coverage |

- **New features:** 80% minimum for new code
- **Bug fixes:** must include a regression test
- **Refactoring:** must not decrease overall coverage

Write tests targeting the **next** gate's threshold when implementing new features.

### By Module Type

- **Models:** 75% — all `clean()`, `save()`, `__str__`, properties, constraints
- **Views:** 75% — GET, POST, auth redirect, error cases, template context
- **Forms:** 75% — `clean()` methods, validation errors, edge cases
- **Integration:** mark with `@pytest.mark.integration`

---

## Test Markers

Only registered markers may be used — `--strict-markers` is enforced in `pyproject.toml`.

| Marker | When to Use |
|--------|------------|
| `unit` | Single model/function, no DB or external calls |
| `integration` | Spans multiple apps or tests an end-to-end workflow |
| `slow` | Takes > 1 second — excluded from the pre-commit fast run |

Tests without a marker are treated as standard tests with database access.

---

## File Organization

```
allergies/tests/
├── __init__.py
├── test_models.py               # Allergen + UserAllergy — TODO at L59 (incomplete)
├── test_views.py                # View tests — existence unverified, audit needed
├── test_admin_error_handling.py # Admin action error scenarios — existence unverified
└── test_exceptions.py           # AllergenNotFoundError, InvalidIngredientError

users/
└── tests.py                     # 382 lines — scope/coverage unknown, audit needed

conftest.py                      # Shared fixtures (project root)
```

---

## Known Gaps — Verify Before Marking Gate 5 Complete

- `allergies/tests/test_models.py` L59: TODO for `UserAllergy` fields —
  `severity_level` choices, `is_confirmed` toggling, `user_reaction_details`
  JSONField key validation, future `symptom_onset_date` rejection
- `users/tests.py`: 382 lines exist but coverage scope is unknown — audit required
- `test_views.py` and `test_admin_error_handling.py` — file existence unverified
- No form tests (blocked on Gate 4)
- No integration test for the full allergy profile → product check flow

---

## Fixture Reference (`conftest.py`)

### ✅ Use These

| Fixture | Creates | Use Case |
|---------|---------|----------|
| `test_user` | CustomUser | Standard authenticated user |
| `user_email` | str | Email for test users |
| `user_password` | str | Auto-dependency of `test_user` |
| `authenticated_client` | Client (logged in) | Auth-required views |
| `contact_allergen` | Allergen (SLS, contact) | Contact/topical allergen |
| `food_allergen` | Allergen (Peanut, food) | Food allergen |
| `user_allergy` | UserAllergy (confirmed, moderate) | Linked user → allergen |
| `unconfirmed_user_allergy` | UserAllergy (defaults) | Tests requiring unconfirmed state |

### ⚠️ Deprecated — Do Not Use in New Tests

| Old Name | Replace With |
|----------|-------------|
| `custom_user` | `test_user` |
| `allergen_contact` | `contact_allergen` |
| `allergen_food` | `food_allergen` |

### Fixture Implementations

Canonical definitions from `conftest.py`. If the source file differs from these,
the source file is the authority — update this doc to match.

```python
@pytest.fixture
def user_email() -> str:
    return "test@example.com"

@pytest.fixture
def user_password() -> str:
    return "SecurePassword123!"

@pytest.fixture
def test_user(db, user_email: str, user_password: str):
    return User.objects.create_user(
        email=user_email,
        username="testuser",
        password=user_password,
    )

@pytest.fixture
def authenticated_client(client, test_user, user_password: str):
    client.login(email=test_user.email, password=user_password)
    return client

@pytest.fixture
def contact_allergen(db):
    """Sodium Lauryl Sulfate (SLS) — contact/topical category."""
    return Allergen.objects.create(
        category=CATEGORY_CONTACT,
        allergen_key="sls",
        is_active=True,
    )

@pytest.fixture
def food_allergen(db):
    """Peanut — food category."""
    return Allergen.objects.create(
        category=CATEGORY_FOOD,
        allergen_key="peanut",
        is_active=True,
    )

@pytest.fixture
def user_allergy(db, test_user, contact_allergen):
    """Confirmed UserAllergy linking test_user → contact_allergen."""
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
        severity_level="moderate",
        is_confirmed=True,
    )

@pytest.fixture
def unconfirmed_user_allergy(db, test_user, contact_allergen):
    """UserAllergy using model defaults — is_confirmed=False, severity_level=''."""
    return UserAllergy.objects.create(
        user=test_user,
        allergen=contact_allergen,
    )
```

---

## Test Patterns

### Naming Convention

Format: `test_<action>_<expected_result>`

```python
# ✅ Good
def test_create_user_allergy_with_duplicate_allergen_raises_validation_error(...)
def test_authenticated_user_sees_only_own_allergies(...)
def test_allergen_str_includes_category_and_name(...)

# ❌ Bad
def test_allergy(...)
def test_view(...)
def test_model_1(...)
```

### Model Tests

Test creation, `__str__`, `clean()` validation, `save()` override, constraints,
and properties. Test public behaviour — never test private/internal state.

```python
@pytest.mark.django_db
class TestAllergenModel:
    def test_str_representation(self, contact_allergen, food_allergen):
        assert str(contact_allergen) == "Contact/Topical Allergens: Sodium Lauryl Sulfate (SLS)"
        assert str(food_allergen) == "Food Allergens: Peanut"

    def test_allergen_label_property(self, contact_allergen):
        assert contact_allergen.allergen_label == "Sodium Lauryl Sulfate (SLS)"

    def test_category_to_allergens_map_contains_expected_keys(self):
        """Verify CATEGORY_TO_ALLERGENS_MAP is complete for both fixture allergens."""
        assert ("sls", "Sodium Lauryl Sulfate (SLS)") in CATEGORY_TO_ALLERGENS_MAP[CATEGORY_CONTACT]
        assert ("peanut", "Peanut") in CATEGORY_TO_ALLERGENS_MAP[CATEGORY_FOOD]

    def test_create_allergy_sets_correct_attributes(self, test_user, contact_allergen):
        allergy = UserAllergy.objects.create(
            user=test_user,
            allergen=contact_allergen,
            severity_level="moderate",
            is_confirmed=True,
        )
        assert allergy.user == test_user
        assert allergy.allergen == contact_allergen
        assert allergy.severity_level == "moderate"
        assert allergy.is_confirmed is True

    def test_duplicate_user_allergen_raises_validation_error(self, user_allergy, test_user, contact_allergen):
        """UniqueConstraint (user, allergen) must surface as ValidationError, not IntegrityError."""
        duplicate = UserAllergy(user=test_user, allergen=contact_allergen)
        with pytest.raises(ValidationError):
            duplicate.full_clean()


@pytest.mark.django_db
class TestUserAllergyClean:
    def test_future_onset_date_rejected(self, user_allergy):
        from datetime import date, timedelta
        user_allergy.symptom_onset_date = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError, match="cannot be in the future"):
            user_allergy.full_clean()

    def test_unknown_reaction_key_rejected(self, user_allergy):
        user_allergy.user_reaction_details = {"unknown_key": "value"}
        with pytest.raises(ValidationError, match="Unknown keys"):
            user_allergy.full_clean()

    def test_unknown_admin_notes_key_rejected(self, user_allergy):
        user_allergy.admin_notes = {"rogue_field": "value"}
        with pytest.raises(ValidationError, match="Unknown keys"):
            user_allergy.full_clean()

    def test_valid_reaction_details_accepted(self, user_allergy):
        user_allergy.user_reaction_details = {
            "symptom": "rash", "severity": "mild", "date": "2024-01-01"
        }
        user_allergy.full_clean()  # must not raise
```

### View Tests

Cover: unauthenticated redirect, authenticated GET (status + template + context),
POST valid (redirect + object created), POST invalid (re-renders with errors).

```python
@pytest.mark.django_db
class TestAllergiesListView:
    def test_unauthenticated_redirects_to_login(self, client):
        response = client.get(reverse("allergies:list"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_access_renders_correct_template(self, authenticated_client):
        response = authenticated_client.get(reverse("allergies:list"))
        assert response.status_code == 200
        assert "allergies/allergies_list.html" in [t.name for t in response.templates]

    def test_user_sees_own_allergies_in_context(self, authenticated_client, test_user, contact_allergen):
        UserAllergy.objects.create(user=test_user, allergen=contact_allergen)
        response = authenticated_client.get(reverse("allergies:list"))
        assert contact_allergen.allergen_label in response.content.decode()

    def test_post_creates_allergy_and_redirects(self, authenticated_client, test_user, contact_allergen):
        data = {"allergen": contact_allergen.id, "severity_level": "moderate", "is_confirmed": True}
        response = authenticated_client.post(reverse("allergy_create"), data=data)
        assert response.status_code == 302
        assert UserAllergy.objects.filter(user=test_user, allergen=contact_allergen).exists()
```

### Error Handling Tests

```python
@pytest.mark.django_db
class TestErrorHandling:
    def test_duplicate_allergy_returns_400_not_500(
        self, authenticated_client, test_user, contact_allergen
    ):
        """Duplicate UserAllergy must surface as a 400, not an unhandled IntegrityError."""
        UserAllergy.objects.create(user=test_user, allergen=contact_allergen)
        data = {"allergen": contact_allergen.id, "severity_level": "mild", "is_confirmed": False}
        response = authenticated_client.post(reverse("allergy_create"), data=data)
        assert response.status_code == 400
        assert "already exists" in response.content.decode().lower()
```

### Integration Tests

```python
@pytest.mark.integration
@pytest.mark.django_db
def test_user_allergy_cascade_delete(test_user, contact_allergen):
    """UserAllergy must be deleted when the owning user is deleted (CASCADE)."""
    UserAllergy.objects.create(user=test_user, allergen=contact_allergen)
    user_id = test_user.id
    test_user.delete()
    assert not UserAllergy.objects.filter(user_id=user_id).exists()
```

### Admin Action Tests

```python
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
            password="admin123",
        )

    def _make_request(self):
        """Minimal admin request with session and messages support."""
        request = self.factory.get("/")
        request.user = self.superuser
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        return request

    def test_deactivate_allergens_deactivates_and_logs(
        self, caplog, contact_allergen, food_allergen
    ):
        queryset = Allergen.objects.filter(id__in=[contact_allergen.id, food_allergen.id])
        with caplog.at_level("INFO", logger="allergies.admin"):
            self.admin.deactivate_allergens(self._make_request(), queryset)

        contact_allergen.refresh_from_db()
        food_allergen.refresh_from_db()
        assert not contact_allergen.is_active
        assert not food_allergen.is_active
        assert "deactivating 2 allergens" in caplog.text.lower()
```

---

## Common Pitfalls

### ❌ Testing Internal State

```python
# ❌ Bad — tests a private implementation detail
def test_allergen_internal_cache():
    assert allergen._cached_label is None

# ✅ Good — tests the public property
def test_allergen_label_returns_correct_value(contact_allergen):
    assert contact_allergen.allergen_label == "Sodium Lauryl Sulfate (SLS)"
```

### ❌ Vague Assertions

```python
# ❌ Bad — passes even if object is broken
assert allergy

# ✅ Good — verifies what actually matters
assert allergy.severity_level == "moderate"
assert allergy.is_confirmed is True
```

### ❌ Duplicating Fixture Setup

```python
# ❌ Bad — manual setup that duplicates conftest.py
def test_something():
    user = User.objects.create_user(email="test@example.com", ...)
    allergen = Allergen.objects.create(category=CATEGORY_CONTACT, allergen_key="sls")

# ✅ Good — use shared fixtures
def test_something(test_user, contact_allergen):
    ...
```

### ❌ Only Testing Happy Paths

Every new feature must cover:
- ✅ Valid input (happy path)
- ✅ Invalid input (validation errors)
- ✅ Unauthenticated access (redirect to login)
- ✅ Edge cases (empty strings, None, boundary values)

---

## Coverage Configuration Reference

Configured in `pyproject.toml` — these are for reference, not duplication.

| Key | Location | Effect |
|-----|----------|--------|
| `branch = true` | `[tool.coverage.run]` | Tests all control flow paths, not just lines |
| `fail_under = 75` | `[tool.coverage.report]` | Fails test run if overall coverage drops below threshold |
| `omit` | `[tool.coverage.run]` | Excludes migrations, tests, settings from measurement |
| `testpaths` | `[tool.pytest.ini_options]` | `allergies/tests`, `users/tests` |
| `-ra --strict-markers --tb=short` | `[tool.pytest.ini_options]` | Default flags applied to every run |

---

## Troubleshooting

**Coverage below 75% threshold:**
- Bypass temporarily: `uv run pytest --no-cov`
- Lower `fail_under` in `pyproject.toml` while catching up (restore before committing)
- Run `uv run pytest --cov --cov-report=html`, open `htmlcov/index.html` to find uncovered lines

**GitHub checks blocking merge despite local tests passing:**
- Check the **Actions** tab — identify which specific job failed
- Verify both `build` and `test` jobs completed
- Check if `codecov/project` shows a coverage drop
- Codecov comments only appear on PRs from within the repo — forks will not receive a comment; this is expected behaviour, not a failure

**PowerShell execution policy error** (`running scripts is disabled`):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Migrations/app errors on test run:**
```bash
uv run python manage.py showmigrations
uv run python manage.py makemigrations allergies users
uv run python manage.py migrate
```

**`PytestUnknownMarkWarning` or marker not found:**
- Only `unit`, `integration`, and `slow` are registered
- `--strict-markers` is on — any unregistered marker fails the run
- Add new markers to the `markers` list in `[tool.pytest.ini_options]` before using them
