from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import File
from app.schemas import FileCreate


def list_files(
    db: Session,
    project_id: int | None = None,
    session_id: int | None = None,
) -> list[File]:
    statement = select(File).order_by(File.relative_path)

    if project_id is not None:
        statement = statement.where(File.project_id == project_id)

    if session_id is not None:
        statement = statement.where(File.session_id == session_id)

    return list(db.scalars(statement))


def get_file(db: Session, file_id: int) -> File | None:
    return db.get(File, file_id)


def create_file(db: Session, payload: FileCreate) -> File:
    file = File(**payload.model_dump())

    db.add(file)
    db.commit()
    db.refresh(file)

    return file
