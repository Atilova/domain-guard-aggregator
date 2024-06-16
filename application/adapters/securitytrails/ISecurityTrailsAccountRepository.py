from typing import (
    Protocol,
    Optional,
    List,
    Tuple
)


from domain.Entities.securitytrails.account import SecurityTrailsAccount
from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountId,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)


class ISecurityTrailsAccountRepository(Protocol):
    """ISecurityTrailsAccountRepository"""

    async def create(self, account: SecurityTrailsAccount) -> SecurityTrailsAccount:
        pass

    async def get(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccount]:
        pass

    async def activate(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccount]:
        pass

    async def deactivate(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccount]:
        pass

    async def set_available_requests(self,
        account_id: SecurityTrailsAccountId,
        available_requests: SecurityTrailsAccountAvailableRequests
    ) -> Optional[SecurityTrailsAccount]:
        pass

    async def all_active(self) -> List[SecurityTrailsAccount]:
        pass

    async def all_enactive(self) -> List[SecurityTrailsAccount]:
        pass

    async def fetch_minimal(self,
        required_request: SecurityTrailsAccountAvailableRequests
    ) -> Tuple[SecurityTrailsAccountAvailableRequests, Tuple[SecurityTrailsAccount, ...]]:
        pass

    async def update_status(self,
        account_id: SecurityTrailsAccountId, *,
        is_active: SecurityTrailsAccountIsActive,
        available_requests: SecurityTrailsAccountAvailableRequests
    ) -> Optional[SecurityTrailsAccount]:
        pass