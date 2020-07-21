from datetime import datetime
from marshmallow import fields, validate
# from flask_bcrypt import generate_password_hash, check_password_hash

from app import db, ma, bcrypt
from models.user_role import users_roles
from models.role import RoleSchema


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(230), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship("Role", secondary=users_roles,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, data):
        self.id
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.image = data.get('image')
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    # def update(self, data):
    #     for key, item in data.items():
    #         setattr(self, key, item)
    #     self.modified_at = datetime.utcnow()
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(
            password, rounds=10).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()

    # @staticmethod
    # def save():
    #     db.session.commit()

    @staticmethod
    def get_user_by_email(value):
        return User.query.filter_by(email=value).first()

    @staticmethod
    def get_user_by_id(value):
        return User.query.filter_by(id=value).first()

    @staticmethod
    def get_user_by_image(value):
        return User.query.filter_by(image=value).first()

    def __repr__(self):
        return '<User {}>'.format(self.password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
    id = ma.auto_field()
    name = fields.Str(required=True, validate=validate.Length(min=3, max=230))
    email = fields.Email(
        required=True, validate=validate.Length(min=10, max=120))
    password = fields.Str(required=True)
    image = fields.Str(required=False)

    roles = fields.Nested(RoleSchema, many=True, only=('id', 'name'))
