import logging

from json import dumps

from typing import Optional, Any

from aio_pika import ExchangeType, Message, DeliveryMode
from aio_pika.abc import AbstractChannel

from domain.Enums.securitytrails.events import SecurityTrailsProducerEvents
from domain.ValueObjects.app import AppUniqueId

from infrastructure.consumer.producer import AsyncProducerBase
from infrastructure.config import SecurityTrailsGatewayConfig


logger = logging.getLogger('SecurityTrailsApiKeyProducer')


class SecurityTrailsApiKeyProducer(AsyncProducerBase):
    """SecurityTrailsApiKeyProducer"""

    def __init__(self, *, config: SecurityTrailsGatewayConfig):
        self.__config = config
        self.__channel: Optional[AbstractChannel] = None

    async def setup(self, channel: AbstractChannel) -> None:
        self.__channel = channel

        exchange_name = self.__config.producer_exchange
        queue_name = self.__config.producer_queue

        await channel.declare_exchange(
            name=exchange_name,
            type=ExchangeType.DIRECT,
            durable=False
        )

        queue = await channel.declare_queue(
            name=queue_name,
            durable=False,
            arguments={
                'x-single-active-consumer': True
            }
        )

        await queue.bind(
            exchange=exchange_name,
            routing_key=self.__config.producer_routing_key
        )

    async def shutdown(self) -> None:
        self.__channel = None

    async def json(self, data: Any) -> None:
        if not self.allowed:
            return logger.warn(f'Could not produce, channel bad state.')

        try:
            jsonified = dumps(data)
        except TypeError as exp:
            return logger.exception(f'Failed to dump data to json: {data}.')

        properties = {
            'content_type': 'application/json',
            'delivery_mode': DeliveryMode.NOT_PERSISTENT
        }

        # Todo: Use built in message_id
        # Todo check pure pika message_id support and implementation
        message = Message(
            body=jsonified.encode(),
            **properties
        )

        await self.__channel.default_exchange.publish(
            message=message,
            routing_key=self.__config.producer_routing_key
        )

    async def fabricate_account(self, _id: AppUniqueId) -> None:
        data = {
            'event': SecurityTrailsProducerEvents.FABRICATE_ACCOUNT,
            '_id': _id.raw()
        }
        return await self.json(data)

    @property
    def allowed(self) -> bool:
        return self.__channel is not None and not self.__channel.is_closed