from typing import Protocol


class IDnsAnalyzeService(Protocol):
    """IDnsAnalyzeService"""

    async def analyze(self) -> None:
        pass