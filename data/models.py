from datetime import datetime
import sqlalchemy
from flask import url_for
from flask_login import UserMixin, current_user
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm

from . import db_session
from .db_session import SqlAlchemyBase

ROLE_USER = 0
ROLE_ADMIN = 1


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    role = sqlalchemy.Column(sqlalchemy.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN


class Map(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'map'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.Integer, default=3)


class Cell(SqlAlchemyBase):
    __tablename__ = 'cell'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    map_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("map.id"))
    coord = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_ship = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    prize_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("product.id"))
    is_view = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class UserMap(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user_map'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    map_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("map.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    shots = sqlalchemy.Column(sqlalchemy.Integer)


class CellUser(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cell_user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    cell_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cell.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    att = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)


class Basket(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'basket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("product.id_"))
    # quantity = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    # add_datetime = с

    #product = orm.relation('Product')

    # @property
    # def get_product_cost(self):
    #     return self.product.price_ * self.quantity

    # def get_total_quantity(self):
    #     db_sess = db_session.create_session()
    #     _items = db_sess.query(Basket).filter(Basket.user_id == current_user.id).all()
    #     _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
    #     return _totalquantity

    # def get_total_cost(self):
    #     db_sess = db_session.create_session()
    #     _items = db_sess.query(Basket).filter(Basket.user_id == current_user.id).all()
    #     _totalcost = sum(map(lambda x: x.get_product_cost, _items))
    #     return f'{_totalcost:.2f}'


# class ProductCategory(SqlAlchemyBase):
#     __tablename__ = 'product_category'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
#     description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
#     is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
#
#     @staticmethod
#     def get_product():
#         db_sess = db_session.create_session()
#         _items = db_sess.query(ProductCategory).filter(ProductCategory.is_active is True).all()
#         for item in _items:
#             pass
#         return _items


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'product'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, unique=True)
    # short_desc = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    # price_ = sqlalchemy.Column(sqlalchemy.DECIMAL, nullable=True)
    # quantity = sqlalchemy.Column(sqlalchemy.SmallInteger, default=1)
    # is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    # category_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                                 sqlalchemy.ForeignKey("product_category.id_"))
    #
    # category = orm.relation('ProductCategory')

    @property
    def get_image(self):
        return f'/static/media/{self.image}'

    @property
    def price(self):
        return f'{self.price_:.2f}'
