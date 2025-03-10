from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.models.consts import ModuleType


class BaseModule(BaseModel):
    name: str
    module_type: ModuleType

    model_config = ConfigDict(use_enum_values=True)


class ModuleRetrieve(BaseModule):
    id: int
    created_at: datetime


class ModuleCreate(BaseModule): ...


class ModuleUpdate(BaseModule):
    name: str | None = None
    module_type: ModuleType | None = None
