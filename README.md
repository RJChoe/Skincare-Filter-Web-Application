# Skincare Allergy Filter

[![codecov](https://codecov.io/gh/RJChoe/filter-project/branch/main/graph/badge.svg)](https://codecov.io/gh/RJChoe/filter-project)
[![Tests](https://github.com/RJChoe/filter-project/workflows/Tests/badge.svg)](https://github.com/RJChoe/filter-project/actions)

## Project Overview
The **Skincare Allergy Filter** is a web application that helps users determine if skincare products are safe based on their personal allergies. Users can enter their allergies along with a product's ingredient list, and the app will check for potential allergens and return a safety recommendation.

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

## ⚙️ Project Workflow Diagram

Diagram flow of data through application
![Detailed workflow of the application components](./assets/workflow_allergy_filter.png)

---

## Tech Stack
- **Framework:** Python Django 5.2 (handles both frontend and backend)  
- **Database:** SQLite (default) or any Django-supported database
- **Python:** 3.9+ (required for Django 5.2 LTS support)

---

## Installation
How to install and set up your project:

Note: Unless explicitly labeled, commands are shell-agnostic and work in Windows PowerShell, CMD, and Unix shells. Use the Windows-specific blocks where provided.

1. Clone the repository:
     - Windows (PowerShell):
         ```powershell
         git clone https://github.com/RJChoe/filter-project.git
         ```

     - macOS/Linux:
         ```bash
         git clone https://github.com/RJChoe/filter-project.git
         ```

2. Navigate to the project folder:
     - Windows (PowerShell):
         ```powershell
         cd filter-project
         ```

     - macOS/Linux:
         ```bash
         cd filter-project
         ```


(Remember to .gitignore .venv prior to setting up)

3. Create a virtual environment:
     - Windows (PowerShell):
         ```powershell
         python -m venv .venv
         ```

     - macOS/Linux:
         ```bash
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
     - Windows (PowerShell):
         ```powershell
         pip install -r requirements.txt
         ```

     - macOS/Linux:
         ```bash
         pip install -r requirements.txt
         ```

6. Apply migrations:
     - Windows (PowerShell):
         ```powershell
         python manage.py makemigrations allergies user
         python manage.py migrate
         ```

     - macOS/Linux:
         ```bash
         python manage.py makemigrations allergies user
         python manage.py migrate
         ```

7. Run the development server:
     - Windows (PowerShell):
         ```powershell
         python manage.py runserver
         ```

     - macOS/Linux:
         ```bash
         python manage.py runserver
         ```

8. Open your browser and visit http://localhost:8000

---

## Verify Setup
Quick checks to confirm your environment:

 - Windows (PowerShell):
     ```powershell
     python -V
     python -c "import django; print(django.get_version())"
     ```

 - macOS/Linux:
     ```bash
     python -V
     python -c "import django; print(django.get_version())"
     ```

---

## Testing & Code Coverage

### Running Tests
Execute the test suite:

- Windows (PowerShell):
    ```powershell
    python -m pytest
    ```

- macOS/Linux:
    ```bash
    python -m pytest
    ```

### Code Coverage
Measure test coverage to ensure your code is well-tested. Coverage helps identify untested lines and ensures reliability.

Run tests with coverage reporting:

- Windows (PowerShell):
    ```powershell
    python -m pytest --cov=allergies --cov=users --cov-report=html --cov-report=term-missing
    ```

- macOS/Linux:
    ```bash
    python -m pytest --cov=allergies --cov=users --cov-report=html --cov-report=term-missing
    ```

This generates:
- **Terminal output** showing coverage percentage and which lines aren't covered
- **HTML report** in `htmlcov/index.html` for detailed, line-by-line browsing

#### Coverage Targets
| Phase | Target | When |
|-------|--------|------|
| Phase 1 | 50% | Foundation testing |
| Phase 2 | 70% | Views + users tests added |
| Phase 3 | 85% | Project maturity |

### Advanced Coverage Features

#### Branch Coverage
This project uses **branch coverage** (not just line coverage), which means tests measure both:
- **Line coverage:** Whether each line of code is executed
- **Branch/decision coverage:** Whether all paths through control structures (if/else, loops, try/except) are tested

Branch coverage is enabled via `branch = True` in `pytest.ini`, providing more thorough test quality measurement.

#### Simplified Coverage Command
Since `.coveragerc` pre-configures the source packages (`allergies` and `users`), you can use a shorter command:

- Windows (PowerShell):
    ```powershell
    python -m pytest --cov --cov-report=html --cov-report=term-missing
    ```

- macOS/Linux:
    ```bash
    python -m pytest --cov --cov-report=html --cov-report=term-missing
    ```

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
```powershell
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

- Run only fast tests (exclude slow tests):
    ```powershell
    python -m pytest -m "not slow"
    ```

- Run only integration tests:
    ```powershell
    python -m pytest -m integration
    ```

- Run all tests except integration tests:
    ```powershell
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

---
## Development Workflow

### Pre-commit Hooks
Automate code quality checks before each commit to maintain consistent standards and catch issues early.

#### Setup
Install and configure pre-commit hooks:

- Windows (PowerShell):
    ```powershell
    pip install pre-commit
    pre-commit install
    ```

- macOS/Linux:
    ```bash
    pip install pre-commit
    pre-commit install
    ```

#### Configuration
Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

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
- **Black:** Auto-formats Python code
- **isort:** Organizes imports alphabetically
- **File hygiene:** Removes trailing whitespace, ensures newlines at end of files
- **Fast tests:** Runs non-slow tests (typically ~5-10 seconds)

**Note:** Pre-commit hooks run automatically before each commit. If checks fail, the commit is blocked until issues are resolved.

### CI/CD Integration

#### GitHub Actions Workflow
Automate testing and coverage reporting on pull requests to maintain code quality.

**First, create the workflow directory** (if it doesn't exist):

- Windows (PowerShell):
    ```powershell
    New-Item -ItemType Directory -Force -Path .github\workflows
    ```

- macOS/Linux:
    ```bash
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
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run migrations
      run: |
        python manage.py makemigrations allergies users
        python manage.py migrate
    
    - name: Run tests with coverage
      run: |
        pytest --cov --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true

  test:
    runs-on: ubuntu-latest
    needs: build
    
    steps:
    - name: Coverage check passed
      run: echo "All tests and coverage checks passed"
```

This workflow:
- **Triggers:** Only on PRs to `main` and `develop` branches
- **Matrix testing:** Tests Python 3.9, 3.10, and 3.11 on Ubuntu
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

-------
## Troubleshooting
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
    python manage.py makemigrations allergies user
    python manage.py migrate
    ```

- Port already in use: Run on a different port.
    ```powershell
    python manage.py runserver 8001
    ```

---

## Usage
1. Enter your personal allergies.
2. Input the ingredients of a skincare product.
3. Click "Check Safety".
4. View the results indicating whether the product is safe.

---

## Screenshots/Demo

Here’s an example of how the app looks:
Allergy Input Page
![Website requesting User's Allergy Input](link to image)

Ingredients Input Page
![Website requesting input of skincare product's ingredients](link to image)

Result Page
![Website with the Result Page. Green background for "SAFE" & Red background for "UNSAFE".](link to image)

((Replace the above images with actual screenshots from your project in a screenshots/ folder.))

---

## Contact
    - Developer: Rebecca Jisoo Simpson

    - Email: RJSimpson1004@gmail.com

    - GitHub: RJChoe