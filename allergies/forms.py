"""Forms for the allergies app.

AllergenSelectForm  — batch allergen selection from the DB catalog
UserAllergyEditForm — edit detail fields on a single UserAllergy row
"""

import logging
from itertools import groupby
from typing import cast

from django import forms

from .models import Allergen, UserAllergy

logger = logging.getLogger(__name__)


class AllergenSelectForm(forms.Form):
    """Batch allergen selection form.

    Renders one checkbox per active Allergen, grouped by subcategory.
    Call get_grouped_allergens() from the view to build template context.
    """

    allergens = forms.ModelMultipleChoiceField(
        queryset=Allergen.objects.filter(is_active=True).order_by(
            "subcategory", "label"
        ),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def get_grouped_allergens(self) -> list[tuple[str, list[Allergen]]]:
        """Return allergens grouped by subcategory for template rendering.

        Returns:
            List of (subcategory_name, [Allergen, ...]) tuples, in subcategory
            order. Relies on the queryset already being ordered by subcategory.
        """
        qs = cast(
            forms.ModelMultipleChoiceField[Allergen], self.fields["allergens"]
        ).queryset
        assert qs is not None
        result: list[tuple[str, list[Allergen]]] = []
        for subcategory, group in groupby(qs, key=lambda a: a.subcategory):
            result.append((subcategory, list(group)))
        return result


class UserAllergyEditForm(forms.ModelForm):
    """Edit detail fields on a single UserAllergy row.

    All fields are optional — users are not required to fill in any detail
    beyond the allergen selection itself (which happens via AllergenSelectForm).
    """

    class Meta:
        model = UserAllergy
        fields = [
            "severity_level",
            "is_confirmed",
            "source_info",
            "symptom_onset_date",
            "user_reaction_details",
        ]
