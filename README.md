# Django Pay

Simple Django module for easy integration of online payments in your application.

### Supporting Providers

- PayU


### Planned

- others ;)


# Installation

## 1. Install package
```
pip install git+git://github.com/DariuszAniszewski/django-pay.git#egg=django-pay
```

## 2. Edit your `settings.py` 

Add django-pay to `installed_apps`:

```
INSTALLED_APPS = (
    ...
    'djangopay',
    ...
)
```


and to middlewares at very bottom:

```
MIDDLEWARE_CLASSES = (
    ...
    'djangopay.middleware.DjangoPayExceptionsMiddleware'
)
```

...