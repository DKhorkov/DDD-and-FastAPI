# DDD and FastAPI

This project is a tutorial on how to implement Domain Driven Design using FastAPI, 
and was also created to demonstrate the advantages of this approach.

All commands should be executed in project's root directory:

## Getting started

To run application via source files, use next commands:

```bash
python -m venv venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn src.app:app --env-file .env --host <Ypur host here> --port <Your por here> --reload 
```

### Run via IDE:

Run ```src/main.py``` file, using project's root directory as Working Directory and 
provide path to .env.local file as the environments file.

## Linters

```bash
flake8 ./ -v
```

## Type Checkers

```bash
mypy ./
```

## Alembic

To create new migration use next command:
```bash
alembic revision -m "<your migration description here>" --autogenerate
```

To migrate use next command:
```bash
alembic upgrade head
```

To downgrade database use next command:
```bash
alembic downgrade <Number of migrations>  # -1, -2 or base to downgrade to start point
```

## Tests

To run tests use next command in project's root directory:
```bash
pytest -v
```

To check tests coverage use next commands in project's root directory and 
open ```htmlcov/index.html``` file in browser:
```bash
coverage run -m pytest -v
coverage html
```
