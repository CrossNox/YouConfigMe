# YouConfigMe
![PyPI - Downloads](https://img.shields.io/pypi/dm/youconfigme?style=flat-square) ![PyPI](https://img.shields.io/pypi/v/youconfigme?style=flat-square) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/CrossNox/YouConfigMe/Run%20tests?label=tests&style=flat-square) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/CrossNox/YouConfigMe/Run%20linters%20and%20formatters?label=linting&style=flat-square) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black&style=flat-square)

YouConfigMe helps you manage config in a pythonic way.

## Core ideas

### Explicit is better than implicit
There are several ways to define configuration variables, with different levels of explicitness. I prefer to go as close as possible to the [Twelve Factor App](https://12factor.net/config) guide since it's what most people expect anyways.

### Defaults are reasonable
Sometimes you might need a variable to exist even if it hasn't been defined. So, you should be able to provide defaults.

### Types are inherent to the variable
Most of the time, variables are defined as strings, on `.ini` files or as env vars. But what if your variable is an `int`? You should be able to get it as an `int`.

### Sections are good
Config sections are a good thing: separate your config vars under reasonable namespaces.

## Motivation
The main motivation for youconfigme to exist is that most simple config libraries do not take sections into account. And it bugs me greatly.

## Install
Clone this repo, and install it.

```bash
pip install .
```

Or from PyPI.

```bash
pip install YouConfigMe
```

## Development
Start by cloning the repo/forking it.

You should install YouConfigMe's dev packages to help.

```bash
pip install .[dev]
pip install .[test]
```

After that, install the pre-commit hooks:

```bash
pre-commit install
```

This will install several code formatting tools and set them up to run before commits. Also, it will run tests before pushing.

You might find `nox` quite useful to run tests and ensure linting is as expected.

### Docs
To update the docs to the latest changes

```bash
cd docs
make html
```

### Version bumping
This project uses [bump](https://pypi.org/project/bump/) to quickly bump versions.
By default running `bump` will bump the patch version. You can bump minor/major versions like so:

```bash
bump --minor
bump --major
```

## Tests
The `tests` folder contains several tests that run using `pytest` that should give you an idea of how to use this.

## Config discovery
The preferred order should be:

1. Environment variables
2. Config file
3. Default value

## Quickstart

Assume you have an `.ini` file at the root of your project that looks like this:

```ini
[a]
key1=1
key2=2
key7=7

[b]
key3=3
key4=4
```

You can use it like this:

```python3
from youconfigme import AutoConfig
import os

os.environ["A_KEY4"] = "key4value"
os.environ["A_KEY7"] = "key7value"
config = AutoConfig()


print(config.a.key1())				# returns '1'
print(config.a.key1(cast=int))			# returns 1
print(config.a.key2(default='default2val'))	# returns '2'
print(config.a.key3())				# raises ConfigItemNotFound
print(config.a.key3(default='key3value'))	# return 'key3value'
print(config.a.key4())				# returns 'key4value'
print(config.a.key7())				# returns 'key7value'
```
