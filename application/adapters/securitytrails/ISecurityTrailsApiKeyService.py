from typing import Protocol, Optional, Tuple

from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)


class ISecurityTrailsApiKeyService(Protocol):
    """ISecurityTrailsApiKeyService"""

    async def verify(self,
        api_key: SecurityTrailsAccountApiKey
    ) -> Tuple[SecurityTrailsAccountIsActive, SecurityTrailsAccountAvailableRequests]:
        pass