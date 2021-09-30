from app.orm.repository.base import BaseRepository
from app.orm.models.erp.goods.unit import Unit


class UnitRepository(BaseRepository):
    __model__ = Unit