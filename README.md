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


## Run with MySQL locally

FruitAPI uses the in-memory store by default. For the HW4 database-backed mode, set `FRUITAPI_STORE=mysql` and provide database credentials as environment variables.

Start MySQL in Docker:

```bash
docker network create fruitapi-dev
docker run --rm --name fruitapi-mysql --network fruitapi-dev \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=fruitapi \
  -e MYSQL_USER=fruitapi \
  -e MYSQL_PASSWORD=fruitapi \
  -p 3306:3306 \
  mysql:8.4
```

Run the app locally against that database:

```bash
FRUITAPI_STORE=mysql \
DB_HOST=127.0.0.1 \
DB_PORT=3306 \
DB_NAME=fruitapi \
DB_USER=fruitapi \
DB_PASSWORD=fruitapi \
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Run the app container against the MySQL container:

```bash
docker build -t fruitapi .
docker run --rm --name fruitapi --network fruitapi-dev -p 8000:8000 \
  -e FRUITAPI_STORE=mysql \
  -e DB_HOST=fruitapi-mysql \
  -e DB_PORT=3306 \
  -e DB_NAME=fruitapi \
  -e DB_USER=fruitapi \
  -e DB_PASSWORD=fruitapi \
  fruitapi
```

## Run tests

Unit-style tests run without manually starting the server:

```bash
.venv/bin/python -m pytest app
```

Integration tests require FruitAPI to be running. In one terminal:

```bash
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
BASE_URL=http://127.0.0.1:8000 .venv/bin/python -m pytest tests
```

You can also run integration tests against the Docker container:

```bash
docker build -t fruitapi .
docker run --rm -p 8000:8000 fruitapi
BASE_URL=http://127.0.0.1:8000 .venv/bin/python -m pytest tests
```

## CI/CD

This repository has two GitHub Actions workflows:

- Pull requests to `main` run unit tests only.
- Pushes to `main` run unit tests, build the Docker image, run Dockerized MySQL, run integration tests against the MySQL-backed image, tag it with the SemVer value from `VERSION`, and push it to GitHub Container Registry.

After the PR workflow appears in GitHub, configure the `Unit tests` check as a required status check for `main` branch protection.


## Versioning

Docker image releases use Semantic Versioning from the `VERSION` file. Update that file before an application/runtime release, for example `0.4.0`, and the main workflow publishes `ghcr.io/<owner>/fruitapi:<version>` plus `latest`.

Docs-only or Terraform-only changes do not need a `VERSION` bump because they do not change the application image.

## Deploy with Terraform on AWS

The HW4 Terraform configuration lives in `infra/terraform`. It deploys FruitAPI on ECS Fargate with RDS MySQL and stores the generated database password in AWS Secrets Manager.

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars: set allowed_cidr to your public IP with /32.
terraform init
terraform plan
terraform apply
```

The default container image is `ghcr.io/alain-david-001/fruitapi:0.4.0`. Another user can clone this repo and deploy their own copy by using their own AWS credentials and their own `terraform.tfvars` values.

Do not commit `terraform.tfvars` or Terraform state files. When the deployment is no longer needed, run `terraform destroy` from `infra/terraform` to avoid ongoing AWS costs.
