def product_size_transformer(data):
    res = []
    for size_obj in data:
        res.append({
            'sizeId': size_obj['s_id'],
            'code': size_obj['s_code'],
            'value': size_obj['s_value'],
            'productCategory': size_obj['prod_category'],
            'productCategoryName': size_obj['prod_categoryname'],
        })
    return res
