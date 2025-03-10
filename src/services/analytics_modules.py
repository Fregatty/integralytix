from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.models import AnalyticsModule
from src.services.base import BaseService


class ModuleService(BaseService[AnalyticsModule]):
    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_db_session)]
    ) -> None:
        super().__init__(AnalyticsModule, session)
