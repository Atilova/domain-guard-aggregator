import asyncio as aio

from config import conf

from integration.interactor import InteractorFactory
from integration.gateway.views.producer import GatewayProducer
from integration.gateway.views.rpc_consumer import RpcGatewayChannel
from integration.gateway.controllers.domain import DomainController

from application.providers.securitytrails.api_key import SecurityTrailsAccountProvider
from application.modules.securitytrails.api_key import SecurityTrailsAccountModule
from application.channels.securitytrails.api_key import SecurityTrailsApiKeyChannel
from application.producers.securitytrails.api_key import SecurityTrailsApiKeyProducer

from domain.Services.securitytrails.account import SecurityTrailsAccountService

from infrastructure.consumer.main import AsyncConsumer
from infrastructure.db.main import (
    get_engine_factory,
    get_async_sessionmaker_factory
)
from infrastructure.redis.main import get_redis_factory
from infrastructure.repositories.storage.bytes import StrBytesExpiryStorage
from infrastructure.services.securitytrails.api_key import SecurityTrailsApiKeyService


async def main(loop: aio.AbstractEventLoop):
    """main"""

    db_engine_factory = get_engine_factory(conf.postgresql)
    db_engine = await anext(db_engine_factory)
    db_session_factory = await get_async_sessionmaker_factory(db_engine)

    redis_client = await get_redis_factory(conf.redis, conf.securitytrails_provider.redis_db)
    provider_storage = StrBytesExpiryStorage(client=redis_client, key='provider:uuids')

    consumer =  AsyncConsumer(config=conf.rabbitmq, loop=loop)

    securitytrails_producer = SecurityTrailsApiKeyProducer(config=conf.securitytrails_gateway)
    securitytrails_module = SecurityTrailsAccountModule(
        session_factory=db_session_factory,
        service=SecurityTrailsAccountService()
    )
    securitytrails_provider = SecurityTrailsAccountProvider(
        config=conf.securitytrails_provider,
        loop=loop,
        producer=securitytrails_producer,
        module=securitytrails_module,
        storage=provider_storage,
        service=SecurityTrailsApiKeyService()
    )
    securitytrails_channel = SecurityTrailsApiKeyChannel(
        config=conf.securitytrails_gateway,
        provider=securitytrails_provider,
        loop=loop,
        service=SecurityTrailsAccountService()
    )

    ioc = InteractorFactory(
        provider=securitytrails_provider
    )

    gateway_producer = GatewayProducer(
        config=conf.service_gateway
    )

    gateway_domain_controller = DomainController(
        ioc=ioc,
        producer=gateway_producer
    )

    rpc_gateway_channel = RpcGatewayChannel(
        config=conf.service_gateway,
        loop=loop,
        controller=gateway_domain_controller
    )

    consumer.add(rpc_gateway_channel)
    consumer.add(securitytrails_channel)
    consumer.add_producer(gateway_producer)
    consumer.add_producer(securitytrails_producer)

    await consumer.connect()

    initialize_provider = securitytrails_provider.initialize()
    loop.create_task(initialize_provider)