def add_to_cart_transformer(data):
    return {
        'orderId': data['order_id'],
        'cartId': data['orderdetail_id'],
        'productDetailId': data['prod_detail_id'],
        'productPrice': data['orderdetail_price'],
        'currency_type': data['orderdetail_price_id'],
        'shipmentId': data['shipment_id'],
        'productQuantity': data['orderdetail_qty'],
        'totalPrice': data['orderdetail_linetotal']
    }


def get_cart_transformer(data):
    res = []
    for cart_obj in data:
        res.append({
            'orderId': cart_obj['order_id'],
            'cartId': cart_obj['orderdetail_id'],
            'currency_type': cart_obj['orderdetail_price_id'],
            'productName': cart_obj['prod_name'],
            'productImage': cart_obj['prod_img_name'],
            'productImagePath': cart_obj['prod_img_path'],
            'productPrice': cart_obj['orderdetail_price'],
            'productQuantity': cart_obj['orderdetail_qty'],
            'totalPrice': cart_obj['orderdetail_linetotal'],
            'subcategory': cart_obj['ps_name'],
            'productId': cart_obj['prod_id'],
            'productDetailId': cart_obj['pd_id'],
            'availableQuantity': cart_obj['prod_qty']
        })
    return res


def update_cart_transformer(data):
    return {
        'cartId': data['orderdetail_id'],
        'productDetailId': data['prod_detail_id'],
        'productQuantity': data['orderdetail_qty'],
        'productPrice': data['orderdetail_price'],
        'currency_type': data['orderdetail_price_id'],
        'totalPrice': data['orderdetail_linetotal']
    }
