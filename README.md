# intro-to-devops-app

Starter repository for the Intro to DevOps course homework. You will extend this app across the modules (endpoints, database, CI/CD, deployment, security).

**Start here:** [PROJECT-REQUIREMENTS.md](./PROJECT-REQUIREMENTS.md) — what the application must do and how it maps to the course.

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
