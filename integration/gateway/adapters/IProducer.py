from aio_pika import IncomingMessage

from typing import (
    Protocol,
    Optional,
    Any,
    Dict
)


class IProducer(Protocol):
    """IProducer"""

    async def reply_domain_analysis(self, *, message: IncomingMessage, data: Dict[str, Any]) -> None:
        pass

    @property
    def allowed(self) -> bool:
        pass