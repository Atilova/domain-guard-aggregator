from dataclasses import dataclass

from domain.ValueObjects.base import ValueObject
from domain.Enums.securitytrails.events import SecurityTrailsConsumerEvents


@dataclass(frozen=True)
class SecurityTrailsConsumerEvent(ValueObject[SecurityTrailsConsumerEvents]):
    _value: SecurityTrailsConsumerEvents

    def _validate(self) -> None:
        if not SecurityTrailsConsumerEvents.is_valid(self._value):
            raise ValueError(f'Invalid event: {self._value}')