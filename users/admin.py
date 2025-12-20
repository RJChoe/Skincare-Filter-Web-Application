from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for CustomUser model extending Django's UserAdmin.
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "is_superuser", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    # Add date_of_birth to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {"fields": ("date_of_birth",)}),
    )

    # Add date_of_birth to add_fieldsets for user creation
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {"fields": ("date_of_birth",)}),
    )
