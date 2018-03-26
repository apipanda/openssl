#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

setup(
    name='sslme',
    version='0.0.1',
    description='sslme.',
    author='ojengwa',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['app'],
    install_requires=[
        "marshmallow==2.9.1",
        "redis==2.10.5",
    ],
    extras_require={
        'dev': [
            'pytest==3.1.1',
            'coverage==4.4.1',
            'flake8==3.3.0'
        ]
    },
    zip_safe=True,
)
