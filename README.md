# intro-to-devops-app

Starter repository for the Intro to DevOps course homework. You will extend this app across the modules (endpoints, database, CI/CD, deployment, security).

**Start here:** [PROJECT-REQUIREMENTS.md](./PROJECT-REQUIREMENTS.md) — what the application must do and how it maps to the course.

## Branching strategy

This repository uses **trunk-based development** for the course work. The `main` branch is the trunk and should stay runnable. Changes should be small and merged frequently, usually through short-lived branches when a pull request or CI check is needed.

For this project, that means:

- Keep `main` as the source of truth.
- Use short-lived branches for focused homework changes when needed.
- Avoid long-running feature or environment branches.
- Before merging to `main`, run the relevant local checks for that homework.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/health`.

For local testing tools, install:

```bash
pip install -r requirements-dev.txt
```

## Run with Docker

```bash
docker build -t fruitapi .
docker run --rm -p 8000:8000 fruitapi
```

Then open `http://127.0.0.1:8000/health`.
