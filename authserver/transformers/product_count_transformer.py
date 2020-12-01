def product_count_transformer(data):
    res = []
    for product_obj in data:
        res.append({
            'subcategoryId': product_obj['prod_subcategory_id'],
            'subcategoryName': product_obj['prod_subcategroy_name'],
            'colourId': product_obj['colour_id'],
            'colourName': product_obj['colour_name'],
            'sizeId': product_obj['size_id'],
            'sizeName': product_obj['size_name'],
            'count': product_obj['prod_count']
        })
    return res
