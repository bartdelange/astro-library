from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import File, Project
from app.schemas import ProjectCreate


def list_projects(db: Session, object_id: int | None = None) -> list[Project]:
    statement = select(Project).order_by(Project.name)

    if object_id is not None:
        statement = statement.where(Project.object_id == object_id)

    return list(db.scalars(statement))


def get_project(db: Session, project_id: int) -> Project | None:
    return db.get(Project, project_id)


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(**payload.model_dump())

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def set_project_hero_file(
    db: Session,
    project_id: int,
    hero_file_id: int | None,
) -> Project | None:
    project = db.get(Project, project_id)

    if project is None:
        return None

    if hero_file_id is not None:
        hero_file = db.get(File, hero_file_id)

        if hero_file is None:
            raise ValueError("Hero file not found")

        if hero_file.project_id != project.id:
            raise ValueError("Hero file must belong to this project")

    project.hero_file_id = hero_file_id
    db.commit()
    db.refresh(project)

    return project
