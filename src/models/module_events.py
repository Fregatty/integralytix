from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Device, AnalyticsModule
from src.models.consts import EventPriority


class ModuleEvent(Base):
    __tablename__ = "modules_module_event"
    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_path: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    event_timestamp: Mapped[datetime] = mapped_column()
    name: Mapped[str] = mapped_column()
    priority: Mapped[str] = mapped_column(
        default=EventPriority.MEDIUM, server_default=EventPriority.MEDIUM.value
    )
    device_id: Mapped[int] = mapped_column(ForeignKey("devices_device.id"))
    module_id: Mapped[str] = mapped_column(ForeignKey("modules_analytics_module.id"))

    device: Mapped["Device"] = relationship(back_populates="events")
    module: Mapped["AnalyticsModule"] = relationship(back_populates="events")
