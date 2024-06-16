from typing import Protocol, ContextManager, runtime_checkable

from application.UseCases.DnsAnalyzeDomain import DnsAnalyzeDomain


@runtime_checkable
class IInteractorFactory(Protocol):
    """IInteractorFactory"""

    def analyze_domain(self) -> ContextManager[DnsAnalyzeDomain]:
        pass