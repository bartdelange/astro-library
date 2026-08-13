# Contributing

Thanks for taking the time to improve Astro Library.

Astro Library is early-stage software. Small, focused issues and pull requests are the easiest to review.

## Ways to Help

- Report bugs with reproduction steps and screenshots when useful.
- Suggest features that fit the goal of organizing an astrophotography archive.
- Improve documentation, installation notes, and example workflows.
- Submit focused fixes with tests where the behavior is non-trivial.

## Development Setup

Backend:

```bash
cd backend
uv sync --locked --all-extras --dev
cp .env.example .env
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Frontend:

```bash
cd frontend
npm ci
npm run typecheck
npm run lint
npm run format:check
```

Run the app locally:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

```bash
cd frontend
npm run dev
```

The frontend development server proxies `/api` requests to `http://127.0.0.1:8000`.

Validate GitHub Actions from the repository root:

```bash
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:1.7.7
```

## Pull Requests

- Keep changes scoped to one concern.
- Include a clear description of the problem and the fix.
- Add or update tests for behavior changes.
- Run the relevant checks before opening the PR.
- Use the repository commit format, for example `🐛 fix(frontend): handle empty object library`.

## Commit Messages

The repository checks commit messages with:

```text
<emoji> <type>(<scope>): <message>
```

Allowed types are `chore`, `docs`, `feat`, `fix`, `refactor`, `release`, `revert`, and `test`. Keep
the complete header within 100 characters and use the narrowest meaningful scope.
