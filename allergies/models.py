from django.db import models
from django.contrib.auth.models import User
from .constants.choices import CATEGORY_CHOICES, CATEGORY_OTHER

##CATEGORY_CHOICES define single field on Django model
## use: category field on Allergy model
## structure: flat list of 2-tuples (database_key, human_label)
## database value: database_key (e.g., 'food', 'fragrance', 'other') saved to database
## purpose: categorize Allergy model objects themselves
class Allergy(models.Model):
    """
    Pre-defined list of common allergens/ingredients.
    Admins can manage this list, users select from it.
    """
    
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
    )
    #probably not useful#
    #description = models.TextField(
    #    blank=True, 
    #    null=True,
    #    help_text="Optional description of the allergen"
    #)
    
    #probably not useful#
    #common_names = models.TextField(
    #    blank=True, 
    #    null=True,
    #    help_text="Comma-separated list of alternative names for this allergen (e.g., 'milk, lactose, casein')"
    #)
    
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive allergies won't be shown in user selection"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Allergy"
        verbose_name_plural = "Allergies"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class UserAllergy(models.Model):
    """
    Links users to their selected allergies from the pre-defined list.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='user_allergies'
    )
    allergy = models.ForeignKey(
        Allergy,
        on_delete=models.CASCADE,
        related_name='affected_users'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Allergy"
        verbose_name_plural = "User Allergies"
        unique_together = ['user', 'allergy']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.allergy.name}"
