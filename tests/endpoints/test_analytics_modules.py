import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
async def test_get_module_list(http_client: AsyncClient, fake_module):
    response = await http_client.get(url="/api/v1/modules/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_empty_module_list(http_client: AsyncClient):
    response = await http_client.get(url="/api/v1/modules/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_existing_module(http_client: AsyncClient, fake_module):
    response = await http_client.get(url="/api/v1/modules/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Test module"
    assert response.json()["created_at"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existing_module(http_client: AsyncClient, fake_module):
    response = await http_client.get(url="/api/v1/modules/2/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_create_module(http_client: AsyncClient):
    response = await http_client.get(url="/api/v1/modules/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = {
        "name": "My module",
        "module_type": "PEOPLE_COUNTER",
    }
    response = await http_client.post(url="/api/v1/modules/", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "My module"
    assert response.json()["module_type"] == "PEOPLE_COUNTER"
    assert response.json()["created_at"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_update_module(http_client: AsyncClient, fake_module):
    body = {
        "name": "New Name",
        "id": 99,
        "module_type": None,
        "created_at": None,
    }
    response = await http_client.get(url="/api/v1/modules/1/")
    old_obj = response.json()
    response = await http_client.put(url="/api/v1/modules/1/", json=body)
    new_obj = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert new_obj["id"] == 1
    assert old_obj["created_at"] == new_obj["created_at"]
    assert new_obj["name"] == "New Name"
    assert old_obj["module_type"] == new_obj["module_type"]


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_module(http_client: AsyncClient, fake_module):
    response = await http_client.get(url="/api/v1/modules/1/")
    assert response.status_code == status.HTTP_200_OK
    response = await http_client.delete(url="/api/v1/modules/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await http_client.get(url="/api/v1/modules/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
