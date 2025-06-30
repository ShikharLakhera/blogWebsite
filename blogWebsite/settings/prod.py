# blogWebsite/settings/prod.py
from .base import *
import dj_database_url
import os
from decouple import config
import cloudinary
import cloudinary.uploader
import cloudinary.api

DEBUG = False

# Update this with your Render domain after deployment
ALLOWED_HOSTS = ['blogwebsite-b7xr.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://blogwebsite-b7xr.onrender.com']

# PostgreSQL via DATABASE_URL from Render
DATABASE_URL = 'postgresql://blog_db_5m1f_user:qG3RLAzODoRjB2obuqdvIeKmvkFSkluY@dpg-d19iudjipnbc73emqtf0-a.oregon-postgres.render.com/blog_db_5m1f'
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', DATABASE_URL)
    )
}

# Whitenoise setup for serving static files in production
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security best practices
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Secret key from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Add Cloudinary apps - ORDER MATTERS!
INSTALLED_APPS = [
    # Your existing apps from base.py
    'cloudinary_storage',  # Must be before 'django.contrib.staticfiles'
    'cloudinary',
] + INSTALLED_APPS  # Add to the beginning

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

# File Storage Configuration for Django 4.2+
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.ManifestStaticFilesStorage",
    }

}

# Keep this for backward compatibility
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Media URL (can be left as default since Cloudinary handles URLs)
MEDIA_URL = '/media/'

# Site ID for Django sites framework
SITE_ID = 1

# Social Authentication
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        }
    }
}