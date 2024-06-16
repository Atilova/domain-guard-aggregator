from typing import TypeVar, Protocol, List


T = TypeVar('T', str, bytes)


class IStrBytesExpiryStorage(Protocol[T]):
    """IStrBytesExpiryStorage"""

    async def add(self, item: T, ttl: int):
        pass

    async def exists(self, item: T) -> bool:
        pass

    async def remove(self, item: T) -> None:
        pass

    async def remove_expired(self) -> List[T]:
        pass

    async def all_alive(self) -> int:
        pass