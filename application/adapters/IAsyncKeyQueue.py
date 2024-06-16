from asyncio import Event

from typing import (
    Protocol, 
    TypeVar, 
    Generic, 
    Optional
)


K = TypeVar('K')
V = TypeVar('V')


class IAsyncKeyQueue(Protocol, Generic[K, V]):
    """IAsyncKeyQueue"""

    async def place(self, key: K) -> Event:
        pass

    async def set(self, key: K, result: V) -> None:
        pass

    async def get(self, key: K) -> Optional[V]:
        pass

    @property
    def length(self) -> int:
        pass