def product_coupon_transformer(data):
    res = []
    for colour_obj in data:
        res.append({
            'couponId': colour_obj['cp_id'],
            'code': colour_obj['cp_code'],
            'value': colour_obj['cp_value']
        })
    return res
