import logging

from aiohttp import ClientSession
from http import HTTPStatus as status

from functools import partial

from .types.records import RecordType
from .types.data import (
    ApiKeyUsage,
    DomainData,
    SubDomainData,
    DnsHistoryData
)
from .types.response import (
    BaseStatus,
    BaseResponse
)
from .mappers import (
    usage_mapper,
    domain_mapper,
    subdomains_mapper,
    history_dns_mapper
)


logger = logging.getLogger('SecurityTrailsClient')


# Todo: make these types similar to ValueObjects and add custom validation errors.
DomainT = str
ApiKeyT = str

BASE_URL = 'https://api.securitytrails.com/v1'
ENDPOINTS = {
    'usage': f'{BASE_URL}/account/usage/',
    'base_domain': lambda domain: f'{BASE_URL}/domain/{domain}/',
    'subdomain_list': lambda domain: f'{BASE_URL}/domain/{domain}/subdomains/',
    'history_dns': lambda domain, record_type: f'{BASE_URL}/history/{domain}/dns/{record_type}/'
}
STATUS_BY_DETAILS = {
    'The requested domain is invalid': BaseStatus.INVALID_DOMAIN
}

def _headers(api_key: str):
    """_headers"""

    return {
        'APIKEY': api_key,
        'Content-Type': 'application/json'
    }

def _params(api_key: str):
    """_params"""

    return {
        'headers': _headers(api_key)
    }

async def _fetch(url, *, mapper, **params) -> BaseResponse:
    """_fetch"""

    async with ClientSession() as session:
        async with session.get(url, **params) as response:
            match response.status:
                case status.OK:
                    data = await response.json()
                    return BaseResponse(status=BaseStatus.FETCHED, response=mapper(data))

                case status.TOO_MANY_REQUESTS:
                    return BaseResponse(status=BaseStatus.API_KEY_EXHAUSTED)

                case status.BAD_REQUEST:
                    details = await response.json()
                    detailed_status = STATUS_BY_DETAILS.get(details.get('message'))
                    if detailed_status is None:
                        logger.warning(f'Received unknown details: {details} from {url}.')
                    return BaseResponse(status=detailed_status or BaseResponse.UNDEFINED)

                case status.UNAUTHORIZED:
                    return BaseResponse(status=BaseStatus.UNAUTHORIZED)

                case status.NOT_FOUND:
                    return BaseResponse(status=BaseStatus.NO_INFO)

                case _:
                    logger.warning(f'Encountered unknown server reponse status: {response.status}.')
                    return BaseResponse(status=BaseStatus.UNDEFINED)


class SecurityTrailsClient:
    """
    SecurityTrails Async Python Wrapper.
    Partial implementation of production release from https://jsapi.apiary.io/apis/securitytrailsrestapi/introduction/authentication.html

        Available Functions
        - get_usage                 Provides a method to retrieve current account usage.
        - get_domain                Domain information endpoints that return various information about domains.
        - get_subdomain             Returns subdomains for a given domain.
        - get_history_dns           Lists out specific historical information about the given domain parameter.
    """

    async def get_usage(self, api_key: ApiKeyT) -> BaseResponse[ApiKeyUsage]:
        endpoint = ENDPOINTS['usage']
        return await _fetch(endpoint, mapper=usage_mapper, **_params(api_key))

    async def get_domain(self,
        domain: DomainT, *,
        api_key: ApiKeyT
    ) -> BaseResponse[DomainData]:
        endpoint = ENDPOINTS['base_domain'](domain)
        return await _fetch(endpoint, mapper=domain_mapper, **_params(api_key))

    async def get_subdomains(self,
        domain: DomainT, *,
        api_key: ApiKeyT
    ) -> BaseResponse[SubDomainData]:
        endpoint = ENDPOINTS['subdomain_list'](domain)
        return await _fetch(endpoint, mapper=subdomains_mapper, **_params(api_key))

    async def get_history_dns(self,
        domain: DomainT,
        record_type: RecordType, *,
        api_key: ApiKeyT
    ) -> BaseResponse[DnsHistoryData]:
        if not record_type in RecordType:
            raise TypeError(f'get_history_dns received inappropriate record_type: {record_type}')

        endpoint = ENDPOINTS['history_dns'](domain, record_type.value)
        return await _fetch(endpoint, mapper=partial(history_dns_mapper, type=record_type), **_params(api_key))