from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
import secrets
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost/alembicdb"
db = SQLAlchemy(app)

# jwt_secret = secrets.token_hex()
jwt_secret = '2e717c22b824ea4220c8dc343289cede7c752cb54a4c4bbf2b666a804f878e0e'

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  email = db.Column(db.String)
  password_hash = db.Column(db.String)

  def __repr__(self):
    return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


@app.route('/users', methods=['POST'])
def create_user():
  try:  
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(name=name, email=email, password_hash=hashed.decode('utf8'))

    db.session.add(user)
    db.session.commit()
    user_response = []

    return jsonify({'id': user.id, 'name': user.name}), 201
  except IntegrityError:
    return jsonify('user cannot be created'), 400


@app.route('/login', methods=['POST'])
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
    encoded_jwt = jwt.encode({"user_email": user.email}, jwt_secret, algorithm="HS256")
    return jsonify(encoded_jwt)
  else:
    return jsonify('wrong credentials'), 401

@app.route('/me', methods=['GET'])
def me():  
  token = request.headers['Authorization']
  payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
  
  stmt = select(User).where(User.email == payload['user_email'])
  user = db.session.execute(stmt).fetchone()
   
  if (user == None):
    return jsonify('unauthorized'), 401
  else:
    user = user[0]
  
  return jsonify({'id': user.id, 'name': user.name})

@app.route('/users', methods=['GET'])
def list_users():  
  user_response = []

  for user in User.query.all():
    user_response.append(f"id: {user.id}, name: {user.name}, passwordhash: {user.password_hash}")
  return jsonify(user_response)