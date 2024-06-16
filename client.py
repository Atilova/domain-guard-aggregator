import asyncio as aio

from uuid import uuid4
from json import dumps

from typing import Optional, Any

from aio_pika import connect, Message, IncomingMessage
from aio_pika.abc import AbstractConnection, AbstractChannel

from config import conf

from infrastructure.config import ServiceGatewayConfig


def _compose_request_body(domain: str):
    """_compose_request_body"""

    return domain and { 'event': 'analyze_domain', 'data': { 'domain': domain } } or None


class TestRPCClient:
    """TestRPCClient"""

    def __init__(self, *, uri: str, config: ServiceGatewayConfig):
        self.__uri = uri
        self.__config = config
        self.__response_futures: dict[str, aio.Future[Any]] = {}
        self.__connection: Optional[AbstractConnection] = None
        self.__channel: Optional[AbstractChannel] = None

    async def __on_response(self, message: IncomingMessage):
        future = self.__response_futures.pop(message.correlation_id, None)
        if not future: return
        future.set_result(message.body.decode())

    async def call(self, request_body: bytes | str, timeout: int):
        if self.__channel is None or self.__channel.is_closed: return

        correlation_id = uuid4().hex
        future = aio.get_event_loop().create_future()
        self.__response_futures[correlation_id] = future

        await self.__channel.default_exchange.publish(
            Message(
                request_body.encode(),
                correlation_id=correlation_id,
                reply_to=self.__config.producer_queue
            ),
            routing_key=self.__config.consumer_routing_key
        )

        try:
            response = await aio.wait_for(future, timeout)
            return response
        except aio.TimeoutError:
            self.__response_futures.pop(correlation_id, None)
        return None

    async def call_json(self, serializable: Any, timeout: int=10):
        try:
            jsonified = dumps(serializable)
        except TypeError:
            return None
        return await self.call(jsonified, timeout)

    async def begin(self):
        self.__connection = await connect(self.__uri)
        self.__channel = await self.__connection.channel()

        result_queue = await self.__channel.declare_queue(self.__config.producer_queue, durable=True)
        await result_queue.consume(self.__on_response)

    async def stop(self):
        if self.__channel is not None and not self.__channel.is_closed:
            await self.__channel.close()

        if self.__connection is not None and not self.__connection.is_closed:
            await self.__connection.close()

async def main():
    client = TestRPCClient(
        uri=conf.rabbitmq.uri,
        config=conf.service_gateway
    )

    await client.begin()

    try:
        while True:
            domain = input('Enter domain: ')
            request_body = _compose_request_body(domain)
            if request_body is None: continue

            response = await client.call_json(request_body, 15)
            print(f'Analyzed: {response}')
    except KeyboardInterrupt:
        print('Quitting...')
        await client.stop()


if __name__ == "__main__":
    aio.run(main())