from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.file import FileRole


class FileBase(BaseModel):
    project_id: int
    session_id: int | None = None
    relative_path: str
    filename: str
    extension: str | None = None
    file_role: FileRole = FileRole.UNKNOWN
    size_bytes: int | None = None
    modified_at: datetime | None = None
    width: int | None = None
    height: int | None = None


class FileCreate(FileBase):
    pass


class FileRead(FileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
