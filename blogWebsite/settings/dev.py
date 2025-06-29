# blogWebsite/settings/dev.py
# I have splt the settings into 3 parts so i can continue development even when my site is deployed
from .base import *

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogwebsitedb',
        'USER': 'blog_user',
        'PASSWORD': 'selmonbhoi123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
from decouple import config

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
        }
    }
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dphwkezyr',
    'API_KEY': '783164194962795',
    'API_SECRET': 'vtKERxS6mTngNQan770VKb6Tydo',
}


