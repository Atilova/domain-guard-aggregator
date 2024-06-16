from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Integer,
    BigInteger,
    String,
    Boolean,
    DateTime
)

from domain.ValueObjects.securitytrails.account import (
    SecurityTrailsAccountId,
    SecurityTrailsAccountEmail,
    SecurityTrailsAccountPassword,
    SecurityTrailsAccountApiKey,
    SecurityTrailsAccountSignUpDate,
    SecurityTrailsAccountIsActive,
    SecurityTrailsAccountAvailableRequests
)

from infrastructure.db.base import BaseModel


class SecurityTrailsAccountModel(BaseModel):
    __tablename__ = 'securitytrails_account'

    id: Mapped[SecurityTrailsAccountId] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    email: Mapped[SecurityTrailsAccountEmail] = mapped_column(
        String(30), nullable=False, unique=True
    )
    password: Mapped[SecurityTrailsAccountPassword] = mapped_column(
        String(32), nullable=False
    )
    api_key: Mapped[SecurityTrailsAccountApiKey] = mapped_column(
        String(64), nullable=False
    )
    sign_up_date: Mapped[SecurityTrailsAccountSignUpDate] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    is_active: Mapped[SecurityTrailsAccountIsActive] = mapped_column(
        Boolean, nullable=False
    )
    available_requests: Mapped[SecurityTrailsAccountAvailableRequests] = mapped_column(
        Integer, nullable=False
    )