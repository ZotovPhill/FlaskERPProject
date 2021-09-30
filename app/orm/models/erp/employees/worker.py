import enum
from app.orm.models.base import BaseUUIDModel
from sqlalchemy import (
    Column,
    String,
    Text,
    Unicode,
    DateTime,
    Enum,
)
from sqlalchemy import event
from sqlalchemy.orm import composite
from sqlalchemy_utils import CountryType, PhoneNumber


class MaterialLiabilityType(str, enum.Enum):
    LIMITED = "LIMITED"
    COMPLETE = "COMPLETE"
    COLLECTIVE = "COLLECTIVE"
    INCREASED = "INCREASED"


class Worker(BaseUUIDModel):
    __tablename__ = "emp_worker"
    
    full_name = Column(String, nullable=False)
    birth_date = Column(DateTime)
    position = Column(String)
    entry_date = Column(DateTime)
    dismissal_date = Column(DateTime, nullable=True)
    country_code = Column(CountryType, nullable=False)
    address = Column(Text)
    _phone_number = Column(Unicode(20), nullable=False) # https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/phone_number.html
    phone_number = composite(
        PhoneNumber,
        _phone_number,
        country_code
    )
    contact_person = Column(String, nullable=False)
    material_liability = Column(Enum(MaterialLiabilityType))

    
    
@event.listens_for(Worker, 'before_insert')
def do_stuff(mapper, connect, target: Worker):
# target is an instance of Table
    if target.dismissal_date and target.entry_date < target.dismissal_date:
        raise ValueError("Entry date can`t be less than dismissal date")