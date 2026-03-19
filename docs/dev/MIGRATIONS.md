# Migration Workflow

## Rules

- **Always pass `--name`** to makemigrations — This applies to both allergies/ and users/ apps (including --merge output). The enforce-migration-naming pre-commit hook (Stage 7) rejects auto-generated names matching `^\d{4}_auto_\d+\.py$` and will block any commit that doesn't follow this naming convention.
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

# For users app model changes:
uv run python manage.py makemigrations users --name add_field_to_customuser

# Review the generated file in <app>/migrations/ before committing

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

Status: ⚠️ BLOCKED Data migrations for the allergen catalog are currently blocked by incomplete choice lists.

See [STATUS.md](../../STATUS.md) → Known Gaps (Item 6) for the current resolution status of `choices.py` stubs.

**WARNING**
Do not run seeding migrations until the stubs in allergies/constants/choices.py are fully resolved. Running this against incomplete lists will result in a partial catalog without triggering a validation error.

1. Finish writing your model tests and run `uv run pytest`. All tests must pass.
2. Create the data migration: `uv run python manage.py makemigrations --empty allergies --name seed_allergens`
3. Edit the generated file, then run `uv run python manage.py migrate`.

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
    Allergen = apps.get_model("allergies", "Allergen")
    from allergies.constants.choices import FORM_ALLERGIES_CHOICES
    seeded_keys = [key for _, _, choices in FORM_ALLERGIES_CHOICES for key, _ in choices]
    Allergen.objects.filter(allergen_key__in=seeded_keys).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("allergies", "0001_initial"),  # always check: uv run python manage.py showmigrations
    ]
    operations = [
        migrations.RunPython(seed_allergens, reverse_seed),
    ]
```
## Data Migrations Involving `UserAllergy`

`UserAllergy.save()` always calls `full_clean()`. Any data migration that creates
or updates `UserAllergy` rows must bypass the `save()` method to avoid triggering
these internal validations.

### Permitted Methods

To successfully bypass `full_clean()`, use only the following:

For updates: use `queryset.update(**kwargs)`.

For creation: use `Model.objects.bulk_create([objs])`. Do not use
`Model.objects.create()`, as it internally calls `.save()` and will trigger validation.

### Data Constraints

When bypassing validation, you are responsible for ensuring data conforms
to the following canonical JSONField keys:

- `user_reaction_details`: `symptom`, `severity`, `date` — no other keys.
- `admin_notes`: `verified_by`, `verification_date` — no other keys.
- `symptom_onset_date`: must not be a future date.

**IMPORTANT**
Use `bulk_create(objs, ignore_conflicts=False)` for seeding to ensure that
genuine integrity errors (like unique constraint violations) are still caught
while bypassing the `save()`-based validation logic.

## Rollback

```bash
# allergies app
uv run python manage.py migrate allergies zero           # Full rollback
uv run python manage.py migrate allergies 0001_initial   # To specific migration

# users app
uv run python manage.py migrate users zero               # Full rollback
uv run python manage.py migrate users 0001_initial       # To specific migration

uv run python manage.py migrate --plan                   # Dry-run preview (either app)
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
uv run python manage.py makemigrations --merge --name merge_<description>  # Auto-merge if possible
uv run python manage.py migrate                 # Verify
```
