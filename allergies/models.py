from django.conf import settings #links CustomUser model
from django.db import models
from .constants.choices import (
CATEGORY_CHOICES,
CATEGORY_OTHER,
FLAT_ALLERGEN_LABEL_MAP,
)

##CATEGORY_CHOICES define single field on Django model
## use: category field on AllergenExposure model
## structure: flat list of 2-tuples (database_key, human_label)
## database value: database_key (e.g., 'food', 'fragrance', 'other') saved to database
## purpose: categorize AllergenExposure model objects themselves

# Allergen model (the allergen catalog in allergies app)
# CustomUser model (in users app, extends Django User model)
# UserAllergy model to link users to their allergies)
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
        help_text="Inactive allergies won't be shown in user selection",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'allergen_name'],
                name='uniq_category_allergen',
            ),
        ]
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"
        ordering = ['category', 'allergen_name']
        
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
        related_name='user_allergies',
        help_text='The user who has this allergy',
    )
    
    allergen = models.ForeignKey(
        Allergen,
        on_delete=models.CASCADE,
        related_name='allergen_users',
        help_text='The allergen this user is allergic to',
    )
    noted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'allergen'],
                name='uniq_user_allergen',
            ),
        ]
        verbose_name = "User Allergy"
        verbose_name_plural = "User Allergies"
        ordering = ['user', 'allergen__category', 'allergen__allergen_name']
        # double-underscore (__) to follow the Foreign Key relationship
        # and order by fields in the linked Allergen model

    def __str__(self):
        return f"{self.user.username} - {self.allergen.allergen_name}"
    # self.allergen.allergen_name calls exact data needed from the related table
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.allergen and not self.allergen.is_active:
            raise ValidationError("Cannot link to an inactive allergen.")
   
    # models.py. Keep running python [manage.py](http://_vscodecontentref_/3) check to validate model syntax and imports as you go.