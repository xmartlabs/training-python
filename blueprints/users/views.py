from flask import Blueprint, request, current_app, jsonify, g
import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models.user import User
from database import db
import bcrypt
from functools import wraps

users = Blueprint('users', __name__)
 
def skip_login(func):
  func.is_public = True
  return func

def jwt_secret():
  return current_app.config['JWT_SECRET']

@users.before_request
def set_current_user():
  token = request.headers.get('Authorization', None)

  if token is None:
    g.current_user = None
    return

  payload = jwt.decode(token, jwt_secret(), algorithms=["HS256"])
  
  stmt = select(User).where(User.email == payload['user_email'])
  user = db.session.execute(stmt).first()
  
  if user is not None:
    g.current_user = user[0]
  else:
    g.current_user = None
  

@users.before_request
def require_login():
    login_valid = g.current_user is not None

    if (request.endpoint and 
        'static' not in request.endpoint and 
        not login_valid and 
        not getattr(current_app.view_functions[request.endpoint], 'is_public', False) ) :
        return 'unauthorized', 401

@users.route('/me', methods=['GET'])
def me():  
  return jsonify({'id': g.current_user.id, 'name': g.current_user.name})

@users.route('/login', methods=['POST'])
@skip_login
def login():  
  password = request.form.get('password')
  email = request.form.get('email')
  stmt = select(User).where(User.email == email)
  user = db.session.execute(stmt).first()
  
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

  for user in User.query.yield_per(10):
    user_response.append({"id": user.id, 'name': user.name, 'email': user.email})
  return jsonify(user_response)

@users.route('/users', methods=['POST'])
@skip_login
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
