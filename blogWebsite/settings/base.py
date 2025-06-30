# blogWebsite/settings/base.py

import os
from pathlib import Path
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-h+_-ix+&be!=)6ws(iy)fh6_=*gllljb#_xjlz@$5$2h&$xip*'

INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'blog',
    'blogHome',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'blogWebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogWebsite.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "blogWebsite/static")]

# TinyMCE and CSP Settings
CSP_DEFAULT_SRC = ("'self'", "https://cdn.tiny.cloud")
CSP_SCRIPT_SRC = ("'self'", "https://cdn.tiny.cloud", "'unsafe-inline'", "'unsafe-eval'")

# Authentication
LOGIN_URL = reverse_lazy('blog:login')
LOGIN_REDIRECT_URL = reverse_lazy('blog:home')

#for integrating google login
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
]
#Very important-so the problem was site id was set to 1 but in db it didnt exiated site with pk=2 was there
SITE_ID = 2

ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # * means required
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_VERIFICATION_METHOD = 'optional'  # or 'mandatory', if you want strict email checks

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'  # needed if you're not verifying via email
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET= True

