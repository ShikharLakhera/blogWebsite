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
