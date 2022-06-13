from .local import *

#DIR IP -  DOM PROD
HOST = 'DIR_IP_PROD'

# CONFIG EMAIL PRODI
EMAIL_HOST = 'smtp-server'  # Your Mailhog Host
EMAIL_PORT = '1025'


TWILIO_SECRET_KEY='super_secret_key_to_prod'

# DATABASE PROD
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}