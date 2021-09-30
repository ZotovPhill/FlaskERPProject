from app.orm.schemas.base import BaseSchema
from app.orm.models import Product


class ProductSchema(BaseSchema):
    __envelope__ = {
        'single': 'product',
        'many': 'products',
    }
        
    class Meta(BaseSchema.Meta):
        model = Product
        include_relationships = True