from authserver.transformers.login_transformer import login_transformer


def admin_orders(data):
    res = []
    for orders_obj in data:
        print(orders_obj['userdetails'])
        order_items = []
        for items in orders_obj['orderitems']:
            order_items.append(({
                'orderDetailId': items['orderdetail_id'],
                'productDetailId': items['prod_detail_id'],
                'productName': items['prod_name'],
                'productId': items['prod_id'],
                'quantity': items['orderdetail_qty'],
                'currency': items['orderdetail_price_id'],
                'productPrice': str(items['orderdetail_price']),
                'productImage': items['prod_img_path'],
                'shipmentDetails': {
                    'shipmentId': items['shipment_id'],
                    'shipper': items['shipper_id'],
                    'shippingDate': items['shipment_date'],
                    'trackingNumber': items['shipment_trackingnumber'],
                    'deliveryDate': items['shipment_deliverydate'],
                    'returnStatus': items['orderdetail_return'],
                    'paymentReturned': items['orderdetail_returnpayment'],
                }
            }))
        res.append({
            'orderId': orders_obj['order_id'],
            'totalPrice': str(orders_obj['order_totalprice']),
            'paymentDate': str(orders_obj['order_paymentdate']),
            'paymentMode': orders_obj['payment_type_name'],
            'orderNumber': orders_obj['order_number'],
            'orderItems': order_items,
            'razorpayPaymentId': orders_obj['razorpay_payment_id'],
            'paypalResponse': orders_obj['paypal_response'],
            'standardShipping': orders_obj['standard_shipping'],
            'userDetails': login_transformer(orders_obj['userdetails'][0], orders_obj['userdetails'][0]['emailid'])
        })
    return res
