from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from app.config import BACKEND_DIR, settings

DB_PATH = settings.data_dir / "astro-library.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
ALEMBIC_INI_PATH = BACKEND_DIR / "alembic.ini"
BASELINE_REVISION = "20260708_0001"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def drop_legacy_session_count_columns() -> None:
    legacy_columns = {"light_count", "dark_count", "flat_count", "bias_count"}
    inspector = inspect(engine)

    if not inspector.has_table("sessions"):
        return

    existing_columns = {column["name"] for column in inspector.get_columns("sessions")}
    columns_to_drop = legacy_columns & existing_columns

    if not columns_to_drop:
        return

    with engine.begin() as connection:
        for column in sorted(columns_to_drop):
            connection.execute(text(f"ALTER TABLE sessions DROP COLUMN {column}"))


def get_alembic_config() -> Config:
    config = Config(str(ALEMBIC_INI_PATH))
    config.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
    return config


def database_has_tables() -> bool:
    return bool(inspect(engine).get_table_names())


def database_has_revision() -> bool:
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        return context.get_current_revision() is not None


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    alembic_config = get_alembic_config()

    if database_has_tables() and not database_has_revision():
        drop_legacy_session_count_columns()
        command.stamp(alembic_config, BASELINE_REVISION)

    command.upgrade(alembic_config, "head")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
