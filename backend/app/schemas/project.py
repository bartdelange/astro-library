from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    object_id: int
    name: str
    slug: str
    path: str
    hero_file_id: int | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectHeroFileUpdate(BaseModel):
    hero_file_id: int | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
