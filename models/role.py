from datetime import datetime
from marshmallow import fields, validate
from app import db, ma


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, data):
        self.id,
        self.name = data.get('name')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_role_by_name(value):
        return Role.query.filter_by(name=value).first()

    @staticmethod
    def get_role_by_id(value):
        return Role.query.get(value)


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        ordered = True
    id = ma.auto_field()
    name = fields.Str(
        required=True, validate=validate.Length(min=3, max=120))
    users = fields.Nested("UserSchema", only=("id", "name"), many=True)
