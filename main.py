import os
import random

from flask import Flask, render_template, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_restful import abort, Api
from werkzeug.utils import redirect, secure_filename
from flask_bootstrap import Bootstrap

from adminapp.views import blueprint as adminapp_blueprint
from api import BascetResource, ProductResource
from basketapp.views import blueprint as basketapp_blueprint
from data import db_session
from data.forms import RegisterForm, LoginForm, ProfileEditForm
from data.models import User, Product, Basket

app = Flask(__name__, static_folder='static')
api = Api(app)
Bootstrap(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'media'
app.register_blueprint(adminapp_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


db_session.global_init("db/data_base.sqlite")




@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Авторизация'
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title = 'Авторизация', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Регистрация'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User(name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash('Вы успешно зарегистрированы')
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileEditForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        user.set_password(form.password.data)
        db_sess.commit()
        flash('Пароль успешно изменен')
        return redirect(url_for('profile_edit'))
    return render_template('profile_edit.html', title='Изменение пароля', form=form)


@app.route('/size-setting', methods=['GET', 'POST'])
@login_required
def size_setting():
    title = 'Size Setting'
    form = SizeSettingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # Save the user's preferred size to the database
        current_user.size = form.size.data
        db_sess.commit()
        flash('Your size has been updated')
        return redirect(url_for('index'))
    return render_template('size_setting.html', title=title, form=form)

@app.errorhandler(403)
def authenticated_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


api.add_resource(BascetResource, '/api/v1/basket')
api.add_resource(ProductResource, '/api/v1/products/category-<int:category>')

if __name__ == '__main__':
    app.run(port=5001)
