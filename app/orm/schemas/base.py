from flask_sqlalchemy import Pagination
from marshmallow import pre_load, post_dump, pre_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.core.extensions import ma


class BaseSchema(SQLAlchemyAutoSchema):
    # Custom options
    __envelope__ = {
        'single': None,
        'many': None
    }
    pagination = None
    
    def get_envelope_key(self, many):
        """Helper to get the envelope key."""
        key = self.__envelope__['many'] if many else self.__envelope__['single']
        assert key is not None, "Envelope key undefined"
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many):
        key = self.get_envelope_key(many)
        return data[key]

    @pre_dump(pass_many=True)
    def get_pagination_info(self, data, many):
        if many and isinstance(data, Pagination):
            self.pagination = {
                'offset': (data.page - 1) * data.per_page,
                'limit': data.per_page,
                'has_next': data.has_next,
                'has_prev': data.has_prev,
                'total': data.total
            }
            """Need to be inside list extraction session"""
            return data.items
        return data
        
    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        key = self.get_envelope_key(many)
        result = {key: data} 
        if self.pagination:
            result.update({"pagination": self.pagination})
        return result
