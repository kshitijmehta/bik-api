def customer_orders(data):
    res = []
    for orders_obj in data:
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
                'categoryId': items['prod_category_id'],
                'shipmentDetails': {
                    'shipper': items['shipper_id'],
                    'shippingDate': items['shipment_date'],
                    'trackingNumber': items['shipment_trackingnumber'],
                    'deliveryDate': items['shipment_deliverydate'],
                    'returnStatus': items['orderdetail_return'],
                    'paymentReturned': items['orderdetail_returnpayment'],
                }
            }))
        print(order_items)
        res.append({
            'orderId': orders_obj['order_id'],
            'totalPrice': str(orders_obj['order_totalprice']),
            'paymentDate': str(orders_obj['order_paymentdate']),
            'paymentMode': orders_obj['payment_type_name'],
            'orderNumber': orders_obj['order_number'],
            'orderItems': order_items
        })
    return res
