# Skincare Allergy Filter — Product Overview

> **Medical Disclaimer:** This tool is a personal safety aid, not a substitute for professional medical advice. Always consult a dermatologist or allergist for diagnosis and treatment of allergic conditions.

---

## Problem Statement

Reading skincare ingredient labels is time-consuming and error-prone, especially for people managing multiple allergies or sensitivities. Ingredient lists are often long, use unfamiliar chemical names, and vary in formatting between brands — making it easy to miss a known allergen and risk a reaction. Worse, the same ingredient can appear under many different names: "Vitamin C," "L-Ascorbic Acid," and "Ascorbate" all refer to the same compound, but a naive string matcher treats them as unrelated. The Skincare Allergy Filter solves the first problem today — a personal allergen profile checked instantly against any ingredient list — and is being built toward solving the second: an intelligent alias-aware matching engine that catches allergens regardless of how they are labelled on a product.

---

## Target User

People with known skincare sensitivities or allergies who want a fast, reliable second opinion before purchasing or using a product — including those managing conditions such as contact dermatitis, fragrance sensitivity, or food-derived ingredient allergies.

---

## Core User Flows

### 1. Building a Personal Allergen Profile
1. User creates an account and logs in.
2. User navigates to **My Allergies**.
3. User selects allergens from a structured catalog (grouped by category: contact/topical, food-derived, inhalant, and other).
4. For each allergen, the user optionally records:
   - Severity level (Mild / Moderate / Severe / Life-Threatening)
   - How the allergy was identified (self-reported, doctor diagnosed, allergy test, family history)
   - Date symptoms first appeared
   - Notes on past reactions
5. Profile is saved and used for all future product checks.

### 2. Checking a Product's Safety
1. User navigates to **Check a Product**.
2. User pastes or types the product's ingredient list (copied from a label or website).
3. The app sanitizes, tokenizes, and normalizes the input (case-insensitive matching).
4. The app cross-references the ingredient list against the user's active allergen profile.
5. The result is returned immediately:
   - ✅ **Safe** — no allergens detected in the ingredient list.
   - ⚠️ **Unsafe** — one or more allergens found; the offending ingredient(s) are identified by name.

---

## Feature List

### ✅ Built
- Structured allergen catalog with 80+ ingredients across four categories (contact/topical, food, inhalant, other), organized into meaningful groups (fragrances, preservatives, acids, botanicals, sunscreen filters, surfactants, etc.)
- Personal allergen profile: add/remove allergens with severity level, source, reaction history, and confirmation status
- Ingredient list safety check with case-insensitive, whitespace-normalized matching
- "Fail fast" detection — flags a product unsafe at the first allergen match and names the offending ingredient
- Admin panel for managing the allergen catalog (activate/deactivate entries, bulk actions with audit logging)
- User authentication via a custom user model

### 🔄 In Progress
- User-facing forms for creating and editing allergy entries with dynamic allergen selection (category → specific allergen cascading)
- Expanded test coverage for allergy profile CRUD and form validation

### 📋 Planned

**Alias-Aware Matching — the strategic next step**

The current engine matches ingredients by normalized string (case-insensitive, whitespace-stripped). This works well for exact names but cannot detect an allergen when a product uses an alternate INCI name, abbreviation, or common synonym. The planned Synonym Mapper addresses this directly:

- A many-to-one alias system maps every known name for a compound to a single canonical allergen entry (e.g., "Ascorbic Acid," "L-Ascorbic Acid," and "Vitamin C" all resolve to the same allergen record).
- Users profile their allergy once; the engine catches every surface form on a label automatically.
- This transforms the product from a simple string checker into an intelligent ingredient safety tool that handles real-world label variability.

**Additional planned features**
- Product ingredient input form with full POST handling and result display
- User management pages (profile view, edit, list)
- Image/OCR ingredient capture — photograph a product label instead of typing
- Barcode scanning integration for automatic ingredient lookup

---

## Known Limitations

- **Text input only (MVP):** Ingredients must be manually pasted or typed; image and barcode input are not yet supported.
- **Alias matching not yet implemented:** Until the Synonym Mapper ships, a product listing "Ascorbic Acid" will not match a profile entry saved as "Vitamin C." Users should be aware that alternate ingredient names may not be caught in the current version.
- **Catalog scope:** The allergen catalog covers common skincare-relevant allergens. Highly niche or regional ingredients may not appear in the current catalog.
- **No medical validation:** Severity levels and confirmation status are user-reported and are not verified by a medical professional through this tool.
