`Starter / upstream:`  
  `https://github.com/AntonAleksandrov13/intro-to-devops-starter`

# 

# `Plan — Lecture 1`

* `[Mandatory] Fork the course repository and use it as your project for the whole course.`  
* `[Mandatory] Read project-requirements.md and treat it as the specification for FruitAPI.`

# `Code — Lecture 1`

* `[Mandatory] Implement FruitAPI according to project-requirements.md (programming language and framework are your choice unless the brief says otherwise).`  
* `AI tools are welcome; the repository may include guidance for agents (e.g. agents.md). The application itself is not graded on code style, but it must meet the requirements and support the tests and pipelines below.`

# `Build — Lecture 2`

*   `[Mandatory] Use one concrete Git branching strategy in your repository for the rest of the course (e.g. trunk-based, GitHub Flow, or another approach discussed in class).`  
*   `[Mandatory] Dockerize FruitAPI (a Dockerfile that produces a runnable image).`  
*   `[Optional] Keep the image small (e.g. multi-stage build, slim base image, fewer dependencies).`  
*   `[Optional] Generate SBOMs for your Docker image.`

# `Test — Lecture 3`

`Use the reference implementation in the course repository as the shape of what you deliver:`

* `- intro-to-devops-app/test_main.py — unit-style tests`  
  * `- intro-to-devops-app/test_integration.py — integration tests against a running app`

  `Adapt names and paths to your stack; keep the same coverage intent.`

  `Unit tests`

  `Run without manually starting the server (e.g. FastAPI TestClient, or your framework’s equivalent). Reset or isolate application state between tests where needed (see the fixture pattern in the reference).`

  `Minimum parity with test_main.py:`

  * `Response helper: pure logic — the function that builds a fruit JSON object (id + fields) returns the expected structure for given input.`  
  * `List fruits: positive — GET /fruits returns 200, list matches your fixture data.`  
  * `Cheapest fruit: positive — GET /fruits/cheapest returns 200, response is the cheapest fruit for the fixture data.`  
*   `Additional unit tests (mandatory — positive and negative):`  
  * `Positive: If your API supports it: GET /fruits?in_season=true and GET /fruits?in_season=false return only matching rows.`  
  * `Negative: GET /fruits/{id} for an unknown id returns 404 (and response matches your API).`  
  * `Negative: POST /fruits with invalid or incomplete body (e.g. missing name, wrong type for price) returns 422 or the validation status your API uses.`  
  * `Negative: PUT /fruits/{id} or DELETE /fruits/{id} for an unknown id returns 404.`  
  * `Negative: If your API defines it: e.g. GET /fruits/cheapest when there are no fruits returns 404 (or whatever you implement — test that behavior).`  
* `Integration tests`  
* `Use an HTTP client against a running application (local process or container). Base URL from configuration or environment as in the reference.`  
  * `Minimum parity with test_integration.py:`  
    * `Health: positive — GET /health returns 200, body matches your health contract (e.g. {"status": "ok"}).`  
    * `CRUD lifecycle: positive — POST create, GET read, PUT partial update, DELETE, GET again returns 404.`  
    * `Cheapest consistency: positive — price from GET /fruits/cheapest matches the minimum price from GET /fruits.`  
  * `At least one extra integration scenario (mandatory), for example:`  
    * `Positive: After POST, the new fruit appears in GET list.`  
    * `Negative: POST with empty body or wrong Content-Type returns an error status as your API defines.`  
* `How tests connect to CI`  
  * `Pull request workflow: runs unit tests only; results must be visible on the PR (checks and/or comments).`  
  * `main branch workflow: runs unit tests, then build Docker image, then integration tests against that image (as shown in Lecture 3).`

# `Release — Lecture 3`

`[Mandatory] Pipeline on main: unit tests, then build Docker image, then integration tests, then version the image, then push to a container registry (e.g. GitHub Packages).`  
  `[Mandatory] Second pipeline for pull requests: triggered on PR open and on new commits to the PR branch; runs only unit tests; report results on the PR; configure the check so broken PRs cannot be merged (required status check / branch protection), as demonstrated in class.`

# `Deploy - Lecture 4(part 1 and 2)`

* `[Mandatory] Setup Terraform in your project`  
* `[Optional] Replicate Terraform configurations to run Docker image locally`  
  * `Run terraform init and terraform apply commands`  
  * `Read about terraform state rm and terraform state mv commands`  
    * `Try to remove a resources from the state and run terraform plan`  
    * `Try to re-add resource using terraform import and run terraform plan`  
* `[Mandatory] Setup a free tier AWS account`  
* `[Mandatory] Create a Terraform ECS configuration that runs your latest version of FruitAPI`  
* `[Mandatory] Rework fruit data storage - use MySQL instead`  
  * `Adjust your unit and integration tests accordingly. Your CI pipeline should work`  
  * `Database credentials should be provided as environment variables`  
* `[Mandatory] Deploy AWS RDS MySQl database`  
* `[Mandatory] Use the newly deployed database for FruitAPI ECS task`  
  * `Be careful with the database credentials!`  
  * `Explore the options to store them securely inside the AWS account and provide them to ECS task`

# `Deploy - Lecture 5`

* `[Mandatory] Implement FruitAPI logs collection to CloudWatch`  
* `[Mandatory] Run FruitAPI in multiple replicas`  
* `[Mandatory] Deploy ALB to server traffic to FruitAPI`

# `Deploy - Lecture 6`

* `[Mandatory] Turn CI pipeline into CI/CD` 




# `Hand-in for grading — end of course`

  `[Mandatory] Share your repository with the instructor: repository URL, and collaborator access (or equivalent) if the repository is private, so main, workflows, and commit history can be reviewed.`  
  `[Mandatory] Ensure main reflects all mandatory items in this document (the checklist above).`

