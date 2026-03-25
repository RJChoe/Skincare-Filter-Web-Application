## 🔴 HARD PROHIBITIONS — READ FIRST

| Prohibited Pattern | Reason | Required Comment | Lift Condition |
|---|---|---|---|
| `async def` view functions | All views are synchronous `def` | `# Future Refactor: async views not yet adopted`| When product safety check requires external API calls |
| `{% partialdef %}` / `{% partial %}` | Template partials not yet adopted | `# Future Refactor: template partials not yet adopted` |When HTMX is formally adopted |
| `django.tasks` / `@task` | Background tasks not yet adopted | `# Future Refactor: background tasks not yet adopted` | When email notifications or scheduled data cleanup are scoped.|
| `pip install` / `python -m pip install` | Always use `uv add` | N/A | Never |
| Python 3.14-only features (T-strings, etc.) | Project targets Python 3.13 | N/A | When `.python-version` is updated to 3.14 |

---

# Copilot Instructions — Skincare Allergy Filter

Django 6.0 · Python 3.13 · SQLite (dev) · `uv` for all package management.

## Read These First

| File | Purpose |
|------|---------|
| [`STATUS.md`](STATUS.md) | **Current gate status and active work items — read before writing any code** |
| [`docs/dev/LOGGING.md`](docs/dev/LOGGING.md) | Gate 2: logging standards and per-file checklist |
| [`docs/dev/FORMS.md`](docs/dev/FORMS.md) | Gate 4: form patterns, dynamic filtering, CSRF |
| [`docs/dev/MIGRATIONS.md`](docs/dev/MIGRATIONS.md) | Migration rules, seeding pattern, rollback |
| [`docs/dev/ADMIN.md`](docs/dev/ADMIN.md) | Admin class patterns, actions, N+1 prevention |
| [`docs/dev/TESTING.md`](docs/dev/TESTING.md) | Fixtures, coverage thresholds, test examples |

## Critical Field Names

**`UserAllergy` fields — use these names exactly:**

| Field | Type | Values / Notes |
|-------|------|---------------|
| `severity_level` | CharField | `mild` `moderate` `severe` `life_threatening` |
| `is_confirmed` | BooleanField | NOT "confirmation" |
| `source_info` | CharField | `self_reported` `medical_professional` `allergy_test` `family_history` |
| `user_reaction_details` | JSONField | Keys: `symptom` `severity` `date` only |
| `admin_notes` | JSONField | Keys: `verified_by` `verification_date` only |
| `symptom_onset_date` | DateField | nullable; cannot be future |

**`Allergen` fields:** `category` · `allergen_key` · `is_active` · `created_at` · `updated_at`
Unique constraint: `(category, allergen_key)`. `allergen_key` has intentional `choices=[]`
in the model — filtering happens in forms, not the model field.

**`allergen_key` naming rule:** the key is the name a cosmetics-literate person would use in conversation, lowercased, and underscored
No apostrophes, hyphens, spaces, or special characters. Example: `birch_pollen` ✅ · `lamb's_quarters` ❌

**Related names:** `user.user_allergies` · `allergen.user_allergy_entries`

**JSONField discipline:** `UserAllergy.clean()` rejects unknown keys. Never invent new ones.
Inventing keys silently corrupts existing data.

## Common Commands

```bash
# Environment
uv sync --group dev
uv add <package>                     # base dep
uv add --group test <package>        # test dep

# Run
uv run python manage.py runserver
uv run python manage.py migrate
uv run python manage.py makemigrations allergies --name <describe_change>

# Quality — run all before committing
uv run pytest --cov --cov-report=term-missing
uv run ruff check . --fix && uv run ruff format .
uv run mypy .
uv run bandit -r allergies users skincare_project
uv run safety scan --non-interactive
```

## Current vs. Future Patterns

### ✅ Use Now

- Synchronous `def` views only
- `{% extends 'layout.html' %}` and `{% include %}` — never `{% partialdef %}`
- `uv` for all package operations — never `pip`
- `list[T]` / `dict[K,V]` / `type` alias syntax (Python 3.13)
- `QuerySet[Allergen]` not bare `QuerySet` (Mypy / django-stubs)
- `pathlib.Path` not `os.path`
- `.select_related('allergen')` on every `UserAllergy` query
- Named URL routes everywhere; `{% url '...' %}` in templates

### ⚠️ Future Only — Not in This Codebase

| Feature | When to Consider |
|---------|-----------------|
| `async def` views | External API / product scanning integration |
| `{% partialdef %}` / `{% partial %}` | If HTMX is adopted |
| `django.tasks` / `@task` | Email notifications, data cleanup |
| Django 6.0 Form Field Groups | Complex multi-section forms |

When a user asks about these: acknowledge the capability, clarify it is not used
here, and recommend the current synchronous/traditional pattern instead.

## Agent Rules

1. **Read `STATUS.md` before writing any code.** Do not start Gate N if Gate N-1 is incomplete.
2. **Verify, don't assume.** Open the actual file and confirm lines exist — use `grep` if needed.
3. **Update `STATUS.md` after completing work** — never update this file for status changes.
4. **Minimal blast radius** — touch only files required; use `.select_related()`; run adjacent tests.
5. **Never mark a gate complete** without running `pytest`, `ruff`, `mypy`, and updating `STATUS.md`.
6. **Stop and ask** if the same CI job fails 3+ times after attempted fixes.
