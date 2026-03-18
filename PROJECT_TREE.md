Skincare Project Structure:
├── 📁 Root Configuration
│   ├── ARCHITECTURE.md          # System design overview
│   ├── PRODUCT.md               # Product requirements/scope
│   ├── STATUS.md                # Current project health/milestones
│   ├── pyproject.toml           # Build system & dependencies (using uv)
    └── README.md
    └── uv.lock                  # dependencies uv
    └── CONTRIBUTING.md          #
    └── conftest.py
    └── codecov.yml


📦.github
 ┣ 📂actions
 ┃ ┗ 📂setup-python-uv
 ┃ ┃ ┗ 📜action.yml
 ┣ 📂instructions
 ┃ ┗ 📜copilot-instructions.md
 ┣ 📂ISSUE_TEMPLATE
 ┃ ┣ 📜bug_report.md
 ┃ ┗ 📜feature_request.md
 ┣ 📂scripts
 ┃ ┗ 📜annotate_safety.py
 ┗ 📂workflows
 ┃ ┣ 📜ci.yml
 ┃ ┗ 📜uv-export.yml

 📦allergies
 ┣ 📂constants
 ┃ ┗ 📜choices.py
 ┣ 📂migrations
 ┃ ┣ 📜0001_initial.py
 ┃ ┗ 📜__init__.py
 ┣ 📂templates
 ┃ ┗ 📂allergies
 ┃ ┃ ┗ 📜allergies_list.html
 ┣ 📂tests
 ┃ ┣ 📜test_admin_error_handling.py
 ┃ ┣ 📜test_models.py
 ┃ ┣ 📜test_views_error_handling.py
 ┃ ┗ 📜__init__.py
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜models.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py

📦dev
 ┣ 📜ADMIN.md
 ┣ 📜DEPLOYMENT.md
 ┣ 📜FORMS.md
 ┣ 📜LOGGING.md
 ┣ 📜MIGRATIONS.md
 ┣ 📜SECURITY.md
 ┗ 📜TESTING.md

 📦skincare_project
 ┣ 📜asgi.py
 ┣ 📜settings.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┣ 📜wsgi.py
 ┗ 📜__init__.py

 📦static
 ┣ 📂css
 ┃ ┗ 📜main.css
 ┣ 📂js
 ┃ ┗ 📜main.js
 ┗ 📜favicon.svg

 📦templates
 ┣ 📜base.html
 ┣ 📜home.html
 ┣ 📜layout.html
 ┗ 📜product.html

 📦users
 ┣ 📂migrations
 ┃ ┣ 📜0001_initial.py
 ┃ ┗ 📜__init__.py
 ┣ 📂templates
 ┃ ┗ 📂users
 ┃ ┃ ┣ 📜user.html
 ┃ ┃ ┗ 📜user_list.html
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜managers.py
 ┣ 📜models.py
 ┣ 📜signals.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜validators.py
 ┣ 📜views.py
 ┣ 📜_log_utils.py
 ┗ 📜__init__.py
