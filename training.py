from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost/alembicdb"
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  email = db.Column(db.String)

  def __repr__(self):
    return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"



@app.route('/create_user')
def create_user():
  user = User(name='ed', email='Ed Jones')
  db.session.add(user)
  db.session.commit()

  return jsonify([f"id: {user.id}, name: {user.name}" for user in User.query.all()])