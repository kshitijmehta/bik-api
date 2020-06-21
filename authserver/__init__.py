from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'auth_secret'
app.config['JWT_SECRET_KEY'] = '$29000$F.K8lxLi3HuP0bo3Rui9Vw$dZy1iHEJZKJ/MgUAVPm1jaR9y/fK/0Xvt3AyRj3HvII'


api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


from authserver import routes
