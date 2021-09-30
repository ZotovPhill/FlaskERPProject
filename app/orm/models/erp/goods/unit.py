from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Text
from app.orm.models.base import BaseUUIDModel


class Unit(BaseUUIDModel):
    __tablename__ = "gds_unit"

    name=Column(String)
    description=Column(Text)