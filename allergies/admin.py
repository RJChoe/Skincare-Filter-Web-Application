from django.contrib import admin

from .models import Allergen, UserAllergy


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "allergen_key", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("allergen_key",)
    ordering = ("category", "allergen_key")
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Allergen Information", {"fields": ("category", "allergen_key", "is_active")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(UserAllergy)
class UserAllergyAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "allergen",
        "severity_level",
        "is_confirmed",
        "is_active",
        "created_at",
    )
    list_filter = (
        "severity_level",
        "is_confirmed",
        "is_active",
        "source_info",
        "created_at",
    )
    search_fields = ("user__username", "user__email", "allergen__allergen_key")
    ordering = ("user", "allergen__category", "allergen__allergen_key")
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "allergen")

    fieldsets = (
        (
            "User & Allergen",
            {
                "fields": ("user", "allergen"),
            },
        ),
        (
            "Allergy Details",
            {
                "fields": (
                    "severity_level",
                    "is_confirmed",
                    "symptom_onset_date",
                    "source_info",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": ("user_reaction_details", "admin_notes"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    # Date drilldown navigation bar at top of admin list page
    date_hierarchy = "noted_at"


# call above links your database models to the built-in admin interface
# using your specific display rules (list_display, list_filter, etc.)
# "Allergens" and "User Allergies" listed under your application name, ready to manage
