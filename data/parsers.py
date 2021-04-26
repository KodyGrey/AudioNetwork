from flask_restful import reqparse
import werkzeug

posts_parser = reqparse.RequestParser()
posts_parser.add_argument('login', required=True)
posts_parser.add_argument('password', required=True)
posts_parser.add_argument('title', required=True)
posts_parser.add_argument('file', required=True)
