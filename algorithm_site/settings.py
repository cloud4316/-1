import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── СЕКРЕТНЫЙ КЛЮЧ ────────────────────────────────────────────────────────────
# При первом запуске генерируется и сохраняется в secret_key.txt рядом с manage.py
_KEY_FILE = BASE_DIR / 'secret_key.txt'
if _KEY_FILE.exists():
    SECRET_KEY = _KEY_FILE.read_text(encoding='utf-8').strip()
else:
    SECRET_KEY = secrets.token_urlsafe(50)
    _KEY_FILE.write_text(SECRET_KEY, encoding='utf-8')

# ─── РЕЖИМ ─────────────────────────────────────────────────────────────────────
# Переключается файлом DEBUG.lock рядом с manage.py:
#   создай файл  →  DEBUG=True  (отладка, красивые ошибки)
#   удали файл   →  DEBUG=False (продакшн, нет стектрейсов пользователям)
DEBUG = (BASE_DIR / 'DEBUG.lock').exists()

# ─── РАЗРЕШЁННЫЕ ХОСТЫ ─────────────────────────────────────────────────────────
# Принимаем запросы с любого IP — сеть корпуса уже закрыта файрволлом.
# Если хочешь ограничить конкретными IP — замени '*' на список:
# ['192.168.1.*', '10.0.0.*', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']  # Для локальной сети — в prod заменить на IP

# Для шаблонного тега {{ debug }} и dev auto-reload
INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost']

# ─── CSRF ──────────────────────────────────────────────────────────────────────
# Разрешаем POST-запросы из локальной сети (иначе Django блокирует формы)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://192.168.0.0:8000',
    'http://10.0.0.0:8000',
]

# ─── ПРИЛОЖЕНИЯ ────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'works',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',        # отдаёт статику без отдельного сервера
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'works.optimized_middleware.OptimizedTimeTrackingMiddleware',
    'works.optimized_middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = 'algorithm_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'algorithm_site.wsgi.application'

# ─── БАЗА ДАННЫХ ───────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,
            # WAL-режим: несколько пользователей читают одновременно без блокировок
            'init_command': (
                "PRAGMA journal_mode=WAL;"
                "PRAGMA synchronous=NORMAL;"
                "PRAGMA cache_size=10000;"
                "PRAGMA temp_store=MEMORY;"
                "PRAGMA foreign_keys=ON;"
            ),
        },
    }
}

# ─── КЭШ (в памяти, для одного сервера вполне достаточно) ──────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'oaip-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}


# ─── БЭКЕНДЫ АВТОРИЗАЦИИ ────────────────────────────────────────────────────
# Сначала наш (по Фамилия Имя), затем стандартный (по username) для /admin/
AUTHENTICATION_BACKENDS = [
    'works.backends.FullNameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ─── ПАРОЛИ ────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── ЛОКАЛИЗАЦИЯ ───────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ─── СТАТИКА И МЕДИА ───────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'   # куда собирает collectstatic
# Django 5.x: используем STORAGES dict вместо устаревшего STATICFILES_STORAGE
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
# WhiteNoise: отдаёт staticfiles напрямую из Python-процесса, nginx не нужен


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── СЕССИИ ────────────────────────────────────────────────────────────────────
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400          # 24 часа
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False       # HTTP, не HTTPS — ок для закрытой сети
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ─── АУТЕНТИФИКАЦИЯ ────────────────────────────────────────────────────────────
LOGIN_REDIRECT_URL  = 'home'
LOGIN_URL           = '/login/'
LOGOUT_REDIRECT_URL = 'home'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ─── ЛОГИРОВАНИЕ ───────────────────────────────────────────────────────────────
# В DEBUG-режиме — пишем все SQL и ошибки в консоль.
# В продакшне — только WARNING+ в файл с ротацией (макс 5 МБ × 3 файла).
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
        'simple': {'format': '{levelname}: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'django.log',
            'maxBytes': 5 * 1024 * 1024,   # 5 МБ
            'backupCount': 3,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
    },
}

# ─── EMAIL ─────────────────────────────────────────────────────────────────────
# Для отправки уведомлений через Gmail SMTP.
# Установи переменные окружения EMAIL_HOST_USER и EMAIL_HOST_PASSWORD,
# или замени на реальные данные (не коммить в git!).
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD', '')
DEFAULT_FROM_EMAIL = f'AlgorithmMaster <{os.environ.get("DJANGO_EMAIL_USER", "noreply@algorithmmaster.local")}>'
