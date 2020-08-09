from flask_restful import Resource
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from authserver.validation_schemas import pswdchng
from authserver.connection import run_db_query


class changepass(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        user_validation = pswdchng.validate_user(data)
        if user_validation['isValid']:

            try:
                identity = get_jwt_identity()
                args = {'user_id': identity['id']}
                result = run_db_query('select user_password from userPasswordSelect'
                                      '(%(user_id)s)', args, 'user password select from DB', True)
                if result == 'error':
                    raise Exception

                if not result:
                    return {"message": "user not found"}, 500

                if bcrypt.check_password_hash(result['user_password'], data['currentPassword']):
                    new_password = bcrypt.generate_password_hash(data['newPassword']).decode('utf-8')
                    args1 = {'ser': 3, 'password': new_password, 'email': identity['email'], 'mobile': '', 'typecode': 'c'}
                    run_db_query('call spUserInsertUpdate ('
                                 '_ser=>%(ser)s, '
                                 '_email=>%(email)s, '
                                 '_mobileno=>%(mobile)s, '
                                 '_pwd=>%(password)s, '
                                 '_typecode=>%(typecode)s)',
                                 args1, 'user register in DB', False)

                    if result == 'error':
                        raise Exception

                    return {'message': 'password change success'}, 200
                else:
                    return {'message': 'Current password is incorrect'}, 500

            except Exception as e:
                print(e)
                return {'message': 'cant change password'}, 500
        else:
            return {'message': 'change password validation error'}, 500

    @jwt_required
    def get(self):
        try:
            identity = get_jwt_identity()
            if identity['email'] != '':
                return {'message': 'get user setting success', 'data': {'emailAddress': identity['email']}}, 200
            return {'message': 'could not validate user', }, 500
        except Exception as e:
            print(e)
            return {'message': 'could not validate user exception', }, 500