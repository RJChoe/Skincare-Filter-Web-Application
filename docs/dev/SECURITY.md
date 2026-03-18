Disclaimer: This app is a helper tool and not a substitute for professional medical advice. Always consult a dermatologist for severe allergies.

# Security Best Practices

This document outlines security best practices for the Skincare Allergy Filter application, particularly for production deployments.

---

## Environment Variables

Never commit sensitive configuration values to version control. Use environment variables to manage secrets and environment-specific settings.

### Recommended Tool: django-environ

This project uses [django-environ](https://django-environ.readthedocs.io/) for environment variable management, which provides a clean, type-safe interface for configuration.

#### Installation

```bash
uv add django-environ
```

#### Setup

1. **Create a `.env` file in your project root** (never commit this file):

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# For production PostgreSQL:
# DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

2. **Add `.env` to `.gitignore`**:

```gitignore
# Environment variables
.env
.env.local
.env.*.local
```

3. **Create `.env.example` as a template** (safe to commit):

```bash
# .env.example
DEBUG=False
SECRET_KEY=generate-a-secure-key-for-production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

4. **Update `settings.py`** to use django-environ (see implementation in [settings.py](../skincare_project/settings.py)):

```python
import environ
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),  # Default to False for safety
)

# Read .env file
environ.Env.read_env(BASE_DIR / '.env')

# Security settings from environment
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Database configuration
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}
```

---

## SECRET_KEY Management

The `SECRET_KEY` is used for cryptographic signing and must be kept secret in production.

### Generating a Secure SECRET_KEY

```bash
# Generate a new secret key
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Best Practices

- **Never commit** `SECRET_KEY` to version control
- **Use different keys** for development, staging, and production
- **Rotate keys periodically** (requires session invalidation)
- **Minimum length:** 50+ characters with high entropy

---

## DEBUG Mode

The `DEBUG` setting should **always be `False` in production**.

### Risks of DEBUG=True in Production

- Exposes detailed error pages with sensitive information
- Shows source code snippets in tracebacks
- Reveals database queries and application structure
- Allows potential attackers to probe your application

### Configuration

```python
# Development
DEBUG=True

# Production
DEBUG=False
```

---

## ALLOWED_HOSTS

`ALLOWED_HOSTS` prevents HTTP Host header attacks and must be configured in production.

### Configuration Examples

```bash
# Development
ALLOWED_HOSTS=localhost,127.0.0.1

# Production (single domain)
ALLOWED_HOSTS=example.com,www.example.com

# Production (multiple domains)
ALLOWED_HOSTS=example.com,www.example.com,api.example.com
```

### Common Hosting Providers

```bash
# Heroku
ALLOWED_HOSTS=yourapp.herokuapp.com

# DigitalOcean
ALLOWED_HOSTS=your-droplet-ip,yourdomain.com

# AWS EC2
ALLOWED_HOSTS=ec2-xx-xxx-xxx-xx.compute-1.amazonaws.com,yourdomain.com

# Render
ALLOWED_HOSTS=yourapp.onrender.com,yourdomain.com
```

---

## Database Security

### SQLite (Development Only)

SQLite is suitable for development but **not recommended for production** due to:
- Limited concurrent access
- No built-in user management
- File-based storage limitations

### PostgreSQL (Production)

For production, use PostgreSQL with proper credentials:

```bash
# .env
DATABASE_URL=postgres://username:secure_password@hostname:5432/database_name

# Or with connection pooling:
DATABASE_URL=postgres://username:secure_password@hostname:5432/database_name?conn_max_age=600
```

#### PostgreSQL Security Checklist

- ✅ Use strong passwords (minimum 16 characters, random)
- ✅ Restrict database user permissions (don't use superuser)
- ✅ Enable SSL/TLS for database connections
- ✅ Use connection pooling to limit concurrent connections
- ✅ Regular backups with encryption
- ✅ Keep PostgreSQL version updated

---

## HTTPS/SSL Configuration

Always use HTTPS in production to encrypt data in transit.

### Django Settings for HTTPS

```python
# settings.py (production only)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

Add to your `.env`:

```bash
# .env (production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Production Security Settings

### Complete Production Configuration

Django provides a comprehensive set of security settings for production deployments. These settings should be configured in [settings.py](../skincare_project/settings.py) with conditional logic based on the `DEBUG` setting.

#### Required Security Headers

```python
# settings.py
import os
from pathlib import Path

# ... existing settings ...

# Production Security Settings (conditional on DEBUG=False)
if not DEBUG:
    # HTTPS/SSL Configuration
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)

    # HTTP Strict Transport Security (HSTS)
    SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
    SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=True)

    # Security Headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    # Referrer Policy
    SECURE_REFERRER_POLICY = 'same-origin'

    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF Protection
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Lax'
```

#### Environment Variables for Production

Update your production `.env` file (see [.env.example](../.env.example) for complete template):

```bash
# .env (production)
DEBUG=False
SECRET_KEY=your-unique-production-secret-key-50-plus-characters
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://username:secure_password@hostname:5432/dbname

# Security Settings (optional overrides)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

#### Django Security Check Command

Before deploying to production, **always** run Django's built-in security check:

```bash
# Verify production security configuration
uv run python manage.py check --deploy

# Example output shows missing/incorrect settings:
# WARNINGS:
# ?: (security.W004) You have not set a value for SECURE_HSTS_SECONDS.
# ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True.
```

**Fix all warnings** before deploying. This command checks for:
- Missing `SECURE_*` settings
- Insecure `SECRET_KEY`
- `DEBUG=True` in production
- Missing `ALLOWED_HOSTS` configuration
- Insecure cookie settings
- Missing security middleware

#### Required Dependencies

The security configuration requires `django-environ` for environment variable management:

```bash
# Install django-environ (REQUIRED, not optional)
uv add django-environ
```

This package is **required** for this project (already used in [settings.py](../skincare_project/settings.py)) but may be missing from your dependencies. After installation, run:

```bash
# Sync dependencies
uv sync

# Verify installation
uv run python -c "import environ; print('django-environ installed successfully')"
```

#### Security Settings Checklist

Before production deployment:

- [ ] `DEBUG=False` in production `.env`
- [ ] Strong, unique `SECRET_KEY` (50+ characters, high entropy)
- [ ] `ALLOWED_HOSTS` configured with actual domain(s)
- [ ] All `SECURE_*` settings enabled (SSL_REDIRECT, HSTS, etc.)
- [ ] Secure cookies enabled (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- [ ] Security headers configured (`X_FRAME_OPTIONS`, `CONTENT_TYPE_NOSNIFF`)
- [ ] `uv run python manage.py check --deploy` passes with no warnings
- [ ] HTTPS/SSL certificate installed and verified
- [ ] `django-environ` installed and configured
- [ ] `.env` file excluded from version control (in `.gitignore`)

#### Common Pitfalls

1. **Setting security flags in development:** Only enable `SECURE_SSL_REDIRECT` and secure cookies when HTTPS is properly configured. Development servers (e.g., `runserver`) use HTTP by default.

2. **HSTS without testing:** Once `SECURE_HSTS_PRELOAD=True` is enabled and your site is added to the HSTS preload list, browsers will **permanently** refuse HTTP connections. Test thoroughly before enabling.

3. **Missing django-environ:** The project uses `django-environ` in [settings.py](../skincare_project/settings.py) but it may not be in your dependency list. Install with `uv add django-environ`.

4. **Incorrect ALLOWED_HOSTS:** Must include all domains/subdomains where your app is accessible. Wildcard patterns (e.g., `*.example.com`) are supported.

---

## Security Scanning Tools

This project includes automated security scanning in CI/CD. Run these tools locally before committing:

### Bandit (Python Security Linter)

Scans for common security issues in Python code:

```bash
uv run bandit -r allergies users skincare_project -ll
```

### Safety (Dependency Vulnerability Scanner)

Checks dependencies for known security vulnerabilities:

```bash
uv run safety check
```

### Gitleaks (Secret Detection)

Prevents committing secrets to version control:

```bash
# Install gitleaks first
# Windows: choco install gitleaks
# macOS: brew install gitleaks
# Linux: see https://github.com/gitleaks/gitleaks

gitleaks detect --verbose
```

### Running All Security Checks

```bash
# Run all security checks locally (same as CI)
uv run bandit -r allergies users skincare_project -ll && \
uv run safety check && \
gitleaks detect --verbose
```

---

## Static Files Security

In production, serve static files through a web server (Nginx, Apache) or CDN, not Django.

```python
# settings.py (production)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Collect static files before deployment
# uv run python manage.py collectstatic --noinput
```

---

## Additional Security Headers

Consider adding these security headers in production:

```python
# settings.py (production)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

---

## Secrets Management in Production

For enterprise deployments, consider using dedicated secrets management:

- **AWS Secrets Manager** (AWS deployments)
- **HashiCorp Vault** (multi-cloud)
- **Azure Key Vault** (Azure deployments)
- **Google Secret Manager** (GCP deployments)
- **Doppler** (cloud-agnostic)

---

## Security Checklist

Before deploying to production:

- [ ] `DEBUG = False`
- [ ] Strong, unique `SECRET_KEY` (50+ characters)
- [ ] `ALLOWED_HOSTS` configured with actual domain(s)
- [ ] Using PostgreSQL or production-grade database
- [ ] Database credentials use strong passwords
- [ ] HTTPS/SSL enabled with proper certificates
- [ ] Security headers configured
- [ ] `.env` file excluded from version control
- [ ] Static files served through web server/CDN
- [ ] All dependencies scanned for vulnerabilities
- [ ] Regular security updates scheduled
- [ ] Backup strategy implemented
- [ ] Monitoring and alerting configured

---

## Reporting Security Issues

If you discover a security vulnerability, please email **RJSimpson1004@gmail.com** with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if known)

**Do not** create public GitHub issues for security vulnerabilities.

---

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/6.0/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [django-environ Documentation](https://django-environ.readthedocs.io/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
