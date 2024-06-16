from  asyncio_redis import Connection

from infrastructure.config import RedisConfig


async def get_redis_factory(config: RedisConfig, db: int=0):
    """get_redis_factory"""
    
    
    return await Connection.create(
        host=config.host,
        port=config.port,
        password=config.password,
        db=db,
        auto_reconnect=True
    )