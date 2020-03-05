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
    description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/crossnox/YouConfigMe',
    author='CrossNox',
    install_requires=[],
    extras_require={
        'test': ['pytest'],
        'dev': [
            'precommit',
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
