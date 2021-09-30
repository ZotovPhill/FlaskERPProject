from app.orm.models.base import BaseUUIDModel
from sqlalchemy import (
    Column,
    String,
    Text,
    Unicode
)
from sqlalchemy.orm import composite
from sqlalchemy_utils import CountryType, PhoneNumber


class Supplier(BaseUUIDModel):
    __tablename__ = "emp_supplier"
    
    title = Column(String, nullable=False)
    iban_code = Column(String, nullable=False)  # https://pythonhosted.org/schwifty/
    country_code = Column(CountryType, nullable=False)
    address = Column(Text)
    _phone_number = Column(Unicode(20), nullable=False) # https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/phone_number.html
    phone_number = composite(
        PhoneNumber,
        _phone_number,
        country_code
    )
    contact_person = Column(String, nullable=False)
    position = Column(String)