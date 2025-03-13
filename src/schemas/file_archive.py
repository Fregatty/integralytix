from datetime import datetime

from pydantic import BaseModel


class DeviceFileArchiveBase(BaseModel):
    timestamp_start: datetime
    timestamp_end: datetime


class DeviceFileArchiveRetrieve(DeviceFileArchiveBase):
    id: int
    device_id: int
    is_deleted: bool
    filepath: str | None


class DeviceFileArchiveCreate(DeviceFileArchiveBase):
    device_id: int


class DeviceFileArchiveUpdate(DeviceFileArchiveBase):
    timestamp_start: datetime | None = None
    timestamp_end: datetime | None = None
