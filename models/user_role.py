from app import db

users_roles = db.Table('users_roles', db.Column('user_id', db.BigInteger(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.BigInteger(), db.ForeignKey('roles.id')))
