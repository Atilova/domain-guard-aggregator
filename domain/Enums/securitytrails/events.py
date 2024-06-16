class SecurityTrailsConsumerEvents:
    """SecurityTrailsConsumerEvents"""

    ACCOUNT_RESPONSE = 'account_response'

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.__dict__.values()
    

class SecurityTrailsProducerEvents:
    """SecurityTrailsProducerEvents"""
    
    FABRICATE_ACCOUNT = 'fabricate_account'
    RETRIEVE_ACCOUNT = 'retrieve_account'