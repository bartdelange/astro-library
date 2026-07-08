from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import ProjectCreate, ProjectHeroFileUpdate, ProjectRead
from app.services.projects import create_project, get_project, list_projects, set_project_hero_file

router = APIRouter(prefix="/projects", tags=["projects"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ProjectRead])
def read_projects(
    db: DbSession,
    object_id: int | None = Query(default=None),
):
    return list_projects(db, object_id=object_id)


@router.get("/{project_id}", response_model=ProjectRead)
def read_project(project_id: int, db: DbSession):
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project_route(payload: ProjectCreate, db: DbSession):
    return create_project(db, payload)


@router.patch("/{project_id}/hero-file", response_model=ProjectRead)
def update_project_hero_file(
    project_id: int,
    payload: ProjectHeroFileUpdate,
    db: DbSession,
):
    try:
        project = set_project_hero_file(db, project_id, payload.hero_file_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project
