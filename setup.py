#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cerberus',
        'coverage',
        'flake8',
        'flake8-bandit',
        'flake8-bugbear',
        'flake8-builtins',
        'flake8-eradicate',
        'flake8-pytest-style',
        'flask',
        'flask-cors',
        'flask-marshmallow',
        'flask-sqlalchemy',
        'gunicorn',
        'marshmallow-sqlalchemy',
        'pyjwt',
        'pytest',
        'python-dotenv',
        'wemake-python-styleguide',
    ],
)
