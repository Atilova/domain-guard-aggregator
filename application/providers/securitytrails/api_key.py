import logging

import asyncio as aio
from math import ceil
from uuid import uuid4

from typing import (
    Dict,
    Generic,
    TypeVar,
    TypedDict,
    Set,
    Hashable,
    Callable
)

from utils.cancel_tasks import cancel_all

from application.adapters.IStrBytesExpiryStorage import IStrBytesExpiryStorage
from application.adapters.securitytrails.ISecurityTrailsApiKeyProducer import ISecurityTrailsApiKeyProducer
from application.adapters.securitytrails.ISecurityTrailsAccountModule import ISecurityTrailsAccountModule
from application.adapters.securitytrails.ISecurityTrailsApiKeyService import ISecurityTrailsApiKeyService
from application.Dto.securitytrails.consumer_provider import ConsumerToProviderDTO

from domain.Entities.securitytrails.account import SecurityTrailsAccount
from domain.ValueObjects.app import AppUniqueId
from domain.ValueObjects.securitytrails.account import SecurityTrailsAccountAvailableRequests

from infrastructure.config import SecurityTrailsProviderConfig


logger = logging.getLogger('SecurityTrailsAccountProvider')


T = TypeVar('T', bound=Hashable, covariant=True)


class ReusableQueueItem(TypedDict):
    retrievals: int
    expiries_after: int
    expired: bool


# Todo add unit tests
class AsyncReusableQueue(Generic[T]):
    """An asynchronous queue with support for reusable items and expiration tracking."""

    def __init__(self, id_mapper: Callable[[T], Hashable]=lambda item: item):
        self.__mapper = id_mapper
        self.__queue = aio.Queue()
        self.__expirations: Dict[T, ReusableQueueItem] = {}
        self.__remaining_gets = 0
        self.__lock = aio.Lock()

    async def put(self, item: T, expires_after: int) -> None:
        """Put an item into the queue with expiration settings."""

        if expires_after <= 0: raise ValueError(':expires_after should be greater then zero.')

        self.__expirations[self.__mapper(item)] = {
            'expiries_after': expires_after,
            'retrievals': 0,
            'expired': False
        }
        await self.__queue.put(item)
        async with self.__lock:
            self.__remaining_gets += expires_after

    async def get(self) -> T:
        """Get an item from the queue, considering expiration settings."""

        item: T = await self.__queue.get()
        key = self.__mapper(item)
        item_expiration = self.__expirations[key]

        if item_expiration['expired']:
            del self.__expirations[key]
            return await self.get()

        async with self.__lock:
            self.__remaining_gets -= 1

        if item_expiration['retrievals'] >= item_expiration['expiries_after']:
            del self.__expirations[key]
            return item

        item_expiration['retrievals'] += 1
        await self.__queue.put(item)
        return item

    async def expire(self, item: T):
        key = self.__mapper(item)
        if not key in self.__expirations: return

        self.__expirations[key]['expired'] = True
        not_retrieved = self.__expirations[key]['expiries_after'] - self.__expirations[key]['retrievals']
        async with self.__lock:
            self.__remaining_gets -= not_retrieved

    async def flush(self) -> None:
        async with self.__lock:
            while not self.__queue.empty():
                self.__queue.get_nowait()
                self.__queue.task_done()

            self.__queue = aio.Queue()
            self.__expirations.clear()
            self.__remaining_gets = 0

    @property
    def length(self) -> int:
        """Get the total number of remaining retrievals allowed for all items in the queue."""

        return self.__remaining_gets


class SecurityTrailsAccountProvider:
    """SecurityTrailsAccountProvider"""

    def __init__(self, *,
        config: SecurityTrailsProviderConfig,
        loop: aio.AbstractEventLoop,
        producer: ISecurityTrailsApiKeyProducer,
        module: ISecurityTrailsAccountModule,
        storage: IStrBytesExpiryStorage[str],
        service: ISecurityTrailsApiKeyService
    ):
        self.__config = config
        self.__loop = loop
        self.__producer = producer
        self.__module = module
        self.__storage = storage
        self.__service = service
        self.__inner_queue: AsyncReusableQueue[SecurityTrailsAccount] = AsyncReusableQueue(
            id_mapper=lambda account: account.api_key.raw()
        )
        self.__aio_tasks: Set[aio.Task] = set()
        self.__loading_accounts = False

    async def initialize(self):
        return await self.__health_check()

    async def get(self) -> SecurityTrailsAccount:
        return await self.__get_account()

    async def expire_account(self, account: SecurityTrailsAccount) -> SecurityTrailsAccount:
        _account = await self.__health_check_account_api_key(account)
        async with self.__module.repository() as (uow, repository):
            logger.info((
                f'Updating account: {account._id}; '
                f'IsActive: {_account.is_active.raw()}; '
                f'Request: {_account.available_requests.raw()}.'
            ))
            updated_account = await repository.update_status(
                account._id,
                is_active=_account.is_active,
                available_requests=_account.available_requests
            )
            await uow.commit()
        return updated_account

    async def response(self, dto: ConsumerToProviderDTO) -> None:
        await self.__handle_response(dto)
        await self.__storage.remove_expired()

    async def shutdown(self) -> None:
        await cancel_all(self.__aio_tasks)
        self.__aio_tasks.clear()

    async def __fetch_and_fill_minimal(self):
        await self.__inner_queue.flush()

        required = self.__config.requests_capacity
        async with self.__module.repository() as (_, repository):
            activate_requests, accounts = await repository.fetch_minimal(
                SecurityTrailsAccountAvailableRequests(required)
            )

        logger.debug(f'Required {required}, received {activate_requests.raw()} available requested.')
        for account in accounts:
            await self.__add_account_to_inner_queue(account)

    async def __add_account_to_inner_queue(self, account: SecurityTrailsAccount):
        await self.__inner_queue.put(account, expires_after=account.available_requests.raw())

    # Todo: move to pure function
    async def __health_check(self):
        try:
            await self.__storage.remove_expired()

            total_available_requests = self.__available_requests
            if not self.__loading_accounts and total_available_requests >= self.__config.requests_capacity - self.__config.sync_inaccuracy:
                return logger.debug(f'Sufficient available accounts: {total_available_requests}.')

            if not self.__loading_accounts:
                await self.__fetch_and_fill_minimal()

            total_available_requests = self.__available_requests
            if total_available_requests >= self.__config.requests_capacity:
                return logger.debug(f'Sufficient available accounts refilled: {total_available_requests}.')

            self.__loading_accounts = True

            total_available_requests = self.__available_requests
            pending_accounts = await self.__pending_accounts
            accounts_to_request = ceil(
                (self.__config.requests_capacity-total_available_requests) / self.__config.requests_per_account
            )
            demand = accounts_to_request - pending_accounts

            if demand <= 0:
                if not pending_accounts:
                    self.__loading_accounts = False
                return logger.debug(f'No new accounts required. Demand: {demand}.')

            if pending_accounts >= self.__config.max_pending_requests:
                return logger.debug('Unable to request, limit of pending requests reached.')

            available_account_requests = self.__config.max_pending_requests - pending_accounts
            available_demand = min(demand, available_account_requests)

            logger.debug(f'Available demand: {available_demand}.')

            for _ in range(available_demand):
                task = self.__loop.create_task(
                    self.__fabricate_new_account()
                )
                task.add_done_callback(self.__task_completed)
                self.__aio_tasks.add(task)
        except Exception as exp:
            logger.exception('FUCKING ERROR: ')

    async def __fabricate_new_account(self):
        request_id = AppUniqueId(uuid4().hex)
        await self.__storage.add(request_id.raw(), ttl=self.__config.storage_uuid_expire_time)
        await self.__producer.fabricate_account(request_id)

    def __task_completed(self, task: aio.Task) -> None:
        self.__aio_tasks.discard(task)

    async def __handle_response(self, dto: ConsumerToProviderDTO):
        await self.__storage.remove(dto._id.raw())

        is_success = dto.success
        if is_success:
            account = await self.__health_check_account_api_key(dto.account)
            await self.__add_new_account(account)
        else:
            logger.warning(f'Account fabrication failure: {dto.error}.')
        await self.__health_check()

    async def __health_check_account_api_key(self, account: SecurityTrailsAccount) -> SecurityTrailsAccount:
        is_active, requests = await self.__service.verify(account.api_key)
        account.set_is_active(is_active)
        account.set_available_requests(requests)

        logger.info((
            f'Verified ApiKey: {account.api_key.raw()}; '
            f'IsActive: {is_active.raw()}; Requests: {requests.raw()}; '
            f'Requests: {requests.raw()}.'
        ))
        return account

    async def __add_new_account(self, account: SecurityTrailsAccount):
        async with self.__module.repository() as (uow, repository):
            new_account = await repository.create(account)
            await uow.commit()

        await self.__add_account_to_inner_queue(new_account)
        logger.debug('Account created and added to queue.')

    async def __get_account(self) -> SecurityTrailsAccount:
        await self.__health_check()

        account: SecurityTrailsAccount = await self.__inner_queue.get()
        account.decrement_requests()

        async with self.__module.repository() as (uow, repository):
            await repository.set_available_requests(account._id,
                                                    available_requests=account.available_requests)

            if not account.is_available_requests:
                logger.debug(f'Account expired, deactivating. ID: {account._id}.')
                await repository.deactivate(account._id)
            await uow.commit()

        await self.__health_check()

        logger.debug(f'Returning account: {account._id}.')
        return account

    @property
    def __available_requests(self):
        return self.__inner_queue.length

    @property
    async def __pending_accounts(self):
        return await self.__storage.all_alive()