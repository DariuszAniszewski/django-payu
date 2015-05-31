# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-payu',
    version='0.1.0',
    author=u'Dariusz Aniszewski',
    author_email='dariusz@aniszewski.eu',
    packages=find_packages(),
    url='https://github.com/DariuszAniszewski/django-payu',
    license='TBD',
    description='TBD',
    install_requires=['pytz'],
    zip_safe=False,
)