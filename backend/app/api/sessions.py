from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import SessionCreate, SessionNotesUpdate, SessionRead
from app.services.sessions import create_session, get_session, list_sessions, update_session_notes

router = APIRouter(prefix="/sessions", tags=["sessions"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[SessionRead])
def read_sessions(
    db: DbSession,
    project_id: int | None = Query(default=None),
):
    return list_sessions(db, project_id=project_id)


@router.get("/{session_id}", response_model=SessionRead)
def read_session(session_id: int, db: DbSession):
    imaging_session = get_session(db, session_id)

    if imaging_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    return imaging_session


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session_route(payload: SessionCreate, db: DbSession):
    return create_session(db, payload)


@router.patch("/{session_id}/notes", response_model=SessionRead)
def patch_session_notes(
    session_id: int,
    payload: SessionNotesUpdate,
    db: DbSession,
):
    imaging_session = update_session_notes(db, session_id, payload.notes)

    if imaging_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    return imaging_session
