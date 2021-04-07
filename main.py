from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Flask, render_template, redirect, request
from data import db_session
from user import User
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    login = StringField('Login / email', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        form = RegisterForm()
        if form.validate_on_submit():
            return redirect('/success')
        return render_template('index.html', title='Регистрация', form=form)
    elif request.method == 'POST':
        try:
            user = User()
            user.email = request.form["login"]
            user.hashed_password = hash(request.form["login"])
            user.name = request.form["name"]
            user.surname = request.form["surname"]
            user.age = int(request.form["age"])
            user.position = request.form["position"]
            user.speciality = request.form["speciality"]
            user.address = request.form["address"]
            database_name = "db/user_list.sqlite"
            db_session.global_init(database_name)
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return render_template('answer.html', title='Регистрация', text='Форма успешно отправлена')
        except Exception:
            return render_template('answer.html', title='Регистрация', text='Произошла ошибка')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
