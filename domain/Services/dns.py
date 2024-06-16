from typing import Optional, Tuple

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


class DomainDnsService:
    """DomainDnsService"""

    def new_summary(self, *,
        hostname: Hostname,
        current: CurrentDnsTable,
        history: HistoryDnsTable,
        subdomains: Tuple[SubDomain, ...]
    ) -> DomainSummary:
        return DomainSummary(
            hostname=hostname,
            current=current,
            history=history,
            subdomains=subdomains
        )

    def new_current_dns_table(self, *,
        a: Optional[CurrentDnsRow[ARecord]]=None,
        aaaa: Optional[CurrentDnsRow[AAAARecord]]=None,
        mx: Optional[CurrentDnsRow[MXRecord]]=None,
        ns: Optional[CurrentDnsRow[NSRecord]]=None,
        soa: Optional[CurrentDnsRow[SOARecord]]=None,
        txt: Optional[CurrentDnsRow[TXTRecord]]=None,
    ) -> CurrentDnsTable:
        return CurrentDnsTable(
            a=a,
            aaaa=aaaa,
            mx=mx,
            ns=ns,
            soa=soa,
            txt=txt
        )

    def new_history_dns_table(self, *,
        a: Tuple[HistoryDnsRow[ARecord], ...]=tuple(),
        aaaa: Tuple[HistoryDnsRow[AAAARecord], ...]=tuple(),
        mx: Tuple[HistoryDnsRow[MXRecord], ...]=tuple(),
        ns: Tuple[HistoryDnsRow[NSRecord], ...]=tuple(),
        soa: Tuple[HistoryDnsRow[SOARecord], ...]=tuple(),
        txt: Tuple[HistoryDnsRow[TXTRecord], ...]=tuple()
    ) -> HistoryDnsTable:
        return HistoryDnsTable(
            a=a,
            aaaa=aaaa,
            mx=mx,
            ns=ns,
            soa=soa,
            txt=txt
        )

    def new_current_row(self, *,
        first_seen: FirstSeen,
        values: Tuple[TRecord, ...]
    ) -> CurrentDnsRow[TRecord]:
        return CurrentDnsRow(
            first_seen=first_seen,
            values=values
        )

    def new_history_row(self, *,
        first_seen: FirstSeen,
        last_seen: LastSeen,
        organizations: Tuple[Organization, ...],
        values: Tuple[TRecord, ...],
    ) -> HistoryDnsRow[TRecord]:
        return HistoryDnsRow(
            first_seen=first_seen,
            last_seen=last_seen,
            organizations=organizations,
            values=values
        )