import logging

from integration.adapters.IInteractorFactory import IInteractorFactory
from integration.gateway.adapters.IProducer import IProducer
from integration.gateway.models.request import RpcRequest

from application.Dto.dns import DomainAnalysisInputDTO, DomainAnalysisOutputDTO


logger = logging.getLogger('DomainController')


class DomainController:
    """DomainController"""

    def __init__(self, *,
        ioc: IInteractorFactory,
        producer: IProducer
    ):
        self.__ioc = ioc
        self.__producer = producer

    async def analyze(self, request: RpcRequest) -> None:
        domain_name = request.data.get('domain')
        logger.info(f'Analyzing domain: {domain_name}.')
        async with self.__ioc.analyze_domain() as analyze_domain:
            result: DomainAnalysisOutputDTO = await analyze_domain(DomainAnalysisInputDTO(
                domain=domain_name
            ))

        dicted = result.to_dict()
        await self.__producer.reply_domain_analysis(
            message=request.message,
            data=dicted
        )