import logging

from asyncio_redis import RedisProtocol, Error

from typing import TypeVar, Generic


logger = logging.getLogger(__name__)


T = TypeVar('T', str, bytes)


class AsyncSetStorage(Generic[T]):
    """AsyncSetStorage"""

    def __init__(self, *, client: RedisProtocol, key: str):
        self.__client = client
        self.__key = key

    async def add(self, encodable: T):
        try:
            await self.__client.sadd(self.__key, [encodable])
        except Error as exp:
            logger.exception(f'Error occurred while adding item to set ({self.__key}).')

    async def remove(self, encodable: T):
        try:
            await self.__client.srem(self.__key, [encodable])
        except Error as exp:
            logger.exception(f'Error occurred while removing item from set: {encodable} on ({self.__key}).')

    async def exists(self, encodable: T) -> bool:
        try:
            return await self.__client.sismember(self.__key, encodable)
        except Error as exp:
            logger.exception(f'Error occurred while checking existence of item: {encodable} on ({self.__key}).')
        return False