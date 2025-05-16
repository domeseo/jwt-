"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/register', methods=['POST'])
def user_registration():
    response_body = {}
    new_user = request.json
    if not new_user:
        response_body['message'] = "Insert email and password"
    
    new_user['email'] = new_user['email'].lower()
    user_a_register = User(
        email = new_user['email'],
        password=new_user['password'],
        is_active = True
    )

    db.session.add(user_a_register)
    db.session.commit()
    response_body['message'] = "Welcome, User Registered"
    return response_body, 201


@api.route('/login', methods=['POST'])
def user_login():
    response_body = {

    }

    user = request.json
    if not user:
        response_body['message'] = "Insert your email and password"
    
    user['email'] = user['email'].lower()

    db_user = User.query.filter_by(email=user['email'], password=user['password']).first()

    if not db_user:
        response_body['message'] = "Wrong password or email"
        return response_body, 404
    response_body['message'] = "Login successful"
    access_toker = create_access_token(identify=str(db_user.id)) 
    response_body['token'] = access_token
    return response_body, 200


@api.route('private', methods=['POST'])
@jwt_required()
def handle_private():
    response_body = {}
    current_user = get_jwt_identity()
    user = User.query.filter_by(int(current_user))

    if not user:
        response_body['message'] = "User not found"
        return response_body, 404
    
    response_body['message'] = "User found"
    response_body['userInfo'] = user.serialize()
    return response_body, 200
    
