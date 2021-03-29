from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost/alembicdb"
db = SQLAlchemy(app)

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
  password = request.form['password']
  name = request.form['name']
  email = request.form['email']

  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
  user = User(name=name, email=email, password_hash=hashed.decode('utf8'))

  db.session.add(user)
  db.session.commit()
  user_response = []

  for user in User.query.all():
    user_response.append(f"id: {user.id}, name: {user.name}, passwordhash: {user.password_hash}")
  return jsonify(user_response), 201