"""Django models for the allergies app.

Defines:
- Allergen: Pre-defined catalog of allergens/ingredients
- UserAllergy: Junction model linking users to their allergens
"""

from typing import Any

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .constants.compounds import (
    CATEGORY_CHOICES,
    CATEGORY_CONTACT,
    FLAT_ALLERGEN_LABEL_MAP,
)

# Python 3.13 type aliases (PEP 695) — used as return/parameter annotations
# in forms.py and views.py, not on the field declarations themselves
# (django-stubs does not support freeform JSONField body annotations).
type ReactionDetails = dict[str, str | list[str] | None]
type AdminNotes = dict[str, str | int | None]


class Allergen(models.Model):
    """Pre-defined catalog of allergens/ingredients.
    Admins can manage this list, users select from it.

    allergen_key is the canonical identifier for this compound.
    A planned AllergenAlias model will map many alternate names
    (INCI names, common names, abbreviations) to this key.

    Do not treat allergen_key as a display value —
    use allergen_label for display and
    allergen_key as the stable matching target.
    """

    # Primary Selection: broad category (user selects first)
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CONTACT,
        db_index=True,
        help_text="Generic allergen category",
    )

    # Secondary Selection: specific allergen/ingredient KEY
    # (filtered dynamically based on category)
    allergen_key = models.CharField(
        max_length=50,
        choices=[],
        blank=False,
        null=False,
        db_index=True,
        help_text=("Specific allergen (choices filtered via category)"),
    )

    is_active = models.BooleanField(
        default=True,
        db_index=False,
        help_text=("Inactive allergens won't be shown in user selection"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "allergen_key"],
                name="uniq_category_allergen",
            ),
        ]
        indexes = [
            models.Index(
                fields=["category", "is_active"],
                name="allergen_cat_active_idx",
            ),
        ]
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"
        ordering = ["category", "allergen_key"]

    def __str__(self) -> str:
        """Display as 'Category: Allergen Label'."""
        category_display = self.get_category_display()

        if self.allergen_key:
            allergen_label = FLAT_ALLERGEN_LABEL_MAP.get(
                self.allergen_key, self.allergen_key
            )
            return f"{category_display}: {allergen_label}"
        return f"{category_display}: [No Allergen Selected]"

    @property
    def allergen_label(self) -> str:
        """Return user-friendly label for this allergen."""
        if not self.allergen_key:
            # Keep behavior consistent with __str__ by never returning None
            return ""
        return FLAT_ALLERGEN_LABEL_MAP.get(
            self.allergen_key,
            self.allergen_key,
        )


class UserAllergy(models.Model):
    """Junction model linking a CustomUser to an Allergen.
    Represents a user's specific allergy selection.
    """

    class SeverityLevel(models.TextChoices):
        MILD = "mild", "Mild"
        MODERATE = "moderate", "Moderate"
        SEVERE = "severe", "Severe"
        LIFE_THREATENING = "life_threatening", "Life-Threatening"

    class SourceInfo(models.TextChoices):
        SELF_REPORTED = "self_reported", "Self-Reported"
        MEDICAL_PROFESSIONAL = "medical_professional", "Medical Professional"
        ALLERGY_TEST = "allergy_test", "Formal Allergy Test"
        FAMILY_HISTORY = "family_history", "Family History"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_allergies",
        help_text="The user who has this allergy",
    )

    allergen = models.ForeignKey(
        Allergen,
        on_delete=models.CASCADE,
        related_name="user_allergy_entries",
        help_text="The allergen this user is allergic to",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    severity_level = models.CharField(
        max_length=20,
        choices=SeverityLevel.choices,
        blank=True,
        default="",
        help_text="Optional severity level of the allergy",
    )

    is_confirmed = models.BooleanField(
        default=False,
        # No standalone index — covered by user_allergy_user_idx and user_allergy_alrgn_idx
        help_text="Clinically confirmed: True/False",
    )

    symptom_onset_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date when symptoms first appeared",
    )

    source_info = models.CharField(
        max_length=20,
        choices=SourceInfo.choices,
        blank=True,
        default="",
        help_text="Source of allergy information",
    )

    user_reaction_details = models.JSONField(
        default=dict,
        blank=True,
        help_text=("Past reactions: {symptom: str, severity: str, date: str}"),
    )

    admin_notes = models.JSONField(
        default=dict,
        blank=True,
        help_text=("Internal notes: {verified_by: str, verification_date: str}"),
    )

    is_active = models.BooleanField(
        default=True,
        # No standalone index — covered by user_allergy_user_idx and user_allergy_alrgn_idx
        help_text=("Inactive user allergies won't be considered in assessments"),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "allergen"],
                name="uniq_user_allergen",
            ),
        ]
        indexes = [
            models.Index(
                fields=["user", "is_active"],
                name="user_allergy_user_idx",
            ),
            models.Index(
                fields=["allergen", "is_active"],
                name="user_allergy_alrgn_idx",
            ),
            models.Index(
                fields=["is_confirmed", "is_active"],
                name="user_allergy_conf_idx",
            ),
        ]
        verbose_name = "User Allergy"
        verbose_name_plural = "User Allergies"
        ordering = [
            "user",
            "allergen__category",
            "allergen__allergen_key",
        ]

    def __str__(self) -> str:
        # Requires select_related('user', 'allergen') to avoid N+1 queries
        return f"{self.user.username} - {self.allergen}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to ensure validation always runs.
        Guarantees data integrity regardless of save method.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if self.symptom_onset_date and self.symptom_onset_date > timezone.now().date():
            raise ValidationError(
                {"symptom_onset_date": "Symptom onset date cannot be in the future"}
            )

        # Guard JSONField structure — reject unknown keys per the canonical schema
        allowed_reaction_keys = {"symptom", "severity", "date"}
        if self.user_reaction_details:
            unknown = self.user_reaction_details.keys() - allowed_reaction_keys
            if unknown:
                raise ValidationError(
                    {"user_reaction_details": f"Unknown keys: {sorted(unknown)}"}
                )
        allowed_admin_keys = {"verified_by", "verification_date"}
        if self.admin_notes:
            unknown = self.admin_notes.keys() - allowed_admin_keys
            if unknown:
                raise ValidationError(
                    {"admin_notes": f"Unknown keys: {sorted(unknown)}"}
                )
