import logging

import asyncio as aio

from typing import (
    Optional,
    Tuple,
    Any,
    Callable,
    Dict,
    TypeVar,
    Awaitable
)

from libs.securitytrails.client import (
    SecurityTrailsClient,
    BaseResponse,
    BaseStatus,
    RecordType,
    DomainData,
    DnsHistoryData
)

from .mappers import (
    empty_response,
    map_to_current_dns,
    map_to_history_dns,
    map_to_subdomains_list
)

from domain.Entities.dns import (
    DomainSummary,
    HistoryDnsTable
)
from domain.ValueObjects.app import Domain
from domain.ValueObjects.dns import Hostname, SubDomain

from infrastructure.adapters.IDomainDnsService import IDomainDnsService
from infrastructure.adapters.securitytrails.ISecurityTrailsAccountProvider import ISecurityTrailsAccountProvider


logger = logging.getLogger('DnsAnalyzeService')


MAX_FETCH_ATTEMPTS = 5
SUPPORTED_DNS_RECORDS = [
    RecordType.A,
    RecordType.AAAA,
    RecordType.MX,
    RecordType.NS,
    RecordType.SOA,
    RecordType.TXT
]

TMethod = TypeVar('TMethod', bound=Callable[..., Awaitable[BaseResponse]])

async def _fetch(
    method: TMethod, *,
    provider: ISecurityTrailsAccountProvider,
    args: Tuple[Any, ...]=tuple(),
    kwargs: Dict[str, Any]=dict(),
    max_attempts: int=MAX_FETCH_ATTEMPTS
):
    """_fetch"""

    attempts = 0
    account = await provider.get()
    response = await method(*args, **kwargs, api_key=account.api_key.raw())

    while attempts < max_attempts and (
        response.status is BaseStatus.API_KEY_EXHAUSTED or
        response.status is BaseStatus.UNAUTHORIZED
    ):
        attempts += 1
        logger.warning(f'Bad key response: {response.status}')
        await provider.expire_account(account)
        await aio.sleep(2)
        account = await provider.get()
        response = await method(*args, **kwargs, api_key=account.api_key.raw())
    return response

async def _process_domain(
    domain: Domain,
    client: SecurityTrailsClient,
    provider: ISecurityTrailsAccountProvider
) -> Tuple[bool, Optional[DomainData]]:
    """_process_domain"""

    domain_name = domain.raw()
    response = await _fetch(client.get_domain, provider=provider,
                            args=(domain_name,))

    data = response.response
    if response.status is not BaseStatus.FETCHED:
        return False, data
    return True, data

async def _process_subdomains(
    domain: Domain,
    client: SecurityTrailsClient,
    provider: ISecurityTrailsAccountProvider
) -> Tuple[SubDomain, ...]:
    """_process_subdomains"""

    domain_name = domain.raw()
    response = await _fetch(client.get_subdomains, provider=provider,
                            args=(domain_name,))

    data = response.response
    if response.status is not BaseStatus.FETCHED:
        return tuple()
    return map_to_subdomains_list(data)

async def _process_dns_record(
    domain: Domain,
    client: SecurityTrailsClient,
    provider: ISecurityTrailsAccountProvider,
    record: RecordType
) -> Optional[DnsHistoryData]:
    """_process_dns_record"""

    domain_name = domain.raw()
    response = await _fetch(client.get_history_dns, provider=provider,
                            args=(domain_name,), kwargs={'record_type': record})

    return response.response

async def _process_history(
    domain: Domain,
    client: SecurityTrailsClient,
    provider: ISecurityTrailsAccountProvider,
    service: IDomainDnsService
) -> HistoryDnsTable:
    """_process_history"""

    a, aaaa, mx, ns, soa, txt = await aio.gather(*(
        _process_dns_record(domain, client, provider, record)
        for record in SUPPORTED_DNS_RECORDS
    ))

    return map_to_history_dns(
        service,
        a_data=a,
        aaaa_data=aaaa,
        mx_data=mx,
        ns_data=ns,
        soa_data=soa,
        txt_data=txt
    )


class DnsAnalyzeService:
    """DnsAnalyzeService"""

    def __init__(self, *,
        provider: ISecurityTrailsAccountProvider,
        service: IDomainDnsService
    ):
        self.__provider = provider
        self.__service = service
        self.__client = SecurityTrailsClient()

    async def analyze(self, domain: Domain) -> DomainSummary:
        success, data = await _process_domain(domain, self.__client, self.__provider)
        if not success:
            return empty_response(domain, self.__service)

        current_dns_table = map_to_current_dns(data, self.__service)
        subdomains, history_dns_table = await aio.gather(
            _process_subdomains(domain, self.__client, self.__provider),
            _process_history(domain, self.__client, self.__provider, self.__service)
        )

        return self.__service.new_summary(
            hostname=Hostname(domain.raw()),
            current=current_dns_table,
            history=history_dns_table,
            subdomains=subdomains
        )