from typing import Protocol, AsyncContextManager, Tuple

from .ISecurityTrailsAccountRepository import ISecurityTrailsAccountRepository

from application.adapters.IUnitOfWork import IUnitOfWork


class ISecurityTrailsAccountModule(Protocol):
    """ISecurityTrailsAccountModule"""

    def repository(self) -> AsyncContextManager[Tuple[IUnitOfWork, ISecurityTrailsAccountRepository]]:
        pass