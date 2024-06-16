from typing import Optional, Generic, Tuple
from dataclasses import dataclass

from domain.ValueObjects.dns import (
    Hostname,
    SubDomain,
    FirstSeen,
    LastSeen,
    Organization
)
from domain.ValueObjects.records import (
    ARecord,
    AAAARecord,
    MXRecord,
    NSRecord,
    SOARecord,
    TXTRecord,
    TRecord
)


@dataclass(frozen=True)
class CurrentDnsRow(Generic[TRecord]):
    """CurrentDnsRow"""

    first_seen: FirstSeen
    values: Tuple[TRecord, ...]


@dataclass(frozen=True)
class HistoryDnsRow(Generic[TRecord]):
    """HistoryDnsRow"""

    first_seen: FirstSeen
    last_seen: LastSeen
    organizations: Tuple[Organization, ...]
    values: Tuple[TRecord, ...]


@dataclass(frozen=True)
class CurrentDnsTable:
    a: Optional[CurrentDnsRow[ARecord]]
    aaaa: Optional[CurrentDnsRow[AAAARecord]]
    mx: Optional[CurrentDnsRow[MXRecord]]
    ns: Optional[CurrentDnsRow[NSRecord]]
    soa: Optional[CurrentDnsRow[SOARecord]]
    txt: Optional[CurrentDnsRow[TXTRecord]]

@dataclass(frozen=True)
class HistoryDnsTable:
    a: Tuple[HistoryDnsRow[ARecord], ...]
    aaaa: Tuple[HistoryDnsRow[AAAARecord], ...]
    mx: Tuple[HistoryDnsRow[MXRecord], ...]
    ns: Tuple[HistoryDnsRow[NSRecord], ...]
    soa: Tuple[HistoryDnsRow[SOARecord], ...]
    txt: Tuple[HistoryDnsRow[TXTRecord], ...]


@dataclass
class DomainSummary:
    hostname: Hostname
    current: CurrentDnsTable
    history: HistoryDnsTable
    subdomains: Tuple[SubDomain, ...]