from app.orm.models.erp.management.money import MoneyMixin
from sqlalchemy.sql.schema import CheckConstraint
from app.orm.models.base import BaseIDModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import UUID


class GoodsArrival(BaseIDModel, MoneyMixin):
    __tablename__ = "mgt_goods_arrival"
    
    arrival_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mgt_arrival.id", ondelete="CASCADE")
    )
    arrival = relationship(
        "Arrival",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('goods_arrivals', lazy='dynamic')
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gds_product.id", ondelete="CASCADE")
    )
    product = relationship(
        "Product",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('goods_arrivals', lazy='dynamic')
    )
    quantity = Column(Integer, nullable=False)
    
    
    __table_args__ = (
        CheckConstraint(quantity >= 0, name='check_non_negative_quantity'),
    )
