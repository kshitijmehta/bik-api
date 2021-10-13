import math


def order_data_csv_transformer(data):
    res = []
    for size_obj in data:
        mrp_gst = calculate_gst_mrp(int(size_obj['originaltotal']),
                                    int(size_obj['userdiscount']) if size_obj['userdiscount'] else None,
                                    int(size_obj['coupondiscount']) if size_obj['coupondiscount'] else None,
                                    size_obj['prod_category'])
        res.append({
            'orderDetailId': size_obj['orderdetailid'],
            'productCategory': size_obj['prod_category'],
            'name': size_obj['prod_name'],
            'state': size_obj['addr_state'],
            'quantity': size_obj['qty'],
            'paymentType': 'INR' if size_obj['paymenttype'] == 1 else 'USD',
            'paymentMode': size_obj['paymentmode'],
            'mrp': mrp_gst['mrp'],
            'gst': mrp_gst['gst'],
            'totalAmount': str(size_obj['originaltotal']),
            'orderReturned': size_obj['orderreturned'] if size_obj['orderreturned'] else 'No',
        })
    return res


def calculate_discount(original_price, user_discount, coupon):
    discounted_price = original_price
    if user_discount:
        discounted_price = math.ceil(discounted_price - (discounted_price * (user_discount / 100)))
    if coupon:
        discounted_price = math.ceil(discounted_price - (discounted_price * (coupon / 100)))
    return math.ceil(discounted_price)


def calculate_gst_mrp(original_price, coupon, user_discount, category):
    discounted_price = calculate_discount(original_price, coupon, user_discount)
    mrp = discounted_price / (1 + (get_gst_rate(category)/100))
    gst = discounted_price - mrp

    return {
        'mrp': math.floor(mrp),
        'gst': math.ceil(gst)
    }


def get_gst_rate(category):
    if str(category).lower() == 'footwear' or str(category).lower() == 'lingerie':
        return 5
    elif str(category).lower() == 'home essential' or str(category).lower() == 'cosmetics':
        return 18
    elif str(category).lower() == 'fashion accessories':
        return 3
    else:
        return 0
