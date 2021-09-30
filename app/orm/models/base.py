from typing import Mapping
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.core.extensions import db


class BaseModel(object):
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    
    def _process_args(cls, attr, out_args, out_kwargs):
        args = cls.__dict__.get(attr, None)
        if not args:
            raise AttributeError

        if isinstance(args, Mapping):  # it's a dictionary
            out_kwargs.update(args)
        else:  # it's a list
            if isinstance(args[-1], Mapping):  # it has a dictionary at the end
                out_kwargs.update(args.pop())

            out_args.extend(args)

    @declared_attr
    def __table_args__(cls):
        args = []
        kwargs = {}

        for mixin in reversed(cls.mro()):
            cls._process_args(mixin, '__table_args__', args, kwargs)

        cls._process_args(cls, '__local_table_args__', args, kwargs)

        args.append(kwargs)  # [item, item, ...,  kwargs]
        return tuple(args)

    
class BaseIDModel(db.Model, BaseModel):
    __abstract__ = True
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
 
class BaseUUIDModel(db.Model, BaseModel):
    __abstract__ = True
    __table_args__ = ()
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
