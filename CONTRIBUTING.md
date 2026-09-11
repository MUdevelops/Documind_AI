# Contributing to DocuMind

1. Fork the repo and create a feature branch.
2. Install dev dependencies: `pip install -e ".[dev]"`.
3. Run `ruff check .` and `pytest` before opening a PR.
4. Keep route handlers thin; put business logic in `app/services/`.
5. Add/extend tests for any behavior change, including auth/ownership checks.
6. Open a PR against `main` describing the change and testing performed.
