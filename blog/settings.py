"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import django_heroku
import dj_database_url #setup the database for heroku
from decouple import config

# from dotenv import load_dotenv
# load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     # my Apps
    "BlogApp",
    "marketing",
    #3rd party App
    "taggit",
    "ckeditor",
    "crispy_forms",
    # "django_ajax",
    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    'allauth.socialaccount.providers.github',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# DATABASE_URL="postgres://dckejeheevvcfx:74f6d68d56b04789ed9be1ac5ae80525fc33b4b9697ea3243e02d1b67f9ce9bd@ec2-34-225-167-77.compute-1.amazonaws.com:5432/d6vkcutlkikgcl"
# DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
CRISPY_TEMPLATE_PACK = "bootstrap4"

#TinyMce TextEditor
CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        
},
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': "auto",
},
}
CKEDITOR_UPLOAD_PATH = "uploads/"
# "Email Backend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'abdullahnasser6@gmail.com'
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL= False
EMAIL_PORT = '587'

#Django allauth
SITE_ID = 1
ACCOUNT_CONFIRM_EMAIL_ON_GET =True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_AUTHENTICATION_METHOD = ("username_email")
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX ="Site"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT =2
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT =120
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =True
ACCOUNT_LOGIN_ON_PASSWORD_RESET =True
LOGIN_REDIRECT_URL ="/"
ACCOUNT_LOGOUT_REDIRECT_URL ="/"
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =True
ACCOUNT_USERNAME_VALIDATORS = 'BlogApp.validators.custom_username_validators'
ACCOUNT_USER_MODEL_EMAIL_FIELD ="email"
ACCOUNT_FORMS ={"signup":"BlogApp.forms.MyCustomSignupForm",

  }
ACCOUNT_SESSION_REMEMBER =True
#social accounts
SOCIALACCOUNT_AUTO_SIGNUP =True
SOCIALACCOUNT_EMAIL_VERIFICATION =ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_QUERY_EMAIL =ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS =True
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]
  

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': config("google_client_id"),
            'secret': config("google_secret"),
            'key': ''
        }
    },
    'facebook': {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'APP': {
        'client_id':config("facebook_client_id"),
        'secret':config("facebook_secret"),
        'key': '',
       
    }
},
   'github': {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'APP': {
        'client_id':config("git_client_id"),
        'secret': config("git_secret"),
        'key': '',
       
    }
}


}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT= os.path.join(BASE_DIR,'static')

MEDIA_URL = "/media/"

MEDIA_ROOT =os.path.join(BASE_DIR,'media')

STATICFILES_DIRS=[
   os.path.join(BASE_DIR,'static_in_env'),
]


STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"


django_heroku.settings(locals())
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


GOOGLE_ANALYTICS_KEY="G-TTSCG3GJHY"
