from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import AstroObjectCreate, AstroObjectHeroFileUpdate, AstroObjectRead
from app.services.astro_objects import (
    create_astro_object,
    get_astro_object,
    list_astro_objects,
    set_astro_object_hero_file,
)

router = APIRouter(prefix="/objects", tags=["objects"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[AstroObjectRead])
def read_astro_objects(db: DbSession):
    return list_astro_objects(db)


@router.get("/{object_id}", response_model=AstroObjectRead)
def read_astro_object(object_id: int, db: DbSession):
    astro_object = get_astro_object(db, object_id)

    if astro_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

    return astro_object


@router.post("", response_model=AstroObjectRead, status_code=status.HTTP_201_CREATED)
def create_astro_object_route(payload: AstroObjectCreate, db: DbSession):
    return create_astro_object(db, payload)


@router.patch("/{object_id}/hero-file", response_model=AstroObjectRead)
def update_astro_object_hero_file(
    object_id: int,
    payload: AstroObjectHeroFileUpdate,
    db: DbSession,
):
    try:
        astro_object = set_astro_object_hero_file(db, object_id, payload.hero_file_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if astro_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

    return astro_object
