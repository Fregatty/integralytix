from datetime import datetime

from pydantic import BaseModel

from src.models.consts import EventPriority


class EventBase(BaseModel):
    artifact_path: str
    description: str
    event_timestamp: datetime
    name: str
    priority: EventPriority
    device_id: int
    module_id: int


class EventCreate(EventBase): ...


class EventRetrieve(EventBase):
    id: int


class EventUpdate(EventBase):
    artifact_path: str | None = None
    description: str | None = None
    name: str | None = None
    priority: EventPriority | None = None
    device_id: int | None = None
    module_id: int | None = None
