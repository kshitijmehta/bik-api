from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import secrets

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secrets.secrets['JWT_SECRET_KEY']


api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


from authserver import routes
