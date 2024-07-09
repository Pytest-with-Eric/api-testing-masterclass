# Pytest API Testing Masterclass with FastAPI, Postgres and SQLAlchemy - 2 Part Series

## Description

This repository contains the example code for the article series on [Pytest API Testing with FastAPI, SQLAlchemy, Postgres - 1/2](https://pytest-with-eric.com/api-testing/pytest-api-testing-1/).


## Installation

To install the project, you need to have Poetry installed. If you don't have it installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

## Requirements
- Python 3.12
- Poetry

## Usage

### How To Run the Server

To run the server, use the following command:

```shell
$ poetry run uvicorn app.main:app --host localhost --port 8000 --reload
```

This will spin up the server at `http://localhost:8000`

Please follow further instructions on how to run the app in the [blog post](https://pytest-with-eric.com/api-testing/pytest-api-testing-1/).

If you have any questions about the project please raise an Issue on GitHub.