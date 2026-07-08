from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.project import Project


class EnrichmentSource(StrEnum):
    SIMBAD = "SIMBAD"
    NED = "NED"
    VIZIER = "VizieR"


class EnrichmentSourceList(TypeDecorator[list[EnrichmentSource]]):
    impl = JSON
    cache_ok = True

    def process_bind_param(
        self,
        value: list[EnrichmentSource | str] | None,
        dialect: Any,
    ) -> list[str]:
        if value is None:
            return []

        return [EnrichmentSource(source).value for source in value]

    def process_result_value(
        self,
        value: list[str] | None,
        dialect: Any,
    ) -> list[EnrichmentSource]:
        if value is None:
            return []

        return [EnrichmentSource(source) for source in value]


class AstroObject(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    primary_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String)
    object_type: Mapped[str | None] = mapped_column(String, index=True)
    constellation: Mapped[str | None] = mapped_column(String, index=True)
    distance_ly: Mapped[float | None] = mapped_column(Float)
    distance_display: Mapped[str | None] = mapped_column(String)
    angular_size_arcmin: Mapped[float | None] = mapped_column(Float)
    angular_size_display: Mapped[str | None] = mapped_column(String)
    magnitude: Mapped[float | None] = mapped_column(Float)
    ra: Mapped[float | None] = mapped_column(Float)
    dec: Mapped[float | None] = mapped_column(Float)
    coordinate_system: Mapped[str | None] = mapped_column(String)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    catalog_ids: Mapped[dict[str, str]] = mapped_column(JSON, default=dict, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    enrichment_sources: Mapped[list[EnrichmentSource]] = mapped_column(
        EnrichmentSourceList,
        default=list,
        nullable=False,
    )
    last_enriched_at: Mapped[datetime | None] = mapped_column(DateTime)
    hero_file_id: Mapped[int | None] = mapped_column(
        ForeignKey("files.id", name="fk_objects_hero_file_id_files", use_alter=True),
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    projects: Mapped[list[Project]] = relationship(
        "Project",
        back_populates="object",
        cascade="all, delete-orphan",
    )
    hero_file: Mapped[File | None] = relationship(
        "File",
        foreign_keys=[hero_file_id],
        post_update=True,
    )
