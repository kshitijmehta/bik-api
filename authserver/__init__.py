from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'auth_secret'

try:
    conn = psycopg2.connect("dbname ='postgres' user='postgres' host='localhost' password='kpworks'")
except Exception as e:
    print('Not able to connect server')
    print(e)


api = Api(app)
# db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


from authserver import routes