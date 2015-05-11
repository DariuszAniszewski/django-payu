# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_pay',
    version='0.0.1',
    author=u'Dariusz Aniszewski',
    author_email='dariusz@aniszewski.eu',
    packages=find_packages(),
    url='https://github.com/DariuszAniszewski/django-pay',
    license='TBD',
    description='TBD',
    zip_safe=False,
)