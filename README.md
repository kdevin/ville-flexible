# Ville Flexible

[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![fastapi](https://img.shields.io/pypi/v/fastapi?color=%252334D058&label=fastapi)](https://pypi.org/project/fastapi)

Ville Flexible is a FastAPI service handling TSO requests.

Project structure is inspired by [Netflix Dispatch](https://github.com/Netflix/dispatch).

## Useful commands

### Create the virtualenv

    virtualenv ville-flexible

### Activate the virtualenv

    source ville-flexible/bin/activate

### Install your dependencies from pyproject.toml

    pip install .

### Install your optional dependencies from pyproject.toml

    pip install .[test]

### Execute pre-commit

    pre-commit run --all-files
