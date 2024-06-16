from dataclasses import dataclass

from utils.is_root_domain import is_root_domain

from domain.ValueObjects.base import ValueObject


@dataclass(frozen=True)
class AppUniqueId(ValueObject[str]):
    _value: str

    def _validate(self) -> None:
        if not isinstance(self._value, str):
            raise TypeError(f'AppUniqueId received invalid type: {type(self._value)}, {self._value}')
        

@dataclass(frozen=True)
class Domain(ValueObject[str]):
    _value: str

    def _validate(self) -> None:
        if not is_root_domain(self._value):
            raise ValueError(f'Received invalid domain name: {self._value}.')