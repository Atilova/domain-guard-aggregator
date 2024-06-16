from typing import Tuple

from libs.securitytrails.client import SecurityTrailsClient, BaseStatus

from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)


class SecurityTrailsApiKeyService:
    """SecurityTrailsApiKeyService"""

    def __init__(self):
        self.__client = SecurityTrailsClient()

    async def verify(self,
        api_key: SecurityTrailsAccountApiKey
    ) -> Tuple[SecurityTrailsAccountIsActive, SecurityTrailsAccountAvailableRequests]:

        response = await self.__client.get_usage(api_key.raw())
        data = response.response

        if response.status is BaseStatus.FETCHED:
            available = data.monthly_available - data.usage
            return SecurityTrailsAccountIsActive(True), SecurityTrailsAccountAvailableRequests(available)

        return SecurityTrailsAccountIsActive(False), SecurityTrailsAccountAvailableRequests(0)