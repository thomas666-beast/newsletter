# Русский

## Установка
* Примечание: Перед началом установки вам необходимо установить Python 2.7 с помощью pyenv.

```
git clone git@github.com:thomas666-beast/newsletter.git
cd newsletter
pip install requirements.txt
```

* Сначала вам нужно изменить файл settings.py
```
DOMAIN_NAME = 'domain_of_yourpublic_site'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email_host'
EMAIL_PORT = '2525'
# EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'username_or_email'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'email'
```
* Затем выполните
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
* Откройте другую вкладку и выполните
```
celery -A newsletter_service worker --loglevel=info
```

Наслаждайтесь тестированием!

# English

## install
* Note: Before you start the install you must install python 2.7 via pyenv.

```
git clone git@github.com:thomas666-beast/newsletter.git
cd newsletter
pip install requirements.txt
```

* You must first change your settings.py
```
DOMAIN_NAME = 'domain_of_yourpublic_site'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email_host'
EMAIL_PORT = '2525'
# EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'username_or_email'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'email'
```
* Then
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
* Open other tab and you run
```
celery -A newsletter_service worker --loglevel=info
```

Enjoy testing