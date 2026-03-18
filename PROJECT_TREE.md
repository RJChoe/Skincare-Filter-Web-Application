Skincare Project Structure:
├── 📁 Root Configuration
│   ├── ARCHITECTURE.md          # System design & data flow
│   ├── PRODUCT.md               # Requirements & Scope
│   ├── STATUS.md                # Roadmap & Current progress
│   ├── pyproject.toml           # uv dependencies & project metadata
│   ├── manage.py                # Django entry point
│   └── .env.example             # Required environment variables
│
├── 📁 Documentation (docs/dev/)
│   ├── ADMIN.md, DEPLOYMENT.md, FORMS.md
│   ├── LOGGING.md, MIGRATIONS.md, SECURITY.md
│   └── TESTING.md
│
├── 📁 Core: skincare_project/   # Project Settings & Global Routing
│   ├── settings.py              # Main Django config
│   ├── urls.py                  # Root URL dispatcher
│   └── wsgi.py / asgi.py        # Server interfaces
│
├── 📁 App: allergies/           # Ingredient & Filter Logic
│   ├── models.py                # DB Schema (Allergies)
│   ├── views.py                 # Filtering logic
│   ├── constants/choices.py     # Static mapping data
│   └── templates/allergies/     # List views & partials
│
├── 📁 App: users/               # Auth & Profile Management
│   ├── models.py                # Custom User Model
│   ├── managers.py              # User creation logic
│   ├── signals.py               # Post-save triggers
│   ├── validators.py            # Custom input validation
│   └── _log_utils.py            # User-specific logging helpers
│
├── 📁 Global UI (templates/)
│   ├── base.html                # Main skeleton
│   ├── layout.html              # Structural wrapper
│   └── home.html / product.html # Main landing pages
│
└── 📁 Static & Assets/
    ├── css/main.css             # Global styles
    └── assets/                  # Workflow diagrams/images
