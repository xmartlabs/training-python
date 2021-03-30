from flask import Flask
from sqlalchemy.exc import IntegrityError
import bcrypt
import secrets
import pdb
from blueprints.users.views import users
import database

# jwt_secret = secrets.token_hex()
jwt_secret = '2e717c22b824ea4220c8dc343289cede7c752cb54a4c4bbf2b666a804f878e0e'

def create_app():
  print('lolaaa')
  app = Flask(__name__)
  app.config['JWT_SECRET'] = '2e717c22b824ea4220c8dc343289cede7c752cb54a4c4bbf2b666a804f878e0e'

  database.setup(app)

  app.register_blueprint(users)
  print(users)
  return app

if __name__ == "__main__":
    app = create_app()
    app.run()