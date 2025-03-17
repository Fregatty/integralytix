import datetime
import io

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
async def test_get_archive_list(http_client: AsyncClient, fake_file_archive):
    response = await http_client.get(url="/api/v1/archive/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_empty_archive_list(http_client: AsyncClient):
    response = await http_client.get(url="/api/v1/archive/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_existing_file_archive_instance(
    http_client: AsyncClient, fake_file_archive
):
    response = await http_client.get(url="/api/v1/archive/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["filepath"] == "correct_filepath"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existing_file_archive_instance(
    http_client: AsyncClient, fake_file_archive
):
    response = await http_client.get(url="/api/v1/archive/2/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_create_file_archive_instance(http_client: AsyncClient, fake_device):
    response = await http_client.get(url="/api/v1/archive/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = {
        "device_id": 1,
        "timestamp_start": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        "timestamp_end": datetime.datetime.now(tz=datetime.UTC).isoformat(),
    }
    response = await http_client.post(url="/api/v1/archive/", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["filepath"] is None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_file_archive_instance_device_not_exists(http_client: AsyncClient):
    response = await http_client.get(url="/api/v1/archive/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = {
        "filepath": "Some filepath",
        "device_id": 1,
        "timestamp_start": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        "timestamp_end": datetime.datetime.now(tz=datetime.UTC).isoformat(),
    }
    response = await http_client.post(url="/api/v1/archive/", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_update_file_archive(http_client: AsyncClient, fake_file_archive):
    body = {
        "filepath": "New filepath",
        "id": 99,
        "timestamp_end": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        "created_at": None,
    }
    response = await http_client.get(url="/api/v1/archive/1/")
    old_obj = response.json()
    response = await http_client.put(url="/api/v1/archive/1/", json=body)
    new_obj = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert new_obj["id"] == 1
    assert new_obj["filepath"] == "correct_filepath"
    assert old_obj["timestamp_end"] != new_obj["timestamp_end"]


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_file_archive(http_client: AsyncClient, fake_file_archive):
    response = await http_client.get(url="/api/v1/archive/1/")
    assert response.status_code == status.HTTP_200_OK
    response = await http_client.delete(url="/api/v1/archive/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await http_client.get(url="/api/v1/archive/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_file_to_archive(http_client: AsyncClient, fake_file_archive):
    files = {"file": ("test_video.mp4", io.BytesIO(b"some binary data"), "video/mp4")}
    response = await http_client.post(
        url="/api/v1/archive/1/upload/",
        files=files,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(loop_scope="session")
async def test_download_file_from_archive(http_client: AsyncClient, fake_file_archive):
    response = await http_client.get(url="/api/v1/archive/1/download_file/")
    assert response.status_code == status.HTTP_200_OK
    assert response.content == b"test bytes string"


@pytest.mark.asyncio(loop_scope="session")
async def test_download_wrong_file(
    http_client: AsyncClient, fake_file_archive_without_file
):
    response = await http_client.get(url="/api/v1/archive/1/download_file/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_download_link(http_client: AsyncClient, fake_file_archive):
    response = await http_client.get(url="/api/v1/archive/1/get_download_link/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "file_link"
