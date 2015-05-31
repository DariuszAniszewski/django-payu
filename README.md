# Django PayU

Simple Django module for painless integration of PayU online payments in your application.

# Installation

Instalation of `django-payu` is very easy - you just need to get it via pip and modify your settings and urls:

## 1. Install package
```
pip install git+git://github.com/DariuszAniszewski/django-payu.git#egg=django-payu
```

## 2. Edit your `settings.py` 

Add django-pay to `installed_apps`:

```
INSTALLED_APPS = (
    ...
    'django_payu',
    ...
)
```


and to middlewares at very bottom:

```
MIDDLEWARE_CLASSES = (
    ...
    'django_payu.middleware.DjangoPayExceptionsMiddleware'
    ...
)
```

## 3. Add django-pay to your `urls.py`:

```
urlpatterns = [
    ...
    url(r'^django_payu/', include('django_payu.urls')),
    ...
```

# API
