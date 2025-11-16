# Calculation Model Assignment

This repository contains:
- SQLAlchemy model for `Calculation` (app/models.py)
- Pydantic schemas (app/schemas.py)
- Factory pattern to select calculation logic (app/factory.py)
- CRUD helpers (app/crud.py)
- Minimal FastAPI app (app/main.py) so the Docker image is runnable
- Unit and integration tests (tests/)
- GitHub Actions workflow to run tests with a PostgreSQL service and push Docker image to Docker Hub
- Reflection document (REFLECTION.md)

## How to run tests locally

1. Create a virtual environment and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run unit tests (use SQLite in-memory):
   ```bash
   pytest -q
   ```

## Docker image

The included GitHub Actions workflow builds and pushes the Docker image to Docker Hub when tests pass.
Replace `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets in your repository for the push step to work.

## Download
The project ZIP is included with this submission.
