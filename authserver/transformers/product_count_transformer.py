def product_count_transformer(data):
    res = []
    for product_obj in data:
        res.append({
            'subcategoryId': product_obj['prod_subcateg_id'],
            'subcategoryName': product_obj['prod_subacateg_name'],
            'colourId': product_obj['prod_colour'],
            'colourName': product_obj['colour_value'],
            'sizeId': product_obj['prod_size'].split(","),
            # 'sizeName': product_obj['size_name'],
            # 'count': product_obj['prod_count']
        })
    return res
