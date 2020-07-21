import os
import math
import warnings
import numpy
from PIL import Image, ImageDraw
from flask import request
from flask_restful import Resource, reqparse, url_for
import face_recognition
from models.user import User, UserSchema
from marshmallow import ValidationError
from werkzeug import datastructures
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.custom_response import ok, bad_request
from utils.jwt_custom_decorator import admin_required
from utils.utils import allowed_file
from config import APP_STATIC
import concurrent.futures

parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=datastructures.FileStorage, location='files')


def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        ranges = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (ranges * 2.0)
        return linear_val
    else:
        ranges = face_match_threshold
        linear_val = 1.0 - (face_distance / (ranges * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


class CompareImageResources(Resource):
    @jwt_required
    def post(self):
        try:
            user_identity = get_jwt_identity()
            users = User.get_user_by_id(user_identity['id'])
            data_parser = parser.parse_args()
            if not users:
                return bad_request('User not found!', 422)
            if data_parser['file'] == "":
                return bad_request('File not found!', 422)
            photo = data_parser['file']
            if photo and allowed_file(photo.filename):
                user_photo = os.path.join(APP_STATIC, users.image)
                known_face = face_recognition.load_image_file(user_photo)
                known_face_encoding = face_recognition.face_encodings(known_face)[
                    0]
                unknown_face = face_recognition.load_image_file(photo)
                factor = 0
                if unknown_face.shape[0] > 1028 or unknown_face.shape[1] > 1028:
                    if unknown_face.shape[0] > unknown_face.shape[1]:
                        factor = 1028 / unknown_face.shape[0]
                    else:
                        factor = 1028 / unknown_face.shape[1]
                    resized_image = Image.fromarray(
                        unknown_face).resize((int(unknown_face.shape[1] * factor), int(unknown_face.shape[0] * factor)))
                    unknown_face = numpy.array(resized_image)
                unknown_face_encoding = face_recognition.face_encodings(unknown_face)[
                    0]
                distance = face_recognition.face_distance(
                    [known_face_encoding], unknown_face_encoding)
                result = face_recognition.compare_faces(
                    [known_face_encoding], unknown_face_encoding)
                if result[0]:
                    return ok({'result': 'Verified', 'user': users.name, 'tingkat kemiripan': str(int(round((face_distance_to_conf(distance)[0]), 2) * 100)) + '%'}, 200)
                else:
                    return ok({'result': 'Not verified', 'tingkat kemiripan': str(int(round((face_distance_to_conf(distance)[0]), 2) * 100)) + '%'}, 200)
        except Exception as e:
            return bad_request(str(e), 400)


class CompareImagesResources(Resource):
    """
    Search user by image
    """
    @admin_required
    def post(self):
        try:
            data_parser = parser.parse_args()
            if data_parser['file'] == "":
                return bad_request('File not found!', 422)
            photo = data_parser['file']
            if photo and allowed_file(photo.filename):
                unknown_face = face_recognition.load_image_file(photo)
                factor = 0
                if unknown_face.shape[0] > 1028 or unknown_face.shape[1] > 1028:
                    if unknown_face.shape[0] > unknown_face.shape[1]:
                        factor = 1028 / unknown_face.shape[0]
                    else:
                        factor = 1028 / unknown_face.shape[1]
                    resized_image = Image.fromarray(
                        unknown_face).resize((int(unknown_face.shape[1] * factor), int(unknown_face.shape[0] * factor)))
                    unknown_face = numpy.array(resized_image)
                unknown_face_encoding = face_recognition.face_encodings(unknown_face)[
                    0]
                for filename in os.listdir(APP_STATIC):
                    user_photo = os.path.join(APP_STATIC, filename)
                    known_face = face_recognition.load_image_file(user_photo)
                    if known_face.shape[0] > 1028 or known_face.shape[1] > 1028:
                        if known_face.shape[0] > known_face.shape[1]:
                            factor = 1028 / known_face.shape[0]
                        else:
                            factor = 1028 / known_face.shape[1]
                        resized_image = Image.fromarray(
                            known_face).resize((int(known_face.shape[1] * factor), int(known_face.shape[0] * factor)))
                        known_face = numpy.array(resized_image)
                    known_face_encoding = face_recognition.face_encodings(known_face)[
                        0]
                    result = face_recognition.compare_faces(
                        [known_face_encoding], unknown_face_encoding)

                    if result[0]:
                        users = User.get_user_by_image(filename)
                        photo_url = request.url_root + url_for(
                            'static', filename="image/" + users.image)
                        distance = face_recognition.face_distance(
                            [known_face_encoding], unknown_face_encoding)
                        return ok({'result': 'user ditemukan', 'user': users.name, 'image': photo_url, 'tingkat kemiripan': str(int(round((face_distance_to_conf(distance)[0]), 2) * 100)) + '%'}, 200)
                        break
                return ok({'result': 'user tidak ditemukan'}, 200)
        except Exception as e:
            return bad_request(str(e), 400)
