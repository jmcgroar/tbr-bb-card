"""
Django settings for tbr_bb_card project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6e55b44e-520e-4407-8fd8-68bcdd3cae04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.4']

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tbr_bb_card.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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

WSGI_APPLICATION = 'tbr_bb_card.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

# MLB Stats base URL
MLB_STATS_BASE_URL = "https://statsapi.mlb.com/api/v1/"
# MLB Leagues REST API string
MLB_LEAGUES_STRING = "league?sportId=1"
# MLB Teama REST API string
MLB_TEAMS_STRING = "teams?sportId=1"
# Primary REST API format string.  Retrives both biographical and statistical data
PLAYER_INFO_FORMAT_STRING = "people/{}?hydrate=currentTeam,team,education,draft,stats(group=[{}],type=[yearByYear,career])"
# String to format the image source for the player's headshot
PLAYER_HEADSHOT_FORMAT_STRING = "app/images/headshots/{}_80x120.jpg"
# String to format the player's current team logo
TEAM_LOGO_FORMAT_STRING = "app/images/logos/{}"

# Sample of MLB Players for use in thisdemo application.  Using a mix of pitchers and hitters.  Also included the special situation of Shohei Otani.  He appears twice in the
#  dropdown in the UI -- once as a hitter and again as a pitcher.  A more sophisticated version of this demo would have him listed once and the internal logic would 
#  determine which stats to retrieve based on his primary position.

SAMPLE_MLB_PLAYERS = [
        {'PLAYER_KEY' : '0_', 'NAME' : 'Select a Player', 'TEAM_LOGO' : '', 'STATE' : ''},
        {'PLAYER_KEY' : '668227_H', 'NAME' : 'Arozarena, Randy', 'TEAM_LOGO' : 'tb_110x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '605141_H', 'NAME' : 'Betts, Mookie', 'TEAM_LOGO' : 'lad_95x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '594798_P', 'NAME' : 'deGrom, Jacob', 'TEAM_LOGO' : 'nym_101x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '665489_H', 'NAME' : 'Guerraro, Vlad', 'TEAM_LOGO' : 'tor_97x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '660271_H', 'NAME' : 'Ohtani, Shohei (Hitting)', 'TEAM_LOGO' : 'laa_76x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '660271_P', 'NAME' : 'Ohtani, Shohei (Pitching)', 'TEAM_LOGO' : 'laa_76x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '453286_P', 'NAME' : 'Scherzer, Max', 'TEAM_LOGO' : 'lad_95x101.png', 'STATE' : ''},
        {'PLAYER_KEY' : '545361_H', 'NAME' : 'Trout, Mike', 'TEAM_LOGO' : 'laa_76x101.png', 'STATE' : ''}
    ]