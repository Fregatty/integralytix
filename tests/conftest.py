import datetime
import os
import pathlib
import sys

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from src.config.database import get_db_session
from src.config.project_settings import settings
from src.consts import ModuleType
from src.external_services.storage.minio_s3 import get_file_storage
from src.main import app
from src.models import Device, AnalyticsModule
from src.models.devices import DeviceType, DeviceFileArchive
from tests.mocks.fake_storage import FakeFileStorage

sys.dont_write_bytecode = True

tables_for_trunc = [
    "devices_device",
    "devices_device_file_archive",
    "module_device_association",
    "modules_analytics_module",
    "modules_module_event",
]


@pytest.fixture(scope="session", autouse=True)
def setup_migrations():
    os.environ["TESTING"] = "1"
    alembic_config: Config = Config(
        pathlib.Path(__file__).resolve().parent.parent / "alembic.ini"
    )
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")
    os.environ.pop("TESTING")


test_engine: AsyncEngine = create_async_engine(url=str(settings.test_db_url))

test_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def _get_test_db_session():
    async with test_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


def _get_test_file_storage():
    return FakeFileStorage()


@pytest.fixture()
async def db_session():
    test_engine: AsyncEngine = create_async_engine(url=str(settings.test_db_url))

    test_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    yield test_session_factory


@pytest.fixture()
async def http_client() -> AsyncClient:
    app.dependency_overrides[get_db_session] = _get_test_db_session
    app.dependency_overrides[get_file_storage] = _get_test_file_storage
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        # base_url="http://127.0.0.1",
    ) as client:
        yield client
    app.dependency_overrides = {}


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(db_session):
    async with db_session() as session:
        for table in tables_for_trunc:
            await session.execute(
                text(f"""TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;""")
            )

        await session.commit()


@pytest.fixture()
async def fake_device(db_session):
    async with db_session() as session:
        device = Device(
            device_type=DeviceType.CAMERA,
            name="Test Camera",
            source="rtsp://localhost:1111",
            additional_settings={"a": 1, "b": 2},
        )
        session.add(device)
        await session.commit()
    yield


@pytest.fixture()
async def fake_module(db_session):
    async with db_session() as session:
        name: str

        module = AnalyticsModule(
            name="Test module",
            module_type=ModuleType.PEOPLE_COUNTER.value,
        )
        session.add(module)
        await session.commit()
    yield


@pytest.fixture()
async def fake_file_archive(db_session, fake_device):
    async with db_session() as session:
        name: str

        instance = DeviceFileArchive(
            device_id=1,
            filepath="correct_filepath",
            timestamp_start=datetime.datetime.now(tz=datetime.UTC),
            timestamp_end=datetime.datetime.now(tz=datetime.UTC),
        )
        session.add(instance)
        await session.commit()
    yield


@pytest.fixture()
async def fake_file_archive_without_file(db_session, fake_device):
    async with db_session() as session:
        name: str

        instance = DeviceFileArchive(
            device_id=1,
            filepath="",
            timestamp_start=datetime.datetime.now(tz=datetime.UTC),
            timestamp_end=datetime.datetime.now(tz=datetime.UTC),
        )
        session.add(instance)
        await session.commit()
    yield
