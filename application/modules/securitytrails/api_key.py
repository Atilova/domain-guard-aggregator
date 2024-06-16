from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from contextlib import asynccontextmanager

from typing import AsyncIterator, Tuple

from application.adapters.IUnitOfWork import IUnitOfWork
from application.adapters.securitytrails.ISecurityTrailsAccountService import ISecurityTrailsAccountService
from application.adapters.securitytrails.ISecurityTrailsAccountRepository import ISecurityTrailsAccountRepository

from infrastructure.db.uow import SQLAlchemyUoW
from infrastructure.repositories.db.securitytrails.account import SecurityTrailsAccountRepository


class SecurityTrailsAccountModule:
    """SecurityTrailsAccountModule"""

    def __init__(self, *,
            session_factory: async_sessionmaker[AsyncSession],
            service: ISecurityTrailsAccountService,
        ):
        self.__session_factory = session_factory
        self.__service = service        

    @asynccontextmanager
    async def repository(self) -> AsyncIterator[Tuple[IUnitOfWork, ISecurityTrailsAccountRepository]]:
        async with self.__session_factory() as session:
            uow = SQLAlchemyUoW(session)
            repository = SecurityTrailsAccountRepository(session=session,
                                                         service=self.__service)

            yield uow, repository