from typing import Protocol

from domain.Entities.securitytrails.account import SecurityTrailsAccount


class ISecurityTrailsAccountProvider(Protocol):
    """ISecurityTrailsAccountProvider"""

    async def get(self) -> SecurityTrailsAccount:
        pass

    async def expire_account(self, account: SecurityTrailsAccount) -> SecurityTrailsAccount:
        pass