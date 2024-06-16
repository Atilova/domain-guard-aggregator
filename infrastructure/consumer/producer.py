from abc import ABC, abstractmethod

from aio_pika.abc import AbstractChannel


class AsyncProducerBase(ABC):
    """Base class for asynchronous producers."""

    @abstractmethod
    async def setup(self, channel: AbstractChannel):
        """Setup the channel for consuming messages."""

        raise NotImplemented

    async def shutdown(self):
        """Shutdown the channel."""