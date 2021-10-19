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
            unit_repository.find(1)
            ThingOne().go(session)
    """
    session = db.create_scoped_session(options={"autoflush": False, "expire_on_commit": False})
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()



class BaseRepository:
    def __init__(self):
        self.model = None

    def list_paginate(self):
        with session_scope() as session:
            return session.query(self.model).order_by(self.model.id).options(FromCache("default")).all()
        
    def find_all(self):
        with session_scope() as session:
            return session.query(self.model).all()
    
    def find(self, id: str):
        with session_scope() as session:
            return session.query(self.model).get(id)
    
    def count(self, session: Session):
        with session_scope() as session:
            return session.query(func.count(self.model.id)).scalar()

    def create(self):
        with session_scope() as session:
            # create logic
            session.commit()
