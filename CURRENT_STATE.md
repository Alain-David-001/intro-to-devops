# Current State — DevOps HWs

Last updated: 2026-05-24

## Project goal

Build the course FruitAPI step by step, following `PROJECT-REQUIREMENTS.md` and the lecture checklist in `Homeworks.md`.

## Homework progress

- Lecture 1 plan: complete. Course docs were reviewed: `README.md`, `AGENTS.md`, `PROJECT-REQUIREMENTS.md`, and `Homeworks.md`.
- Lecture 1 code: complete for HW1. FruitAPI is implemented with health, list, create, get one, update, delete, optional `in_season` filtering, optional `limit`, and `/fruits/cheapest`.
- Manual verification: complete for HW1. Health, list, cheapest, limit, create, update, and delete were checked locally against the running API.
- Lecture 3 test: complete for test requirements. Unit-style tests and integration tests have been added and verified locally; integration tests were also verified against the Docker container.
- Lecture 3 CI/release: in progress. GitHub Actions workflows were added for PR unit tests, PR result comments, and main branch unit/build/integration/publish pipeline. Image versioning uses SemVer from the `VERSION` file.
- Branch protection verification: complete. A temporary failing PR test caused the required `PR Unit Tests / Unit tests` check to fail and blocked merging.
- Lecture 2 build: complete for mandatory HW2 scope. Trunk-based development was selected and documented; Dockerfile was added; Docker image was built and run locally; `GET /health` worked from the container.

## Implementation details

- Branching strategy: trunk-based development. `main` is the trunk and should stay runnable; use short-lived branches for focused changes when PR/CI checks are needed.
- Stack: Python 3.12 + FastAPI + Uvicorn.
- Runtime dependencies are pinned in `requirements.txt`; dev/test dependencies are pinned in `requirements-dev.txt`.
- Docker image definition lives in `Dockerfile`; build context exclusions live in `.dockerignore`.
- Application code lives under `app/`, as required.
- Root entrypoint is `main.py`, which creates the FastAPI app and includes the API router.
- Current data storage is an in-memory `FruitStore` in `app/store.py`.
- Seed data:
  - Apple, price 1.25, in season.
  - Banana, price 0.75, in season.
  - Mango, price 2.50, not in season.

- Release version source: `VERSION` currently contains `0.3.0`.

## Current API surface

- `GET /health` returns `{"status": "ok"}`.
- `GET /fruits` lists fruits. Optional query params: `in_season=true|false` and `limit=1` or larger.
- `POST /fruits` creates a fruit and returns it with an `id`.
- `GET /fruits/cheapest` returns the cheapest fruit or 404 if the store is empty.
- `GET /fruits/{id}` returns one fruit or 404.
- `PUT /fruits/{id}` updates provided fruit fields or returns 404.
- `DELETE /fruits/{id}` deletes a fruit and returns 204, or 404 if missing.

## Verification notes

- Unit tests passed locally on 2026-05-24: `.venv/bin/python -m pytest app` -> 11 passed.
- Integration tests passed locally against running app on 2026-05-24: `BASE_URL=http://127.0.0.1:8000 .venv/bin/python -m pytest tests` -> 4 passed.
- Integration tests passed locally against Docker container on 2026-05-24 with the same `BASE_URL` command -> 4 passed.
- PR branch protection was verified on 2026-05-24: an intentional failing test made the required PR check fail and disabled merging until fixed.
- Test file syntax check passed with Python AST parsing in Codex.
- `python3 -m compileall app main.py` passed after Dockerfile changes.
- Docker image verification passed locally on 2026-05-24: `docker build -t fruitapi .` and `docker run --rm -p 8000:8000 fruitapi` worked, and `GET /health` returned `{"status":"ok"}`.
- Runtime and dev dependencies were installed into `.venv`.
- Direct Python smoke check of route functions passed:
  - `health()` returns `{"status": "ok"}`.
  - `list_fruits()` returns the three seeded fruits.
  - `get_cheapest_fruit()` returns Banana.
- Local manual HTTP checks passed on 2026-05-24 using `.venv/bin/python -m uvicorn main:app --reload`: `GET /health` returned 200 with `{"status": "ok"}`, `GET /fruits` worked, `GET /fruits/cheapest` worked, `GET /fruits?limit=...` worked, and `POST /fruits` successfully created Orange with id 4, `PUT /fruits/4` updated its price, and `DELETE /fruits/4` returned 204 No Content. `GET /` and `GET /favicon.ico` return 404, which is expected because no homepage or favicon endpoint is required.

## Next steps

- Push `hw3-tests`, open a PR, confirm the PR unit-test workflow reports on the PR, then configure that check as required for `main`.
- After merge, confirm the main workflow builds, integration-tests, versions, and pushes the Docker image to GHCR.
