from typing import Optional
from dataclasses import dataclass

from domain.Entities.securitytrails.account import SecurityTrailsAccount
from domain.ValueObjects.app import AppUniqueId


@dataclass(frozen=True)
class ConsumerToProviderDTO:
    """ConsumerToProviderDTO"""

    _id: AppUniqueId
    success: bool
    error: Optional[str]=None
    account: Optional[SecurityTrailsAccount]=None