import ast
import http
import json
import time
from datetime import date

from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request
import razorpay
from paypalcheckoutsdk.core import SandboxEnvironment, PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersGetRequest
from paypalhttp import HttpError

from authserver import admin_required, app
from authserver.connection import run_db_query
from authserver.transformers.admin_orders_transformer import admin_orders
from authserver.transformers.customer_orders_transformer import customer_orders
from authserver.transformers.order_data_csv_transformer import order_data_csv_transformer
from authserver.utils.send_email import send_email, customer_order_details_helper
from authserver.validation_schemas import order
from authserver.validation_schemas.product import customer_returns
from secrets import secrets


class PlaceOrder(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            identity = get_jwt_identity()
            validation = order.validate_razorpay_paypal_cod_order(data)
            if validation['isValid']:
                if identity['id']:
                    args = {'user_id': identity['id'],
                            'user_amount': data['amount'],
                            'order_id': data['orderId'],
                            'coupon_id': data['couponId'] if 'couponId' in data else None}
                    # Price check
                    result = run_db_query('select _finaltotalvalue, status from '
                                          ' store.fncheckprice('
                                          '_user_id=>%(user_id)s, '
                                          '_order_id=>%(order_id)s, '
                                          '_coupon_id=>%(coupon_id)s, '
                                          '_webtotalvalue=>%(user_amount)s )'
                                          , args, 'price check call', True)

                    if result == 'error':
                        raise Exception
                    elif result['status']:
                        client = razorpay.Client(auth=(secrets['TEST_RAZORPAY_ID'], secrets['TEST_RAZORPAY_SECRET']))
                        today = date.today()
                        order_amount = float(args['user_amount']) * 100
                        order_currency = 'INR'
                        order_receipt = str(identity['id']) + '-' + str(int(round(time.time() * 1000)))
                        # notes = {'Shipping address': 'Bommanahalli, Bangalore'}  # OPTIONAL

                        response = client.order.create(dict(
                            amount=order_amount,
                            currency=order_currency,
                            receipt=order_receipt))

                        if response['id']:
                            response_data = {
                                'key': 'rzp_test_WDzaF0uIiGcdMu',
                                'amount': order_amount,
                                'currency': order_currency,
                                'name': 'Basic Kart',
                                'orderId': response['id'],
                                'receipt': order_receipt
                            }
                            return {'message': 'success', 'data': response_data}, 200
                        else:
                            return {'message': 'payment error'}, 500
                    else:
                        return {'message': 'Price changed for one or more product. Getting the latest price'}, 203
                else:
                    return {'message': 'User Auth is missing.'}, 401
            else:
                return {'message': 'Validation error, try again'}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'error', 'data': e}, 500


class PaymentSuccessRazorpay(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            validation = order.validate_razorpay_payment(data)
            if validation['isValid']:
                identity = get_jwt_identity()
                if identity['id']:
                    args = {'razorpay_payment_id': data['razorpayPaymentId'],
                            'razorpay_order_id': data['razorpayOrderId'],
                            'razorpay_signature': data['razorpaySignature'],
                            'order_id': data['orderId'],
                            'order_number': data['orderNumber'],
                            'address_id': data['addressId'],
                            'user_id': identity['id'],
                            'userName': data['userName'], 'userAddress': data['userAddress'],
                            'coupon_id': data['couponId'] if 'couponId' in data else None}
                    params_dict = {
                        'razorpay_order_id': args['razorpay_order_id'],
                        'razorpay_payment_id': args['razorpay_payment_id'],
                        'razorpay_signature': args['razorpay_signature']}

                    client = razorpay.Client(auth=(secrets['TEST_RAZORPAY_ID'], secrets['TEST_RAZORPAY_SECRET']))
                    is_payment_authentic = client.utility.verify_payment_signature(params_dict)
                    if is_payment_authentic is None:

                        result = run_db_query('call store.order_complete_razorpay('
                                              '_razorpay_payment_id=>%(razorpay_payment_id)s, '
                                              '_razorpay_order_id=>%(razorpay_order_id)s, '
                                              '_razorpay_signature=>%(razorpay_signature)s, '
                                              '_order_id=>%(order_id)s, '
                                              '_order_number=>%(order_number)s, '
                                              '_address_id=>%(address_id)s ,'
                                              '_user_id=>%(user_id)s, '
                                              '_coupon_id=>%(coupon_id)s )',
                                              args,
                                              'save payment success for razorpay', True)

                        if result[0] == 200:
                            # send order detail mail to customer
                            result = run_db_query('select productname, totalamount,'
                                                  'coupondiscount, userdiscount from public.fngetorderdetailsformail'
                                                  '(%(order_id)s)', args, 'user info select from DB', True, True)
                            if result == 'error':
                                app.logger.debug('Error in sending order detail mail to customer')
                                # raise Exception
                            product_data = customer_order_details_helper(result)

                            send_email(secrets['CUSTOMER_ORDER_DETAILS_TEMPLATE'], {
                                "to_email": identity['email'],
                                "variables": {
                                    "NAME": args['userName'],
                                    "ADDRESS": args['userAddress'],
                                    "ORDERNUMBER": "#" + str(args['order_number']),
                                    "ORDERDATE": date.today().strftime("%m/%d/%Y"),
                                    "PRODUCTIST": product_data['product_list'],
                                    "TOTALAMOUNT": product_data['total_amount'],
                                }
                            })
                            return {'message': 'success'}, 200
                        else:
                            return {'message': 'Some error occurred while processing the payment.'
                                               ' If the money has been deducted, please wait'
                                               ' for sometime and check the status of your order.'}, 500
                else:
                    return {'message': 'The user is invalid, please login again'}, 401
            else:
                return {'message': 'Some error occurred while processing the payment.'
                                   ' If the money has been deducted, please wait'
                                   ' for sometime and check the status of your order.'}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'The payment was not authentic. '
                               'Please try again or wait for sometime for us to check'}, 500


class PlaceOrderPaypal(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            identity = get_jwt_identity()
            validation = order.validate_razorpay_paypal_cod_order(data)
            if validation['isValid']:
                if identity['id']:
                    args = {'user_id': identity['id'], 'user_amount': data['amount'],
                            'user_display_amount': data['displayAmount'], 'order_id': data['orderId'],
                            'coupon_id': data['couponId'] if 'couponId' in data else None}
                    # Price check

                    result = run_db_query('select _finaltotalvalue, status from '
                                          ' store.fncheckprice('
                                          '_user_id=>%(user_id)s, '
                                          '_order_id=>%(order_id)s, '
                                          '_coupon_id=>%(coupon_id)s, '
                                          '_webtotalvalue=>%(user_amount)s )'
                                          , args, 'price check call', True)

                    if result == 'error':
                        raise Exception
                    elif result['status']:
                        # Creating Access Token for Sandbox
                        client_id = secrets['SANDBOX_PAYPAL_ID']
                        client_secret = secrets['SANDBOX_PAYPAL_SECRET']

                        # Creating an environment
                        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
                        client = PayPalHttpClient(environment)
                        order_request = OrdersCreateRequest()

                        order_request.prefer('return=representation')

                        order_request.request_body(
                            {
                                "intent": "CAPTURE",
                                "purchase_units": [
                                    {
                                        "amount": {
                                            "currency_code": "USD",
                                            "value": args['user_display_amount']
                                        }
                                    }
                                ],
                                "application_context": {
                                    "shipping_preference": 'NO_SHIPPING'
                                }
                            }
                        )
                        try:
                            # Call API with your client and get a response for your call
                            response = client.execute(order_request)
                            if response.result and response.result.id:

                                return {'message': 'success',
                                        'data': {'orderId': response.result.id}
                                        }, 200
                            else:
                                return {'message': 'Error while completing payment, please retry.'}, 500
                        except IOError as ioe:
                            if isinstance(ioe, HttpError):
                                # Something went wrong server-side
                                print(ioe.status_code)
                            return {'message': 'Error while completing payment, please retry.'
                                               ' If the issue still persists, try after sometime.'}, 500
                    else:
                        return {'message': 'Price changed for one or more product. Getting the latest price'},
                else:
                    return {'message': 'User Auth is missing.'}, 401
            else:
                return {'message': 'Validation error, try again'}, 500

        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Error while completing payment, please retry.'
                               ' If the issue still persists, try after sometime.'}, 500


class PaymentSuccessPaypal(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            identity = get_jwt_identity()
            validation = order.validate_paypal_payment(data)
            if validation['isValid']:
                if identity['id']:
                    args = {'paypal_response': json.dumps(data['paypalResponse']), 'order_id': data['orderId'],
                            'address_id': data['addressId'],'user_id': identity['id'], 'quantity': data['quantity'],
                            'userName': data['userName'],'userAddress': data['userAddress'],
                            'order_number': str(identity['id']) + '-' + str(int(round(time.time() * 1000))),
                            'coupon_id': data['couponId'] if 'couponId' in data else None,
                            'is_standard': data['isStandard']}
                    result = run_db_query('call store.order_complete_paypal('
                                          '_paypal_response=>%(paypal_response)s, '
                                          '_order_id=>%(order_id)s, '
                                          '_order_number=>%(order_number)s, '
                                          '_address_id=>%(address_id)s ,'
                                          '_is_standard=>%(is_standard)s ,'
                                          '_quantity=>%(quantity)s, '
                                          '_user_id=>%(user_id)s, '
                                          '_coupon_id=>%(coupon_id)s )',
                                          args,
                                          'save payment success for paypal', True)

                    if result[0] == 200:
                        # send order detail mail to customer
                        result = run_db_query('select productname, totalamount,'
                                              'coupondiscount, userdiscount from public.fngetorderdetailsformail'
                                              '(%(order_id)s)', args, 'user info select from DB', True, True)
                        if result == 'error':
                            app.logger.debug('Error in sending order detail mail to customer')
                            # raise Exception
                        product_data = customer_order_details_helper(result)

                        send_email(secrets['CUSTOMER_ORDER_DETAILS_TEMPLATE'], {
                            "to_email": identity['email'],
                            "variables": {
                                "NAME": args['userName'],
                                "ADDRESS": args['userAddress'],
                                "ORDERNUMBER": "#" + str(args['order_number']),
                                "ORDERDATE": date.today().strftime("%m/%d/%Y"),
                                "PRODUCTIST": product_data['product_list'],
                                "TOTALAMOUNT": product_data['total_amount'],
                            }
                        })
                        return {
                                   'message': 'Payment successful ! You can check you order details from order section.'}, 200
                    else:
                        return {'message': 'Some error occurred while processing the payment.'
                                           ' If the money has been deducted, please wait'
                                           ' for sometime and check the status of your order.'}, 500
                else:
                    return {'message': 'The user is invalid, please login again'}, 401
            else:
                return {'message': 'Some error occurred while processing the payment.'
                                   ' If the money has been deducted, please wait'
                                   ' for sometime and check the status of your order.'}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Some error occurred while processing the payment.'
                               ' If the money has been deducted, please wait'
                               ' for sometime and check the status of your order.'}, 500


class PlaceOrderCOD(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            identity = get_jwt_identity()
            validation = order.validate_razorpay_paypal_cod_order(data)
            if validation['isValid']:
                if identity['id']:
                    args = {'_ser_id': 1, '_user_id': identity['id'],
                            'user_amount': data['amount'], 'order_id': data['orderId'],
                            'coupon_id': data['couponId'] if 'couponId' in data else None}
                    result = run_db_query('select _finaltotalvalue, status from '
                                          ' store.fncheckprice('
                                          '_user_id=>%(_user_id)s, '
                                          '_order_id=>%(order_id)s, '
                                          '_coupon_id=>%(coupon_id)s, '
                                          '_webtotalvalue=>%(user_amount)s )'
                                          , args, 'price check call', True)

                    if result == 'error':
                        raise Exception
                    elif result['status']:
                        result = run_db_query('select * from store.fncansendotp'
                                              '(%(_user_id)s)', args, 'user info select from DB', True)

                        if result == 'error':
                            raise Exception
                        if not result[0]:
                            return {'message': 'To many attempts, please try after 10 minutes.'}, 500
                        result = run_db_query('select mobno from PersonalInfoSelect'
                                              '(%(_user_id)s)', args, 'user info select from DB', True)
                        if result == 'error':
                            raise Exception

                        if not result:
                            return {"message": "user not found, login again"}, 500
                        mobile_number = result['mobno']
                        result = run_db_query('call store.spcodotp ('
                                              '_ser_id=>%(_ser_id)s, '
                                              '_user_id=>%(_user_id)s )',
                                              args, 'order details Update in DB', False)
                        if result == 'error':
                            raise Exception
                        # Sending OTP
                        conn = http.client.HTTPSConnection('api.msg91.com')
                        headers = {'content-type': 'application/json'}

                        conn.request('GET', '/api/v5/otp?'
                                            'authkey=346784A9nXIgTbv5faa2c51P1'
                                            '&template_id=5fab7dd9c7f9882608603eca'
                                            '&mobile=' + ''.join(e for e in mobile_number if e.isalnum())
                                     , headers=headers)
                        res = conn.getresponse()
                        data = res.read()
                        data = data.decode("UTF-8")
                        data = ast.literal_eval(data)
                        if data['type'] == 'error':
                            return {'message': 'OTP failed, try again.'}, 500
                        return {'message': 'OTP sent to mobile.', 'data': {'otp': 'sent'}}, 200
                    else:
                        return {'message': 'Price changed for one or more product. Getting the latest price'}, 203
                else:
                    return {'message': 'User Auth is missing.'}, 401
            else:
                return {'message': 'Error occurred, try again please.'}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Error occurred, please try again'}, 500


class ResendCODOTP(Resource):
    @jwt_required
    def get(self):
        try:
            identity = get_jwt_identity()
            if identity['id']:
                args = {'_ser_id': 1, '_user_id': identity['id']}
                result = run_db_query('select * from store.fncansendotp'
                                      '(%(_user_id)s)', args, 'user info select from DB', True)

                if result == 'error':
                    raise Exception
                if not result[0]:
                    return {'message': 'To many attempts, please try after 10 minutes.'}, 500

                result = run_db_query('select mobno from PersonalInfoSelect'
                                      '(%(_user_id)s)', args, 'user info select from DB', True)
                if result == 'error':
                    raise Exception

                if not result:
                    return {"message": "user not found, login again"}, 500
                mobile_number = result['mobno']
                result = run_db_query('call store.spcodotp ('
                                      '_ser_id=>%(_ser_id)s, '
                                      '_user_id=>%(_user_id)s )',
                                      args, 'order details Update in DB', False)
                if result == 'error':
                    raise Exception
                # Sending OTP
                conn = http.client.HTTPSConnection('api.msg91.com')
                headers = {'content-type': 'application/json'}

                conn.request('GET', '/api/v5/otp/retry?'
                                    'authkey=346784A9nXIgTbv5faa2c51P1'
                                    '&retrytype=text'
                                    '&mobile=' + ''.join(e for e in mobile_number if e.isalnum())
                             , headers=headers)
                res = conn.getresponse()
                data = res.read()
                data = data.decode("UTF-8")
                data = ast.literal_eval(data)

                if data['type'] == 'error':
                    # If max retry reached sending a new OTP
                    if data['message'] == 'OTP retry count maxed out':
                        conn.request('GET', '/api/v5/otp?'
                                            'authkey=346784A9nXIgTbv5faa2c51P1'
                                            '&template_id=5fab7dd9c7f9882608603eca'
                                            '&mobile=' + ''.join(e for e in mobile_number if e.isalnum())
                                     , headers=headers)
                        res = conn.getresponse()
                        data = res.read()
                        data = data.decode("UTF-8")
                        data = ast.literal_eval(data)
                        if data['type'] == 'error':
                            return {'message': 'OTP failed, try again'}, 500
                    else:
                        return {'message': 'OTP failed, try again'}, 500
                return {'message': 'OTP resent', 'data': {'otp': 'resent'}}, 200
            else:
                return {'message': 'User Auth is missing.'}, 401
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Error occurred, please try again'}, 500


class CheckCODStatus(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            identity = get_jwt_identity()
            validation = order.validate_cod_status(data)
            if validation['isValid']:
                if identity['id']:
                    today = date.today()
                    args = {'ser_id': 2, 'user_id': identity['id'], 'user_otp': data['otp'],
                            'order_id': data['orderId'],
                            'address_id': data['addressId'],
                            'userName': data['userName'],
                            'userAddress': data['userAddress'],
                            'coupon_id': data['couponId'] if 'couponId' in data else None,
                            'order_number': str(identity['id']) + str(int(round(time.time() * 1000)))}
                    # Getting mobile number from DB
                    result = run_db_query('select mobno from PersonalInfoSelect'
                                          '(%(user_id)s)', args, 'user info select from DB', True)

                    if result == 'error':
                        raise Exception

                    if not result:
                        return {"message": "user not found, login again"}, 500
                    mobile_number = result['mobno']
                    # Validating OTP
                    conn = http.client.HTTPSConnection("api.msg91.com")

                    conn.request("POST", "/api/v5/otp/verify?"
                                         "mobile=" + ''.join(e for e in mobile_number if e.isalnum()) +
                                 "&otp=" + args['user_otp'] +
                                 "&authkey=346784A9nXIgTbv5faa2c51P1")
                    res = conn.getresponse()
                    data = res.read()
                    data = data.decode("UTF-8")
                    data = ast.literal_eval(data)

                    if data['type'] != 'error':
                        result = run_db_query('call store.spcodotp ('
                                              '_ser_id=>%(ser_id)s, '
                                              '_user_id=>%(user_id)s, '
                                              '_address_id=>%(address_id)s, '
                                              '_order_number=>%(order_number)s, '
                                              '_order_id=>%(order_id)s, '
                                              '_coupon_id=>%(coupon_id)s )',
                                              args, 'Payment save for COD', False)
                        if result == 'error':
                            raise Exception

                        #send order detail mail to customer
                        result = run_db_query('select productname, totalamount,'
                                              'coupondiscount, userdiscount from public.fngetorderdetailsformail'
                                              '(%(order_id)s)', args, 'user info select from DB', True, True)
                        if result == 'error':
                            app.logger.debug('Error in sending order detail mail to customer')
                            # raise Exception
                        product_data = customer_order_details_helper(result)

                        send_email(secrets['CUSTOMER_ORDER_DETAILS_TEMPLATE'], {
                            "to_email": identity['email'],
                            "variables": {
                                "NAME": args['userName'],
                                "ADDRESS": args['userAddress'],
                                "ORDERNUMBER": "#" + str(args['order_number']),
                                "ORDERDATE": date.today().strftime("%m/%d/%Y"),
                                "PRODUCTIST": product_data['product_list'],
                                "TOTALAMOUNT": product_data['total_amount'],
                            }
                        })
                        return {'message': 'Payment Success'}, 200
                    else:
                        return {'message': 'OTP incorrect, please try again.'}, 500
                else:
                    return {'message': 'User Auth is missing.'}, 401
            else:
                return {'message': 'Validation error, retry again.'}
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Error occurred, please try again.'}, 500


class GetCustomerOrders(Resource):
    @jwt_required
    def get(self):
        try:
            identity = get_jwt_identity()
            if identity['id']:
                args = {
                    'offset': request.args.getlist('offset')[0],
                    'limit': request.args.getlist('limit')[0],
                    'user_id': identity['id']
                }

                # print(args)
                result = run_db_query('select order_id, order_totalprice, order_paymentdate, '
                                      ' payment_type_name, orderitems, order_number, coupon_value, user_discount'
                                      ' from store.order_view '
                                      ' where user_id =' + str(args['user_id']) + ' '
                                                                                  ' LIMIT ' + args[
                                          'limit'] + ' OFFSET ' + args['offset'],
                                      args, 'get customer orders', True, True)

                if result == 'error':
                    raise Exception
                return {"message": "get productlist for customer", 'data': customer_orders(result)}, 200
            else:
                return {'message': 'Invalid Auth'}, 401
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'get productlist for customer error'}, 500


class GetAdminOrders(Resource):
    @admin_required
    def get(self):
        try:
            identity = get_jwt_identity()
            if identity['id']:
                args = {
                    'user_id': request.args.getlist('userId')[0]
                }
                user_clause = ''
                if args['user_id'] != '0':
                    user_clause = ' where user_id =' + str(args['user_id'])
                # print(args)
                result = run_db_query('select order_id, order_totalprice, order_paymentdate, '
                                      ' payment_type_name, orderitems, order_number, userdetails, '
                                      'razorpay_payment_id, paypal_response, standard_shipping, coupon_value, user_discount '
                                      ' from store.customer_order_view ' +
                                      user_clause, args, 'get customer orders', True, True)
                if result == 'error':
                    raise Exception
                return {"message": "get orders for admin", 'data': admin_orders(result)}, 200
            else:
                return {'message': 'Invalid Auth'}, 401
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'get productlist for customer error'}, 500


class CustomerReturn(Resource):
    @jwt_required
    def post(self):
        try:
            identity = get_jwt_identity()
            if identity['id']:
                data = request.get_json()
                return_validation = customer_returns(data)
                if return_validation['isValid']:
                    args = {'ser': 1, 'order_detail_id': data['orderDetailsId'], 'return_reason': data['returnReason']}

                    result = run_db_query('call store.spReturnUpdate ('
                                          '_ser=>%(ser)s, '
                                          '_orderdetailid=>%(order_detail_id)s )',
                                          args, 'return flags added or changed  in DB', False)
                    if result == 'error':
                        raise Exception
                    # send customer email
                    send_email(secrets['CUSTOMER_ORDER_RETURN_CANCEL_EMAIL_TEMPLATE'], {
                        "to_email": identity['email'],
                        "variables": {
                            "NAME": data['userName'],
                            "ORDERNUMBER": "#" + str(data['orderNumber']),
                            "PRODUCTNAME": data['productName']
                        }
                    })
                    #send admin email
                    send_email(secrets['ADMIN_ORDER_RETURN_CANCEL_EMAIL_TEMPLATE'], {
                        "to_email": secrets['ADMIN_EMAIL'],
                        "variables": {
                            "ORDERNUMBER": "#" + str(data['orderNumber']),
                            "PRODUCTNAME": data['productName'],
                            "REASON": data['returnReason']
                        }
                    })
                    return {'message': 'Return process initialed'}, 200
                else:
                    return {'message': 'Payload incorrect'}, 500
            else:
                return {'message': 'User Invalid, login again'}, 401
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'error while processing return'}, 500


class OrderDataForCsv(Resource):
    @admin_required
    def get(self):
        try:
            result = run_db_query('select orderdetailid, prod_category, prod_name, '
                                  ' addr_state, qty, paymenttype, paymentmode, '
                                  'originaltotal, userdiscount, coupondiscount, orderreturned '
                                  ' from store.fngetorderdatacsv() ', {},
                                  'get order data for csv', True, True)
            if result == 'error':
                raise Exception
            return {"message": "success get order data for csv", "data":order_data_csv_transformer(result)}, 200
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'get order data for csv error'}, 500