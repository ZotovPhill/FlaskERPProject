from app.orm.repository.base import BaseRepository
from app.orm.models.erp.goods.category import Category


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = Unit
