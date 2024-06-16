
from dataclasses import dataclass
from typing import (
    Generic,
    TypeVar,
    Tuple,
    Optional
)

from enum import Enum


class RecordType(Enum):
    """RecordType"""

    A = 'a'
    AAAA = 'aaaa'
    MX = 'mx'
    NS = 'ns'
    SOA = 'soa'
    TXT = 'txt'


def _require_fields(data, *fields):
    """_require_fields"""

    return {
        field: data.get(field)
        for field in fields
    }


@dataclass(frozen=True)
class ARecord:
    """ARecord"""

    ip: str
    ip_count: int
    ip_organization: Optional[str] = None

    @classmethod
    def from_response(cls, data):
        return cls(**_require_fields(data, 'ip', 'ip_count', 'ip_organization'))


@dataclass(frozen=True)
class AAAARecord:
    """AAAARecord"""

    ipv6: str
    ipv6_count: int
    ipv6_organization: Optional[str] = None

    @classmethod
    def from_response(cls, data):
        return cls(**_require_fields(data, 'ipv6', 'ipv6_count', 'ipv6_organization'))


@dataclass(frozen=True)
class MXRecord:
    """MXRecord"""

    priority: int
    host: str
    host_count: int
    hostname_organization: Optional[str] = None

    @classmethod
    def from_response(cls, data):
        return cls(**_require_fields(data, 'priority', 'host', 'host_count', 'hostname_organization'))


@dataclass(frozen=True)
class NSRecord:
    """NSRecord"""

    nameserver: str
    nameserver_count: int
    nameserver_organization: Optional[str] = None

    @classmethod
    def from_response(cls, data):
        return cls(**_require_fields(data, 'nameserver', 'nameserver_count', 'nameserver_organization'))


@dataclass(frozen=True)
class SOARecord:
    """SOARecord"""

    ttl: int
    email: str
    email_count: int

    @classmethod
    def from_response(cls, data):
        return cls(**_require_fields(data, 'ttl', 'email', 'email_count'))


@dataclass(frozen=True)
class TXTRecord:
    """TXTRecord"""

    value: str

    @classmethod
    def from_response(cls, data):
        return cls(**_require_fields(data, 'value'))


TRecord = TypeVar('TRecord', ARecord, AAAARecord, MXRecord, NSRecord, SOARecord, TXTRecord)


@dataclass(frozen=True)
class BaseRecordInfo(Generic[TRecord]):
    """RecordInfo"""

    first_seen: str
    values: Tuple[TRecord, ...]


@dataclass(frozen=True)
class HistoryRecordInfo(BaseRecordInfo):
    """HistoryRecordInfo"""

    last_seen: str
    organizations: tuple[str]