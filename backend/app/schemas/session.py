import datetime as dt

from pydantic import BaseModel, ConfigDict


class SessionBase(BaseModel):
    project_id: int
    date: dt.date
    path: str
    integration_seconds: int | None = None
    light_count: int = 0
    dark_count: int = 0
    flat_count: int = 0
    bias_count: int = 0
    notes: str | None = None


class SessionCreate(SessionBase):
    pass


class SessionNotesUpdate(BaseModel):
    notes: str | None = None


class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: dt.datetime
    updated_at: dt.datetime
