from typing import Annotated, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.config.database import get_db_session
from src.models import Device, AnalyticsModule, AnalyticsModuleDevice
from src.services.base import BaseService


class DeviceService(BaseService[Device]):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_db_session)]
    ) -> None:
        super().__init__(Device, session)

    async def get_connected_modules(self, device: Device) -> Sequence[AnalyticsModule]:
        stmt = (
            Select(AnalyticsModule)
            .join(
                AnalyticsModuleDevice,
                AnalyticsModule.id == AnalyticsModuleDevice.module_id,
            )
            .join(
                Device,
                Device.id == AnalyticsModuleDevice.device_id,
            )
            .where(Device.id == device.id)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def connect_module(self, device: Device, module: AnalyticsModule) -> Device:
        existing_connection = await self.session.scalars(
            Select(AnalyticsModuleDevice).where(
                AnalyticsModuleDevice.module_id == module.id,
                AnalyticsModuleDevice.device_id == device.id,
            )
        )
        if existing_connection.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Connection already exists",
            )
        connection = AnalyticsModuleDevice(device=device, module=module)
        self.session.add(connection)
        await self.session.commit()
        return await self.session.scalar(
            Select(Device)
            .options(selectinload(Device.connected_modules))
            .where(Device.id == device.id)
        )
