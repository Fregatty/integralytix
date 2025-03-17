from typing import Annotated

from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.infrastructure.storage.base import FileStorage
from src.models import DeviceFileArchive
from src.services.base import BaseService

import uuid


class ArchiveService(BaseService[DeviceFileArchive]):
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_db_session)],
    ) -> None:
        super().__init__(DeviceFileArchive, session)

    async def upload_file_to_storage(
        self, instance: DeviceFileArchive, file: UploadFile, storage: FileStorage
    ) -> DeviceFileArchive:
        file_path = f"{uuid.uuid4()}_{file.filename}"
        await storage.upload_file(payload=file.file, path=file_path)
        await file.close()
        instance.filepath = file_path
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def get_download_link(
        self, instance: DeviceFileArchive, storage: FileStorage
    ) -> str:
        if instance.filepath is None:
            raise HTTPException(
                status_code=400,
                detail=f"This instance has no file",
            )
        return await storage.get_file_link(instance.filepath)

    async def download_file(self, instance: DeviceFileArchive, storage: FileStorage):
        if instance.filepath is None:
            raise HTTPException(
                status_code=400,
                detail=f"This instance has no file",
            )
        file = await storage.get_file(instance.filepath)

        if file is None:
            raise HTTPException(
                status_code=404,
                detail="File not found in storage",
            )

        # TODO: Fix this mess somehow?
        async def file_generator():
            yield file

        return file_generator()
