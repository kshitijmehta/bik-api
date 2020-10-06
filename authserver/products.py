import datetime
import json
import os

import werkzeug
from flask_restful import Resource, reqparse
from authserver import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from authserver.transformers.product_list_transformer import product_list_transformer, single_product_transformer
from authserver.transformers.product_size_transformer import product_size_transformer
from authserver.transformers.product_subcategory_transformer import product_subcategory_transformer
from authserver.utils.products_util import save_image, delete_image, create_image_query, update_arg_for_image
from authserver.validation_schemas import product
from authserver.connection import run_db_query, run_db_query_multiple
from authserver.transformers.product_colour_transformer import product_colour_transformer


class Productsizeinsert(Resource):
    # @jwt_required
    def get(self):
        try:
            args = ''
            result = run_db_query('select s_id,s_value,s_code,prod_category, prod_categoryname '
                                  'from fnSizeSelect()', args, 'user info select from DB', True, True)
            return {"message": "color select success", 'data': product_size_transformer(result)}, 200
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
                        'product_category': data['product_category'],
                        'size_id': data['size_id']}

                if args['size_id'] != '0':
                    args['ser'] = 2

                result = run_db_query('call spsizeInsertUpdateDelete ('
                                      '_ser=>%(ser)s, '
                                      '_code=>%(product_size_code)s, '
                                      '_pcid=>%(product_category)s, '
                                      '_sid=>%(size_id)s, '
                                      '_value=>%(product_size)s )',
                                      args, 'Admin enter product size in DB', False)

                if result == 'error':
                    raise Exception

                return {'message': 'Size and code Insert success'}, 200
            except Exception as e:
                print(e)
                return {'message': 'Size and code Insert Error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productcolourinsert(Resource):
    # @jwt_required
    def get(self):
        try:
            args = ''
            result = run_db_query('select col_id , col_code, col_value  from fncolourSelect()',
                                  args, 'user info select from DB', True, True)
            if result == 'error':
                raise Exception

            return {'message': 'color select success', 'data': product_colour_transformer(result)}, 200
        except Exception as e:
            print(e)
            return {'message': 'color select error'}, 500

    def post(self):
        data = request.get_json()
        print(data)
        product_color_validation = product.validate_Product_colour(data)
        if product_color_validation['isValid']:
            try:
                args = {'ser': 1, 'product_color_code': data['product_color_code'],
                        'product_color': data['product_color'], 'colour_id': data['colour_id']}

                if args['colour_id'] != 0:
                    args['ser'] = 2

                run_db_query('call spColourInsertUpdateDelete ('
                             '_ser=>%(ser)s, '
                             '_code=>%(product_color_code)s, '
                             '_value=>%(product_color)s ,'
                             '_cid=>%(colour_id)s) ',
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

            args = request.args.getlist('productId')
            if not args:
                result = run_db_query(
                    'select prodid , prodcategory , prodname, proddesc, inrprice, usdprice, colour, size, '
                    'qty from fnAdminProductSelect()',
                    args, 'Prod info select select from DB', True, True)
                return {"message": "product info details select success", 'data': product_list_transformer(result)}, 200
            else:
                result = run_db_query(
                    'select prodid , prodcategory , prodname, proddesc, inrprice, usdprice, colour, size, '
                    'qty, subcategoryid, sizeid, colourid, imagename, imagepath from fnsingleproductselect(' + args[
                        0] + ')',
                    args, 'Prod info select select from DB', True, True)

            return {
                       "message": "product info details select success",
                       'singleData': single_product_transformer(result)[0]
                   }, 200
        except Exception as e:
            print(e)
            return {'message': 'product info details select error'}, 500

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('product_image_0', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('product_image_1', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('product_image_2', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('product_image_3', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('product_image_4', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('product_INR_price')
        parse.add_argument('product_USD_price')
        parse.add_argument('product_size_code')
        parse.add_argument('product_color_code')
        parse.add_argument('product_Qty')
        parse.add_argument('product_name')
        parse.add_argument('product_desc')
        parse.add_argument('product_subcategory_id')
        parse.add_argument('prod_id')
        parse.add_argument('deleted_image_paths')
        parse.add_argument('is_product_delete')

        data = parse.parse_args()

        # print(data)
        product_validation = product.validate_Product(data)
        if product_validation['isValid']:
            try:
                args = {'ser': 1, 'ser_image': 1, 'product_subcategory_id': data['product_subcategory_id'],
                        'product_INR_price': float(data['product_INR_price']),
                        'product_USD_price': float(data['product_USD_price']),
                        'product_Qty': int(data['product_Qty']),
                        'product_size_code': int(data['product_size_code']),
                        'product_color_code': int(data['product_color_code']),
                        'prod_id': int(data['prod_id']),
                        'prod_name': data['product_name'],
                        'prod_desc': data['product_desc'],
                        'deleted_image_paths': list(list(json.loads(data['deleted_image_paths']))),
                        'is_product_delete': bool(int(data['is_product_delete']))
                        }

                prod_id_query = ''
                if args['prod_id'] != 0:
                    prod_id_query = '_prod_id=>%(prod_id)s, '
                    if args['is_product_delete']:
                        args['ser'] = 3
                    else:
                        args['ser'] = 2

                # if args['ser'] == 1:
                image_save_status = save_image(data, 'product_image_0', 'product_image_1',
                                               'product_image_2', 'product_image_3', 'product_image_4')
                if image_save_status == 'error':
                    raise Exception

                product_save_result = run_db_query('call spproductinsertupdatedelete ('
                                                   '_ser=>%(ser)s, '
                                                   '_subcategid=>%(product_subcategory_id)s, '
                                                   '_inrprice=>%(product_INR_price)s, '
                                                   '_usdprice=>%(product_USD_price)s, '
                                                   '_colour=>%(product_color_code)s, '
                                                   '_size=>%(product_size_code)s, '
                                                   '_name=>%(prod_name)s, '
                                                   '_desc=>%(prod_desc)s, '
                                                   + prod_id_query +
                                                   '_qty=>%(product_Qty)s) ',
                                                   args, 'Admin enter product details in DB', True)
                if product_save_result == 'error':
                    raise Exception

                # set product_id for newly added product
                if args['ser'] == 1:
                    args['prod_id'] = product_save_result[0]

                # if args['product_image_id'] is not None:
                #     args['ser'] = 2

                if image_save_status:
                    # getting key:value dict using the
                    # uuid created and image name
                    image_query = create_image_query(image_save_status)
                    args.update(update_arg_for_image(image_save_status))

                    if image_query == 'error':
                        raise Exception

                    product_image_result = run_db_query('call spImageInsertUpdateDelete ('
                                                        '_ser=>%(ser_image)s, '
                                                        '_prodid=>%(prod_id)s,' +
                                                        image_query, args, 'Admin enter images in DB', False)
                    if product_image_result == 'error':
                        raise Exception

                # Delete images on updated
                if args['ser'] == 2 and len(args['deleted_image_paths']) > 0:
                    args['ser_image'] = 3
                    delete_images = run_db_query('call spImageInsertUpdateDelete ('
                                                 '_ser=>%(ser_image)s, '
                                                 '_prodid=>%(prod_id)s,'
                                                 '_imgpaths=>%(deleted_image_paths)s)',
                                                 args, 'Admin delete images in DB', False)
                    if delete_images == 'error':
                        raise Exception

                return {'message': 'Product details Insert success'}, 200
            except Exception as e:
                print(e)
                error_at = ''
                if image_save_status != 'error':
                    # delete images if the error was
                    # not at image saving to server
                    delete_image(image_save_status)
                    error_at = 'product save'

                    # delete product saved
                    # if the image save to db gave
                    # error for updated product
                    if product_save_result != 'error' and args['prod_id'] == 0:
                        error_at = 'image save'
                        args['ser'] = 4
                        run_db_query('call spproductinsertupdatedelete ('
                                     '_ser=>%(ser)s, '
                                     '_subcategid=>%(product_subcategory_id)s, '
                                     '_inrprice=>%(product_INR_price)s, '
                                     '_usdprice=>%(product_USD_price)s, '
                                     '_colour=>%(product_color_code)s, '
                                     '_size=>%(product_size_code)s, '
                                     '_name=>%(prod_name)s, '
                                     '_desc=>%(prod_desc)s, '
                                     '_prod_id=>%(prod_id)s, '
                                     '_qty=>%(product_Qty)s) ',
                                     args, 'Admin enter product details in DB', True)

                    # give proper error
                    # if the image save to db gave
                    # error for updated product
                    if product_save_result != 'error' and args['prod_id'] != 0:
                        error_at = 'Saving images, retry with the same images'

            return {'message': 'Product details Insert Error at ' + error_at}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productsubcategoryinformation(Resource):
    # @jwt_required
    def get(self):
        try:
            args = ''
            result = run_db_query('select ps_id ,cat_name, cat_id, ps_name, ps_desc '
                                  'from fnProdSubCategSelect()',
                                  args, 'Prod sub category select select from DB', True, True)

            return {"message": "product sub category details select success",
                    'data': product_subcategory_transformer(result)}, 200
        except Exception as e:
            print(e)
            return {'message': 'SubCategory details select error'}, 500

    def post(self):
        data = request.get_json()
        print(data)
        product_subcategory_validation = product.validate_Product_subcategory(data)
        if product_subcategory_validation['isValid']:
            try:
                args = {'ser': 1, 'product_category_id': data['product_category_id'],
                        'product_name': data['product_name'],
                        'product_desc': data['product_desc'], 'subcategory_id': data['subcategory_id']}

                if args['subcategory_id'] != '0':
                    args['ser'] = 2
                result = run_db_query('call spProdSubCategInsertUpdateDelete ('
                                      '_ser=>%(ser)s, '
                                      '_pcid=>%(product_category_id)s, '
                                      '_name=>%(product_name)s, '
                                      '_psid=>%(subcategory_id)s,'
                                      '_desc=>%(product_desc)s)',
                                      args, 'Admin enter SubCategory type in DB', False)
                if result == 'error':
                    raise Exception

                return {'message': 'SubCategory type Insert success'}, 200
            except Exception as e:
                print(e)
            return {'message': 'SubCategory type insert error'}, 500
        else:
            return {'message': 'SubCategory field validation error'}, 500
