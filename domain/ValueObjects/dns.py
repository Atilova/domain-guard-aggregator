from dataclasses import dataclass

from domain.ValueObjects.base import ValueObject


@dataclass(frozen=True)
class Hostname(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class FirstSeen(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class LastSeen(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class LastSeen(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Count(ValueObject[int]):
    _value: int


@dataclass(frozen=True)
class Organization(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Host(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class SubDomain(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Priority(ValueObject[int]):
    _value: int


@dataclass(frozen=True)
class Ipv4(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Ipv6(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Nameserver(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Ttl(ValueObject[int]):
    _value: int


@dataclass(frozen=True)
class Email(ValueObject[str]):
    _value: str


@dataclass(frozen=True)
class Txt(ValueObject[str]):
    _value: str