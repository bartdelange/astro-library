from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.astro_object import EnrichmentSource


class AstroObjectBase(BaseModel):
    slug: str
    primary_name: str
    display_name: str | None = None
    object_type: str | None = None
    constellation: str | None = None
    distance_ly: float | None = None
    distance_display: str | None = None
    angular_size_arcmin: float | None = None
    angular_size_display: str | None = None
    magnitude: float | None = None
    ra: float | None = None
    dec: float | None = None
    coordinate_system: str | None = None
    aliases: list[str] = Field(default_factory=list)
    catalog_ids: dict[str, str] = Field(default_factory=dict)
    description: str | None = None
    enrichment_sources: list[EnrichmentSource] = Field(default_factory=list)
    last_enriched_at: datetime | None = None
    hero_file_id: int | None = None


class AstroObjectCreate(AstroObjectBase):
    pass


class AstroObjectHeroFileUpdate(BaseModel):
    hero_file_id: int | None = None


class AstroObjectRead(AstroObjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
