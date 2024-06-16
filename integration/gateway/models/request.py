from typing import NamedTuple

from aio_pika import IncomingMessage

from .events import ConsumerEvents


class RpcRequest(NamedTuple):
    """RpcRequest"""

    data: dict
    event: ConsumerEvents
    message: IncomingMessage