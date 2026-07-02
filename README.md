# ci-demo-app-python

The Python/Flask counterpart to `ci-demo-app` (the Node version). Same task API,
same test coverage, same purpose: a reusable sample app for the CI/CD comparison
video series — small enough to run on any free CI tier, with real logic worth
testing and breaking on camera.

## Why a Python version

- Some viewers in the dev-tools/DevOps audience are Python-first — showing the
  same pipeline pattern in a language other than Node broadens who the content
  is useful to.
- Also sets up a legitimate future video: "Same CI Pipeline, Different Language —
  Does the Language Change the Build Time?" using Node vs Python on identical
  pipeline configs.

## What it does

Identical API surface to the Node version:
- `GET /health` — health check
- `GET /api/tasks/` — list tasks, sorted by computed priority score
- `POST /api/tasks/` — create a task (`title`, `due_date`, optional `important`)
- `DELETE /api/tasks/<id>` — remove a task

## Local development

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

flake8 app tests                # lint
pytest                          # test (with coverage)
python -m app.main              # run locally on http://localhost:3000
docker build -t ci-demo-app-python .   # build
```

## Using this repo across videos

Same rule as the Node version: only the CI config file changes between videos
(`.github/workflows/ci.yml`, `.gitlab-ci.yml`, `.circleci/config.yml`) — the app,
tests, and Dockerfile stay identical so comparisons remain apples-to-apples.
