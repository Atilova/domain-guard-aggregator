from typing import Protocol

from aio_pika.abc import AbstractChannel


class IAsyncProducer(Protocol):
    """IAsyncProducer"""

    async def setup(self, channel: AbstractChannel):
        pass

    async def shutdown(self):
        """Shutdown the channel."""