from datetime import datetime

from app import db


def insert(obj):
    db.session.add(obj)
    db.session.commit()


def update(obj, data):
    for key, item in data.items():
        setattr(obj, key, item)
    obj.updated_at = datetime.utcnow()
    db.session.commit()


def delete(obj):
    db.session.delete(obj)
    db.session.commit()


def only_save():
    db.session.commit()
