from datetime import datetime
from typing import Any

from pydantic import BaseModel

from src.models.devices import DeviceType
from src.schemas.analytics_modules import ModuleRetrieve


class DeviceBase(BaseModel):
    device_type: DeviceType
    name: str
    source: str
    additional_settings: dict[str, Any] | None


class DeviceCreate(DeviceBase): ...


class DeviceRetrieve(DeviceBase):
    id: int
    created_at: datetime

    # model_config = ConfigDict(from_attributes=True)


class DeviceUpdate(DeviceBase):
    device_type: DeviceType | None = None
    name: str | None = None
    source: str | None = None
    additional_settings: dict[str, Any] | None = None


class DeviceRetrieveWithModules(DeviceRetrieve):
    connected_modules: list[ModuleRetrieve]
