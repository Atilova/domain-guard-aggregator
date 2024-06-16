import logging

from asyncio_redis import RedisProtocol, Error, ZScoreBoundary

from time import time

from typing import TypeVar, Generic, List


logger = logging.getLogger(__name__)


T = TypeVar('T', str, bytes)


class StrBytesExpiryStorage(Generic[T]):
    """StrBytesStorage"""

    def __init__(self, *, client: RedisProtocol, key: str):
        self.__client = client
        self.__key = key

    async def add(self, item: T, ttl: int):
        try:
            expire_at = time() + ttl
            await self.__client.zadd(self.__key, { item: expire_at })
        except Error as exp:
            logger.exception(f'Failed to add {item} with TTL {ttl}.')

    async def exists(self, item: T) -> bool:
        try:
            score = await self.__client.zscore(self.__key, item)
            if score is None:
                return False
            elif score > time():
                return True
            await self.remove(item)
            return False
        except Error as exp:
            logger.exception(f'Failed to check existence of {item}.')
        return False

    async def remove(self, item: T) -> None:
        try:
            await self.__client.zrem(self.__key, [item])
        except Error as exp:
            logger.exception(f'Failed to remove {item}.')

    async def remove_expired(self) -> List[T]:
        boundary_min = ZScoreBoundary('-inf')
        boundary_max = ZScoreBoundary(time())
        try:
            expired_items = await self.__client.zrangebyscore(self.__key, boundary_min, boundary_max)
            if expired_items:
                await self.__client.zremrangebyscore(self.__key, boundary_min, boundary_max)

            return [await item for item in expired_items]
        except Error as exp:
            logger.exception('Failed to remove expired items. Error: {e}')
        return []
    
    async def all_alive(self) -> int:
        boundary_min = ZScoreBoundary(time())
        boundary_max = ZScoreBoundary('+inf')
        try:
            return await self.__client.zcount(self.__key, boundary_min, boundary_max)
        except Error as exp:
            logger.exception('Failed to count items not expired.')
        return 0