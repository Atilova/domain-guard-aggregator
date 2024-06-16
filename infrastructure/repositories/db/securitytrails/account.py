from typing import (
    Protocol,
    Optional,
    List,
    Tuple
)

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .queries import select_at_least_n_available_requests

from domain.Entities.securitytrails.account import SecurityTrailsAccount
from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountId,
    SecurityTrailsAccountEmail,
    SecurityTrailsAccountPassword,
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountSignUpDate,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)

from infrastructure.adapters.securitytrails.ISecurityTrailsAccountService import ISecurityTrailsAccountService
from infrastructure.db.models.securitytrails import SecurityTrailsAccountModel


def _map_account(
    account: SecurityTrailsAccountModel,
    service: ISecurityTrailsAccountService
) -> SecurityTrailsAccount:
    """_map_account"""

    return service.new_account(
        _id=SecurityTrailsAccountId(account.id),
        email=SecurityTrailsAccountEmail(account.email),
        password=SecurityTrailsAccountPassword(account.password),
        api_key=SecurityTrailsAccountApiKey(account.api_key),
        sign_up_date=SecurityTrailsAccountSignUpDate(account.sign_up_date),
        is_active=SecurityTrailsAccountIsActive(account.is_active),
        available_requests=SecurityTrailsAccountAvailableRequests(account.available_requests)
    )


class SecurityTrailsAccountRepository:
    """SecurityTrailsAccountRepository"""

    def  __init__(self, session: AsyncSession, service: ISecurityTrailsAccountService):
        self.__session = session
        self.__service = service

    async def create(self, account: SecurityTrailsAccount) -> SecurityTrailsAccount:
        db_account = SecurityTrailsAccountModel(
            email=account.email.raw(),
            password=account.password.raw(),
            api_key=account.api_key.raw(),
            is_active=account.is_active.raw(),
            available_requests=account.available_requests.raw()
        )

        self.__session.add(db_account)
        await self.__session.flush()
        await self.__session.refresh(db_account)
        return _map_account(db_account, self.__service)

    async def get(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccount]:
        db_account = await self.__get(account_id)
        if db_account is None: return

        return _map_account(db_account, self.__service)

    async def activate(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccount]:
        return await self.__set_active(account_id, True)

    async def deactivate(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccount]:
        return await self.__set_active(account_id, False)

    async def set_available_requests(self,
        account_id: SecurityTrailsAccountId,
        available_requests: SecurityTrailsAccountAvailableRequests
    ) -> Optional[SecurityTrailsAccount]:
        db_account = await self.__get(account_id)
        if db_account is None: return

        db_account.available_requests = available_requests.raw()
        await self.__session.flush()

        return _map_account(db_account, self.__service)

    async def all_active(self) -> List[SecurityTrailsAccount]:
        return await self.__select_by_active(True)

    async def all_enactive(self) -> List[SecurityTrailsAccount]:
        return await self.__select_by_active(False)

    async def fetch_minimal(self,
        required_request: SecurityTrailsAccountAvailableRequests
    ) -> Tuple[SecurityTrailsAccountAvailableRequests, Tuple[SecurityTrailsAccount, ...]]:
        query = select_at_least_n_available_requests(required_request.raw())
        result = await self.__session.execute(query)
        db_accounts = result.fetchall()

        total_available_requests = db_accounts[-1].total_available_requests
        return SecurityTrailsAccountAvailableRequests(total_available_requests), tuple((
            _map_account(db_account, self.__service)
            for db_account in db_accounts
        ))
    async def update_status(self,
        account_id: SecurityTrailsAccountId, *,
        is_active: SecurityTrailsAccountIsActive,
        available_requests: SecurityTrailsAccountAvailableRequests
    ) -> Optional[SecurityTrailsAccount]:
        db_account = await self.__get(account_id)
        if db_account is None: return

        db_account.is_active = is_active.raw()
        db_account.available_requests = available_requests.raw()
        await self.__session.flush()
        return _map_account(db_account, self.__service)

    async def __select_by_active(self, is_active: bool) -> list[SecurityTrailsAccount]:
        query = select(SecurityTrailsAccountModel).where(SecurityTrailsAccountModel.is_active == is_active)
        result = await self.__session.execute(query)
        db_accounts = result.scalars().all()
        return [
            _map_account(db_account, self.__service)
            for db_account in db_accounts
        ]

    async def __get(self, account_id: SecurityTrailsAccountId) -> Optional[SecurityTrailsAccountModel]:
        query = select(SecurityTrailsAccountModel).where(SecurityTrailsAccountModel.id == account_id.raw())
        result = await self.__session.execute(query)
        db_account = result.scalars().one_or_none()

        return db_account

    async def __set_active(self, account_id: SecurityTrailsAccountId, is_active: bool) -> Optional[SecurityTrailsAccount]:
        db_account = await self.__get(account_id)
        if db_account is None: return

        db_account.is_active = is_active
        await self.__session.flush()

        return _map_account(db_account, self.__service)