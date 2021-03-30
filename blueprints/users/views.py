from flask import Blueprint, request, current_app, jsonify
import jwt
from sqlalchemy import select
from models.user import User
from database import db
import bcrypt

users = Blueprint('users', __name__)

def jwt_secret():
  return current_app.config['JWT_SECRET']

@users.route('/me', methods=['GET'])
def me():  
  token = request.headers['Authorization']
  payload = jwt.decode(token, jwt_secret(), algorithms=["HS256"])
  
  stmt = select(User).where(User.email == payload['user_email'])
  user = db.session.execute(stmt).fetchone()
   
  if (user == None):
    return jsonify('unauthorized'), 401
  else:
    user = user[0]
  
  return jsonify({'id': user.id, 'name': user.name})

@users.route('/login', methods=['POST'])
def login():  
  password = request.form.get('password')
  email = request.form.get('email')
  stmt = select(User).where(User.email == email)
  user = db.session.execute(stmt).fetchone()
  
  if (user == None):
    return jsonify('wrong credentials'), 401
  else:
    user = user[0]

  if (user != None) and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
    encoded_jwt = jwt.encode({"user_email": user.email}, jwt_secret(), algorithm="HS256")
    return jsonify(encoded_jwt)
  else:
    return jsonify('wrong credentials'), 401

@users.route('/users', methods=['GET'])
def list_users():  
  user_response = []

  for user in User.query.all():
    user_response.append({"id": user.id, 'name': user.name, 'email': user.email})
  return jsonify(user_response)

@users.route('/users', methods=['POST'])
def create_user():
  try:  
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(name=name, email=email, password_hash=hashed.decode('utf8'))

    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'name': user.name}), 201
  except IntegrityError:
    return jsonify('user cannot be created'), 400