# YouConfigMe

YouConfigMe helps you manage config in a pythonic way.

## Core ideas

### Explicit is better than implicit
There are several ways to define configuration variables, with different levels of explicitness.
From most to less explicit:

- Variable defined in config file
- Variable set as env var

### Defaults are reasonable
Sometimes you might need a variable to exist even if it hasn't been defined. So, you should be able to provide defaults.

### Types are inherent to the variable
Most of the time, variables are defined as strings, on `.ini` files or as env vars. But what if your variable is an `int`? You should be able to get it as an `int`.

### Sections are good
Config sections are a good thing: separate your config vars under reasonable namespaces.

## Install
Clone this repo, and install it.

```terminal
git clone https://github.com/CrossNox/YouConfigMe.git
cd YouConfigMe
pip install .
```

## Development
You can install YouConfigMe's dev packages to help.

```terminal
pip install .[dev]
```

After that, install the pre-commit hooks:

```terminal
pre-commit install
```

This will install several code formatting tools and set them up to run before commits. Also, it will run tests before pushing.

## Tests
The `tests` folder contains several tests that run using `pytest` that should give you an idea of how to use this.
