# Skincare Allergy Filter
[![codecov](https://codecov.io/gh/RJChoe/Skincare-Filter-Web-Application/branch/main/graph/badge.svg)](https://codecov.io/gh/RJChoe/Skincare-Filter-Web-Application)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Disclaimer: This app is a helper tool and not a substitute for professional medical advice. Always consult a dermatologist for severe allergies.

---

## Project Overview
The Skincare Allergy Filter provides an instant safety check by cross-referencing product ingredient lists against a user's personal allergen profile to flag potential sensitivities. The next milestone is the implementation of the Synonym Mapper, an intelligent alias-aware engine designed to resolve the industry-wide problem of ingredient labeling variability by mapping chemical synonyms and EU Annex III 2023 names to single canonical allergens.

---

## ⚙️ Project Workflow Diagram

Diagram flow of data through application represents Phase 1 (exact matching) and Phase 2 (alias resolution) will extend the pipeline.
![Detailed workflow of the application components](./assets/workflow_allergy_filter.png)

---
## Features

### ✅ Built
- **Admin catalog management** — Activate/deactivate allergens, bulk actions with audit logging
- **User authentication** — Account creation and login via a custom user model

### 🔄 In Progress
- **Constants** — database of allergens selected by user via grouped checkbox selection grouped by subcategories (fragrances, preservatives, botanicals, etc.)
- **Personal allergen profile** — Select from a catalog of 80+ ingredients across a single category with subcategory grouping (preservatives, fragrances, botanicals, surfactants, etc.); record severity, source, and reaction history per allergen
- **Ingredient safety check** — Paste any product's ingredient list; the app tokenizes, normalizes (case-insensitive, whitespace-stripped), and cross-references it against the user's active profile

### 📋 Planned
- **Allergy profile forms** — User-facing create/edit forms with dynamic allergen selection (checkbox grouped by subcategories of fragrances, surfactants, preservatives, botanicals, etc.)
- **Test coverage** — Comprehensive tests for allergy profile CRUD and form validation
- **Alias-Aware Matching (Synonym Mapper)** — The core technical next step. Maps every known surface form of an ingredient (INCI name, common name, abbreviation) to a single canonical allergen record, so "Vitamin C", "L-Ascorbic Acid", and "Ascorbate" all match the same allergy. Transforms the product from a string checker into an intelligent ingredient safety tool.
- **Product check form** — Full POST handling and result display on the product page
- **Allergy list autocomplete search** — hybrid feature along with the existing checkboxes divided into subcategories.
- **Product lookup** — planned input method.
- **User management pages** — Profile view, edit, and list
- **Severity-aware result** — display allergen results with severity (Mild / Moderate / Severe / Life-Threatening) as a planned feature.
- **Image/OCR capture** — Photograph a product label instead of typing the ingredient list
- **Barcode scanning** — Automatic ingredient lookup from a product barcode

---

## How It Works
1. Users selects from a searchable catalog of skincare ingredients. (checkboxes divided into subcategories)
2. Users input the skincare product's ingredient list.
3. The application compares the ingredient list against the user's allergies.
4. The app returns a result:
   - **Safe:** No allergens detected.
   - **Unsafe:** Product contains one or more allergens.

---

## Tech Stack
- **Framework:** Python Django 6.0 (handles both frontend and backend)
- **Database:** SQLite (Development) & PostgreSQL (Production)
- **Python:** 3.13 (Aligned with Django 6.0 requirements)
- **Package Management:** uv (fast, reliable dependency resolver with lockfiles)

---

## Quick Start

Get up and running in 5 minutes:

1. **Install uv** (if not already installed):
   ```bash
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and navigate:**
   ```bash
   git clone https://github.com/RJChoe/Skincare-Filter-Web-Application.git
   cd Skincare-Filter-Web-Application
   ```

3. **Set up Python environment:**
   ```bash
   uv python install 3.13
   uv python pin 3.13
   uv venv
   uv sync --group dev
   ```

4. **Run migrations and start server:**
   ```bash
   uv run python manage.py migrate
   uv run python manage.py runserver
   ```

5. **Run tests:**
   ```bash
   uv run pytest
   ```

6. **Set up pre-commit hooks (optional):**
   ```bash
   uv run pre-commit install
   ```

**Note:** Commands use `uv run` so manual venv activation is optional.

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Product Overview](PRODUCT.md) | Feature scope, user flows, known limitations |
| [Installation & Deployment](docs/DEPLOYMENT.md) | Local setup, CI/CD, hosting providers |
| [Testing & Coverage](docs/TESTING.md) | Running tests, coverage targets, patterns |
| [Architechture](ARCHITECTURE.md) | System design, data flow, decisions |
| [Contributing](CONTRIBUTING.md) | Development workflow, code style, gates |
| [Security](docs/SECURITY.md) | Environment variables, production hardening |

---

## Usage
1. Enter your personal allergies.
2. Input the ingredients of a skincare product.
3. Click "Check Safety".
4. View the results indicating whether the product is safe.

---

## Screenshots/Demo

Here's an example of how the app looks:

Coming Soon

<!--Allergy Input Page:
![Website requesting User's Allergy Input](link to image)

Ingredients Input Page
![Website requesting input of skincare product's ingredients](link to image)

Result Page
![Website with the Result Page. Green background for "SAFE" & Red background for "UNSAFE".](link to image)

((Replace the above images with actual screenshots from your project in a screenshots/ folder.))
-->

---

## Troubleshooting

Common setup issues and quick fixes:

- **Coverage below 75% threshold:** If tests fail with "coverage is below 75%":
    - **Temporary bypass:** Run tests without coverage: `uv run pytest --no-cov`
    - **Adjust threshold:** Temporarily lower `fail_under` value in `pyproject.toml` under `[tool.coverage.report]` (remember to restore it)
    - **Add tests:** Write additional tests to increase coverage before committing

- **GitHub status checks blocking merge:** If PR shows "Some checks failed" despite local tests passing:
    - Check the **Actions** tab in GitHub to see which workflow step failed
    - Verify the `build` and `test` jobs completed successfully
    - Check if `codecov/project` status shows coverage drop
    - Review the PR comments for Codecov report details

- Activation policy error (PowerShell): If you see "running scripts is disabled on this system":
    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate
    ```

- Python not found: Use uv to manage Python installations.
    ```bash
    uv python install 3.13
    uv python pin 3.13
    uv venv
    uv sync --group dev
    ```

- Migrations/app errors: Ensure apps are installed and migrations ran.
    ```bash
    uv run python manage.py showmigrations
    uv run python manage.py makemigrations allergies users
    uv run python manage.py migrate
    ```

- Port already in use: Run on a different port.
    ```bash
    uv run python manage.py runserver 8001
    ```

---
## Contact
    - Developer: Rebecca Jisoo Simpson

    - GitHub: RJChoe

---
