# Skincare Allergy Filter
[![codecov](https://codecov.io/gh/RJChoe/filter-project/branch/main/graph/badge.svg)](https://codecov.io/gh/RJChoe/filter-project)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Disclaimer: This app is a helper tool and not a substitute for professional medical advice. Always consult a dermatologist for severe allergies.

---

## Project Overview
The **Skincare Allergy Filter** is a Django-based web application that cross-references product ingredient lists against personal allergens and returns a safety recommendation.

---

## ⚙️ Project Workflow Diagram

Diagram flow of data through application
![Detailed workflow of the application components](./assets/workflow_allergy_filter.png)

---
## Features
- **Personal Allergy Input:** Users can list their known allergens.
- **Ingredient Check:** Users can input a skincare product’s ingredient list.
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
- **Framework:** Python Django 5.2 LTS (handles both frontend and backend)
- **Database:** SQLite (Development) & PostgreSQL (Production)
- **Python:** 3.11+ (Aligned with Django 5.2+ requirements)

---

## Installation

<details>
<summary><b>📦 Click to expand installation steps</b></summary>

How to install and set up your project:

Note: Commands are shell-agnostic and work across Windows PowerShell, CMD, and Unix shells.

1. Clone the repository:
    ```bash
    git clone https://github.com/RJChoe/filter-project.git
    ```

2. Navigate to the project folder:
    ```bash
    cd filter-project
    ```


(Remember to .gitignore .venv prior to setting up)

3. Create a virtual environment:
    ```bash
    # macOS/Linux: use python3 if python is not available
    python -m venv .venv
    ```

4. Activate the virtual environment:
     - Windows (PowerShell):
         ```powershell
         .\.venv\Scripts\Activate
         ```

     - Windows (CMD):
         ```bat
         .\.venv\Scripts\activate.bat
         ```

     - macOS/Linux:
         ```bash
         source .venv/bin/activate
         ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Apply migrations:
    ```bash
    python manage.py makemigrations allergies users
    python manage.py migrate
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

8. Open your browser and visit http://localhost:8000

</details>

---

## Verify Setup

<details>
<summary><b>✅ Click to expand setup verification</b></summary>

Quick checks to confirm your environment:

```bash
# macOS/Linux: use python3 if python is not available
python -V
python -c "import django; print(django.get_version())"
```

</details>

---

## Usage
1. Enter your personal allergies.
2. Input the ingredients of a skincare product.
3. Click "Check Safety".
4. View the results indicating whether the product is safe.

---

## Screenshots/Demo

Here’s an example of how the app looks:

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

## Testing & Code Coverage

<details>
<summary><b>🧪 Click to expand testing & coverage details</b></summary>

### Running Tests
Execute the test suite:

```bash
python -m pytest
```

All test discovery, markers, and coverage settings are configured in `pyproject.toml`, so `pytest` automatically applies:
- Test discovery from `allergies/tests` and `users/tests`
- Coverage of `allergies`, `users`, and `skincare_project` packages
- Coverage reports in terminal and XML (for CI)
- Fail-under threshold of 50%

### Code Coverage
Test coverage is measured automatically when running pytest. The configuration in `pyproject.toml` includes:
- **Branch coverage** (tests all control flow paths, not just lines)
- **XML report** for CI/Codecov uploads
- **Terminal report** showing coverage percentage and untested lines
- **Omit patterns** to exclude migrations, tests, settings, and utility modules

#### Coverage Targets
| Phase | Target | When |
|-------|--------|------|
| Phase 1 | 50% | Foundation testing |
| Phase 2 | 70% | Views + users tests added |
| Phase 3 | 85% | Project maturity |

#### Viewing Coverage Details
To view an HTML coverage report for detailed line-by-line analysis:

```bash
# Generate HTML report (pytest runs with coverage automatically)
python -m pytest
# Then open htmlcov/index.html in your browser
```

The HTML report shows:
- Which lines are covered/uncovered
- Branch coverage details
- Coverage summary by file

</details>

#### Terminal Output Example
The `--cov-report=term-missing` flag produces output like:

```
Name                                Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------
allergies/__init__.py                   0      0      0      0   100%
allergies/models.py                    45      8     12      3    78%   23-27, 45, 67->69
allergies/views.py                     32      5      8      1    82%   15-17, 42
users/models.py                        28      0      6      0   100%
users/views.py                         19      4      4      1    73%   8, 22-24
--------------------------------------------------------------------------------
TOTAL                                 124     17     30      5    82%
```

This shows:
- **Stmts:** Total statements
- **Miss:** Uncovered lines
- **Branch/BrPart:** Branch coverage metrics
- **Missing:** Specific line numbers and ranges not covered

#### Automatic Coverage Threshold Enforcement
The project enforces a **minimum 50% coverage threshold** via `fail_under = 50` in `pytest.ini`. This means:
- **Local development:** Test suite fails if coverage drops below 50%
- **CI/CD pipelines:** Builds fail automatically if coverage is insufficient
- **Quality gate:** Prevents merging code that significantly reduces test coverage

To bypass coverage checks temporarily (e.g., during development):
```bash
python -m pytest --no-cov
```

#### Viewing HTML Coverage Reports
After generating the HTML report, open it in your browser:

- Windows (PowerShell):
    ```powershell
    Invoke-Item htmlcov\index.html
    ```

- macOS:
    ```bash
    open htmlcov/index.html
    ```

- Linux:
    ```bash
    xdg-open htmlcov/index.html
    ```

The HTML report provides:
- **File listing dashboard:** Overview of coverage by file with sortable columns
- **Source code view:** Line-by-line highlighting (green = covered, red = missed)
- **Search functionality:** Find specific files or code sections quickly
- **Coverage statistics:** Detailed metrics including branch coverage percentages

*Note: HTML report screenshot will be added in a future update.*

### Test Filtering with Markers

The project uses pytest markers to categorize tests, allowing you to run specific subsets:

#### Available Markers
- `@pytest.mark.integration` - Integration tests that interact with multiple components
- `@pytest.mark.slow` - Tests that take longer to execute

#### Using Markers in Your Tests
Add markers to test functions in files like `allergies/tests/test_models.py`:

```python
import pytest
from allergies.models import Allergy

@pytest.mark.slow
def test_complex_allergen_matching():
    # Test that takes significant time
    pass

@pytest.mark.integration
def test_user_allergy_workflow():
    # Test that spans multiple components
    pass
```

#### Filtering Tests
Run specific test subsets using the `-m` flag:

```bash
# Run only fast tests (exclude slow tests)
python -m pytest -m "not slow"

# Run only integration tests
python -m pytest -m integration

# Run all tests except integration tests
python -m pytest -m "not integration"
```

### Configuration Files

The coverage system uses two configuration files:

#### `.coveragerc`
Controls coverage.py behavior:
- **Source packages:** Defines `allergies` and `users` as measured code
- **Omit patterns:** Excludes `*/migrations/*`, `*/tests/*`, `*/__pycache__/*` from coverage
- **Exclusions:** Ignores debug-only code, `TYPE_CHECKING` blocks, and pragma comments
- **HTML output:** Configures `htmlcov/` directory and report formatting

#### `pytest.ini`
Controls pytest and coverage integration:
- **Branch coverage:** Enables `branch = True` for decision coverage
- **Fail threshold:** Sets `fail_under = 50` to enforce minimum coverage
- **Markers:** Registers `integration` and `slow` markers
- **Default flags:** Applies `-ra --strict-markers` for better test reporting

**For advanced customization, see:**
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [coverage.py documentation](https://coverage.readthedocs.io/)

</details>

---
## Development Workflow

### Pre-commit Hooks

<details>
<summary><b>🔧 Click to expand pre-commit hooks setup</b></summary>
Automate code quality checks before each commit to maintain consistent standards and catch issues early.

#### Setup
Install and configure pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

#### Configuration
Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.1
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: local
    hooks:
      - id: pytest-fast
        name: pytest-fast
        entry: pytest -m "not slow" --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

This configuration runs:
- **Ruff Linter:** Checks code quality (500+ rules, including Django-specific checks)
- **Ruff Formatter:** Auto-formats Python code (Black-compatible)
- **File hygiene:** Removes trailing whitespace, ensures newlines at end of files
- **Fast tests:** Runs non-slow tests (typically ~5-10 seconds)

**Note:** Pre-commit hooks run automatically before each commit. If checks fail, the commit is blocked until issues are resolved.

</details>

### Fail Fast Checklist
Catch issues in ~10-15 seconds before committing. Run these manual checks during active development to verify code quality before pre-commit hooks execute.

#### Quick Verification Commands

- **Run fast tests** — Verify core logic without slow integration tests:
    ```bash
    python -m pytest -m "not slow"
    ```

- **Lint with Ruff** — Check code quality and formatting:
    ```bash
    ruff check . --fix
    ruff format . --check
    ```

- **Confirm migrations applied** — Check database migration status:
    ```bash
    python manage.py showmigrations
    ```

#### Power User Tip
Run all checks sequentially with a single command:

```bash
python -m pytest -m "not slow" && ruff check . --fix && ruff format . --check && python manage.py showmigrations
```

**Note:** While pre-commit hooks automate these checks, running them manually helps catch issues faster during development. See [Troubleshooting](#troubleshooting) for resolving common failures.

### CI/CD Integration

<details>
<summary><b>⚙️ Click to expand CI/CD configuration</b></summary>

#### GitHub Actions Workflow
Automate testing and coverage reporting on pull requests to maintain code quality.

**First, create the workflow directory** (if it doesn't exist):

```bash
# Windows: New-Item -ItemType Directory -Force -Path .github\workflows
mkdir -p .github/workflows
```

**Then create `.github/workflows/test.yml`:**

```yaml
name: Tests

on:
  pull_request:
    branches:
      - main
      - develop

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.14']

    steps:
    - uses: actions/checkout@v5

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run migrations
      run: |
        python manage.py migrate

    - name: Run tests with coverage
      run: |
        pytest --cov --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v5
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true
```

This workflow:
- **Triggers:** Only on PRs to `main` and `develop` branches
- **Matrix testing:** Tests Python 3.11, 3.12, and 3.14 on Ubuntu
- **Job names:** Uses "build" and "test" for status check references
- **Coverage enforcement:** Fails if coverage drops below 50% (via `pytest.ini`)

#### Branch Protection Rules
Enforce quality standards by requiring all checks to pass before merging.

**Setup in GitHub repository settings:**

1. Navigate to **Settings → Branches**
2. Click **Add rule** (or edit existing rule)
3. Enter branch name pattern: `main` (repeat for `develop`)
4. Enable these settings:
   - ☑ **Require status checks to pass before merging**
   - ☑ **Require branches to be up to date before merging**
5. In **Status checks that are required**, select:
   - `build` (from GitHub Actions workflow)
   - `test` (from GitHub Actions workflow)
   - `codecov/project` (from Codecov integration)
6. Click **Create** or **Save changes**

**Admin Override Process:**
If emergency merges are needed despite failed checks, repository admins can override protection. This requires:
- Maintainer review and approval
- Documented justification in PR comments explaining the urgency
- Post-merge remediation plan committing to fix coverage or tests within a specific timeframe

This setup ensures coverage drops and test failures block merges, maintaining code quality standards.

#### Codecov Integration
Track and visualize coverage trends across commits and pull requests.

**Step-by-step setup:**

1. **Sign up for Codecov:**
   - Visit [codecov.io](https://codecov.io/) and sign in with your GitHub account
   - Authorize Codecov to access your repositories

2. **Link your repository:**
   - Select `RJChoe/filter-project` from your repository list
   - Codecov will provide an upload token

3. **Add Codecov token to GitHub:**
   - Go to repository **Settings → Secrets and variables → Actions**
   - Click **New repository secret**
   - Name: `CODECOV_TOKEN`
   - Value: Paste the token from Codecov
   - Click **Add secret**

4. **Configure coverage thresholds (optional):**
   Create `.codecov.yml` in project root:

   ```yaml
   coverage:
     status:
       project:
         default:
           target: 80%           # Target coverage percentage
           threshold: 5%         # Allow coverage to drop 5% before failing
       patch:
         default:
           target: 70%           # New code should have 70% coverage

     range: 50..100              # Coverage color coding (red at 50%, green at 100%)

   comment:
     layout: "header, diff, files"
     behavior: default

   ignore:
     - "*/migrations/*"
     - "*/tests/*"
   ```

   This configuration:
   - Fails PR if overall coverage drops more than 5%
   - Requires 70% coverage on newly added code
   - Posts coverage report comments on PRs

5. **Verify badge:**
   The badge at the top of this README updates automatically after each push.

**For more advanced configuration, see:**
- [Codecov documentation](https://docs.codecov.com/)

</details>

-------
## Troubleshooting

<details>
<summary><b>🔍 Click to expand troubleshooting guide</b></summary>

Common setup issues and quick fixes:

- **Coverage below 50% threshold:** If tests fail with "coverage is below 50%":
    - **Temporary bypass:** Run tests without coverage: `pytest --no-cov`
    - **Adjust threshold:** Temporarily lower `fail_under` value in `pytest.ini` (remember to restore it)
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

- Python not found on Windows: Use the `py` launcher.
    ```powershell
    py -V
    py -m venv .venv
    py -m pip install -r requirements.txt
    ```

- Migrations/app errors: Ensure apps are installed and migrations ran.
    ```powershell
    python manage.py showmigrations
    python manage.py makemigrations allergies users
    python manage.py migrate
    ```

- Port already in use: Run on a different port.
    ```powershell
    python manage.py runserver 8001
    ```

</details>

---
## Contact
    - Developer: Rebecca Jisoo Simpson

    - Email: RJSimpson1004@gmail.com

    - GitHub: RJChoe

---
