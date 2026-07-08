from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.session import Session


class FileRole(StrEnum):
    LIGHT = "LIGHT"
    DARK = "DARK"
    FLAT = "FLAT"
    BIAS = "BIAS"
    EXPORT = "EXPORT"
    EDIT = "EDIT"
    INTERMEDIATE = "INTERMEDIATE"
    PROJECT_METADATA = "PROJECT_METADATA"
    SESSION_METADATA = "SESSION_METADATA"
    NOTE = "NOTE"
    LOG = "LOG"
    UNKNOWN = "UNKNOWN"


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True, nullable=False)
    session_id: Mapped[int | None] = mapped_column(ForeignKey("sessions.id"), index=True)
    relative_path: Mapped[str] = mapped_column(String, index=True, nullable=False)
    filename: Mapped[str] = mapped_column(String, index=True, nullable=False)
    extension: Mapped[str | None] = mapped_column(String, index=True)
    file_role: Mapped[FileRole] = mapped_column(
        Enum(FileRole),
        index=True,
        nullable=False,
        default=FileRole.UNKNOWN,
    )
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    modified_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)

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

    project: Mapped[Project] = relationship(
        "Project",
        back_populates="files",
        foreign_keys=[project_id],
    )
    session: Mapped[Session | None] = relationship("Session", back_populates="files")
