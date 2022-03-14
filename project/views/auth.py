from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db
from project.tools.security import login_user, refresh_token

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        """User authentication"""
        req_json = request.json
        if not req_json:
            abort(400)
        try:
            user = UsersService(db.session).get_user_by_email(email=req_json.get('email'))
            tokens = login_user(req_json, user)
            return tokens, 200
        except ItemNotFound:
            abort(401, "Authorization error")

    def put(self):
        """Refresh user's tokens"""
        req_json = request.json
        if not req_json:
            abort(400)
        try:
            tokens = refresh_token(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, "Authorization error")


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        """Create new user"""
        req_json = request.json
        if not req_json:
            abort(400)
        return UsersService(db.session).create(req_json)