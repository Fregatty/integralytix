from typing import BinaryIO

from src.infrastructure.storage.base import FileStorage


class FakeFileStorage(FileStorage):
    file_uploaded = False

    async def upload_file(self, payload: BinaryIO, path: str) -> None:
        return None

    async def get_file(self, path: str) -> bytes | None:
        if path == "correct_filepath":
            payload = b"test bytes string"
            return payload
        return None

    async def delete_file(self, path: str) -> None:
        return None

    async def get_file_link(self, path: str) -> str:
        return "file_link"
