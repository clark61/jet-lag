# Airline API

An API to get statistics on delayed flights across major airports in the United States from 2003 to 2016.

## Prerequisites

Python 3.10

pipenv

## Installation

To install the dependencies:

```bash
pipenv install
```

## Starting the server

```bash
python -m app.main
```

The api will be available at http://localhost:8000/api/airlines

## Testing the API

```bash
python -m pytest app/tests
```
