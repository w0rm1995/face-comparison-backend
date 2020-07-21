from datetime import timedelta
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims, exceptions
from utils.jwt_custom_decorator import admin_required

from app import jwt
from models.user import User, UserSchema
from utils.custom_response import ok, bad_request


@jwt.user_claims_loader
def add_claims_to_access_token(users):
    if users['roles'][0]['name'] == 'admin':
        return {'roles': users['roles'][0]['name']}
    elif users['roles'][0]['name'] == 'user':
        return {'roles': users['roles'][0]['name']}
    else:
        return {'roles': 'unknown'}


class AuthResources(Resource):
    @admin_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            tes = get_jwt_claims()
            return ok(current_user, 200)
        except Exception:
            return bad_request('Something went wrong', 500)

    def post(self):
        try:
            json_data = request.get_json(force=True)
            if not json_data:
                return bad_request('No input data provided', 400)
            if 'email' not in request.json:
                return bad_request('email not provided', 422)
            if 'password' not in request.json:
                return bad_request('password not provided', 422)
            if json_data['email'] == '' or json_data['email'] == None:
                return bad_request('email can\'t be empty or null', 422)
            if json_data['password'] == '' or json_data['password'] == None:
                return bad_request('password can\'t be empty or null', 422)
            user_in_db = User.get_user_by_email(json_data['email'])
            if user_in_db:
                authorized = user_in_db.check_password(json_data['password'])
                if authorized:
                    users = UserSchema(
                        only=('id', 'name', 'roles')).dump(user_in_db)
                    expires = timedelta(days=1)
                    token = create_access_token(
                        identity=users, expires_delta=expires)
                    return ok({'id': users['id'], 'name': users['name'], 'token': token}, 200)
                else:
                    return bad_request('wrong password', 422)
            else:
                return bad_request('user not found!', 404)
        except Exception as e:
            return bad_request(str(e), 500)
