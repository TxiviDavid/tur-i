"""
Django settings for turi project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '6us4ffl1i_fufjzjz4)#s4%ij$0r_j%c@@o=$(9+w5&b#k-7yr'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = bool(int(os.environ.get('DEBUG',0)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS','').split(','),
    )
)

#CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
   'http://localhost:4200',
)
CORS_ALLOWED_ORIGINS = [
'http://localhost:4200'
]
# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'corsheaders',
    'core',
    'user',
    'django.contrib.gis',
    'recursos'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'turi.urls'

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

WSGI_APPLICATION = 'turi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


LEAFLET_CONFIG = {

    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'DEFAULT_ZOOM': 11,
    'DEFAULT_CENTER': (42.9, -2.0),
    'TILES': [('Imagen satelite',
                   'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   {
                       'attribution': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'}),
                  ('OSM', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                   {
                       'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'})],
    #'SPATIAL_EXTENT': (-1.86, 43.055, -2.41, 42.44),

    'PLUGINS': {
            'leaflet.snap': {
                #'css': ['relative/path/to/stylesheet.css', '/root/path/to/stylesheet.css'],
                'js': '/static/leaflet/draw/leaflet.snap.js',
                'auto-include': True,
            },
            'leaflet.geometry': {
                #'css': ['relative/path/to/stylesheet.css', '/root/path/to/stylesheet.css'],
                 'js': '/static/leaflet/draw/leaflet.geometryutil.js',
                'auto-include': True,
            },
            'leaflet.myGeometry': {
                #'css': ['relative/path/to/stylesheet.css', '/root/path/to/stylesheet.css'],
                'js': '/static/leaflet/draw/myGeometry.js',
                'auto-include': True,
            },
            'turf':{
                'js': 'https://npmcdn.com/@turf/turf/turf.min.js',
                'auto-include': True,
            }

        }
    }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'

AUTH_USER_MODEL = 'core.User'
