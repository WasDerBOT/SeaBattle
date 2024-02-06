import os

import flask
from PIL import Image
from flask import render_template, flash, url_for, request
from flask_login import current_user
from flask_restful import abort
from werkzeug.utils import secure_filename, redirect

from adminapp.forms import CategoryForm, ProductForm
from data import db_session
from data.models import ProductCategory, ROLE_ADMIN, Product, User

blueprint = flask.Blueprint('admin-app', __name__, template_folder='templates')


def _resize(file_path, max_size=300, max_height=False):
    img = Image.open(file_path)
    width, height = img.size
    _max_size = max(width, height)
    if max_height:
        img = img.resize(
            (round(width / max_size),
             round(height / max_size)),
            Image.ANTIALIAS
        )
    elif _max_size > max_size:
        img = img.resize(
            (round(width / _max_size * max_size),
            round(height / _max_size * max_size)),
            Image.ANTIALIAS
        )
        img.save(file_path)

@blueprint.before_request
def before():
    if current_user.role != ROLE_ADMIN:
        abort(403)


@blueprint.route('/admin/categories')
def admin_categories():
    title = 'админка/категории'
    db_sess = db_session.create_session()
    categories_list = db_sess.query(ProductCategory).all()
    content = {
        'title': title,
        'objects': categories_list
    }
    return render_template('adminapp/categories.html', **content)


@blueprint.route('/admin/category/create', methods=['GET', 'POST'])
def admin_category_create():
    title = 'Админка/Продукты/Создание'
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        _category = ProductCategory(name=form.name.data, description=form.description.data)
        db_sess.add(_category)
        db_sess.commit()
        flash('Категория успешно добавлена')
        return redirect(url_for('admin-app.admin_categories'))
    return render_template('adminapp/_form.html', title=title, form=form)


@blueprint.route('/admin/category/<int:id_>/update', methods=['GET', 'POST'])
def admin_category_update(id_):
    title = 'Админка/Продукты/Создание'
    db_sess = db_session.create_session()
    _category = db_sess.query(ProductCategory).get(id_)
    if not _category:
        abort(404)
    form = CategoryForm(name=_category.name, description=_category.description)
    if form.validate_on_submit():
        _category.name = form.name.data
        _category.description = form.description.data
        db_sess.commit()
        flash('Вы успешно зарегистрированы')
        return redirect(url_for('admin-app.admin_categories'))
    return render_template('adminapp/_form.html', title=title, form=form)


@blueprint.route('/admin/category/<int:id_>/delete', methods=['GET', 'POST'])
def admin_category_delete(id_):
    title = 'Админка/Продукты/Создание'
    db_sess = db_session.create_session()
    _category = db_sess.query(ProductCategory).get(id_)
    if not _category:
        abort(404)
    _category.is_active = False
    db_sess.commit()
    return redirect(url_for('admin-app.admin_categories'))


@blueprint.route('/admin/category/<int:id>/products')
def admin_products(id):
    title = 'админка/категории'
    db_sess = db_session.create_session()
    _category = db_sess.query(ProductCategory).get(id)
    if not _category:
        abort(404)
    _products = db_sess.query(Product).filter(Product.category_id == id).all()
    content = {
        'title': title,
        'category': _category,
        'objects': _products
    }
    return render_template('adminapp/products.html', **content)


@blueprint.route('/admin/product/create/category-<int:cat_id>', methods=['GET', 'POST'])
def product_create(cat_id):
    title = 'Админка/Продукты/Создание'
    form = ProductForm()
    if form.validate_on_submit():
        if form.image.data:
            image = form.image.data
            f_name = secure_filename(image.filename)
            i = 0
            while os.path.exists(os.path.join('static', 'media', f_name)):
                f_name = f'{i}-{f_name}'
                i += 1
            path_file = os.path.join('static', 'media', f_name)
            image.save(path_file)
            _resize(path_file)
        _product = Product(
            name=form.name.data,
            image=f_name if form.image.data else None,
            short_desc=form.short_desc.data,
            description=form.description.data,
            price_=form.price.data,
            quantity=form.quantity.data,
            category_id=cat_id
        )
        db_sess = db_session.create_session()
        db_sess.add(_product)
        db_sess.commit()

        flash('Товар успешно добавлен')
        return redirect(url_for('admin-app.product_create', cat_id=_product.category_id))
    return render_template('adminapp/_form.html', title=title, form=form)


@blueprint.route('/admin/product/<int:id>/edit/', methods=['GET', 'POST'])
def product_edit(id):
    title = 'админка/продукты/редактирование'
    db_sess = db_session.create_session()
    _product = db_sess.query(Product).get(id)
    if not _product:
        abort(404)
    form = ProductForm(name=_product.name, short_desc=_product.short_desc, description=_product.description,
                       price=_product.price_, quantity=_product.quantity, image=_product.image)
    if form.validate_on_submit():
        if form.image.data:
            image = form.image.data
            f_name = secure_filename(image.filename)
            i = 0
            while os.path.exists(os.path.join('static', 'media', f_name)):
                f_name = f'{i}-{f_name}'
                i += 1
            path_file = os.path.join('static', 'media', f_name)
            image.save(path_file)
            _resize(path_file)

        _product.name = form.name.data
        _product.image = f_name if form.image.data else _product.image
        _product.short_desc = form.short_desc.data
        _product.description = form.description.data
        _product.price_ = form.price.data
        _product.quantity = form.quantity.data
        db_sess.commit()
        flash('Товар успешно добавлен')
        return redirect(url_for('admin-app.product_create', cat_id=_product.category_id))
    return render_template('adminapp/_form.html', title=title, form=form)


@blueprint.route('/admin/product/<int:id>')
def product_detail(id):
    db_sess = db_session.create_session()
    _product = db_sess.query(Product).get(id)
    if not _product:
        abort(404)
    return render_template('detail_product.html', object=_product)


@blueprint.route('/admin/product/<int:id>/delete')
def product_delete(id):
    db_sess = db_session.create_session()
    _product = db_sess.query(Product).filter(Product.id_ == id).first()
    cat_id = _product.category_id
    if not _product:
        abort(404)
    _product.is_active = not _product.is_active
    db_sess.commit()
    flash('Товар успешно добавлен в архив')
    return redirect(url_for('admin-app.admin_products', id=_product.category_id))


@blueprint.route('/admin/users')
def admin_users():
    title = 'информация'
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    context = {
        'users': users,
        'title': title,
    }

    return render_template('adminapp/users.html', **context)


@blueprint.route('/admin/users/<int:id>/set-admin')
def admin_user_set_admin(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if not user:
        return abort(404)
    user.role = not user.role
    db_sess.commit()
    return redirect(url_for('admin-app.admin_users'))

