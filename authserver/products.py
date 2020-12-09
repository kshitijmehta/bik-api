import datetime
import json
import os

import werkzeug
from flask_restful import Resource, reqparse
from authserver import bcrypt, admin_required, app
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from authserver.transformers.product_category_transformer import product_category_transformer
from authserver.transformers.product_count_transformer import product_count_transformer
from authserver.transformers.product_list_customer_transformer import product_list_customer_transformer
from authserver.transformers.product_list_transformer import product_list_transformer, single_product_transformer
from authserver.transformers.product_size_transformer import product_size_transformer
from authserver.transformers.product_subcategory_transformer import product_subcategory_transformer
from authserver.utils.products_util import save_image, delete_image, create_image_query, update_arg_for_image, \
    create_tuple_for_product_details
from authserver.validation_schemas import product
from authserver.connection import run_db_query, run_db_query_multiple
from authserver.transformers.product_colour_transformer import product_colour_transformer
from authserver.transformers.product_quick_list_transformer import product_quick_list_transformer, \
    product_trending_latest_list


class Productsizeinsert(Resource):
    def get(self):
        try:
            args = ''
            result = run_db_query('select s_id,s_value,s_code,prod_category, prod_categoryname '
                                  'from fnSizeSelect()', args, 'user info select from DB', True, True)
            return {"message": "color select success", 'data': product_size_transformer(result)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'color select error'}, 500

    @admin_required
    def post(self):
        data = request.get_json()
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
                app.logger.debug(e)
                return {'message': 'Size and code Insert Error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productcolourinsert(Resource):
    def get(self):
        try:
            args = ''
            result = run_db_query('select col_id , col_code, col_value  from fncolourSelect()',
                                  args, 'user info select from DB', True, True)
            if result == 'error':
                raise Exception

            return {'message': 'color select success', 'data': product_colour_transformer(result)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'color select error'}, 500

    @admin_required
    def post(self):
        data = request.get_json()
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
                app.logger.debug(e)
            return {'message': 'Color and code Insert Error'}, 500
        else:
            return {'message': 'Product field validation error'}, 500


class Productinformation(Resource):
    def get(self):
        try:

            args = request.args.getlist('productId')
            if not args:
                result = run_db_query(
                    'select prodid , prodcategory , prodname, proddesc, qty, trending, latest from '
                    'fnAdminProductSelect()',
                    args, 'Prod info select select from DB', True, True)

                return {"message": "product info details select success", 'data': product_list_transformer(result)}, 200
            else:
                result = run_db_query(
                    'select prodid , prodcategory , prodname, proddesc, inrprice, usdprice, colour, size, proddetailid,'
                    'qty, subcategoryid, sizeid, colourid, imagename, imagepath from fnsingleproductselect(' + args[
                        0] + ')',
                    args, 'Prod info select select from DB', True, True)

            return {
                       "message": "product info details select success",
                       'singleData': single_product_transformer(result)[0]
                   }, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'product info details select error'}, 500

    @admin_required
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
        parse.add_argument('size_colour_quantity_combo')
        parse.add_argument('deleted_product_detailIds')

        data = parse.parse_args()

        product_validation = product.validate_Product(data)
        if product_validation['isValid']:
            try:
                args = {'ser': 1, 'ser_image': 1, 'product_subcategory_id': data['product_subcategory_id'],
                        'product_INR_price': float(data['product_INR_price']),
                        'product_USD_price': float(data['product_USD_price']),
                        # 'product_Qty': int(data['product_Qty']),
                        # 'product_size_code': int(data['product_size_code']),
                        # 'product_color_code': int(data['product_color_code']),
                        'prod_id': int(data['prod_id']),
                        'prod_name': data['product_name'],
                        'prod_desc': data['product_desc'],
                        'size_colour_quantity_combo': data['size_colour_quantity_combo'],
                        'deleted_image_paths': list(list(json.loads(data['deleted_image_paths']))),
                        'is_product_delete': bool(int(data['is_product_delete'])),
                        'deleted_product_detailIds': list(json.loads(data['deleted_product_detailIds']))
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
                                                   '_name=>%(prod_name)s, '
                                                   + prod_id_query +
                                                   '_desc=>%(prod_desc)s ) ',
                                                   args, 'Admin enter product details in DB', True)
                if product_save_result == 'error':
                    raise Exception

                # set product_id for newly added product
                if args['ser'] == 1:
                    args['prod_id'] = product_save_result[0]

                # if args['product_image_id'] is not None:
                #     args['ser'] = 2

                product_details_query = create_tuple_for_product_details(
                    json.loads(args['size_colour_quantity_combo']),
                    args['prod_id'],
                    args['product_INR_price'],
                    args['product_USD_price']
                )

                if product_details_query != '':
                    args['product_details_query'] = product_details_query
                    product_details = run_db_query('call spproductdetails_add ('
                                                   '_prod_details=>%(product_details_query)s )',
                                                   args, 'Save product details to DB', False)

                    if product_details == 'error':
                        raise Exception

                for update_product_details_items in json.loads(args['size_colour_quantity_combo']):
                    do_update = False
                    update_args = {}
                    for key, value in update_product_details_items.items():
                        update_args[key] = value
                        if key == 'productDetailId' and value != '0':
                            do_update = True
                    if do_update:
                        update_args['product_INR_price'] = args['product_INR_price']
                        update_args['product_USD_price'] = args['product_USD_price']
                        update_pd_result = run_db_query('call spProductDetails_Update ('
                                                        '_pd_id=>%(productDetailId)s, '
                                                        '_size=>%(size)s, '
                                                        '_colour=>%(colour)s,'
                                                        '_inrprice=>%(product_INR_price)s,'
                                                        '_usdprice =>%(product_USD_price)s,'
                                                        '_qty=>%(quantity)s )',
                                                        update_args, 'Updateproduct details to DB', False)
                        if update_pd_result == 'error':
                            raise Exception

                if int(data['prod_id']) != 0:
                    update_pd_price = run_db_query('call spproductdetails_price_update ('
                                                   '_prod_id=>%(prod_id)s, '
                                                   '_inrprice=>%(product_INR_price)s,'
                                                   '_usdprice =>%(product_USD_price)s )',
                                                   args, 'Updating price', False)
                    if update_pd_price == 'error':
                        raise Exception

                if len(args['deleted_product_detailIds']) > 0:
                    for delete_id in args['deleted_product_detailIds']:
                        if delete_id != '':
                            delete_id_args = {'delete_id': int(delete_id)}
                            delete_id_result = run_db_query('call spproductdetails_delete('
                                                            '_pd_id=>%(delete_id)s )',
                                                            delete_id_args, 'Delete product details', False)
                            if delete_id_result == 'error':
                                raise Exception

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
                app.logger.debug(e)
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


class ProductCategory(Resource):
    def get(self):
        try:
            args = ''
            result = run_db_query('select ps_id ,cat_name'
                                  ' from fnProdCategSelect()',
                                  args, 'Prod sub category select select from DB', True, True)
            if result == 'error':
                raise Exception
            identity = get_jwt_identity()
            return {"message": "product category details select success",
                    'data': product_category_transformer(result, identity['usertype'] == 'a' if identity else False)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'product category details select error'}, 500


class Productsubcategoryinformation(Resource):
    def get(self):
        try:
            args = ''
            result = run_db_query('select ps_id ,cat_name, cat_id, ps_name, ps_desc '
                                  'from fnProdSubCategSelect()',
                                  args, 'Prod sub category select select from DB', True, True)

            return {"message": "product sub category details select success",
                    'data': product_subcategory_transformer(result)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'SubCategory details select error'}, 500

    @admin_required
    def post(self):
        data = request.get_json()
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
                app.logger.debug(e)
            return {'message': 'SubCategory type insert error'}, 500
        else:
            return {'message': 'SubCategory field validation error'}, 500


class Productcount(Resource):
    def get(self):
        try:
            args = ''
            result = run_db_query('select prod_subcateg_id,'
                                  'prod_subacateg_name, '
                                  'prod_colour, '
                                  'colour_value, '
                                  # 'size_id, '
                                  'prod_size '
                                  # 'prod_count '
                                  'from vw_product_counts', args, 'product count view', True, True)
            return {"message": "product count success", 'data': product_count_transformer(result)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'product count error'}, 500


class ProductListCustomer(Resource):
    def get(self):
        try:
            args = {
                'offset': request.args.getlist('offset')[0],
                'limit': request.args.getlist('limit')[0],
                'cid': None,
                'sub_cid': None,
                'sid': None,
                'pid': None,
                'price': None,
                'search_text': request.args.getlist('searchText')[0]
            }
            cid = request.args.getlist('colourId')[0]
            if cid:
                args['cid'] = '(' + cid + ')'

            sid = request.args.getlist('sizeId')[0]
            if sid:
                args['sid'] = '(' + sid + ')'

            sub_cid = request.args.getlist('subCategoryId')[0]
            if sub_cid:
                args['sub_cid'] = '(' + sub_cid + ')'

            pid = request.args.getlist('categorydId')[0]
            if pid:
                args['pid'] = '(' + pid + ')'

            sp = request.args.getlist('startPrice')[0]
            ep = request.args.getlist('endPrice')[0]
            currency = request.args.getlist('currency')[0]

            if currency != '':
                if sp != '' and ep != '':
                    if currency == 'IN':
                        args['price'] = 'prod_inr_price >= ' + str(sp) + ' and prod_inr_price <= ' + str(ep)
                    else:
                        args['price'] = 'prod_usd_price >= ' + str(sp) + ' and prod_usd_price <= ' + str(ep)
                elif sp != '':
                    if currency == 'IN':
                        args['price'] = 'prod_inr_price >= ' + str(sp)
                    else:
                        args['price'] = 'prod_usd_price >= ' + str(sp)
                elif ep != '':
                    if currency == 'IN':
                        args['price'] = 'prod_inr_price <= ' + str(ep)
                    else:
                        args['price'] = 'prod_usd_price <= ' + str(ep)
            # print(args)
            result = run_db_query('select prodid, prodcategory,prodsubcategory ,prodname, proddesc, inrprice, '
                                  'usdprice, colour, size, prodimgpath, prodimgname, proddetailid '
                                  'from fnproductlistselect('
                                  '_colour=>%(cid)s, '
                                  '_size=>%(sid)s, '
                                  '_prodcategid=>%(pid)s, '
                                  '_subcategid=>%(sub_cid)s, '
                                  '_prodname=>%(search_text)s, '
                                  '_price=>%(price)s '
                                  ') LIMIT ' + args['limit'] + ' OFFSET ' + args['offset'],
                                  args, 'get productlist for customer', True, True)

            return {"message": "get productlist for customer", 'data': product_list_customer_transformer(result)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'get productlist for customer error'}, 500


class ProductHighlight(Resource):
    @admin_required
    def post(self):
        try:
            data = request.get_json()
            args = {'ser': 4, '_latest': data['latest'], '_trending': data['trending'], '_prod_id': data['productId'],
                    '_subcategid': 0, '_name': '', '_desc': ''}
            product_update_result = run_db_query('call spproductinsertupdatedelete ('
                                                 '_ser=>%(ser)s, '
                                                 '_subcategid=>%(_subcategid)s, '
                                                 '_name=>%(_name)s, '
                                                 '_latest=>%(_latest)s, '
                                                 '_trending=>%(_trending)s, '
                                                 '_prod_id=>%(_prod_id)s, '
                                                 '_desc=>%(_desc)s ) ',
                                                 args, 'Update product highlight', False)
            if product_update_result == 'error':
                raise Exception
            return {'message': 'Highlight saved.'}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Some error occurred, try again'}, 500


class ProductReturn(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        return_validation = product.validate_returns(data)
        if return_validation['isValid']:
            try:
                args = {'ser': 1, 'order_detail_id': data['order_detail_id'],
                        'return_status': data['return_status'] if 'return_status' in data else None,
                        'payment_status': data['payment_status'] if 'payment_status' in data else None,
                        'is_admin_return': data['is_admin_return']
                        }

                if args['is_admin_return']:
                    args['ser'] = 2
                run_db_query('call store.spReturnUpdate ('
                             '_ser=>%(ser)s, '
                             '_orderdetailid=>%(order_detail_id)s, '
                             '_returnstatus=>%(return_status)s, '
                             '_paymentstatus=>%(payment_status)s )',
                             args, 'return flags added or changed  in DB', False)
                return {'message': 'return flags add or change success'}, 200
            except Exception as e:
                app.logger.debug(e)
                return {'message': 'return flags add or change Error'}, 500
        else:
            return {'message': 'return field validation error'}, 500


class ProductRelated(Resource):
    def post(self):
        try:
            data = request.get_json()
            product_related_validation = product.product_related_check(data)
            if product_related_validation['isValid']:
                args = {'subcategory_id': data['subcategoryId'], 'product_id': data['productId']}
                result = run_db_query('select prodid, prod_categ_name , prodname, prodinrprice ,'
                                      'produsdprice ,productdetailid, prodimgname, prodimgpath'
                                      ' from fnRelatedProduct ('
                                      '_subcategid=>%(subcategory_id)s, '
                                      '_productid=>%(product_id)s)'
                                      , args, ' related products returned from DB', True, True)
                if result == 'error':
                    raise Exception
                return {"message": "related products return success ",
                        'data': product_quick_list_transformer(result)}, 200
            else:
                return {'message': 'related product validation error'}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'related products return error'}, 500


class TrendingLatest(Resource):
    def get(self):
        try:
            data = request.args.getlist('type')[0]
            if data:
                args = {"type": int(data)}
                result = run_db_query(
                    'select  prod_id, prod_categ_name , prod_name, prod_inr_price ,prod_usd_price ,'
                    'productdetailid, prod_img_name, prod_img_path '
                    ' from fnGetLatestTrendingProduct('
                    'i=>%(type)s)', args, ' trending latest info select select from DB', True, True)
                return {"message": "trending latest product select success",
                        'data': product_trending_latest_list(result)}, 200
            else:
                return {"message": "No tye defined"}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'trending latest product select error'}, 500
