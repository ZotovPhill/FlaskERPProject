from app.core.constants import DEFAULT_LIMIT
from flask.blueprints import Blueprint
from werkzeug.exceptions import HTTPException
from app.orm.schemas.goods import ProductSchema
from app.orm.repository import product_repository
from app.orm.repository.base import cached_session_scope
from flask import jsonify, request

goods_page = Blueprint('goods_page', __name__, url_prefix="/goods")

def session_decorator(f):
    def wrapped(*args, **kwargs):
        session = cached_session_scope()
        return f(session, *args, **kwargs)
    return wrapped

@goods_page.route("")
@session_decorator
def goods_list(session):
    try:
        limit = request.args.get("limit", default=DEFAULT_LIMIT, type=int)
        offset = request.args.get("offset", default=0, type=int)
    except Exception:
        raise HTTPException
    goods = product_repository.list_paginate(session, limit, offset)
    schema = ProductSchema().dump(goods, many=True)
    return jsonify(schema)


@goods_page.route("/<uuid:product_id>")
@session_decorator
def single_product(session, product_id: str):
    product = product_repository.find(session, product_id)
    return jsonify(ProductSchema().dump(product))