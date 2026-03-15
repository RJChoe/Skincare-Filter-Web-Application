"""Admin configuration for the users app."""

import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser

# Module-level logger setup
logger = logging.getLogger(__name__)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom admin for CustomUser model."""

    # List View
    list_display = (
        "email",
        "username",
        "get_age",
        "allergy_status_display",
        "date_joined",
        "is_staff",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
        "allergies_updated_at",
    )

    # Search
    search_fields = ("email", "username")
    ordering = ("-date_joined",)

    # Detail View
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "username",
                    "date_of_birth",
                    "age",
                    "bio",
                    "profile_picture",  # YAGNI should remove
                )
            },
        ),
        (
            "Health Data",
            {
                "fields": ("allergies_updated_at",),
                "description": "Automatically updated when allergy information changes.",
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Add User form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("age", "allergies_updated_at", "last_login", "date_joined")

    @admin.display(description="Age")
    def get_age(self, obj):
        """Display user's age in list view."""
        return obj.age if obj.age is not None else "-"

    @admin.display(description="Allergy Profile")
    def allergy_status_display(self, obj):
        """
        Display allergy profile status with visual indicators.

        Shows:
        - Green checkmark if allergies are set
        - Red X if no allergy data
        - The date when last updated (if available)
        """
        if obj.allergies_updated_at:
            # Format: "✓ Jan 15, 2026"
            date_str = obj.allergies_updated_at.strftime("%b %d, %Y")
            return format_html(
                '<span style="color: green;">✓</span> {}',
                date_str,
            )
        else:
            return format_html(
                '<span style="color: red;">✗</span> Not set',
            )
