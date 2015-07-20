DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vacations_db',
        'USER': 'user_vacation',
	'PASSWORD': 'v@c@t10ns',
        'HOST': 'localhost',
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 443
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL = True
