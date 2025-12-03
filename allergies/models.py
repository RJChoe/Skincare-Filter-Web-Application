from django.db import models
from django.contrib.auth.models import User
from .constants.choices import (
CATEGORY_CHOICES,
CATEGORY_OTHER,
CATEGORY_TO_ALLERGENS_MAP,
)

##CATEGORY_CHOICES define single field on Django model
## use: category field on AllergenExposure model
## structure: flat list of 2-tuples (database_key, human_label)
## database value: database_key (e.g., 'food', 'fragrance', 'other') saved to database
## purpose: categorize AllergenExposure model objects themselves

# Allergy model
# User model (Django's built-in User)
# UserAllergy model to link users to their allergies)
class AllergenExposure(models.Model):
    """
    Pre-defined list of common allergens/ingredients.
    Admins can manage this list, users select from it.
    """
    # 1. Primary Selection: The broad category (User selects this first)   
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES, #e.g., food, contact, inhalant
        default=CATEGORY_OTHER,
        help_text = 'Generic category of allergen'
    )
    
    # 2. Secondary Selection: The specific allergen/ingredient
    # selected based on the category chosen above
    allergen_name = models.CharField(
        max_length=50,
        choices=[],  # Choices will be dynamically set in forms
        blank=True,
        null=True,
        help_text='Specific allergen (choices filtered via category)'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive allergies won't be shown in user selection"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Allergy"
        verbose_name_plural = "Allergies"
        ordering = ['category', 'allergen_name']

    def __str__(self):
        if self.allergen_name:
            label_map = dict(CATEGORY_TO_ALLERGENS_MAP.get(self.category, []))
            allergen_label = label_map.get(self.allergen_name, self.allergen_name)
            return f"{self.get_category_display()} - {allergen_label}"
        else:
            return f"{self.get_category_display()}"

class UserAllergy(models.Model):
    """
    Links users to their selected allergies from the pre-defined list.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='user_allergies'
    )
    allergen_exposure = models.ForeignKey(
        AllergenExposure,
        on_delete=models.CASCADE,
        related_name='affected_users'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Allergy"
        verbose_name_plural = "User Allergies"
        unique_together = ['user', 'allergen_exposure']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.allergen_exposure.allergen_name}"
