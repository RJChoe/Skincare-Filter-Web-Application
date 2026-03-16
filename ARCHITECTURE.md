# ARCHITECTURE.md — Skincare-Filter-Web-Application

> **Important Version Note:**
> This project uses **Django 6.0** and **Python 3.13**. All code, syntax, and conventions should follow the latest standards for these versions.
> (For example: use `path()` for URL routing, async views, and new ORM features; avoid legacy patterns from Django 4.x or earlier.)

## Product Vision & Purpose
The Skincare Allergy Filter empowers users to make safer skincare choices by checking product ingredient lists against a personal allergen profile. Phase 1 delivers fast, normalized exact matching. Phase 2 — the strategic focus — replaces naive string comparison with an alias-aware Synonym Mapper so that 'Vitamin C', 'L-Ascorbic Acid', and 'Ascorbate' all resolve to the same allergen record regardless of how a brand labels it.
_Disclaimer: This tool is not a substitute for professional medical advice._

## Project Summary
- Django-based web application for allergy filtering.
- Users input their allergens and product ingredient lists.
- The app compares ingredients to allergies and returns a safety alert: “Safe” or “Unsafe.”
- Tech stack: Django 6.0, Python 3.13, SQLite (dev), PostgreSQL (prod), uv for package management.
- See [README.md](./README.md) for a workflow diagram and feature list.

## High-Level Architecture Overview
- **Backend:** Django framework (models, views, admin, migrations)
- **Frontend:** Django templates (`./templates/`), static assets (`./static/`)
- **Database:** SQLite (development), PostgreSQL (production)
- **Apps:** Modular structure with `./allergies/` and `./users/` as main Django apps
- **Configuration:** Managed via `./skincare_project/settings.py` and `.env` (django-environ)

## Main Components & Responsibilities

- **./allergies/**
  - Models: Allergen, UserAllergy
  - Views: Allergy input, ingredient check, safety alert
  - Admin: Manage allergy data
  - Templates: User-facing allergy forms and results
  - **Normalization:**
    - Skincare ingredients often have multiple names (e.g., "Vitamin C" vs. "Ascorbic Acid").
    - The app includes a normalization step in the matching logic: all tokens are converted to lowercase and stripped of whitespace to ensure consistent matching (e.g., "Almond Oil" matches "almond oil").
    - Future enhancements may include synonym mapping and fuzzy matching.

- **./users/**
  - Models: CustomUser
  - Views: User management
  - Signals, validators, admin

- **./skincare_project/**
  - Project settings, URL routing, WSGI/ASGI entry points

- **./templates/**
  - Shared layouts, home, product, user, allergy forms

- **./static/**
  - CSS and JS for UI/UX

## Core Logic: Text-to-Database Flow

**Input Strategy:**
- Users provide raw text input (copy/paste from product websites or manual typing).

**Processing Pipeline:**
1. **Sanitization:** Clean input text (remove special characters, formatting, and whitespace).
2. **Tokenization:** Split text into individual ingredient strings using comma delimiters.
3. **Normalization:** Convert all tokens to lowercase and strip whitespace to ensure consistent matching (e.g., "Almond Oil" matches "almond oil").
4. **Matching:** Cross-reference normalized tokens against the UserAllergen database to determine if any allergens are present.
    - **Note on Future Normalization:** Plan for a "Synonym Mapper" (e.g., Vitamin C → Ascorbic Acid). The system should eventually support many-to-one aliases for ingredients.
5. **Alias Resolution (Planned — Synonym Mapper)**: Before matching, resolve each normalized token against a many-to-one alias table. All known surface forms of a compound (INCI name, common name, abbreviation) map to a single canonical allergen_key. This stage is deliberately separated from normalization so it can be developed, tested, and toggled independently.

**Verdict:**
- “Search & Destroy” Logic: Prioritize the core matching algorithm. The system’s primary goal is rapid identification of blacklisted ingredients. Once an allergen is detected, the process should immediately flag the product as "Unsafe" and identify the offending ingredient.

## Interface: View-to-Template Context Variables

| Template Path                        | Context Variable         | Type            | Description / Example Value                        |
|--------------------------------------|-------------------------|-----------------|---------------------------------------------------|
| `allergies/allergies_list.html`      | `user_allergies`        | List[Allergen]  | Allergens associated with the current user         |
| `allergies/allergies_list.html`      | `ingredient_list`       | List[str]       | Ingredients entered for the product                |
| `allergies/allergies_list.html`      | `is_safe`               | bool            | True if product is safe for user, else False       |
| `users/user_list.html`               | `users`                 | List[User]      | List of all users (admin view)                     |
| `users/user.html`                    | `user`                  | User            | The user being viewed or edited                    |
| `home.html`                          | `form`                  | Form            | Allergy or ingredient input form                   |
| `product.html`                       | `product_ingredients`   | List[str]       | Ingredients for the product being checked          |
| `product.html`                       | `allergy_result`        | str             | "Safe" or "Unsafe" result string                  |

**Notes:**
- `request.user` is always available in templates, but custom user data (like allergies) is passed explicitly as `user_allergies`.
- Do not assume ORM relationships are available in templates unless explicitly passed.
- Update this table as new views/templates are added or context variables change.

## Data Flow & API Contract
- **Frontend/Backend Contract:**
  - Uses Django server-side rendering with HTML templates (no REST API or SPA at present).
  - Data is submitted via standard HTML forms; responses are rendered as new HTML pages.
  - If future API endpoints are added, document them in [API.md](./docs/API.md) (create if needed).

## Third-Party Integrations
- **OCR Engine:** (If used) e.g., Tesseract or Google Vision for ingredient extraction from images.
  - _Note: Specify in this section if/when integrated._
- **Ingredient Databases:** (If used) e.g., INCI or other public ingredient lists.
- **Security/Testing:**
  - [django-environ](https://django-environ.readthedocs.io/) for environment management
  - [pytest](https://docs.pytest.org/) for testing
  - [bandit](https://bandit.readthedocs.io/) for security scanning
  - [safety](https://pyup.io/safety/) for dependency vulnerability checks (advisory-only until Gate 5 — runs in CI but will not block merges)

## Key Design Decisions & ADRs
- **Why Django?**
  - Chosen for rapid development, robust admin, and built-in security features.
- **Why PostgreSQL?**
  - Preferred for production due to reliability, scalability, and Django compatibility.
- **Why server-rendered templates?**
  - Simpler deployment, SEO benefits, and reduced frontend complexity.
- **Testing & Security:**
  - Minimum 50% coverage, environment variables for secrets, CI/CD integration.
- **See [docs/adr/](./docs/adr/)** for detailed Architectural Decision Records (create and expand as needed).

## Scalability & Future-Proofing

**Current State:**
- All processing (including OCR extraction and ingredient parsing) is synchronous, handled within the Django view’s request-response cycle.

**Performance Target:**
- End-to-end processing time (from upload to result) should remain under 3.0 seconds for a typical user request.

**Optimization Strategies:**
- Downscale images on the client or server before OCR to reduce processing time.
- Display a “Processing...” loading state in the UI to manage user expectations during longer operations.

**Decision Trigger — The “Celery” Threshold:**
- If real-world testing shows OCR or ingredient parsing consistently exceeds 5.0 seconds, or if concurrent uploads cause server timeouts, migrate to an asynchronous task queue (e.g., Celery with Redis/RabbitMQ).
- Alias resolution against a large synonym table (e.g., full INCI database) is a second trigger: if lookup latency exceeds 1.0 second per request, move alias resolution to a background pre-computation step or cached lookup layer rather than inline in the request cycle.
- This migration will decouple heavy processing from the main request cycle, improving scalability and user experience.

**Future-Proofing:**
- Monitor processing times and server load as usage grows.
- Document any architectural changes (e.g., Celery integration) in [docs/adr/](./docs/adr/).

---

**Future Considerations:**
- The system is designed to be input-agnostic. While the MVP uses manual text entry, the backend logic expects a standard string, allowing for future integration of OCR or barcode scanning without refactoring the core matching engine.

---

## References to Other Documentation
- [PRODUCT.md](./PRODUCT.md) — User-facing product scope, feature status, known limitations
- [README.md](./README.md) — Project overview, features, workflow diagram
- [.github/instructions/copilot-instructions.md](.github/instructions/copilot-instructions.md) — AI agent instructions, current Gate status, critical field names
- [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) — Production deployment checklist and CI/CD secrets
- [docs/SECURITY.md](./docs/SECURITY.md) — Security best practices and environment variable management
- [docs/TESTING.md](./docs/TESTING.md) — Testing strategy, coverage targets, fixture patterns
- [docs/adr/](./docs/adr/) — Architectural Decision Records (ADRs)

---

**Note:**
This document is intended for use as custom instructions to ground AI agents in the project’s vision, architecture, and conventions. Update as the project evolves.

---
