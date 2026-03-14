# Production Deployment Guide

This guide covers deploying the Skincare Allergy Filter application to production environments.

---

## Table of Contents

0. [Local Development Setup](#local-development-setup)
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [CI/CD Alignment](#cicd-alignment)
3. [CI/CD Secrets](#cicd-secrets)
4. [CI/CD Configurations](#cicd-configurations)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [Static Files](#static-files)
8. [WSGI Server Configuration](#wsgi-server-configuration)
9. [Common Hosting Providers](#common-hosting-providers)
10. [Post-Deployment](#post-deployment)

---
## Local Development Setup
How to install and set up your project:

Note: This project uses [uv](https://docs.astral.sh/uv/) for dependency management, which provides fast, reliable installs with lockfile support.

1. Clone the repository:
    ```bash
    git clone https://github.com/RJChoe/Skincare-Filter-Web-Application.git
    ```

2. Navigate to the project folder:
    ```bash
    cd Skincare-Filter-Web-Application
    ```

3. Install uv (if not already installed):
    ```bash
    # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Windows (PowerShell)
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # Or via pip
    pip install uv
    ```

   **Windows users:** If the installation script fails, ensure PowerShell execution policy allows scripts. Run as Administrator if needed, or check `where.exe uv` to verify the installation path. Alternatively, use WSL2 for a Unix-like environment.

   **Note:** `uv sync` may prune undeclared tools (pip/uv) inside the venv; this is expected behavior.

4. Install Python 3.13 (if needed):
    ```bash
    uv python install 3.13
    ```

5. Pin Python version for this project:
    ```bash
    uv python pin 3.13
    ```

    This creates/updates `.python-version` which CI uses to enforce consistency (see [CI workflow](.github/workflows/ci.yml#L54-L64)).

    Verify the pin:
    ```bash
    # Windows
    type .python-version

    # macOS/Linux
    cat .python-version
    ```
    Output should show `3.13`.

    **Note:** If `.python-version` doesn't exist, run `uv python pin 3.13` to generate it. This file ensures CI and local development use the same Python version.

6. Create virtual environment (activation optional):
    ```bash
    # Create venv
    uv venv

    # Activate on Windows (PowerShell)
    .venv\Scripts\Activate.ps1

    # Activate on Windows (CMD)
    .venv\Scripts\activate.bat

    # Activate on macOS/Linux
    source .venv/bin/activate
    ```

    **Note:** All commands in this README use `uv run`, which automatically uses the venv without manual activation. Activation is optional but shown for reference.

7. Install all dependencies (runtime + dev):
    ```bash
    uv sync --group dev
    ```

8. Apply migrations:
    ```bash
    uv run python manage.py makemigrations allergies users
    uv run python manage.py migrate
    ```

9. Run the development server:
    ```bash
    uv run python manage.py runserver
    ```

10. Open your browser and visit http://localhost:8000

### Dependency Management with uv

**Note:** `requirements.txt` and `requirements-dev.txt` are not committed —
generate them on demand from `uv.lock`:
```bash
uv export --no-hashes --format requirements-txt -o requirements.txt
uv export --no-hashes --format requirements-txt --group dev -o requirements-dev.txt
```
`uv.lock` is the source of truth for all dependency resolution. The `--no-hashes` flag ensures cross-platform compatibility.
`uv.lock` is the source of truth for all dependency resolution.

This project uses **PEP 735 dependency groups** for organized development dependencies:
- `test` - Testing tools (pytest, pytest-cov, coverage)
- `lint` - Code formatting and linting (ruff, pre-commit)
- `type-check` - Type checking tools (mypy, django-stubs)
- `security` - Security scanning (bandit, safety)
- `dev` - Full development environment (includes all groups above)

**Adding dependencies:**
```bash
# Add a runtime dependency
uv add package-name

# Add a dependency to a specific group
uv add --group test pytest-mock
uv add --group lint pylint
uv add --group type-check types-requests
uv add --group security semgrep
```

**Installing specific groups:**
```bash
# Install only test dependencies
uv sync --group test

# Install multiple groups
uv sync --group test --group lint
#

# Install full dev environment
uv sync --group dev
```

**Updating dependencies:**
```bash
# Update all dependencies
uv lock --upgrade
```

**Note:** The pre-commit hooks automatically validate that requirements files stay in sync with `uv.lock`. CI will fail if they drift.

## Technical Decisions

### Migrating from [project.optional-dependencies]

If you have an existing development environment from before the PEP 735 migration:

1. Remove your existing virtual environment:
   ```bash
   # On Windows
   Remove-Item -Recurse -Force .venv

   # On macOS/Linux
   rm -rf .venv
   ```

2. Recreate the virtual environment:
   ```bash
   uv venv
   ```

3. Activate the virtual environment (see installation steps above)

4. Install dependencies with the new group system:
   ```bash
   uv sync --group dev
   ```

The new structure allows faster CI builds by installing only required dependencies per job (e.g., only `--group test` for test jobs).

---

## Verify Setup

<details>
<summary><b>✅ Click to expand setup verification</b></summary>

Quick checks to confirm your environment:

```bash
# Check Python version (should be 3.13)
uv run python -V

# Check Django version (should be 6.0)
uv run python -c "import django; print(django.get_version())"

# Verify uv installation
uv --version
```

</details>

---
## Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass locally: `uv run pytest`
- [ ] Coverage meets minimum threshold (75%)
- [ ] Security scan passes: `uv run bandit -r allergies users skincare_project`
- [ ] Dependencies are up to date and secure: `uv run safety scan --non-interactive`
- [ ] `.env` file configured with production values
- [ ] Database migrations are up to date
- [ ] Static files collected
- [ ] `DEBUG = False` in production environment
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS/SSL certificate obtained
- [ ] `SAFETY_API_KEY` GitHub secret configured (see [CI/CD Secrets](#cicd-secrets))

---

## CI/CD Alignment

This project's CI enforces consistency between local development and automated testing:

- **Python 3.13 enforcement:** CI verifies `.python-version` matches the active interpreter ([see workflow](.github/workflows/ci.yml#L54-L64))
- **uv-based commands:** All CI jobs use `uv run` for consistent Python/tool resolution
- **Dependency group isolation:** Each CI job installs only required groups (test, lint, type-check, security)
- **Lockfile validation:** The [uv-export workflow](.github/workflows/uv-export.yml) ensures `requirements.txt` files stay in sync with `uv.lock`
- **Safety scan authentication:** `safety scan` requires a `SAFETY_API_KEY` repository secret — without it the `static-analysis` job fails and blocks the merge. See [CI/CD Secrets](docs/DEPLOYMENT.md#cicd-secrets) for setup.

**Run the same checks locally:**

```bash
# Verify Python version matches .python-version
uv run python --version

# Run pre-commit (same as CI lint job)
uv run pre-commit run --all-files

# Run tests (same as CI test job)
uv run pytest

# Validate lockfile sync
uv lock --check
```

**Before committing:** Ensure `.python-version` exists (`uv python pin 3.13`) and pre-commit hooks are installed (`uv run pre-commit install`). CI will fail if Python versions mismatch or requirements files drift from `uv.lock`.

---

## CI/CD Secrets

The CI workflow uses GitHub Actions secrets for external service integrations. Unlike Variables, secrets are **masked (`***`) in all log output**, preventing accidental key exposure to anyone with read access to the repository.

### Required Secrets

| Secret | Required | Purpose |
| :--- | :--- | :--- |
| `SAFETY_API_KEY` | ✅ Yes | Authenticates `safety scan` for vulnerability checks |
| `CODECOV_TOKEN` | ⚠️ Recommended | Uploads coverage reports to Codecov |

### Setting Up `SAFETY_API_KEY`

#### 1. Obtain an API key

Register or log in at [safety.pyup.io](https://safety.pyup.io), then navigate to **Account Settings → API Keys → New API Key**.

#### 2. Add the secret to GitHub

1. Go to your repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click the **Secrets tab** — ⚠️ **not the Variables tab**: Variables are stored in plaintext and visible in workflow logs, which would expose your API key
4. Click **"New repository secret"**
5. Set the name to exactly `SAFETY_API_KEY`
6. Paste your API key as the value
7. Click **"Add secret"**

#### 3. CI behaviour by authentication state

| State | CI behaviour |
| :--- | :--- |
| Secret set and valid | ✅ Scan runs authenticated; results appear in step summary |
| Secret missing or expired | ❌ Annotation step exits with code 1; `static-analysis` job fails; merge blocked via branch protection |

---
## CI/CD Configuration

### CI/CD Integration

<details>
<summary><b>⚙️ Click to expand CI/CD configuration</b></summary>

#### GitHub Actions Workflow
Automate testing and coverage reporting on pull requests to maintain code quality.

**Note:** The example below shows a simplified workflow for learning purposes. This project's actual CI workflow is [.github/workflows/ci.yml](.github/workflows/ci.yml), which includes 5 specialized jobs (dependencies, lint, test, type-check, security) for comprehensive quality enforcement.

**First, create the workflow directory** (if it doesn't exist):

```bash
# Windows: New-Item -ItemType Directory -Force -Path .github\workflows
mkdir -p .github/workflows
```

**Example simplified workflow (`.github/workflows/test.yml`):**

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
        python-version: ['3.13']

    steps:
    - uses: actions/checkout@v5

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        uv sync --group test

    - name: Run migrations
      run: |
        uv run python manage.py migrate

    - name: Run tests with coverage
      run: |
        uv run pytest

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
- **Matrix testing:** Tests Python 3.13 on Ubuntu
- **Job names:** Uses "build" and "test" for status check references
- **Coverage enforcement:** Fails if coverage drops below 75% (via `pyproject.toml`)

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
   - `ci-success` (from GitHub Actions workflow — aggregates all jobs)
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
   - Select `RJChoe/Skincare-Filter-Web-Application` from your repository list
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
           target: 75%           # Target coverage percentage
           threshold: 5%         # Allow coverage to drop 5% before failing
       patch:
         default:
           target: 80%           # New code should have 80% coverage

     range: 75..100              # Coverage color coding (red at 75%, green at 100%)

   comment:
     layout: "header, diff, files"
     behavior: default

   ignore:
     - "*/migrations/*"
     - "*/tests/*"
   ```

   This configuration:
   - Fails PR if overall coverage drops more than 5%
   - Requires 80% coverage on newly added code
   - Posts coverage report comments on PRs

5. **Verify badge:**
   The badge at the top of this README updates automatically after each push.

**For more advanced configuration, see:**
- [Codecov documentation](https://docs.codecov.com/)

---

## Environment Configuration

### Install django-environ

```bash
uv add django-environ
```

### Create Production .env File

Create a `.env` file on your production server (never commit this):

```bash
# Production .env
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://username:password@hostname:5432/database_name

# Optional: Security settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Generate a Secure SECRET_KEY

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Important:** Use a different `SECRET_KEY` for each environment (development, staging, production).

### ALLOWED_HOSTS Configuration

Configure based on your hosting provider:

#### Common Hosting Providers

```bash
# Heroku
ALLOWED_HOSTS=yourapp.herokuapp.com

# DigitalOcean
ALLOWED_HOSTS=your-droplet-ip,yourdomain.com,www.yourdomain.com

# AWS EC2
ALLOWED_HOSTS=ec2-xx-xxx-xxx-xx.compute-1.amazonaws.com,yourdomain.com

# Render
ALLOWED_HOSTS=yourapp.onrender.com,yourdomain.com

# Multiple domains
ALLOWED_HOSTS=example.com,www.example.com,api.example.com
```

---

## Database Setup

### PostgreSQL (Recommended for Production)

#### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### 2. Create Database and User

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE skincare_filter_db;

# Create user with password
CREATE USER skincare_user WITH PASSWORD 'secure_password_here';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE skincare_filter_db TO skincare_user;

# Exit
\q
```

#### 3. Configure DATABASE_URL

```bash
# .env
DATABASE_URL=postgres://skincare_user:secure_password_here@localhost:5432/skincare_filter_db

# With connection pooling (recommended)
DATABASE_URL=postgres://skincare_user:secure_password_here@localhost:5432/skincare_filter_db?conn_max_age=600
```

#### 4. Install PostgreSQL Adapter

```bash
uv add psycopg2-binary
```

#### 5. Run Migrations

```bash
uv run python manage.py migrate
```

### PostgreSQL Security Best Practices

- Use strong passwords (16+ characters, random)
- Restrict user permissions (avoid superuser)
- Enable SSL/TLS connections
- Regular backups with encryption
- Keep PostgreSQL updated

---

## Static Files

Django should not serve static files in production. Use a web server or CDN.

### 1. Configure Static Files Settings

Update `settings.py`:

```python
# settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

### 2. Collect Static Files

```bash
uv run python manage.py collectstatic --noinput
```

### 3. Serve Static Files

#### Option A: Nginx

```nginx
# /etc/nginx/sites-available/skincare_filter
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Option B: WhiteNoise (Simple Solution)

```bash
uv add whitenoise
```

Update `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## WSGI Server Configuration

Django's development server is not suitable for production. Use Gunicorn or uWSGI.

### Option A: Gunicorn (Recommended)

#### 1. Install Gunicorn

```bash
uv add gunicorn
```

#### 2. Test Gunicorn Locally

```bash
uv run gunicorn skincare_project.wsgi:application --bind 0.0.0.0:8000
```

#### 3. Create Gunicorn Configuration

Create `gunicorn_config.py`:

```python
# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 3  # (2 x $num_cores) + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
errorlog = "-"
accesslog = "-"
loglevel = "info"
```

#### 4. Run Gunicorn

```bash
uv run gunicorn skincare_project.wsgi:application -c gunicorn_config.py
```

#### 5. Systemd Service (Linux)

Create `/etc/systemd/system/skincare_filter.service`:

```ini
[Unit]
Description=Skincare Filter Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/.venv/bin"
ExecStart=/path/to/your/project/.venv/bin/gunicorn \
          skincare_project.wsgi:application \
          -c gunicorn_config.py

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable skincare_filter
sudo systemctl start skincare_filter
sudo systemctl status skincare_filter
```

### Option B: uWSGI

#### 1. Install uWSGI

```bash
uv add uwsgi
```

#### 2. Create uWSGI Configuration

Create `uwsgi.ini`:

```ini
[uwsgi]
module = skincare_project.wsgi:application
master = true
processes = 4
socket = /tmp/skincare_filter.sock
chmod-socket = 666
vacuum = true
die-on-term = true
```

#### 3. Run uWSGI

```bash
uv run uwsgi --ini uwsgi.ini
```

---

## Common Hosting Providers

### Heroku

1. **Install Heroku CLI**:

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Heroku App**:

```bash
heroku create your-app-name
```

3. **Add PostgreSQL**:

```bash
heroku addons:create heroku-postgresql:mini
```

4. **Set Environment Variables**:

```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

5. **Create `Procfile`**:

```
web: gunicorn skincare_project.wsgi --log-file -
```

6. **Deploy**:

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
```

### DigitalOcean App Platform

1. **Create `app.yaml`**:

```yaml
name: skincare-filter
services:
- name: web
  github:
    repo: RJChoe/Skincare-Filter-Web-Application
    branch: main
  build_command: uv sync && uv run python manage.py collectstatic --noinput
  run_command: uv run gunicorn skincare_project.wsgi:application
  envs:
  - key: DEBUG
    value: "False"
  - key: SECRET_KEY
    type: SECRET
  - key: ALLOWED_HOSTS
    value: "${APP_DOMAIN}"
databases:
- name: skincare-db
  engine: PG
  version: "14"
```

2. **Deploy via DigitalOcean Dashboard** or `doctl` CLI.

### AWS EC2

1. **Launch EC2 Instance** (Ubuntu 22.04 LTS recommended)

2. **SSH into Instance**:

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**:

```bash
sudo apt update
sudo apt install python3.13 python3.13-venv postgresql nginx
curl -LsSf https://astral.sh/uv/install.sh | sh
```

4. **Clone Repository**:

```bash
git clone https://github.com/RJChoe/Skincare-Filter-Web-Application.git
cd Skincare-Filter-Web-Application
```

5. **Set Up Application** (follow environment configuration above)

6. **Configure Nginx** (see Static Files section)

7. **Set Up SSL** with Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Render

1. **Create `render.yaml`**:

```yaml
services:
  - type: web
    name: skincare-filter
    env: python
    buildCommand: "uv sync && uv run python manage.py collectstatic --noinput && uv run python manage.py migrate"
    startCommand: "uv run gunicorn skincare_project.wsgi:application"
    envVars:
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.13
      - key: DATABASE_URL
        fromDatabase:
          name: skincare-db
          property: connectionString

databases:
  - name: skincare-db
    plan: starter
```

2. **Connect GitHub Repository** in Render Dashboard

3. **Deploy** (automatic on push to main)

---

## Post-Deployment

### 1. Verify Deployment

```bash
# Check application is running
curl https://yourdomain.com

# Check admin access
curl https://yourdomain.com/admin/

# Check static files
curl https://yourdomain.com/static/css/style.css
```

### 2. Create Superuser

```bash
uv run python manage.py createsuperuser
```

### 3. Set Up Monitoring

Consider using:
- **Sentry** for error tracking
- **New Relic** for application performance monitoring
- **Datadog** for infrastructure monitoring
- **UptimeRobot** for uptime monitoring

### 4. Set Up Backups

#### Database Backups

```bash
# PostgreSQL backup
pg_dump -U skincare_user skincare_filter_db > backup_$(date +%Y%m%d).sql

# Automated daily backups (cron)
0 2 * * * pg_dump -U skincare_user skincare_filter_db > /backups/backup_$(date +\%Y\%m\%d).sql
```

### 5. Configure Logging

Update `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 6. Security Hardening

- Enable HTTPS enforcement
- Set up firewall rules
- Regular security updates
- Monitor access logs
- Implement rate limiting
- Set up intrusion detection

---

## Troubleshooting

### Static Files Not Loading

```bash
# Verify STATIC_ROOT
uv run python manage.py findstatic style.css

# Recollect static files
uv run python manage.py collectstatic --clear --noinput
```

### Database Connection Errors

```bash
# Test database connection
uv run python manage.py dbshell

# Verify DATABASE_URL format
echo $DATABASE_URL
```

### Permission Errors

```bash
# Fix file permissions
sudo chown -R www-data:www-data /path/to/project
sudo chmod -R 755 /path/to/project
```

### Application Not Starting

```bash
# Check logs
sudo journalctl -u skincare_filter -n 50

# Test WSGI application
uv run python manage.py check --deploy
```

### Python Version Issues

## Troubleshooting Python Version

<details>
<summary><b>🔧 Python Version Issues</b></summary>

**Important:** CI enforces `.python-version` matching (see [workflow](.github/workflows/ci.yml#L54-L64)). Always run `uv python pin 3.13` after cloning to ensure alignment.

This project uses a `.python-version` file to pin Python 3.13 for local development. uv automatically detects and uses this version.

### Check Your Python Version

```bash
# List all installed Python versions managed by uv
uv python list

# Example output:
# cpython-3.13.0-windows-x86_64-none    <-- active
# cpython-3.12.1-windows-x86_64-none
```

The active version (marked with `<--`) should be 3.13.x to match `.python-version`.

### Install Python 3.13

If you don't have Python 3.13 installed:

```bash
# Install python 3.13 (uv will download and manage it)
uv python install 3.13

# Verify installation
uv python list
```

### Pin Python Version

If you need to explicitly pin or change the Python version:

```bash
# Pin to python 3.13 (updates .python-version)
uv python pin 3.13

# Verify the pin
cat .python-version    # Should output: 3.13
```

### Recreate Virtual Environment

If your virtual environment is using the wrong Python version:

```bash
# Remove existing venv
Remove-Item -Recurse -Force .venv    # Windows PowerShell
rm -rf .venv                          # macOS/Linux

# Create new venv with correct Python version
uv venv --python 3.13

# Reinstall dependencies
uv sync --group dev
```

### Common Issues

**Issue:** `python --version` shows wrong version despite `.python-version`

**Solution:** The `.python-version` file is for uv's Python management. To ensure consistency:
- Always use `uv run python` instead of `python` directly
- Or activate your venv: `.venv\Scripts\Activate.ps1` (Windows) / `source .venv/bin/activate` (Linux/macOS)

**Issue:** Pre-commit hook fails with version mismatch

**Solution:** Your system Python differs from the pinned version. Either:
1. Activate the virtual environment before committing
2. Install python 3.13 system-wide
3. Use `uv run` commands which automatically use the correct version

---

## Scaling Considerations

As your application grows:

1. **Load Balancing**: Use multiple Gunicorn workers across servers
2. **Caching**: Implement Redis or Memcached
3. **CDN**: Use CloudFlare or AWS CloudFront for static files
4. **Database**: Set up read replicas for PostgreSQL
5. **Task Queue**: Use Celery for background tasks
6. **Auto-Scaling**: Configure based on traffic patterns

---

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

---

## Support

For deployment issues or questions, contact **RJSimpson1004@gmail.com** or open an issue on [GitHub](https://github.com/RJChoe/Skincare-Filter-Web-Application/issues).
