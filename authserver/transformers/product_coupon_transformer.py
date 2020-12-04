def product_coupon_transformer(data):
    res = []
    for coupon_obj in data:
        res.append(coupon_format(coupon_obj))
    return res


def coupon_format(data):
    return{
        'couponId': data['cp_id'],
        'code': data['cp_code'],
        'value': data['cp_value']
    }
