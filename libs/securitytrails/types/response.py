from dataclasses import dataclass
from typing import Optional, Generic, TypeVar

from enum import Enum, auto

from .data import (
    ApiKeyUsage,
    DomainData,
    SubDomainData,
    DnsHistoryData
)


ResponseT = TypeVar('ResponseT', ApiKeyUsage, DomainData, SubDomainData, DnsHistoryData)


@dataclass(frozen=True)
class BaseStatus(Enum):
    """BaseStatus"""

    FETCHED = auto()
    NO_INFO = auto()
    UNAUTHORIZED = auto()
    INVALID_DOMAIN = auto()
    API_KEY_EXHAUSTED = auto()
    UNDEFINED = auto()


@dataclass(frozen=True)
class BaseResponse(Generic[ResponseT]):
    """BaseResponse"""

    status: BaseStatus
    response: Optional[ResponseT] = None