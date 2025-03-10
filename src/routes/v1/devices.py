from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.analytics_modules import ModuleRetrieve
from src.schemas.devices import (
    DeviceRetrieve,
    DeviceCreate,
    DeviceUpdate,
    DeviceRetrieveWithModules,
)
from src.schemas.global_schemas import ErrorMessage
from src.services.analytics_modules import ModuleService
from src.services.devices import DeviceService

router = APIRouter()


@router.get("/", response_model=list[DeviceRetrieve])
async def devices_list(
    device_service: Annotated[DeviceService, Depends()],
):
    return await device_service.get_list()


@router.get(
    "/{device_id}/connected_modules/",
    response_model=list[ModuleRetrieve],
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def list_connected_modules(
    device_id: int, device_service: Annotated[DeviceService, Depends()]
):
    device = await device_service.get_by_id(device_id)
    return await device_service.get_connected_modules(device)


@router.post(
    "/{device_id}/connect_module/",
    response_model=DeviceRetrieveWithModules,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def connect_module(
    device_id: int,
    module_id: int,
    device_service: Annotated[DeviceService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
):
    device = await device_service.get_by_id(device_id)
    module = await module_service.get_by_id(module_id)
    return await device_service.connect_module(device, module)


@router.get(
    "/{device_id}/",
    response_model=DeviceRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def devices_retrieve(
    device_id: int,
    device_service: Annotated[DeviceService, Depends()],
):
    device = await device_service.get_by_id(device_id)
    return device


@router.post("/", response_model=DeviceRetrieve, status_code=201)
async def devices_create(
    device: DeviceCreate, device_service: Annotated[DeviceService, Depends()]
):
    return await device_service.create(device)


@router.put(
    "/{device_id}/",
    response_model=DeviceRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def devices_update(
    device_id: int,
    device: DeviceUpdate,
    device_service: Annotated[DeviceService, Depends()],
):
    return await device_service.update(device_id, device)


@router.delete(
    "/{device_id}/",
    response_model=None,
    status_code=204,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def devices_delete(
    device_id: int,
    device_service: Annotated[DeviceService, Depends()],
) -> None:
    await device_service.delete(device_id)


# TODO: POST Add file to archive
