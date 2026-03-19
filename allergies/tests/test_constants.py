from allergies.constants.choices import (
    FORM_ALLERGIES_CHOICES,
    _assert_allergen_keys_unique,
)


def test_allergen_keys_are_unique():
    """Regression: duplicate keys silently overwrite in FLAT_ALLERGEN_LABEL_MAP."""
    _assert_allergen_keys_unique(FORM_ALLERGIES_CHOICES)
