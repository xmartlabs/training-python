from flask import Flask
from sqlalchemy.exc import IntegrityError
import bcrypt
import secrets
import pdb
from blueprints.users.views import users
import database

def create_app():
  app = Flask(__name__)
  app.config.from_object("config.settings")

  database.setup(app)

  app.register_blueprint(users)
  return app

if __name__ == "__main__":
    app = create_app()
    app.run()
