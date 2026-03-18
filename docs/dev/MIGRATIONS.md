# Migration Workflow

## Rules

- **Always pass `--name`** — auto-generated names like `0004_auto_<timestamp>` are
  rejected at commit time by the `enforce-migration-naming` pre-commit hook.
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

# Confirm
uv run python manage.py showmigrations
```

## Data Migrations (Allergen Catalog Seeding)

⚠️ `allergies/constants/choices.py` must be complete (no `# ... and so on` stubs)
before this migration is written. Check [STATUS.md](../../STATUS.md) → Known Gaps.

```bash
uv run python manage.py makemigrations --empty allergies --name seed_allergens
# Edit the generated file, then:
uv run python manage.py migrate
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
        ("allergies", "0002_initial"),  # adjust to actual latest migration
    ]
    operations = [
        migrations.RunPython(seed_allergens, reverse_seed),
    ]
```

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
# Commit the merge migration
```
