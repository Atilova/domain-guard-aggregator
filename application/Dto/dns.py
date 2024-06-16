from dataclasses import dataclass, asdict

from typing import (
    Optional,
    TypeVar,
    Generic,
    Tuple
)


@dataclass(frozen=True)
class ARecord:
    """ARecord"""

    ip: str
    count: int
    organization: Optional[str]


@dataclass(frozen=True)
class AAAARecord:
    """AAAARecord"""

    ipv6: str
    count: int
    organization: Optional[str]


@dataclass(frozen=True)
class MXRecord:
    """MXRecord"""

    priority: int
    host: str
    count: Optional[int]
    organization: Optional[str]


@dataclass(frozen=True)
class NSRecord:
    """NSRecord"""

    nameserver: str
    count: int
    organization: Optional[str]


@dataclass(frozen=True)
class SOARecord:
    """SOARecord"""

    ttl: int
    email: str
    count: int


@dataclass(frozen=True)
class TXTRecord:
    """TXTRecord"""

    value: str


TRecord = TypeVar('TRecord', ARecord, AAAARecord, MXRecord, NSRecord, SOARecord, TXTRecord)


@dataclass(frozen=True)
class RecordRow(Generic[TRecord]):
    """RecordRow"""

    first_seen: str
    values: Tuple[TRecord, ...]
    last_seen: Optional[str] = None
    organizations: Optional[Tuple[str, ...]] = None


@dataclass
class PresentTable:
    """PresentTable"""

    a: Optional[RecordRow] = None
    aaaa: Optional[RecordRow] = None
    mx: Optional[RecordRow] = None
    ns: Optional[RecordRow] = None
    soa: Optional[RecordRow] = None
    txt: Optional[RecordRow] = None


@dataclass
class HistoryTable:
    """HistoryTable"""

    a: Tuple[RecordRow, ...]
    aaaa: Tuple[RecordRow, ...]
    mx: Tuple[RecordRow, ...]
    ns: Tuple[RecordRow, ...]
    soa: Tuple[RecordRow, ...]
    txt: Tuple[RecordRow, ...]


@dataclass
class DomainSummary:
    """DomainSummary"""

    hostname: str
    present: PresentTable
    history: HistoryTable
    subdomains: Tuple[str, ...]


class ResultCode:
    """ResultCode"""

    FETCHED = 'fetched'
    INVALID_DOMAIN = 'invalid_domain'


@dataclass(frozen=True)
class DomainAnalysisInputDTO:
    """DomainAnalysisInputDTO"""

    domain: str


@dataclass(frozen=True)
class DomainAnalysisOutputDTO:
    """DomainAnalysisOutputDTO"""

    code: ResultCode
    summary: Optional[DomainSummary] = None

    def to_dict(self):
        return asdict(self)