import os
from dataclasses import dataclass, field


def _boolean(value: str) -> bool:
    """_boolean"""

    return bool(int(value))


@dataclass
class PostgreSQLConfig:
    """PostgreSQLConfig"""

    db: str
    host: str
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    uri: str = field(init=False)

    def __post_init__(self):
        self.uri = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


@dataclass
class RabbitMQConfig:
    """RabbitMQConfig"""

    host: str
    port: int
    user: str
    password: str
    is_ssl: bool
    v_host: str = '/'
    uri: str = field(init=False)

    def __post_init__(self):
        protocol = { True: 'amqps://', False: 'amqp://' }[self.is_ssl]
        self.uri = f'{protocol}{self.user}:{self.password}@{self.host}:{self.port}{self.v_host}'


@dataclass
class RedisConfig:
    """RedisConfig"""

    host: str
    port: int = 6379
    user: str = ''
    password: str = ''
    uri: str = field(init=False)

    def __post_init__(self):
        self.uri = f'redis://{self.user}:{self.password}@{self.host}:{self.port}/'

    def get_db_uri(self, db: int):
        return f'{self.uri}{db}'


@dataclass
class SecurityTrailsGatewayConfig:
    """SecurityTrailsGatewayConfig"""

    consumer_exchange: str
    consumer_queue: str
    consumer_routing_key: str
    producer_exchange: str
    producer_queue: str
    producer_routing_key: str


@dataclass
class SecurityTrailsProviderConfig:
    """SecurityTrailsProviderConfig"""

    redis_db: int
    requests_capacity: int
    requests_per_account: int
    max_pending_requests: int
    storage_uuid_expire_time: int
    sync_inaccuracy: int


@dataclass
class ServiceGatewayConfig:
    """ServiceGatewayConfig"""

    consumer_exchange: str
    consumer_queue: str
    consumer_routing_key: str
    producer_exchange: str
    producer_queue: str
    producer_routing_key: str


@dataclass
class Config:
    """Config"""

    is_development: bool
    postgresql: PostgreSQLConfig
    rabbitmq: RabbitMQConfig
    redis: RedisConfig
    securitytrails_gateway: SecurityTrailsGatewayConfig
    securitytrails_provider: SecurityTrailsProviderConfig
    service_gateway: ServiceGatewayConfig


def load_postgresql_config() -> PostgreSQLConfig:
    """load_postgresql_config"""

    db: str = os.environ.get('POSTGRESQL_DB', 'domain_guard_aggregator')
    host: str = os.environ.get('POSTGRESQL_HOST', 'localhost')
    port: int = int(os.environ.get('POSTGRESQL_PORT', 5432))
    user: str = os.environ.get('POSTGRESQL_USER', 'postgres')
    password: str = os.environ.get('POSTGRESQL_PASSWORD', 'postgres')

    return PostgreSQLConfig(
        db=db,
        host=host,
        port=port,
        user=user,
        password=password
    )

def load_rabbitmq_config() -> RabbitMQConfig:
    """load_rabbitmq_config"""

    host: str = os.environ.get('RABBITMQ_HOST', 'localhost')
    port: int = int(os.environ.get('RABBITMQ_PORT', 5672))
    user: str = os.environ.get('RABBITMQ_USER', 'guest')
    password: str = os.environ.get('RABBITMQ_PASSWORD', 'guest')
    v_host: str = os.environ.get('RABBITMQ_V_HOST', '/')
    is_ssl: bool = _boolean(os.environ.get('RABBITMQ_IS_SSL', False))

    return RabbitMQConfig(
        host=host,
        port=port,
        user=user,
        password=password,
        v_host=v_host,
        is_ssl=is_ssl
    )

def load_redis_config() -> RedisConfig:
    """load_redis_config"""

    host: str = os.environ.get('REDIS_HOST', 'localhost')
    port: int = int(os.environ.get('REDIS_PORT', 6379))
    user: str = os.environ.get('REDIS_USER', '')
    password: str = os.environ.get('REDIS_PASSWORD', '')

    return RedisConfig(
        host=host,
        port=port,
        user=user,
        password=password
    )

def load_securitytrails_gateway_config() -> SecurityTrailsGatewayConfig:
    """load_securitytrails_gateway_config"""

    consumer_exchange: str = os.environ.get('SECURITYTRAILS_GATEWAY_CONSUMER_EXCHANGE', 'exchange')
    consumer_queue: str = os.environ.get('SECURITYTRAILS_GATEWAY_CONSUMER_QUEUE', 'consumer.default')
    consumer_routing_key: str = os.environ.get('SECURITYTRAILS_GATEWAY_CONSUMER_ROUTING_KEY', 'consumer.key')
    producer_exchange: str = os.environ.get('SECURITYTRAILS_GATEWAY_PRODUCER_EXCHANGE', 'exchange')
    producer_queue: str = os.environ.get('SECURITYTRAILS_GATEWAY_PRODUCER_QUEUE', 'producer.res')
    producer_routing_key: str = os.environ.get('SECURITYTRAILS_GATEWAY_PRODUCER_ROUTING_KEY', 'producer.res')

    return SecurityTrailsGatewayConfig(
        consumer_exchange=consumer_exchange,
        consumer_queue=consumer_queue,
        consumer_routing_key=consumer_routing_key,
        producer_exchange=producer_exchange,
        producer_queue=producer_queue,
        producer_routing_key=producer_routing_key
    )

def load_securitytrails_provider_config() -> SecurityTrailsProviderConfig:
    """load_securitytrails_provider_config"""

    redis_db: int = int(os.environ.get('PROVIDER_REDIS_DB', 0))
    requests_capacity: int = int(os.environ.get('PROVIDER_REQUESTS_CAPACITY', 100))
    requests_per_account: int = int(os.environ.get('PROVIDER_REQUESTS_PER_ACCOUNT', 50))
    max_pending_requests: int = int(os.environ.get('PROVIDER_MAX_PENDING_REQUESTS', 5))
    storage_uuid_expire_time: int = int(os.environ.get('PROVIDER_STORAGE_UUID_EXPIRE_TIME', 800))
    sync_inaccuracy: int = int(os.environ.get('PROVIDER_SYNC_INACCURACY', 70))

    return SecurityTrailsProviderConfig(
        redis_db=redis_db,
        requests_capacity=requests_capacity,
        requests_per_account=requests_per_account,
        max_pending_requests=max_pending_requests,
        storage_uuid_expire_time=storage_uuid_expire_time,
        sync_inaccuracy=sync_inaccuracy
    )

def load_service_gateway_config() -> ServiceGatewayConfig:
    """load_service_gateway_config"""

    consumer_exchange: str = os.environ.get('SERVICE_GATEWAY_CONSUMER_EXCHANGE', 'exchange')
    consumer_queue: str = os.environ.get('SERVICE_GATEWAY_CONSUMER_QUEUE', 'aggregator.req')
    consumer_routing_key: str = os.environ.get('SERVICE_GATEWAY_CONSUMER_ROUTING_KEY', 'aggregator.req')
    producer_exchange: str = os.environ.get('SERVICE_GATEWAY_PRODUCER_EXCHANGE', 'exchange')
    producer_queue: str = os.environ.get('SERVICE_GATEWAY_PRODUCER_QUEUE', 'aggregator.res')
    producer_routing_key: str = os.environ.get('SERVICE_GATEWAY_PRODUCER_ROUTING_KEY', 'aggregator.res')

    return ServiceGatewayConfig(
        consumer_exchange=consumer_exchange,
        consumer_queue=consumer_queue,
        consumer_routing_key=consumer_routing_key,
        producer_exchange=producer_exchange,
        producer_queue=producer_queue,
        producer_routing_key=producer_routing_key
    )

def load() -> Config:
    """load"""

    is_development: bool = _boolean(os.environ.get('IS_DEVELOPMENT', True))
    postgresql = load_postgresql_config()
    rabbitmq = load_rabbitmq_config()
    redis = load_redis_config()
    securitytrails_gateway = load_securitytrails_gateway_config()
    securitytrails_provider = load_securitytrails_provider_config()
    service_gateway = load_service_gateway_config()

    return Config(
        is_development=is_development,
        postgresql=postgresql,
        rabbitmq=rabbitmq,
        redis=redis,
        securitytrails_gateway=securitytrails_gateway,
        securitytrails_provider=securitytrails_provider,
        service_gateway=service_gateway
    )