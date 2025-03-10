from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func, JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.config.database import Base

if TYPE_CHECKING:
    from src.models import ModuleEvent, AnalyticsModuleDevice, AnalyticsModule


class DeviceType(str, Enum):
    CAMERA = "CAMERA"
    MICROPHONE = "MICROPHONE"


class Device(Base):
    __tablename__ = "devices_device"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_type: Mapped[DeviceType] = mapped_column()
    name: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    additional_settings: Mapped[JSON | None] = mapped_column(type_=JSON, nullable=True)

    archive_files: Mapped[list["DeviceFileArchive"]] = relationship(
        back_populates="device"
    )

    events: Mapped[list["ModuleEvent"]] = relationship(back_populates="device")
    device_associations: Mapped[list["AnalyticsModuleDevice"]] = relationship(
        back_populates="device"
    )
    connected_modules: Mapped[list["AnalyticsModule"]] = relationship(
        secondary="module_device_association", viewonly=True
    )


class DeviceFileArchive(Base):
    __tablename__ = "devices_device_file_archive"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices_device.id"))
    filepath: Mapped[str] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(server_default="false")
    timestamp_start: Mapped[datetime] = mapped_column()
    timestamp_end: Mapped[datetime] = mapped_column()

    device: Mapped["Device"] = relationship(back_populates="archive_files")
