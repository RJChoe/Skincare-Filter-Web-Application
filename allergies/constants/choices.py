# --- Category Definitions ---
# Catehory Keys (Borad, Database values)
CATEGORY_FOOD = 'food'
CATEGORY_CONTACT = 'contact'
CATEGORY_INHALANT = 'inhalant'
CATEGORY_OTHER = 'other'

# --- 2. Category Choices (For the Model field) ---
CATEGORY_CHOICES = [
    (CATEGORY_FOOD, 'Food Allergens'),
    (CATEGORY_CONTACT, 'Contact/Topical Allergens'),
    (CATEGORY_INHALANT, 'Inhalant Allergens'),
    (CATEGORY_OTHER, 'Other Allergens'), # <-- Category label
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
    ("lanolin", "Lanolin (Wool Alcohol)"),
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

# --- 3. Form Grouping for OptGroups (3-tuples) ---
# Structure: (generic_key, optgroup_label, choices_list)
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