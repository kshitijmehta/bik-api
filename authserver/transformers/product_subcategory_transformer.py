def product_subcategory_transformer(data):
    res = []
    for sub_category in data:
        res.append({
            'subCategoryId': sub_category['ps_id'],
            'code': sub_category['ps_name'],
            'value': sub_category['ps_desc'],
            'productCategoryId': sub_category['cat_id'],
            'productCategoryName': sub_category['cat_name'],
        })
    return res
