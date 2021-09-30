from app.orm.repository.base import BaseRepository
from app.orm.models.erp.goods.product import Product


class ProductRepository(BaseRepository):
    __model__ = Product