from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.astro_object import AstroObject
    from app.models.file import File
    from app.models.session import Session


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, index=True, nullable=False)
    path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hero_file_id: Mapped[int | None] = mapped_column(ForeignKey("files.id"), index=True)

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

    object: Mapped[AstroObject] = relationship("AstroObject", back_populates="projects")
    sessions: Mapped[list[Session]] = relationship(
        "Session",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    files: Mapped[list[File]] = relationship(
        "File",
        back_populates="project",
        cascade="all, delete-orphan",
        foreign_keys="File.project_id",
    )
    hero_file: Mapped[File | None] = relationship(
        "File",
        foreign_keys=[hero_file_id],
        post_update=True,
    )
