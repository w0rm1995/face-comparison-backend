from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models.user import User, UserSchema
from models.role import Role, RoleSchema
from utils.custom_response import ok, bad_request
from utils.jwt_custom_decorator import admin_required
from utils import db_helper


class RolesResources(Resource):
    def get(self):
        roles = Role.query.all()
        roles = RoleSchema(many=True).dump(roles)
        return ok(roles, 200)

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return bad_request('No input data provided', 400)
        try:
            data = RoleSchema().load(json_data)
            role_in_db = Role.get_role_by_name(data.get('name'))
            if role_in_db:
                return bad_request('Role already exist, please supply another role name', 422)
            roles = Role(data)
            db_helper.insert(roles)
            role_data = RoleSchema().dump(roles)
            return ok(role_data, 200)
        except ValidationError as e:
            return bad_request(e.messages, 422)
        except Exception:
            return bad_request('Something went wrong', 500)


class RoleResources(Resource):
    """
    assign a user to a role
    """

    @admin_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return bad_request('No input data provided', 400)
        try:
            user_in_db = User.get_user_by_id(json_data['user_id'])
            role_in_db = Role.get_role_by_id(json_data['role_id'])
            if not user_in_db:
                return bad_request('User not found', 422)
            if not role_in_db:
                return bad_request('Role not found', 422)
            role_in_db.users.append(user_in_db)
            db_helper.only_save()
            return ok('ok', 200)
        except Exception as e:
            return bad_request(str(e), 500)
