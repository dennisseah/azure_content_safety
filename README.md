# azure_content_safety

azure_content_safety is a Python library for interacting with the Azure Content Moderator API. It provides a simple interface for sending images and text to the API and retrieving the results.

## Prerequisites

- python 3.12 and above
- install poetry (https://python-poetry.org/docs/)
- install vscode (https://code.visualstudio.com/)

## Setup

1. Clone the repository
2. `cd azure_content_safety` (root directory of this git repository)
3. `python -m venv .venv`
4. `poetry install` (install the dependencies)
5. code . (open the project in vscode)
6. install the recommended extensions (cmd + shift + p -> `Extensions: Show Recommended Extensions`)
7. `pre-commit install` (install the pre-commit hooks)

## Infrastructure

To deploy Azure content safety service.
see [infrastructure](./infrastructure/README.md)

## Samples
see `./samples` directory for examples on how to use the library.
content for the samples is from https://learn.microsoft.com/en-us/azure/ai-services/content-safety/

## Unit Test Coverage

```sh
python -m pytest -p no:warnings --cov-report term-missing --cov=azure_content_safety tests
```

## Dependency Injection

In order to handle the dependency injection, we have a `hosting.py` file in the `azure_content_safety` module.
`lagom` is a simple dependency injection library that we use in this project.