# Skincare Allergy Filter
[![codecov](https://codecov.io/gh/RJChoe/Skincare-Filter-Web-Application/branch/main/graph/badge.svg)](https://codecov.io/gh/RJChoe/Skincare-Filter-Web-Application)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Disclaimer: This app is a helper tool and not a substitute for professional medical advice. Always consult a dermatologist for severe allergies.

---
<!-- comment establish commit
-->
## Project Overview
The **Skincare Allergy Filter** is a Django-based web application that cross-references product ingredient lists against personal allergens and returns a safety recommendation.

---

## ⚙️ Project Workflow Diagram

Diagram flow of data through application
![Detailed workflow of the application components](./assets/workflow_allergy_filter.png)

---
## Features
- **Personal Allergy Input:** Users can list their known allergens.
- **Ingredient Check:** Users can input a skincare product's ingredient list.
- **Safety Alert:** The app notifies whether the product is safe or contains allergens.

---

## How It Works
1. Users enter their personal allergies (e.g., nuts, parabens, fragrance).
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
| [Installation & Deployment](docs/DEPLOYMENT.md) | Local setup, CI/CD, hosting providers |
| [Testing & Coverage](docs/TESTING.md) | Running tests, coverage targets, patterns |
| [ARCHITECTURE](ARCHITECTURE.md) | System design, data flow, decisions |
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
