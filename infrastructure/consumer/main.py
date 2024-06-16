import logging

import asyncio as aio

from typing import Set, Optional

from utils.cancel_tasks import cancel_all

from aio_pika import connect_robust
from aio_pika.exceptions import AMQPConnectionError
from aio_pika.abc import AbstractRobustConnection, AbstractChannel

from .channel import AsyncChannelBase
from .producer import AsyncProducerBase

from infrastructure.config import RabbitMQConfig


logger = logging.getLogger('AsyncConsumer')


async def _connect(config: RabbitMQConfig, loop: aio.AbstractEventLoop) -> AbstractRobustConnection:
    """Connect to RabbitMQ."""

    connection = await connect_robust(config.uri, loop=loop)
    logger.info('Successfully connected to RabbitMQ.')

    return connection

async def _start_channel_consuming(i_channel: AsyncChannelBase, channel: AbstractChannel):
    """Start consuming messages from a channel."""

    while not channel.is_closed:
        try:
            await i_channel.consume(channel)
        except aio.CancelledError:
            logger.info('Consumption task cancelled.')
            break
        except Exception as exp:
            logger.exception(f'Exception in consumption task.')
            await aio.sleep(5)


class AsyncConsumer:
    """AsyncConsumer"""

    _max_reconnect_interval = 30

    def __init__(self, *, config: RabbitMQConfig, loop: aio.AbstractEventLoop):
        self.__config = config
        self.__loop = loop
        self.__running = False
        self.__connection: Optional[AbstractRobustConnection] = None
        self.__channels: Set[AsyncChannelBase] = set()
        self.__producers: Set[AsyncProducerBase] = set()
        self.__consumer_tasks: Set[aio.Task] = set()
        self.__reconnect_interval = 1

    def add(self, channel: AsyncChannelBase):
        """Add a channel to consume messages from."""

        self.__channels.add(channel)

    def add_producer(self, producer: AsyncProducerBase):
        """"Add a producer to provide connection channel."""

        self.__producers.add(producer)

    async def connect(self):
        """Connect to RabbitMQ."""

        self.__running = True
        while self.__running:
            try:
                self.__connection = await _connect(self.__config, self.__loop)
                self.__connection.reconnect_callbacks.add(self.__on_reconnect)
                self.__connection.close_callbacks.add(self.__on_close)
                await self.__initiate_channels(self.__connection)
                await self.__initiate_producers(self.__connection)
                self.__reconnect_interval = 1
                logger.info('Connection and channels initiated.')
                return
            except AMQPConnectionError as exp:
                logger.warning(f'Connection failed. Retrying in {self.__reconnect_interval} seconds.', exc_info=True)
                await aio.sleep(self.__reconnect_interval)
                self.__reconnect_interval = min(self._max_reconnect_interval,
                                                self.__reconnect_interval * 2)

    async def disconnect(self):
        """Disconnect from RabbitMQ."""

        self.__running = False
        await self.__shutdown_channels()
        await self.__shutdown_producers()
        if self.__connection:
            await self.__connection.close()
        logger.info('Disconnected from RabbitMQ.')

    async def __on_close(self, connection: AbstractRobustConnection, exception: Exception):
        """Callback when RabbitMQ connection had been closed."""

        logger.info(f'RabbitMQ connection failed: {exception}.')
        await self.__shutdown_channels()
        await self.__shutdown_producers()

    async def __on_reconnect(self, connection: AbstractRobustConnection):
        """Callback when reconnected to RabbitMQ."""

        logger.info('Reconnected to RabbitMQ.')
        await self.__initiate_channels(connection)
        await self.__initiate_producers(connection)

    async def __initiate_channels(self, connection: AbstractRobustConnection):
        """Initialize channels for consuming messages."""

        for i_channel in self.__channels:
            if connection.is_closed:
                self.__shutdown_channels()
                return logger.error(f'Unexpected closed connection encountered while setting channel: {i_channel}.')

            channel = await connection.channel()
            try:
                await i_channel.setup(channel)
            except Exception as exp:
                logger.exception(f'Failed to setup channel: {i_channel}.')
                continue

            task = self.__loop.create_task(_start_channel_consuming(i_channel, channel))
            self.__consumer_tasks.add(task)

    async def __shutdown_channels(self):
        """Shutdown all channels and cancel associated tasks."""

        for i_channel in self.__channels:
            await i_channel.shutdown()

        await cancel_all(self.__consumer_tasks)
        self.__consumer_tasks.clear()

    async def __initiate_producers(self, connection: AbstractRobustConnection):
        """Initialize producer to provide channels."""

        for i_producer in self.__producers:
            if connection.is_closed:
                self.__shutdown_producers()
                return logger.error(f'Unexpected closed connection encountered while setting producer: {i_producer}.')

            channel = await connection.channel()
            try:
                await i_producer.setup(channel)
            except Exception as exp:
                logger.exception(f'Failed to setup producer: {i_producer}.')
                continue

    async def __shutdown_producers(self):
        """Shutdown all producer channels and cancel associated tasks."""

        for i_producer in self.__producers:
            await i_producer.shutdown()