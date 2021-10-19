from app.orm.repository.base import BaseRepository
from app.orm.models.erp.goods.unit import Unit


class UnitRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = Unit
