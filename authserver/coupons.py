import datetime
from flask_restful import Resource
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from authserver.transformers.product_coupon_transformer import product_coupon_transformer
from authserver.validation_schemas import coupon
from authserver.connection import run_db_query


class Coupondetails(Resource):
    # @jwt_required
    def get(self):
        try:
            args = ''
            result = run_db_query('select cp_id,cp_code,cp_value '
                                  'from fnCouponSelect()', args, 'coupon info select from DB', True, True)
            return {"message": "color select success", 'data': product_coupon_transformer(result)}, 200
        except Exception as e:
            print(e)
            return {'message': 'color select error'}, 500

    def post(self):
        data = request.get_json()
        print(data)
        coupon_validation = coupon.validate_coupon(data)
        if coupon_validation['isValid']:
            try:
                args = {'ser': 1, 'coupon_code': data['coupon_code'],
                        'coupon_value': data['coupon_value'], 'coupon_id': data['coupon_id'],
                        'delete_flag': data['isDelete']
                        }

                if args['coupon_id'] != 0 and args['delete_flag'] is False:
                    args['ser'] = 2
                elif args['coupon_id'] != 0 and args['delete_flag'] is True:
                    args['ser'] = 3
                print(args)
                result = run_db_query('call spCouponInsertUpdateDelete ('
                                      '_ser=>%(ser)s, '
                                      '_cp_code=>%(coupon_code)s, '
                                      '_cp_value=>%(coupon_value)s,'
                                      '_cp_id=>%(coupon_id)s )',
                                      args, 'Admin enter update or delete coupon in DB', True)
                if result == 'error':
                    raise Exception

                return {'message': 'Coupon size insert,update,delete success'}, 200
            except Exception as e:
                print(e)
                return {'message': 'Coupon size insert,update,delete Error'}, 500
        else:
            return {'message': 'Coupon field validation error'}, 500
