"""
Django settings for bobjiang project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o30=mn+6+^s!*96$!*0nq6r-i0+_s)uw-+kz%&-fdcw30pkfoj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]

APPEND_SLASH = True

# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comments',
    'ckeditor',
    'ckeditor_uploader',
    #'xadmin',
    #'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bobjiang.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bobjiang.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj-bobjiang-v2',
        'USER': 'root',
        'PASSWORD': 'Jiangbo86',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            'autocommit': True,
        },
    }

}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = '/home/bob/djproject/bobjiang/blog/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    'default': {
         'toolbar': (['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
                    ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-','Print','SpellChecker','Scayt'],
                    ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat','-','Maximize', 'ShowBlocks', '-',"CodeSnippet", 'Subscript', 'Superscript'],
                    ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                     'HiddenField'],
                    ['Bold', 'Italic', 'Underline', 'Strike', '-'],
                    ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
                    ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
                    ['Link', 'Unlink', 'Anchor'],
                    ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
                    ['Styles', 'Format', 'Font', 'FontSize'],
                    ['TextColor', 'BGColor'],
 
                    ),
        'extraPlugins': 'codesnippet',
    }
}

