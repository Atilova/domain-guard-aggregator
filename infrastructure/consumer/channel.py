from abc import ABC, abstractmethod

from aio_pika.abc import AbstractChannel


class AsyncChannelBase(ABC):
    """Base class for asynchronous channels."""

    @abstractmethod
    async def setup(self, channel: AbstractChannel):
        """Setup the channel for consuming messages."""

        raise NotImplemented

    @abstractmethod
    async def consume(self, channel: AbstractChannel):
        """Start consuming messages from the channel."""

        raise NotImplemented

    async def shutdown(self):
        """Shutdown the channel."""