from typing import (
    Optional,
    TypeVar,
    NamedTuple
)
from dataclasses import dataclass

from .dns import (
    Count,
    Organization,
    Host,
    Priority,
    Ipv4,
    Ipv6,
    Nameserver,
    Ttl,
    Email,
    Txt
)

from domain.ValueObjects.base import ValueObject


class ARecordValue(NamedTuple):
    """ARecord"""

    ip: Ipv4
    count: Count
    organization: Optional[Organization] = None


class AAAARecordValue(NamedTuple):
    """AAAARecord"""

    ipv6: Ipv6
    count: Count
    organization: Optional[Organization] = None


class MXRecordValue(NamedTuple):
    """MXRecord"""

    priority: Priority
    host: Host
    count: Count
    organization: Optional[Organization] = None


class NSRecordValue(NamedTuple):
    """NSRecord"""

    nameserver: Nameserver
    count: Count
    organization: Optional[Organization] = None


class SOARecordValue(NamedTuple):
    """SOARecord"""

    ttl: Ttl
    email: Email
    count: Count


class TXTRecordValue(NamedTuple):
    """TXTRecord"""

    value: Txt


@dataclass(frozen=True)
class ARecord(ValueObject[ARecordValue]):
    _value: ARecordValue


@dataclass(frozen=True)
class AAAARecord(ValueObject[AAAARecordValue]):
    _value: AAAARecordValue


@dataclass(frozen=True)
class MXRecord(ValueObject[MXRecordValue]):
    _value: MXRecordValue


@dataclass(frozen=True)
class NSRecord(ValueObject[NSRecordValue]):
    _value: NSRecordValue


@dataclass(frozen=True)
class SOARecord(ValueObject[SOARecordValue]):
    _value: SOARecordValue


@dataclass(frozen=True)
class TXTRecord(ValueObject[TXTRecordValue]):
    _value: TXTRecordValue


TRecord = TypeVar('TRecord', ARecord, AAAARecord, MXRecord, NSRecord, SOARecord, TXTRecord)