import datetime
from flask_restful import Resource
from authserver import bcrypt, admin_required
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt

from authserver.transformers.shipment_transformer import shipment_transformer
from authserver.utils.send_email import send_email
from authserver.validation_schemas import shipper, shipment
from authserver.connection import run_db_query
from secrets import secrets


class ShipperDetails(Resource):
    def get(self):
        try:
            args = {}
            result = run_db_query('select shipr_id, shipr_name, shipr_link '
                                  'from store.fnshipperSelect()', args, 'shipper info select from DB', True, True)
            if result == 'error':
                raise Exception

            return {"message": "shipper info select success", 'data': shipment_transformer(result)}, 200
        except Exception as e:
            print(e)
            return {'message': 'shipper select error'}, 500

    @admin_required
    def post(self):
        data = request.get_json()
        print(data)
        shipper_validation = shipper.validate_shipper(data)
        if shipper_validation['isValid']:
            try:
                args = {'ser': 1, 'shipper_name': data['shipper_name'],
                        'shipper_link': data['shipper_link'], 'shipper_id': data['shipper_id'],
                        'delete_flag': data['delete_flag']
                        }

                if args['shipper_id'] != 0 and not args['delete_flag']:
                    args['ser'] = 2
                elif args['shipper_id'] != 0 and args['delete_flag']:
                    args['ser'] = 3
                result = run_db_query('call store.spshipperinsertupdatedelete ('
                                      '_ser=>%(ser)s, '
                                      '_shippername=>%(shipper_name)s, '
                                      '_shipperlink=>%(shipper_link)s,'
                                      ' _shipperid=>%(shipper_id)s )',
                                      args, 'Admin enter update or delete shipper details in DB', False)
                print(result)
                if result == 'error':
                    raise Exception
                return {'message': 'shipper details saved'}, 200
            except Exception as e:
                print(e)
                return {'message': 'shipper details insert,update,delete Error'}, 500
        else:
            return {'message': 'shipper field validation error'}, 500


class ShipmentDetails(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        print(data)
        shipment_validation = shipment.validate_shipment(data)
        if shipment_validation['isValid']:
            try:
                args = {'ser': 1, 'shipment_track_no': data['trackingNumber'],
                        'shipment_date': data['shippingDate'] if 'shippingDate' in data else None,
                        'shipment_delivery_date': data['deliveryDate'] if 'deliveryDate' in data else None,
                        'shipper_id': int(data['shipper']) if 'shipper' in data else None,
                        'shipment_id': data['shipmentId'] if 'shipmentId' in data else None,
                        'delete_flag': data['deleteFlag'] if 'deleteFlag' in data else False,
                        'return_status': data['returnStatus'] if 'returnStatus' in data else None,
                        'payment_returned': data['paymentReturned'] if 'paymentReturned' in data else None,
                        'order_detail_id': data['orderDetailId'] if 'orderDetailId' in data else None
                        }

                if args['shipment_date']:
                    args['shipment_date'] = datetime.datetime.strptime(args['shipment_date'], '%Y-%m-%d').isoformat()
                if args['shipment_delivery_date']:
                    args['shipment_delivery_date'] = datetime.datetime.strptime(args['shipment_delivery_date'],
                                                                                '%Y-%m-%d').isoformat()

                if args['shipment_id'] != '0' and not args['delete_flag']:
                    args['ser'] = 2
                elif args['shipment_id'] != '0' and args['delete_flag']:
                    args['ser'] = 3
                result = run_db_query('call store.spshipmentsinsertupdatedelete ('
                                      '_ser=>%(ser)s, '
                                      '_shipperid=>%(shipper_id)s, '
                                      '_shipmenttracknumber=>%(shipment_track_no)s, '
                                      '_orderdetailid=>%(order_detail_id)s, '
                                      '_shipmentdate=>%(shipment_date)s,'
                                      '_shipmentdeliverydate=>%(shipment_delivery_date)s,'
                                      '_shipmentid=>%(shipment_id)s )',
                                      args, 'Admin enter update or delete shipment details in DB', False)
                if result == 'error':
                    raise Exception

                if args['return_status'] or args['payment_returned']:
                    args['ser'] = 2
                    result = run_db_query('call store.spReturnUpdate ('
                                          '_ser=>%(ser)s, '
                                          '_orderdetailid=>%(order_detail_id)s, '
                                          '_returnstatus=>%(return_status)s, '
                                          '_paymentstatus=>%(payment_returned)s )',
                                          args, 'return flags added or changed  in DB', False)
                    if result == 'error':
                        raise Exception

                if data['sendTrackingEmail'] and data["trackingNumber"] \
                        and data['customerEmail'] and data['orderNumber'] and data['customerName']:
                    send_email(secrets['PRODUCT_SHIPPED_TEMPLATE'], {
                        "to_email": data['customerEmail'],
                        "variables": {
                            "NAME": data['customerName'],
                            "ORDERNUMBER": data['orderNumber'],
                            "TRACKING URL": data["trackingNumber"]
                        }
                    })
                return {'message': 'Shipment details saved.'}, 200
            except Exception as e:
                print(e)
                return {'message': 'Some error occurred, try again.'}, 500
        else:
            return {'message': 'shipper field validation error'}, 500
