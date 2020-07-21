from flask import jsonify, make_response


def ok(data, status_code):
    return {
        'status': 'ok',
        'data': data
    }, status_code

    # return make_response(jsonify(res)), status_code


def bad_request(message, status_code):
    return {
        'status': 'error',
        'message': message
    }, status_code

    # return make_response(jsonify(res)), status_code
