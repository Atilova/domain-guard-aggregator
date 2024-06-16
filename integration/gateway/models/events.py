class ConsumerEvents:
    """ConsumerEvents"""

    ANALYZE_DOMAIN = 'analyze_domain'

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.__dict__.values()