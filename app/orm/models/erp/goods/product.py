from app.orm.caching.caching_query import RelationshipCache
from sqlalchemy.dialects.postgresql.base import UUID
from app.orm.models.base import BaseUUIDModel
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils import CountryType


class Product(BaseUUIDModel):
    __tablename__ = "gds_product"
    
    name = Column(String)
    country_of_origin = Column(CountryType)
    expiration_time = Column(DateTime)
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gds_category.id", ondelete="SET NULL")
    )
    category = relationship(
        "Category", 
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('products', lazy='dynamic'),
        remote_side='Category.id'
    )
    unit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gds_unit.id", ondelete="SET NULL")
    )
    unit = relationship(
        "Unit",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('products', lazy='dynamic'),
        remote_side='Unit.id'
    )


# cache_address_bits = (
#     RelationshipCache(Product.category, "default")
#     .and_(RelationshipCache(Product.unit, "default"))
# )
