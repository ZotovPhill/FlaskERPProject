from app.orm.repository.base import BaseRepository
from app.orm.models.erp.goods.product import Product


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.model = Unit
