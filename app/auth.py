from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app, bcrypt,db
from app.models import User

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get['username']
    email = data.get['email']
    password = data.get['password']

    if not email or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Username already exist"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200