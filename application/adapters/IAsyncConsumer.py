from aio_pika.abc import AbstractChannel

from typing import Protocol

from .IAsyncChannel import IAsyncChannel


class IAsyncConsumer(Protocol):
    """IAsyncConsumer"""
    
    async def add(self, channel: IAsyncChannel):
        pass

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass