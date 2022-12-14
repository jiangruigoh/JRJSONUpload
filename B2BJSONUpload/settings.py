"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2+06dv0)hylx2sy3hikg1hh^l$2@y00%wuxu$dh28(wz^hpkbh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Add in new
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    #'djoser',
    'django_filters',

    #Folder
    'main',
    '_mc_allcode.apps.McAllcodeConfig',    
    '_mc_category.apps.McCategoryConfig',
    '_mc_companyprofile.apps.McCompanyprofileConfig',
    '_mc_department.apps.McDepartmentConfig',
    '_mc_set_group.apps.McSetGroupConfig',
    '_mc_set_group_dept.apps.McSetGroupDeptConfig',
    '_mc_subdept.apps.McSubdeptConfig',
    '_ml_itembarcode.apps.MlItembarcodeConfig',
    '_ml_itemmaster.apps.MlItemmasterConfig',
    '_ml_itemmaster_block_by_branch.apps.MlItemmasterBlockByBranchConfig',
    '_ml_itemmaster_branch_stock.apps.MlItemmasterBranchStockConfig',
    '_ml_itemmaster_itemtype.apps.MlItemmasterItemtypeConfig',
    '_ml_itemmaster_listed_branch.apps.MlItemmasterListedBranchConfig',
    '_ml_itemmaster_miscellaneous.apps.MlItemmasterMiscellaneousConfig',   
    '_ml_itemmaster_othersinfo.apps.MlItemmasterOthersinfoConfig', 
    '_ml_itemmaster_pricetype.apps.MlItemmasterPricetypeConfig', 
    '_ml_itemmaster_replenishment.apps.MlItemmasterReplenishmentConfig', 
    '_ml_itemmastersupcode.apps.MlItemmastersupcodeConfig', 
    '_ml_location.apps.MlLocationConfig',
    '_ml_locationgroup.apps.MlLocationgroupConfig',
    '_ml_supcus.apps.MlSupcusConfig',
    '_ml_supcus_branch.apps.MlSupcusBranchConfig',
    '_ml_sysuser.apps.MlSysuserConfig',
    '_mc_department_v2.apps.McDepartmentV2Config',
    '_mc_subdept_v2.apps.McSubdeptV2Config',
    '_mc_category_v2.apps.McCategoryV2Config',
    '_ts_simain.apps.TsSimainConfig',
    '_ts_sichild.apps.TsSichildConfig',
    '_ts_sipayment.apps.TsSipaymentConfig',
]


####ADD
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework'
}

ALLOWED_HOSTS=['*']  ####ADD

CORS_ORIGIN_ALLOW_ALL = True  ####ADD


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'backend',
#        'USER': 'panda_dev',
#        'PASSWORD': 'Dev@3323966',
#        'HOST': '192.168.9.246',
#        'PORT': 3306,
#    }

# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'b2b_summary',
        'USER': 'panda_backup',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}



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

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
