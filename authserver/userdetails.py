from datetime import datetime
from flask_restful import Resource
from authserver import bcrypt, admin_required
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from authserver.transformers.login_transformer import login_transformer
from authserver.transformers.user_transformer import admin_user_transformer
from authserver.validation_schemas import userinfo
from authserver.connection import run_db_query


class UserInfo(Resource):
    @jwt_required
    def get(self):
        try:
            identity = get_jwt_identity()
            args = {'user_id': identity['id'], 'email': identity['email']}
            result = run_db_query('select userid, fname, lname, mobno, dob, gender,discount, addrid, addrline1, '
                                  'addrline2, addrline3, city, state, pincode ,country from PersonalInfoSelect'
                                  '(%(user_id)s)', args, 'user info select from DB', True)
            if not result:
                return {"message": "user not found"}, 500
            else:
                data = login_transformer(result, args['email'], identity['usertype'] == 'a')
                return {"message": "User select success", "data": data}, 200
        except Exception as e:
            print(e)
            return {'message': 'user select error'}, 500

    @jwt_required
    def post(self):
        data = request.get_json()
        user_validation = userinfo.validate_user(data)
        if user_validation['isValid']:
            identity = get_jwt_identity()
            print(data)
            try:
                args = {'ser': 2, 'user_id': identity['id'],
                        'email': identity['email'],
                        'f_name': data['firstName'], 'l_name': data['lastName'],'mobile': data['mobile'],
                        'gender': data['gender'], 'dob': data['dob'], 'typecode': 'c',
                        'line1': data['addressLineOne'], 'line2': data['addressLineTwo'], 'line3': data['addressLineThree'],
                        'city': data['city'], 'state': data['state'], 'pincode': data['pincode'],
                        'country': data['country'], 'pwd': '', 'addressId': data['addressId'], 'addrserial': 1}
                if args['dob'] != 'None':
                    args['dob'] = datetime.strptime(args['dob'], '%Y-%m-%d').isoformat()
                else:
                    args['dob'] = None
                result = run_db_query('call spUserInsertUpdate ('
                                      '_ser=>%(ser)s, '
                                      '_email=>%(email)s, '
                                      '_mobileno=>%(mobile)s, '
                                      '_pwd=>%(pwd)s, '
                                      '_typecode=>%(typecode)s, '
                                      '_fname=>%(f_name)s, '
                                      '_lname=>%(l_name)s, '
                                      '_gender=>%(gender)s,'
                                      '_dob=>%(dob)s) ',
                                      args, 'user enter details in DB', False)
                if result == 'error':
                    raise Exception

                address = data['addressId'] != ''
                if not address:
                    args['ser'] = 1
                else:
                    args['ser'] = 2
                args['typecode'] = 'h'
                result = run_db_query('call spaddressinsertupdatedelete ('
                                      '_ser=>%(ser)s, '
                                      '_userid=>%(user_id)s, '
                                      '_addrserial=>%(addrserial)s, '
                                      '_typecode=>%(typecode)s, '
                                      '_line1=>%(line1)s, '
                                      '_line2=>%(line2)s, '
                                      '_line3=>%(line3)s,'
                                      '_city=>%(city)s, '
                                      '_state=>%(state)s, '
                                      '_pincode=>%(pincode)s, '
                                      '_country=>%(country)s)',
                                      args, 'user enter/update address in DB', True)
                print(str(result[0]))
                if result == 'error':
                    raise Exception
                return {'message': 'user personal detail add success', 'data': str(result[0])}, 200
            except Exception as e:
                print(e)
                return {'message': 'user personal detail error'}, 500

        else:
            return {'message': 'Userinfo field validation error'}, 500


class AllUserInfo(Resource):
    @admin_required
    def get(self):
        try:
            result = run_db_query('select userid, fname, lname, mobno, dob, gender,emailid,'
                                  'userdiscount, addrid, addrline1, addrline2,'
                                  '  addrline3, city, state, pincode ,country from alluserinformation'
                                  '()', {}, 'user info select from DB', True, True)
            if result == 'error':
                raise Exception

            data = admin_user_transformer(result)
            return {"message": "User select success", "data": data}, 200
        except Exception as e:
            print(e)
            return {'message': 'Some error occurred, retry'}, 500


class UpdateUserDiscount(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        discount_validation = userinfo.validate_user_discount(data)
        if discount_validation['isValid']:
            try:
                args = {'ser': 5, '_email': data['email'],
                        '_discount': data['discount'], '_mobileno': '',
                        '_pwd': '', '_typecode': ''}

                result = run_db_query('call spUserInsertUpdate ('
                                      '_ser=>%(ser)s, '
                                      '_email=>%(_email)s, '
                                      '_mobileno=>%(_mobileno)s, '
                                      '_pwd=>%(_pwd)s, '
                                      '_typecode=>%(_typecode)s, '
                                      '_discount=>%(_discount)s )',
                                      args, 'user enter details in DB', False)
                if result == 'error':
                    raise Exception
                return {'message': 'Discount Update'}, 200

            except Exception as e:
                print(e)
                return {'message': 'Some error occurred'}, 500
        else:
            return {'message':'User discount schema validation error'}, 500
