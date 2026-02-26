# Ville Flexible

[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![fastapi](https://img.shields.io/pypi/v/fastapi?color=%252334D058&label=fastapi)](https://pypi.org/project/fastapi)

Ville Flexible is a FastAPI service handling TSO requests.

# Getting started

## Configure your environment

First, create your virtualenv and activate it

    virtualenv ville-flexible
    source ville-flexible/bin/activate

Then, install your dependencies from pyproject.toml

    pip install .

You can also install your optional dependencies

    pip install .[test]

## Run the project

Start your FastAPI server

    uvicorn ville_flexible.main:app --host 0.0.0.0 --port 8000

Server is started at: http://127.0.0.1:8000<br>
Access to the Swagger docs at: http://127.0.0.1:8000/docs

## Containerize the project

Build the docker image

    docker build -t ville-flexible:latest .

Run the docker image

    docker run -d -p 127.0.0.1:8000:8000 ville-flexible

## Useful commands

Execute pre-commit

    pre-commit run --all-files

Start your FastAPI server and watch for changes

    fastapi dev ville_flexible/main.py

# Implementation and reasoning

## Project structure

Project structure is inspired by [Netflix Dispatch](https://github.com/Netflix/dispatch).

`main.py` creates the FastAPi server object.<br>
`api.py` creates the main router by grouping all application routers.<br>
`dependencies.py` declares service dependencies so that dependency injection is possible.<br>
`logging.py` takes care of the logging configuration.<br>

Code is grouped by its subject. Each app follows the same structure:
- `views.py` is the API, declaring its own router
- `service.py` is focused on business logic and data access
- `models.py` is the data layer
- `exceptions.py` contains custom exceptions

## Data

Assets have been generated thanks to AI.<br>
It is hardcoded in a JSON list, which is read and loaded in a list at startup.

## Reasoning for the algorithm

My first thoughts was about having a weighted algorithm:
- computing the cost of activating one kW for an asset
- rating the asset based on its volume and the requested volume

### Cheapest comes first

You compute a rate from 0 to infinity for each available asset, i.e. volume divided by requested volume.
Being equal to 1 or higher means the requested volume is covered by the current available asset.<br>
So the cheapest of them all is going to be the selected asset.

#### Drawbacks

The sum of two smaller assets might be cheaper than the cheapest asset covering the request volume.

### Cheapest sum of assets

You compute a rate from 0 to infinity for each available asset, i.e. volume divided by requested volume.
Being lower to 1 means the requested volume is covered by a sum of available assets.<br>
You then compute the kilowatt price for each asset. You pick the cheapest prices until you reach the requested volume.

#### Drawbacks

If you do the sum of all your assets having a rate lower to 1, your requested volume might not be covered.<br>
Also, you only consider kilowatt price for each asset.
So a cheap asset might provide too much volume compared to others, while you only need a portion of it

### Best of both wolrds

You combine the two strategies and make them compete against each other.
The lower activation cost wins. In some cases, only one might be applicable, so it wins by default.
