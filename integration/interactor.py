from contextlib import asynccontextmanager

from typing import AsyncIterator

from application.adapters.securitytrails.ISecurityTrailsAccountProvider import ISecurityTrailsAccountProvider
from application.UseCases.DnsAnalyzeDomain import DnsAnalyzeDomain

from domain.Services.dns import DomainDnsService

from infrastructure.services.dns import DnsAnalyzeService


class InteractorFactory:
    """InteractorFactory"""

    def __init__(self, *, provider: ISecurityTrailsAccountProvider):
        self.__analyze_service = DnsAnalyzeService(provider=provider, service=DomainDnsService())

    @asynccontextmanager
    async def analyze_domain(self) -> AsyncIterator[DnsAnalyzeDomain]:
        yield DnsAnalyzeDomain(
            service=self.__analyze_service
        )