from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AstroObject, File, Project
from app.schemas import AstroObjectCreate


def list_astro_objects(db: Session) -> list[AstroObject]:
    return list(db.scalars(select(AstroObject).order_by(AstroObject.primary_name)))


def get_astro_object(db: Session, object_id: int) -> AstroObject | None:
    return db.get(AstroObject, object_id)


def create_astro_object(db: Session, payload: AstroObjectCreate) -> AstroObject:
    astro_object = AstroObject(**payload.model_dump())

    db.add(astro_object)
    db.commit()
    db.refresh(astro_object)

    return astro_object


def set_astro_object_hero_file(
    db: Session,
    object_id: int,
    hero_file_id: int | None,
) -> AstroObject | None:
    astro_object = db.get(AstroObject, object_id)

    if astro_object is None:
        return None

    if hero_file_id is not None:
        hero_file = db.get(File, hero_file_id)

        if hero_file is None:
            raise ValueError("Hero file not found")

        project = db.get(Project, hero_file.project_id)

        if project is None or project.object_id != astro_object.id:
            raise ValueError("Hero file must belong to a project for this object")

    astro_object.hero_file_id = hero_file_id
    db.commit()
    db.refresh(astro_object)

    return astro_object
