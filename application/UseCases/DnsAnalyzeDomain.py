from application.adapters.Interactor import Interactor
from application.adapters.IDnsAnalyzeService import IDnsAnalyzeService

from application.Dto.dns import (
    ResultCode,
    DomainAnalysisInputDTO,
    DomainAnalysisOutputDTO
)
from application.Dto.mappers.dns import map_data_to_dns_output_dto

from domain.ValueObjects.app import Domain


class DnsAnalyzeDomain(Interactor[DomainAnalysisInputDTO, DomainAnalysisOutputDTO]):
    """DnsAnalyzeDomain"""

    def __init__(self, service: IDnsAnalyzeService):
        self.__service = service

    async def __call__(self, data: DomainAnalysisInputDTO) -> DomainAnalysisOutputDTO:
        try:
            domain = Domain(data.domain)
        except ValueError:
            return DomainAnalysisOutputDTO(code=ResultCode.INVALID_DOMAIN)

        result = await self.__service.analyze(domain)
        mapped = map_data_to_dns_output_dto(result)
        return mapped