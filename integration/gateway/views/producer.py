import logging

from json import dumps

from typing import Optional, Any, Dict

from aio_pika import (
    ExchangeType,
    Message,
    DeliveryMode,
    IncomingMessage
)
from aio_pika.abc import AbstractChannel

from infrastructure.consumer.producer import AsyncProducerBase
from infrastructure.config import ServiceGatewayConfig


logger = logging.getLogger('GatewayProducer')


class GatewayProducer(AsyncProducerBase):
    """GatewayProducer"""

    def __init__(self, *, config: ServiceGatewayConfig):
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
            durable=True,
        )

        await queue.bind(
            exchange=exchange_name,
            routing_key=self.__config.producer_routing_key
        )

    async def shutdown(self) -> None:
        self.__channel = None

    async def reply_domain_analysis(self, *, message: IncomingMessage, data: Dict[str, Any]) -> None:
        if not self.allowed:
            return logger.warn(f'Could not produce, channel bad state.')

        try:
            jsonified = dumps(data)
        except TypeError as exp:
            return logger.exception(f'Failed to dump data to json: {data}.')

        properties = {
            'content_type': 'application/json',
            'delivery_mode': DeliveryMode.NOT_PERSISTENT,
            'reply_to': message.reply_to,
            'correlation_id': message.correlation_id
        }

        await self.__channel.default_exchange.publish(
            message=Message(
                body=jsonified.encode(),
                **properties
            ),
            routing_key=self.__config.producer_routing_key
        )

    @property
    def allowed(self) -> bool:
        return self.__channel is not None and not self.__channel.is_closed