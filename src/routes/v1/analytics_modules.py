from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.analytics_modules import ModuleRetrieve, ModuleCreate, ModuleUpdate
from src.schemas.global_schemas import ErrorMessage
from src.services.analytics_modules import ModuleService

router = APIRouter()


@router.get("/", response_model=list[ModuleRetrieve])
async def modules_list(
    module_service: Annotated[ModuleService, Depends()],
):
    return await module_service.get_list()


@router.get(
    "/{module_id}",
    response_model=ModuleRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def modules_retrieve(
    module_id: int,
    module_service: Annotated[ModuleService, Depends()],
):
    module = await module_service.get_by_id(module_id)
    return module


@router.post("/", response_model=ModuleRetrieve, status_code=201)
async def modules_create(
    module: ModuleCreate, module_service: Annotated[ModuleService, Depends()]
):
    return await module_service.create(module)


@router.put(
    "/{module_id}",
    response_model=ModuleRetrieve,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def modules_update(
    module_id: int,
    module: ModuleUpdate,
    module_service: Annotated[ModuleService, Depends()],
):
    return await module_service.update(module_id, module)


@router.delete(
    "/{module_id}",
    response_model=None,
    status_code=204,
    responses={404: {"description": "Not found", "model": ErrorMessage}},
)
async def modules_delete(
    module_id: int,
    module_service: Annotated[ModuleService, Depends()],
) -> None:
    await module_service.delete(module_id)
