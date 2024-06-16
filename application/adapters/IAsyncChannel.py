from aio_pika.abc import AbstractChannel

from typing import Protocol


class IAsyncChannel(Protocol):
    """IAsyncChannel"""

    async def setup(self, channel: AbstractChannel):
        pass

    async def consume(self, channel: AbstractChannel):
        pass

    async def shutdown(self):
        pass