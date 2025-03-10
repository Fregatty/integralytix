from fastapi import APIRouter

from src.routes.v1.devices import router as devices_router
from src.routes.v1.analytics_modules import router as modules_router

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(devices_router, tags=["devices"], prefix="/devices")
router_v1.include_router(modules_router, tags=["modules"], prefix="/modules")
