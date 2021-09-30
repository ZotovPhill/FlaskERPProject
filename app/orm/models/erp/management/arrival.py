from app.orm.models.base import BaseUUIDModel
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import UUID


class Arrival(BaseUUIDModel):
    __tablename__ = "mgt_arrival"
    
    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey("emp_supplier.id", ondelete="SET NULL")
    )
    supplier = relationship(
        "Supplier",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('arrivals', lazy='dynamic')
    )
    power_of_attorney = Column(String, nullable=False) # best approach to create table for document
    date_of_issue = Column(DateTime)
    responsible_worker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("emp_worker.id", ondelete="SET NULL")
    )
    responsible_worker = relationship(
        "Worker",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('arrivals', lazy='dynamic')
    )
    arrival_date = Column(DateTime)
