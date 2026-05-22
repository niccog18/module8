# CI/CD Basics with GitHub Actions — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/ci-setup/`

Compare your solution to the reference. Key things to check:

- Does the workflow file live at `.github/workflows/ci.yml`?
- Does it trigger on both push and pull_request to main?
- Do the test and docker jobs run successfully?
- Do your tests use `TestClient` from FastAPI for endpoint testing?
- Does the Actions tab show green checkmarks?

Your specific tests and workflow details may differ. The important thing is that CI runs automatically and catches real problems.