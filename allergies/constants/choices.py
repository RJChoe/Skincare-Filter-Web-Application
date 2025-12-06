# --- Category Definitions ---
# Category Keys (Generic Database values)
CATEGORY_FOOD = 'food'
CATEGORY_CONTACT = 'contact'
CATEGORY_INHALANT = 'inhalant'
CATEGORY_OTHER = 'other' # <-- String Value stored in DB (self.category)

# --- Category Choices (For the Model field) ---
CATEGORY_CHOICES = [
    (CATEGORY_FOOD, 'Food Allergens'),
    (CATEGORY_CONTACT, 'Contact/Topical Allergens'),
    (CATEGORY_INHALANT, 'Inhalant Allergens'),
    (CATEGORY_OTHER, 'Other Allergens'), # <-- Category label (displayed via self.get_category_display())
]

# --- Severity Level Choices (For UserAllergy Model) ---
SEVERITY_CHOICES = [
    ('mild', 'Mild'),
    ('moderate', 'Moderate'),
    ('severe', 'Severe / Anaphylactic'),
]

# --- Source Information Choices (For UserAllergy Model) ---
SOURCE_INFO_CHOICES = [
    ('self_reported', 'Self Reported'),
    ('tested', 'Clinically Tested'),
    ('family_history', 'Family History'),
]

# --- choices/specific allergen lists (Key-Value Pairs for the database) ---
## alphabetical ##

# Acids and exfoliants
ACID_ALLERGENS = [
    ("glycolic_acid", "Glycolic Acid"),
    ("salicylic_acid", "Salicylic Acid"),
    ("lactic_acid", "Lactic Acid"),
    ("citric_acid", "Citric Acid"),
    ("benzoic_acid", "Benzoic Acid"),
    ("sorbic_acid", "Sorbic Acid"),
]

# Botanical/Essential oils
BOTANICAL_ALLERGENS = [
    ("tea_tree_oil", "Tea Tree Oil"),
    ("lavender_oil", "Lavender Oil"),
    ("peppermint_oil", "Peppermint Oil"),
    ("eucalyptus_oil", "Eucalyptus Oil"),
    ("rose_oil", "Rose Oil"),
    ("chamomile", "Chamomile"),
    ("ylang_ylang", "Ylang Ylang"),
    ("sandalwood", "Sandalwood"),
    ("bergamot", "Bergamot Oil"),
    ("lemongrass", "Lemongrass Oil"),
]

# Colorants and dyes
COLORANT_ALLERGENS = [
    ("ci_dyes", "CI Dyes (Color Index)"),
    ("fd_c_dyes", "FD&C Dyes"),
    ("carmine", "Carmine (CI 75470)"),
    ("iron_oxides", "Iron Oxides"),
    ("mica", "Mica"),
]

# Contact/Topical Allergens (example)
CONTACT_ALLERGENS = [
    ("nickel", "Nickel"),
    ("latex", "Latex"),
    ("lanolin", "Lanolin"),
]

DUST_ALLERGENS = [
    ("dust_mite", "Dust Mite"),
    ("mold_spores", "Mold Spores"),
    ("pet_dander", "Pet Dander"),
]

# Fragrance Allergens (based on your example)
FRAGRANCE_ALLERGENS = [
    ("linalool", "Linalool"),
    ("limonene", "Limonene"),
    ("geraniol", "Geraniol"),
    ("citronellol", "Citronellol"),
    ("eugenol", "Eugenol"),
    # ... and so on
]

# Food Allergens (example)
FOOD_ALLERGENS = [
    ("peanut", "Peanut"),
    ("tree_nut", "Tree Nut (General)"),
    ("gluten", "Gluten / Wheat"),
    ("dairy", "Dairy / Milk"),
    ("soy", "Soy"),
    ("shellfish", "Shellfish"),
]

# Other common allergens
OTHER_ALLERGENS = [
    ("retinol", "Retinol/Retinoids"),
    ("vitamin_c", "Vitamin C (L-Ascorbic Acid)"),
    ("niacinamide", "Niacinamide"),
    ("propylene_glycol", "Propylene Glycol"),
    ("butylene_glycol", "Butylene Glycol"),
    ("dimethicone", "Dimethicone"),
    ("tocopherol", "Tocopherol (Vitamin E)"),
    ("alcohol_denat", "Alcohol Denat"),
    ("isopropyl_alcohol", "Isopropyl Alcohol"),
]

# Pollen Allergens
POLLEN_ALLERGENS = [
    ("birch_pollen", "Birch Pollen"),
    ("chrysanthemum","Chrysanthemum"),
    ("goldenrod","Goldenrod"),
    ("grass_pollen", "Grass Pollen"),
    ("humulus_japonicus","Humulus Japonicus"),
    ("lamb's_quarters","Lamb's Quarters"),
    ("mulberry","Mulberry"),
    ("locust","Locust"),
    ("oak_pollen", "Oak Pollen"),
    ("pine","Pine"),
    ("plane_tree","Plane Tree"),
    ("ragweed", "Ragweed Pollen"),
    ("rape","Rape"),
    ("spruce","Spruce"),
    ("tree_pollen", "Tree Pollen"),
    ("queen_palm","Queen Palm"),
]

# Preservatives
PRESERVATIVE_ALLERGENS = [
    ("parabens", "Parabens (Methylparaben, Propylparaben, etc.)"),
    ("formaldehyde", "Formaldehyde"),
    ("formaldehyde_releasers", "Formaldehyde Releasers"),
    ("methylisothiazolinone", "Methylisothiazolinone (MI)"),
    ("methylchloroisothiazolinone", "Methylchloroisothiazolinone (MCI)"),
    ("phenoxyethanol", "Phenoxyethanol"),
    ("benzalkonium_chloride", "Benzalkonium Chloride"),
    ("bronopol", "Bronopol"),
    ("iodopropynyl_butylcarbamate", "Iodopropynyl Butylcarbamate"),
]

# Proteins and extracts
PROTEIN_ALLERGENS = [
    ("collagen", "Collagen"),
    ("keratin", "Keratin"),
    ("silk_protein", "Silk Protein"),
    ("wheat_protein", "Wheat Protein"),
    ("soy_protein", "Soy Protein"),
    ("beeswax", "Beeswax"),
    ("propolis", "Propolis"),
    ("royal_jelly", "Royal Jelly"),
]

# UV filters/Sunscreen ingredients
SUNSCREEN_ALLERGENS = [
    ("oxybenzone", "Oxybenzone (Benzophenone-3)"),
    ("octinoxate", "Octinoxate (Octyl Methoxycinnamate)"),
    ("avobenzone", "Avobenzone"),
    ("octocrylene", "Octocrylene"),
    ("homosalate", "Homosalate"),
    ("titanium_dioxide", "Titanium Dioxide"),
    ("zinc_oxide", "Zinc Oxide"),
]

# Surfactants and emulsifiers
SURFACTANT_ALLERGENS = [
    ("sls", "Sodium Lauryl Sulfate (SLS)"),
    ("sles", "Sodium Laureth Sulfate (SLES)"),
    ("cocamidopropyl_betaine", "Cocamidopropyl Betaine"),
    ("peg_compounds", "PEG Compounds (Polyethylene Glycol)"),
    ("polysorbates", "Polysorbates"),
    ("sodium_lauroyl_sarcosinate", "Sodium Lauroyl Sarcosinate"),
]

# --- The Grouped Choice Constant (Grouping/UI)---
# list of 3-tuples: (database_key, human_readable_label, choice_list)
# useful django form rendering <optgroup> tags
# template iteration (require human readable category label)
# Assuming you have defined the Category Keys (GENERIC_CONTACT, etc.)
# and the Specific Allergen Lists (FRAGRANCE_ALLERGENS, etc.)

# --- Form Grouping for OptGroups (3-tuples) ---
# Structure: (category_key, optgroup_label, choices_list)
FORM_ALLERGIES_CHOICES = [
    # All of these items will be classified as 'contact' in the database
    (CATEGORY_CONTACT, "Acids & Exfoliants", ACID_ALLERGENS),
    (CATEGORY_CONTACT,"Botanicals & Essential Oils", BOTANICAL_ALLERGENS),
    (CATEGORY_CONTACT, "Colorants & Dyes", COLORANT_ALLERGENS),
    (CATEGORY_CONTACT, "General Contact Allergens", CONTACT_ALLERGENS),
    (CATEGORY_CONTACT, "Cosmetic Fragrances", FRAGRANCE_ALLERGENS),
    (CATEGORY_CONTACT, "Cosmetic Preservatives", PRESERVATIVE_ALLERGENS),
    (CATEGORY_CONTACT, "Proteins & Extracts", PROTEIN_ALLERGENS),
    (CATEGORY_CONTACT, "Sunscreen Ingredients", SUNSCREEN_ALLERGENS),
    (CATEGORY_CONTACT, "Surfactants & Emulsifiers", SURFACTANT_ALLERGENS),
    
    # This item will be classified as 'food' in the database
    (CATEGORY_FOOD, "Major Food Allergens", FOOD_ALLERGENS),
    
    # This item will be classified as 'inhalant' in the database
    (CATEGORY_INHALANT, "Environmental Inhalants", DUST_ALLERGENS),
    (CATEGORY_INHALANT, "Pollen Allergens", POLLEN_ALLERGENS),
    
    (CATEGORY_OTHER, "Other General Contact", OTHER_ALLERGENS),
]

# --- Inverse Map (Category -> Specific Choices) ---
# Maps category_key -> list of (specific_key, specific_label)

def build_category_to_allergens_map(form_allergies_choices):
    category_allergen_map = {}
    for category_key, optgroup_label, choice_list in form_allergies_choices:
        # Use .setdefault() to ensure the list exists before extending it
        category_allergen_map.setdefault(category_key, []).extend(choice_list)
    return category_allergen_map

CATEGORY_TO_ALLERGENS_MAP = build_category_to_allergens_map(FORM_ALLERGIES_CHOICES)

# Now, CATEGORY_TO_ALLERGENS_MAP looks like:
# {
#    'contact': [('glycolic_acid', 'Glycolic Acid'), ('tea_tree_oil', 'Tea Tree Oil'), ...],
#    'food': [('peanut', 'Peanut'), ('tree_nut', 'Tree Nut (General)'), ...],
#    ...
# }


# --- Pre-calculate a flat map for efficient lookups ---
# Maps specific allergen_key -> human_readable_label across ALL categories.
def build_flat_allergen_label_map(category_to_allergens_map):
    """
    Creates a single dictionary mapping all allergen keys (e.g., 'peanut') 
    to their labels (e.g., 'Peanut'), optimized for __str__ lookups.
    """
    flat_map = {}
    
    # Iterate through the values of the category map (which are lists of (key, label) tuples)
    for allergen_list in category_to_allergens_map.values():
        # Update the flat_map with the tuples from the list. 
        # Since dict() can take a list of tuples, this is a clean way to merge.
        # Note: If keys are duplicated across categories, the last one processed wins.
        flat_map.update(dict(allergen_list))
        
    return flat_map

# This dictionary is created once when the module is loaded.
FLAT_ALLERGEN_LABEL_MAP = build_flat_allergen_label_map(CATEGORY_TO_ALLERGENS_MAP)

# FLAT_ALLERGEN_LABEL_MAP now looks like:
# {
#     'glycolic_acid': 'Glycolic Acid',
#     'tea_tree_oil': 'Tea Tree Oil',
#     'peanut': 'Peanut',
#     'linalool': 'Linalool',
#     # ... every single allergen key is mapped to its label
# }