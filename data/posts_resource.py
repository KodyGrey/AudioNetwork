from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from flask_cors import cross_origin
from .posts import Posts
from .users import Users
from .db_session import create_session
from .parsers import posts_parser


def abort_if_post_is_not_found(post_id):
    sess = create_session()
    post = sess.query(Posts).get(post_id)
    if not post:
        abort(404, message=f'Post {post_id} is not found')


def abort_if_user_is_not_found_or_wrong_password(login, password):
    sess = create_session()
    user = sess.query(Users).filter(Users.login == login).first()
    if not user:
        abort(404, message=f'User {login} is not found')
    if not (user.check_password(password)):
        abort(403, message=f'Wrong password')


class PostsResource(Resource):

    def get(self, id):
        abort_if_post_is_not_found(id)
        sess = create_session()
        post = sess.query(Posts).get(id)
        return jsonify({
            'posts': [post.to_dict()]
        })


class PostsListResource(Resource):

    def get(self):
        sess = create_session()
        posts = sess.query(Posts).all()
        return jsonify({
            'posts': [el.to_dict() for el in posts]
        })

    def post(self):
        sess = create_session()
        parser = posts_parser.parse_args()
        abort_if_user_is_not_found_or_wrong_password(parser['login'], parser['password'])
        post = Posts()
        post.title = parser['title']
        user = sess.query(Users).filter(Users.login == parser['login']).first()
        post.author = user.id
        post.creation_date = datetime.now()
        posts = sess.query(Posts).all()
        try:
            num = posts[-1].audio_file
        except IndexError:
            num = 0
        num = str(int(num) + 1)
        with open('C:\\Projects\\AudioNetwork\\static\\audio\\mp3\\' + num + '.mp3',
                  'wb') as f:
            exec(f'f.write({parser["file"]})')
        post.audio_file = num
        sess.add(post)
        sess.commit()
        return jsonify({'success': 'OK'})


class PostsListResourceForInfiniteScrolling(Resource):

    @cross_origin()
    def get(self, start, amount):
        sess = create_session()
        if start == 0 and amount == 0:
            return jsonify({'id': max([post.id for post in sess.query(Posts).all()])})
        abort_if_post_is_not_found(start)
        if start - amount < 1:
            amount = start
        posts = sess.query(Posts).filter(Posts.id <= start, Posts.id > start - amount)
        return jsonify({
            'posts': [el.to_dict() for el in posts[::-1]]
        })
