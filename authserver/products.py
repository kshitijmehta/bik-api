import datetime
from flask_restful import Resource
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from authserver.validation_schemas import product
from authserver.connection import run_db_query


class Productsizeinsert(Resource):
   # @jwt_required
    def get(self):
        try:
            args = ''
            result = run_db_query('select s_id,s_value,s_code,prod_category '
                         'from fnSizeSelect()', args, 'user info select from DB', True)
            return {"message": "color select success", 'data': result}, 200
        except Exception as e:
            print(e)
            return {'message': 'color select error'}, 500

    def post(self):
        data = request.get_json()
        print(data)
        product_size_validation = product.validate_Product_size(data)
        if product_size_validation['isValid']:
            try:
                args = {'ser': 1, 'product_size': data['product_size'],
                        'product_size_code': data['product_size_code'],
                        'product_category': data['product_category']}

                run_db_query('call spsizeInsertUpdateDelete ('
                             '_ser=>%(ser)s, '
                             '_code=>%(product_size_code)s, '
                             '_category_id=>%(product_category)s, '
                             '_value=>%(product_size)s )',
                             args, 'Admin enter product size in DB', False)
                return {'message': 'Size and code Insert success'}, 200
            except Exception as e:
                print(e)
                return {'message': 'Size and code Insert Error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productcolourinsert(Resource):
    #@jwt_required
    def get(self):
        try:
            args = ''
            run_db_query('select col_id , col_code, col_value  from fnColourSelect()', args, 'user info select from DB')
            return {"message": "color select success"}, 200
        except Exception as e:
            print(e)
            return {'message': 'color select error'}, 500

    def post(self):
        data = request.get_json()
        product_color_validation = product.validate_Product_colour(data)
        if product_color_validation['isValid']:
            try:
                args = {'ser': 1, 'product_color_code': data['product_color_code'],
                        'product_color': data['product_color']}

                run_db_query('call spColourInsertUpdateDelete ('
                             '_ser=>%(ser)s, '
                             '_code=>%(product_color_code)s, '
                             '_value=>%(product_color)s )',
                             args, 'Admin enter product color DB', False)
                return {'message': 'Color and code Insert success'}, 200
            except Exception as e:
                print(e)
            return {'message': 'Color and code Insert Error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productinformation(Resource):

    def get(self):
        try:
            args = ''
            result= run_db_query('select prodID , prodCategory , prodName, prodDesc, inrPrice, usdPrice, colour, size, '
                         'qty from fnAdminProductSelect()',
                         args, 'Prod info select select from DB', True)
            return {"message": "product info details select success", 'data': result}, 200
        except Exception as e:
            print(e)
            return {'message': 'product info details select error'}, 500

    def post(self):
        data = request.get_json()
        product_validation = product.validate_Product(data)
        if product_validation['isValid']:
            try:
                args = {'ser': 1, 'product_subcategory_id': data['product_subcategory_id'],
                        'product_INR_price': data['product_INR_price'],
                        'product_USD_price': data['product_USD_price'],
                        'product_Qty': data['product_Qty'],
                        'product_size_code': data['product_size_code'],
                        'product_color_code': data['product_color_code'],
                        'product_image_name': data['product_image_name'],
                        'product_image_path': data['product_image_path'],
                        'product_image_id': data['product_image_id'],
                        'prod_id': data['prod_id']
                        }

                if args['prod_id'] is not None:
                    args['ser'] = 2

                run_db_query('call spproductinsertupdatedelete ('
                             '_ser=>%(ser)s, '
                             '_subcategID=>%(product_subcateg_id)s, '
                             '_inrprice=>%(product_priceINR)s, '
                             '_usdprice=>%(product_USD_price)s, '
                             '_colour=>%(product_color_code)s, '
                             '_size=>%(product_size_code)s,)'
                             '_qty=>%(product_Qty)s)',
                             args, 'Admin enter product details in DB', False)
                if args['product_image_id'] is not None:
                    args['ser'] = 2
                run_db_query('call spImageInsertUpdateDelete ('
                             '_ser=>%(ser)s, '
                             '_prodid=>%(prod_id)s, '
                             '_name1=>%(product_image_name)s, '
                             '_imgpath1=>%(product_image_id)s) ',
                             args, 'Admin enter images in DB', False)

                return {'message': 'Product details Insert success'}, 200
            except Exception as e:
                print(e)
            return {'message': 'Product details Insert Error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productsubcategoryinformation(Resource):
   # @jwt_required
    def get(self):
        try:
            args = ''
            result = run_db_query('select ps_id ,cat_name, ps_name, ps_desc '
                                  'from fnProdSubCategSelect()',
                                  args, 'Prod sub category select select from DB', True)
            return {"message": "product sub category details select success",  'data': result}, 200
        except Exception as e:
            print(e)
            return {'message': 'product sub category details select error'}, 500

    def post(self):
        data = request.get_json()
        product_subcategory_validation = product.validate_Product_subcategory(data)
        if product_subcategory_validation['isValid']:
            try:
                args = {'ser': 1, 'product_category_id': data['product_category_id'],
                        'product_name': data['product_name'],
                        'product_desc': data['product_desc'], 'subcategory_id': data['subcategory_id']}

                if args['subcategory_id'] != "":
                    args['ser'] = 2
                run_db_query('call spProdSubCategInsertUpdateDelete ('
                             '_ser=>%(ser)s, '
                             '_pcid=>%(product_category_id)s, '
                             '_name=>%(product_name)s, '
                             '_psid=>%(subcategory_id)s,'
                             '_desc=>%(product_desc)s)',
                             args, 'Admin enter product type in DB', False)
                return {'message': 'Product type Insert success'}, 200
            except Exception as e:
                print(e)
            return {'message': 'Product type insert error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500
