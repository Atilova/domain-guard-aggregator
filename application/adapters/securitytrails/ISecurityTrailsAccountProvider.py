from typing import Protocol

from application.Dto.securitytrails.consumer_provider import ConsumerToProviderDTO

from domain.Entities.securitytrails.account import SecurityTrailsAccount


class ISecurityTrailsAccountProvider(Protocol):
    """ISecurityTrailsAccountProvider"""

    async def response(dto: ConsumerToProviderDTO) -> None:
        pass

    async def initialize(self):
        pass

    async def get(self) -> SecurityTrailsAccount:
        pass

    async def expire_account(self, account: SecurityTrailsAccount) -> SecurityTrailsAccount:
        pass

    async def response(self, dto: ConsumerToProviderDTO) -> None:
        pass

    async def shutdown(self) -> None:
        pass