from dataclasses import dataclass
from typing import Tuple, Optional

from .records import (
    BaseRecordInfo,
    HistoryRecordInfo,
    ARecord,
    AAAARecord,
    MXRecord,
    NSRecord,
    SOARecord,
    TXTRecord,
    RecordType
)


@dataclass(frozen=True)
class ApiKeyUsage:
    """ApiKeyUsage"""

    usage: int
    monthly_available: int


@dataclass(frozen=True)
class DnsRecordsInfo:
    """DnsRecordsInfo"""

    A: Optional[BaseRecordInfo[ARecord]] = None
    AAAA: Optional[BaseRecordInfo[AAAARecord]] = None
    MX: Optional[BaseRecordInfo[MXRecord]] = None
    NS: Optional[BaseRecordInfo[NSRecord]] = None
    SOA: Optional[BaseRecordInfo[SOARecord]] = None
    TXT: Optional[BaseRecordInfo[TXTRecord]] = None


@dataclass(frozen=True)
class DomainData:
    """DomainData"""

    hostname: str
    records: DnsRecordsInfo
    alexa_rank: Optional[int] = None


@dataclass(frozen=True)
class SubDomainData:
    """SubDomainData"""

    count: int
    subdomains: tuple[str]


@dataclass(frozen=True)
class DnsHistoryData:
    """DnsHistoryData"""

    type: RecordType
    records: Tuple[HistoryRecordInfo, ...]