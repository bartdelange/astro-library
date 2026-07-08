# Backend

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
