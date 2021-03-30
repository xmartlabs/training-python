from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup(app):
  print(app.config)
  db.init_app(app)