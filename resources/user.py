import os

from flask import request
from flask_restful import Resource, reqparse, url_for
from models.user import User, UserSchema
from marshmallow import ValidationError
from werkzeug import datastructures
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from uuid import uuid4
from datetime import datetime
from config import APP_ROOT, APP_STATIC
from utils.custom_response import ok, bad_request
from utils.jwt_custom_decorator import admin_required
from utils.utils import allowed_file, get_file_extension
from utils import db_helper


parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=datastructures.FileStorage, location='files')


class UsersResources(Resource):
    def get(self):
        users_schema = UserSchema(many=True, exclude=['password'])
        users = User.query.all()
        users = users_schema.dump(users)
        return ok(users, 200)

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return bad_request('No input data provided', 400)
        try:
            data = UserSchema().load(json_data)
            user_in_db = User.get_user_by_email(data.get('email'))
            if user_in_db:
                return bad_request('User already exist, please supply another email address', 422)
            users = User(data)
            db_helper.insert(users)
            ser_data = UserSchema(exclude=['password']).dump(users)
            return ok(ser_data, 201)
        except ValidationError as e:
            return bad_request(e.messages, 422)
        except Exception:
            return bad_request('Something went wrong', 500)


class UserResources(Resource):
    def get(self, user_id):
        user_schema = UserSchema()
        users = User.query.get(user_id)
        if not users:
            return {'status': 'error', 'data': 'not found'}, 404
        print(users.image)
        users = user_schema.dump(users)
        return {'status': 'ok', 'data': users}, 200

    def put(self, user_id):
        try:
            req_data = request.get_json(force=True)
            user_in_db = User.get_user_by_id(user_id)
            if not user_in_db:
                return bad_request('User not found!', 422)
            data = UserSchema().load(req_data, partial=True)
            db_helper.update(user_in_db, data)
            data = UserSchema(exclude=['password']).dump(user_in_db)
            return ok(data, 200)
        except ValidationError as e:
            return bad_request(e.messages, 422)
        except Exception as e:
            print(e)
            return bad_request('Something went wrong', 500)

    @admin_required
    def delete(self, user_id):
        try:
            user_in_db = User.get_user_by_id(user_id)
            if not user_in_db:
                return bad_request('User not found!', 422)
            if user_in_db.image:
                os.remove(os.path.join(APP_STATIC, user_in_db.image))
            db_helper.delete(user_in_db)
            return ok('user deleted', 200)
        except Exception as e:
            return bad_request('Something went wrong', 500)


class UserImageResources(Resource):
    @admin_required
    def patch(self, user_id):
        try:
            data_parser = parser.parse_args()
            users = User.get_user_by_id(user_id)
            if not users:
                return bad_request('User not found!', 422)
            if data_parser['file'] == "":
                return bad_request('File not found!', 422)
            photo = data_parser['file']
            if photo and allowed_file(photo.filename):
                secure_name = secure_filename(photo.filename)
                secure_name = get_file_extension(secure_name)
                secure_name = '{}{:-%Y%m%d%H%M%S}.{}'.format(
                    str(uuid4().hex), datetime.now(), secure_name)
                photo.save(os.path.join(APP_STATIC, secure_name))
                if users.image:
                    os.remove(os.path.join(APP_STATIC, users.image))
                # photo_url = request.url_root + url_for(
                #     'static', filename="image/" + secure_name)
                users.image = secure_name
                users.updated_at = datetime.now()
                db_helper.only_save()
                users = UserSchema(exclude=['password']).dump(users)
                return ok(users, 200)
            else:
                return bad_request('File not allowed!', 422)
        except Exception as e:
            return bad_request('Something went wrong', 500)
