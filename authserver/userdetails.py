import datetime
from flask_restful import Resource
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from authserver.validation_schemas import userinfo
from authserver.connection import run_db_query

class Userinfo(Resource):
    @jwt_required
    def get(self):
        try:
            args = {'user_id': '1'}
            result = run_db_query('select * from PersonalInfoSelect'
                                  '(%(user_id)s)', args, 'user info select from DB')
            if not result:
              return {"message": "user not found"}, 500
            else:
                return {"message": "User select success"}, 200
        except Exception as e:
            print(e)
            return {'message': 'user select error'}, 500

    @jwt_required
    def post(self):
         data = request.get_json()
         user_validation = userinfo.validate_user(data)
         if user_validation['isValid']:
            try:
                    args = {'ser': 2, 'f_name': data['f_name'], 'l_name': data['l_name'],
                            'gender': data['gender'], 'dob': data['dob'],
                            'typecode': 'c', 'line1': data['line1'],
                            'line2': data['line2'], "line3": data['line3'],
                            'city': data['city'], 'state': data['state'],
                            "country": data['country']}

                    run_db_query('call spUserInsertUpdate ('
                                 '_ser=>%(ser)s, '
                                 '_fname=>%(f_name)s, '
                                 '_lname=>%(l_name)s, '
                                 '_gender=>%(gender)s,'
                                 '_dob=>%(dob)s )',
                                 args, 'user enter details in DB')

                    args['ser'] = 1
                    run_db_query('call spaddressinsertupdatedelete ('
                                 '_ser=>%(ser)s, '
                                 '_typecode=>%(typecode)s, '
                                 '_line1=>%(line1)s, '
                                 '_line2=>%(line2)s, '
                                 '_line3=>%(gline3)s,'
                                 '_city=>%(city)s'
                                 '_state=>%(state)s'
                                 '_country=>%(country)s)',
                                 args, 'user enter details in DB')

                    return {'message': 'user personal detail add success'}, 200
            except Exception as e:
                        print(e)
                        return {'message': 'user personal detail error'}, 500


         else:
            return {'message': 'register field validation error'}, 500

