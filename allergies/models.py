from django.conf import settings #links CustomUser model
from django.db import models
from .constants.choices import (
CATEGORY_CHOICES,
CATEGORY_OTHER,
FLAT_ALLERGEN_LABEL_MAP,
SEVERITY_CHOICES,
SOURCE_INFO_CHOICES,
)

# Allergen model (the allergen catalog in allergies app)
# CustomUser model (in users app, extends Django User model)
# UserAllergy model to link users to their allergies)

##CATEGORY_CHOICES define single field on Django model
## use: category field on AllergenExposure model
## structure: flat list of 2-tuples (database_key, human_label)
## database value: database_key (e.g., 'food', 'fragrance', 'other') saved to database
## purpose: categorize AllergenExposure model objects themselves
class Allergen(models.Model):
    """
    Pre-defined catalog of allergens/ingredients.
    Admins can manage this list, users select from it.
    """
    # Primary Selection: The broad category (User selects this first)   
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
        db_index=True,
        help_text='Generic allergen category',
    )
    
    # Secondary Selection: The specific allergen/ingredient KEY
    # selected based on the category chosen above
    allergen_key = models.CharField(
        max_length=50,
        choices=[],
        # leave choices=[] because the choices are category-dependent 
        # and are filtered dynamically in the forms.
        blank=False,
        null=False,
        db_index=True,
        help_text='Specific allergen (choices filtered via category)',
    )
    
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Inactive allergies won't be shown in user selection",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'allergen_key'],
                name='uniq_category_allergen',
            ),
        ]
        indexes = [
            models.Index(
                fields=['category', 'is_active'],
                name='allergen_cat_active_idx'),
        ]
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"
        ordering = ['category', 'allergen_key']
        
    def __str__(self):
        # Display as "Category: Allergen Label"
        category_display = self.get_category_display()
        
        if self.allergen_key:
            allergen_label = FLAT_ALLERGEN_LABEL_MAP.get(self.allergen_key, self.allergen_key)

            return f"{category_display}: {allergen_label}"
        else:
            return f"{category_display}: [No Allergen Selected]"

class UserAllergy(models.Model):
    """
    Junction model linking a CustomUser to an Allergen from the catalog.
    Represents a user's specific allergy selection.
    1-to-Many relationship: One user can have many allergens.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # <-- correct link to custom user model
        on_delete=models.CASCADE,
        related_name='allergic_users',
        help_text='The user who has this allergy',
    )
    
    allergen = models.ForeignKey(
        Allergen,
        on_delete=models.CASCADE,
        related_name='user_allergens',
        help_text='The allergen this user is allergic to',
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    severity_level = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        blank=True,
        null=True,
        help_text='Optional severity level of the allergy',
    )
    
    is_confirmed = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Clinically confirmed: True/False',
    
    )
    
    symptom_onset_date = models.DateField(
        blank=True,
        null=True,
        help_text='Date when symptoms first appeared',
    )
    # The default form widget for this field is a DateInput.
    # The admin adds a JavaScript calendar, and a shortcut for “Today”.
    # Includes an additional invalid_date error message key.
    
    source_info = models.CharField(
        max_length=20,
        choices=SOURCE_INFO_CHOICES,
        blank=True,
        null=True,
        help_text='Source of allergy information',
    )
    
    user_reaction_details = models.JSONField(
        default=dict,
        blank=True,
        help_text='Detailed past reaction information in JSON format',
    )
    
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Inactive user allergies won't be considered in assessments",
    )
    
    # internal tracking, verification, follow-up notes, etc.
    admin_notes = models.JSONField(
        default=dict,
        blank=True,
        help_text='Administrative notes in JSON format',
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'allergen'],
                name='uniq_user_allergen',
            ),
        ]
        indexes = [
            models.Index(fields=['user', 'is_active'], name='userallergy_user_active_idx'),
            models.Index(fields=['allergen', 'is_active'], name='userallergy_allergen_active_idx'),
            models.Index(fields=['is_confirmed', 'is_active'], name='userallergy_confirmed_active_idx'),
        ]
        verbose_name = "User Allergy"
        verbose_name_plural = "User Allergies"
        ordering = ['user', 'allergen__category', 'allergen__allergen_key']
        # double-underscore (__) to follow the Foreign Key relationship
        # and order by fields in the linked Allergen model

    def __str__(self):
        return f"{self.user.username} - {self.allergen}"
    
    def clean(self):
        """
        Validate that the allergen being linked is active.

        Raises:
            ValidationError: If attempting to link to an inactive allergen.
        """
        from django.core.exceptions import ValidationError
        if self.allergen and not self.allergen.is_active:
            raise ValidationError("Cannot link to an inactive allergen.")
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure validation always runs.
        Guarantees data integrity regardless of how to object is saved (admin, form, script).
        """
        self.full_clean()
        super().save(*args, **kwargs)