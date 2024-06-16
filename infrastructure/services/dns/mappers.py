import logging

from typing import (
    Optional,
    Tuple,
    Any,
    Callable
)

from libs.securitytrails.client import (
    DomainData,
    SubDomainData,
    DnsHistoryData
)
from libs.securitytrails.types.records import (
    BaseRecordInfo,
    HistoryRecordInfo,
    TRecord as TClientRecord,
    ARecord as ClientARecord,
    AAAARecord as ClientAAAARecord,
    MXRecord as ClientMXRecord,
    NSRecord as ClientNSRecord,
    SOARecord as ClientSOARecord,
    TXTRecord as ClientTXTRecord
)

from domain.Entities.dns import (
    CurrentDnsRow,
    CurrentDnsTable,
    HistoryDnsTable
)
from domain.ValueObjects.app import Domain
from domain.ValueObjects.dns import (
    Hostname,
    SubDomain,
    FirstSeen,
    LastSeen,
    LastSeen,
    Count,
    Organization,
    Host,
    Priority,
    Ipv4,
    Ipv6,
    Nameserver,
    Ttl,
    Email,
    Txt,
)
from domain.ValueObjects.records import (
    ARecordValue,
    AAAARecordValue,
    MXRecordValue,
    NSRecordValue,
    SOARecordValue,
    TXTRecordValue,
    ARecord,
    AAAARecord,
    MXRecord,
    NSRecord,
    SOARecord,
    TXTRecord,
    TRecord
)


from infrastructure.adapters.IDomainDnsService import IDomainDnsService


logger = logging.getLogger('DnsAnalyzeService')

TMapper = Callable[[TClientRecord], TRecord]


def empty_response(domain: Domain, service: IDomainDnsService):
    """empty_response"""

    return service.new_summary(
        hostname=Hostname(domain.raw()),
        current=service.new_current_dns_table(),
        history=service.new_history_dns_table(),
        subdomains=tuple()
    )

def map_to_current_dns(data: DomainData, service: IDomainDnsService) -> CurrentDnsTable:
    """map_to_current_dns"""

    records = data.records
    return service.new_current_dns_table(
        a=_init_current_row(records.A, service, _map_a_record),
        aaaa=_init_current_row(records.AAAA, service, _map_aaaa_record),
        mx=_init_current_row(records.MX, service, _map_mx_record),
        ns=_init_current_row(records.NS, service, _map_ns_record),
        soa=_init_current_row(records.SOA, service, _map_soa_record),
        txt=_init_current_row(records.TXT, service, _map_txt_record)
    )

def map_to_subdomains_list(data: SubDomainData) -> Tuple[SubDomain, ...]:
    """map_to_subdomains_list"""

    return tuple((
        SubDomain(subdomain)
        for subdomain in data.subdomains
    ))

def map_to_history_dns(
    service: IDomainDnsService, *,
    a_data: Optional[DnsHistoryData],
    aaaa_data: Optional[DnsHistoryData],
    mx_data: Optional[DnsHistoryData],
    ns_data: Optional[DnsHistoryData],
    soa_data: Optional[DnsHistoryData],
    txt_data: Optional[DnsHistoryData]
) -> HistoryDnsTable:
    """map_to_history_dns"""

    return service.new_history_dns_table(
        a=_init_history_tuple(a_data, service, _map_a_record),
        aaaa=_init_history_tuple(aaaa_data, service, _map_aaaa_record),
        mx=_init_history_tuple(mx_data, service, _map_mx_record),
        ns=_init_history_tuple(ns_data, service, _map_ns_record),
        soa=_init_history_tuple(soa_data, service, _map_soa_record),
        txt=_init_history_tuple(txt_data, service, _map_txt_record)
    )

def _init_current_row(
    record: Optional[BaseRecordInfo],
    service: IDomainDnsService,
    mapper: TMapper
) -> CurrentDnsRow:
    """_init_current_row"""

    if record is None: return None

    return service.new_current_row(
        first_seen=FirstSeen(record.first_seen),
        values=tuple((
            mapper(value)
            for value in record.values
            if value
        ))
    )

def _init_history_tuple(
    data: Optional[DnsHistoryData],
    service: IDomainDnsService,
    mapper: TMapper
):
    """_init_history_tuple"""

    if data is None: return tuple()

    records = data.records
    return tuple((
        _init_history_row(record, service, mapper)
        for record in records
        if record.values
    ))

def _init_history_row(
    record: HistoryRecordInfo,
    service: IDomainDnsService,
    mapper: TMapper
):
    """_init_history_row"""

    return service.new_history_row(
        first_seen=FirstSeen(record.first_seen),
        last_seen=LastSeen(record.last_seen),
        organizations=tuple((
            Organization(organization)
            for organization in record.organizations
        )),
        values=tuple((
            mapper(value)
            for value in record.values
            if value
        ))
    )

def _init_not_none(value: Any, initializer: Callable):
    """_init_not_none"""

    return value is not None and initializer(value) or None

def _map_a_record(record: ClientARecord) -> ARecord:
    """_map_a_record"""

    return ARecord(ARecordValue(
        ip=Ipv4(record.ip),
        count=Count(record.ip_count),
        organization=_init_not_none(record.ip_organization, Organization)
    ))

def _map_aaaa_record(record: ClientAAAARecord) -> AAAARecord:
    """_map_aaaa_record"""

    return AAAARecord(AAAARecordValue(
        ipv6=Ipv6(record.ipv6),
        count=Count(record.ipv6_count),
        organization=_init_not_none(record.ipv6_organization, Organization)
    ))

def _map_mx_record(record: ClientMXRecord) -> MXRecord:
    """_map_mx_record"""

    return MXRecord(MXRecordValue(
        priority=Priority(record.priority),
        host=Host(record.host),
        count=Count(record.host_count),
        organization=_init_not_none(record.hostname_organization, Organization)
    ))

def _map_ns_record(record: ClientNSRecord) -> NSRecord:
    """_map_ns_record"""

    return NSRecord(NSRecordValue(
        nameserver=Nameserver(record.nameserver),
        count=Count(record.nameserver_count),
        organization=_init_not_none(record.nameserver_organization, Organization)
    ))

def _map_soa_record(record: ClientSOARecord) -> SOARecord:
    """_map_soa_record"""

    return SOARecord(SOARecordValue(
        ttl=Ttl(record.ttl),
        email=Email(record.email),
        count=Count(record.email_count),
    ))

def _map_txt_record(record: ClientTXTRecord) -> TXTRecord:
    """_map_txt_record"""

    return TXTRecord(TXTRecordValue(
        value=Txt(record.value)
    ))