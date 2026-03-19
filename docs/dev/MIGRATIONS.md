# Migration Workflow

## Rules

- **Always pass `--name`** to makemigrations — This applies to both allergies/ and users/ apps (including --merge output). The enforce-migration-naming pre-commit hook (Stage 7) matches ^(allergies|users)/migrations/ and requires the ^\d{4}_auto_\d+\.py$ format; it will block any commit that doesn't follow this naming convention.
- **Commit model + migration together** — never commit one without the other.
- **After every model change**, remind yourself:
  ```bash
  uv run python manage.py makemigrations allergies --name describe_the_change
  uv run python manage.py migrate
  ```

## Schema Migrations (Model Changes)

```bash
# Create (always name it)
uv run python manage.py makemigrations allergies --name add_severity_to_userallergy

# Review the generated file in allergies/migrations/ before committing

# Apply locally
uv run python manage.py migrate

# If this migration required a new dependency, sync and commit the lockfile
uv sync --group dev
# Then commit pyproject.toml and uv.lock together — the uv-lock pre-commit
# hook will block the commit if they are out of sync.

# Confirm
uv run python manage.py showmigrations
```

### Related Name Change (already applied in `0001_initial`)

The canonical related names as of `0001_initial` are:

- `user.user_allergies` (FK from `UserAllergy` to `CustomUser`)
- `allergen.user_allergy_entries` (FK from `UserAllergy` to `Allergen`)


## Data Migrations (Allergen Catalog Seeding)

⚠️ `allergies/constants/choices.py` must be complete (no `# ... and so on` stubs)
before this migration is written. Check [STATUS.md](../../STATUS.md) → Known Gaps.

⚠️ **Do not write this migration until `choices.py` stubs are fully resolved.**
See [STATUS.md](../../STATUS.md) → Known Gaps. Running this migration against
incomplete choice lists will produce an incomplete allergen catalog with no error.

```bash
# (Blocked) Seed allergen catalog — do not run until choices.py stubs are
# fully resolved. See STATUS.md → Known Gaps.
# uv run python manage.py makemigrations --empty allergies --name seed_allergens
# Edit the generated file, then:
# uv run python manage.py migrate
```

```python
# allergies/migrations/000X_seed_allergens.py
from django.db import migrations


def seed_allergens(apps, schema_editor):
    Allergen = apps.get_model("allergies", "Allergen")
    from allergies.constants.choices import FORM_ALLERGIES_CHOICES

    for category_key, _, choice_list in FORM_ALLERGIES_CHOICES:
        for key, label in choice_list:
            Allergen.objects.get_or_create(
                category=category_key,
                allergen_key=key,
                defaults={"is_active": True},
            )


def reverse_seed(apps, schema_editor):
    apps.get_model("allergies", "Allergen").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("allergies", "0001_initial"),  # always check: uv run python manage.py showmigrations
    ]
    operations = [
        migrations.RunPython(seed_allergens, reverse_seed),
    ]
```
## Data Migrations Involving `UserAllergy`

`UserAllergy.save()` always calls `full_clean()` (see `allergies/models.py`).
Any data migration that creates or updates `UserAllergy` rows **must** use
`Allergen.objects.get_or_create(...)` patterns that bypass `save()`, or must
pass only the canonical JSONField keys:

- `user_reaction_details`: `symptom`, `severity`, `date` — no other keys
- `admin_notes`: `verified_by`, `verification_date` — no other keys
- `symptom_onset_date`: must not be a future date

Use `queryset.update(...)` or direct `Model.objects.create(...)` with validated
data. Never call `.save()` in a data migration without accounting for these
constraints.

You need to know your models work (via tests) before you reliably load data into them.
(Finish writing your tests in tests.py.)

Run `uv run pytest` and ensure all tests pass. Do not use `manage.py test` this project uses pytest exclusively (configured in `pyproject.toml` under `[tool.pytest.ini_options]`).

Then create the data migration file and populate your allergen catalog.

Then run python manage.py migrate Run Migrations: Only after your models are tested and refined do you sync them with the database (makemigrations, migrate).


## Rollback

```bash
uv run python manage.py migrate allergies zero           # Full rollback
uv run python manage.py migrate allergies 0001_initial   # To specific migration
uv run python manage.py migrate --plan                   # Dry-run preview
```

## Fresh Database

```bash
cp db.sqlite3 db.sqlite3.backup   # Always back up first
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

## Conflict Resolution (Team)

```bash
git pull origin main
uv run python manage.py showmigrations          # Identify conflicts
uv run python manage.py makemigrations --merge  # Auto-merge if possible
uv run python manage.py migrate                 # Verify
# - **Always pass `--name`** to `makemigrations` for **both** `allergies` and `users` apps. The `enforce-migration-naming` hook matches `^(allergies|users)/migrations/`.
```
