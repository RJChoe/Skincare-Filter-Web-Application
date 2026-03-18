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

## GDPR Note

Admin actions that touch user data must log only `request.user.id` — never
email addresses or usernames. See [LOGGING.md](LOGGING.md).
