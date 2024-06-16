from typing import Protocol, Any

from domain.ValueObjects.app import AppUniqueId


class ISecurityTrailsApiKeyProducer(Protocol):
    async def json(self, data: Any) -> None:
        pass

    async def fabricate_account(self, _id: AppUniqueId) -> None:
        pass

    @property
    def allowed(self) -> bool:
        pass