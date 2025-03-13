from abc import ABC, abstractmethod
from typing import BinaryIO


class FileStorage(ABC):

    @abstractmethod
    async def upload_file(self, payload: BinaryIO, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, path: str) -> bytes | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_file_link(self, path: str) -> str:
        raise NotImplementedError
