from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'auth_secret'
app.config['JWT_SECRET_KEY'] = '$29000$F.K8lxLi3HuP0bo3Rui9Vw$dZy1iHEJZKJ/MgUAVPm1jaR9y/fK/0Xvt3AyRj3HvII'


try:
    conn = psycopg2.connect("dbname ='postgres' user='postgres' host='localhost' password='kpworks'")
except Exception as e:
    print('Not able to connect server')
    print(e)
#finally close the connection, use traceback module for exception -> traceback.print_exc()

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


from authserver import routes
