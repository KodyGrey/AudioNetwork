import datetime
from flask import Flask, url_for, redirect, render_template, request, abort
from data import db_session, posts_resource, users_resources
from data.users import Users
from data.posts import Posts
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, DateField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, login_user, logout_user, \
    current_user
from flask_restful import reqparse, abort, Api, Resource
import os
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ehal_greka_cherez_reku'
db_session.global_init('db/audio_network.sqlite')
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeated_password = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class NewPostForm(FlaskForm):
    title = StringField('Title')
    audio_field = FileField('Audio file', validators=[FileRequired(),
                                                      FileAllowed(['mp3', 'mp3 only!'])])
    submit = SubmitField('Upload')


@login_manager.user_loader
def load_user(user_id):
    sess = db_session.create_session()
    return sess.query(Users).get(user_id)


@app.route('/', methods=[''
                         'GET'])
def index():
    sess = db_session.create_session()
    posts = sess.query(Posts).all()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeated_password.data:
            return render_template('register.html', form=form,
                                   error_message="Passwords don't match",
                                   title='Register')
        sess = db_session.create_session()
        if sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', form=form,
                                   error_message='User with same email already exists',
                                   title='Register')
        if sess.query(Users).filter(Users.login == form.login.data).first():
            return render_template('register.html', form=form,
                                   error_message='User with same login exists',
                                   title='Register')
        user = Users()
        user.email = form.email.data
        user.login = form.login.data
        user.generate_password(form.password.data)
        user.creation_date = datetime.datetime.now()
        sess.add(user)
        sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        user = sess.query(Users).filter(Users.login == form.login.data).first()
        if not user:
            return render_template('register.html', form=form,
                                   error_message='User with this login is not registered',
                                   title='Login')
        if not user.check_password(form.password.data):
            return render_template('register.html', form=form,
                                   error_message='Wrong password', title='Login')
        login_user(user)
        return redirect('/')

    return render_template('register.html', form=form, title='Login')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')


@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        f = form.audio_field.data
        if f.filename[-3:] != 'mp3':
            return render_template('new_post.html', form=form,
                                   error_message='Only mp3 files supports')
        post = Posts()
        post.title = form.title.data
        sess = db_session.create_session()
        posts = sess.query(Posts).all()
        try:
            num = posts[-1].audio_file
        except IndexError:
            num = 0
        num = str(int(num) + 1)
        post.audio_file = num
        post.author = current_user.id
        post.creation_date = datetime.datetime.now()

        f.save(os.path.join('C:\\Projects\\AudioNetwork', 'static', 'audio', 'mp3',
                            num + '.mp3'))

        sess.add(post)
        sess.commit()

    return render_template('new_post.html', form=form)


if __name__ == '__main__':
    api.add_resource(posts_resource.PostsListResourceForInfiniteScrolling,
                     '/api/feed/<int:start>/<int:amount>')
    api.add_resource(posts_resource.PostsResource, '/api/posts/<int:id>')
    api.add_resource(posts_resource.PostsListResource, '/api/posts')
    api.add_resource(users_resources.UsersResource, '/api/users/<int:id>')
    api.add_resource(users_resources.UsersListResources, '/api/users')

    # app.run(port=5000, host='127.0.0.1')
    serve(app, port=5000, host='0.0.0.0')
