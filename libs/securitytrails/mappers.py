import logging

from typing import Optional, Any, Callable, Tuple

from .types.records import (
    BaseRecordInfo,
    HistoryRecordInfo,
    ARecord,
    AAAARecord,
    MXRecord,
    NSRecord,
    SOARecord,
    TXTRecord,
    TRecord,
    RecordType
)
from .types.data import (
    ApiKeyUsage,
    DomainData,
    SubDomainData,
    DnsHistoryData,
    DnsRecordsInfo
)


logger = logging.getLogger(__name__)


InputDataT = dict[str, Any]

TYPE_BY_ENUM = {
    RecordType.A: ARecord,
    RecordType.AAAA: AAAARecord,
    RecordType.MX: MXRecord,
    RecordType.NS: NSRecord,
    RecordType.SOA: SOARecord,
    RecordType.TXT: TXTRecord
}

def _init_base_record(data: InputDataT, mapper: Callable[[InputDataT], Tuple[TRecord, ...]]):
    """_init_base_record"""

    return data and BaseRecordInfo(
        first_seen=data['first_seen'],
        values=mapper(data['values'])
    ) or None

def _init_history_record(data: InputDataT, mapper: Callable[[InputDataT], Tuple[TRecord, ...]]):
    """_init_history_record"""

    return data and HistoryRecordInfo(
        first_seen=data['first_seen'],
        last_seen=data['last_seen'],
        organizations=tuple(data['organizations']),
        values=mapper(data['values'])
    ) or None

def _map_record(initializer):
    """_map_record"""

    def do_map(values: list[InputDataT] | InputDataT):
        if isinstance(values, dict):
            return initializer(values),

        return tuple((
            initializer(record)
            for record in values
        ))
    return do_map

def usage_mapper(data: InputDataT) -> Optional[ApiKeyUsage]:
    """usage_mapper"""

    try:
        mapped = ApiKeyUsage(
            usage=data['current_monthly_usage'],
            monthly_available=data['allowed_monthly_usage']
        )
        return mapped
    except Exception as exp:
        logger.exception('Failed to map `usage` data.')
    return None

def domain_mapper(data: InputDataT) -> Optional[DomainData]:
    """domain_mapper"""

    try:
        dns = data['current_dns']
        mapped = DomainData(
            hostname=data['hostname'],
            alexa_rank=data['alexa_rank'],
            records=DnsRecordsInfo(
                A=_init_base_record(dns['a'], _map_record(ARecord.from_response)),
                AAAA=_init_base_record(dns['aaaa'], _map_record(AAAARecord.from_response)),
                MX=_init_base_record(dns['mx'], _map_record(MXRecord.from_response)),
                NS=_init_base_record(dns['ns'], _map_record(NSRecord.from_response)),
                SOA=_init_base_record(dns['soa'], _map_record(SOARecord.from_response)),
                TXT=_init_base_record(dns['txt'], _map_record(TXTRecord.from_response))
        )
    )
        return mapped
    except Exception as exp:
        logger.exception('Failed to map `domain` data.')
    return None

def subdomains_mapper(data: InputDataT) -> Optional[SubDomainData]:
    """subdomain_mapper"""

    count = data.get('subdomain_count')
    if not count: return SubDomainData(count=0, subdomains=tuple())

    try:
        mapped = SubDomainData(
            count=count,
            subdomains=tuple(data['subdomains'])
        )
        return mapped
    except Exception as exp:
        logger.exception('Failed to map `subdomains` data.')
    return None

def history_dns_mapper(data: InputDataT, *, type: RecordType) -> Optional[DnsHistoryData]:
    """history_dns_mapper"""

    try:
        record_mapper = TYPE_BY_ENUM[type].from_response
        records = tuple((
            _init_history_record(record, _map_record(record_mapper))
            for record in data['records']
        ))

        mapped = DnsHistoryData(
            type=type,
            records=records
        )
        return mapped
    except Exception as exp:
        logger.exception('Failed to map `history_dns` data.')
    return None