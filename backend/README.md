# Backend

## Database Migrations

The backend uses Alembic for schema migrations. The database URL is derived from
`ASTRO_LIBRARY_DATA_DIR` through `app.config.settings`, so the CLI and app startup use
the same SQLite database path.

Apply migrations:

```bash
uv run alembic upgrade head
```

Create a migration after changing SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

FastAPI startup also runs `upgrade head`. Existing databases created before Alembic are
stamped at the baseline revision the first time `init_db()` runs, then upgraded normally.

## Seed Demo Data

The database can be populated with realistic demo astronomy data using Faker and Factory Boy:

```bash
uv run python -m app.seed
```

By default this clears objects, projects, sessions, and files before creating 12 deep-sky
objects with related projects, imaging sessions, calibration frames, logs, and exports.

Useful options:

```bash
uv run python -m app.seed --objects 20 --min-sessions 2 --max-sessions 6 --seed 123
uv run python -m app.seed --no-clear
```
