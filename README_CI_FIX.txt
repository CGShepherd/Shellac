Shellac CI develop-branch trigger fix

Cause:
branches: was incorrectly unindented from beneath push:, so GitHub Actions
parsed the workflow trigger incorrectly and ran no jobs.

Apply by extracting this ZIP at the repository root, then:
  git diff -- .github/workflows/ci.yml
  git add .github/workflows/ci.yml
  git commit -m "fix(ci): repair develop branch trigger indentation"
  git push origin develop
