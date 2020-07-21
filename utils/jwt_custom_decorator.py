from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, exceptions
from jwt import exceptions as jwt_exception
from utils.custom_response import bad_request


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if claims['roles'] != 'admin':
                return bad_request('Admins only', 403)
            else:
                return fn(*args, **kwargs)
        except jwt_exception.DecodeError as e:
            return bad_request(str(e), 401)
        # except jwt_exception.DecodeError as e:
        #     return bad_request(str(e), 401)
        except jwt_exception.PyJWTError as e:
            return bad_request(str(e), 401)
        except exceptions.JWTExtendedException as e:
            return bad_request(str(e), 403)
    return wrapper
