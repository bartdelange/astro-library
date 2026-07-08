from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import FileCreate, FileRead
from app.services.files import create_file, get_file, list_files

router = APIRouter(prefix="/files", tags=["files"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[FileRead])
def read_files(
    db: DbSession,
    project_id: int | None = Query(default=None),
    session_id: int | None = Query(default=None),
):
    return list_files(db, project_id=project_id, session_id=session_id)


@router.get("/{file_id}", response_model=FileRead)
def read_file(file_id: int, db: DbSession):
    file = get_file(db, file_id)

    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return file


@router.post("", response_model=FileRead, status_code=status.HTTP_201_CREATED)
def create_file_route(payload: FileCreate, db: DbSession):
    return create_file(db, payload)
