from typing import Protocol

from integration.gateway.models.request import RpcRequest


class IDomainController(Protocol):
    """IDomainController"""

    async def analyze(self, request: RpcRequest) -> None:
        pass