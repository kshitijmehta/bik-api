from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request

from authserver.connection import run_db_query
from authserver.transformers.cart_transformer import get_cart_transformer, add_to_cart_transformer, \
    update_cart_transformer


class CustomerCart(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        if identity['id']:
            args = {'user_id': identity['id']}
            result = run_db_query('select js from store.fn_get_cart (_userid=>%(user_id)s)',
                                  args, 'get cart information', True)

            if result[0]:
                return {'message': 'Get customer cart success', 'data': get_cart_transformer(result[0])}, 200
            else:
                return {'message': 'Get customer cart success', 'data': []}, 200
        else:
            return {'message': "Please login"}, 500

    @jwt_required
    def post(self):
        data = request.get_json()
        identity = get_jwt_identity()
        # order_validation = order.validate_order(data)
        # if order_validation['isValid']:
        try:
            args = {'user_id': identity['id'], 'product_detail_id': data['product_detail_id'],
                    'order_quantity': data['order_quantity'],
                    'price_id': data['price_id'], 'orderdetail_id': data['orderdetail_id'],
                    'delete_flag': data['delete_flag']
                    }

            if args['orderdetail_id'] != "0" and not args['delete_flag']:
                result = run_db_query('call store.order_item_update ('
                                      '_qty=>%(order_quantity)s, '
                                      '_odid=>%(orderdetail_id)s)',
                                      args, 'order details Update in DB', True)

                if not result[1]:
                    return {'message': 'order update success', 'data': {}}, 200
                else:
                    return {'message': 'order update success', 'data': update_cart_transformer(result[1])}, 200
            elif args['delete_flag']:
                result = run_db_query('call store.order_item_delete ('
                                      '_odid=>%(orderdetail_id)s)',
                                      args, 'order details Deleted in DB', False)

                return {'message': 'order delete success', 'message': result}, 200

            else:
                result = run_db_query('select * from store.order_item_add('
                                      '_uid=>%(user_id)s, '
                                      '_pdid=>%(product_detail_id)s, '
                                      '_prid=>%(price_id)s, '
                                      '_qty=>%(order_quantity)s)'
                                      , args, 'order details updated in DB', True)
                return {'message': 'order insert,update,delete success',
                        'data': add_to_cart_transformer(result[1])}, 200
        except Exception as e:
            print(e)
            return {'message': ' order insert,update,delete Error'}, 500
        # else:
        #   return {'message': 'order field validation error'}, 500


class UpdateCartQuantity(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            args = {'_order_detail_ids': data['orderDetailId']}
            result = run_db_query('select * from store.updatecartquantity ('
                                  '_order_detail_ids=>%(_order_detail_ids)s)',
                                  args, 'update cart quantities', True)
            if result == 'error':
                raise Exception
            if result['status']:
                return {'message': 'We updated your cart based on the product availability'}, 203
            else:
                return {'message': 'Cart quantity is valid'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Some error occurred, retry again'}, 500
