from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Text
from app.orm.models.base import BaseUUIDModel


class Category(BaseUUIDModel):
    __tablename__ = "gds_category"
    
    name=Column(String)
    description=Column(Text)
    
