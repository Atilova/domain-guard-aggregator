from dataclasses import dataclass

from datetime import datetime

from domain.ValueObjects.base import ValueObject


@dataclass(frozen=True)
class SecurityTrailsAccountId(ValueObject[int]):
    _value: int


@dataclass(frozen=True)
class SecurityTrailsAccountEmail(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class SecurityTrailsAccountPassword(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class SecurityTrailsAccountApiKey(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class SecurityTrailsAccountSignUpDate(ValueObject[datetime]):
    _value: datetime


@dataclass(frozen=True)
class SecurityTrailsAccountIsActive(ValueObject[bool]):
    _value: bool

@dataclass(frozen=True)
class SecurityTrailsAccountAvailableRequests(ValueObject[int]):
    _value: int