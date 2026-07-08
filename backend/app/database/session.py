from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database.base import Base

DB_PATH = settings.data_dir / "astro-library.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

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


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Import models so SQLAlchemy registers them before create_all()
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    drop_legacy_session_count_columns()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
