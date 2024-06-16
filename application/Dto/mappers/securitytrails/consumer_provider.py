from typing import Dict, Any

from application.adapters.securitytrails.ISecurityTrailsAccountService import ISecurityTrailsAccountService
from application.Dto.securitytrails.consumer_provider import ConsumerToProviderDTO

from domain.ValueObjects.app import AppUniqueId
from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountEmail,
    SecurityTrailsAccountPassword,
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountIsActive    
)


class ApiKeyResponseStatus:
    """ApiKeyResponseStatus"""

    NOT_FOUND = 'not_found'
    FORBIDDEN = 'forbidden'
    PROCESSING = 'processing'
    REJECTED = 'rejected'
    READY = 'ready'


def map_api_key_response(*,
    service: ISecurityTrailsAccountService,
    _id: AppUniqueId,
    data: Dict[str, Any]
) -> ConsumerToProviderDTO:
    """map_api_key_response"""

    try:
        status = data['status']
        payload = data['data']
        error = data['error']

        if status == ApiKeyResponseStatus.READY:
            return ConsumerToProviderDTO(
                _id=_id,
                success=True,
                error=None,
                # Todo: obtain is_active and available_requests from service
                # Todo: wait until it is being implemented
                account=service.new_account(
                    email=SecurityTrailsAccountEmail(payload['email']),
                    password=SecurityTrailsAccountPassword(payload['password']),
                    api_key=SecurityTrailsAccountApiKey(payload['api_key']),
                    is_active=SecurityTrailsAccountIsActive(True)
                )
            )
    except Exception as exp:
        return ConsumerToProviderDTO(
            _id=_id,
            success=False,
            error=f'Failed to map response {exp}.',
            account=None
        )

    return ConsumerToProviderDTO(
        _id=_id,
        success=False,
        error=(error or status),
        account=None
    )