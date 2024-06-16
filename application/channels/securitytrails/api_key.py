import logging

import asyncio as aio
from aio_pika import ExchangeType, IncomingMessage
from aio_pika.abc import AbstractChannel, AbstractQueue

from typing import (
    Optional,
    Set,
    NamedTuple,
    Tuple,
    Optional
)

from utils.cancel_tasks import cancel_all

from application.adapters.securitytrails.ISecurityTrailsAccountProvider import ISecurityTrailsAccountProvider
from application.adapters.securitytrails.ISecurityTrailsAccountService import ISecurityTrailsAccountService
from application.Dto.mappers.securitytrails.consumer_provider import map_api_key_response

from domain.Enums.securitytrails.events import SecurityTrailsConsumerEvents
from domain.ValueObjects.app import AppUniqueId
from domain.ValueObjects.securitytrails.events import SecurityTrailsConsumerEvent

from infrastructure.config import SecurityTrailsGatewayConfig
from infrastructure.consumer.channel import AsyncChannelBase
from infrastructure.consumer.extensions.json_processor import process_as_json


logger = logging.getLogger('SecurityTrailsApiKeyChannel')


class Request(NamedTuple):
    """Request"""

    id: AppUniqueId
    data: object
    event: SecurityTrailsConsumerEvent


def _validate_request(message: IncomingMessage) -> Tuple[bool, Optional[Request]]:
    """_validate_request"""

    is_json, body = process_as_json(message)
    if not is_json: return False, None

    event_name = body.get('event')
    try:
        event = SecurityTrailsConsumerEvent(event_name)
    except ValueError:
        logger.warning(f'Received unknown event: {event_name}.')
        return False, None

    try:
        _id = AppUniqueId(body.get('_id'))
    except TypeError:
        logger.warning(f'Request missing _id of proper type on: {event.raw()}.')
        return False, None

    data = body.get('data')
    if data is None:
        logger.warning(f'Request missing data object on: {event.raw()}.')
        return False, None

    return True, Request(id=_id, event=event, data=data)


class SecurityTrailsApiKeyChannel(AsyncChannelBase):
    """SecurityTrailsApiKeyChannel"""

    def __init__(self, *,
        config: SecurityTrailsGatewayConfig,
        provider: ISecurityTrailsAccountProvider,
        loop: aio.AbstractEventLoop,
        service: ISecurityTrailsAccountService
    ):
        self.__config = config
        self.__provider = provider
        self.__loop = loop
        self.__aio_tasks: Set[aio.Task] = set()
        self.__service = service
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
            durable=True,
            arguments={
                'x-single-active-consumer': True
            }
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

                match request.event.raw():
                    case SecurityTrailsConsumerEvents.ACCOUNT_RESPONSE:
                        mapped = map_api_key_response(service= self.__service, _id=request.id,
                                                      data=request.data)

                        task_coroutine = self.__try_process(self.__provider.response(mapped))
                        task = self.__loop.create_task(task_coroutine)
                        task.add_done_callback(self.__task_completed)
                        self.__aio_tasks.add(task)
                    case _:
                        logger.warning(f'Unexpected event encountered: {request.event.raw()}.')

    async def shutdown(self) -> None:
        await self.__queue.cancel(nowait=True)
        await cancel_all(self.__aio_tasks)
        self.__aio_tasks.clear()


    async def __try_process(self, coroutine):
        try:
            await coroutine
        except Exception as exp:
            logger.exception(f'Failed to process message.')

    def __task_completed(self, task: aio.Task):
        self.__aio_tasks.discard(task)