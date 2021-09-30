from flask_sqlalchemy import SQLAlchemy, SignallingSession
from flask_caching import Cache
from flask_marshmallow import Marshmallow
from sqlalchemy import event, inspect, orm
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from app.core.settings import settings

class CustomSQLAlcemy(SQLAlchemy):
    database_engine = create_engine(settings.sqlalchemy_database_uri, echo=True)

    def create_session(self, options):
        return orm.sessionmaker(bind=self.database_engine, **options)

db = CustomSQLAlcemy()
cache = Cache()
ma = Marshmallow()