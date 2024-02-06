import flask
from flask import render_template, url_for
from flask_login import login_required, current_user
from flask_restful import abort
from werkzeug.utils import redirect

from data import db_session
from data.models import Basket, Product

blueprint = flask.Blueprint('basket-app', __name__, template_folder='templates')


@blueprint.before_request
def before():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))


@blueprint.route('/basket')
@login_required
def basket():
    title = 'корзина'
    db_sess = db_session.create_session()
    basket_items = db_sess.query(Basket).filter(Basket.user_id == current_user.id).all()

    content = {
        'title': title,
        'basket_items': basket_items,
    }

    return render_template('basketapp/basket.html', **content)


@blueprint.route('/basket/add/<int:product>')
@login_required
def basket_add(product):
    db_sess = db_session.create_session()
    product_db = db_sess.query(Product).filter(Product.id_ == product, Product.quantity > 0).first()
    if not product_db:
        abort(404)
    old_basket_item = db_sess.query(Basket).filter(Basket.product_id == product,
                                                   Basket.user_id == current_user.id).first()
    if old_basket_item:
        old_basket_item.quantity += 1
    else:
        new_basket_item = Basket(user_id=current_user.id, product_id=product)
        db_sess.add(new_basket_item)
    product_db.quantity -= 1
    db_sess.commit()

    return redirect(url_for('basket-app.basket'))


@blueprint.route('/basket/remove/<int:product>')
@login_required
def basket_remove(product):
    db_sess = db_session.create_session()
    basket_record = db_sess.query(Basket).filter(Basket.id_ == product, Basket.user_id == current_user.id).first()
    if not basket_record:
        abort(404)
    product_db = db_sess.query(Product).get(basket_record.product_id)
    product_db.quantity += basket_record.quantity
    db_sess.delete(basket_record)
    db_sess.commit()

    return redirect(url_for('basket-app.basket'))
