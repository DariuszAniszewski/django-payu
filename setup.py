# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-payu',
    version='0.2.3',
    author=u'Dariusz Aniszewski',
    author_email='dariusz@aniszewski.eu',
    packages=find_packages(),
    url='https://github.com/DariuszAniszewski/django-payu',
    license='TBD',
    description='Minimalistic PayU wrapper.',
    install_requires=['pytz==2015.2', 'requests==2.7.0'],
    zip_safe=False,
)