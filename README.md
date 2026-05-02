# github-actions-capstone

<!-- BADGES START -->
![PR Pipeline](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/github-actions-capstone/pr-pipeline.yml?label=PR%20pipeline&style=flat-square)
![Main Pipeline](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/github-actions-capstone/main-pipeline.yml?label=main%20pipeline&style=flat-square)
![Health Check](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/github-actions-capstone/health-check.yml?label=health%20check&style=flat-square)
![Docker Image](https://img.shields.io/docker/v/YOUR_DOCKERHUB_USERNAME/myapp/latest?label=docker%20hub&style=flat-square&logo=docker)
<!-- BADGES END -->

A production-style CI/CD pipeline built with GitHub Actions as part of the **90 Days of DevOps** challenge (Day 48). The project demonstrates end-to-end automation: from pull request validation through Docker image publishing to a gated production deployment, all wired together using reusable workflows.

---

## What's inside

| File | Purpose |
|------|---------|
| `app.py` | Minimal Flask app with a `/health` endpoint |
| `Dockerfile` | Containerises the app on `python:3.10-slim` |
| `requirements.txt` | Python dependencies (`Flask`, `pytest`) |
| `tests/test_app.py` | Pytest suite that hits the health endpoint |
| `test.sh` | Local smoke test — builds the image, runs it, curls `/health` |

---

## Pipeline architecture

```
PR opened / synchronize
  └─► reusable-build-test  (run_tests: true)
  └─► pr-comment job       (prints branch name, no Docker push)

push to main
  └─► Job 1: reusable-build-test
  └─► Job 2: reusable-docker  →  mydockerhubuser/myapp:latest
                              →  mydockerhubuser/myapp:sha-<short>
  └─► Job 3: deploy           →  environment: production (manual approval)

cron 0 */12 * * *  (+ workflow_dispatch)
  └─► health-check  →  pulls image → runs container → curls /health → GITHUB_STEP_SUMMARY
```

---

## Reusable workflows

### `reusable-build-test.yml`
Called by both the PR and main pipelines. Accepts `python_version` and `run_tests` as inputs; outputs `test_result` (`passed` or `skipped`).

### `reusable-docker.yml`
Logs in to Docker Hub, builds the image, and pushes it with the supplied `image_name` and `tag`. Outputs `image_url` consumed by the deploy job.

---

## Secrets required

Add these in **Settings → Secrets and variables → Actions**:

| Secret | Value |
|--------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_TOKEN` | Docker Hub personal access token |

---

## Local development

```bash
# Run the app directly
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health   # {"status": "ok"}

# Run tests
pytest

# Build and smoke-test the container
./test.sh
```

---

## Production environment

The deploy job targets the `production` environment. To require manual approval before every deployment, go to **Settings → Environments → production → Required reviewers** and add yourself or your team.

---
