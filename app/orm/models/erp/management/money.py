from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy import (
    Column,
    Integer,
    String,
)

class MoneyMixin:
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)

    __table_args__ = (
        CheckConstraint(amount >= 0, name='check_non_negative_amount'),
        CheckConstraint("regexp_like(currency, [A-Z]{3})", name='check_valid_currency_code'),
    )