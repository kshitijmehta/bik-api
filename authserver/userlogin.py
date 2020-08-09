import datetime
from flask_restful import Resource
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from authserver.validation_schemas import register, login
from authserver.connection import run_db_query


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        user_validation = register.validate_user(data)
        if user_validation['isValid']:
            try:
                email = data['email']
                phone_number = data['mobile']
                password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                args = {'ser': 1, 'email': email, 'phone_number': phone_number, "password": password, "typecode": 'c'}

                result = run_db_query('select userid, userpassword from getuseridpassword ('
                                      '_email=>%(email)s)',
                                      args, 'get userid and password from DB', True)
                if result == 'error':
                    raise Exception

                if not result:
                    result = run_db_query('call spUserInsertUpdate ('
                                          '_ser=>%(ser)s, '
                                          '_email=>%(email)s, '
                                          '_mobileno=>%(phone_number)s, '
                                          '_pwd=>%(password)s,'
                                          '_typecode=>%(typecode)s )',
                                          args, 'user register in DB', False)

                    if result == 'error':
                        raise Exception

                    return {'message': 'Registration success, please login'}, 200

                else:
                    return {'message': 'User already exists, trying login'}, 500
            except Exception as e:
                print(e)
                return {'message': 'user registration error'}, 500

        else:
            return {'message': 'Error occurred, please try again'}, 500


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user_login_validation = login.validate_user_login(data)
        if user_login_validation['isValid']:
            try:
                args = {'email': data['email']}
                result = run_db_query('select userid, userpassword from getuseridpassword ('
                                      '_email=>%(email)s)',
                                      args, 'get userid and password from DB', True)
                if result == 'error':
                    raise Exception

                if not result:
                    return {"message": "User already exists"}, 500
                password = data['password'].encode('utf-8')
                if bcrypt.check_password_hash(result['userpassword'], password):
                    access_token = create_access_token(identity={'email': args['email'], 'id': result['userid']},
                                                       expires_delta=datetime.timedelta(hours=1))
                    return {"message": 'Login successful', "access_token": access_token}, 200
                else:
                    return {"message": "Invalid credentials"}, 500

            except Exception as e:
                print(e)
                return {'message': 'user login error'}, 500

        else:
            return {'message': 'login field validation error'}, 500


class ProtectedRoute(Resource):
    """This is a test route to check jwt token"""

    @jwt_required
    def get(self):
        return {"message": "this is a protected route"}