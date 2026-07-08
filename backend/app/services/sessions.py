from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Session as ImagingSession
from app.schemas import SessionCreate


def list_sessions(db: Session, project_id: int | None = None) -> list[ImagingSession]:
    statement = select(ImagingSession).order_by(ImagingSession.date.desc())

    if project_id is not None:
        statement = statement.where(ImagingSession.project_id == project_id)

    return list(db.scalars(statement))


def get_session(db: Session, session_id: int) -> ImagingSession | None:
    return db.get(ImagingSession, session_id)


def create_session(db: Session, payload: SessionCreate) -> ImagingSession:
    imaging_session = ImagingSession(**payload.model_dump())

    db.add(imaging_session)
    db.commit()
    db.refresh(imaging_session)

    return imaging_session


def update_session_notes(
    db: Session,
    session_id: int,
    notes: str | None,
) -> ImagingSession | None:
    imaging_session = db.get(ImagingSession, session_id)

    if imaging_session is None:
        return None

    imaging_session.notes = notes
    db.commit()
    db.refresh(imaging_session)

    return imaging_session
