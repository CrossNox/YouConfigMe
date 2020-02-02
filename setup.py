# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from setuptools import setup

from youconfigme import __version__

setup(
    name='youconfigme',
    version=__version__,
    description='',
    url='https://github.com/crossnox/YouConfigMe',
    author='CrossNox',
    install_requires=[],
    extras_require={
        'dev': [
            'precommit',
            'pytest',
            'mypy',
            'flake8',
            'isort',
            'black',
            'pylint',
            'sphinx',
            'bump',
            'sphinx_rtd_theme',
            'm2r',
        ],
    },
    packages=['youconfigme'],
    classifiers=['Programming Language :: Python :: 3'],
)
