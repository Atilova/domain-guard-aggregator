# from aioredis.connection import EncodableT
from typing import Protocol, TypeVar


T = TypeVar('T', str, bytes)


class IAsyncSetStorage(Protocol[T]):
    """IAsyncSetStorage"""

    async def add(self, encodable: T) -> None:
        pass

    async def remove(self, encodable: T) -> None:
        pass

    async def exists(self, encodable: T) -> bool:
        pass