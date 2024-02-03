from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_login import LoginManager
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import sqlalchemy
from flask import request


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

# login_manager = LoginManager()
# login_manager.init_app(app)

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')





@app.route('/')
def index():
    form = RegistrationForm()
    return render_template('LoginForm_page.html',form=form)



@app.route('/adminpage')
def game():
    return render_template('admin_main_page.html')
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')