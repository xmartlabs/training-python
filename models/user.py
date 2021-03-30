from database import db

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  email = db.Column(db.String)
  password_hash = db.Column(db.String)

  def __repr__(self):
    return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"