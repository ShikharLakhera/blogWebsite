# blogWebsite/settings/prod.py

from .base import *
import dj_database_url
import os

DEBUG = False

# ⚠️ Update this with your Render domain after deployment (or use '*', but it's not secure)
ALLOWED_HOSTS = ['your-app-name.onrender.com']

# PostgreSQL via DATABASE_URL from Render
DATABASE_URL='postgresql://blog_db_5m1f_user:qG3RLAzODoRjB2obuqdvIeKmvkFSkluY@dpg-d19iudjipnbc73emqtf0-a.oregon-postgres.render.com/blog_db_5m1f'
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(DATABASE_URL)
    )
}

# Whitenoise setup for serving static files in production
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security best practices (optional but recommended)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Make sure secret key is read from environment in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')  # fallback is optional for safety

# Optional: allow Render health checks
# if using `/healthz` or similar endpoints, add them to ALLOWED_HOSTS or middleware exclusions

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")