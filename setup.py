# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path

from setuptools import setup


def get_version():
    init_f = Path(__file__).parent / "youconfigme" / "__init__.py"
    with open(init_f) as f:
        for line in f:
            if "__version__" in line:
                return line.split("=")[-1].strip().strip('"')


def read_readme():
    readme_f = Path(__file__).parent / "README.md"
    with open(readme_f) as f:
        return f.read()


setup(
    name="youconfigme",
    version=get_version(),
    description="YouConfigMe helps you manage config in a pythonic way",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/crossnox/YouConfigMe",
    author="CrossNox",
    install_requires=["toml"],
    extras_require={
        "test": ["pytest"],
        "dev": [
            "pre-commit",
            "mypy",
            "flake8",
            "isort",
            "black",
            "pylint",
            "bump",
            "nox",
            "types-toml",
        ],
    },
    packages=["youconfigme"],
    classifiers=["Programming Language :: Python :: 3"],
)
