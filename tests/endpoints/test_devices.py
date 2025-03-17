from datetime import datetime

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
async def test_get_device_list(http_client: AsyncClient, fake_device):
    response = await http_client.get(url="/api/v1/devices/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_existing_device(http_client: AsyncClient, fake_device):
    response = await http_client.get(url="/api/v1/devices/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Test Camera"
    assert response.json()["source"] == "rtsp://localhost:1111"
    assert response.json()["created_at"]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existing_device(http_client: AsyncClient, fake_device):
    response = await http_client.get(url="/api/v1/devices/1/")
    assert response.status_code == status.HTTP_200_OK
    response = await http_client.get(url="/api/v1/devices/2/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_create_device(http_client: AsyncClient):
    response = await http_client.get(url="/api/v1/devices/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = {
        "name": "Test obj 1",
        "source": "rtsp://1.2.3.4:1234",
        "device_type": "CAMERA",
        "additional_settings": {"setting_1": 1, "setting_2": 2},
    }
    response = await http_client.post(url="/api/v1/devices/", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test obj 1"
    assert response.json()["additional_settings"] == {"setting_1": 1, "setting_2": 2}


@pytest.mark.asyncio(loop_scope="session")
async def test_update_device(http_client: AsyncClient, fake_device):
    body = {
        "name": "New Name",
        "id": 99,
        "additional_settings": None,
        "device_type": None,
        "created_at": datetime.now().isoformat(),
    }
    response = await http_client.get(url="/api/v1/devices/1/")
    old_obj = response.json()
    response = await http_client.put(url="/api/v1/devices/1/", json=body)
    new_obj = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert new_obj["id"] == 1
    assert old_obj["created_at"] == new_obj["created_at"]
    assert new_obj["name"] == "New Name"
    assert old_obj["device_type"] == new_obj["device_type"]
    assert new_obj["additional_settings"] is None


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_device(http_client: AsyncClient, fake_device):
    response = await http_client.get(url="/api/v1/devices/1/")
    assert response.status_code == status.HTTP_200_OK
    response = await http_client.delete(url="/api/v1/devices/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await http_client.get(url="/api/v1/devices/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_connect_module(http_client: AsyncClient, fake_device, fake_module):
    response = await http_client.post(
        url=f"/api/v1/devices/1/connect_module/?module_id=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["connected_modules"][0]["name"] == "Test module"


@pytest.mark.asyncio(loop_scope="session")
async def test_unable_to_connect_module_twice(
    http_client: AsyncClient, fake_device, fake_module
):
    response = await http_client.post(
        url=f"/api/v1/devices/1/connect_module/?module_id=1"
    )
    assert response.status_code == status.HTTP_200_OK
    response = await http_client.post(
        url=f"/api/v1/devices/1/connect_module/?module_id=1"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio(loop_scope="session")
async def test_list_connected_modules(
    http_client: AsyncClient, fake_device, fake_module
):
    response = await http_client.get(url=f"/api/v1/devices/1/connected_modules/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    await http_client.post(url=f"/api/v1/devices/1/connect_module/?module_id=1")
    response = await http_client.get(url=f"/api/v1/devices/1/connected_modules/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["name"] == "Test module"
    assert len(response.json()) == 1
