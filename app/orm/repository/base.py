from functools import lru_cache
from app.orm.caching.caching_query import FromCache
import math
from flask_sqlalchemy import Pagination
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session
from sqlalchemy import func
from app.core.constants import DEFAULT_LIMIT
from contextlib import contextmanager
from app.core.extensions import db
from app.orm.caching.environment import cache

@lru_cache
def cached_session_scope():
    session = db.create_scoped_session(options={"autoflush": False, "expire_on_commit": False})
    cache.listen_on_session(session)
    
    return session

@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    class ThingOne(object):
    def go(self, session):
        session.query(FooBar).update({"x": 5})

    def run_my_program():
        with session_scope() as session:
            ThingOne().go(session)
    """
    session = db.create_scoped_session(options={"autoflush": False, "expire_on_commit": False})
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Meta(type):
    def __new__(cls, name, bases, attrs):        
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if attrname ==  '__model__':
                newattrs[attrname.removesuffix('__').removeprefix('__')] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super().__new__(cls, name, bases, newattrs)

        

class BaseRepository(metaclass=Meta):
    def list_paginate(
        self,
        session: Session,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0
    ):
        return session.query(self.model).order_by(self.model.id).options(FromCache("default")).all()
        
        return Pagination(
            query,
            page=int(math.floor(offset / limit) + 1), 
            per_page=limit, 
            total=query.count(), 
            items=query.limit(limit).offset(offset)
        )
    
    def find_all(self, session: Session):
        return session.query(self.model).all()
    
    def find(self, session: Session, id: str):
        return session.query(self.model).get(id)
    
    def count(self, session: Session):
        return session.query(func.count(self.model.id)).scalar()

