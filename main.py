from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from user import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
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


@app.route('/<title>')
@app.route('/index/<title>')
def hello(title):
    return render_template('base.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        form = LoginForm()
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
