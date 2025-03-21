from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from starlette.responses import StreamingResponse

from src.external_services.storage.base import FileStorage
from src.external_services.storage.minio_s3 import get_file_storage
from src.schemas.file_archive import (
    DeviceFileArchiveRetrieve,
    DeviceFileArchiveCreate,
    DeviceFileArchiveUpdate,
)
from src.schemas.global_schemas import ErrorMessage
from src.services.devices import DeviceService
from src.services.file_archive import ArchiveService

router = APIRouter()


@router.get("/", response_model=list[DeviceFileArchiveRetrieve])
async def archive_list(
    archive_service: Annotated[ArchiveService, Depends()],
):
    return await archive_service.get_list()


@router.post(
    "/{archive_id}/upload/",
    response_model=DeviceFileArchiveRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def upload_file_to_archive(
    archive_id: int,
    file: Annotated[UploadFile, File()],
    storage: Annotated[FileStorage, Depends(get_file_storage)],
    archive_service: Annotated[ArchiveService, Depends()],
):
    archive_instance = await archive_service.get_by_id(archive_id)
    return await archive_service.upload_file_to_storage(
        instance=archive_instance, file=file, storage=storage
    )


@router.get(
    "/{archive_id}/download_file/",
    responses={
        404: {"description": "Not found", "model": ErrorMessage},
        400: {"description": "No File", "model": ErrorMessage},
    },
)
async def download_file(
    archive_id: int,
    storage: Annotated[FileStorage, Depends(get_file_storage)],
    archive_service: Annotated[ArchiveService, Depends()],
):
    archive_instance = await archive_service.get_by_id(archive_id)

    file_generator = await archive_service.download_file(archive_instance, storage)
    return StreamingResponse(
        file_generator,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={archive_instance.filepath}"
        },
    )


@router.get(
    "/{archive_id}/get_download_link/",
    responses={
        404: {"description": "Not found", "model": ErrorMessage},
        400: {"description": "No File", "model": ErrorMessage},
    },
)
async def get_file_download_link(
    archive_id: int,
    storage: Annotated[FileStorage, Depends(get_file_storage)],
    archive_service: Annotated[ArchiveService, Depends()],
) -> str:
    archive_instance = await archive_service.get_by_id(archive_id)

    return await archive_service.get_download_link(archive_instance, storage)


@router.get(
    "/{archive_id}/",
    response_model=DeviceFileArchiveRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def archive_retrieve(
    archive_id: int,
    archive_service: Annotated[ArchiveService, Depends()],
):
    archive_instance = await archive_service.get_by_id(archive_id)
    return archive_instance


@router.post("/", response_model=DeviceFileArchiveRetrieve, status_code=201)
async def archive_create(
    archive_instance: DeviceFileArchiveCreate,
    archive_service: Annotated[ArchiveService, Depends()],
    device_service: Annotated[DeviceService, Depends()],
):
    await device_service.get_by_id(archive_instance.device_id)
    return await archive_service.create(archive_instance)


@router.put(
    "/{archive_id}/",
    response_model=DeviceFileArchiveRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def archive_update(
    archive_id: int,
    archive_instance: DeviceFileArchiveUpdate,
    archive_service: Annotated[ArchiveService, Depends()],
):
    return await archive_service.update(archive_id, archive_instance)


@router.delete(
    "/{archive_id}/",
    response_model=None,
    status_code=204,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def archive_delete(
    archive_id: int,
    archive_service: Annotated[ArchiveService, Depends()],
) -> None:
    await archive_service.delete(archive_id)
