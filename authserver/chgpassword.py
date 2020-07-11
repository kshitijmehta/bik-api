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
                                      '(%(user_id)s)', args, 'user password select from DB')
                if not result:
                    return {"message": "user not found"}, 500
                if bcrypt.check_password_hash(result['user_password'], data['password']):
                    new_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
                    args1 = {'ser': 3, 'password': new_password, 'email': ''}
                    run_db_query('call spUserInsertUpdate ('
                                 '_ser=>%(ser)s, '
                                 '_pwd=>%(password)s )',
                                 args1, 'user register in DB')

                    return {'message': 'password change success'}, 200

            except Exception as e:
                print(e)
                return {'message': 'cant change password'}
