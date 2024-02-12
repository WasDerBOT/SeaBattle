from flask import jsonify
from flask_login import current_user
from flask_restful import Resource, abort

from data import db_session
from data.models import Basket, Product


def get_objcet_or_404():
    if not current_user.is_authenticated:
        abort(401, message=f"Требуется авторизация")
    session = db_session.create_session()
    products = session.query(Basket).filter(Basket.user_id == current_user.id).all()
    if not products:
        abort(404, message=f'Ваша корзина пуста')
    return products


class BascetResource(Resource):
    def get(self):
        basket = get_objcet_or_404()
        return jsonify({'products': [product.to_dict(
            only=('product.id_', 'product.name', 'quantity',)) for product in basket]})

    def delete(self):
        basket = get_objcet_or_404()
        session = db_session.create_session()
        session.delete(basket)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductResource(Resource):
    def get(self, category=None):
        session = db_session.create_session()
        products = session.query(Product).filter(Product.is_active == True)
        if category:
            products = products.filter(Product.category_id == category).all()
        return jsonify({'products': [
            product.to_dict(only=('id_', 'name', 'get_image', 'short_desc', 'description', 'price_', 'quantity'))
            for product in products]})


