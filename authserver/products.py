import datetime
from flask_restful import Resource
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from authserver.connection import run_db_query


class Productsizeinsert(Resource):
    @jwt_required
    def post(self):
        data = request.get_jason()
        try:
            args = {'ser': 1, 'product_size': data['product_size'],
                    'product_size_code': data['product_size_code']}

            run_db_query('call spsizeInsertUpdateDelete ('
                         '_ser=>%(ser)s, '
                         '_code=>%(product_size_code)s, '
                         '_value=>%(product_size)s, )', args, 'Admin enter product size in DB')
            return {'message': 'Size and code Insert success'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Size and code Insert Error'}, 500


class Productscolourinsert(Resource):
    @jwt_required
    def post(self):
        data = request.get_jason()
        try:
            args = {'ser': 1, 'product_color_code': data['product_color_code'],
                    'product_color': data['product_color']}

            run_db_query('call spColourInsertUpdateDelete ('
                         '_ser=>%(ser)s, '
                         '_code=>%(product_color_code)s, '
                         '_value=>%(product_color)s, )', args, 'Admin enter product color DB')
            return {'message': 'Color and code Insert success'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Color and code Insert Error'}, 500


class Productinfoinsert(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            args = {'ser': 1, 'product_subcategory_id': data['product_subcategory_id'],
                    'product_INR_price': data['product_INR_price'],
                    'product_USD_price': data['product_USD_price'],
                    'product_Qty': data['product_Qty'],
                    'product_size_code': data['product_size_code'],
                    'product_color_code': data['product_color_code']
                    }
            run_db_query('call spproductinsertupdatedelete ('
                         '_ser=>%(ser)s, '
                         '_subcategID=>%(product_subcateg_id)s, '
                         '_inrprice=>%(product_priceINR)s, '
                         '_usdprice=>%(product_USD_price)s, '
                         '_colour=>%(product_color_code)s, '
                         '_size=>%(product_size_code)s,)'
                         '_qty=>%(product_Qty)s,)',
                         args, 'Admin enter product details in DB')

            return {'message': 'Product details Insert success'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Product details Insert Error'}, 500


class Productsubcategoryinsert(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            args = {'ser': 1, 'product_category_id': data['product_category_id'], 'product_name': data['product_name'],
                    'product_desc': data['product_desc']}

            run_db_query('call spProdTypeInsertUpdateDelete ('
                         '_ser=>%(ser)s, '
                         '_categoryid=>%(product_category_id)s, '
                         '_name=>%(product_name)s, '
                         '_desc=>%(product_desc)s,)',
                         args, 'Admin enter product type in DB')
            return {'message': 'Product type Insert success'}, 200
        except Exception as e:
            print(e)
        return {'message': 'Product type insert error'}, 500


class Productsubcategoryupdate(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            args = {'ser': 2, 'product_category_id': '', 'product_name': data['product_name'],
                    'product_desc': data['product_desc'],
                    'product_subcategory_id': data['product_subcategory_id']}

            run_db_query('call spProdTypeInsertUpdateDelete ('
                         '_ser=>%(ser)s, '
                         '_subcateg_id=>%(product_subcategory_id)s, '
                         '_name=>%(product_name)s, '
                         '_desc=>%(product_desc)s,)',
                         args, 'Admin update product type in DB')
            return {'message': 'Product type update success'}, 200
        except Exception as e:
            print(e)
        return {'message': 'Product type update error'}, 500


class Productinfouppdate(Resource):
    def post(self):
        data = request.get_json()
        try:

            args = {'ser': 2, 'product_subcategory_id': data['product_subcategory_id'],
                    'product_INR_price': data['product_INR_price'],
                    'product_USD_price': data['product_USD_price'],
                    'product_Qty': data['product_Qty'],
                    'product_size_code': data['product_size_code'],
                    'product_color_code': data['product_color_code']}
            run_db_query('call spproductinsertupdatedelete ('
                         '_ser=>%(ser)s, '
                         '_subcategID=>%(product_subcateg_id)s, '
                         '_inrprice=>%(product_priceINR)s, '
                         '_usdprice=>%(product_USD_price)s, '
                         '_colour=>%(product_color_code)s, '
                         '_size=>%(product_size_code)s,)'
                         '_qty=>%(product_Qty)s,)',
                         args, 'Admin Updated product details in DB')

            return {'message': 'Product details Update success'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Product details Update Error'}, 500
