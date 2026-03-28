from allergies.constants.compounds import (
    CATEGORY_CHOICES,
    CATEGORY_CONTACT,
    COMPOUNDS,
    FLAT_ALLERGEN_LABEL_MAP,
    CompoundEntry,
)


def test_compounds_is_non_empty_tuple_of_entries():
    """COMPOUNDS must be a non-empty tuple of CompoundEntry instances."""
    assert isinstance(COMPOUNDS, tuple)
    assert len(COMPOUNDS) > 0
    assert all(isinstance(c, CompoundEntry) for c in COMPOUNDS)


def test_flat_allergen_label_map_is_non_empty():
    """FLAT_ALLERGEN_LABEL_MAP must be a non-empty dict."""
    assert isinstance(FLAT_ALLERGEN_LABEL_MAP, dict)
    assert len(FLAT_ALLERGEN_LABEL_MAP) > 0


def test_category_contact_value():
    """CATEGORY_CONTACT must equal 'contact'."""
    assert CATEGORY_CONTACT == "contact"


def test_category_choices_single_entry():
    """CATEGORY_CHOICES must be a single-entry list containing CATEGORY_CONTACT."""
    assert len(CATEGORY_CHOICES) == 1
    assert CATEGORY_CHOICES[0][0] == CATEGORY_CONTACT
