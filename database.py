from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup(app):
  print('databas')
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost/alembicdb"
  db.init_app(app)