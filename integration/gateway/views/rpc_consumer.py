import logging

import asyncio as aio
from aio_pika import ExchangeType, IncomingMessage
from aio_pika.abc import AbstractChannel, AbstractQueue

from typing import (
    Optional,
    Set,
    Tuple,
    Optional,
    Coroutine
)

from utils.cancel_tasks import cancel_all

from integration.gateway.adapters.IDomainController import IDomainController
from integration.gateway.models.request import RpcRequest
from integration.gateway.models.events import ConsumerEvents

from infrastructure.config import ServiceGatewayConfig
from infrastructure.consumer.channel import AsyncChannelBase
from infrastructure.consumer.extensions.json_processor import process_as_json


logger = logging.getLogger('RpcGatewayChannel')


def _validate_request(message: IncomingMessage) -> Tuple[bool, Optional[RpcRequest]]:
    """_validate_request"""

    is_json, body = process_as_json(message)
    if not is_json: return False, None

    event = body.get('event')
    is_valid_event = ConsumerEvents.is_valid(event)
    if not is_valid_event:
        logger.warning(f'Received unknown event: {event}.')
        return False, None

    if message.correlation_id is None or message.reply_to is None:
        logger.warning(f'Request missing `correlation_id` or `reply_to` property on: {event}.')
        return False, None

    data = body.get('data')
    if data is None or not isinstance(data, dict):
        logger.warning(f'Request missing proper data object on: {event}.')
        return False, None

    return True, RpcRequest(
        data=data,
        event=event,
        message=message
    )


class RpcGatewayChannel(AsyncChannelBase):
    """RpcGatewayChannel"""

    def __init__(self, *,
        config: ServiceGatewayConfig,
        loop: aio.AbstractEventLoop,
        controller: IDomainController
    ):
        self.__config = config
        self.__loop = loop
        self.__controller = controller
        self.__aio_tasks: Set[aio.Task] = set()
        self.__queue: Optional[AbstractQueue] = None

    async def setup(self, channel: AbstractChannel) -> None:
        exchange_name = self.__config.consumer_exchange
        queue_name = self.__config.consumer_queue

        await channel.set_qos(prefetch_count=10)

        await channel.declare_exchange(
            name=exchange_name,
            type=ExchangeType.DIRECT,
            durable=False
        )

        self.__queue = await channel.declare_queue(
            name=queue_name,
            durable=False
        )

        await self.__queue.bind(
            exchange=exchange_name,
            routing_key=self.__config.consumer_routing_key
        )

    async def consume(self, channel: AbstractChannel) -> None:
        if self.__queue is None: return

        message: IncomingMessage
        async for message in self.__queue.iterator():
            async with message.process():
                is_valid, request = _validate_request(message)
                if not is_valid: continue

                match request.event:
                    case ConsumerEvents.ANALYZE_DOMAIN:
                        coroutine = self.__controller.analyze(request)
                        self.__add_task(coroutine)
                    case _:
                        logger.warning(f'Unexpected event encountered: {request.event}.')


    async def shutdown(self) -> None:
        await self.__queue.cancel(nowait=True)
        await cancel_all(self.__aio_tasks)
        self.__aio_tasks.clear()

    def __add_task(self, coroutine: Coroutine):
        safe_executable = self.__try_process(coroutine)
        task = self.__loop.create_task(safe_executable)
        task.add_done_callback(self.__task_completed)
        self.__aio_tasks.add(task)

    async def __try_process(self, coroutine: Coroutine):
        try:
            await coroutine
        except Exception as exp:
            logger.exception(f'Failed to process message.')

    def __task_completed(self, task: aio.Task):
        self.__aio_tasks.discard(task)