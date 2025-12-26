# Production Deployment Guide

This guide covers deploying the Skincare Allergy Filter application to production environments.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Database Setup](#database-setup)
4. [Static Files](#static-files)
5. [WSGI Server Configuration](#wsgi-server-configuration)
6. [Common Hosting Providers](#common-hosting-providers)
7. [Post-Deployment](#post-deployment)

---

## Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass locally: `uv run pytest`
- [ ] Coverage meets minimum threshold (50%)
- [ ] Security scan passes: `uv run bandit -r allergies users skincare_project`
- [ ] Dependencies are up to date and secure: `uv run safety check`
- [ ] `.env` file configured with production values
- [ ] Database migrations are up to date
- [ ] Static files collected
- [ ] `DEBUG = False` in production environment
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS/SSL certificate obtained

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
sudo apt install python3.14 python3.14-venv postgresql nginx
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
        value: 3.14
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
