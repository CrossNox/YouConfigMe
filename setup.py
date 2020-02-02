# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from setuptools import setup

setup(
    name='youconfigme',
    version='0.0.1',
    description='',
    url='https://github.com/crossnox/YouConfigMe',
    author='CrossNox',
    install_requires=[],
    extras_require={
        'dev': ['precommit', 'pytest', 'mypy', 'flake8', 'isort', 'black', 'pylint'],
    },
    packages=['youconfigme'],
    classifiers=['Programming Language :: Python :: 3'],
)
