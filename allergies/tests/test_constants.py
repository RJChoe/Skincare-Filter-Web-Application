from allergies.constants.choices import (
    FORM_ALLERGIES_CHOICES,
    _assert_allergen_keys_unique,
    _assert_allergen_tuples_well_formed,
)


def test_allergen_tuples_are_well_formed():
    """Each group must be a 3-tuple and each choice a 2-tuple of strings.
    A trailing comma in a hand-edited tuple would otherwise cause an
    inscrutable import-time crash.
    """
    _assert_allergen_tuples_well_formed(FORM_ALLERGIES_CHOICES)


def test_allergen_keys_are_unique():
    """Regression: duplicate keys silently overwrite in FLAT_ALLERGEN_LABEL_MAP."""
    _assert_allergen_keys_unique(FORM_ALLERGIES_CHOICES)
