from typing import Protocol, Optional, Tuple

from domain.Entities.dns import (
    CurrentDnsRow,
    HistoryDnsRow,
    DomainSummary,
    CurrentDnsTable,
    HistoryDnsTable,
)
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


class IDomainDnsService(Protocol):
    """IDomainDnsService"""

    def new_summary(self, *,
        hostname: Hostname,
        current: CurrentDnsTable,
        history: HistoryDnsTable,
        subdomains: Tuple[SubDomain, ...]
    ) -> DomainSummary:
        pass

    def new_current_dns_table(self, *,
        a: Optional[CurrentDnsRow[ARecord]]=None,
        aaaa: Optional[CurrentDnsRow[AAAARecord]]=None,
        mx: Optional[CurrentDnsRow[MXRecord]]=None,
        ns: Optional[CurrentDnsRow[NSRecord]]=None,
        soa: Optional[CurrentDnsRow[SOARecord]]=None,
        txt: Optional[CurrentDnsRow[TXTRecord]]=None,
    ) -> CurrentDnsTable:
        pass

    def new_history_dns_table(self, *,
        a: Tuple[HistoryDnsRow[ARecord], ...],
        aaaa: Tuple[HistoryDnsRow[AAAARecord], ...],
        mx: Tuple[HistoryDnsRow[MXRecord], ...],
        ns: Tuple[HistoryDnsRow[NSRecord], ...],
        soa: Tuple[HistoryDnsRow[SOARecord], ...],
        txt: Tuple[HistoryDnsRow[TXTRecord], ...]
    ) -> HistoryDnsTable:
        pass

    def new_current_row(self, *,
        first_seen: FirstSeen,
        values: Tuple[TRecord, ...]
    ) -> CurrentDnsRow[TRecord]:
        pass

    def new_history_row(self, *,
        first_seen: FirstSeen,
        last_seen: LastSeen,
        organizations: Tuple[Organization, ...],
        values: Tuple[TRecord, ...],
    ) -> HistoryDnsRow[TRecord]:
        pass