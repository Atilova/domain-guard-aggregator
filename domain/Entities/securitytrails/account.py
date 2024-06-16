from typing import Optional

from dataclasses import dataclass

from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountId,
    SecurityTrailsAccountEmail,
    SecurityTrailsAccountPassword,
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountSignUpDate,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)


@dataclass
class SecurityTrailsAccount:
    _id: Optional[SecurityTrailsAccountId]
    email: SecurityTrailsAccountEmail
    password: SecurityTrailsAccountPassword
    api_key: SecurityTrailsAccountApiKey
    sign_up_date: Optional[SecurityTrailsAccountSignUpDate]
    is_active: SecurityTrailsAccountIsActive
    available_requests: Optional[SecurityTrailsAccountAvailableRequests]

    def set_is_active(self, is_active: SecurityTrailsAccountIsActive):
        self.is_active = is_active

    def set_available_requests(self, available_requests: SecurityTrailsAccountAvailableRequests):
        self.available_requests = available_requests

    def decrement_requests(self) -> None:
        if self.available_requests is None or self.available_requests.raw() <= 0: return

        decremented = self.available_requests.raw() - 1
        self.set_available_requests(
            SecurityTrailsAccountAvailableRequests(decremented)
        )

    @property
    def is_available_requests(self) -> bool:
        return self.available_requests.raw() > 0