from application.Dto.dns import (
    ARecord,
    AAAARecord,
    MXRecord,
    NSRecord,
    SOARecord,
    TXTRecord,
    RecordRow,
    PresentTable,
    HistoryTable,
    ResultCode,
    DomainSummary,
    DomainAnalysisOutputDTO
)

from domain.Entities.dns import (
    CurrentDnsRow,
    HistoryDnsRow,
    CurrentDnsTable,
    HistoryDnsTable,
    DomainSummary as AppDomainSummary
)
from domain.ValueObjects.records import (
    ARecord as AppARecord,
    AAAARecord as AppAAAARecord,
    MXRecord as AppMXRecord,
    NSRecord as AppNSRecord,
    SOARecord as AppSOARecord,
    TXTRecord as AppTXTRecord
)


def _map_a_record(record: AppARecord) -> ARecord:
    """_map_a_record"""

    values = record.raw()
    return ARecord(
        ip=values.ip.raw(),
        count=values.count.raw(),
        organization=values.organization and values.organization.raw()
    )

def _map_aaaa_record(record: AppAAAARecord) -> AAAARecord:
    """_map_aaaa_record"""

    values = record.raw()
    return AAAARecord(
        ipv6=values.ipv6.raw(),
        count=values.count.raw(),
        organization=values.organization and values.organization.raw()
    )

def _map_mx_record(record: AppMXRecord) -> MXRecord:
    """_map_mx_record"""

    values = record.raw()
    return MXRecord(
        priority=values.priority.raw(),
        host=values.host.raw(),
        count=values.count.raw(),
        organization=values.organization and values.organization.raw()
    )

def _map_ns_record(record: AppNSRecord) -> NSRecord:
    """_map_ns_record"""

    values = record.raw()
    return NSRecord(
        nameserver=values.nameserver.raw(),
        count=values.count.raw(),
        organization=values.organization and values.organization.raw()
    )

def _map_soa_record(record: AppSOARecord) -> SOARecord:
    """_map_soa_record"""

    values = record.raw()
    return SOARecord(
        ttl=values.ttl.raw(),
        email=values.email.raw(),
        count=values.count.raw()
    )

def _map_txt_record(record: AppTXTRecord) -> TXTRecord:
    """_map_txt_record"""

    values = record.raw()
    return TXTRecord(
        value=values.value.raw()
    )

RECORD_MAPPER = {
    'a': _map_a_record,
    'aaaa': _map_aaaa_record,
    'mx': _map_mx_record,
    'ns': _map_ns_record,
    'soa': _map_soa_record,
    'txt': _map_txt_record
}

def map_data_to_dns_output_dto(data: AppDomainSummary) -> DomainAnalysisOutputDTO:
    """map_data_to_dns_output_dto"""

    return DomainAnalysisOutputDTO(
        code=ResultCode.FETCHED,
        summary=DomainSummary(
            hostname=data.hostname.raw(),
            present=_map_current_dns_table(data.current),
            history=_map_history_dns_table(data.history),
            subdomains=[subdomain.raw() for subdomain in data.subdomains]
        )
    )

def _map_current_dns_table(table: CurrentDnsTable) -> PresentTable:
    """_map_current_dns_table"""

    return PresentTable(
        a=_map_row(table.a, 'a'),
        aaaa=_map_row(table.aaaa, 'aaaa'),
        mx=_map_row(table.mx, 'mx'),
        ns=_map_row(table.ns, 'ns'),
        soa=_map_row(table.soa, 'soa'),
        txt=_map_row(table.txt, 'txt')
    )

def _map_history_dns_table(table: HistoryDnsTable) -> HistoryTable:
    """_map_history_dns_table"""

    return HistoryTable(
        a=tuple((_map_row(row, 'a') for row in table.a)),
        aaaa=tuple((_map_row(row, 'aaaa') for row in table.aaaa)),
        mx=tuple((_map_row(row, 'mx') for row in table.mx)),
        ns=tuple((_map_row(row, 'ns') for row in table.ns)),
        soa=tuple((_map_row(row, 'soa') for row in table.soa)),
        txt=tuple((_map_row(row, 'txt') for row in table.txt))
    )

def _map_row(row: CurrentDnsRow | HistoryDnsRow, record_type: str) -> RecordRow:
    """_map_row"""

    if row is None: return None

    is_history = isinstance(row, HistoryDnsRow)
    return RecordRow(
        first_seen=row.first_seen.raw(),
        last_seen=is_history and row.last_seen.raw() or None,
        organizations=is_history and tuple((organization.raw() for organization in row.organizations)) or None,
        values=tuple((RECORD_MAPPER[record_type](record) for record in row.values))
    )