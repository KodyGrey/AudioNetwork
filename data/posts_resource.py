from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from flask_cors import cross_origin
from .posts import Posts
from .db_session import create_session


def abort_if_post_is_not_found(post_id):
    sess = create_session()
    post = sess.query(Posts).get(post_id)
    if not post:
        abort(404, message=f'Post {post_id} is not found')


class PostsResource(Resource):
    pass


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
            'posts': [el.to_dict() for el in posts]
        })



