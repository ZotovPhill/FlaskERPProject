from app.orm.repository.base import BaseRepository
from app.orm.models.erp.goods.category import Category


class CategoryRepository(BaseRepository):
    __model__ = Category