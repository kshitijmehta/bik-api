from functools import wraps

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_bcrypt import Bcrypt
import secrets
import logging

app = Flask(__name__, static_folder='images')
app.config['JWT_SECRET_KEY'] = secrets.secrets['JWT_SECRET_KEY']
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity['usertype'] == 'a':
        return {'roles': 'admin'}
    else:
        return {'roles': 'customer'}


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return {'message': 'Not an admin, login again'}, 403
        else:
            return fn(*args, **kwargs)

    return wrapper


from authserver import routes
