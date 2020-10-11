# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path

from setuptools import setup

from youconfigme import __version__


def read_readme():
    readme_f = Path(__file__).parent / 'README.md'
    with open(readme_f) as f:
        return f.read()


setup(
    name='youconfigme',
    version=__version__,
    description='YouConfigMe helps you manage config in a pythonic way',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/crossnox/YouConfigMe',
    author='CrossNox',
    install_requires=[],
    extras_require={
        'test': ['pytest'],
        'dev': [
            'pre-commit',
            'mypy',
            'flake8',
            'isort',
            'black',
            'pylint',
            'bump',
            'nox',
        ],
    },
    packages=['youconfigme'],
    classifiers=['Programming Language :: Python :: 3'],
)
