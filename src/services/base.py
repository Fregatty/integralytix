from typing import Annotated, Sequence, TypeVar, Generic, Type

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from starlette.exceptions import HTTPException

from src.config.database import get_db_session
from src.models.devices import Device
from src.schemas.devices import DeviceCreate, DeviceUpdate

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
PydanticModelType = TypeVar("PydanticModelType", bound=BaseModel)


class BaseService(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        session: AsyncSession,
    ) -> None:
        self.session: AsyncSession = session
        self.model: Type[ModelType] = model

    async def get_list(self) -> Sequence[ModelType]:
        stmt = Select(self.model).order_by(self.model.id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_by_id(self, obj_id: int) -> ModelType:
        stmt = Select(self.model).where(self.model.id == obj_id)
        result = await self.session.scalar(stmt)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {obj_id} not found",
            )
        return result

    async def create(self, obj_in: PydanticModelType) -> ModelType:
        async with self.session.begin():
            db_obj: ModelType = self.model(**obj_in.model_dump())
            self.session.add(db_obj)
        return db_obj

    async def update(self, obj_id: int, obj_in: PydanticModelType) -> ModelType:
        async with self.session.begin():
            db_obj: ModelType = await self.get_by_id(obj_id)
            for k, v in obj_in.model_dump(exclude_unset=True).items():
                setattr(db_obj, k, v)
        return db_obj

    async def delete(self, obj_id: int) -> None:
        async with self.session.begin():
            db_obj: ModelType = await self.get_by_id(obj_id)
            await self.session.delete(db_obj)
