from typing import Optional

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


class SecurityTrailsAccountService:
    """SecurityTrailsAccountService"""

    def new_account(self, *,
        _id: Optional[SecurityTrailsAccountId]=None,
        email: SecurityTrailsAccountEmail,
        password: SecurityTrailsAccountPassword,
        api_key: SecurityTrailsAccountApiKey,
        sign_up_date: Optional[SecurityTrailsAccountSignUpDate]=None,
        is_active: SecurityTrailsAccountIsActive,
        available_requests: Optional[SecurityTrailsAccountAvailableRequests]=None
    ) -> SecurityTrailsAccount:

        return SecurityTrailsAccount(
            _id=_id,
            email=email,
            password=password,
            api_key=api_key,
            sign_up_date=sign_up_date,
            is_active=is_active,
            available_requests=available_requests
        )