from flask import jsonify
from flask_cors import cross_origin
from flask_restful import abort, Resource

from .db_session import create_session
from .users import Users


def abort_if_user_is_not_found(id):
    sess = create_session()
    user = sess.query(Users).get(id)
    if not user:
        abort(404, message=f'User {id} is not found')


class UsersResource(Resource):

    @cross_origin()
    def get(self, id):
        abort_if_user_is_not_found(id)
        sess = create_session()
        user = sess.query(Users).get(id)
        return jsonify({
            'users': [
                {'id': user.id, "login": user.login, "creation_date": user.creation_date}
            ]
        })


class UsersListResources(Resource):

    @cross_origin()
    def get(self):
        sess = create_session()
        users = sess.query(Users).all()
        json = []
        for user in users:
            json.append({
                'id': user.id,
                'login': user.login,
                'creation_date': user.creation_date
            })
        return jsonify({
            json
        })
