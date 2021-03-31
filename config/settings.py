from environs import Env

env = Env()
env.read_env()

# JWT_SECRET is required
JWT_SECRET = env.str("JWT_SECRET")

SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
