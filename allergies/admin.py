import logging

from django.contrib import admin, messages

from .models import Allergen, UserAllergy

# Module-level logger setup
logger = logging.getLogger(__name__)


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

    # Custom admin actions with error handling
    actions = ["deactivate_allergens", "activate_allergens"]

    @admin.action(description="Deactivate selected allergens")
    def deactivate_allergens(self, request, queryset):
        """Bulk deactivate allergens with logging and error handling."""
        try:
            count = queryset.count()
            logger.info(f"Admin {request.user.id} deactivating {count} allergens")

            updated = queryset.update(is_active=False)

            logger.info(f"Successfully deactivated {updated} allergens")
            self.message_user(
                request,
                f"Successfully deactivated {updated} allergen(s).",
                messages.SUCCESS,
            )
        except Exception as e:
            logger.error(
                f"Error deactivating allergens by admin {request.user.id}: {e}",
                exc_info=True,
            )
            self.message_user(
                request, f"Error deactivating allergens: {e}", messages.ERROR
            )

    @admin.action(description="Activate selected allergens")
    def activate_allergens(self, request, queryset):
        """Bulk activate allergens with logging and error handling."""
        try:
            count = queryset.count()
            logger.info(f"Admin {request.user.id} activating {count} allergens")

            updated = queryset.update(is_active=True)

            logger.info(f"Successfully activated {updated} allergens")
            self.message_user(
                request,
                f"Successfully activated {updated} allergen(s).",
                messages.SUCCESS,
            )
        except Exception as e:
            logger.error(
                f"Error activating allergens by admin {request.user.id}: {e}",
                exc_info=True,
            )
            self.message_user(
                request, f"Error activating allergens: {e}", messages.ERROR
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
    search_fields = (
        "user__username",
        "user__email",
        "allergen__allergen_key",
    )
    ordering = (
        "user",
        "allergen__category",
        "allergen__allergen_key",
    )
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "allergen")

    fieldsets = (
        ("User & Allergen", {"fields": ("user", "allergen", "is_active")}),
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
    # date_hierarchy adds a date drilldown
    # navigation bar at the top of the
    # admin list page
    date_hierarchy = "noted_at"


# call above links your database
# models to the built-in admin interface
# using your specific display rules
# (list_display, list_filter, etc.)
# "Allergens" and "User Allergies"
# listed under your application name,
# ready to manage
