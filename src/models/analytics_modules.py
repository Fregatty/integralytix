from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.models import Device, ModuleEvent


class AnalyticsModule(Base):
    __tablename__ = "modules_analytics_module"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column()
    module_type: Mapped[str] = mapped_column()

    module_associations: Mapped[list["AnalyticsModuleDevice"]] = relationship(
        back_populates="module"
    )
    events: Mapped[list["ModuleEvent"]] = relationship(back_populates="module")


class AnalyticsModuleDevice(Base):
    __tablename__ = "module_device_association"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices_device.id"))
    module_id: Mapped[str] = mapped_column(ForeignKey("modules_analytics_module.id"))

    device: Mapped["Device"] = relationship(back_populates="device_associations")
    module: Mapped[AnalyticsModule] = relationship(back_populates="module_associations")
