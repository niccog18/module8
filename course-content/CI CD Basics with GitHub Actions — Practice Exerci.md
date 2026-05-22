# CI/CD Basics with GitHub Actions — Practice Exercise

## Set Up CI for Your RAG Project

**Objective:** Add a GitHub Actions CI workflow to your RAG project that runs tests and verifies Docker builds on every push.

**Time:** 25 minutes

**What you’ll do:**

1. Create `.github/workflows/ci.yml` in your RAG project
2. Configure the workflow to trigger on pushes to `main` and pull requests
3. Include at least **two jobs:**
    - **test** — Set up Python, install dependencies, run pytest on your backend tests
    - **docker** — Build both backend and frontend Docker images, verify they were created
4. Write at least **3 simple tests** in `backend/tests/test_api.py`:
    - Test that `/` returns 200
    - Test that `/health` returns 200 with expected fields
    - Test that `/stats` returns 200 with a `document_count` field
5. Push to GitHub and verify the workflow runs in the Actions tab

**Deliverable:** A working CI pipeline visible in your GitHub repository’s Actions tab.

**Why this exercise?** CI is a professional practice that makes your portfolio project stand out. It also catches bugs before they become problems in your containerized deployment.