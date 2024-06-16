from typing import Protocol


class IUnitOfWork(Protocol):
    """IUnitOfWork"""

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass