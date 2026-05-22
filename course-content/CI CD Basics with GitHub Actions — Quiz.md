# CI/CD Basics with GitHub Actions — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** What does Continuous Integration (CI) do?

- A) Deploys code to production automatically
- B) Automatically runs tests, builds, and checks on every code push, catching problems before they reach the main codebase
- C) Continuously writes code for you
- D) Integrates your code with other programming languages

> **Answer: B** — CI automates quality checks on every push or pull request. Tests run, Docker images build, code is linted — all without human intervention. If anything fails, the developer is notified immediately. This prevents broken code from reaching the main branch and catches issues while they’re fresh.
> 

---

**Question 2:** Where do GitHub Actions workflow files live in your repository?

- A) In the root directory as `actions.yml`
- B) In `.github/workflows/` as `.yml` files
- C) In a `ci/` directory
- D) They’re configured in GitHub’s web UI only

> **Answer: B** — GitHub Actions reads workflow files from `.github/workflows/`. You can have multiple workflow files (e.g., `ci.yml`, `deploy.yml`). They’re checked into your repo like any other code, meaning CI configuration is version-controlled alongside your application.
> 

---

**Question 3:** Why include a Docker build step in your CI pipeline?

- A) To deploy containers automatically
- B) To verify that the Dockerfile is valid and the image builds successfully, catching build errors before deployment
- C) Docker builds are faster in CI
- D) It’s required by GitHub

> **Answer: B** — A Docker build step catches Dockerfile errors, missing files, and dependency issues in CI. If you can’t build the image, you can’t deploy it. Catching this in CI (before merge) is much better than discovering it during deployment.
>