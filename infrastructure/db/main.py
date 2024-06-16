import logging

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from .uow import SQLAlchemyUoW

from infrastructure.config import PostgreSQLConfig


async def get_engine_factory(config: PostgreSQLConfig) -> AsyncGenerator[AsyncEngine, None]:
    """get_engine_factory"""

    engine = create_async_engine(config.uri, future=True)

    logging.info("Engine is created.")

    yield engine

    await engine.dispose()

    logging.info("Engine is disposed.")


async def get_async_sessionmaker_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """get_async_sessionmaker"""

    session_factory = async_sessionmaker(engine, expire_on_commit=False, 
                                         class_=AsyncSession)

    return session_factory


def get_uow_factory(session: AsyncSession) -> SQLAlchemyUoW:
    """get_uow_factory"""
    
    return SQLAlchemyUoW(session)