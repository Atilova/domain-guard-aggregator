from typing import Protocol, Optional

from domain.Entities.securitytrails.account import SecurityTrailsAccount
from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountId,
    SecurityTrailsAccountEmail,
    SecurityTrailsAccountPassword,
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountSignUpDate,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)


class ISecurityTrailsAccountService(Protocol):
    """ISecurityTrailsAccountService"""

    def new_account(self, *,
        _id: Optional[SecurityTrailsAccountId]=None,
        email: SecurityTrailsAccountEmail,
        password: SecurityTrailsAccountPassword,
        api_key: SecurityTrailsAccountApiKey,
        sign_up_date: Optional[SecurityTrailsAccountSignUpDate]=None,
        is_active: SecurityTrailsAccountIsActive,
        available_requests: Optional[SecurityTrailsAccountAvailableRequests]
    ) -> SecurityTrailsAccount:
        pass