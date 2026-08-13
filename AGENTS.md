# Repository guidance

## Project purpose and architecture

Astro Library is a self-hosted astrophotography archive. `frontend/` is the React, TypeScript, and
Vite client; `backend/` is the FastAPI, SQLAlchemy, and SQLite service; `docker/` packages the built
client and API. Keep browser concerns in the frontend, persistence and integrations in the backend,
and preserve indexed source files rather than mutating a user's image library.

## Canonical commands

Use npm for `frontend/` and the locked uv environment for `backend/`:

```bash
cd frontend && npm ci
npm run dev
npm run format:check
npm run lint
npm run typecheck
npm run build

cd ../backend && uv sync --locked --all-extras --dev
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

Run actionlint through the pinned container command documented in `CONTRIBUTING.md`. Validate the
Docker build when changing container or release files.

## Code organization and testing

Inspect nearby code and existing conventions before creating a new pattern. Keep API schemas,
database migrations, and generated frontend clients synchronized. Add regression tests for backend
behavior changes; do not make tests depend on live credentials or external services. Keep frontend
components focused and reuse an existing feature or shared boundary when it owns the same concern.

## Git, CI, and dependencies

Use focused branches and pull requests. Commit headers use
`<emoji> <type>(<scope>): <description>`, for example
`⬆️ chore(repo): update dependencies`; keep the complete header within 100 characters. Never bypass
hooks. CI must retain formatting, lint, type checking, builds, tests, and workflow validation.
Dependabot updates run weekly; keep lockfiles with dependency changes and retain project-specific
version exclusions only when compatibility requires them.

Never commit `.env`, databases, credentials, tokens, indexed libraries, or generated local data.
Use least-privilege workflow permissions and never expose release credentials to pull requests.

## Change discipline

Keep changes scoped, preserve unrelated user work, update documentation with intended commands or
behavior, inspect existing repository conventions before creating new patterns, and run all
relevant validation before completion.
