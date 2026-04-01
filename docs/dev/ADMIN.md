# Admin Customisation Patterns

> Reference implementations: `allergies/admin.py` and `users/admin.py`.

## Checklist for Every New ModelAdmin

- [ ] `list_select_related` set for any FK in `list_display`
- [ ] `created_at`, `updated_at` in `readonly_fields`
- [ ] Module-level logger present (Gate 2 requirement — see [LOGGING.md](LOGGING.md))
- [ ] All custom actions log at INFO level

## N+1 Prevention

```python
class UserAllergyAdmin(admin.ModelAdmin):
    list_display = ["user", "allergen", "severity_level", "is_active"]
    list_select_related = ["user", "allergen"]  # one query, not N+1
    readonly_fields = ["created_at", "updated_at"]
```

## Fieldsets

Group related fields so the admin form is readable:

```python
fieldsets = [
    (None, {"fields": ["user", "allergen"]}),
    ("Severity & Confirmation", {"fields": ["severity_level", "is_confirmed", "source_info"]}),
    ("Details", {"fields": ["symptom_onset_date", "user_reaction_details"]}),
    ("Admin", {"fields": ["admin_notes", "is_active"]}),
    ("Audit", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
]
```

## Custom Actions

All bulk actions must log before mutating and use `exc_info=True` on errors:

```python
import logging
logger = logging.getLogger(__name__)

@admin.action(description="Deactivate selected allergens")
def deactivate_allergens(modeladmin, request, queryset):
    count = queryset.count()
    logger.info("Admin %s deactivating %s allergens", request.user.id, count)
    queryset.update(is_active=False)
    modeladmin.message_user(request, f"{count} allergen(s) deactivated.")

@admin.action(description="Activate selected allergens")
def activate_allergens(modeladmin, request, queryset):
    count = queryset.count()
    logger.info("Admin %s activating %s allergens", request.user.id, count)
    queryset.update(is_active=True)
    modeladmin.message_user(request, f"{count} allergen(s) activated.")
```

## Search & Filtering

```python
class AllergenAdmin(admin.ModelAdmin):
    list_display = ["allergen_label", "category", "allergen_key", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["allergen_key"]
    ordering = ["category", "allergen_key"]
    actions = [deactivate_allergens, activate_allergens]
```

## ⚠️ Admin is Seed-Only Until Gate 4

Adding a novel `allergen_key` via the admin panel will create a database row
but the allergen **will not appear** in:
- `FLAT_ALLERGEN_LABEL_MAP` (used by `Allergen.__str__` and `allergen_label`)
- `CATEGORY_TO_ALLERGENS_MAP` (used by form rendering)
- `FORM_ALLERGIES_CHOICES` (used by the user-facing allergy selection form)

These maps are built from static tuples in `compounds.py` at import time, not
from the database. Any key not in those tuples will display its raw key string
instead of a human-readable label, and will be invisible to users in the form.

**Until the seed migration lands and the display layer is database-driven,
treat this admin as seed-only.** Use it to manage the seeded catalog
(activate/deactivate, audit), not to introduce new allergen keys.

This gap closes automatically when:
1. `Allergen.label` field is added in the seed migration
2. `__str__` and `allergen_label` switch to `self.label`
3. Form choices are queried from the DB instead of `compounds.py`

## GDPR Note

Admin actions that touch user data must log only `request.user.id` — never
email addresses or usernames. See [LOGGING.md](LOGGING.md).
