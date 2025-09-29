import os
from pathlib import Path
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://arnav:e92jdzBSERj8al5c8eSUTMH7vTJ8zLgT@dpg-d3d7on37mgec73b4m9q0-a.singapore-postgres.render.com/notes_vn5s',
        conn_max_age=600
    )
}   

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATIC_URL = '/static/'
